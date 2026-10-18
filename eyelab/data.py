"""Eye Lab data: its own pinned snapshots, separate from the prior system's data/ folder.

Layout under OUT/data/<pool>/<tf>/<SYM>.csv.gz plus OUT/data/<pool>/manifest.json (sha256 per file).
The benchmark (SPY) is stored once under the pool "bench".

Access rules (enforced by load):
  dev  -> purpose "fidelity" only (charts you look at; never graded)
  A    -> purpose "discovery" (and "example": bars up to an example date, for fidelity checks)
  B    -> purpose "confirm" only, through confirm.py, which records the opening in the seal
  bench-> any purpose
A file whose sha256 differs from the manifest is refused (pinned snapshot).
"""
from __future__ import annotations

import gzip
import hashlib
import io
import json
import time
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from .guard import CFG, ROOT, out

ALLOWED = {
    "dev": {"fidelity", "example", "selftest"},
    "A": {"discovery", "example", "selftest"},
    "B": {"confirm", "example", "selftest"},
    "bench": {"fidelity", "example", "discovery", "confirm", "selftest"},
    "ex": {"fidelity", "example", "selftest"},       # symbols from your examples that sit in no pool
}


def pool_symbols(pool: str) -> list[str]:
    f = ROOT / CFG["pools"][pool]["file"]
    return [s.strip() for s in f.read_text().splitlines() if s.strip() and not s.startswith("#")]


def pool_of(sym: str) -> str | None:
    for p in ("dev", "A", "B"):
        if sym in pool_symbols(p):
            return p
    return None


def home(sym: str) -> str:
    """Where an example symbol's data lives: its pool, or the examples store 'ex'."""
    return pool_of(sym) or "ex"


# ----------------------------------------------------------------------------- cleaning (as the prior system)
def sanitize(df: pd.DataFrame) -> pd.DataFrame:
    px = df[["open", "high", "low", "close"]]
    ok = (px > 0).all(axis=1) & (df["high"] >= df["low"])
    df = df[ok].copy()
    df["high"] = df[["open", "high", "close"]].max(axis=1)
    df["low"] = df[["open", "low", "close"]].min(axis=1)
    c = df["close"]
    up = np.log(c / c.shift(1))
    dn = np.log(c.shift(-1) / c)
    spike = (up.abs() > np.log(1.4)) & (dn.abs() > np.log(1.4)) & (np.sign(up) != np.sign(dn))
    return df[~spike.fillna(False)]


def _clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns=str.lower)[["open", "high", "low", "close", "volume"]]
    df = df.dropna(subset=["open", "high", "low", "close"])
    df = df[~df.index.duplicated(keep="last")].sort_index()
    return sanitize(df)


def to_4h(h1: pd.DataFrame) -> pd.DataFrame:
    """1h RTH bars -> TradingView-style US 4H session slots (09:30-13:30, 13:30-16:00)."""
    idx = pd.to_datetime(h1.index)
    idx = idx.tz_localize("America/New_York") if idx.tz is None else idx.tz_convert("America/New_York")
    h1 = h1.copy()
    h1.index = idx
    mins = idx.hour * 60 + idx.minute
    h1 = h1[(mins >= 570) & (mins < 960)]
    mins = h1.index.hour * 60 + h1.index.minute
    offset = pd.to_timedelta(np.where(mins >= 810, 810, 570), unit="m")
    g = h1.groupby(h1.index.normalize() + offset)
    o = pd.DataFrame({"open": g["open"].first(), "high": g["high"].max(), "low": g["low"].min(),
                      "close": g["close"].last(), "volume": g["volume"].sum()})
    o.index = o.index.tz_localize(None)
    o["slot"] = (o.index.hour * 60 + o.index.minute >= 810).astype(int)
    return o


def weekly(d: pd.DataFrame) -> pd.DataFrame:
    w = d.resample("W-FRI")
    o = pd.DataFrame({"open": w["open"].first(), "high": w["high"].max(), "low": w["low"].min(),
                      "close": w["close"].last(), "volume": w["volume"].sum()}).dropna(subset=["close"])
    return o


# ----------------------------------------------------------------------------- download and snapshot
def _download(tickers: list[str], tf: str) -> dict[str, pd.DataFrame]:
    import yfinance as yf

    kw = dict(period="max", interval="1d") if tf == "D" else dict(period="730d", interval="1h", prepost=False)
    got: dict[str, pd.DataFrame] = {}
    for i in range(0, len(tickers), 50):
        chunk = tickers[i:i + 50]
        for attempt in range(3):
            try:
                raw = yf.download(chunk, group_by="ticker", auto_adjust=False, threads=True, progress=False, **kw)
                break
            except Exception:
                if attempt == 2:
                    raise
                time.sleep(15 * (attempt + 1))
        for t in chunk:
            try:
                sub = raw[t] if isinstance(raw.columns, pd.MultiIndex) else raw
                sub = _clean(sub)
            except KeyError:
                continue
            if tf == "H4":
                sub = to_4h(sub)
            else:
                sub.index = pd.to_datetime(sub.index).tz_localize(None)
                sub = sub[sub.index >= CFG["history_start"]]
            if len(sub):
                got[t] = sub
        time.sleep(2)
    return got


