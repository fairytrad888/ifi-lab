"""Trade simulator, setups, exit rules, metrics and pre-registered decision rules.

Execution model (identical for every experiment):
- Signal on a bar's close; fill at the NEXT bar's open.
- Initial stop = lowest low of the last 5 bars - 0.5 x ATR(14), measured at the signal bar.
  1R = fill - stop. Trades with no room (stop >= fill) are skipped.
- Stops and targets are checked intrabar; if the bar gaps through, the fill is the open.
  If stop and target could both trigger in one bar, the stop is assumed first (conservative).
- Close-based exits (Trend line, stage drop, time) fill at the next open (time exits at that bar's close).
- One open trade per symbol per setup/exit combination. Max hold 60 bars.
- Costs: `cost` fraction of price per side, converted to R.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .states import _bars_since

MAX_HOLD = 60


# --------------------------------------------------------------------------- setups (entries)
def setups(x: pd.DataFrame) -> dict[str, pd.Series]:
    bs_wexit = _bars_since(x["ad_washout_exit"])
    bs_nine = _bars_since(x["tr_nine"] == -1)
    exh = (bs_wexit <= 3) & (bs_nine <= 3)
    st = x["stage"]
    was_below = (st.shift(1) < 2)
    for k in range(2, 6):
        was_below &= (st.shift(k) < 2)
    s = {
        "E1_trigger_with_trend": x["sig_trig_bull"] & x["trend200_up"],
        "E1b_trigger_counter_trend": x["sig_trig_bull"] & ~x["trend200_up"],
        "E2_exhaustion_confluence": exh & ~exh.shift(1, fill_value=False),
        "E3_stage2_transition": (st >= 2) & was_below & x["chk1_higher_low"],
        "E4_anchor_reclaim": x["chk2_above_anchor"] & ~x["chk2_above_anchor"].shift(1, fill_value=False)
        & ~x["tr_anchor_is_support"].shift(1, fill_value=True),
        "E5_score4": (x["score"] >= 4) & (x["score"].shift(1) < 4),
    }
    return {k: v.fillna(False).astype(bool) for k, v in s.items()}


def random_setup(x: pd.DataFrame, rate: float, seed: int) -> pd.Series:
    rng = np.random.default_rng(seed)
    m = rng.random(len(x)) < rate
    m[:250] = False  # skip warm-up
    return pd.Series(m, index=x.index)


# --------------------------------------------------------------------------- exits
EXITS = {
    "X1_time10": dict(time=10),
    "X2_target2R": dict(target=2.0),
    "X3_target3R": dict(target=3.0),
    "X4_trendline_trail": dict(line_trail=True),
    "X5_chandelier3atr": dict(chandelier=3.0),
    "X6_partial1R_then_line": dict(partial=1.0, line_trail=True),
    "X7_stage_drop": dict(stage_drop=True),
}


@dataclass
class Trade:
    symbol: str
    setup: str
    exit_rule: str
    entry_date: pd.Timestamp
    exit_date: pd.Timestamp
    bars: int
    r: float
    mfe_r: float
    mae_r: float
    reason: str
    risk_pct: float


def simulate(sym: str, x: pd.DataFrame, entries: pd.Series, setup: str, exit_rule: str, cost: float = 0.0005) -> list[Trade]:
    rule = EXITS[exit_rule]
    o, h, l, c = (x[k].to_numpy() for k in ("open", "high", "low", "close"))
    atr = x["atr"].to_numpy()
    line = x["tr_line"].to_numpy()
    rising = x["tr_line_rising"].to_numpy()
    low5 = x["low"].rolling(5).min().to_numpy()
    sig = entries.to_numpy()
    idx = x.index
    n = len(x)
    trades: list[Trade] = []
    t = 0
    while t < n - 2:
        if not sig[t] or np.isnan(atr[t]) or np.isnan(low5[t]) or np.isnan(line[t]):
            t += 1
            continue
        e = t + 1
        fill = o[e]
        stop = low5[t] - 0.5 * atr[t]
        risk = fill - stop
        if not (risk > 0) or np.isnan(fill):
            t += 1
            continue
        target = fill + rule["target"] * risk if "target" in rule else np.inf
        part_lvl = fill + rule["partial"] * risk if "partial" in rule else np.inf
        part_done = False
        realized = 0.0  # R already banked by a partial
        weight = 1.0
        hi_since = h[e]
        mfe = mae = 0.0
        exit_px = None
        reason = ""
        j = e
        while j < n:
            # intrabar: stop first, then partial / target
            if o[j] <= stop and j > e:
                exit_px, reason = o[j], "stop_gap"
            elif l[j] <= stop:
                exit_px, reason = (min(o[j], stop) if j > e else stop), "stop"
            if exit_px is not None:
                break
            mfe = max(mfe, (h[j] - fill) / risk)
            mae = min(mae, (l[j] - fill) / risk)
            if not part_done and h[j] >= part_lvl:
                realized += 0.5 * rule["partial"]
                weight = 0.5
                part_done = True
                stop = max(stop, fill)  # breakeven on the rest
            if h[j] >= target:
                exit_px, reason = (max(o[j], target) if j > e else target), "target"
                break
            # close-based rules (decide on close j, act at open j+1)
            held = j - e + 1
            hi_since = max(hi_since, h[j])
            if "chandelier" in rule and not np.isnan(atr[j]):
                stop = max(stop, hi_since - rule["chandelier"] * atr[j])
            close_exit = None
            if "time" in rule and held >= rule["time"]:
                exit_px, reason = c[j], "time"
                break
            if rule.get("line_trail") and c[j] < line[j]:
                close_exit = "line"
            if rule.get("stage_drop") and c[j] < line[j] and not rising[j]:
                close_exit = "stage_drop"
            if held >= MAX_HOLD:
                exit_px, reason = c[j], "max_hold"
                break
            if close_exit and j + 1 < n:
                j += 1
                exit_px, reason = o[j], close_exit
                break
            j += 1
        if exit_px is None:  # data ended: mark to last close
            j = n - 1
            exit_px, reason = c[j], "open_at_end"
        r = realized + weight * (exit_px - fill) / risk
        r -= cost * (fill + exit_px) / risk
        trades.append(Trade(sym, setup, exit_rule, idx[e], idx[min(j, n - 1)], int(min(j, n - 1) - e + 1),
                            float(r), float(mfe), float(mae), reason, float(risk / fill)))
        t = max(j, t + 1)  # no overlapping trades for this symbol/setup/exit
    return trades


# --------------------------------------------------------------------------- metrics
def metrics(r: np.ndarray, boot: int = 2000, alpha: float = 0.05, seed: int = 7) -> dict:
    r = np.asarray(r, dtype=float)
    n = len(r)
    if n == 0:
        return dict(n=0)
    wins, losses = r[r > 0], r[r <= 0]
    exp = r.mean()
    sd = r.std(ddof=1) if n > 1 else np.nan
    rng = np.random.default_rng(seed)
    if n > 1:
        bs = rng.choice(r, size=(boot, n), replace=True).mean(axis=1)
        lo, hi = np.quantile(bs, [alpha / 2, 1 - alpha / 2])
    else:
        lo = hi = np.nan
    return dict(
        n=n, win_rate=len(wins) / n, avg_win=wins.mean() if len(wins) else 0.0,
        avg_loss=losses.mean() if len(losses) else 0.0, expectancy=exp,
        ci_low=lo, ci_high=hi,
        profit_factor=(wins.sum() / -losses.sum()) if losses.sum() < 0 else np.inf,
        sqn=np.sqrt(min(n, 100)) * exp / sd if sd and sd > 0 else np.nan,
        best=r.max(), worst=r.min(),
    )


def portfolio(trades: pd.DataFrame, risk_pct: float = 0.01, max_open: int = 5, start: float = 100_000.0) -> dict:
    """Fixed-fractional sizing across all trades in time order, with a cap on concurrent positions."""
    if trades.empty:
        return {}
    tr = trades.sort_values("entry_date")
    eq = start
    open_pos: list[tuple[pd.Timestamp, float]] = []  # (exit_date, pnl)
    curve = []
    for _, row in tr.iterrows():
        # close positions that ended before this entry
        still = []
        for ex, pnl in open_pos:
            if ex <= row.entry_date:
                eq += pnl
                curve.append((ex, eq))
            else:
                still.append((ex, pnl))
        open_pos = still
        if len(open_pos) >= max_open:
            continue
        open_pos.append((row.exit_date, row.r * risk_pct * eq))
    for ex, pnl in sorted(open_pos):
        eq += pnl
        curve.append((ex, eq))
    if not curve:
        return {}
    cv = pd.Series([v for _, v in curve], index=pd.to_datetime([d for d, _ in curve])).sort_index()
    cv = cv.groupby(level=0).last()
    years = max((cv.index[-1] - tr.entry_date.min()).days / 365.25, 1e-9)
    cagr = (cv.iloc[-1] / start) ** (1 / years) - 1 if cv.iloc[-1] > 0 else -1.0
    dd = (cv / cv.cummax() - 1).min()
    return dict(risk_pct=risk_pct, final=cv.iloc[-1], cagr=cagr, max_dd=dd, mar=(cagr / -dd) if dd < 0 else np.nan)


# --------------------------------------------------------------------------- decision rule
def verdict(m: dict, halves: list[dict], random_ref: dict | None, n_tests: int, min_trades: int = 100) -> str:
    """Pre-registered: ADOPT needs n >= min_trades, a Bonferroni-adjusted bootstrap CI above 0,
    positive expectancy in every split half, and expectancy above the random-entry 95th percentile."""
    if m.get("n", 0) < min_trades:
        return "INCONCLUSIVE (too few trades)"
    halves_ok = all(hm.get("n", 0) > 0 and hm["expectancy"] > 0 for hm in halves)
    beats_random = random_ref is None or m["expectancy"] > random_ref.get("p95", -np.inf)
    if m["expectancy"] <= 0 or not beats_random:
        return "REJECT"
    if m.get("ci_low_adj", m["ci_low"]) > 0 and halves_ok:
        return "ADOPT"
    if halves_ok:
        return "PROMISING (not significant after correction)"
    return "UNSTABLE (fails a split half)"
