"""Eye Lab command line.

  python -m eyelab.run selftest
  python -m eyelab.run build-data --pools bench,dev,A,B --tf D [--tf H4]
  python -m eyelab.run fidelity  --rule R001
  python -m eyelab.run discovery --rule R001 [--force]
  python -m eyelab.run lock      --rule R001
  python -m eyelab.run confirm   --rule R001
  python -m eyelab.run freeze-verify
Outputs go to EYELAB_OUT (default eyelab/_out). Nothing is written anywhere else.
"""
from __future__ import annotations

import argparse
import json
import sys

from .guard import in_guard_window, out_dir


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="eyelab")
    ap.add_argument("stage", choices=["selftest", "build-data", "fidelity", "discovery", "lock", "confirm", "freeze-verify"])
    ap.add_argument("--rule")
    ap.add_argument("--pools", default="bench,dev,A,B")
    ap.add_argument("--tf", action="append")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--ignore-window", action="store_true", help="local runs only; the workflow never passes it")
    a = ap.parse_args(argv)

    w = in_guard_window()
    if w and not a.ignore_window and a.stage not in ("selftest", "freeze-verify"):
        print(f"ABORT: inside a prior-system window ({w}); run again later")
        return 2
    print(f"eyelab: stage {a.stage} · out {out_dir()}")
    if a.stage == "selftest":
        from .selftest import run_all
        res = run_all()
    elif a.stage == "freeze-verify":
        from .freeze import verify
        res = verify()
    elif a.stage == "build-data":
        from .data import build
        res = {f"{p}/{tf}": build(p, tf) for p in a.pools.split(",") for tf in (a.tf or ["D"])}
    else:
        if not a.rule:
            ap.error("--rule is required")
        if a.stage == "fidelity":
            from .data import add_symbols, home
            from .fidelity import examples, run
            from .registry import load_rule
            tf = load_rule(a.rule).SPEC["timeframe"]
            ex = examples(a.rule)
            off = sorted({s for s in ex["symbol"] if home(s) == "ex"}) if len(ex) else []
            if off:
                print("examples store:", add_symbols("ex", "D" if tf == "W" else tf, off))
            res = run(a.rule)
        elif a.stage == "discovery":
            from .discovery import run
            res = run(a.rule, force=a.force)
        elif a.stage == "lock":
            from .confirm import lock
            res = lock(a.rule)
        else:
            from .confirm import run
            res = run(a.rule)
    print(json.dumps(res, indent=1, default=str)[:4000])
    return 0


if __name__ == "__main__":
    sys.exit(main())
