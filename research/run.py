"""Research runner: the only entry point the workflow uses.

  python -m research.run --step all            # Step 0, then Step 1 (gated by Step 0)
  python -m research.run --step step0
  python -m research.run --step step1          # needs reports/research/STEP0_gate.json
  add --refresh-data to download a new frozen snapshot (otherwise the committed snapshot is reused)

Order of operations (every check aborts the run before the real result it protects is produced):
  1. pre-registration lock: prereg_v21.yaml, fixtures and every research module must match PREREG.lock
  2. look-ahead check: events recomputed on truncated data must equal the full-history events
  3. frozen data snapshot (research/snapshot, sha256 manifest; Yahoo source only)
  4. Step 0: synthetic null (random walks must show no information), then real data -> STEP0.md, STEP0_gate.json
  5. Step 1 gate: Step 0 must come from the same snapshot and lock; STOP means Step 1 does not run
  6. Step 1 synthetic null (0 PASS on random walks) and power check (planted trends: T1 and T3 must pass)
  7. Step 1 on real data, only the tests Step 0 allows -> STEP1.md + CSVs + audit sheets
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

import yaml

from research import step0, step1
from research.checks import check_no_lookahead
from research.common import (OUT, RESEARCH, load_prereg, load_snapshot, make_snapshot, manifest_hash,
                             snapshot_manifest, universe)
from research.synthetic import null_loader, planted_loader


def _commit() -> str:
    sha = os.environ.get("GITHUB_SHA")
    if sha:
        return sha
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return "local"


def _versions() -> str:
    import matplotlib
    import numpy
    import pandas
    import scipy
    return (f"Python {sys.version.split()[0]}, pandas {pandas.__version__}, numpy {numpy.__version__}, "
            f"scipy {scipy.__version__}, matplotlib {matplotlib.__version__}")


def allowed_tests(cfg: dict, gate: dict) -> tuple[list[str], dict]:
    ok, blocked = [], {}
    for tid in step1.TEST_IDS:
        need = cfg["gate"]["requires"][tid]
        if any(gate["passed"].get(p, False) for p in need):
            ok.append(tid)
        else:
            blocked[tid] = "Step 0: none of " + ", ".join(need) + " passed"
    return ok, blocked


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--step", choices=["all", "step0", "step1"], default="all")
    ap.add_argument("--refresh-data", action="store_true")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)

    # 1. lock
    cfg, prereg_sha = load_prereg(check_lock=True)
    step0.BLOCK_MONTHS = cfg["stats"]["block_months"]
    print(f"[1/7] pre-registration lock ok (fingerprint {prereg_sha})")
    validity = [("Pre-registration lock", f"ok (`{prereg_sha[:16]}`)", "prereg, fixtures and all research code match PREREG.lock")]

    # 2. look-ahead
    base = dict(step1.E.DEFAULTS, **cfg["thresholds"])
    ok, msgs = check_no_lookahead(base)
    print("[2/7] look-ahead check:", "ok" if ok else "FAILED", "|", "; ".join(msgs))
    if not ok:
        print("ABORT: an event depends on data after its own date.")
        return 1
    validity.append(("Look-ahead (truncation) check", "ok: " + msgs[-1], "identical events"))

    # 3. frozen data snapshot
    gs, go, bench = universe(cfg)
    symbols = [bench] + gs + go + list(cfg["universe"]["macro"])
    if a.refresh_data or snapshot_manifest() is None:
        man = make_snapshot(symbols)
        print(f"[3/7] new data snapshot, cutoff {man['cutoff']}, {len(man['files'])} symbols")
    man = snapshot_manifest()
    if not str(man.get("source", "")).startswith("Yahoo"):
        print(f"ABORT: the committed snapshot is not market data (source: {man.get('source')}). "
              "Delete research/snapshot and run again with refresh_data.")
        return 1
    missing = [s for s in symbols if s not in man["files"]]
    print(f"[3/7] snapshot cutoff {man['cutoff']} · manifest {manifest_hash()[:16]} · missing: {missing or 'none'}")
    if bench in missing or cfg["universe"]["macro"][0] in missing:
        print("ABORT: benchmark or macro series missing from the snapshot.")
        return 1

    # 4. Step 0: synthetic null first, then real data
    if a.step in ("all", "step0"):
        r0, ic0 = step0.run(step0._synthetic_loader(), "Step 0 pipeline check on random walks (should show NO information)",
                            "STEP0_synthetic.md")
        g0 = step0.gate(r0, ic0)
        print("[4/7] Step 0 null:", "ok" if g0["stop"] else "FAILED", g0["passed"])
        if not g0["stop"]:
            print("ABORT: Step 0 found information in random walks.")
            return 1
        step0.run(load_snapshot, "Step 0: does the Daily ratio state carry information?", "STEP0.md", "STEP0_gate.json")
        g = json.loads((OUT / "STEP0_gate.json").read_text())
        g.update(manifest=manifest_hash(), lock=prereg_sha, cutoff=man["cutoff"], null_ok=True)
        (OUT / "STEP0_gate.json").write_text(json.dumps(g, indent=1))
        print("[4/7] Step 0 written:", g["passed"])
    if a.step == "step0":
        for f in list(OUT.glob("STEP1*")) + list((OUT / "audit").glob("*.png")):
            f.unlink()  # a Step 1 result from an earlier snapshot must not sit next to a new Step 0
        return 0

    # 5. Step 1 gate
    gate_file = OUT / "STEP0_gate.json"
    if not gate_file.exists():
        print("ABORT: Step 0 has not been run (reports/research/STEP0_gate.json missing).")
        return 1
    gate = json.loads(gate_file.read_text())
    if gate.get("manifest") != manifest_hash() or gate.get("lock") != prereg_sha:
        print("ABORT: the Step 0 result was made on a different data snapshot or lock. Run with step = all.")
        return 1
    for f in list(OUT.glob("STEP1*")) + list((OUT / "audit").glob("*.png")):
        f.unlink()  # no stale Step 1 files can survive next to a new result
    if not gate.get("null_ok"):
        print("ABORT: the Step 0 result has no passing synthetic null on record. Run with step = all.")
        return 1
    validity.append(("Step 0 synthetic null (random walks)", "ok: no P-test passed (stamped in STEP0_gate.json)", "no PASS"))
    if gate["stop"]:
        (OUT / "STEP1.md").write_text("# Step 1: not run\n\nStep 0 found no information in Daily ratio states "
                                      "(every P-test failed), so by the pre-registered gate no ratio rule is tested.\n")
        print("[5/7] Step 0 gate = STOP; Step 1 not run")
        return 0
    allowed, blocked = allowed_tests(cfg, gate)
    print("[5/7] Step 1 tests allowed by Step 0:", allowed, "| blocked:", blocked or "none")
    validity.append(("Step 0 gate", "passed: " + (", ".join(k for k, v in gate["passed"].items() if v) or "none"),
                     "a Step 1 test runs only if its Step 0 prerequisite passed"))

    # 6. Step 1 synthetic null and power check (all 7 comparisons, gate ignored on synthetic data)
    null = step1.run_step1(null_loader(3), cfg, step1.TEST_IDS, tag="null")
    npass = step1.count_passes(null)
    verdicts = {t: r["verdict"] for t, r in null["results"].items()}
    print("[6/7] Step 1 null:", "ok" if npass == 0 else "FAILED", verdicts)
    if npass:
        print("ABORT: Step 1 reported a PASS on random walks.")
        return 1
    validity.append(("Synthetic null (random walks, all 7 comparisons)", "ok: 0 PASS · " +
                     ", ".join(f"{k} {v}" for k, v in verdicts.items()), "0 PASS"))
    pw = step1.run_step1(planted_loader(5), cfg, step1.TEST_IDS, tag="power")
    pv = {t: r["verdict"] for t, r in pw["results"].items()}
    detected = all(pv[t] in step1.PASS_LABELS for t in ("T1", "T3"))
    print("[6/7] power check (planted trends):", "ok" if detected else "FAILED", pv)
    if not detected:
        print("ABORT: the pipeline did not detect planted trend persistence (T1 and T3 must pass).")
        return 1
    validity.append(("Power check (planted trend persistence)", "ok: " + ", ".join(f"{k} {v}" for k, v in pv.items()),
                     "T1 and T3 must detect; T2, T5, T6 have no planted effect"))

    # 7. Step 1 on real data
    meta = dict(run_utc=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"), commit=_commit(), prereg=prereg_sha,
                cutoff=man["cutoff"], manifest=manifest_hash(), gate=gate, versions=_versions())
    fixtures = yaml.safe_load((RESEARCH / "fixtures_scan.yaml").read_text())
    out = step1.run_step1(load_snapshot, cfg, allowed, tag="real", sheets=True, fixtures=fixtures)
    v = cfg["validity"]
    aud_ok = out["audit_share"] >= v["definition_audit_min"]
    par_ok = out["parity_share"] >= v["parity_min"]
    validity.append(("Definition audit (eye-logged scan events found)", f"{100 * out['audit_share']:.0f}%",
                     f">= {100 * v['definition_audit_min']:.0f}%"))
    validity.append(("TradingView parity (screenshot values)", f"{100 * out['parity_share']:.0f}%",
                     f">= {100 * v['parity_min']:.0f}% within {100 * v['parity_tol']:.1f}%"))
    meta["validity"] = validity
    meta["status"] = "VALID" if (aud_ok and par_ok) else (
        "PROVISIONAL: " + "; ".join(x for x, bad in (("definition audit below threshold", not aud_ok),
                                                     ("parity below threshold", not par_ok)) if bad)
        + ". Results are written but must not be acted on until the misses are reviewed.")
    (OUT / "STEP1.md").write_text(step1.write_report(out, cfg, meta, allowed, blocked))
    step1.save_tables(out)
    (OUT / "STEP1_meta.json").write_text(json.dumps(dict(
        {k: v_ for k, v_ in meta.items() if k != "validity"},
        validity=[list(r) for r in validity],
        verdicts={t: r["verdict"] for t, r in out["results"].items()}, blocked=blocked), indent=1, default=str))
    print("[7/7] Step 1 written:", {t: r["verdict"] for t, r in out["results"].items()}, "| status:", meta["status"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
