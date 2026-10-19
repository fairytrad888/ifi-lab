"""Daily bars from Yahoo (yfinance), split-adjusted like TradingView; weekly bars ending Friday.

A week counts only once it is complete: its Friday has passed (run on Saturday or later). A mid-week run uses the
last completed week, never a partial bar.
"""
from __future__ import annotations

import time
from datetime import datetime, timezone

import numpy as np
import pandas as pd


def sanitize(df: pd.DataFrame) -> pd.DataFrame:
    px = df[["open", "high", "low", "close"]]
    ok = (px > 0).all(axis=1) & (df["high"] >= df["low"])
    df = df[ok].copy()
    df["high"] = df[["open", "high", "close"]].max(axis=1)
    df["low"] = df[["open", "low", "close"]].min(axis=1)
    c = df["close"]
    up, dn = np.log(c / c.shift(1)), np.log(c.shift(-1) / c)
    spike = (up.abs() > np.log(1.4)) & (dn.abs() > np.log(1.4)) & (np.sign(up) != np.sign(dn))
    return df[~spike.fillna(False)]


def daily(tickers: list[str], period: str = "10y", chunk: int = 100) -> tuple[dict[str, pd.DataFrame], list[str]]:
    import yfinance as yf

    got: dict[str, pd.DataFrame] = {}
    for k in range(0, len(tickers), chunk):
        part = tickers[k:k + chunk]
        raw = None
        for attempt in range(3):
            try:
                raw = yf.download(part, period=period, interval="1d", group_by="ticker", auto_adjust=False,
                                  threads=True, progress=False)
                break
            except Exception:
                time.sleep(15 * (attempt + 1))
        if raw is None:
            continue
        for t in part:
            try:
                sub = raw[t] if isinstance(raw.columns, pd.MultiIndex) else raw
                sub = sub.rename(columns=str.lower)[["open", "high", "low", "close", "volume"]].dropna(
                    subset=["open", "high", "low", "close"])
            except KeyError:
                continue
            sub.index = pd.to_datetime(sub.index).tz_localize(None)
            sub = sanitize(sub[~sub.index.duplicated(keep="last")].sort_index())
            if len(sub) > 60:
                got[t] = sub
        time.sleep(2)
    return got, sorted(set(tickers) - set(got))


def weekly(d: pd.DataFrame, now: datetime | None = None) -> pd.DataFrame:
    w = d.resample("W-FRI")
    o = pd.DataFrame({"open": w["open"].first(), "high": w["high"].max(), "low": w["low"].min(),
                      "close": w["close"].last(), "volume": w["volume"].sum()}).dropna(subset=["close"])
    now = now or datetime.now(timezone.utc)
    today = pd.Timestamp(now.date())
    return o[o.index < today]            # the week ending Friday counts from Saturday on


def dollar_volume(d: pd.DataFrame, n: int = 20) -> float:
    t = d.tail(n)
    return float((t["close"] * t["volume"]).mean()) if len(t) else 0.0
