"""Exit simulator for the E4 exit test (prereg_exits_v1.yaml).

Execution is identical to ifi/backtest.py simulate(): fill at the next open; initial stop = 5-bar low -
0.5 ATR at the signal bar; skip if the open is below that 5-bar low or risk <= 0; inside each bar the stop
is checked first (a gap through it fills at the open), then the target; a time cap exits at that bar's
close; close-based exits are decided on the close and filled at the next open; costs per side in R.
X3 reproduces the Lab's X3_target3R exactly (checked trade by trade in run.py and tests/test_exits.py).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

KINDS = ["X3", "X8", "X9", "X10", "X11", "X12"]


def arrays(x: pd.DataFrame, ev: dict) -> dict:
    c = x["close"].to_numpy(float)
    if "adjclose" in x.columns:
        a = (x["adjclose"].to_numpy(float) / c)
        a = pd.Series(a).ffill().bfill().fillna(1.0).to_numpy()
    else:
        a = np.ones(len(x))
    return dict(o=x["open"].to_numpy(float), h=x["high"].to_numpy(float), l=x["low"].to_numpy(float),
                c=c, a=a, atr=x["atr"].to_numpy(float),
                low5=x["low"].rolling(5).min().to_numpy(float), ph=ev["ph"], pl=ev["pl"], last_pl=ev["last_pl"],
                breakdown=ev["breakdown"], warn_cum=ev["warn_cum"], n=len(x))


def simulate(A: dict, t: int, kind: str, X: dict, P: dict, cost: float, path: bool = False) -> dict | None:
    """One trade from E4 signal bar t with exit `kind`. X = exit definitions, P = engine params.
    r  : price-only R (identical to the Lab's accounting)
    rt : total-return R: the same trade with dividends received during the hold credited
         (price at bar j valued as price * a[j] / a[e], a = Adj Close / Close from Yahoo)
    path (optional): total-return R marked at each close from the entry bar to the bar before the exit."""
    o, h, l, c, atr, n, a = A["o"], A["h"], A["l"], A["c"], A["atr"], A["n"], A["a"]
    e = t + 1
    if e >= n or np.isnan(atr[t]) or np.isnan(A["low5"][t]):
        return None
    fill = o[e]
    low5 = A["low5"][t]
    stop = low5 - 0.5 * atr[t]
    risk = fill - stop
    if np.isnan(fill) or fill < low5 or not risk > 0:
        return dict(cancelled=True)
    cfg = X[kind]
    target = fill + cfg["target_r"] * risk if "target_r" in cfg else np.inf
    cap = cfg["time_cap"]
    use_r3 = kind in ("X10", "X11", "X12")
    ph, pl, bd, wc, piv = A["ph"], A["pl"], A["breakdown"], A["warn_cum"], P["piv"]
    peak, lh = None, False
    lastpl = A["last_pl"][e - 1]
    part, realized, realized_t, weight, px_half = False, 0.0, 0.0, 1.0, np.nan
    hi_since = -np.inf
    px, why, j = None, "", e
    marks = []
    while j < n:
        if j > e and o[j] <= stop:
            px, why = o[j], ("trail_gap" if part else "stop_gap")
            break
        if l[j] <= stop:
            px, why = (min(o[j], stop) if j > e else stop), ("trail" if part else "stop")
            break
        if h[j] >= target:
            hit = max(o[j], target) if j > e else target
            if kind == "X8":
                if not part:
                    part, px_half, weight = True, hit, 0.5
                    realized = 0.5 * (hit - fill) / risk
                    realized_t = 0.5 * (hit * a[j] / a[e] - fill) / risk
                    target = np.inf
            else:
                px, why = hit, "target"
                break
        held = j - e + 1
        if path:
            marks.append(realized_t + weight * (c[j] * a[j] / a[e] - fill) / risk)
        hi_since = max(hi_since, h[j])
        if kind == "X8" and part and not np.isnan(atr[j]):
            stop = max(stop, hi_since - cfg["chandelier_atr"] * atr[j])
        if held >= cap:
            px, why = c[j], "time"
            break
        ex = None
        if use_r3:
            if not np.isnan(ph[j]) and j - piv >= e:
                if peak is None or ph[j] > peak:
                    peak, lh = ph[j], False
                elif ph[j] < peak:
                    lh = True
            if not np.isnan(pl[j]):
                lastpl = pl[j]
            if peak is not None and lh and not np.isnan(lastpl) and c[j] < lastpl:
                ex = "rule3"
            if kind == "X11" and ex is None and bd[j]:
                lo = max(e, j - P["xb_win"] + 1)
                if wc[j] - (wc[lo - 1] if lo >= 1 else 0) >= P["xb_warn"]:
                    ex = "fast"
        if ex is not None:
            if j + 1 < n:
                j += 1
                px, why = o[j], ex
            else:
                px, why = c[j], "open_at_end"
            break
        j += 1
    if px is None:
        j = n - 1
        px, why = c[j], "open_at_end"
    r = realized + weight * (px - fill) / risk
    rt = realized_t + weight * (px * a[j] / a[e] - fill) / risk
    avg_exit = px if not part else 0.5 * px_half + 0.5 * px
    r -= cost * (fill + avg_exit) / risk
    rt -= cost * (fill + avg_exit) / risk
    out = dict(cancelled=False, r=float(r), rt=float(rt), bars=int(j - e + 1), why=why, exit_i=int(j), e=int(e),
               risk_pct=float(risk / fill))
    if path:
        # marks were taken at closes e..j (the exit bar's mark is replaced by the realised result)
        out["path"] = np.array(marks[:max(0, j - e)] + [rt])
    return out


def no_overlap(trades: pd.DataFrame) -> pd.DataFrame:
    """Lab sequencing per symbol: after a trade, the next signal is taken only from its exit bar onward."""
    keep = []
    for _, g in trades.sort_values(["sym", "t"]).groupby("sym", sort=False):
        nxt = -1
        for row in g.itertuples():
            if row.t >= nxt:
                keep.append(row.Index)
                nxt = row.exit_i
    return trades.loc[keep]
