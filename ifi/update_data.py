"""Download/refresh market data.

  python -m ifi.update_data            # daily for ETFs + stocks, 4H for the watchlist, earnings for stocks
  python -m ifi.update_data --no-earnings
"""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from .data import ROOT, fetch_daily, fetch_4h, earnings_dates


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-earnings", action="store_true")
    a = ap.parse_args()
    c = yaml.safe_load((ROOT / "config.yaml").read_text())
    stocks = [s for v in c["stocks"].values() for s in v]
    daily = sorted(set(c["etfs"] + stocks + c["watchlist"] + [c["benchmark"]]))
    c14f = ROOT / "config_v14.yaml"          # v1.5: the extended (paper-only) universe is downloaded too
    if c14f.exists():
        ext = (yaml.safe_load(c14f.read_text()) or {}).get("extended_universe") or {}
        daily = sorted(set(daily) | set(ext.get("etfs", [])) | set(ext.get("stocks", [])))
    got = fetch_daily(daily)
    print(f"daily: {len(got)}/{len(daily)} symbols")
    from .freshness import ensure  # v1.4: make sure the newest completed session is present
    rep = ensure(daily)
    print(f"freshness: expected session {rep['expected']} · SPY ends {rep['spy_last']} · "
          f"repaired {len(rep['repaired'])} · still stale {len(rep['still_stale'])}" + (f" · {rep['error']}" if rep['error'] else ""))
    h4 = sorted(set(c["watchlist"] + [c["benchmark"]]))
    got4 = fetch_4h(h4)
    print(f"4H: {len(got4)}/{len(h4)} symbols")
    if not a.no_earnings:
        edir = ROOT / "data" / "earnings"
        edir.mkdir(parents=True, exist_ok=True)
        n = 0
        for s in sorted(set(stocks + [w for w in c["watchlist"] if w not in c["etfs"]])):
            e = earnings_dates(s)
            if e is not None:
                f = edir / f"{s}.csv"
                if f.exists():  # keep older rows Yahoo no longer returns
                    import pandas as pd
                    old = pd.read_csv(f, index_col=0, parse_dates=True)
                    e = pd.concat([old[~old.index.isin(e.index)], e]).sort_index()
                e.to_csv(f)
                n += 1
        print(f"earnings: {n} symbols")


if __name__ == "__main__":
    main()
