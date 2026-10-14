"""IFI ratio rules v2.1: event engine (pre-registered definitions, research/prereg_v21.yaml).

Every event is dated on the bar where it is KNOWN (at that bar's close). Outcomes start at the next
open. The state machines below are pure functions of arrays so they can be unit-tested and checked for
look-ahead (tests/test_research.py).

Per-bar definitions (t = bar index):
  slope        (line[t] - line[t-10]) / ATR[t]; flat if |slope| < flat, rising if >= flat, falling if <= -flat
  pivots       piv/piv pivot highs/lows (strictly beyond the left bars, >= / <= the right bars), confirmed piv bars later
  bull trend   rising line and the last two confirmed pivots are a higher high and a higher low
  breakdown    first close below line - tol*ATR after a bull trend (re-armed only by a new bull trend);
               also the X-B trigger when >= xb_warn warnings fell within the last xb_win bars of the trade
  up-9 warning completed up-9 with extension (close-line)/ATR >= ext_up, or completed while the line is flat
  down-9       early if <= early9 bars after the breakdown bar, late if >= late9 bars, otherwise neutral
  warning      bearish WT trigger, A&D bearish divergence, Matrix 2-of-3 bearish divergence, or an up-9 warning
  floor        components (only while the line is not rising): washout exit W, bullish divergence D
               (A&D or Matrix 2-of-3), late down-9 L. Tier A = W and D within floor_win bars; tier B = any
               other floor containing W or L (a D + L floor without W is tier B). Floor low Lf = lowest low
               from the first component to the latest component. The floor ends on a close below
               Lf - tol*ATR, or deadline bars after its last component.
  reclaim      close back above the RESISTANCE anchor (identical to the Lab's E4 signal)
  entry        a reclaim while a floor is active (tier A or B; the floor is consumed); otherwise class "none"
  touch        first bar whose low reaches line + tol*ATR with no such bar in the previous touch_gap bars;
               "rising" if the bar before was in a bull trend, "flat" if the line was flat (and not a bull trend)
  rule 3       after a higher-high pivot confirmed while the line is rising (the peak), a lower pivot high,
               then a close below the most recent pivot low. Re-arms only on a new such higher high.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ifi import pine as p
from ifi.states import read

DEFAULTS = dict(ext_up=2.0, early9=10, late9=20, floor_win=40, deadline=60, flat=0.5, slope_bars=10, tol=0.25, piv=3,
                xb_warn=2, xb_win=20, stop="e4", target_r=3.0, max_hold_3r=60, max_hold_struct=250,
                held_bars=10, touch_gap=5, stack_gap=20, cost=0.0005)


# ------------------------------------------------------------------ base indicators (parameter-free)
def base(r: pd.DataFrame) -> pd.DataFrame:
    x = read(r)
    x["sma200"] = p.sma(x["close"], 200)
    return x


# ------------------------------------------------------------------ pure state machines
def last_two(piv_vals: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Most recent and previous confirmed pivot values as of each bar."""
    n = len(piv_vals)
    last, prev = np.full(n, np.nan), np.full(n, np.nan)
    a = b = np.nan
    for i in range(n):
        if not np.isnan(piv_vals[i]):
            b, a = a, piv_vals[i]
        last[i], prev[i] = a, b
    return last, prev


