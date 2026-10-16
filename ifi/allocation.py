"""v1.4 allocation ladder, safety nets, process health and context tags (IFI_Lab_v1.4_Design.md).

Evidence and money are separate: every playbook signal is paper-traded forever (forward.py); this module
only decides how much RISK each setup deserves from the evidence so far.

  posterior mean = (N0 * haircut * backtest R + live total R) / (N0 + live n)
  P(edge > 0)    = Phi(posterior mean / (sigma / sqrt(N0 + live n)))
  risk           = tier(P), then x breaker multiplier (1, 0.5 or 0)
"""
from __future__ import annotations

import json
import math

import numpy as np
import pandas as pd
import yaml

from .data import ROOT

RESULTS = ROOT / "reports" / "results"
ALLOC = ROOT / "logs" / "allocation.json"
RISK_AT_FILL = ROOT / "logs" / "risk_at_fill.json"
HEALTH = ROOT / "logs" / "health.json"
PB_EXIT = "X3_target3R"


def cfg14() -> dict:
    f = ROOT / "config_v14.yaml"
    return yaml.safe_load(f.read_text()) if f.exists() else {}


def _phi(z: float) -> float:
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


# ------------------------------------------------------------------ backtest prior
_READ: dict = {}


def _read_trades(f) -> pd.DataFrame:
    """The backtest trade file, read once per run (cached by path and modification time)."""
    key = (str(f), f.stat().st_mtime_ns)
    if key not in _READ:
        _READ.clear() if len(_READ) > 4 else None
        _READ[key] = pd.read_csv(f)
    return _READ[key]


def backtest_trades(setup: str, ex: str = PB_EXIT) -> pd.DataFrame:
    parts = []
    for uni in ("etfs", "stocks"):
        f = RESULTS / f"trades_daily_{uni}.csv.gz"
        if f.exists():
            d = _read_trades(f)
            parts.append(d[(d["setup"] == setup) & (d["exit_rule"] == ex)].assign(universe=uni))
    return pd.concat(parts) if parts else pd.DataFrame(columns=["r"])


def prior(setup: str, c14: dict) -> dict:
    """Backtest mean R, sigma and win rate for a setup (both universes pooled)."""
    t = backtest_trades(setup)
    if len(t) >= 30:
        r = t["r"].to_numpy(float)
        return dict(n=len(r), mean=float(r.mean()), sigma=float(r.std(ddof=1)), win=float((r > 0).mean()), source="backtest trades")
    # fall back to the P1 summary rows
    means, ns = [], []
    for uni in ("etfs", "stocks"):
        f = RESULTS / f"P1_daily_{uni}.csv"
        if f.exists():
            d = pd.read_csv(f)
            m = d[(d["setup"] == setup) & (d["exit"] == PB_EXIT)]
            if len(m):
                means.append(float(m.iloc[0]["expectancy"]))
                ns.append(int(m.iloc[0]["n"]))
    if ns:
        return dict(n=sum(ns), mean=float(np.average(means, weights=ns)), sigma=c14["allocation"]["sigma_default"],
                    win=0.45, source="P1 summary")
    return dict(n=0, mean=np.nan, sigma=c14["allocation"]["sigma_default"], win=0.45, source="missing")


def tier(p: float, live_n: int, a: dict) -> float:
    for lo, risk in a["tiers"]:
        if p >= lo:
            if risk >= 0.01 and live_n < a["min_live_for_top"]:
                return 0.0075
            return float(risk)
    return 0.0


def posterior(prior_mean: float, sigma: float, live_n: int, live_total: float, a: dict) -> tuple[float, float]:
    n0, h = a["n0"], a["haircut"]
    if np.isnan(prior_mean):
        return np.nan, np.nan
    mean = (n0 * h * prior_mean + live_total) / (n0 + live_n)
    se = sigma / math.sqrt(n0 + live_n)
    return float(mean), float(_phi(mean / se)) if se > 0 else np.nan


