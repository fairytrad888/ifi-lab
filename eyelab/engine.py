"""Process advantage: does the rule's entry beat matched null entries on the same geometry?

For every signal (bar t, entry at the open of t+1, unit u = the rule's 1R distance):
  fp1 / fp2  first passage: 1 if price reaches entry + k*u before entry - u within H bars, else 0
             (a bar touching both counts as a loss; reaching neither by H is a 0 and counted as a timeout)
  fwd_h      close at t+h minus entry, in units of u
Nulls, built with the same unit definition at the null bar:
  cross      same date, other symbols of the pool (removes that day's market move)
  time       same symbol, random other dates (keeps the symbol's own drift and volatility)
Advantage of a signal = its outcome - the mean of its nulls. Inference: bootstrap over calendar months.
Binary first-passage outcomes have about a tenth of the variance of trade R, so they resolve far faster.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import guard
from .guard import CFG


def _check_blind():
    if guard.is_blind():
        raise PermissionError("blind mode: outcomes are never computed during fidelity work")


def metric_names(tf: str) -> list[str]:
    return [m["name"] for m in CFG["outcomes"]["first_passage"]] + [f"fwd{h}" for h in CFG["outcomes"]["forward"][tf]]


def max_horizon(tf: str) -> int:
    return max([m["horizon"][tf] for m in CFG["outcomes"]["first_passage"]] + CFG["outcomes"]["forward"][tf]) + 1


class Arrays:
    """Numpy views of one symbol's frame."""
    __slots__ = ("o", "h", "l", "c", "u", "dates", "n", "elig")

    def __init__(self, x: pd.DataFrame, u: pd.Series, tf: str):
        self.o, self.h, self.l, self.c = (x[k].to_numpy(float) for k in ("open", "high", "low", "close"))
        self.u = u.reindex(x.index).to_numpy(float)
        self.dates = x.index
        self.n = len(x)
        mh = max_horizon(tf)
        b = np.arange(self.n)
        self.elig = (b >= CFG["nulls"]["min_history_bars"]) & (b < self.n - mh) & np.isfinite(self.u) & (self.u > 0)


def outcome(a: Arrays, i: int, tf: str, direction: str) -> dict | None:
    """All metrics for an entry triggered on bar i. None if the bar is not eligible (history, unit, or future)."""
    _check_blind()
    if not a.elig[i]:
        return None
    sgn = 1.0 if direction == "long" else -1.0
    j = i + 1
    entry, u = a.o[j], a.u[i]
    out = {}
    for m in CFG["outcomes"]["first_passage"]:
        H, k = m["horizon"][tf], m["k"]
        hs, ls = a.h[j:j + H], a.l[j:j + H]
        if sgn > 0:
            win, loss = hs >= entry + k * u, ls <= entry - u
        else:
            win, loss = ls <= entry - k * u, hs >= entry + u
        wi = int(np.argmax(win)) if win.any() else H
        li = int(np.argmax(loss)) if loss.any() else H
        out[m["name"]] = 1.0 if wi < li else 0.0          # same bar (wi == li < H) -> loss
        out[m["name"] + "_timeout"] = 1.0 if wi == H and li == H else 0.0
    for h in CFG["outcomes"]["forward"][tf]:
        out[f"fwd{h}"] = sgn * (a.c[i + h] - entry) / u
    return out


