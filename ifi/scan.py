"""Nightly scan: read every watchlist symbol on Daily and 4H, log new events, fill outcomes,
update the journal statistics, push alerts and rebuild the dashboard.

  python -m ifi.scan                 # normal nightly run
  python -m ifi.scan --backfill 250  # seed the log with events from the last N bars (run once)
"""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import yaml

from .data import ROOT, load
from .states import read, events_on_bar
from .backtest import setups as bt_setups
from . import allocation as alloc
from . import forward as fw
from . import freshness

LOG = ROOT / "logs" / "events.csv"
JOURNAL_STATS = ROOT / "logs" / "journal_stats.json"
STATE = ROOT / "state" / "last_scan.json"
HORIZONS = (5, 10)


# ---------------------------------------------------------------- completed bars only (v1.3.1)
# A run during the session sees bars that are still forming. Events and paper trades use completed
# bars only, and any event logged before its bar had closed is purged and re-detected on the final bar.
_SETTLE = pd.Timedelta(minutes=15)


def bar_close_utc(tf: str, ts) -> pd.Timestamp:
    """UTC time at which a bar is final. Daily index = date; 4H index = ET slot start (09:30 / 13:30)."""
    ts = pd.Timestamp(ts)
    if tf == "daily":
        end = ts.normalize() + pd.Timedelta(hours=16)
    else:
        end = ts.normalize() + pd.Timedelta(hours=13, minutes=30) if ts.hour * 60 + ts.minute < 13 * 60 + 30 \
            else ts.normalize() + pd.Timedelta(hours=16)
    return end.tz_localize("America/New_York").tz_convert("UTC") + _SETTLE


def completed(tf: str, x: pd.DataFrame | None, now: pd.Timestamp) -> pd.DataFrame | None:
    if x is None or x.empty:
        return x
    n = len(x)
    while n > 0 and bar_close_utc(tf, x.index[n - 1]) > now:
        n -= 1
    return x.iloc[:n]


