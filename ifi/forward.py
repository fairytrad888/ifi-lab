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


def paper_trades(log: pd.DataFrame, frames: dict, c: dict) -> pd.DataFrame:
    if log.empty or "family" not in log:
        return pd.DataFrame()
    ex = _exit_rule(c)
    r_mult = c.get("playbook", {}).get("target_r", 3)
    start = pd.Timestamp(str(c.get("forward_test", {}).get("start", "2100-01-01")))
    etfs = set(c["etfs"])
    sig = log[(log["family"] == "Playbook") & (log["tf"] == "daily")]
    rows = []
    for e in sig.itertuples():
        x = frames.get(("daily", e.symbol))
        bar = pd.Timestamp(e.bar)
        if x is None or bar not in x.index:
            continue
        i = x.index.get_loc(bar)
        setup = getattr(e, "setup", None)
        if not isinstance(setup, str):
            setup = "E4_anchor_reclaim" if "E4" in str(e.event) else "E1_trigger_with_trend"
        base = dict(signal_id=e.id, symbol=e.symbol, setup=setup, signal_bar=bar, oos=bool(bar >= start))
        if i + 1 >= len(x):
            rows.append({**base, "status": "pending"})
            continue
        low5 = x["low"].iloc[max(i - 4, 0):i + 1].min()
        stop = low5 - 0.5 * x["atr"].iloc[i]
        fill = x["open"].iloc[i + 1]
        ent = pd.Series(False, index=x.index)
        ent.iloc[i] = True
        cost = c["costs"]["etf"] if e.symbol in etfs else c["costs"]["stock"]
        tr = bt.simulate(e.symbol, x, ent, setup, ex, cost)
        if not tr:
            rows.append({**base, "status": "cancelled", "fill_date": x.index[i + 1], "fill": round(fill, 4),
                         "stop": round(stop, 4), "exit_reason": "opened below structure"})
            continue
        t = tr[0]
        risk = fill - stop
        is_open = t.reason == "open_at_end"
        rows.append({**base, "status": "open" if is_open else "closed", "exit_reason": "" if is_open else t.reason,
                     "fill_date": t.entry_date, "fill": round(fill, 4), "stop": round(stop, 4),
                     "target": round(fill + r_mult * risk, 4), "exit_date": pd.NaT if is_open else t.exit_date,
                     "bars": t.bars, "r": round(t.r, 3), "mfe_r": round(t.mfe_r, 3), "mae_r": round(t.mae_r, 3)})
    pt = pd.DataFrame(rows)
    if not pt.empty:
        pt = pt.sort_values("signal_bar").reset_index(drop=True)
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
    for su, b in board.items():
        old = prev.get("status", {}).get(su)
        if not first_run and old and old != b["status"] and not b["status"].startswith("COLLECTING"):
            lines.insert(0, f"⚠ Scoreboard {su}: {old} -> {b['status']} (live {b['live_expectancy']:+.2f}R, n={b['live_n']})")
    for su, d in dr.items():
        old = prev.get("drift", {}).get(su)
        if not first_run and old is not None and old != d["ok"]:
            lines.insert(0, f"⚠ Drift {su}: {'back to ADOPT' if d['ok'] else 'lost ADOPT'} (ETFs {d['etfs']}, stocks {d['stocks']})")
    SENT.parent.mkdir(parents=True, exist_ok=True)
    SENT.write_text(json.dumps({"paper": cur_paper, "status": {k: v["status"] for k, v in board.items()},
                                "drift": {k: v["ok"] for k, v in dr.items()},
                                "updated": datetime.now(timezone.utc).isoformat()}, indent=1))
    return lines
