"""Model L: L2 logistic regression on O2 with time-blocked out-of-fold scores (prereg amendment_1.model_L_details).

Loss (sklearn convention): 0.5 * ||w||^2 + C * sum(log-loss), intercept unpenalized, solved by Newton steps.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

FLAGS = ["f_signals_trigger", "f_ad_divergence", "f_matrix_divergence", "f_down9", "f_accumulation_exit"]
ORDINAL = ["n_types", "red_age"]
BINARY = FLAGS + ["trig2", "leader"]
CONTINUOUS = ["flow_min", "breadth_acc", "breadth_stage2", "log_stop", "dist_anchor_atr"]
STAGES = [-1, 0, 1, 2, 3]
GSTATES = ["bullish", "basing", "neutral", "bearish", "missing"]
INPUTS = ORDINAL + BINARY + CONTINUOUS + ["stage", "group_state"]          # 16 inputs for leave-one-out
BLOCKS = [(2008, 2011), (2012, 2015), (2016, 2018), (2019, 2021), (2022, 2026)]
C_GRID = [0.03, 0.1, 0.3]


def base_frame(ev: pd.DataFrame) -> pd.DataFrame:
    x = pd.DataFrame(index=ev.index)
    for c in ORDINAL + FLAGS + ["trig2", "flow_min", "dist_anchor_atr"]:
        x[c] = pd.to_numeric(ev[c], errors="coerce")
    x["leader"] = pd.to_numeric(ev["leader"], errors="coerce").fillna(0.0)
    x["breadth_acc"] = pd.to_numeric(ev["breadth_acc"], errors="coerce").fillna(0.0)
    x["breadth_stage2"] = pd.to_numeric(ev["breadth_stage2"], errors="coerce").fillna(0.0)
    x["log_stop"] = np.log(np.maximum(pd.to_numeric(ev["stop_pct"], errors="coerce").fillna(0.0), 0.005))
    x["stage"] = pd.to_numeric(ev["stage"], errors="coerce").fillna(0).astype(int)
    x["group_state"] = ev["group_state"].fillna("missing").astype(str)
    return x


class Design:
    """Training-fitted transforms: medians, winsor limits, means and sds; one-hot levels fixed."""

    def __init__(self, xtr: pd.DataFrame, drop: str | None = None):
        self.drop = drop
        self.med = {"dist_anchor_atr": float(xtr["dist_anchor_atr"].median())}
        z = self._raw(xtr, fit=True)
        self.mu = z.mean(axis=0)
        sd = z.std(axis=0)
        self.sd = np.where(sd > 1e-12, sd, 1.0)

    def _raw(self, x: pd.DataFrame, fit: bool = False) -> np.ndarray:
        x = x.copy()
        x["dist_anchor_atr"] = x["dist_anchor_atr"].fillna(self.med["dist_anchor_atr"])
        if fit:
            self.lim = {c: (float(x[c].quantile(0.01)), float(x[c].quantile(0.99))) for c in CONTINUOUS}
        for c in CONTINUOUS:
            x[c] = x[c].clip(*self.lim[c])
        cols = []
        for c in ORDINAL + BINARY + CONTINUOUS:
            if c != self.drop:
                cols.append(x[c].fillna(0.0).to_numpy(dtype=float))
        if self.drop != "stage":
            cols += [(x["stage"] == s).to_numpy(dtype=float) for s in STAGES]
        if self.drop != "group_state":
            cols += [(x["group_state"] == g).to_numpy(dtype=float) for g in GSTATES]
        return np.column_stack(cols)

    def __call__(self, x: pd.DataFrame) -> np.ndarray:
        return (self._raw(x) - self.mu) / self.sd


def fit_logit(X: np.ndarray, y: np.ndarray, C: float, iters: int = 100) -> np.ndarray:
    n, k = X.shape
    Xa = np.column_stack([np.ones(n), X])
    w = np.zeros(k + 1)
    pen = np.ones(k + 1)
    pen[0] = 0.0
    for _ in range(iters):
        z = Xa @ w
        p = 1.0 / (1.0 + np.exp(-z))
        g = pen * w + C * Xa.T @ (p - y)
        H = np.diag(pen) + C * (Xa.T * (p * (1 - p))) @ Xa
        step = np.linalg.solve(H + 1e-10 * np.eye(k + 1), g)
        w -= step
        if np.max(np.abs(step)) < 1e-9:
            break
    return w


def predict(w: np.ndarray, X: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-(w[0] + X @ w[1:])))


def logloss(p: np.ndarray, y: np.ndarray) -> float:
    p = np.clip(p, 1e-9, 1 - 1e-9)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def block_of(years: np.ndarray) -> np.ndarray:
    b = np.full(len(years), -1)
    for k, (a, z) in enumerate(BLOCKS):
        b[(years >= a) & (years <= z)] = k
    return b


def _fit_predict(x: pd.DataFrame, y: np.ndarray, tr: np.ndarray, te: np.ndarray, C: float, drop: str | None = None):
    D = Design(x[tr], drop)
    w = fit_logit(D(x[tr]), y[tr], C)
    return predict(w, D(x[te])), predict(w, D(x[tr]))


def oof(ev: pd.DataFrame, y: np.ndarray, extra: pd.DataFrame | None = None) -> dict:
    """Out-of-fold probabilities, tiers (training terciles per fold), chosen C per fold, leave-one-out contributions.
    `extra` (e.g. skipped events, no label) is scored by its own block's model and cut points, for counts only."""
    x = base_frame(ev).reset_index(drop=True)
    xe = base_frame(extra).reset_index(drop=True) if extra is not None and len(extra) else None
    be = block_of(pd.to_datetime(extra["week"]).dt.year.to_numpy()) if xe is not None else None
    extra_tier = np.full(len(xe) if xe is not None else 0, -1)
    y = np.asarray(y, dtype=float)
    years = pd.to_datetime(ev["week"]).dt.year.to_numpy()
    blk = block_of(years)
    p_oof = np.full(len(x), np.nan)
    tier = np.full(len(x), -1)
    base = np.full(len(x), np.nan)
    chosen = {}
    for k in range(len(BLOCKS)):
        te, trb = blk == k, [j for j in range(len(BLOCKS)) if j != k]
        tr = np.isin(blk, trb)
        if te.sum() == 0 or tr.sum() == 0:
            continue
        scores = {}
        for C in C_GRID:
            ll = []
            for j in trb:
                itr, ite = tr & (blk != j), blk == j
                if ite.sum() == 0 or itr.sum() == 0:
                    continue
                pj, _ = _fit_predict(x, y, itr, ite, C)
                ll.append(logloss(pj, y[ite]))
            scores[C] = float(np.mean(ll)) if ll else np.inf
        C = min(C_GRID, key=lambda c: (scores[c], c))
        chosen[k] = {"C": C, "inner_logloss": scores}
        D = Design(x[tr])
        w = fit_logit(D(x[tr]), y[tr], C)
        p_te, p_tr = predict(w, D(x[te])), predict(w, D(x[tr]))
        q = np.quantile(p_tr, [1 / 3, 2 / 3])
        if xe is not None and (be == k).any():
            pe = predict(w, D(xe[be == k]))
            extra_tier[be == k] = np.where(pe > q[1], 2, np.where(pe > q[0], 1, 0))
        p_oof[te] = p_te
        tier[te] = np.where(p_te > q[1], 2, np.where(p_te > q[0], 1, 0))
        base[te] = float(y[tr].mean())
    ok = ~np.isnan(p_oof)
    ll_model, ll_base = logloss(p_oof[ok], y[ok]), logloss(base[ok], y[ok])
    loo = {}
    for inp in INPUTS:
        p_d = np.full(len(x), np.nan)
        for k, ch in chosen.items():
            te, tr = blk == k, (blk != k) & (blk >= 0)
            p_d[te], _ = _fit_predict(x, y, tr, te, ch["C"], drop=inp)
        loo[inp] = logloss(p_d[ok], y[ok]) - ll_model         # > 0: the input helps out of fold
    dec = pd.qcut(pd.Series(p_oof[ok]), 10, labels=False, duplicates="drop")
    cal = pd.DataFrame({"decile": dec.to_numpy(), "pred": p_oof[ok], "obs": y[ok]}).groupby("decile").agg(
        n=("obs", "size"), predicted=("pred", "mean"), observed=("obs", "mean")).reset_index()
    return {"p": p_oof, "tier": tier, "chosen": chosen, "logloss_model": ll_model, "logloss_base": ll_base,
            "loo": loo, "calibration": cal, "extra_tier": extra_tier}
