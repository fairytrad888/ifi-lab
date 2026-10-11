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

LOG = ROOT / "logs" / "events.csv"
JOURNAL_STATS = ROOT / "logs" / "journal_stats.json"
STATE = ROOT / "state" / "last_scan.json"
HORIZONS = (5, 10)


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


def journal_stats(url: str) -> dict:
    if not url:
        return {}
    try:
        t = pd.read_csv(url)
    except Exception as ex:
        return {"error": str(ex)}
    t.columns = [c.strip().lower() for c in t.columns]
    t = t.dropna(subset=["entry", "stop", "exit"])
    side = t.get("side", pd.Series("long", index=t.index)).fillna("long").str.lower()
    sign = np.where(side.str.startswith("s"), -1, 1)
    t["r"] = sign * (t["exit"] - t["entry"]) / (sign * (t["entry"] - t["stop"]))
    by = t.groupby(t.get("setup", pd.Series("all", index=t.index)).fillna("untagged"))["r"]
    out = {"n": int(len(t)), "expectancy": float(t["r"].mean()) if len(t) else None,
           "win_rate": float((t["r"] > 0).mean()) if len(t) else None,
           "avg_win": float(t.loc[t.r > 0, "r"].mean()) if (t.r > 0).any() else None,
           "avg_loss": float(t.loc[t.r <= 0, "r"].mean()) if (t.r <= 0).any() else None,
           "by_setup": {k: {"n": int(v.count()), "expectancy": float(v.mean())} for k, v in by}}
    return out


def notify(c, new_rows: list[dict]):
    topic = os.environ.get("NTFY_TOPIC", "").strip()
    if not topic or not new_rows:
        return
    import requests

    want = set(c["alerts"]["notify_events"])
    lines = []
    for r in new_rows:
        fam = r["family"]
        stage_up = fam.startswith("Stage") and int(r["event"].split("-> ")[-1]) >= c["alerts"]["min_stage_change_to"]
        if fam in want or stage_up:
            lines.append(f"{r['symbol']} {r['tf']}: {r['event']} | stage {r['stage']} score {r['score']} | "
                         f"stop {r['stop']} size {r['shares_1pct']}")
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
    for tf in ("daily", "h4"):
        b = load(bench_sym, tf)
        bench[tf] = b
        for s in c["watchlist"]:
            df = load(s, tf)
            if df is None or len(df) < 260:
                continue
            x = read(df, b)
            frames[(tf, s)] = x
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    log = pd.read_csv(LOG, parse_dates=["bar"]) if LOG.exists() else pd.DataFrame()
    seen = set(log["id"]) if not log.empty else set()
    new_rows = []
    for (tf, s), x in frames.items():
        key = f"{tf}|{s}"
        last_done = pd.Timestamp(state[key]) if key in state else None
        if a.backfill:
            start = max(len(x) - a.backfill, 1)
        elif last_done is not None:
            start = int(np.searchsorted(x.index.values, np.datetime64(last_done), side="right"))
        else:
            start = len(x) - 1
        for i in range(max(start, 1), len(x)):
            for ev in events_on_bar(x, i):
                row = _row(s, tf, x, i, ev, c)
                if row["id"] not in seen:
                    new_rows.append(row)
                    seen.add(row["id"])
        state[key] = str(x.index[-1])
    if new_rows:
        log = pd.concat([log, pd.DataFrame(new_rows)], ignore_index=True)
    if not log.empty:
        log["bar"] = pd.to_datetime(log["bar"])
        log = fill_outcomes(log, frames, bench)
        log = log.sort_values(["bar", "symbol"]).reset_index(drop=True)
        LOG.parent.mkdir(parents=True, exist_ok=True)
        log.to_csv(LOG, index=False)
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=1))
    js = journal_stats(c["journal"].get("trades_csv_url", ""))
    JOURNAL_STATS.write_text(json.dumps(js, indent=1))
    if not a.backfill:
        notify(c, new_rows)
    from .dashboard import build
    build(frames, log, js, c)
    print(f"{len(new_rows)} new events; log size {len(log)}")


if __name__ == "__main__":
    main()
