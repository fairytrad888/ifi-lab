"""Frozen price snapshot for the E4 exit test (research/exits/snapshot/), separate from the ratio snapshot.

Same rules as research/common.py: Yahoo via yfinance (auto_adjust=False: split-adjusted, not dividend-adjusted,
like TradingView), trimmed to the last completed session, gzip CSV per symbol plus a sha256 manifest. Yahoo's
Adj Close is kept as `adjclose` so dividends received during a trade can be credited (signals never use it).
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

SNAP = Path(__file__).resolve().parent / "snapshot"
SOURCE = "Yahoo Finance via yfinance, auto_adjust=False (split-adjusted, not dividend-adjusted)"


def _yahoo(syms: list[str]) -> dict[str, pd.DataFrame]:
    """Daily OHLCV (split-adjusted, as TradingView) plus Yahoo's Adj Close, which carries the dividend
    adjustment used to credit dividends received during a trade (total-return R)."""
    import time

    import yfinance as yf

    out: dict[str, pd.DataFrame] = {}
    for k in range(0, len(syms), 20):           # batches keep Yahoo requests small
        batch = syms[k:k + 20]
        for attempt in range(3):
            try:
                raw = yf.download(batch, group_by="ticker", auto_adjust=False, threads=True, progress=False,
                                  period="max", interval="1d")
                break
            except Exception:
                if attempt == 2:
                    raise
                time.sleep(10 * (attempt + 1))
        for t in batch:
            try:
                sub = raw[t] if isinstance(raw.columns, pd.MultiIndex) else raw
            except KeyError:
                continue
            sub = sub.rename(columns=str.lower).rename(columns={"adj close": "adjclose"})
            if not {"open", "high", "low", "close", "volume"} <= set(sub.columns):
                continue
            cols = ["open", "high", "low", "close", "volume"] + (["adjclose"] if "adjclose" in sub.columns else [])
            sub = sub[cols].dropna(subset=["open", "high", "low", "close"])
            sub = sub[~sub.index.duplicated(keep="last")].sort_index()
            if len(sub):
                out[t] = sub
    return out


def make_snapshot(symbols: list[str], downloader=None, source: str | None = None) -> dict:
    if downloader is not None and (not source or source == SOURCE):
        raise ValueError("a custom downloader needs its own source label (never the Yahoo label)")
    if downloader is None:
        downloader = _yahoo
    got = downloader(symbols)
    cutoff = _last_completed(pd.Timestamp.now(tz="UTC"))
    SNAP.mkdir(parents=True, exist_ok=True)
    for f in SNAP.glob("*.csv.gz"):
        f.unlink()
    files = {}
    for s in symbols:
        if s not in got:
            print("snapshot: no data for", s)
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
            print("snapshot: no completed bars for", s)
            continue
        buf = io.StringIO()
        df.to_csv(buf, float_format="%.6f")
        raw = buf.getvalue().encode()
        name = s.replace("^", "") + ".csv.gz"
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
        raise SystemExit(f"exit-test snapshot file for {sym} does not match its manifest checksum")
    from ifi.data import sanitize
    return sanitize(pd.read_csv(io.BytesIO(raw), index_col=0, parse_dates=True))  # keeps adjclose if present
