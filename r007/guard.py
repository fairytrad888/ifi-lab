"""Isolation and honesty guards for R007.

- Output: everything R007 writes goes under OUT (env R007_OUT, default r007/_out, git-ignored). OUT may never point
  inside the repository anywhere else, so a run cannot touch the prior system, the Eye Lab or the weekly scan.
- Time windows: no run while the prior system or the weekly scan downloads or commits (config guard_windows_utc).
- Outcomes: no outcome may be computed on real data until a later phase is deployed and opened
  (outcomes_open() is False in Phase 0; only synthetic data may be scored).
- Lock: prereg_r007.yaml and the method code are pinned by PREREG.lock.
"""
from __future__ import annotations

import hashlib
import os
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent          # .../r007
REPO = ROOT.parent
CFG = yaml.safe_load((ROOT / "config.yaml").read_text())
PREREG = yaml.safe_load((ROOT / "prereg_r007.yaml").read_text())
LOCK = ROOT / "PREREG.lock"
LOCKED_FILES = ["r007/prereg_r007.yaml", "r007/config.yaml", "r007/guard.py", "r007/data.py", "r007/sets.py",
                "r007/events.py", "r007/outcomes.py", "r007/metric.py", "r007/power.py", "r007/lookahead.py",
                "r007/parity.py", "r007/phase0.py", "r007/model.py", "r007/phase1.py",
                # the live weekly-scan code and settings R007 reuses (signal, arm logic, groups, score, filters)
                "weekscan/scan.py", "weekscan/config.yaml", "weekscan/marketdata.py", "weekscan/universe.py",
                "weekscan/core/indicators.py", "weekscan/core/pine.py", "weekscan/core/states.py"]
PRIOR_PACKAGES = ("ifi", "research", "eyelab")   # R007 imports weekscan (read-only) and nothing else of the repo
OPEN_PHASES: tuple[str, ...] = ("1",)            # Phase 1 deploy: only R007_PHASE=1 may compute outcomes (S1+S2)


def out_dir() -> Path:
    p = Path(os.environ.get("R007_OUT", ROOT / "_out")).resolve()
    inside_repo = REPO in p.parents or p == REPO
    allowed = p == (ROOT / "_out").resolve() or (ROOT / "_out").resolve() in p.parents
    if inside_repo and not allowed:
        raise RuntimeError(f"R007_OUT={p} is inside the repository outside r007/_out: refused (isolation)")
    p.mkdir(parents=True, exist_ok=True)
    return p


def out(*parts: str) -> Path:
    f = out_dir().joinpath(*parts)
    f.parent.mkdir(parents=True, exist_ok=True)
    return f


def in_guard_window(now: datetime | None = None) -> str | None:
    now = now or datetime.now(timezone.utc)
    hm = now.hour * 60 + now.minute
    for w in CFG["guard_windows_utc"]:
        s = int(w["start"][:2]) * 60 + int(w["start"][3:])
        e = int(w["end"][:2]) * 60 + int(w["end"][3:])
        if now.weekday() in w["days"] and s <= hm < e:
            return f"{w['start']}-{w['end']} UTC on weekday {now.weekday()}"
    return None


def overlaps_guard(now: datetime | None = None, minutes: int = 150) -> str | None:
    """A run started now and lasting up to `minutes` would touch a guard window (checked every 5 minutes)."""
    from datetime import timedelta
    now = now or datetime.now(timezone.utc)
    for m in range(0, minutes + 1, 5):
        w = in_guard_window(now + timedelta(minutes=m))
        if w:
            return f"{w} (within {m} minutes of the start)"
    return None


def outcomes_open() -> bool:
    """True only when a deployed later phase is running (env R007_PHASE in OPEN_PHASES)."""
    return os.environ.get("R007_PHASE", "") in OPEN_PHASES


def _sha(rel: str) -> str:
    return hashlib.sha256((REPO / rel).read_bytes()).hexdigest()


def make_lock() -> str:
    LOCK.write_text("".join(f"{_sha(f)}  {f}\n" for f in LOCKED_FILES))
    return lock_id()


def lock_id() -> str:
    return hashlib.sha256(LOCK.read_bytes()).hexdigest()


def verify_lock() -> dict:
    if not LOCK.exists():
        return {"ok": False, "error": "PREREG.lock missing"}
    bad = []
    listed = []
    for line in LOCK.read_text().splitlines():
        sha, rel = line.split("  ", 1)
        listed.append(rel)
        if not (REPO / rel).exists() or _sha(rel) != sha:
            bad.append(rel)
    missing = sorted(set(LOCKED_FILES) - set(listed))
    return {"ok": not bad and not missing, "changed": bad, "unlisted": missing, "id": lock_id()}
