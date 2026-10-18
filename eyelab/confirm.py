"""Stages 4 and 6: lock a rule version, then confirm it once on sealed pool B.

lock    : fingerprints the rule file, the Eye Lab code + config + pool lists, and pool B's manifest, and writes
          the pre-registered pass rule (config `primary`). Needs a discovery run of this exact rule version.
confirm : refuses unless the lock still matches. Records the opening in pool B's seal BEFORE reading any pool B
          data, so a crashed run still counts. One opening per rule version, ever.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone

from . import engine, ledger
from .guard import CFG, ROOT, out, outdir
from .registry import load_rule, rule_sha

_STATE = {"open": False}


def assert_open() -> None:
    if not _STATE["open"]:
        raise PermissionError("pool B is sealed: only confirm.run() may read it, once per locked rule version")


def code_sha() -> str:
    h = hashlib.sha256()
    files = sorted(p for p in ROOT.rglob("*") if p.is_file() and p.suffix in (".py", ".yaml", ".txt")
                   and "rules" not in p.relative_to(ROOT).parts and "tests" not in p.relative_to(ROOT).parts
                   and "examples" not in p.relative_to(ROOT).parts and "_out" not in p.relative_to(ROOT).parts
                   and "__pycache__" not in p.parts)
    for p in files:
        h.update(str(p.relative_to(ROOT)).encode())
        h.update(p.read_bytes())
    return h.hexdigest()


def b_manifest_sha() -> str:
    f = out("data", "B", "manifest.json")
    return hashlib.sha256(f.read_bytes()).hexdigest() if f.exists() else ""


def lock_path(rule_id: str, version) -> object:
    return out("locks", f"{rule_id}_v{version}.json")


def lock(rule_id: str) -> dict:
    mod = load_rule(rule_id)
    if mod.SPEC["status"] == "demo":
        raise PermissionError("demo rules cannot be locked")
    sha = rule_sha(rule_id)
    if not out("discovery", rule_id, sha[:16], "DISCOVERY.json").exists():
        raise PermissionError("lock needs a discovery run of this exact rule version")
    if not b_manifest_sha():
        raise PermissionError("pool B snapshot not built yet")
    f = lock_path(rule_id, mod.SPEC["version"])
    if f.exists():
        raise PermissionError(f"{f.name} exists: a locked version is never re-locked; bump the rule version")
    hyps = None
    if hasattr(mod, "STUDY"):
        from .study import carried
        hyps = carried(rule_id)
        if not hyps:
            raise PermissionError("nothing passed discovery: there is no hypothesis to confirm (bump the version to try again)")
    body = {"rule_id": rule_id, "version": mod.SPEC["version"], "rule_sha": sha, "code_sha": code_sha(),
            "pool_B_manifest_sha": b_manifest_sha(), "primary": CFG["primary"] if hyps is None else mod.PRIMARY,
            "hypotheses": hyps,
            "locked_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")}
    body["lock_sha"] = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()
    f.write_text(json.dumps(body, indent=1))
    ledger.append(stage="lock", rule_id=rule_id, version=mod.SPEC["version"], rule_sha=sha, pool="B",
                  looked_at="nothing (fingerprints only)", result=body["lock_sha"][:16])
    return body


def run(rule_id: str) -> dict:
    from .discovery import measure, report

    mod = load_rule(rule_id)
    v = mod.SPEC["version"]
    f = lock_path(rule_id, v)
    if not f.exists():
        raise PermissionError(f"{rule_id} v{v} is not locked")
    lk = json.loads(f.read_text())
    now = {"rule_sha": rule_sha(rule_id), "code_sha": code_sha(), "pool_B_manifest_sha": b_manifest_sha()}
    bad = [k for k, val in now.items() if lk[k] != val]
    if bad:
        raise PermissionError(f"lock mismatch on {bad}: the rule, the Eye Lab code or pool B changed after locking")
    seal_f = out("data", "B", "SEAL.json")
    seal = json.loads(seal_f.read_text()) if seal_f.exists() else {"openings": []}
    if any(o["rule_id"] == rule_id and str(o["version"]) == str(v) for o in seal["openings"]):
        raise PermissionError(f"pool B was already opened for {rule_id} v{v}: a confirmation runs once")
    seal["openings"].append({"rule_id": rule_id, "version": v, "lock_sha": lk["lock_sha"],
                             "utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")})
    seal_f.write_text(json.dumps(seal, indent=1))            # recorded before any pool B read
    _STATE["open"] = True
    try:
        if hasattr(mod, "STUDY"):
            from .study import confirm as study_confirm
            meta = study_confirm(rule_id, lk)
        else:
            df, info = measure(rule_id, "B", "confirm")
    finally:
        _STATE["open"] = False
    if hasattr(mod, "STUDY"):
        ledger.append(stage="confirm", rule_id=rule_id, version=v, rule_sha=now["rule_sha"], pool="B", tf="D",
                      n_signals=meta["events"], looked_at="all outcomes on pool B ETF ratios (opened once)", result=meta["verdict"])
        return meta
    pv = engine.primary_verdict(df, info["tf"]) if len(df) > 1 else {"pass": False}
    verdict = "CONFIRMED" if pv.get("pass") else "NOT CONFIRMED"
    n_prior = len(seal["openings"]) - 1
    extra = [f"**Verdict: {verdict}** under the locked rule: {CFG['primary']['rule']}.", "",
             f"Lock `{lk['lock_sha'][:16]}` (locked {lk['locked_utc']} UTC). Pool B openings before this one: {n_prior} "
             f"(each earlier confirmation on the same pool slightly weakens this one).", ""]
    if pv.get("main"):
        m = pv["main"]
        other = "time" if pv["null"] == "cross" else "cross"
        extra += [f"Primary: {pv['metric']} advantage vs {pv['null']} null {m['mean'] * 100:+.1f} pts "
                  f"(95% {m['lo'] * 100:+.1f} to {m['hi'] * 100:+.1f}); vs the other null "
                  f"{pv[f'adv_{other}_mean'] * 100:+.1f} pts; halves {pv['half_before'] * 100:+.1f} / {pv['half_after'] * 100:+.1f} pts.", ""]
    md = report(rule_id, df, info, "confirmation", "B", extra)
    base = outdir("confirm", rule_id, f"v{v}")
    (base / "CONFIRM.md").write_text("\n".join(md) + "\n")
    df.to_csv(base / "signals.csv", index=False)
    meta = {"rule_id": rule_id, "version": v, "verdict": verdict, "signals": int(len(df)), "lock_sha": lk["lock_sha"],
            "primary": pv}
    (base / "CONFIRM.json").write_text(json.dumps(meta, indent=1, default=str))
    ledger.append(stage="confirm", rule_id=rule_id, version=v, rule_sha=now["rule_sha"], pool="B", tf=info["tf"],
                  n_signals=len(df), looked_at="all outcomes on pool B (opened once)", result=verdict)
    return meta
