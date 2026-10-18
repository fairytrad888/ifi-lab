"""The IFI reading of a chart (vendored IFI 2.0 indicator code, byte-identical to the prior system's at freeze)
plus the columns rules most often need. One call per symbol and timeframe; cached in memory."""
from __future__ import annotations

from functools import lru_cache

import numpy as np
import pandas as pd

from .core.states import read
from .data import load


@lru_cache(maxsize=64)
def _bench(tf: str, purpose: str) -> pd.DataFrame | None:
    return load("bench", "SPY", tf, purpose)


def frame(pool: str, sym: str, tf: str, purpose: str, until=None, extra_bars: int = 0) -> pd.DataFrame | None:
    df = load(pool, sym, tf, purpose, until=until, extra_bars=extra_bars)
    if df is None or len(df) < 60:
        return None
    return enrich(df, _bench(tf, purpose))


def enrich(df: pd.DataFrame, bench: pd.DataFrame | None = None) -> pd.DataFrame:
    x = read(df[["open", "high", "low", "close", "volume"] + (["slot"] if "slot" in df else [])], bench)
    x["bar"] = np.arange(len(x))
    x["sma50"] = x["close"].rolling(50, min_periods=50).mean()
    x["sma200"] = x["close"].rolling(200, min_periods=200).mean()
    x["hh20"] = x["high"].rolling(20, min_periods=20).max()
    x["ll20"] = x["low"].rolling(20, min_periods=20).min()
    if bench is not None:
        b = bench["close"].reindex(x.index).ffill()
        x["spy_close"] = b
        bs = b.rolling(200, min_periods=200).mean()
        x["spy_trend_up"] = ((b > bs) & (bs > bs.shift(20))).fillna(False)
    else:
        x["spy_trend_up"] = False
    return x
