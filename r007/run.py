"""R007 command line.

  python -m r007.run verify        lock check only
  python -m r007.run snapshot      live reference, symbol sets and the one-time price snapshot (committed on its own)
  python -m r007.run phase0        Phase 0 (reuses the snapshot; needs origin/weekscan-results fetched)
  python -m r007.run phase1-mark   one-time marker for Phase 1 (pushed on its own before any outcome)
  R007_PHASE=1 python -m r007.run phase1   Phase 1 gate on S1+S2 (runs once; outcomes for S1+S2 only)

Phases 3 and E are not available in this deploy: each needs its own deploy and an explicit go.
"""
from __future__ import annotations

import argparse
import json
import sys

from . import guard


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="r007")
    ap.add_argument("stage", choices=["verify", "snapshot", "phase0", "phase1-mark", "phase1"])
    ap.add_argument("--live-ref", default="origin/weekscan-results")
    a = ap.parse_args(argv)
    if a.stage == "verify":
        v = guard.verify_lock()
        print(json.dumps(v))
        return 0 if v["ok"] else 1
    w = guard.overlaps_guard(minutes=120)
    if w:
        print(f"refused: a run started now could reach guard window {w}")
        return 1
    if a.stage == "phase1-mark":
        from . import phase1
        phase1.mark()
        return 0
    if a.stage == "phase1":
        from . import phase1
        res = phase1.run(a.live_ref)
        print(json.dumps({"passed": res["passed"], "gate": res["gate"]}, default=str))
        return 0
    if guard.outcomes_open():
        print("refused: snapshot and phase0 run with outcomes closed (unset R007_PHASE)")
        return 1
    from . import phase0
    if a.stage == "snapshot":
        lk, u, ref, daily, man = phase0.prepare(a.live_ref)
        print(json.dumps({"snapshot": man["id"][:16], "tickers": len(daily), "missing": man["missing"],
                          "reused": man.get("reused"), "sets": u["set"].value_counts().to_dict()}))
        return 0
    res = phase0.run(a.live_ref)
    print(json.dumps({"phase0_pass": res["phase0_pass"], "status": res["status"], "events": res["events"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
