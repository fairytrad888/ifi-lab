"""Pine Script primitives reproduced in pandas/numpy.

Conventions follow TradingView's documented behaviour:
- ema / rma are seeded with the SMA of the first `n` valid values (Pine's reference implementation).
- Division by zero yields NaN (Pine returns na).
- crossover(a, b): a > b and a[1] <= b[1].
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def _arr(x) -> np.ndarray:
    return np.asarray(x, dtype=float)


def sma(x: pd.Series, n: int) -> pd.Series:
    return x.rolling(n, min_periods=n).mean()


def wma(x: pd.Series, n: int) -> pd.Series:
    w = np.arange(1, n + 1, dtype=float)
    return x.rolling(n, min_periods=n).apply(lambda v: np.dot(v, w) / w.sum(), raw=True)


def _seeded_recursive(x: pd.Series, n: int, alpha: float) -> pd.Series:
    v = _arr(x)
    out = np.full(v.shape, np.nan)
    valid = ~np.isnan(v)
    # first index where n consecutive valid values are available
    run = 0
    start = None
    for i in range(len(v)):
        run = run + 1 if valid[i] else 0
        if run >= n:
            start = i
            break
    if start is None:
        return pd.Series(out, index=x.index)
    out[start] = v[start - n + 1:start + 1].mean()
    prev = out[start]
    for i in range(start + 1, len(v)):
        if np.isnan(v[i]):
            out[i] = prev
            continue
        prev = alpha * v[i] + (1 - alpha) * prev
        out[i] = prev
    return pd.Series(out, index=x.index)


def ema(x: pd.Series, n: int) -> pd.Series:
    return _seeded_recursive(x, n, 2.0 / (n + 1))


def rma(x: pd.Series, n: int) -> pd.Series:
    return _seeded_recursive(x, n, 1.0 / n)


def rsi(x: pd.Series, n: int = 14) -> pd.Series:
    ch = x.diff()
    up = rma(ch.clip(lower=0), n)
    dn = rma((-ch).clip(lower=0), n)
    out = 100 - 100 / (1 + up / dn)
    out = out.where(dn != 0, 100.0)
    out = out.where(up != 0, 0.0)
    out[up.isna() | dn.isna()] = np.nan
    return out


def highest(x: pd.Series, n: int) -> pd.Series:
    return x.rolling(n, min_periods=n).max()


def lowest(x: pd.Series, n: int) -> pd.Series:
    return x.rolling(n, min_periods=n).min()


def stoch(close: pd.Series, high: pd.Series, low: pd.Series, n: int) -> pd.Series:
    hh, ll = highest(high, n), lowest(low, n)
    rng = (hh - ll).replace(0, np.nan)
    return 100 * (close - ll) / rng


def true_range(df: pd.DataFrame) -> pd.Series:
    pc = df["close"].shift(1)
    tr = pd.concat([df["high"] - df["low"], (df["high"] - pc).abs(), (df["low"] - pc).abs()], axis=1).max(axis=1)
    tr.iloc[0] = df["high"].iloc[0] - df["low"].iloc[0]
    return tr


def atr(df: pd.DataFrame, n: int = 14) -> pd.Series:
    return rma(true_range(df), n)


def linreg(x: pd.Series, n: int, offset: int = 0) -> pd.Series:
    t = np.arange(n, dtype=float)
    tm = t.mean()
    denom = ((t - tm) ** 2).sum()

    def f(v):
        vm = v.mean()
        slope = ((t - tm) * (v - vm)).sum() / denom
        intercept = vm - slope * tm
        return intercept + slope * (n - 1 - offset)

    return x.rolling(n, min_periods=n).apply(f, raw=True)


def tsi(x: pd.Series, short: int, long: int) -> pd.Series:
    pc = x.diff()
    num = ema(ema(pc, long), short)
    den = ema(ema(pc.abs(), long), short)
    return num / den.replace(0, np.nan)


def crossover(a: pd.Series, b) -> pd.Series:
    b = b if isinstance(b, pd.Series) else pd.Series(b, index=a.index)
    return (a > b) & (a.shift(1) <= b.shift(1))


def crossunder(a: pd.Series, b) -> pd.Series:
    b = b if isinstance(b, pd.Series) else pd.Series(b, index=a.index)
    return (a < b) & (a.shift(1) >= b.shift(1))


def cross(a: pd.Series, b) -> pd.Series:
    return crossover(a, b) | crossunder(a, b)


def pivot_high(x: pd.Series, left: int, right: int) -> pd.Series:
    """Value of the pivot on the bar where it is CONFIRMED (right bars later), else NaN.
    Center must be strictly greater than the left bars and >= the right bars."""
    v = _arr(x)
    out = np.full(v.shape, np.nan)
    for t in range(left + right, len(v)):
        c = t - right
        center = v[c]
        if np.isnan(center):
            continue
        lw, rw = v[c - left:c], v[c + 1:t + 1]
        if np.all(center > lw) and np.all(center >= rw):
            out[t] = center
    return pd.Series(out, index=x.index)


def pivot_low(x: pd.Series, left: int, right: int) -> pd.Series:
    v = _arr(x)
    out = np.full(v.shape, np.nan)
    for t in range(left + right, len(v)):
        c = t - right
        center = v[c]
        if np.isnan(center):
            continue
        lw, rw = v[c - left:c], v[c + 1:t + 1]
        if np.all(center < lw) and np.all(center <= rw):
            out[t] = center
    return pd.Series(out, index=x.index)


def anchored_vwap(src: pd.Series, volume: pd.Series, reset: pd.Series, include_prior_bar: bool = False) -> pd.Series:
    """Cumulative VWAP of `src` restarting on bars where `reset` is True.
    include_prior_bar=True starts the accumulation at the pivot bar (bar before confirmation),
    which is the standard anchored-VWAP definition (IFI 2.0); False reproduces Pine's ta.vwap(src, anchor).
    If volume is missing or zero, falls back to equal weights (TWAP)."""
    s, vol, r = _arr(src), _arr(volume.fillna(0)), reset.to_numpy(dtype=bool)
    use_twap = np.nansum(vol) == 0
    w = np.ones_like(vol) if use_twap else vol
    out = np.full(s.shape, np.nan)
    num = den = np.nan
    for i in range(len(s)):
        if r[i]:
            num, den = s[i] * w[i], w[i]
            if include_prior_bar and i > 0:
                num += s[i - 1] * w[i - 1]
                den += w[i - 1]
        elif not np.isnan(num):
            num += s[i] * w[i]
            den += w[i]
        if not np.isnan(num) and den > 0:
            out[i] = num / den
    return pd.Series(out, index=src.index)
