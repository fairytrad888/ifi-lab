"""Market data: Yahoo Finance via yfinance (free). Cached as CSV under data/.

Daily  : full history, split-adjusted OHLC (matches TradingView's default, which is not dividend-adjusted).
4H     : built from 1h bars (Yahoo keeps ~730 days) in TradingView's US session slots:
         slot A 09:30-13:30, slot B 13:30-16:00 (regular trading hours only).
"""
from __future__ import annotations

import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DAILY_DIR = ROOT / "data" / "daily"
H4_DIR = ROOT / "data" / "h4"


def _clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns=str.lower)[["open", "high", "low", "close", "volume"]]
    df = df.dropna(subset=["open", "high", "low", "close"])
    df = df[~df.index.duplicated(keep="last")].sort_index()
    return df


def _yf_download(tickers: list[str], **kw) -> dict[str, pd.DataFrame]:
    import yfinance as yf

    out: dict[str, pd.DataFrame] = {}
    for attempt in range(3):
        try:
            raw = yf.download(tickers, group_by="ticker", auto_adjust=False, threads=True, progress=False, **kw)
            break
        except Exception as e:  # network hiccup / rate limit
            if attempt == 2:
                raise
            time.sleep(10 * (attempt + 1))
    for t in tickers:
        try:
            sub = raw[t] if isinstance(raw.columns, pd.MultiIndex) else raw
            sub = _clean(sub)
            if len(sub):
                out[t] = sub
        except KeyError:
            continue
    return out


def fetch_daily(tickers: list[str]) -> dict[str, pd.DataFrame]:
    DAILY_DIR.mkdir(parents=True, exist_ok=True)
    got = _yf_download(tickers, period="max", interval="1d")
    for t, df in got.items():
        df.index = pd.to_datetime(df.index).tz_localize(None)
        df.index.name = "date"
        df.to_csv(DAILY_DIR / f"{t}.csv")
    return got


def to_4h(h1: pd.DataFrame) -> pd.DataFrame:
    """Aggregate 1h RTH bars into TradingView-style 4H session slots."""
    idx = pd.to_datetime(h1.index)
    if idx.tz is None:
        idx = idx.tz_localize("America/New_York")
    else:
        idx = idx.tz_convert("America/New_York")
    h1 = h1.copy()
    h1.index = idx
    mins = idx.hour * 60 + idx.minute
    h1 = h1[(mins >= 9 * 60 + 30) & (mins < 16 * 60)]
    mins = h1.index.hour * 60 + h1.index.minute
    is_b = (mins >= 13 * 60 + 30)
    offset = pd.to_timedelta(np.where(is_b, 13 * 60 + 30, 9 * 60 + 30), unit="m")
    key = h1.index.normalize() + offset
    g = h1.groupby(key)
    out = pd.DataFrame({
        "open": g["open"].first(), "high": g["high"].max(), "low": g["low"].min(),
        "close": g["close"].last(), "volume": g["volume"].sum(),
    })
    out.index = out.index.tz_localize(None)
    out.index.name = "datetime"
    out["slot"] = (out.index.hour * 60 + out.index.minute >= 13 * 60 + 30).astype(int)
    return out


def fetch_4h(tickers: list[str]) -> dict[str, pd.DataFrame]:
    H4_DIR.mkdir(parents=True, exist_ok=True)
    got = _yf_download(tickers, period="730d", interval="1h", prepost=False)
    out = {}
    for t, h1 in got.items():
        new = to_4h(h1)
        f = H4_DIR / f"{t}.csv"
        if f.exists():  # keep history beyond Yahoo's 730-day window
            old = pd.read_csv(f, index_col=0, parse_dates=True)
            new = pd.concat([old[old.index < new.index[0]], new])
        new.to_csv(f)
        out[t] = new
    return out


def load(ticker: str, tf: str = "daily") -> pd.DataFrame | None:
    f = (DAILY_DIR if tf == "daily" else H4_DIR) / f"{ticker}.csv"
    if not f.exists():
        return None
    df = pd.read_csv(f, index_col=0, parse_dates=True)
    return df


def earnings_dates(ticker: str, limit: int = 60) -> pd.DataFrame | None:
    """Past and upcoming earnings with EPS estimate/actual/surprise (Yahoo; coverage varies)."""
    try:
        import yfinance as yf

        e = yf.Ticker(ticker).get_earnings_dates(limit=limit)
        if e is None or e.empty:
            return None
        e = e.copy()
        e.index = pd.to_datetime(e.index).tz_localize(None).normalize()
        e.columns = [c.lower().replace(" ", "_").replace("(%)", "pct") for c in e.columns]
        return e.sort_index()
    except Exception:
        return None