def breakdown_bars(bull: np.ndarray, close: np.ndarray, lower: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """breakdown[t]: first close below `lower` after a bull trend. bsb[t]: bars since the last breakdown.
    One breakdown per bull run: after a breakdown the machine re-arms only when a NEW bull run starts
    (a bar in bull trend after a bar that was not), on a bar that closes at or above `lower`."""
    n = len(close)
    bd = np.zeros(n, bool)
    bsb = np.full(n, np.nan)
    armed, used, last = False, False, -1
    for i in range(n):
        below = not np.isnan(lower[i]) and close[i] < lower[i]
        if armed and below:
            bd[i], armed, used, last = True, False, True, i
        if not bull[i]:
            used = False            # the bull run has ended; the next run may arm again
        elif not used and not below:
            armed = True
        if last >= 0:
            bsb[i] = i - last
    return bd, bsb


def rule3_events(ph: np.ndarray, pl: np.ndarray, close: np.ndarray, rising: np.ndarray | None = None) -> tuple[np.ndarray, dict]:
    """Rule 3 confirmations (tops). ph/pl: pivot values on their confirmation bar (NaN elsewhere).
    The top is armed only by a higher-high pivot confirmed while the Trend line is rising (a top of an
    uptrend, not a bounce inside a decline); a later higher pivot raises the peak."""
    n = len(close)
    out = np.zeros(n, bool)
    if rising is None:
        rising = np.ones(n, bool)
    peak, lh, prev_ph, last_pl = None, False, np.nan, np.nan
    for i in range(n):
        v = ph[i]
        if not np.isnan(v):
            if peak is None:
                if not np.isnan(prev_ph) and v > prev_ph and rising[i]:  # a higher high in an uptrend arms the top
                    peak, lh = v, False
            elif v > peak:
                peak, lh = v, False
            elif v < peak:
                lh = True
            prev_ph = v
        if not np.isnan(pl[i]):
            last_pl = pl[i]
        if peak is not None and lh and not np.isnan(last_pl) and close[i] < last_pl:
            out[i] = True
            peak, lh = None, False
    state = dict(peak=peak, lower_high=lh, trigger_level=last_pl)
    return out, state


def floor_machine(low, close, atr, rising, wexit, bdiv, late9, reclaim, floor_win, deadline, tol):
    """Floors (tier A/B) and reclaim entries. Returns entries list and the final floor state."""
    n = len(close)
    W, D, L = [], [], []
    active, tier, Lf, fstart, last_comp = False, None, np.nan, -1, -1
    entries = []
    for i in range(n):
        if active:
            if close[i] < Lf - tol * atr[i]:
                active = False
                W, D, L = [], [], []
            elif i - last_comp > deadline:
                active = False
                W, D, L = [], [], []
        new = False
        if not rising[i]:
            if wexit[i]:
                W.append(i)
                new = True
            if bdiv[i]:
                D.append(i)
                new = True
            if late9[i]:
                L.append(i)
                new = True
        lo = i - floor_win + 1
        W = [j for j in W if j >= lo]
        D = [j for j in D if j >= lo]
        L = [j for j in L if j >= lo]
        has_a = bool(W) and bool(D)
        has_b = bool(W) or bool(L)
        if not active:
            if new and (has_a or has_b):
                active = True
                fstart = min(W + D + L)
                Lf = float(np.min(low[fstart:i + 1]))
                last_comp = i
                tier = "A" if has_a else "B"
        elif new:
            # Lf = lowest low over the span of the floor's components: it moves only when a new
            # component arrives, so a slow grind lower without new evidence still breaks the floor
            last_comp = i
            Lf = float(np.min(low[fstart:i + 1]))
            if has_a:
                tier = "A"
        if reclaim[i]:
            if active:
                entries.append(dict(t=i, tier=tier, lf=Lf, fstart=fstart, age=i - last_comp))
                active, tier = False, None
                W, D, L = [], [], []
            else:
                entries.append(dict(t=i, tier="none", lf=np.nan, fstart=-1, age=-1))
    state = dict(active=active, tier=tier, lf=Lf if active else np.nan, since_last_component=(n - 1 - last_comp) if active else None)
    return entries, state


# ------------------------------------------------------------------ events for one ratio
def events(x: pd.DataFrame, P: dict) -> dict:
    o, h, l, c = (x[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    atr = x["atr"].to_numpy(float)
    line = x["tr_line"].to_numpy(float)
    n = len(c)
    tol, piv = P["tol"], P["piv"]

    slope = (line - np.roll(line, P["slope_bars"])) / atr
    slope[:P["slope_bars"]] = np.nan
    with np.errstate(invalid="ignore"):
        rising = slope >= P["flat"]
        flat = np.abs(slope) < P["flat"]
    ext = (c - line) / atr

    ph = p.pivot_high(x["high"], piv, piv).to_numpy(float)
    pl = p.pivot_low(x["low"], piv, piv).to_numpy(float)
    last_ph, prev_ph = last_two(ph)
    last_pl, prev_pl = last_two(pl)
    with np.errstate(invalid="ignore"):
        bull = rising & (last_ph > prev_ph) & (last_pl > prev_pl)
        lower = line - tol * atr
        bd, bsb = breakdown_bars(bull, c, lower)
        below = c < lower
    linebreak = below & ~np.r_[False, below[:-1]]

    nine = x["tr_nine"].to_numpy()
    with np.errstate(invalid="ignore"):
        up9_warn = (nine == 1) & ((ext >= P["ext_up"]) | flat)
    down9 = nine == -1
    d9_early = down9 & (bsb <= P["early9"])
    d9_late = down9 & (bsb >= P["late9"])

    warn = (x["sig_trig_bear"].to_numpy(bool) | x["ad_bear_div"].to_numpy(bool)
            | x["mx_strong_bear"].to_numpy(bool) | up9_warn)
    wexit = x["ad_washout_exit"].to_numpy(bool)
    bdiv = x["ad_bull_div"].to_numpy(bool) | x["mx_strong_bull"].to_numpy(bool)

    above = x["chk2_above_anchor"].to_numpy(bool)
    sup = x["tr_anchor_is_support"].to_numpy(bool)
    reclaim = above & ~np.r_[False, above[:-1]] & ~np.r_[True, sup[:-1]]

    entries, floor_state = floor_machine(l, c, atr, rising, wexit, bdiv, d9_late, reclaim,
                                         P["floor_win"], P["deadline"], tol)
    r3, r3_state = rule3_events(ph, pl, c, rising)

    # warning stacks (T3 control): >= xb_warn warnings within xb_win bars, in a bull trend
    wc = np.cumsum(warn.astype(int))                     # wc[i] = warnings in [0, i]
    stack = np.zeros(n, bool)
    last_stack = -10 ** 9
    for i in range(n):
        if warn[i] and bull[i]:
            k = wc[i] - (wc[i - P["xb_win"]] if i - P["xb_win"] >= 0 else 0)
            if k >= P["xb_warn"] and i - last_stack >= P["stack_gap"]:
                stack[i], last_stack = True, i

    # first touches of the line (T5)
    with np.errstate(invalid="ignore"):
        near = l <= line + tol * atr
    g = P["touch_gap"]
    nc = np.r_[0, np.cumsum(near.astype(int))]          # nc[k] = near bars in [0, k)
    idx = np.arange(n)
    prior = nc[idx] - nc[np.maximum(idx - g, 0)]         # near bars in [i-g, i)
    first = near & (prior == 0)
    first[:g] = False
    bull_prev = np.r_[False, bull[:-1]]
    flat_prev = np.r_[False, flat[:-1]]
    touch_rise = first & bull_prev
    touch_flat = first & flat_prev & ~bull_prev
    # how each touch held over the next held_bars bars (descriptive, observation 2's classification):
    # 0 = held at the line (no close below line - tol*ATR), 1 = held at the gray support anchor
    # (closed below the line but not below the anchor - tol*ATR), 2 = failed, NaN = horizon incomplete
    held = np.full(n, np.nan)
    anc = x["tr_anchor"].to_numpy(float)
    sup = x["tr_anchor_is_support"].to_numpy(bool)
    Hb = P["held_bars"]
    for i in np.flatnonzero(touch_rise | touch_flat):
        if i + Hb >= n:
            continue
        seg = slice(i + 1, i + Hb + 1)
        broke_line = np.any(c[seg] < line[seg] - tol * atr[seg])
        if not broke_line:
            held[i] = 0
        elif sup[i] and not np.any(c[seg] < anc[i] - tol * atr[i]):
            held[i] = 1
        else:
            held[i] = 2

    return dict(n=n, slope=slope, rising=rising, flat=flat, ext=ext, bull=bull, breakdown=bd, bsb=bsb,
                linebreak=linebreak, warn=warn, warn_cum=wc, ph=ph, pl=pl, last_pl=last_pl, last_ph=last_ph,
                up9_warn=up9_warn, d9_early=d9_early, d9_late=d9_late, wexit=wexit, bdiv=bdiv, reclaim=reclaim,
                entries=entries, floor_state=floor_state, r3=r3, r3_state=r3_state, stack=stack,
                touch_rise=touch_rise, touch_flat=touch_flat, held=held)


# ------------------------------------------------------------------ trades
def simulate(x: pd.DataFrame, ev: dict, t: int, lf: float, kind: str, P: dict,
             num: pd.DataFrame | None = None) -> dict | None:
    """One trade from signal bar t. kind: '3R' | 'A' (structural, rule 3) | 'B' (fast + rule 3).
    Execution follows ifi/backtest.py: fill at the next open, stop = 5-bar low - 0.5 ATR at the signal bar,
    skipped if the open is already below the 5-bar low, stop checked first (gaps fill at the open)."""
    o, h, l, c = (x[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    atr = x["atr"].to_numpy(float)
    n = len(c)
    e = t + 1
    if e >= n or t < 4 or np.isnan(atr[t]):
        return None
    low5 = float(np.min(l[t - 4:t + 1]))
    fill = o[e]
    if P["stop"] == "lf" and not np.isnan(lf):
        stop = lf - P["tol"] * atr[t]
    else:
        stop = low5 - 0.5 * atr[t]
    risk = fill - stop
    if np.isnan(fill) or fill < low5 or not risk > 0:
        return dict(cancelled=True)
    target = fill + P["target_r"] * risk if kind == "3R" else np.inf
    max_hold = P["max_hold_3r"] if kind == "3R" else P["max_hold_struct"]
    ph, pl, bdown, wc = ev["ph"], ev["pl"], ev["breakdown"], ev["warn_cum"]
    piv = P["piv"]
    peak, lh = None, False
    lastpl = ev["last_pl"][e - 1]
    px, reason, at_open, j = None, "", False, e
    while j < n:
        if j > e and o[j] <= stop:
            px, reason, at_open = o[j], "stop_gap", True
            break
        if l[j] <= stop:
            px, reason, at_open = (min(o[j], stop) if j > e else stop), "stop", False
            break
        if h[j] >= target:
            px, reason, at_open = (max(o[j], target) if j > e else target), "target", False
            break
        held = j - e + 1
        ex = None
        if kind in ("A", "B"):
            if not np.isnan(ph[j]) and j - piv >= e:
                if peak is None or ph[j] > peak:
                    peak, lh = ph[j], False
                elif ph[j] < peak:
                    lh = True
            if not np.isnan(pl[j]):
                lastpl = pl[j]
            if peak is not None and lh and not np.isnan(lastpl) and c[j] < lastpl:
                ex = "rule3"
            if kind == "B" and ex is None and bdown[j]:
                lo = max(e, j - P["xb_win"] + 1)
                k = wc[j] - (wc[lo - 1] if lo >= 1 else 0)
                if k >= P["xb_warn"]:
                    ex = "fast"
        if ex is not None:
            if j + 1 < n:
                j += 1
                px, reason, at_open = o[j], ex, True
            else:
                px, reason, at_open = c[j], "open_at_end", False
            break
        if held >= max_hold:
            px, reason, at_open = c[j], "time", False
            break
        j += 1
    if px is None:
        j = n - 1
        px, reason, at_open = c[j], "open_at_end", False
    cost = P["cost"]
    r = (px - fill) / risk - cost * (fill + px) / risk
    out = dict(cancelled=False, r=float(r), bars=int(j - e + 1), reason=reason, exit_i=int(j), risk_pct=float(risk / fill))
    if num is not None:
        no, ncl = num["open"].to_numpy(float), num["close"].to_numpy(float)
        nf = no[e]
        nx = no[j] if at_open else ncl[j]
        rp = risk / fill
        out["rn"] = float((nx / nf - 1) / rp - cost * (1 + nx / nf) / rp) if nf > 0 and nx > 0 else np.nan
    return out
