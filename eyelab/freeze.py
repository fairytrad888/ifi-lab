"""Freeze of the prior system (IFI Lab v1.x and its research tests).

FREEZE.sha256 lists every tracked file outside the Eye Lab, except the folders the prior system rewrites on its own
schedule (logs, state, docs, data, reports). `verify` proves the Eye Lab has not changed any of them.
Created once at deploy, before the Eye Lab files are placed.
"""
from __future__ import annotations

import hashlib
import subprocess
import sys

from .guard import REPO, ROOT

EXCLUDE_PREFIXES = ("eyelab/", ".github/workflows/eyelab.yml", "logs/", "state/", "docs/", "data/", "reports/")
FREEZE = ROOT / "FREEZE.sha256"


def tracked() -> list[str]:
    r = subprocess.run(["git", "ls-files"], cwd=REPO, capture_output=True, text=True, check=True)
    return sorted(f for f in r.stdout.splitlines() if not f.startswith(EXCLUDE_PREFIXES))


def _sha(rel: str) -> str:
    return hashlib.sha256((REPO / rel).read_bytes()).hexdigest()


def make() -> int:
    files = tracked()
    FREEZE.write_text("".join(f"{_sha(f)}  {f}\n" for f in files))
    return len(files)


def verify() -> dict:
    if not FREEZE.exists():
        return {"ok": False, "error": "FREEZE.sha256 missing"}
    changed, missing, n = [], [], 0
    for line in FREEZE.read_text().splitlines():
        sha, rel = line.split("  ", 1)
        n += 1
        p = REPO / rel
        if not p.exists():
            missing.append(rel)
        elif _sha(rel) != sha:
            changed.append(rel)
    return {"ok": not changed and not missing, "files": n, "changed": changed, "missing": missing}


if __name__ == "__main__":
    if sys.argv[1:] == ["make"]:
        print(f"freeze written: {make()} files")
    else:
        v = verify()
        print(f"freeze: {'OK' if v['ok'] else 'CHANGED'} · {v.get('files', 0)} files · changed {v.get('changed')} · missing {v.get('missing')}")
        sys.exit(0 if v["ok"] else 1)
