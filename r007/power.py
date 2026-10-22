"""Synthetic power on the real event-week structure (prereg phase0.power).

Each event keeps its real week; scores are random, so tiers are random thirds. Outcomes are +2R / -1R draws with a
week-level probability shock (crash weeks) and a planted A-C spread in R. No real outcome is involved.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import metric


def simulate(weeks: np.ndarray, spread_R: float, reps: int, draws: int, seed: int, p_base: float, week_sd: float,
             halves, min_spread: float, half_min: float, alpha: float = 0.05, fixed_tiers: np.ndarray | None = None) -> dict:
    """fixed_tiers: use these tiers (0 C, 1 B, 2 A; e.g. model W's, which involve no outcome) instead of random thirds."""
    rng = np.random.default_rng(seed)
    wk = pd.to_datetime(pd.Series(weeks)).to_numpy()
    codes, uniq = pd.factorize(wk)
    n, K = len(codes), len(uniq)
    d_p = spread_R / 3.0                                   # A-C in probability: (+2) - (-1) = 3R per unit
    sig, sig_holm, gate_pass, ests = 0, 0, 0, []
    for r in range(reps):
        pw = np.clip(p_base + rng.normal(0, week_sd, K), 0.02, 0.98)
        if fixed_tiers is not None:
            tier = np.asarray(fixed_tiers, dtype=int)
        else:
            tier = np.empty(n, dtype=int)
            perm = rng.permutation(n)
            tier[perm] = np.repeat([0, 1, 2], [n // 3, n // 3, n - 2 * (n // 3)])
        p = np.clip(pw[codes] + (tier - 1) * d_p / 2.0, 0.005, 0.995)
        y = np.where(rng.random(n) < p, 2.0, -1.0)
        res = metric.evaluate(wk, tier, y, halves, draws, seed + 1 + r)
        g = metric.gate(res, min_spread, half_min)
        ests.append(res["spread"])
        pv = res["p"] if res["p"] == res["p"] else 1.0
        sig += pv < alpha
        sig_holm += pv < alpha / 2
        gate_pass += (pv < alpha) and g["spread_ok"] and g["halves_ok"]
    return {"spread_R": spread_R, "events": n, "weeks_with_events": K, "power": sig / reps,
            "power_holm_worst": sig_holm / reps, "gate_pass": gate_pass / reps,
            "mean_est": float(np.nanmean(ests)) if np.isfinite(ests).any() else float("nan"),
            "sd_est": float(np.nanstd(ests)) if np.isfinite(ests).any() else float("nan")}


def table(weeks: np.ndarray, P: dict, halves, min_spread: float, half_min: float,
          fixed_tiers: np.ndarray | None = None) -> list[dict]:
    return [simulate(weeks, s, P["reps"], P["boot"], P["seed"] + int(round(s * 1000)), P["p_base"], P["week_sd"],
                     halves, min_spread, half_min, fixed_tiers=fixed_tiers) for s in P["spreads_reported"]]
