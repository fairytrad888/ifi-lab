"""Isolation and honesty guards for the Eye Lab.

- Output: everything the Eye Lab writes goes under OUT (env EYELAB_OUT, default eyelab/_out, git-ignored).
  OUT may never point inside the repository anywhere else, so a run cannot touch the prior system's files.
- Time windows: no run while the prior system downloads or commits (config guard_windows_utc).
- Blind mode: during fidelity work no outcome can be computed (outcomes.py refuses).
- Imports: no Eye Lab module may import the prior packages (ifi, research); checked by the tests.
"""
from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent          # .../eyelab
REPO = ROOT.parent
CFG = yaml.safe_load((ROOT / "config.yaml").read_text())
PRIOR_PACKAGES = ("ifi", "research")


def out_dir() -> Path:
    p = Path(os.environ.get("EYELAB_OUT", ROOT / "_out")).resolve()
    inside_repo = REPO in p.parents or p == REPO
    allowed = p == (ROOT / "_out").resolve() or (ROOT / "_out").resolve() in p.parents
    if inside_repo and not allowed:
        raise RuntimeError(f"EYELAB_OUT={p} is inside the repository outside eyelab/_out: refused (isolation)")
    p.mkdir(parents=True, exist_ok=True)
    return p


def out(*parts: str) -> Path:
    f = out_dir().joinpath(*parts)
    f.parent.mkdir(parents=True, exist_ok=True)
    return f


def outdir(*parts: str) -> Path:
    d = out_dir().joinpath(*parts)
    d.mkdir(parents=True, exist_ok=True)
    return d


def in_guard_window(now: datetime | None = None) -> str | None:
    now = now or datetime.now(timezone.utc)
    hm = now.hour * 60 + now.minute
    for w in CFG["guard_windows_utc"]:
        s = int(w["start"][:2]) * 60 + int(w["start"][3:])
        e = int(w["end"][:2]) * 60 + int(w["end"][3:])
        if now.weekday() in w["days"] and s <= hm < e:
            return f"{w['start']}-{w['end']} UTC on weekday {now.weekday()}"
    return None


_BLIND = {"on": False}


def enter_blind() -> None:
    _BLIND["on"] = True


def leave_blind() -> None:
    _BLIND["on"] = False


def is_blind() -> bool:
    return _BLIND["on"]


def prior_imports(root: Path = ROOT) -> list[str]:
    """Lines in Eye Lab code that import the prior system's packages (must be empty)."""
    pat = re.compile(r"^\s*(from|import)\s+(%s)(\.|\s|$)" % "|".join(PRIOR_PACKAGES))
    bad = []
    for f in root.rglob("*.py"):
        for n, line in enumerate(f.read_text().splitlines(), 1):
            if pat.match(line):
                bad.append(f"{f.relative_to(root)}:{n}: {line.strip()}")
    return bad
