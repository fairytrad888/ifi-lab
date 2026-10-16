"""Forward test: paper-trade every Daily playbook signal with the backtest's exact rules,
score live results against the backtest, detect verdict drift, and match journal trades to signals.

Rules are not re-implemented here: each signal is run through backtest.simulate(), so the paper trade
uses the same next-open fill, skip-if-open-below-structure, stop, 3R target, max hold and costs.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from . import backtest as bt
from .data import ROOT

PAPER = ROOT / "logs" / "paper_trades.csv"
SCOREBOARD = ROOT / "logs" / "scoreboard.json"
DRIFT = ROOT / "state" / "drift.json"
SENT = ROOT / "state" / "alerts_sent.json"
RESULTS = ROOT / "reports" / "results"


def _clean(o):
    if isinstance(o, dict):
        return {k: _clean(v) for k, v in o.items()}
    if isinstance(o, float) and np.isnan(o):
        return None
    return o


def _exit_rule(c) -> str:
    return "X2_target2R" if c.get("playbook", {}).get("target_r", 3) == 2 else "X3_target3R"


PLAYBOOK_NAMES = {"E4_anchor_reclaim": "Playbook E4 anchor reclaim", "E1_trigger_with_trend": "Playbook E1 trigger with trend"}
PRELIVE_BARS = 250  # pre-live history paper-traded for reference and to carry open trades into the live period


def _fill_bar_trade(x: pd.DataFrame, i: int, ex: str, cost: float, r_mult: float):
    """A signal whose fill bar is the newest completed bar (i + 1 == n - 1). backtest.simulate()
    only scans signals with t < n - 2, so it never sees this case; apply its rules to that one bar.
    Returns None when the trade is skipped (opened below structure / no risk), else a dict."""
    o, h, l, c = (float(x[k].iloc[i + 1]) for k in ("open", "high", "low", "close"))
    low5 = float(x["low"].iloc[max(i - 4, 0):i + 1].min())
    atr = float(x["atr"].iloc[i])
    if np.isnan(atr) or np.isnan(o):
        return None
    stop = low5 - 0.5 * atr
    risk = o - stop
    if o < low5 or not (risk > 0):
        return None
    target = o + bt.EXITS[ex].get("target", np.inf) * risk if "target" in bt.EXITS[ex] else np.inf
    mfe = mae = 0.0
    if l <= stop:  # same order as simulate(): stop first on the fill bar (exit at the stop level)
        px, reason = stop, "stop"
    else:
        mfe, mae = (h - o) / risk, (l - o) / risk
        if h >= target:
            px, reason = target, "target"
        else:
            px, reason = c, "open_at_end"
    r = (px - o) / risk - cost * (o + px) / risk
    return dict(entry_date=x.index[i + 1], exit_date=x.index[i + 1], bars=1, r=r, mfe_r=mfe, mae_r=mae,
                reason=reason, fill=o, stop=stop, target=o + r_mult * risk)


def paper_trades(log: pd.DataFrame, frames: dict, c: dict, ctx: dict | None = None) -> pd.DataFrame:
    """Paper-trade the Daily playbook exactly as the backtest does (v1.3.2).

    Signals come from backtest.setups() on each symbol's completed Daily bars, and ALL signals of a
    symbol/setup go through ONE backtest.simulate() call, so the forward test keeps the backtest's
    sequencing: a new signal is skipped while that symbol/setup already has a trade open (including
    trades opened before the forward-test start). `log` is kept for the call signature only.
    v1.4: `frames` may hold the full universe; with `ctx` every row also carries context tags (allocation.tags)."""
    from .allocation import tags as context_tags
    ex = _exit_rule(c)
    pb = c.get("playbook", {})
    r_mult = pb.get("target_r", 3)
    start = pd.Timestamp(str(c.get("forward_test", {}).get("start", "2100-01-01")))
    etfs = set(c["etfs"])
    ext = set(c.get("_extended", []))      # v1.5: extended (paper-only) universe
    rows = []
    for (tf, sym), x in frames.items():
        if tf != "daily" or x is None or len(x) < 3:
            continue
        sets = bt.setups(x)
        cost = c["costs"]["etf"] if sym in etfs else c["costs"]["stock"]
        first = max(int(np.searchsorted(x.index.values, np.datetime64(start))) - PRELIVE_BARS, 0)
        low5 = x["low"].rolling(5).min()
        for su in pb.get("setups", []):
            if su not in sets:
                continue
            ent = sets[su].copy()
            ent.iloc[:first] = False
            sig_idx = np.flatnonzero(ent.to_numpy())
            if not len(sig_idx):
                continue
            trades = bt.simulate(sym, x, ent, su, ex, cost)
            pos = {x.index.get_loc(t.entry_date): t for t in trades}
            spans = [(x.index.get_loc(t.entry_date), x.index.get_loc(t.exit_date), t.reason) for t in trades]
            for i in sig_idx:
                bar = x.index[i]
                sid = f"daily|{sym}|{bar:%Y-%m-%d %H:%M}|{PLAYBOOK_NAMES.get(su, su)}"
                base = dict(signal_id=sid, symbol=sym, setup=su, signal_bar=bar, oos=bool(bar >= start),
                            universe="etf" if sym in etfs else "stock", group="extended" if sym in ext else "core")
                if ctx is not None:
                    base.update(context_tags(x, i, sym, ctx, live=bool(bar >= start)))
                stop = low5.iloc[i] - 0.5 * x["atr"].iloc[i]
                in_trade = any(e0 <= i and (i < e1 or why == "open_at_end") for e0, e1, why in spans)
                if (i + 1) in pos:
                    t = pos[i + 1]
                    fill = x["open"].iloc[i + 1]
                    risk = fill - stop
                    is_open = t.reason == "open_at_end"
                    rows.append({**base, "status": "open" if is_open else "closed",
                                 "exit_reason": "" if is_open else t.reason,
                                 "fill_date": t.entry_date, "fill": round(fill, 4), "stop": round(stop, 4),
                                 "target": round(fill + r_mult * risk, 4),
                                 "exit_date": pd.NaT if is_open else t.exit_date, "bars": t.bars,
                                 "r": round(t.r, 3), "mfe_r": round(t.mfe_r, 3), "mae_r": round(t.mae_r, 3)})
                elif in_trade:
                    rows.append({**base, "status": "skipped", "exit_reason": "trade already open (backtest rule)",
                                 "stop": round(stop, 4)})
                elif i + 1 == len(x) - 1:  # fill bar is the newest completed bar (not covered by simulate)
                    t = _fill_bar_trade(x, i, ex, cost, r_mult)
                    if t is None:
                        rows.append({**base, "status": "cancelled", "fill_date": x.index[i + 1],
                                     "fill": round(x["open"].iloc[i + 1], 4), "stop": round(stop, 4),
                                     "exit_reason": "opened below structure"})
                    else:
                        is_open = t["reason"] == "open_at_end"
                        rows.append({**base, "status": "open" if is_open else "closed",
                                     "exit_reason": "" if is_open else t["reason"], "fill_date": t["entry_date"],
                                     "fill": round(t["fill"], 4), "stop": round(t["stop"], 4),
                                     "target": round(t["target"], 4),
                                     "exit_date": pd.NaT if is_open else t["exit_date"], "bars": 1,
                                     "r": round(t["r"], 3), "mfe_r": round(t["mfe_r"], 3), "mae_r": round(t["mae_r"], 3)})
                        if is_open:
                            spans.append((i + 1, len(x) - 1, "open_at_end"))
                elif i + 1 >= len(x):
                    rows.append({**base, "status": "pending", "stop": round(stop, 4),
                                 "cancel_if_open_below": round(low5.iloc[i], 4)})
                else:
                    rows.append({**base, "status": "cancelled", "fill_date": x.index[i + 1],
                                 "fill": round(x["open"].iloc[i + 1], 4), "stop": round(stop, 4),
                                 "exit_reason": "opened below structure"})
    pt = pd.DataFrame(rows)
    if not pt.empty:
        pt = pt.sort_values(["signal_bar", "symbol"]).reset_index(drop=True)
        pt["tag_signals_same_day"] = pt.groupby("signal_bar")["signal_id"].transform("size")
        PAPER.parent.mkdir(parents=True, exist_ok=True)
        pt.to_csv(PAPER, index=False)
    return pt


def _ref(setup: str, ex: str) -> dict:
    out = {}
    for uni in ("etfs", "stocks"):
        f = RESULTS / f"P1_daily_{uni}.csv"
        if not f.exists():
            continue
        d = pd.read_csv(f)
        m = d[(d["setup"] == setup) & (d["exit"] == ex)]
        if len(m):
            r = m.iloc[0]
            out[uni] = dict(n=int(r["n"]), expectancy=float(r["expectancy"]), ci_low=float(r["ci_low"]),
                            verdict=str(r["verdict"]))
    return out


def scoreboard(pt: pd.DataFrame, c: dict) -> dict:
    ex = _exit_rule(c)
    min_n = int(c.get("forward_test", {}).get("min_trades_for_status", 20))
    board = {}
    for su in c.get("playbook", {}).get("setups", []):
        d = pt[pt["setup"] == su] if not pt.empty else pd.DataFrame(columns=["oos", "status", "r"])
        live = d[(d["oos"]) & (d["status"] == "closed")]
        pre = d[(~d["oos"].astype(bool)) & (d["status"] == "closed")]
        ref = _ref(su, ex)
        lows = [v["ci_low"] for v in ref.values()]
        ns = [v["n"] for v in ref.values()]
        ref_exp = float(np.average([v["expectancy"] for v in ref.values()], weights=ns)) if ns else np.nan
        ref_low = min(lows) if lows else np.nan
        n = len(live)
        exp = float(live["r"].mean()) if n else np.nan
        ci = (np.nan, np.nan)
        if n >= 5:
            rng = np.random.default_rng(1)
            bs = rng.choice(live["r"].to_numpy(), size=(2000, n)).mean(axis=1)
            ci = tuple(float(q) for q in np.quantile(bs, [0.025, 0.975]))
        if n < min_n:
            status = f"COLLECTING ({n}/{min_n})"
        elif exp < 0 and exp < ref_low:
            status = "STOP"
        elif exp < ref_low:
            status = "WATCH"
        else:
            status = "ON TRACK"
        board[su] = dict(status=status, live_n=n, live_expectancy=exp, live_ci_low=ci[0], live_ci_high=ci[1],
                         live_win_rate=float((live["r"] > 0).mean()) if n else np.nan,
                         live_total_r=float(live["r"].sum()) if n else 0.0,
                         open_trades=int(((d["oos"]) & (d["status"] == "open")).sum()) if len(d) else 0,
                         prelive_n=len(pre), prelive_expectancy=float(pre["r"].mean()) if len(pre) else np.nan,
                         ref_expectancy=ref_exp, ref_ci_low=ref_low, ref=ref)
    SCOREBOARD.write_text(json.dumps(_clean(board), indent=1))
    return board


def drift(c: dict) -> dict:
    ex = _exit_rule(c)
    out = {}
    for su in c.get("playbook", {}).get("setups", []):
        ref = _ref(su, ex)
        ok = all(v["verdict"].startswith("ADOPT") for v in ref.values()) and len(ref) == 2
        out[su] = dict(ok=bool(ok), etfs=ref.get("etfs", {}).get("verdict", "missing"),
                       stocks=ref.get("stocks", {}).get("verdict", "missing"))
    DRIFT.parent.mkdir(parents=True, exist_ok=True)
    DRIFT.write_text(json.dumps(out, indent=1))
    return out


def match_journal(trades: pd.DataFrame | None, pt: pd.DataFrame) -> dict:
    """Pair journal trades with paper trades (same symbol, fill within 3 days) to measure execution."""
    if trades is None or trades.empty or pt.empty:
        return {}
    live = pt[(pt["oos"]) & (pt["status"].isin(["open", "closed"]))].copy()
    if live.empty:
        return {"matched": 0}
    live["fill_date"] = pd.to_datetime(live["fill_date"].astype(str), format="ISO8601")
    used, slips, gaps = set(), [], []
    for _, t in trades.iterrows():
        cand = live[(live["symbol"] == t["symbol"]) &
                    ((live["fill_date"] - pd.Timestamp(t["date"])).abs() <= pd.Timedelta(days=3))]
        cand = cand[~cand.index.isin(used)]
        if cand.empty:
            continue
        p = cand.iloc[0]
        used.add(cand.index[0])
        risk = p["fill"] - p["stop"]
        if risk > 0:
            slips.append((t["entry"] - p["fill"]) / risk)
        if p["status"] == "closed" and pd.notna(t.get("r")):
            gaps.append(t["r"] - p["r"])
    taken_pool = live[live["fill_date"] >= pd.to_datetime(trades["date"]).min()] if len(trades) else live
    return {"matched": len(used), "journal_trades": int(len(trades)),
            "signals_since_first_journal_trade": int(len(taken_pool)),
            "taken_pct": float(len(used) / len(taken_pool)) if len(taken_pool) else None,
            "avg_entry_slippage_r": float(np.mean(slips)) if slips else None,
            "avg_r_gap_vs_paper": float(np.mean(gaps)) if gaps else None}


def alert_lines(pt: pd.DataFrame, board: dict, dr: dict) -> list[str]:
    """Lines for changes since the last run. State is always updated so alerts never pile up."""
    prev = json.loads(SENT.read_text()) if SENT.exists() else {}
    first_run = not prev
    lines = []
    cur_paper = {r.signal_id: r.status for r in pt.itertuples()} if not pt.empty else {}
    for r in (pt.itertuples() if not pt.empty else []):
        old = prev.get("paper", {}).get(r.signal_id)
        if first_run or old == r.status or not r.oos:
            continue
        if r.status == "open" and old in (None, "pending"):
            lines.append(f"Paper fill: {r.symbol} {r.setup.split('_')[0]} @ {r.fill} stop {r.stop} target {r.target}")
        elif r.status == "closed":
            lines.append(f"Paper exit: {r.symbol} {r.setup.split('_')[0]} {r.exit_reason} {r.r:+.2f}R")
        elif r.status == "cancelled":
            lines.append(f"Paper cancelled: {r.symbol} opened below structure")
        elif r.status == "skipped":
            lines.append(f"Paper skipped: {r.symbol} {r.setup.split('_')[0]} (a trade from this setup is already open)")
    for su, b in board.items():
        old = prev.get("status", {}).get(su)
        if not first_run and old and old != b["status"] and not b["status"].startswith("COLLECTING"):
            le = b.get("live_expectancy")
            le_txt = "–" if le is None or (isinstance(le, float) and np.isnan(le)) else f"{le:+.2f}R"
            lines.insert(0, f"⚠ Risk tier {su}: {old} -> {b['status']} (live {le_txt}, n={b['live_n']})")
    for su, d in dr.items():
        old = prev.get("drift", {}).get(su)
        if not first_run and old is not None and old != d["ok"]:
            lines.insert(0, f"⚠ Drift {su}: {'back to ADOPT' if d['ok'] else 'lost ADOPT'} (ETFs {d['etfs']}, stocks {d['stocks']})")
    SENT.parent.mkdir(parents=True, exist_ok=True)
    SENT.write_text(json.dumps({"paper": cur_paper, "status": {k: v["status"] for k, v in board.items()},
                                "drift": {k: v["ok"] for k, v in dr.items()},
                                "updated": datetime.now(timezone.utc).isoformat()}, indent=1))
    return lines
