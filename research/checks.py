"""Validity checks shared by research/run.py and tests/test_research.py."""
from __future__ import annotations

import numpy as np

from research import engine as E
from research.common import ratio_bars
from research.synthetic import null_loader, planted_loader


def _event_sets(ev: dict, upto: int) -> dict:
    keep = lambda arr: set(int(i) for i in np.flatnonzero(arr) if i < upto)
    return dict(
        entries=set((e["t"], e["tier"]) for e in ev["entries"] if e["t"] < upto),
        r3=keep(ev["r3"]), stack=keep(ev["stack"]), touch_rise=keep(ev["touch_rise"]), touch_flat=keep(ev["touch_flat"]),
        warn=keep(ev["warn"]), breakdown=keep(ev["breakdown"]), wexit=keep(ev["wexit"]), bdiv=keep(ev["bdiv"]),
    )


def check_no_lookahead(P: dict | None = None, cuts=(1800, 3600, 5400)) -> tuple[bool, list[str]]:
    """Recompute everything on data cut at bar k; every event dated before k must be identical to the
    full-history run. Any difference means an event used information from after its own date."""
    P = dict(E.DEFAULTS, **(P or {}))
    msgs, ok = [], True
    for name, loader in (("random walk", null_loader(11)), ("planted trends", planted_loader(12))):
        r = ratio_bars(loader("AAA"), loader("SPY"))
        full = _event_sets(E.events(E.base(r), P), len(r))
        for k in cuts:
            cut = _event_sets(E.events(E.base(r.iloc[:k]), P), k)
            ref = {key: {v for v in val if (v[0] if isinstance(v, tuple) else v) < k} for key, val in full.items()}
            for key in ref:
                if ref[key] != cut[key]:
                    ok = False
                    msgs.append(f"{name}: '{key}' differs when data is cut at bar {k} "
                                f"(full {len(ref[key])}, cut {len(cut[key])})")
    if ok:
        n = sum(len(v) for v in full.values())
        msgs.append(f"identical events at {len(cuts)} cut points on 2 synthetic markets ({n} events in the last full run)")
    return ok, msgs
