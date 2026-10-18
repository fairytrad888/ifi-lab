"""Rule registry. A rule is one file eyelab/rules/<ID>.py with:

  SPEC = {id, version, name, eye_description, timeframe (D/W/H4), direction (long/short), status, ...}
  def signal(x) -> bool Series        # True on bar t when the rule fires; x = features.frame(...)
  def unit(x) -> float Series         # optional: the 1R distance in price at bar t (default 1 x ATR)

A rule may only use bars up to t (the look-ahead test enforces it). Status values:
  demo (self-test only) | draft | fidelity_passed | discovery | locked | confirmed | rejected
"""
from __future__ import annotations

import hashlib
import importlib

import numpy as np
import pandas as pd

from .guard import CFG, ROOT

REQUIRED = ("id", "version", "name", "eye_description", "timeframe", "direction", "status")


def path(rule_id: str):
    return ROOT / "rules" / f"{rule_id}.py"


def load_rule(rule_id: str):
    if not path(rule_id).exists():
        raise FileNotFoundError(f"no rule file eyelab/rules/{rule_id}.py")
    mod = importlib.import_module(f"eyelab.rules.{rule_id}")
    spec = getattr(mod, "SPEC", None)
    if not spec or any(k not in spec for k in REQUIRED):
        raise ValueError(f"{rule_id}: SPEC must define {REQUIRED}")
    if spec["id"] != rule_id or spec["timeframe"] not in ("D", "W", "H4") or spec["direction"] not in ("long", "short"):
        raise ValueError(f"{rule_id}: bad SPEC id/timeframe/direction")
    return mod


def rule_sha(rule_id: str) -> str:
    return hashlib.sha256(path(rule_id).read_bytes()).hexdigest()


def fires(mod, x: pd.DataFrame) -> pd.Series:
    s = mod.signal(x).reindex(x.index).fillna(False).astype(bool)
    s &= x["bar"] >= CFG["nulls"]["min_history_bars"]
    return s


def units(mod, x: pd.DataFrame) -> pd.Series:
    if hasattr(mod, "unit"):
        u = pd.Series(mod.unit(x), index=x.index, dtype=float)
    else:
        u = CFG["outcomes"]["default_unit_atr"] * x["atr"]
    return u.where(u > 0)


def look_ahead_ok(mod, x: pd.DataFrame, cuts: int = 5, seed: int = 1) -> bool:
    """Signals and units on bars <= c must not change when bars after c are deleted."""
    full_s, full_u = fires(mod, x), units(mod, x)
    rng = np.random.default_rng(seed)
    n = len(x)
    if n < 400:
        return True
    from .features import enrich
    base = x[["open", "high", "low", "close", "volume"] + (["slot"] if "slot" in x else [])]
    bench = pd.DataFrame({"close": x["spy_close"]}) if "spy_close" in x else None
    for c in sorted(rng.integers(300, n - 1, size=cuts)):
        xt = enrich(base.iloc[: c + 1], None if bench is None else bench.iloc[: c + 1])
        st, ut = fires(mod, xt), units(mod, xt)
        if not st.equals(full_s.iloc[: c + 1]):
            return False
        a, b = ut.to_numpy(), full_u.iloc[: c + 1].to_numpy()
        if not np.allclose(np.nan_to_num(a, nan=-1), np.nan_to_num(b, nan=-1), rtol=1e-9, atol=1e-12):
            return False
    return True