# ------------------------------------------------------------------ safety nets
def streak_probability(L: int, n: int, p_win: float, sims: int = 4000, seed: int = 7) -> float:
    """P(a losing streak of at least L appears somewhere in n trades) when each trade wins with p_win."""
    if L <= 0 or n <= 0:
        return 1.0
    rng = np.random.default_rng(seed)
    losses = rng.random((sims, n)) >= p_win
    hit = np.zeros(sims, bool)
    run = np.zeros(sims, int)
    for j in range(n):
        run = np.where(losses[:, j], run + 1, 0)
        hit |= run >= L
    return float(hit.mean())


def backtest_losses(setup: str) -> np.ndarray:
    """Backtest trades of a setup (both universes pooled) as a loss sequence in exit-date order, the order a live
    paper stream sees them. Empty when the trade file has no exit dates."""
    t = backtest_trades(setup)
    if len(t) == 0 or "exit_date" not in t:
        return np.array([], bool)
    t = t.assign(_x=pd.to_datetime(t["exit_date"], errors="coerce")).dropna(subset=["_x"])
    t = t.sort_values(["_x", "symbol"] if "symbol" in t else ["_x"], kind="mergesort")
    return (t["r"].to_numpy(float) <= 0)


def streak_probability_block(L: int, n: int, losses: np.ndarray, block: int = 20, sims: int = 4000, seed: int = 7) -> float:
    """P(a losing streak of at least L appears somewhere in n trades), by a moving-block bootstrap of the backtest
    loss sequence. Unlike i.i.d. odds this keeps the clustering of losses in bad markets (the E4 history has a
    19-trade streak where i.i.d. odds put the 99th percentile near 11), so the flag fires on unusual streaks only."""
    if L <= 0 or n <= 0:
        return 1.0
    m = len(losses)
    if m < 3 * block:
        return np.nan
    rng = np.random.default_rng(seed)
    nb = -(-n // block)
    starts = rng.integers(0, m - block + 1, size=(sims, nb))
    idx = (starts[:, :, None] + np.arange(block)).reshape(sims, -1)[:, :n]
    seq = losses[idx]
    hit = np.zeros(sims, bool)
    run = np.zeros(sims, int)
    for j in range(n):
        run = np.where(seq[:, j], run + 1, 0)
        hit |= run >= L
    return float(hit.mean())


def current_streak(r: pd.Series) -> int:
    k = 0
    for v in r.to_numpy()[::-1]:
        if v <= 0:
            k += 1
        else:
            break
    return k


def ks_2samp(a: np.ndarray, b: np.ndarray) -> tuple[float, float]:
    """Two-sample Kolmogorov-Smirnov statistic and asymptotic p-value (no scipy dependency)."""
    a, b = np.sort(np.asarray(a, float)), np.sort(np.asarray(b, float))
    n, m = len(a), len(b)
    if n == 0 or m == 0:
        return np.nan, np.nan
    allv = np.concatenate([a, b])
    d = float(np.max(np.abs(np.searchsorted(a, allv, side="right") / n - np.searchsorted(b, allv, side="right") / m)))
    en = math.sqrt(n * m / (n + m))
    lam = (en + 0.12 + 0.11 / en) * d
    if lam < 0.3:          # the series is ~1 here and converges badly near 0
        return d, 1.0
    p = 2 * sum((-1) ** (k - 1) * math.exp(-2 * k * k * lam * lam) for k in range(1, 101))
    return d, float(min(max(p, 0.0), 1.0))


def portfolio_drawdown(trades: pd.DataFrame, risk_of: dict, max_open: int) -> float:
    """Max drawdown (fraction of equity, simple sum of risk x R) of the live paper trades a max_open-slot
    portfolio would have taken, in fill order. Open trades count at their latest mark. Each trade is weighted
    by the risk in force when it filled (column `risk_at_fill`), falling back to `risk_of[setup]`."""
    if trades.empty:
        return 0.0
    t = trades.sort_values("fill_date")
    taken, busy = [], []
    for _, r in t.iterrows():
        busy = [e for e in busy if not (pd.notna(e) and e <= r["fill_date"])]   # still open at this fill
        if len(busy) >= max_open:
            continue
        busy.append(r["exit_date"] if r["status"] == "closed" else pd.NaT)
        taken.append(r)
    if not taken:
        return 0.0
    k = pd.DataFrame(taken)
    k["when"] = k["exit_date"].where(k["status"] == "closed", pd.Timestamp.max)
    k = k.sort_values("when")
    w = k["risk_at_fill"] if "risk_at_fill" in k else pd.Series(np.nan, index=k.index)
    w = w.fillna(k["setup"].map(lambda s_: risk_of.get(s_, 0.005)))
    eq = np.cumsum((w * k["r"].fillna(0.0)).to_numpy(float))     # a missing mark counts as 0, never NaN
    peak = np.maximum.accumulate(np.r_[0.0, eq])
    return float((np.r_[0.0, eq] - peak).min())


def ref_drawdown(risk: float, c: dict, c14: dict) -> float:
    """Backtest max drawdown of the P6 playbook portfolio at the given risk (ETFs), else the scaled fallback."""
    f = RESULTS / "P6_playbook_daily_etfs.csv"
    if f.exists() and risk > 0:
        try:
            from . import backtest as bt
            k = pd.read_csv(f, parse_dates=["entry_date", "exit_date"])
            pm = bt.portfolio(k, risk, c["risk"]["max_open"])
            if pm and pm.get("max_dd") is not None:
                return float(pm["max_dd"])
        except Exception:
            pass
    return -c14["safety"]["ref_max_dd_at_075"] * risk / 0.0075


# ------------------------------------------------------------------ the board
def ladder(pt: pd.DataFrame, c: dict, c14: dict | None = None) -> dict:
    c14 = c14 or cfg14()
    a, sf = c14["allocation"], c14["safety"]
    board = {}
    for su in c.get("playbook", {}).get("setups", []):
        d = pt[pt["setup"] == su] if not pt.empty else pd.DataFrame(columns=["oos", "status", "r"])
        oos = d["oos"].astype(bool) if len(d) else pd.Series(dtype=bool)
        live = d[oos & (d["status"] == "closed")].copy() if len(d) else d
        if len(live):
            live["exit_date"] = pd.to_datetime(live["exit_date"].astype(str), format="ISO8601", errors="coerce")
            live = live.sort_values("exit_date")
        pr = prior(su, c14)
        n, total = len(live), float(live["r"].sum()) if len(live) else 0.0
        mean, p = posterior(pr["mean"], pr["sigma"], n, total, a)
        risk = tier(p, n, a) if not np.isnan(p) else 0.0
        L = current_streak(live["r"]) if n else 0
        method = sf.get("streak_method", "iid")      # the configured method; "iid (fallback)" when it could not run
        p_streak = 1.0
        if L:
            p_streak = np.nan
            if sf.get("streak_method", "iid") == "block":
                p_streak = streak_probability_block(L, max(n, L), backtest_losses(su), int(sf.get("streak_block", 20)))
                method = "block"
            if np.isnan(p_streak):       # no dated backtest sequence: fall back to i.i.d. odds
                p_streak = streak_probability(L, max(n, L), pr["win"])
                method = "iid (fallback)" if method == "block" else "iid"
        board[su] = dict(
            status=f"{100 * risk:.2f}%", tier_risk=risk, risk=risk, live_n=n, live_total_r=total,
            live_expectancy=float(live["r"].mean()) if n else np.nan,
            live_win_rate=float((live["r"] > 0).mean()) if n else np.nan,
            open_trades=int((oos & (d["status"] == "open")).sum()) if len(d) else 0,
            prior_mean=pr["mean"], prior_n=pr["n"], prior_sigma=pr["sigma"], prior_win=pr["win"], prior_source=pr["source"],
            posterior_mean=mean, p_edge=p, losing_streak=L, streak_p=p_streak, streak_method=method,
            streak_flag=bool(L and p_streak < sf["streak_flag_p"]))
    # risk in force when each live trade filled (persisted, so later tier changes never re-weight history)
    prev = json.loads(ALLOC.read_text()) if ALLOC.exists() else {}
    prev_risk = {k: v.get("risk", v.get("tier_risk")) for k, v in prev.get("board", {}).items()}
    raf = json.loads(RISK_AT_FILL.read_text()) if RISK_AT_FILL.exists() else {}
    live_all = pt[pt["oos"].astype(bool) & pt["status"].isin(["open", "closed"])].copy() if not pt.empty else pd.DataFrame()
    for sid, su in zip(live_all.get("signal_id", []), live_all.get("setup", [])):
        if sid not in raf:
            raf[sid] = prev_risk.get(su, board.get(su, {}).get("tier_risk", 0.0))
    RISK_AT_FILL.parent.mkdir(parents=True, exist_ok=True)
    RISK_AT_FILL.write_text(json.dumps(_clean(raf), indent=1))
    if len(live_all):
        live_all["risk_at_fill"] = live_all["signal_id"].map(raf)
    risk_of = {k: v["tier_risk"] for k, v in board.items()}
    mean_risk = float(np.mean([v for v in risk_of.values() if v > 0])) if any(v > 0 for v in risk_of.values()) else 0.0
    dd = 0.0
    if len(live_all):
        for col in ("fill_date", "exit_date"):
            live_all[col] = pd.to_datetime(live_all[col].astype(str), format="ISO8601", errors="coerce")
        dd = portfolio_drawdown(live_all, risk_of, c["risk"]["max_open"])
    ref = ref_drawdown(mean_risk, c, c14) if mean_risk > 0 else np.nan
    mult, state = 1.0, "ok"
    tripped = None
    if mean_risk > 0 and ref < 0:
        if dd < sf["breaker_paper"] * ref:
            mult, state = 0.0, "PAPER ONLY (drawdown beyond 1.5x the backtest maximum)"
        elif dd < sf["breaker_halve"] * ref:
            mult, state = 0.5, "HALVED (drawdown beyond the backtest maximum)"
    # "paper only until reviewed": a PAPER ONLY trip latches until config_v14.yaml safety.breaker_reset
    # is set to a date on or after the trip
    pp = prev.get("portfolio", {})
    if str(pp.get("breaker", "")).startswith("PAPER ONLY"):
        tripped = pp.get("tripped_utc")
        reset = str(sf.get("breaker_reset") or "")
        if not (reset and tripped and reset >= str(tripped)[:10]):
            mult, state = 0.0, pp.get("breaker")
    if state.startswith("PAPER ONLY") and not tripped:
        tripped = pd.Timestamp.now(tz="UTC").strftime("%Y-%m-%d %H:%M")
    for v in board.values():
        v["risk"] = v["tier_risk"] * mult
        v["status"] = f"{100 * v['risk']:.2f}%"
    meta = dict(live_drawdown=dd, ref_drawdown=ref, breaker=state, multiplier=mult,
                tripped_utc=tripped if state.startswith("PAPER ONLY") else None)
    ALLOC.parent.mkdir(parents=True, exist_ok=True)
    ALLOC.write_text(json.dumps(_clean(dict(board=board, portfolio=meta)), indent=1, default=str))
    return {"_portfolio": meta, **board}


def health(pt: pd.DataFrame, c: dict, c14: dict | None = None) -> dict:
    """Process health: live vs pre-live (backfilled) paper trades, and live R vs the backtest R distribution.
    These flag data or execution problems, not edge."""
    c14 = c14 or cfg14()
    sf = c14["safety"]
    out = {}
    if pt.empty:
        return out
    for su in c.get("playbook", {}).get("setups", []):
        d = pt[pt["setup"] == su]
        oos = d["oos"].astype(bool)
        live, pre = d[oos], d[~oos]
        def rate(x, st):
            return float((x["status"] == st).mean()) if len(x) else np.nan
        def width(x):
            ok = x[x["status"].isin(["open", "closed"])]
            return float(((ok["fill"] - ok["stop"]) / ok["fill"]).median()) if len(ok) else np.nan
        lr = live[live["status"] == "closed"]["r"].to_numpy(float)
        bt_r = backtest_trades(su)["r"].to_numpy(float)
        ks, p = ks_2samp(lr, bt_r) if len(lr) >= sf["health_min_live"] and len(bt_r) else (np.nan, np.nan)
        out[su] = dict(live_signals=len(live), cancel_live=rate(live, "cancelled"), cancel_pre=rate(pre, "cancelled"),
                       skip_live=rate(live, "skipped"), skip_pre=rate(pre, "skipped"),
                       stop_width_live=width(live), stop_width_pre=width(pre), ks=ks, ks_p=p,
                       ks_flag=bool(not np.isnan(p) and p < sf["health_p"]))
    HEALTH.parent.mkdir(parents=True, exist_ok=True)
    HEALTH.write_text(json.dumps(_clean(out), indent=1))
    return out


def _clean(o):
    if isinstance(o, dict):
        return {k: _clean(v) for k, v in o.items()}
    if isinstance(o, float) and (np.isnan(o) or np.isinf(o)):
        return None
    if isinstance(o, (np.floating,)):
        return None if np.isnan(o) else float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


# ------------------------------------------------------------------ context tags (v1.4 section 5)
def earnings_days(sym: str, day: pd.Timestamp) -> tuple[float, float]:
    """(trading-agnostic) calendar days since the last and until the next earnings date, from data/earnings."""
    f = ROOT / "data" / "earnings" / f"{sym}.csv"
    if not f.exists():
        return np.nan, np.nan
    try:
        e = pd.read_csv(f, index_col=0, parse_dates=True).index.normalize()
    except Exception:
        return np.nan, np.nan
    past, fut = e[e <= day], e[e > day]
    return (float((day - past.max()).days) if len(past) else np.nan,
            float((fut.min() - day).days) if len(fut) else np.nan)


def tags(x: pd.DataFrame, i: int, sym: str, ctx: dict, live: bool = True) -> dict:
    """Context known at the close of signal bar i. Descriptive only: no rule reads these.
    live=False (backfilled or historical signals): days-to-next-earnings is left empty, because today's earnings
    file may list dates that were not yet announced at the signal date."""
    r = x.iloc[i]
    day = x.index[i]
    atr_pct = x["atr"] / x["close"]
    win = atr_pct.iloc[max(0, i - 249):i + 1]
    since_wx = np.nan
    wx = np.flatnonzero(x["ad_washout_exit"].to_numpy()[:i + 1])
    if len(wx):
        since_wx = float(i - wx[-1])
    out = dict(tag_stage=int(r["stage"]), tag_score=int(r["score"]), tag_trend200=bool(r["trend200_up"]),
               tag_line_up=bool(r["tr_line_rising"]), tag_dist_anchor_atr=_f(r.get("dist_anchor_atr")),
               tag_dist_line_atr=_f(r.get("dist_line_atr")), tag_rvol=_f(r.get("rvol")),
               tag_atr_pct=_f(atr_pct.iloc[i]), tag_atr_pctile=_f((win <= atr_pct.iloc[i]).mean()),
               tag_stop_width=_f((r["close"] - (x["low"].iloc[max(0, i - 4):i + 1].min() - 0.5 * r["atr"])) / r["close"]),
               tag_bars_since_washout_exit=since_wx, tag_rrg=str(r.get("rrg", "") or ""))
    spy = ctx.get("spy")
    if spy is not None and day in spy.index:
        s = spy.loc[day]
        out.update(tag_spy_stage=int(s["stage"]), tag_spy_trend200=bool(s["trend200_up"]))
    h4 = ctx.get("h4", {}).get(sym)
    if h4 is not None:
        day_close_et = day + pd.Timedelta(hours=16)        # 4H index = ET slot start, tz-naive
        prior = h4[h4.index < day_close_et]
        out["tag_h4_stage"] = int(prior["stage"].iloc[-1]) if len(prior) else np.nan
    since, until = earnings_days(sym, day)
    out.update(tag_days_since_earnings=since, tag_days_to_earnings=until if live else np.nan)
    return out


def _f(v):
    try:
        v = float(v)
        return round(v, 4) if np.isfinite(v) else np.nan
    except Exception:
        return np.nan
