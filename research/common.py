"""Shared research infrastructure: pre-registration lock, frozen data snapshot, ratio bars,
peer-relative outcome panel and calendar-block bootstrap statistics.

Used by Step 0 (research/step0.py) and Step 1 (research/step1.py) so both gates read the same data.
"""
from __future__ import annotations

import gzip
import hashlib
import io
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research"
OUT = ROOT / "reports" / "research"
SNAP = RESEARCH / "snapshot"
PREREG = RESEARCH / "prereg_v21.yaml"
LOCK = RESEARCH / "PREREG.lock"
# everything that defines a result is locked, not only the YAML: a change to any of these files after
# results are seen trips the lock (python -m research.common --write-lock re-locks, visibly, in git)
LOCKED_FILES = ["research/prereg_v21.yaml", "research/fixtures_scan.yaml", "research/engine.py", "research/step1.py",
                "research/step0.py", "research/common.py", "research/checks.py", "research/synthetic.py",
                "research/run.py", "ifi/pine.py", "ifi/indicators.py", "ifi/states.py", "ifi/data.py"]


# ------------------------------------------------------------------ pre-registration lock
def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_lock() -> str:
    lines = [f"{sha256_file(ROOT / f)}  {f}" for f in LOCKED_FILES]
    LOCK.write_text("\n".join(lines) + "\n")
    return sha256_file(LOCK)


def load_prereg(check_lock: bool = True) -> tuple[dict, str]:
    """Returns the pre-registration and the lock fingerprint (sha256 of PREREG.lock)."""
    if check_lock:
        if not LOCK.exists():
            raise SystemExit("PREREG.lock missing: refusing to run")
        want = {}
        for line in LOCK.read_text().splitlines():
            if line.strip():
                h, f = line.split()[:2]
                want[f] = h
        if sorted(want) != sorted(LOCKED_FILES):
            raise SystemExit(f"PREREG.lock lists {sorted(want)}, expected {sorted(LOCKED_FILES)}")
        bad = [f for f in LOCKED_FILES if sha256_file(ROOT / f) != want[f]]
        if bad:
            raise SystemExit("Locked research files changed after locking: " + ", ".join(bad) +
                             ". Results would not be pre-registered. Restore them, or issue a new version with a new lock.")
    fp = sha256_file(LOCK) if LOCK.exists() else "unlocked"
    return yaml.safe_load(PREREG.read_text()), fp


def universe(cfg: dict) -> tuple[list[str], list[str], str]:
    u = cfg["universe"]
    return list(u["group_S"]), list(u["group_O"]), u["benchmark"]


# ------------------------------------------------------------------ frozen data snapshot
def _fname(sym: str) -> str:
    return sym.replace("^", "") + ".csv.gz"


def _last_completed(now_utc: pd.Timestamp) -> pd.Timestamp:
    """Last US session whose daily bar is complete (close 16:00 ET + 15 min settle)."""
    et = now_utc.tz_convert("America/New_York")
    d = et.normalize().tz_localize(None)
    if et.hour * 60 + et.minute < 16 * 60 + 15:
        d -= pd.Timedelta(days=1)
    return d


def make_snapshot(symbols: list[str], downloader=None, source: str | None = None) -> dict:
    """Download full daily history, trim to the last completed session, write gzip CSVs + manifest.
    A custom downloader (tests) must pass its own `source` label; research/run.py only accepts Yahoo snapshots."""
    if downloader is not None and not source:
        raise ValueError("a custom downloader needs a source label")
    if downloader is None:
        from ifi.data import _yf_download

        def downloader(syms):
            return _yf_download(syms, period="max", interval="1d")
    got = downloader(symbols)
    cutoff = _last_completed(pd.Timestamp.now(tz="UTC"))
    SNAP.mkdir(parents=True, exist_ok=True)
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
        df = df[df.index <= cutoff][["open", "high", "low", "close", "volume"]]
        if df.empty:
            print("snapshot: no completed bars for", s)
            continue
        buf = io.StringIO()
        df.to_csv(buf, float_format="%.6f")
        raw = buf.getvalue().encode()
        (SNAP / _fname(s)).write_bytes(gzip.compress(raw, mtime=0))
        files[s] = dict(file=_fname(s), rows=len(df), first=str(df.index[0].date()), last=str(df.index[-1].date()),
                        sha256=hashlib.sha256(raw).hexdigest())
    man = dict(created_utc=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), cutoff=str(cutoff.date()),
               source=source or "Yahoo Finance via yfinance, auto_adjust=False (split-adjusted, not dividend-adjusted)",
               files=files)
    (SNAP / "manifest.json").write_text(json.dumps(man, indent=1, sort_keys=True))
    return man


def snapshot_manifest() -> dict | None:
    f = SNAP / "manifest.json"
    return json.loads(f.read_text()) if f.exists() else None


def manifest_hash() -> str:
    f = SNAP / "manifest.json"
    return sha256_file(f) if f.exists() else "none"


