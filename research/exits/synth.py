"""Synthetic price markets for validating the exit test (no real data).

martingale_loader : prices with zero drift in PRICE terms (log drift -sigma^2/2). No exit can have a real
                    advantage, and holding longer earns nothing, so a correct pipeline reports no PASS.
trend_loader      : prices with persistent up/down regimes (Markov switching). Letting a real trend run is
                    genuinely better than a fixed target here, so the structural exit X10 must PASS.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

DAYS = pd.bdate_range("1998-01-02", "2026-10-09")


def _bars(logc: np.ndarray, rng) -> pd.DataFrame:
    c = 100 * np.exp(logc)
    o = np.r_[c[0], c[:-1]] * np.exp(rng.normal(0, 0.003, len(c)))
    hi = np.maximum(o, c) * np.exp(np.abs(rng.normal(0, 0.006, len(c))))
    lo = np.minimum(o, c) * np.exp(-np.abs(rng.normal(0, 0.006, len(c))))
    vol = rng.integers(1_000_000, 5_000_000, len(c)).astype(float)
    return pd.DataFrame({"open": o, "high": hi, "low": lo, "close": c, "volume": vol}, index=DAYS)


def martingale_loader(seed: int = 3, sd: float = 0.015):
    rng = np.random.default_rng(seed)
    cache: dict[str, pd.DataFrame] = {}

    def f(sym: str) -> pd.DataFrame:
        if sym not in cache:
            cache[sym] = _bars(np.cumsum(rng.normal(-0.5 * sd * sd, sd, len(DAYS))), rng)
        return cache[sym]
    return f


def trend_loader(seed: int = 5, mu: float = 0.002, mean_len: int = 120, sd: float = 0.013):
    rng = np.random.default_rng(seed)
    cache: dict[str, pd.DataFrame] = {}

    def f(sym: str) -> pd.DataFrame:
        if sym not in cache:
            n = len(DAYS)
            state = rng.choice([-1, 1])
            drift = np.empty(n)
            for i in range(n):
                if rng.random() < 1.0 / mean_len:
                    state = -state
                drift[i] = state * mu
            cache[sym] = _bars(np.cumsum(drift - 0.5 * sd * sd + rng.normal(0, sd, n)), rng)
        return cache[sym]
    return f
