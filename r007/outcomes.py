"""R007 trade outcomes on the daily path (prereg `trade` and `outcomes`).

Locked in the Phase 0 deploy so the method is fixed before any outcome exists. In Phase 0 it may only score
synthetic data: real-data calls are refused until a later phase is deployed and opened (guard.outcomes_open).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import guard


def wilder_atr(d: pd.DataFrame, n: int = 14) -> pd.Series:
    pc = d["close"].shift(1)
    tr = pd.concat([d["high"] - d["low"], (d["high"] - pc).abs(), (d["low"] - pc).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1.0 / n, adjust=False, min_periods=n).mean()


def trade(daily: pd.DataFrame, week_end: str | pd.Timestamp, stop: float, T: dict, cutoff: str,
          synthetic: bool = False, atr: pd.Series | None = None) -> dict:
    """One event: entry at the next daily open after the event week, fixed stop, +T['target_R'] target, time cap."""
    if not guard.outcomes_open() and not (synthetic and daily.attrs.get("synthetic") is True):
        raise RuntimeError("R007: outcomes are closed in this phase (no real-data outcome may be computed)")
    we = pd.Timestamp(week_end)
    cut = pd.Timestamp(cutoff)
    d = daily[daily.index <= cut]
    pre = d[d.index <= we]
    post = d[d.index > we]
    if pre.empty or post.empty:
        return {"skip": "no data"}
    a = (atr if atr is not None else wilder_atr(d)).reindex([pre.index[-1]]).iloc[0]
    entry = float(post["open"].iloc[0])
    if entry <= stop:
        return {"skip": "entry open <= stop"}
    risk = entry - stop
    if not np.isfinite(a) or risk < 0.5 * a:
        return {"skip": "risk < 0.5 ATR"}
    target = entry + T["target_R"] * risk
    cap_day = we + pd.Timedelta(weeks=T["time_cap_weeks"])
    path = post[post.index <= cap_day]
    c = T["cost_per_side"]
    exit_px, why, when = None, None, None
    for k, (dt, bar) in enumerate(path.iterrows()):
        o, h, lo = float(bar["open"]), float(bar["high"]), float(bar["low"])
        if k > 0 and o <= stop:
            exit_px, why = o, "gap below stop"
        elif k > 0 and o >= target:
            exit_px, why = o, "gap above target"
        elif lo <= stop:                       # same day both: the stop is assumed first
            exit_px, why = stop, "stop"
        elif h >= target:
            exit_px, why = target, "target"
        if why:
            when = dt
            break
    if why is None:
        if path.empty:
            return {"skip": "no data"}
        exit_px, when = float(path["close"].iloc[-1]), path.index[-1]
        why = "time cap" if (cap_day <= cut and when >= cap_day - pd.Timedelta(days=7)) else "data end"
    R = (exit_px - entry - c * (entry + exit_px)) / risk
    return {"skip": None, "entry_date": post.index[0].date().isoformat(), "entry": entry, "stop": stop,
            "risk": risk, "target": target, "exit_date": when.date().isoformat(), "exit": exit_px, "exit_reason": why,
            "R": R, "O2": int(why in ("target", "gap above target")), "O3": int(R <= -1.25)}
