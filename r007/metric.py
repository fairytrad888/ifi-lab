"""Within-week tier spread, week bootstrap, halves and Holm (prereg `metric`, `phase1`, `phase2`)."""
from __future__ import annotations

import numpy as np
import pandas as pd


def tiers(score: np.ndarray, cuts: tuple[float, float]) -> np.ndarray:
    """0 = C (bottom third), 1 = B, 2 = A (top third) by fixed cut points."""
    s = np.asarray(score, dtype=float)
    return np.where(s > cuts[1], 2, np.where(s > cuts[0], 1, 0))


def tercile_cuts(score: np.ndarray) -> tuple[float, float]:
    q = np.nanquantile(np.asarray(score, dtype=float), [1 / 3, 2 / 3])
    return float(q[0]), float(q[1])


def week_terms(week: np.ndarray, tier: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Per contributing week (>= 1 A and >= 1 C): A-C mean difference d, weight h = nA nC / (nA + nC), week id."""
    wk = pd.factorize(np.asarray(week))[0]
    K = wk.max() + 1 if len(wk) else 0
    t, yv = np.asarray(tier), np.asarray(y, dtype=float)
    nA = np.bincount(wk, weights=(t == 2).astype(float), minlength=K)
    nC = np.bincount(wk, weights=(t == 0).astype(float), minlength=K)
    sA = np.bincount(wk, weights=np.where(t == 2, yv, 0.0), minlength=K)
    sC = np.bincount(wk, weights=np.where(t == 0, yv, 0.0), minlength=K)
    ok = (nA > 0) & (nC > 0)
    d = sA[ok] / nA[ok] - sC[ok] / nC[ok]
    h = nA[ok] * nC[ok] / (nA[ok] + nC[ok])
    labels = pd.factorize(np.asarray(week))[1]
    return d, h, np.asarray(labels)[ok]


def spread(d: np.ndarray, h: np.ndarray) -> float:
    return float(np.sum(h * d) / np.sum(h)) if len(d) else float("nan")


def boot(d: np.ndarray, h: np.ndarray, draws: int, seed: int, chunk: int = 500) -> np.ndarray:
    rng = np.random.default_rng(seed)
    K = len(d)
    out = np.empty(draws)
    for a in range(0, draws, chunk):
        b = min(draws, a + chunk)
        idx = rng.integers(0, K, size=(b - a, K))
        hh = h[idx]
        out[a:b] = (hh * d[idx]).sum(axis=1) / hh.sum(axis=1)
    return out


def one_sided_p(draws: np.ndarray) -> float:
    return float(np.mean(draws <= 0))


def holm(pvals: dict[str, float], alpha: float) -> dict[str, bool]:
    """Holm step-down; True = rejected (passes)."""
    order = sorted(pvals, key=lambda k: pvals[k])
    m, res, stop = len(order), {}, False
    for j, k in enumerate(order):
        if not stop and pvals[k] <= alpha / (m - j):
            res[k] = True
        else:
            stop = True
            res[k] = False
    return res


def evaluate(week, tier, y, halves, draws: int, seed: int) -> dict:
    """Spread, bootstrap p and the two halves for one model's tiers."""
    week = pd.to_datetime(pd.Series(week)).to_numpy()
    d, h, wl = week_terms(week, tier, y)
    est = spread(d, h)
    if len(d):
        bs = boot(d, h, draws, seed)
        out = {"spread": est, "p": one_sided_p(bs), "weeks": int(len(d)), "lo90": float(np.quantile(bs, 0.05)),
               "hi90": float(np.quantile(bs, 0.95)), "halves": []}
    else:
        out = {"spread": est, "p": float("nan"), "weeks": 0, "lo90": float("nan"), "hi90": float("nan"), "halves": []}
    wl = pd.to_datetime(wl)
    for a, b in halves:
        m = (wl >= pd.Timestamp(a)) & (wl <= pd.Timestamp(b))
        out["halves"].append(spread(d[m], h[m]))
    return out


def gate(res: dict, min_spread: float, half_min: float) -> dict:
    """Phase 1 point and halves rules (the p rule is applied with Holm across models)."""
    return {"spread_ok": res["spread"] >= min_spread,
            "halves_ok": all(v == v and v >= half_min for v in res["halves"])}
