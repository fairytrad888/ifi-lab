"""Data-use ledger: every run that looks at anything is one row. Discovery variants are counted from it."""
from __future__ import annotations

import csv
from datetime import datetime, timezone

from .guard import out

COLS = ["utc", "stage", "rule_id", "version", "rule_sha", "pool", "tf", "n_signals", "looked_at", "result", "note"]


def append(**kw) -> None:
    f = out("LEDGER.csv")
    new = not f.exists()
    with f.open("a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        if new:
            w.writeheader()
        row = {k: kw.get(k, "") for k in COLS}
        row["utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
        row["rule_sha"] = str(row["rule_sha"])[:16]
        w.writerow(row)


def rows() -> list[dict]:
    f = out("LEDGER.csv")
    if not f.exists():
        return []
    with f.open() as fh:
        return list(csv.DictReader(fh))


def variants_tried(rule_id: str) -> int:
    """Distinct rule versions (file hashes) of this rule that have seen discovery outcomes."""
    return len({r["rule_sha"] for r in rows() if r["rule_id"] == rule_id and r["stage"] == "discovery"})