def purge_provisional(log: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Drop rows logged before their bar closed. Returns the cleaned log and, per tf|symbol,
    the earliest purged bar (so the scan re-detects events from there)."""
    if log.empty or "logged" not in log:
        return log, {}
    bars = pd.to_datetime(log["bar"].astype(str), format="ISO8601")
    logged = pd.to_datetime(log["logged"].astype(str), format="ISO8601", errors="coerce").dt.tz_localize("UTC")
    closes = pd.Series([bar_close_utc(tf, b) for tf, b in zip(log["tf"], bars)], index=log.index)
    bad = logged.notna() & (logged < closes)
    rewind = {}
    for (tf, sym), b in zip(zip(log.loc[bad, "tf"], log.loc[bad, "symbol"]), bars[bad]):
        k = f"{tf}|{sym}"
        rewind[k] = min(rewind.get(k, b), b)
    return log.loc[~bad].reset_index(drop=True), rewind


def cfg():
    return yaml.safe_load((ROOT / "config.yaml").read_text())


def _row(sym, tf, x, i, ev, c):
    r = x.iloc[i]
    stop = r["stop_suggest"]
    risk_ps = r["close"] - stop if pd.notna(stop) else np.nan
    shares = int(c["risk"]["account"] * c["risk"]["risk_per_trade"] / risk_ps) if risk_ps and risk_ps > 0 else 0
    return dict(
        id=f"{tf}|{sym}|{x.index[i]:%Y-%m-%d %H:%M}|{ev}", tf=tf, symbol=sym, bar=x.index[i], event=ev,
        family=ev.split(" (")[0].split(" #")[0], stage=int(r["stage"]), score=int(r["score"]), close=round(r["close"], 4),
        atr=round(r["atr"], 4), trend_line=round(r["tr_line"], 4), anchor=round(r["tr_anchor"], 4) if pd.notna(r["tr_anchor"]) else np.nan,
        anchor_role="support" if r["tr_anchor_is_support"] else "resistance",
        dist_anchor_atr=round(r["dist_anchor_atr"], 2) if pd.notna(r["dist_anchor_atr"]) else np.nan,
        rsi=round(r["mx_rsi"], 1), wt1=round(r["sig_wt1"], 1), rvol=round(r["rvol"], 2) if pd.notna(r["rvol"]) else np.nan,
        rrg=r.get("rrg", ""), with_trend=bool(r["trend200_up"]), stop=round(stop, 4) if pd.notna(stop) else np.nan,
        shares_1pct=shares, logged=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
    )


PLAYBOOK_NAMES = {"E4_anchor_reclaim": "Playbook E4 anchor reclaim", "E1_trigger_with_trend": "Playbook E1 trigger with trend"}


def playbook_rows(sym, tf, x, i, c, sets):
    out = []
    pb = c.get("playbook", {})
    for su in pb.get("setups", []):
        if su in sets and bool(sets[su].iloc[i]):
            name = PLAYBOOK_NAMES.get(su, su)
            if tf != "daily":  # the playbook is validated on Daily bars only; 4H copies are logged to build evidence
                name = name.replace("Playbook", "4H watch")
            row = _row(sym, tf, x, i, name, c)
            low5 = x["low"].rolling(5).min().iloc[i]
            risk = row["close"] - row["stop"] if pd.notna(row["stop"]) else np.nan
            row["family"] = "Playbook" if tf == "daily" else "4H watch"
            row["setup"] = su
            row["target"] = round(row["close"] + pb.get("target_r", 3) * risk, 4) if risk and risk > 0 else np.nan
            row["cancel_if_open_below"] = round(low5, 4)
            out.append(row)
    return out


def fill_outcomes(log: pd.DataFrame, frames: dict, bench: dict) -> pd.DataFrame:
    for k in HORIZONS:
        for col in (f"ret{k}", f"rel{k}", f"r{k}"):
            if col not in log:
                log[col] = np.nan
    for col in ("mfe10_r", "mae10_r"):
        if col not in log:
            log[col] = np.nan
    for i, e in log.iterrows():
        if pd.notna(log.at[i, "r10"]):
            continue
        x = frames.get((e.tf, e.symbol))
        if x is None:
            continue
        bar = pd.Timestamp(e.bar)
        if bar not in x.index:
            continue
        j = x.index.get_loc(bar)
        risk = e.close - e.stop if pd.notna(e.stop) else np.nan
        b = bench.get(e.tf)
        for k in HORIZONS:
            if j + k < len(x) and pd.isna(log.at[i, f"ret{k}"]):
                c_k = x["close"].iloc[j + k]
                log.at[i, f"ret{k}"] = c_k / e.close - 1
                if b is not None and bar in b.index:
                    bj = b.index.get_loc(bar)
                    if bj + k < len(b):
                        log.at[i, f"rel{k}"] = log.at[i, f"ret{k}"] - (b["close"].iloc[bj + k] / b["close"].iloc[bj] - 1)
                if risk and risk > 0:
                    log.at[i, f"r{k}"] = (c_k - e.close) / risk
        if j + 10 < len(x) and risk and risk > 0:
            w = x.iloc[j + 1:j + 11]
            log.at[i, "mfe10_r"] = (w["high"].max() - e.close) / risk
            log.at[i, "mae10_r"] = (w["low"].min() - e.close) / risk
    return log


def journal_load(url: str) -> pd.DataFrame | None:
    if not url:
        return None
    t = pd.read_csv(url)
    t.columns = [c.strip().lower() for c in t.columns]
    t = t.dropna(subset=["entry", "stop", "exit"])
    side = t.get("side", pd.Series("long", index=t.index)).fillna("long").astype(str).str.lower()
    sign = np.where(side.str.startswith("s"), -1, 1)
    t["r"] = sign * (t["exit"] - t["entry"]) / (sign * (t["entry"] - t["stop"]))
    t["date"] = pd.to_datetime(t["date"], errors="coerce")
    t["symbol"] = t["symbol"].astype(str).str.upper().str.strip()
    return t


def journal_stats(t: pd.DataFrame | None) -> dict:
    if t is None or t.empty:
        return {}
    by = t.groupby(t.get("setup", pd.Series("all", index=t.index)).fillna("untagged"))["r"]
    return {"n": int(len(t)), "expectancy": float(t["r"].mean()),
            "win_rate": float((t["r"] > 0).mean()),
            "avg_win": float(t.loc[t.r > 0, "r"].mean()) if (t.r > 0).any() else None,
            "avg_loss": float(t.loc[t.r <= 0, "r"].mean()) if (t.r <= 0).any() else None,
            "by_setup": {k: {"n": int(v.count()), "expectancy": float(v.mean())} for k, v in by}}


def notify(c, new_rows: list[dict], extra: list[str] | None = None):
    topic = os.environ.get("NTFY_TOPIC", "").strip()
    if not topic or not (new_rows or extra):
        return
    import requests

    want = set(c["alerts"]["notify_events"])
    lines = []
    for r in new_rows:
        fam = r["family"]
        stage_up = fam.startswith("Stage") and int(r["event"].split("-> ")[-1]) >= c["alerts"]["min_stage_change_to"]
        if fam == "Playbook":
            lines.insert(0, f"★ {r['symbol']} {r['tf']}: {r['event']} | entry ~{r['close']} stop {r['stop']} "
                            f"target {r.get('target')} | {r['shares_1pct']} sh | cancel if open < {r.get('cancel_if_open_below')}")
            continue
        if fam in want or stage_up:
            lines.append(f"{r['symbol']} {r['tf']}: {r['event']} | stage {r['stage']} score {r['score']} | "
                         f"stop {r['stop']} size {r['shares_1pct']}")
    lines = list(extra or []) + lines
    if lines:
        try:
            requests.post(f"https://ntfy.sh/{topic}", data="\n".join(lines[:40]).encode(),
                          headers={"Title": f"IFI: {len(lines)} new events", "Priority": "default"}, timeout=20)
        except Exception as ex:
            print("ntfy failed:", ex)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backfill", type=int, default=0)
    a = ap.parse_args()
    c = cfg()
    bench_sym = c["benchmark"]
    frames, bench, latest = {}, {}, []
    now = pd.Timestamp.now(tz="UTC")
    for tf in ("daily", "h4"):
        b = load(bench_sym, tf)
        bench[tf] = b
        for s in c["watchlist"]:
            df = load(s, tf)
            if df is None or len(df) < 260:
                continue
            x = completed(tf, read(df, b), now)
            if x is not None and len(x) >= 260:
                frames[(tf, s)] = x
        bench[tf] = completed(tf, b, now)
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    log = pd.read_csv(LOG) if LOG.exists() else pd.DataFrame()
    log, rewind = purge_provisional(log)
    if rewind:
        print("re-detecting provisional events:", {k: str(v) for k, v in rewind.items()})
    seen = set(log["id"]) if not log.empty else set()
    new_rows = []
    for (tf, s), x in frames.items():
        key = f"{tf}|{s}"
        last_done = pd.Timestamp(state[key]) if key in state else None
        if key in rewind:
            first = pd.Timestamp(rewind[key])
            prior = x.index[x.index < first]
            last_done = prior[-1] if len(prior) else None
        if a.backfill:
            start = max(len(x) - a.backfill, 1)
        elif last_done is not None:
            start = int(np.searchsorted(x.index.values, np.datetime64(last_done), side="right"))
        else:
            start = len(x) - 1
        if not a.backfill:  # always re-check the last 3 completed bars (ids dedupe; catches bars first seen mid-session)
            start = min(start, len(x) - 3)
        sets = bt_setups(x)
        for i in range(max(start, 1), len(x)):
            for row in playbook_rows(s, tf, x, i, c, sets):
                if row["id"] not in seen:
                    new_rows.append(row)
                    seen.add(row["id"])
            for ev in events_on_bar(x, i):
                row = _row(s, tf, x, i, ev, c)
                if row["id"] not in seen:
                    new_rows.append(row)
                    seen.add(row["id"])
        state[key] = str(x.index[-1])
    if new_rows:
        log = pd.concat([log, pd.DataFrame(new_rows)], ignore_index=True)
    if not log.empty:
        log["bar"] = pd.to_datetime(log["bar"].astype(str), format="ISO8601")
        log = fill_outcomes(log, frames, bench)
        log = log.sort_values(["bar", "symbol"]).reset_index(drop=True)
        LOG.parent.mkdir(parents=True, exist_ok=True)
        log.to_csv(LOG, index=False)
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=1))
    # forward test (v1.4): full-universe paper trades with context tags, allocation ladder, health, drift
    c14 = alloc.cfg14()
    pframes = {k: v for k, v in frames.items() if k[0] == "daily"}
    if c14.get("forward_universe", "watchlist") == "full":
        braw = load(bench_sym, "daily")
        stocks = [s for v in c["stocks"].values() for s in v]
        for s in sorted(set(c["etfs"] + stocks)):
            if ("daily", s) in pframes:
                continue
            df = load(s, "daily")
            if df is None or len(df) < 260:
                continue
            x = completed("daily", read(df, braw), now)
            if x is not None and len(x) >= 260:
                pframes[("daily", s)] = x
    ctx = dict(spy=pframes.get(("daily", bench_sym)), h4={s: x for (tf, s), x in frames.items() if tf == "h4"})
    prev_alloc = json.loads(alloc.ALLOC.read_text()) if alloc.ALLOC.exists() else {}
    prev_health = json.loads(alloc.HEALTH.read_text()) if alloc.HEALTH.exists() else {}
    seeded = (ROOT / "state" / "v14_seeded").exists()
    pt = fw.paper_trades(log, pframes, c, ctx)
    full = alloc.ladder(pt, c, c14)
    board = {k: v for k, v in full.items() if not k.startswith("_")}
    pmeta = full["_portfolio"]
    hl = alloc.health(pt, c, c14)
    fresh = freshness.read_state()
    dr = fw.drift(c)
    try:
        jdf = journal_load(c["journal"].get("trades_csv_url", ""))
        js = journal_stats(jdf)
        if jdf is not None:
            # execution metrics keep their v1.3 meaning: watchlist signals (plus any symbol you actually traded)
            mine = set(c["watchlist"]) | set(jdf["symbol"])
            js["execution"] = fw.match_journal(jdf, pt[pt["symbol"].isin(mine)] if not pt.empty else pt)
    except Exception as ex:
        js = {"error": str(ex)}
    JOURNAL_STATS.write_text(json.dumps(js, indent=1, default=str))
    extra = fw.alert_lines(pt, board, dr)
    if not seeded:  # first v1.4 run: record the full-universe history silently instead of pushing it
        extra = [l_ for l_ in extra if not l_.startswith("Paper") or any(f" {w} " in l_ for w in c["watchlist"])]
        (ROOT / "state").mkdir(parents=True, exist_ok=True)
        (ROOT / "state" / "v14_seeded").write_text(datetime.now(timezone.utc).isoformat())
    old_pf = prev_alloc.get("portfolio", {})
    if old_pf and old_pf.get("breaker") != pmeta["breaker"]:
        extra.insert(0, f"⚠ Drawdown breaker: {old_pf.get('breaker')} -> {pmeta['breaker']} "
                        f"(live paper drawdown {100 * pmeta['live_drawdown']:.1f}%)")
    for su, b in board.items():
        was = prev_alloc.get("board", {}).get(su, {}).get("streak_flag")
        if b["streak_flag"] and not was:
            extra.insert(0, f"⚠ Losing streak {su}: {b['losing_streak']} in a row (p = {b['streak_p']:.3f} under the backtest "
                            "win rate). Review, no automatic action.")
    for su, h in hl.items():   # alert when a flag turns on, not every run while it stays on
        if h.get("ks_flag") and not prev_health.get(su, {}).get("ks_flag"):
            extra.append(f"Health {su}: live R distribution differs from the backtest (KS p = {h['ks_p']:.3f}). Check data and execution.")
    fl = freshness.banner_line(fresh)
    sig = json.dumps([fresh.get("expected"), sorted(fresh.get("still_stale", [])), bool(fresh.get("check_failed"))])
    fa = ROOT / "state" / "freshness_alerted.json"
    if fl and (not fa.exists() or fa.read_text() != sig):
        extra.insert(0, fl)
    fa.parent.mkdir(parents=True, exist_ok=True)
    fa.write_text(sig if fl else "")
    if not a.backfill:
        notify(c, new_rows, extra)
    from .dashboard import build
    build(frames, log, js, c, pt, board, dr, alloc_meta=pmeta, health=hl, fresh=fresh, c14=c14)
    print(f"{len(new_rows)} new events; log size {len(log)}")


if __name__ == "__main__":
    main()