def evaluate(frames: dict[str, pd.DataFrame], sig: dict[str, pd.Series], unit: dict[str, pd.Series], tf: str,
             direction: str, seed: int | None = None, exclude: set[str] = frozenset()) -> pd.DataFrame:
    """One row per eligible signal: its metrics, the mean metrics of its cross and time nulls, and advantages."""
    _check_blind()
    rng = np.random.default_rng(CFG["nulls"]["seed"] if seed is None else seed)
    M = CFG["nulls"]["per_signal"]
    syms = sorted(s for s in frames if s not in exclude)
    arr = {s: Arrays(frames[s], unit[s], tf) for s in syms}
    # date -> eligible (sym, bar) for the cross null
    by_date: dict[pd.Timestamp, list[tuple[str, int]]] = {}
    for s in syms:
        a = arr[s]
        for i in np.flatnonzero(a.elig):
            by_date.setdefault(a.dates[i], []).append((s, int(i)))
    names = metric_names(tf)
    rows = []
    for s in syms:
        a = arr[s]
        eidx = np.flatnonzero(a.elig)
        for i in np.flatnonzero(sig[s].reindex(frames[s].index).fillna(False).to_numpy(bool)):
            o = outcome(a, int(i), tf, direction)
            if o is None:
                continue
            row = {"symbol": s, "date": a.dates[i], "bar": int(i), **o}
            # time null: same symbol, other eligible dates
            tn = rng.choice(eidx, size=M, replace=len(eidx) < M + 1)
            tvals = [outcome(a, int(t), tf, direction) for t in tn]
            # cross null: same date, other symbols
            pool = [p for p in by_date.get(a.dates[i], []) if p[0] != s]
            if pool:
                pick = rng.choice(len(pool), size=M, replace=len(pool) < M)
                cvals = [outcome(arr[pool[k][0]], pool[k][1], tf, direction) for k in pick]
            else:
                cvals = []
            for nm in names:
                tv = [v[nm] for v in tvals if v is not None]
                cv = [v[nm] for v in cvals if v is not None]
                row[f"{nm}_time"] = float(np.mean(tv)) if tv else np.nan
                row[f"{nm}_cross"] = float(np.mean(cv)) if cv else np.nan
                row[f"{nm}_adv_time"] = row[nm] - row[f"{nm}_time"]
                row[f"{nm}_adv_cross"] = row[nm] - row[f"{nm}_cross"]
            rows.append(row)
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------- inference
def cluster_boot(values: np.ndarray, clusters: np.ndarray, B: int | None = None, seed: int | None = None) -> dict:
    v = np.asarray(values, float)
    ok = np.isfinite(v)
    v, cl = v[ok], np.asarray(clusters)[ok]
    if len(v) < 2:
        return {"n": int(len(v)), "mean": float(v.mean()) if len(v) else np.nan, "lo": np.nan, "hi": np.nan, "p": np.nan, "deff": np.nan}
    B = B or CFG["inference"]["boot"]
    rng = np.random.default_rng(CFG["inference"]["seed"] if seed is None else seed)
    keys, inv = np.unique(cl, return_inverse=True)
    s = np.bincount(inv, weights=v)
    c = np.bincount(inv).astype(float)
    draw = rng.integers(0, len(keys), size=(B, len(keys)))
    means = s[draw].sum(1) / c[draw].sum(1)
    var_iid = v.var(ddof=1) / len(v)
    return {"n": int(len(v)), "mean": float(v.mean()), "lo": float(np.quantile(means, 0.025)),
            "hi": float(np.quantile(means, 0.975)), "p": float((means <= 0).mean()),
            "deff": float(means.var(ddof=1) / var_iid) if var_iid > 0 else np.nan, "sd": float(v.std(ddof=1))}


def n_needed(effect: float, sd: float, deff: float, z: float = 1.645 + 0.842) -> float:
    """Signals needed for 80% power, one-sided 5%, at a given mean advantage (clustered)."""
    if not (effect and effect > 0 and np.isfinite(sd) and np.isfinite(deff)):
        return np.inf
    return float((z * sd / effect) ** 2 * max(deff, 1.0))


def summarize(df: pd.DataFrame, tf: str) -> dict:
    cl = pd.to_datetime(df["date"]).dt.to_period("M").astype(str).to_numpy() if len(df) else np.array([])
    out = {}
    for nm in metric_names(tf):
        out[nm] = {"signal": float(df[nm].mean()) if len(df) else np.nan,
                   "cross": float(df[f"{nm}_cross"].mean()) if len(df) else np.nan,
                   "time": float(df[f"{nm}_time"].mean()) if len(df) else np.nan,
                   "adv_cross": cluster_boot(df[f"{nm}_adv_cross"].to_numpy(), cl) if len(df) else {},
                   "adv_time": cluster_boot(df[f"{nm}_adv_time"].to_numpy(), cl) if len(df) else {}}
    return out


def halves_split(df: pd.DataFrame) -> pd.Timestamp:
    """The two time halves are split at the median signal date (works for any pool or history length)."""
    return pd.to_datetime(df["date"]).sort_values().iloc[len(df) // 2]


def primary_verdict(df: pd.DataFrame, tf: str) -> dict:
    p = CFG["primary"]
    nm, null = p["metric"], p["vs_null"]
    other = "time" if null == "cross" else "cross"
    cl = pd.to_datetime(df["date"]).dt.to_period("M").astype(str).to_numpy()
    main = cluster_boot(df[f"{nm}_adv_{null}"].to_numpy(), cl)
    sec = float(df[f"{nm}_adv_{other}"].mean())
    split = halves_split(df)
    early = df[pd.to_datetime(df["date"]) < split][f"{nm}_adv_{null}"].mean()
    late = df[pd.to_datetime(df["date"]) >= split][f"{nm}_adv_{null}"].mean()
    ok = bool(main["lo"] > 0 and sec > 0 and early > 0 and late > 0)
    return {"metric": nm, "null": null, "main": main, f"adv_{other}_mean": sec, "split": str(split)[:10],
            "half_before": float(early), "half_after": float(late), "pass": ok}
