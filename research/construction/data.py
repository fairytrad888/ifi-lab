"""Sealed price snapshot for the book construction test (research/construction/snapshot/).

Symbols never used by any IFI test (prereg_construction_v1.yaml, sealed_universe). Downloaded ONCE, by the first
run that reaches it (after the design-data check passed), then committed and reused; never refreshed by this test.
Same source and format as research/exits/data.py (Yahoo, split-adjusted, gzip CSV + sha256 manifest).
"""
from __future__ import annotations

import gzip
import hashlib
import io
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from research.common import _last_completed
from research.exits.data import SOURCE, _yahoo

SNAP = Path(__file__).resolve().parent / "snapshot"


def make_snapshot(symbols: list[str], downloader=None, source: str | None = None) -> dict:
    if downloader is not None and (not source or source == SOURCE):
        raise ValueError("a custom downloader needs its own source label (never the Yahoo label)")
    if (SNAP / "manifest.json").exists():
        raise SystemExit("the sealed snapshot already exists: it is never refreshed")
    got = (downloader or _yahoo)(symbols)
    cutoff = _last_completed(pd.Timestamp.now(tz="UTC"))
    SNAP.mkdir(parents=True, exist_ok=True)
    files = {}
    for s in symbols:
        if s not in got:
            print("sealed snapshot: no data for", s)
            continue
        df = got[s].copy()
        df.index = pd.to_datetime(df.index)
        if df.index.tz is not None:
            df.index = df.index.tz_localize(None)
        df.index = df.index.normalize()
        df.index.name = "date"
        cols = ["open", "high", "low", "close", "volume"] + (["adjclose"] if "adjclose" in df.columns else [])
        df = df[df.index <= cutoff][cols]
        if df.empty:
            continue
        buf = io.StringIO()
        df.to_csv(buf, float_format="%.6f")
        raw = buf.getvalue().encode()
        name = s.replace("^", "").replace("-", "_") + ".csv.gz"
        (SNAP / name).write_bytes(gzip.compress(raw, mtime=0))
        files[s] = dict(file=name, rows=len(df), first=str(df.index[0].date()), last=str(df.index[-1].date()),
                        sha256=hashlib.sha256(raw).hexdigest())
    man = dict(created_utc=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), cutoff=str(cutoff.date()),
               source=source or SOURCE, files=files)
    (SNAP / "manifest.json").write_text(json.dumps(man, indent=1, sort_keys=True))
    return man


def manifest() -> dict | None:
    f = SNAP / "manifest.json"
    return json.loads(f.read_text()) if f.exists() else None


def manifest_hash() -> str:
    f = SNAP / "manifest.json"
    return hashlib.sha256(f.read_bytes()).hexdigest() if f.exists() else "none"


def load(sym: str) -> pd.DataFrame | None:
    man = manifest()
    if man is None or sym not in man["files"]:
        return None
    info = man["files"][sym]
    raw = gzip.decompress((SNAP / info["file"]).read_bytes())
    if hashlib.sha256(raw).hexdigest() != info["sha256"]:
        raise SystemExit(f"sealed snapshot file for {sym} does not match its manifest checksum")
    from ifi.data import sanitize
    df = pd.read_csv(io.BytesIO(raw), index_col=0, parse_dates=True)
    return sanitize(df[["open", "high", "low", "close", "volume"]])
