"""IFI indicator set ported from the original Pine scripts (1.0), with IFI 2.0 corrections behind flags.

Every function takes an OHLCV DataFrame with lowercase columns
[open, high, low, close, volume] and returns a DataFrame aligned to its index.
All constants are the original IFI defaults.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import pine as p


# --------------------------------------------------------------------------- A&D
def ad(df: pd.DataFrame, mirror_divergence: bool = True) -> pd.DataFrame:
    """IFI Accumulation & Distribution (de-lagged 27-bar stochastic).

    washout      : bar with flow <= 2.3 (1.0 'Flow Reserve' red bars)
    washout_exit : flow crosses back above 2.3 (1.0 'Flow In' green bar)
    washout_no   : number of the washout within the current phase (2.0); phase resets when flow > 50
    bear_div     : 1.0 'Flow Out' (price higher high, flow lower high, flow > 60, 5-bar cooldown)
    bull_div     : 2.0 mirror (price lower low, flow higher low, flow < 40, 5-bar cooldown)
    """
    flow_stoch = p.stoch(df["close"], df["high"], df["low"], 27)
    w1 = p.wma(flow_stoch, 5)
    w2 = p.wma(w1, 3)
    flow = 3 * w1 - 2 * w2
    out = pd.DataFrame(index=df.index)
    out["flow"] = flow
    out["washout"] = flow <= 2.3
    out["washout_exit"] = p.crossover(flow, 2.3)

    # numbering within phase
    no = np.zeros(len(df), dtype=int)
    count = 0
    f = flow.to_numpy()
    ex = out["washout_exit"].to_numpy()
    for i in range(len(df)):
        if not np.isnan(f[i]) and f[i] > 50:
            count = 0
        if ex[i]:
            count += 1
            no[i] = count
    out["washout_no"] = no

    # divergences (pivots 5 left / 2 right, confirmed 2 bars later)
    ph = p.pivot_high(df["high"], 5, 2).to_numpy()
    pl = p.pivot_low(df["low"], 5, 2).to_numpy()
    bear = np.zeros(len(df), dtype=bool)
    bull = np.zeros(len(df), dtype=bool)
    last_p = last_m = np.nan
    last_lp = last_lm = np.nan
    last_bear = last_bull = -10_000
    for i in range(len(df)):
        if not np.isnan(ph[i]):
            cur_p, cur_m = ph[i], f[i - 2]
            if not np.isnan(last_p) and cur_p > last_p and cur_m < last_m and cur_m > 60 and i - last_bear >= 5:
                bear[i] = True
                last_bear = i
            last_p, last_m = cur_p, cur_m
        if mirror_divergence and not np.isnan(pl[i]):
            cur_p, cur_m = pl[i], f[i - 2]
            if not np.isnan(last_lp) and cur_p < last_lp and cur_m > last_lm and cur_m < 40 and i - last_bull >= 5:
                bull[i] = True
                last_bull = i
            last_lp, last_lm = cur_p, cur_m
    out["bear_div"] = bear
    out["bull_div"] = bull
    # Chips reduced to its unique information (2.0): 100-bar range position
    hh, ll = p.highest(df["high"], 100), p.lowest(df["low"], 100)
    out["range_pos100"] = (100 * (df["close"] - ll) / (hh - ll).replace(0, np.nan)).clip(0, 100)
    return out


# --------------------------------------------------------------------------- Signals
def signals(df: pd.DataFrame, direction_fix: bool = True) -> pd.DataFrame:
    """IFI Signals (WaveTrend). direction_fix=True uses crossover/crossunder (2.0);
    False reproduces 1.0 (ta.cross in either direction)."""
    ap = (df["high"] + df["low"] + df["close"]) / 3
    esa = p.ema(ap, 10)
    d = p.ema((ap - esa).abs(), 10)
    ci = (ap - esa) / (0.015 * d.replace(0, np.nan))
    ci = ci.ffill()
    wt1 = p.ema(ci, 21)
    wt2 = p.sma(wt1, 4)
    out = pd.DataFrame(index=df.index)
    out["wt1"], out["wt2"] = wt1, wt2
    out["channel"] = p.linreg(wt1, 200, 0)
    if direction_fix:
        out["trig_bull"] = p.crossover(wt1, wt2) & (wt1 < -50)
        out["trig_bear"] = p.crossunder(wt1, wt2) & (wt1 > 60)
    else:
        c = p.cross(wt1, wt2)
        out["trig_bull"] = c & (wt1 < -50)
        out["trig_bear"] = c & (wt1 > 60)
    # streaks: number of same-side triggers since WT1 last crossed the zero midline
    bs = np.zeros(len(df), dtype=int)
    ss = np.zeros(len(df), dtype=int)
    b = s = 0
    w = wt1.to_numpy()
    tb, tsr = out["trig_bull"].to_numpy(), out["trig_bear"].to_numpy()
    for i in range(len(df)):
        if not np.isnan(w[i]):
            if w[i] > 0:
                b = 0
            if w[i] < 0:
                s = 0
        if tb[i]:
            b += 1
            bs[i] = b
        if tsr[i]:
            s += 1
            ss[i] = s
    out["bull_streak"], out["bear_streak"] = bs, ss
    out["zone"] = np.select([wt1 > 60, wt1 > 53, wt1 < -63, wt1 < -50], [2, 1, -2, -1], 0)
    return out


# --------------------------------------------------------------------------- Matrix
def matrix(df: pd.DataFrame, lookback: int = 5) -> pd.DataFrame:
    """IFI Matrix: RSI(14), KDJ(9,3,3), TSI(13,25); 2-of-3 divergence on price pivots.
    Signals are placed on the CONFIRMATION bar (2.0); `pivot_bar_offset` = lookback."""
    v1 = p.rsi(df["close"], 14)
    hh, ll = p.highest(df["high"], 9), p.lowest(df["low"], 9)
    rng = hh - ll
    rsv = (100 * (df["close"] - ll) / rng.replace(0, np.nan)).fillna(50.0).to_numpy()
    k = np.empty(len(df))
    d = np.empty(len(df))
    kp = dp = 50.0
    for i in range(len(df)):
        kp = (2 * kp + rsv[i]) / 3  # identical to the corrected ((n-1)k+rsv)/n at n=3
        dp = (2 * dp + kp) / 3
        k[i], d[i] = kp, dp
    v2 = pd.Series(3 * k - 2 * d, index=df.index)
    v3 = p.tsi(df["close"], 13, 25) * 100
    ph = p.pivot_high(df["high"], lookback, lookback).to_numpy()
    pl = p.pivot_low(df["low"], lookback, lookback).to_numpy()
    vals = [v1.to_numpy(), v2.to_numpy(), v3.to_numpy()]
    bear = np.zeros(len(df), dtype=int)
    bull = np.zeros(len(df), dtype=int)
    last_h = last_l = None  # (price, [osc values])
    for i in range(len(df)):
        if not np.isnan(ph[i]):
            cur = (ph[i], [v[i - lookback] for v in vals])
            if last_h is not None and cur[0] > last_h[0]:
                bear[i] = sum(1 for a, b in zip(cur[1], last_h[1]) if a < b)
            last_h = cur
        if not np.isnan(pl[i]):
            cur = (pl[i], [v[i - lookback] for v in vals])
            if last_l is not None and cur[0] < last_l[0]:
                bull[i] = sum(1 for a, b in zip(cur[1], last_l[1]) if a > b)
            last_l = cur
    out = pd.DataFrame(index=df.index)
    out["rsi"], out["kdj_j"], out["tsi"] = v1, v2, v3
    out["bull_votes"], out["bear_votes"] = bull, bear
    out["strong_bull"], out["strong_bear"] = bull >= 2, bear >= 2
    return out


# --------------------------------------------------------------------------- Trend
def trend(df: pd.DataFrame, anchor_from_pivot_bar: bool = False) -> pd.DataFrame:
    """IFI Trend: weighted-price triple-EMA baseline (de-lagged), 4-bar 9-count, 50-bar VWAP anchors."""
    pt = (df["close"] * 3 + df["open"] * 2 + df["low"] + df["high"]) / 7
    base = (p.ema(pt, 21) + p.ema(pt, 34) + p.ema(pt, 68)) / 3
    line = 3 * p.wma(base, 6) - 2 * p.sma(base, 6)
    out = pd.DataFrame(index=df.index)
    out["line"] = line
    out["line_rising"] = line > line.shift(1)

    # 9-count (close vs close 4 bars ago); records completed and failed sequences
    c = df["close"].to_numpy()
    n = len(df)
    cnt = np.zeros(n, dtype=int)
    direction = np.zeros(n, dtype=int)
    done9 = np.zeros(n, dtype=int)   # +1 completed up-9, -1 completed down-9 on that bar
    failed = np.zeros(n, dtype=int)  # count value (signed) when a sequence died before 9
    k = 0
    dirn = 0
    for i in range(n):
        if i >= 4:
            up, dn = c[i] > c[i - 4], c[i] < c[i - 4]
            if up or dn:
                nd = 1 if up else -1
                if nd != dirn:
                    if 0 < k < 9:
                        failed[i] = dirn * k
                    dirn, k = nd, 1
                elif k < 9:
                    k += 1
                    if k == 9:
                        done9[i] = dirn
            else:
                if 0 < k < 9:
                    failed[i] = dirn * k
                k, dirn = 0, 0
        cnt[i], direction[i] = k, dirn
    out["count"], out["count_dir"] = cnt, direction
    out["nine"], out["count_failed"] = done9, failed

    # anchors
    hi_b, lo_b = p.highest(df["high"], 50), p.lowest(df["low"], 50)
    piv_hi = (df["high"].shift(1) == hi_b.shift(1)) & (df["high"] < hi_b)
    piv_lo = (df["low"].shift(1) == lo_b.shift(1)) & (df["low"] > lo_b)
    vol = df["volume"] if "volume" in df else pd.Series(0.0, index=df.index)
    a_dn = p.anchored_vwap(df["high"], vol, piv_hi.fillna(False), anchor_from_pivot_bar)
    a_up = p.anchored_vwap(df["low"], vol, piv_lo.fillna(False), anchor_from_pivot_bar)
    state = np.zeros(n, dtype=bool)
    s = False
    hb, lb, hi, lo = hi_b.to_numpy(), lo_b.to_numpy(), df["high"].to_numpy(), df["low"].to_numpy()
    for i in range(n):
        if not np.isnan(hb[i]) and hi[i] == hb[i]:
            s = True
        if not np.isnan(lb[i]) and lo[i] == lb[i]:
            s = False
        state[i] = s
    out["state_up"] = state
    out["anchor"] = np.where(state, a_up, a_dn)
    out["anchor_is_support"] = state
    return out


# --------------------------------------------------------------------------- all
def compute_all(df: pd.DataFrame, v2: bool = True) -> pd.DataFrame:
    """All IFI components plus ATR on one frame. v2=True applies the 2.0 corrections."""
    parts = [
        ad(df, mirror_divergence=v2).add_prefix("ad_"),
        signals(df, direction_fix=v2).add_prefix("sig_"),
        matrix(df).add_prefix("mx_"),
        trend(df, anchor_from_pivot_bar=v2).add_prefix("tr_"),
    ]
    out = pd.concat([df] + parts, axis=1)
    out["atr"] = p.atr(df, 14)
    return out
