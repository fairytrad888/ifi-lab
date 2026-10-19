"""S&P 1500 constituents with GICS sector and sub-industry (Wikipedia lists), mapped to sector / industry ETFs.

The list is fetched each run. If a fetch fails, the last saved list (results branch) is used and the report says so.
Tickers are converted to Yahoo form (BRK.B -> BRK-B).
"""
from __future__ import annotations

import io
import re

import pandas as pd

URLS = {
    "sp500": "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
    "sp400": "https://en.wikipedia.org/wiki/List_of_S%26P_400_companies",
    "sp600": "https://en.wikipedia.org/wiki/List_of_S%26P_600_companies",
}
UA = {"User-Agent": "Mozilla/5.0 (IFI weekly scan; contact via GitHub repo)"}


def _col(cols, *needles):
    for c in cols:
        lc = str(c).lower()
        if all(n in lc for n in needles):
            return c
    return None


def parse_constituents(html: str, index: str) -> pd.DataFrame:
    """The first table that has a ticker column and a GICS sector column."""
    for t in pd.read_html(io.StringIO(html)):
        cols = [" ".join(map(str, c)) if isinstance(c, tuple) else str(c) for c in t.columns]
        t.columns = cols
        sym = _col(cols, "symbol") or _col(cols, "ticker")
        sec = _col(cols, "gics", "sector")
        sub = _col(cols, "sub-industry") or _col(cols, "sub industry")
        name = _col(cols, "security") or _col(cols, "company")
        if sym and sec:
            out = pd.DataFrame({
                "symbol": t[sym].astype(str).str.strip().map(yahoo_ticker),
                "name": t[name].astype(str) if name else "",
                "sector": t[sec].astype(str).str.strip(),
                "sub_industry": t[sub].astype(str).str.strip() if sub else "",
                "index": index,
            })
            return out[out["symbol"].str.match(r"^[A-Z][A-Z0-9\-]*$")]
    raise ValueError(f"{index}: no constituent table with a symbol and a GICS sector column")


def yahoo_ticker(s: str) -> str:
    return re.sub(r"[.\s]+", "-", s.strip().upper())


def fetch(sources: list[str]) -> tuple[pd.DataFrame, list[str]]:
    """All sources that load; per-source failures are returned as notes (the run continues with the rest)."""
    import requests

    frames, notes = [], []
    for src in sources:
        try:
            r = requests.get(URLS[src], headers=UA, timeout=60)
            r.raise_for_status()
            frames.append(parse_constituents(r.text, src))
        except Exception as e:
            notes.append(f"{src}: constituent list not loaded ({type(e).__name__}: {str(e)[:80]})")
    if not frames:
        raise RuntimeError("no constituent list could be loaded: " + "; ".join(notes))
    u = pd.concat(frames, ignore_index=True).drop_duplicates("symbol", keep="first")
    return u.reset_index(drop=True), notes


def map_etfs(u: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    u = u.copy()
    u["sector_etf"] = u["sector"].map(cfg["sector_etfs"])
    ind = cfg["industry_etfs"]
    u["industry_etf"] = u["sub_industry"].map(ind)
    u["group_etf"] = u["industry_etf"].fillna(u["sector_etf"])
    return u
