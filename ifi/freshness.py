"""Daily data freshness (v1.4): make sure the newest completed US session is in data/daily before the scan.

Yahoo's full-history daily download sometimes lacks the latest session for hours after the close
(Oct 13-14, 2026: two Nightly runs in a row processed signals one day late). This module:
  1. finds the newest COMPLETED session from SPY's hourly bars (intraday data shows a session as soon as it
     trades, and holidays simply have no bars, so no exchange calendar is needed);
  2. re-downloads the last month of daily bars for every symbol whose file ends before that session and
     appends the missing rows;
  3. writes state/data_freshness.json, which the scan turns into an alert and a dashboard banner if the
     session is still missing. Nothing is invented: a missing bar stays missing until Yahoo has it.

  python -m ifi.freshness        # check and repair (also called by ifi.update_data)
"""
from __future__ import annotations

import json

import pandas as pd

from .data import DAILY_DIR, ROOT

STATE = ROOT / "state" / "data_freshness.json"
SETTLE = pd.Timedelta(minutes=15)


def session_close_utc(d: pd.Timestamp) -> pd.Timestamp:
    return (pd.Timestamp(d).normalize() + pd.Timedelta(hours=16)).tz_localize("America/New_York").tz_convert("UTC") + SETTLE


def expected_session(now: pd.Timestamp, hourly: pd.DataFrame | None) -> pd.Timestamp | None:
    """Newest session date (tz-naive) present in SPY's hourly bars whose daily close has passed."""
    if hourly is None or hourly.empty:
        return None
    idx = pd.DatetimeIndex(hourly.index)
    idx = idx.tz_localize("America/New_York") if idx.tz is None else idx.tz_convert("America/New_York")
    days = sorted(set(idx.normalize().tz_localize(None)))
    for d in reversed(days):
        if session_close_utc(d) <= now:
            return pd.Timestamp(d)
    return None


def last_date(sym: str) -> pd.Timestamp | None:
    f = DAILY_DIR / f"{sym}.csv"
    if not f.exists():
        return None
    try:
        return pd.Timestamp(pd.read_csv(f, usecols=[0]).iloc[-1, 0]).normalize()
    except Exception:
        return None


def _merge(sym: str, new: pd.DataFrame, upto: pd.Timestamp) -> bool:
    """Append rows newer than the file's last date (up to the expected session). Returns True if added."""
    f = DAILY_DIR / f"{sym}.csv"
    if not f.exists() or new is None or new.empty:
        return False
    old = pd.read_csv(f, index_col=0, parse_dates=True)
    new = new.copy()
    new.index = pd.to_datetime(new.index)
    if new.index.tz is not None:
        new.index = new.index.tz_localize(None)
    new.index = new.index.normalize()
    add = new[(new.index > old.index[-1]) & (new.index <= upto)][["open", "high", "low", "close", "volume"]]
    if add.empty:
        return False
    out = pd.concat([old, add])
    out.index.name = "date"
    out.to_csv(f)
    return True


def ensure(symbols: list[str], now: pd.Timestamp | None = None, hourly=None, recent=None) -> dict:
    """Check every daily file against the newest completed session and repair what can be repaired.
    `hourly` / `recent` are injectable for tests: hourly() -> SPY 1h frame; recent(list) -> {sym: daily frame}."""
    from .data import _yf_download

    now = now or pd.Timestamp.now(tz="UTC")
    try:
        h = hourly() if hourly else _yf_download(["SPY"], period="5d", interval="1h", prepost=False).get("SPY")
    except Exception as ex:  # no network / Yahoo hiccup: report, never block the scan
        h, err = None, str(ex)
    else:
        err = ""
    exp = expected_session(now, h)
    rep = dict(checked_utc=now.strftime("%Y-%m-%d %H:%M"), expected=str(exp.date()) if exp is not None else None,
               error=err, stale_before=[], repaired=[], still_stale=[], check_failed=exp is None)
    if exp is not None:
        stale = [s for s in symbols if (ld := last_date(s)) is not None and ld < exp]
        rep["stale_before"] = stale
        if stale:
            try:
                got = recent(stale) if recent else {}
                if not recent:
                    for k in range(0, len(stale), 25):
                        got.update(_yf_download(stale[k:k + 25], period="1mo", interval="1d"))
            except Exception as ex:
                got, rep["error"] = {}, str(ex)
            for s in stale:
                if _merge(s, got.get(s), exp):
                    rep["repaired"].append(s)
            rep["still_stale"] = [s for s in stale if (ld := last_date(s)) is None or ld < exp]
    spy = last_date("SPY")
    rep["spy_last"] = str(spy.date()) if spy is not None else None
    rep["stale"] = bool(exp is not None and (spy is None or spy < exp or rep["still_stale"]))
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(rep, indent=1))
    return rep


def read_state() -> dict:
    return json.loads(STATE.read_text()) if STATE.exists() else {}


def banner_line(rep: dict) -> str | None:
    """Alert / banner text when symbols still lack the newest completed session, or the check could not run."""
    if rep and rep.get("check_failed"):
        return ("⚠ Data freshness check could not run (SPY hourly bars unavailable"
                + (f": {rep.get('error')}" if rep.get("error") else "") + "). Daily data may be a session behind.")
    if not rep or not rep.get("stale"):
        return None
    miss = rep.get("still_stale", [])
    who = ", ".join(miss[:8]) + (f" +{len(miss) - 8} more" if len(miss) > 8 else "")
    return (f"⚠ Data stale: the {rep.get('expected')} session has closed but {len(miss)} symbol(s) still lack it after a "
            f"repair attempt ({who}; SPY ends {rep.get('spy_last')}). Their signals for that day will be processed on the next run.")


if __name__ == "__main__":
    import yaml
    c = yaml.safe_load((ROOT / "config.yaml").read_text())
    stocks = [s for v in c["stocks"].values() for s in v]
    syms = sorted(set(c["etfs"] + stocks + c["watchlist"] + [c["benchmark"]]))
    print(json.dumps(ensure(syms), indent=1))
