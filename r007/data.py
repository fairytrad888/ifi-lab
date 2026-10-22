"""R007 price snapshot: Yahoo daily bars downloaded once, committed with a sha256 manifest, never refreshed.

Layout under OUT: data/daily/<SYMBOL>.csv.gz, data/MANIFEST.json. A later run verifies the manifest and reuses it.
"""
from __future__ import annotations

import gzip
import hashlib
import io
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from weekscan.marketdata import sanitize

from . import guard


def _dir() -> Path:
    d = guard.out_dir() / "data" / "daily"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _manifest() -> Path:
    return guard.out_dir() / "data" / "MANIFEST.json"


def _csv_bytes(df: pd.DataFrame, fmt: str) -> bytes:
    buf = io.StringIO()
    df.to_csv(buf, index_label="date", float_format=fmt)
    return gzip.compress(buf.getvalue().encode(), mtime=0)


def split_factor(splits: pd.Series) -> pd.Series:
    """Product of the split ratios strictly after each date: unadjusted price = split-adjusted price x factor."""
    s = pd.to_numeric(splits, errors="coerce").fillna(0.0)
    s = s.where(s > 0, 1.0)
    return s[::-1].cumprod()[::-1].shift(-1).fillna(1.0)


def download(tickers: list[str], start: str, end: str, chunk: int) -> tuple[dict[str, pd.DataFrame], list[str]]:
    """Split-adjusted daily OHLCV (as weekscan) plus `split_factor` (later splits) for point-in-time price floors."""
    import yfinance as yf

    end_excl = (pd.Timestamp(end) + pd.Timedelta(days=1)).date().isoformat()
    got: dict[str, pd.DataFrame] = {}
    for k in range(0, len(tickers), chunk):
        part = tickers[k:k + chunk]
        raw = None
        for attempt in range(4):
            try:
                raw = yf.download(part, start=start, end=end_excl, interval="1d", group_by="ticker",
                                  auto_adjust=False, actions=True, threads=True, progress=False)
                break
            except Exception:
                time.sleep(20 * (attempt + 1))
        if raw is None:
            continue
        for t in part:
            try:
                sub = raw[t] if isinstance(raw.columns, pd.MultiIndex) else raw
                sub = sub.rename(columns=str.lower)
                splits = sub["stock splits"] if "stock splits" in sub.columns else pd.Series(0.0, index=sub.index)
                sub = sub[["open", "high", "low", "close", "volume"]].copy()
                sub["split_factor"] = split_factor(splits).to_numpy()
                sub = sub.dropna(subset=["open", "high", "low", "close"])
            except KeyError:
                continue
            sub.index = pd.to_datetime(sub.index).tz_localize(None)
            sub = sanitize(sub[~sub.index.duplicated(keep="last")].sort_index())
            if len(sub) > 60:
                got[t] = sub
        time.sleep(3)
    return got, sorted(set(tickers) - set(got))


def snapshot(tickers: list[str], log=print, fetch=download, required: list[str] | None = None,
             ) -> tuple[dict[str, pd.DataFrame], dict]:
    """Load the committed snapshot (verified) or, if none exists, download it once and write it.
    `required` tickers (SPY and every group ETF) must all be present, else nothing is written."""
    D = guard.CFG["data"]
    mf = _manifest()
    if mf.exists():
        man = json.loads(mf.read_text())
        bad = []
        out = {}
        for s, meta in man["files"].items():
            f = _dir() / f"{s}.csv.gz"
            b = f.read_bytes() if f.exists() else b""
            if hashlib.sha256(b).hexdigest() != meta["sha256"]:
                bad.append(s)
                continue
            out[s] = pd.read_csv(io.BytesIO(gzip.decompress(b)), index_col="date", parse_dates=["date"])
        if bad:
            raise RuntimeError(f"snapshot manifest mismatch for {len(bad)} files (e.g. {bad[:5]}): stop")
        log(f"snapshot reused: {len(out)} tickers, manifest {man['id'][:16]}")
        return out, {**man, "reused": True}
    got, missing = fetch(tickers, D["start"], D["end"], D["chunk"])
    req_missing = sorted(set(required or []) - set(got))
    if req_missing:
        raise RuntimeError(f"download incomplete: required tickers missing {req_missing}; snapshot not written, re-run later")
    share = len(missing) / max(1, len(tickers))
    if share > D["max_missing_share"]:
        raise RuntimeError(f"download incomplete: {len(missing)} of {len(tickers)} tickers missing "
                           f"({share:.1%} > {D['max_missing_share']:.0%}); snapshot not written, re-run later. "
                           f"Missing e.g. {missing[:10]}")
    files = {}
    for s, df in sorted(got.items()):
        b = _csv_bytes(df, D["float_format"])
        (_dir() / f"{s}.csv.gz").write_bytes(b)
        files[s] = {"sha256": hashlib.sha256(b).hexdigest(), "rows": len(df),
                    "first": df.index[0].date().isoformat(), "last": df.index[-1].date().isoformat()}
    body = json.dumps(files, sort_keys=True).encode()
    n_split = sum(int((df["split_factor"] != 1.0).any()) for df in got.values() if "split_factor" in df)
    man = {"id": hashlib.sha256(body).hexdigest(), "created_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
           "start": D["start"], "end": D["end"], "requested": len(tickers), "missing": missing,
           "tickers_with_splits": n_split, "files": files}
    mf.write_text(json.dumps(man, indent=1, sort_keys=True))
    out = {s: pd.read_csv(io.BytesIO(gzip.decompress((_dir() / f"{s}.csv.gz").read_bytes())), index_col="date",
                          parse_dates=["date"]) for s in files}
    log(f"snapshot written: {len(out)} tickers, {len(missing)} missing, manifest {man['id'][:16]}")
    return out, {**man, "reused": False}
