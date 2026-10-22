"""Symbol sets: S1 / S2 / S3 / E by a fixed hash deal within each GICS sector.

X  = excluded: stocks already used by IFI tests, and every share class of a company that has a used class.
XD = a second share class of the same company (same name once class labels are removed): only the alphabetically
     first class is dealt, so one company can never sit in two sets.
"""
from __future__ import annotations

import hashlib
import re

import pandas as pd


def excluded(cfg: dict) -> set[str]:
    e = cfg["excluded"]
    return set(e["lab_stocks"]) | set(e["sealed_set1_stocks"])


def company_key(name: str) -> str:
    s = str(name).lower()
    s = re.sub(r"\(.*?\)", " ", s)
    s = re.sub(r"\bclass\s+[a-z]\b", " ", s)
    s = re.sub(r"\bseries\s+[a-z]\b", " ", s)
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def assign(universe: pd.DataFrame, cfg: dict, prereg: dict) -> pd.DataFrame:
    """universe: columns symbol, sector (and name). Returns a copy with `set` in {S1, S2, S3, E, X, XD}."""
    ss = prereg["symbol_sets"]
    salt, cycle = ss["salt"], ss["cycle"]
    u = universe.drop_duplicates("symbol").copy()
    u["sector"] = u["sector"].fillna("")
    u["deal_key"] = [hashlib.sha256((salt + s).encode()).hexdigest() for s in u["symbol"]]
    ex = excluded(cfg)
    u["set"] = ""
    if "name" in u.columns:
        u["company"] = [company_key(n) if str(n).strip() and str(n) != "nan" else s
                        for n, s in zip(u["name"], u["symbol"])]
    else:
        u["company"] = u["symbol"]
    for _, g in u.groupby("company"):
        if g["symbol"].isin(ex).any():
            u.loc[g.index, "set"] = "X"
        elif len(g) > 1:
            first = sorted(g["symbol"])[0]
            u.loc[g.index[g["symbol"] != first], "set"] = "XD"
    keep = u["set"] == ""
    for _, g in u[keep].sort_values(["sector", "deal_key"]).groupby("sector", sort=True):
        for pos, idx in enumerate(g.index):
            u.at[idx, "set"] = cycle[pos % len(cycle)]
    return u
