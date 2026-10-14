"""Synthetic markets for pipeline validation (no real data involved).

null_loader    : independent random walks. Every ratio is pure noise, so a correct pipeline must report
                 no PASS for any test (a PASS would mean look-ahead or a statistics bug).
planted_loader : each ETF's return relative to SPY follows persistent up/down regimes (Markov switching,
                 drift +/-0.2% a day, mean regime 80 bars). Trend persistence is real here, so T1 and T3 must
                 detect it (else the pipeline is broken and the run aborts). T2, T5 and T6 have no planted
                 effect, so they should not pass (a specificity check, reported).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

DAYS = pd.bdate_range("1998-01-02", "2026-10-09")


def _bars(logc: np.ndarray, rng, days=DAYS) -> pd.DataFrame:
    c = 100 * np.exp(logc)
    o = np.r_[c[0], c[:-1]] * np.exp(rng.normal(0, 0.003, len(c)))
    hi = np.maximum(o, c) * np.exp(np.abs(rng.normal(0, 0.006, len(c))))
    lo = np.minimum(o, c) * np.exp(-np.abs(rng.normal(0, 0.006, len(c))))
    return pd.DataFrame({"open": o, "high": hi, "low": lo, "close": c, "volume": 1e6}, index=days)


def null_loader(seed: int = 3):
    rng = np.random.default_rng(seed)
    cache: dict[str, pd.DataFrame] = {}

    def f(sym: str) -> pd.DataFrame:
        if sym not in cache:
            cache[sym] = _bars(np.cumsum(rng.normal(0.0003, 0.012, len(DAYS))), rng)
        return cache[sym]
    return f


def planted_loader(seed: int = 5, mu: float = 0.002, mean_len: int = 80, rel_sd: float = 0.009):
    rng = np.random.default_rng(seed)
    n = len(DAYS)
    spy = np.cumsum(rng.normal(0.0003, 0.011, n))
    cache: dict[str, pd.DataFrame] = {"SPY": _bars(spy, rng)}

    def f(sym: str) -> pd.DataFrame:
        if sym not in cache:
            state = rng.choice([-1, 1])
            drift = np.empty(n)
            for i in range(n):
                if rng.random() < 1.0 / mean_len:
                    state = -state
                drift[i] = state * mu
            rel = np.cumsum(drift + rng.normal(0, rel_sd, n))
            cache[sym] = _bars(spy + rel, rng)
        return cache[sym]
    return f