def _write(pool: str, tf: str, sym: str, df: pd.DataFrame) -> tuple[str, str]:
    rel = f"data/{pool}/{tf}/{sym}.csv.gz"
    f = out(*rel.split("/"))
    buf = io.StringIO()
    df.to_csv(buf, index_label="date")
    raw = gzip.compress(buf.getvalue().encode(), mtime=0)   # mtime 0: identical data -> identical bytes
    f.write_bytes(raw)
    return rel, hashlib.sha256(raw).hexdigest()


def write_snapshot(pool: str, tf: str, frames: dict[str, pd.DataFrame], missing: list[str], source: str) -> dict:
    mf = out("data", pool, "manifest.json")
    man = json.loads(mf.read_text()) if mf.exists() else {"pool": pool, "files": {}, "tfs": {}}
    for sym, df in sorted(frames.items()):
        rel, sha = _write(pool, tf, sym, df)
        man["files"][rel] = {"sha256": sha, "rows": int(len(df)), "first": str(df.index[0])[:16], "last": str(df.index[-1])[:16]}
    lasts = sorted(str(df.index[-1])[:10] for df in frames.values())
    man["tfs"][tf] = {"symbols": len(frames), "missing": missing, "source": source,
                      "cutoff": lasts[len(lasts) // 2] if lasts else None,      # median last date: the common cutoff
                      "created_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")}
    mf.write_text(json.dumps(man, indent=1, sort_keys=True))
    return man["tfs"][tf]


def add_symbols(pool: str, tf: str, syms: list[str]) -> dict:
    """Pool 'ex' only: pin symbols not yet in the snapshot (never re-pins an existing file)."""
    assert pool == "ex", "only the examples store grows"
    have = {k.split("/")[-1][:-7] for k in manifest(pool)["files"] if k.startswith(f"data/{pool}/{tf}/")}
    need = sorted(set(syms) - have)
    if not need:
        return {"added": []}
    got = _download(need, tf)
    write_snapshot(pool, tf, got, sorted(set(need) - set(got)), "yahoo/yfinance (examples)")
    return {"added": sorted(got), "missing": sorted(set(need) - set(got))}


def build(pool: str, tf: str = "D") -> dict:
    """Download one pool for one timeframe and pin it. Refuses to rebuild an existing snapshot (pinning)."""
    mf = out("data", pool, "manifest.json")
    if mf.exists() and tf in json.loads(mf.read_text()).get("tfs", {}):
        return {"skipped": f"{pool}/{tf} already pinned"}
    syms = ["SPY"] if pool == "bench" else pool_symbols(pool)
    got = _download(syms, tf)
    return write_snapshot(pool, tf, got, sorted(set(syms) - set(got)), "yahoo/yfinance")


# ----------------------------------------------------------------------------- loading
def manifest(pool: str) -> dict:
    mf = out("data", pool, "manifest.json")
    return json.loads(mf.read_text()) if mf.exists() else {"files": {}, "tfs": {}}


def cutoff(pool: str, tf: str) -> pd.Timestamp | None:
    c = manifest(pool).get("tfs", {}).get("D" if tf == "W" else tf, {}).get("cutoff")
    return pd.Timestamp(c) + pd.Timedelta(hours=23, minutes=59) if c else None


def load(pool: str, sym: str, tf: str, purpose: str, until: pd.Timestamp | None = None,
         extra_bars: int = 0) -> pd.DataFrame | None:
    """until/extra_bars: for purpose 'example' the frame stops extra_bars after `until` (no outcomes visible)."""
    if purpose not in ALLOWED[pool]:
        raise PermissionError(f"pool {pool} cannot be read for '{purpose}' (allowed: {sorted(ALLOWED[pool])})")
    if purpose == "example" and pool != "bench" and until is None:
        raise PermissionError("purpose 'example' needs `until`: an example frame never shows what came after")
    df = _load(pool, sym, tf, purpose)            # daily frame when tf == "W"
    if df is None:
        return None
    if until is not None:
        if tf == "W":                              # end of the week holding `until`, plus extra weeks
            end = pd.Timestamp(until).normalize()
            end = end + pd.Timedelta(days=(4 - end.weekday()) % 7 + 7 * int(extra_bars), hours=23)
            df = df[df.index <= end]
        else:
            k = int(df.index.searchsorted(pd.Timestamp(until), side="right")) + int(extra_bars)
            df = df.iloc[:k]
    return weekly(df) if tf == "W" else df


def _load(pool: str, sym: str, tf: str, purpose: str) -> pd.DataFrame | None:
    if pool == "B" and purpose == "confirm":
        from .confirm import assert_open
        assert_open()
    base_tf = "D" if tf == "W" else tf
    rel = f"data/{pool}/{base_tf}/{sym}.csv.gz"
    meta = manifest(pool)["files"].get(rel)
    f = out(*rel.split("/"))
    if meta is None or not f.exists():
        return None
    raw = f.read_bytes()
    if hashlib.sha256(raw).hexdigest() != meta["sha256"]:
        raise RuntimeError(f"{rel}: sha256 differs from the manifest (snapshot changed): refused")
    df = pd.read_csv(io.BytesIO(gzip.decompress(raw)), index_col=0, parse_dates=True)
    cut = cutoff(pool, tf)
    if cut is not None:
        df = df[df.index <= cut]
    return df
