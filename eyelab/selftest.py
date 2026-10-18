"""Self-tests of the Eye Lab machinery on synthetic markets (no downloads, no real data).

  null    : a rule that fires at random on random walks must show no advantage; the pass rate of the locked
            primary rule across worlds must stay near or below 5%
  power   : a rule followed by a planted drift must be detected
  geometry: first-passage counting on hand-made bars
  blind   : outcomes refuse to compute in blind mode
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import engine, guard


def world(n_sym: int = 40, n_bar: int = 2000, seed: int = 0, rate: float = 0.01, drift: float = 0.0,
          drift_bars: int = 10, vol: float = 0.015):
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2004-01-01", periods=n_bar)
    frames, sig, unit = {}, {}, {}
    for k in range(n_sym):
        r = rng.normal(0, vol, n_bar)
        s = rng.random(n_bar) < rate
        s[:260] = False
        if drift:
            for t in np.flatnonzero(s):
                r[t + 1:t + 1 + drift_bars] += drift * vol
        c = 100 * np.exp(np.cumsum(r))
        o = np.r_[c[0], c[:-1]] * np.exp(rng.normal(0, vol * 0.2, n_bar))
        hi = np.maximum(o, c) * np.exp(np.abs(rng.normal(0, vol * 0.5, n_bar)))
        lo = np.minimum(o, c) * np.exp(-np.abs(rng.normal(0, vol * 0.5, n_bar)))
        x = pd.DataFrame({"open": o, "high": hi, "low": lo, "close": c}, index=dates)
        tr = np.maximum(hi - lo, np.maximum(abs(hi - np.r_[c[0], c[:-1]]), abs(lo - np.r_[c[0], c[:-1]])))
        x["atr"] = pd.Series(tr, index=dates).rolling(14).mean()
        x["bar"] = np.arange(n_bar)
        name = f"S{k:02d}"
        frames[name], sig[name], unit[name] = x, pd.Series(s, index=dates), x["atr"]
    return frames, sig, unit


def null_calibration(worlds: int = 12) -> dict:
    passes, means = 0, []
    for w in range(worlds):
        f, s, u = world(seed=100 + w)
        df = engine.evaluate(f, s, u, "D", "long", seed=w)
        pv = engine.primary_verdict(df, "D")
        passes += int(pv["pass"])
        means.append(pv["main"]["mean"])
    return {"worlds": worlds, "pass_rate": passes / worlds, "mean_adv": float(np.mean(means)),
            "ok": passes / worlds <= 0.17 and abs(np.mean(means)) < 0.02}


def power(drift: float = 0.35) -> dict:
    f, s, u = world(seed=7, drift=drift)
    df = engine.evaluate(f, s, u, "D", "long", seed=1)
    pv = engine.primary_verdict(df, "D")
    return {"signals": len(df), "adv": pv["main"]["mean"], "lo": pv["main"]["lo"], "ok": bool(pv["pass"])}


def geometry() -> dict:
    idx = pd.bdate_range("2020-01-01", periods=400)
    x = pd.DataFrame({"open": 100.0, "high": 100.5, "low": 99.5, "close": 100.0}, index=idx)
    x["bar"] = np.arange(len(x))
    u = pd.Series(2.0, index=idx)
    i = 300
    x.iloc[i + 3, x.columns.get_loc("high")] = 102.5            # +1u (2.0) reached on entry bar + 2
    a = engine.Arrays(x, u, "D")
    win = engine.outcome(a, i, "D", "long")["fp1"]
    x2 = x.copy()
    x2.iloc[i + 2, x2.columns.get_loc("low")] = 97.5            # -1u reached first
    x2.iloc[i + 3, x2.columns.get_loc("high")] = 102.5
    loss = engine.outcome(engine.Arrays(x2, u, "D"), i, "D", "long")["fp1"]
    x3 = x.copy()
    x3.iloc[i + 3, x3.columns.get_loc("low")] = 97.5            # both on one bar -> loss
    both = engine.outcome(engine.Arrays(x3, u, "D"), i, "D", "long")["fp1"]
    flat = engine.outcome(engine.Arrays(x.assign(high=100.5), u, "D"), i, "D", "long")
    ok = win == 1.0 and loss == 0.0 and both == 0.0 and flat["fp1"] == 0.0 and flat["fp1_timeout"] == 1.0
    return {"win": win, "loss": loss, "both": both, "timeout": flat["fp1_timeout"], "ok": bool(ok)}


def blind() -> dict:
    f, s, u = world(n_sym=2, n_bar=600, seed=3)
    guard.enter_blind()
    try:
        engine.evaluate(f, s, u, "D", "long")
        refused = False
    except PermissionError:
        refused = True
    finally:
        guard.leave_blind()
    return {"ok": refused}


def run_all() -> dict:
    res = {"geometry": geometry(), "blind": blind(), "power": power(), "null": null_calibration()}
    res["ok"] = all(v["ok"] for v in res.values())
    return res