def load_snapshot(sym: str) -> pd.DataFrame | None:
    man = snapshot_manifest()
    if man is None or sym not in man["files"]:
        return None
    info = man["files"][sym]
    raw = gzip.decompress((SNAP / info["file"]).read_bytes())
    if hashlib.sha256(raw).hexdigest() != info["sha256"]:
        raise SystemExit(f"snapshot file for {sym} does not match its manifest checksum")
    from ifi.data import sanitize
    df = pd.read_csv(io.BytesIO(raw), index_col=0, parse_dates=True)
    return sanitize(df)


# ------------------------------------------------------------------ ratio bars
def ratio_bars(a: pd.DataFrame, b: pd.DataFrame) -> pd.DataFrame:
    """TradingView-style ratio: O1/O2, H1/H2, L1/L2, C1/C2, highs/lows clamped to contain open and close.
    No volume, so anchors are time-weighted (as on TradingView)."""
    j = a.index.intersection(b.index)
    a, b = a.loc[j], b.loc[j]
    r = pd.DataFrame({k: a[k] / b[k] for k in ("open", "high", "low", "close")}, index=j)
    r["high"] = r[["open", "high", "low", "close"]].max(axis=1)
    r["low"] = r[["open", "high", "low", "close"]].min(axis=1)
    r["volume"] = 0.0
    return r.replace([np.inf, -np.inf], np.nan).dropna()


# ------------------------------------------------------------------ calendar-block bootstrap
def month_ids(dates, block_months: int = 1) -> np.ndarray:
    """Calendar block id per date: blocks of `block_months` consecutive calendar months."""
    d = pd.DatetimeIndex(dates)
    return ((d.year * 12 + d.month - 1) // block_months).to_numpy()


class Boot:
    """Calendar-block bootstrap (blocks of `block_months` months, resampled with replacement), fixed seed.
    Events and outcomes inside a block move together, so overlapping 20-60 bar outcomes are not treated
    as independent. A resample with no observations on a side is discarded (NaN), not scored as 0."""

    def __init__(self, reps: int, seed: int, k: int, alpha: float = 0.05, block_months: int = 3):
        self.reps, self.seed, self.k, self.alpha, self.bm = reps, seed, k, alpha, block_months

    def _q(self, bs: np.ndarray) -> dict:
        a_adj = self.alpha / self.k
        q = lambda x: float(np.nanquantile(bs, x))
        return dict(lo=q(self.alpha / 2), hi=q(1 - self.alpha / 2), lo_adj=q(a_adj / 2), hi_adj=q(1 - a_adj / 2))

    def diff(self, va, da, vb, db) -> dict:
        """mean(A) - mean(B); A and B resampled jointly by calendar month."""
        va, vb = np.asarray(va, float), np.asarray(vb, float)
        ma, mb = month_ids(da, self.bm), month_ids(db, self.bm)
        okA, okB = ~np.isnan(va), ~np.isnan(vb)
        va, ma, vb, mb = va[okA], ma[okA], vb[okB], mb[okB]
        if len(va) == 0 or len(vb) == 0:
            return dict(est=np.nan, n_a=len(va), n_b=len(vb), lo=np.nan, hi=np.nan, lo_adj=np.nan, hi_adj=np.nan)
        blocks = np.union1d(np.unique(ma), np.unique(mb))
        pos = {b: i for i, b in enumerate(blocks)}
        ia = np.array([pos[m] for m in ma])
        ib = np.array([pos[m] for m in mb])
        K = len(blocks)
        sa, na = np.bincount(ia, va, K), np.bincount(ia, None, K)
        sb, nb = np.bincount(ib, vb, K), np.bincount(ib, None, K)
        est = va.mean() - vb.mean()
        rng = np.random.default_rng(self.seed)
        draw = rng.integers(0, K, size=(self.reps, K))
        cA, cB = na[draw].sum(1), nb[draw].sum(1)
        with np.errstate(invalid="ignore", divide="ignore"):
            bs = np.where((cA > 0) & (cB > 0), sa[draw].sum(1) / cA - sb[draw].sum(1) / cB, np.nan)
        return dict(est=float(est), n_a=int(len(va)), n_b=int(len(vb)), **self._q(bs))

    def mean(self, v, d) -> dict:
        """mean(v) with a calendar-block CI (paired differences)."""
        v = np.asarray(v, float)
        m = month_ids(d, self.bm)
        ok = ~np.isnan(v)
        v, m = v[ok], m[ok]
        if len(v) == 0:
            return dict(est=np.nan, n_a=0, n_b=0, lo=np.nan, hi=np.nan, lo_adj=np.nan, hi_adj=np.nan)
        blocks, inv = np.unique(m, return_inverse=True)
        K = len(blocks)
        s, n = np.bincount(inv, v, K), np.bincount(inv, None, K)
        rng = np.random.default_rng(self.seed)
        draw = rng.integers(0, K, size=(self.reps, K))
        cnt = n[draw].sum(1)
        with np.errstate(invalid="ignore", divide="ignore"):
            bs = np.where(cnt > 0, s[draw].sum(1) / cnt, np.nan)
        return dict(est=float(v.mean()), n_a=int(len(v)), n_b=0, **self._q(bs))


if __name__ == "__main__":
    import sys
    if "--write-lock" in sys.argv:
        print("lock fingerprint", write_lock())
        print(LOCK.read_text())
