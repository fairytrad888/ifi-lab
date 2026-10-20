"""IFI weekly accumulation alerts: one run per completed week (Saturday). v1.1: red accumulation bar + a pairing signal.

  python -m weekscan.run [--out DIR] [--no-push] [--seed-weeks 8]

Output (WEEKSCAN_OUT, default weekscan/_out):
  LATEST.md                     this week's report (also weeks/<friday>/ALERTS.md)
  weeks/<friday>/alerts.csv     ranked releases with their context
  weeks/<friday>/groups.csv     every sector / industry ETF: state, change, breadth
  weeks/<friday>/charts/*.png   weekly IFI chart for each pushed alert
  state.json                    armed stocks and last alert per stock (arm and release memory)
  alerts_log.csv, events.csv    every release / arm / disarm, appended
  universe.csv                  the S&P 1500 list used
The first run (no state) replays the previous `seed_weeks` weeks silently, so only this week's releases are pushed.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from . import marketdata as md
from . import notify, scan
from .universe import fetch, map_etfs

ROOT = Path(__file__).resolve().parent
CFG = yaml.safe_load((ROOT / "config.yaml").read_text())


def out_dir(arg: str | None) -> Path:
    p = Path(arg or os.environ.get("WEEKSCAN_OUT") or ROOT / "_out").resolve()
    repo = ROOT.parent
    if (repo in p.parents or p == repo) and not (p == (ROOT / "_out").resolve() or (ROOT / "_out").resolve() in p.parents):
        raise RuntimeError(f"output {p} is inside the repository outside weekscan/_out: refused (isolation)")
    p.mkdir(parents=True, exist_ok=True)
    return p


def _append_csv(f: Path, rows: list[dict]):
    if not rows:
        return
    new = not f.exists()
    cols = list(rows[0].keys())
    if not new:
        with f.open() as fh:
            cols = next(csv.reader(fh))
    with f.open("a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        if new:
            w.writeheader()
        w.writerows(rows)


def earnings_soon(sym: str, ref: pd.Timestamp, days: int) -> bool | None:
    if os.environ.get("WEEKSCAN_OFFLINE"):
        return None
    try:
        import yfinance as yf
        e = yf.Ticker(sym).get_earnings_dates(limit=8)
        if e is None or e.empty:
            return None
        d = pd.to_datetime(e.index).tz_localize(None).normalize()
        return bool(((d > ref) & (d <= ref + pd.Timedelta(days=days))).any())
    except Exception:
        return None


def run(out: Path, push: bool = True, seed_weeks: int = 8, now: datetime | None = None,
        universe: pd.DataFrame | None = None, daily: dict | None = None) -> dict:
    now = now or datetime.now(timezone.utc)
    notes = []
    # 1. universe
    if universe is None:
        try:
            universe, fnotes = fetch(CFG["universe"]["sources"])
            notes += fnotes
            if fnotes and (out / "universe.csv").exists():      # partial fetch: keep the full saved list instead
                universe = pd.read_csv(out / "universe.csv")
                notes.append("used the saved constituent list because a source failed")
            else:
                universe.to_csv(out / "universe.csv", index=False)
        except Exception as e:
            if (out / "universe.csv").exists():
                universe = pd.read_csv(out / "universe.csv")
                notes.append(f"constituent fetch failed ({type(e).__name__}); used the saved list")
            else:
                raise
    u = map_etfs(universe, CFG)
    by_idx = u.groupby("index").size().to_dict() if "index" in u else {}
    notes.append(f"universe: {len(u)} stocks ({', '.join(f'{k} {v}' for k, v in sorted(by_idx.items()))}); "
                 f"{int(u['industry_etf'].notna().sum())} mapped to an industry ETF, "
                 f"{int(u['sector_etf'].isna().sum())} with no sector ETF")
    etfs = sorted(set(CFG["sector_etfs"].values()) | set(CFG["industry_etfs"].values()))
    # 2. data
    missing = []
    if daily is None:
        daily, missing = md.daily(sorted(set(u["symbol"])) + etfs + [CFG["benchmark"]], CFG["history"])
    spy_w = md.weekly(daily[CFG["benchmark"]], now)
    current = spy_w.index[-1]
    wk = {s: md.weekly(d, now) for s, d in daily.items()}
    gser = scan.group_states({e: wk[e] for e in etfs if e in wk}, spy_w)
    stocks = [s for s in u["symbol"] if s in wk]
    reads = scan.stock_reads({s: wk[s] for s in stocks})
    uc = CFG["universe"]
    eligible = {s for s in reads if daily[s]["close"].iloc[-1] >= uc["min_price"]
                and md.dollar_volume(daily[s]) >= uc["min_dollar_volume"]}
    u = u.set_index("symbol")
    group_of = {}
    for s in reads:
        g = u.at[s, "group_etf"] if s in u.index else None
        if g not in gser:
            g = u.at[s, "sector_etf"] if s in u.index else None
        if g in gser:
            group_of[s] = g
    members: dict[str, list[str]] = {}
    for s, g in group_of.items():
        members.setdefault(g, []).append(s)
    # 3. weeks to process (state = arm/release memory)
    sf = out / "state.json"
    state = json.loads(sf.read_text()) if sf.exists() else {}
    weeks = list(spy_w.index)
    if state and state.get("version") != scan.STATE_VERSION:
        state = {"alerted": state.get("alerted", {}), "version": scan.STATE_VERSION}
        todo = weeks[-(seed_weeks + 1):]
        notes.append(f"trigger upgraded (state v{scan.STATE_VERSION}): the {seed_weeks} weeks before {current.date()} were "
                     "replayed silently with the new trigger; earlier alerts still block repeats")
    elif state.get("last_week") and pd.Timestamp(state["last_week"]) in spy_w.index:
        todo = [w for w in weeks if w > pd.Timestamp(state["last_week"])]
    else:
        todo = weeks[-(seed_weeks + 1):]
        notes.append(f"first run: the {seed_weeks} weeks before {current.date()} were replayed silently to build the armed list")
    if not todo:
        return {"week": str(current.date()), "status": "already processed; nothing pushed", "notes": notes}
    all_events, releases = [], []
    for w in todo:
        gstate = {g: s.get(w) for g, s in gser.items()}
        recs = scan.week_records(reads, w, CFG["signal"]["window_weeks"], CFG["signal"]["pair_signals"])
        state, rel, ev = scan.step(state, w, recs, group_of, gstate, eligible, CFG)
        for r in rel:
            r["pushed"] = w == current and push
        all_events += ev
        if w == current:
            releases = rel
        else:
            _append_csv(out / "alerts_log.csv", [{**r, "seeded": True} for r in rel])
    # 4. rank this week's releases
    br = scan.breadth(reads, members, current, CFG["breadth_weeks"])
    for r in releases:
        g = r["group"]
        lr = scan.read_weekly(scan.ratio_bars(wk[r["symbol"]], wk[g])) if g in wk else None
        r["leader"] = bool(lr is not None and current in lr.index and int(lr.loc[current, "stage"]) >= 1)
        r["sector"] = u.at[r["symbol"], "sector"] if r["symbol"] in u.index else ""
        r["sub_industry"] = u.at[r["symbol"], "sub_industry"] if r["symbol"] in u.index else ""
        sec_etf = u.at[r["symbol"], "sector_etf"] if r["symbol"] in u.index else None
        r["sector_etf"] = sec_etf
        r["sector_state"] = gser[sec_etf].get(current) if sec_etf in gser else None
        r["breadth_acc"] = br.get(g, {}).get("acc_share")
        r["breadth_stage2"] = br.get(g, {}).get("stage2_share")
        r["score"] = scan.score(r, br, r["leader"], CFG)
    releases.sort(key=lambda r: (-r["score"], r["stop_pct"]))
    top = releases[:CFG["push_top"]]
    for r in releases:
        r["earnings_soon"] = earnings_soon(r["symbol"], current, CFG["earnings_flag_days"]) if r in top else None
    # 5. outputs
    wdir = out / "weeks" / str(current.date())
    (wdir / "charts").mkdir(parents=True, exist_ok=True)
    pd.DataFrame(releases).to_csv(wdir / "alerts.csv", index=False)
    grows = []
    for g in sorted(gser):
        s = gser[g]
        cur = s.get(current)
        prev = s.iloc[s.index.get_loc(current) - 1] if current in s.index and s.index.get_loc(current) > 0 else None
        grows.append({"etf": g, "state": cur, "previous": prev, "changed": cur != prev, "members": len(members.get(g, [])),
                      "breadth_acc": br.get(g, {}).get("acc_share"), "breadth_stage2": br.get(g, {}).get("stage2_share"),
                      "armed_waiting": sum(1 for a in state["armed"].values() if a["group"] == g and not a["released"])})
    gdf = pd.DataFrame(grows)
    gdf.to_csv(wdir / "groups.csv", index=False)
    from .charts import render
    for r in top:
        x = reads[r["symbol"]]
        if current in x.index:
            render(x, x.index.get_loc(current), wdir / "charts" / f"{r['symbol']}.png", bars=104, blind=False,
                   title=f"{r['symbol']} weekly · {r['group']} {r['group_state']} · {r['reason']}")
    _append_csv(out / "alerts_log.csv", [{**r, "seeded": False} for r in releases])
    _append_csv(out / "events.csv", all_events)
    sf.write_text(json.dumps(state, indent=1))
    ok = gdf[gdf["state"].isin(CFG["qualifying_states"])]
    waiting = sorted((s, a) for s, a in state["armed"].items() if not a["released"])
    repo = os.environ.get("GITHUB_REPOSITORY", "fairytrad888/ifi-lab")
    link = f"https://github.com/{repo}/blob/weekscan-results/weeks/{current.date()}/ALERTS.md"
    pct = lambda v: "–" if v is None or v != v else f"{v:.0%}"  # noqa: E731
    mdl = [f"# IFI weekly accumulation alerts · week ending {current.date()}", "",
           f"_Run {now:%Y-%m-%d %H:%M} UTC · {len(reads)} stocks read, {len(eligible)} liquid (price ≥ ${uc['min_price']:.0f}, "
           f"≥ ${uc['min_dollar_volume'] / 1e6:.0f}M a day) · {len(gser)} sector/industry ETFs · missing data: {len(missing)}_", ""]
    mdl += [f"- {n}" for n in notes] + ([""] if notes else [])
    mdl += [f"**{len(releases)} released** (top {len(top)} pushed) · {sum(1 for _ in waiting)} armed and waiting for their group · "
            f"{len(ok)} of {len(gdf)} groups bullish or basing", "",
            "## Alerts (ranked)", "",
            "| # | stock | group | why | close | stop (window low) | score | signals with the red bar | tags |",
            "|---|---|---|---|---|---|---|---|---|"]
    for k, r in enumerate(releases, 1):
        sigs = " + ".join(scan.PAIR_LABEL.get(k, k) for k in r["signals"])
        tags = " ".join(t for t, on in (("leader", r["leader"]), ("earnings ≤14d", r.get("earnings_soon"))) if on)
        sec = "" if r["sector_etf"] == r["group"] else f" · sector {r['sector_etf']} {r['sector_state']}"
        mdl.append(f"| {k} | {r['symbol']} | {r['group']} ({r['group_state']}){sec} · {r['sub_industry']} | {r['reason']} | "
                   f"{r['close']:.2f} | {r['acc_low']:.2f} ({r['stop_pct']:.0%}) | {r['score']:.2f} | {sigs} | {tags} |")
    mdl += ["", "## Groups (ETF ratio to SPY, weekly IFI stage)", "",
            "| ETF | state | last week | members | red/green accumulation in 8w | stage ≥ 2 | armed, waiting |", "|---|---|---|---|---|---|---|"]
    order = {"bullish": 0, "basing": 1, "neutral": 2, "bearish": 3}
    for g in sorted(grows, key=lambda r: (order.get(r["state"], 9), r["etf"])):
        ch = " ← new" if g["changed"] and g["previous"] is not None else ""
        mdl.append(f"| {g['etf']} | {g['state']}{ch} | {g['previous']} | {g['members']} | {pct(g['breadth_acc'])} | "
                   f"{pct(g['breadth_stage2'])} | {g['armed_waiting']} |")
    if waiting:
        mdl += ["", "## Armed, waiting for the group to turn basing or bullish", "",
                "| stock | group | armed (week) | stop (window low) | signals with the red bar |", "|---|---|---|---|---|"]
        mdl += [f"| {s} | {a['group']} ({gser[a['group']].get(current)}) | {a['armed_week']} | {a['low']:.2f} | "
                f"{' + '.join(scan.PAIR_LABEL.get(k, k) for k in a.get('signals', []))} |" for s, a in waiting]
    mdl += ["", "_Selection aid, not a tested edge: weekly sector state as a filter has not been tested yet. "
                "Signal = a red A&D accumulation bar plus at least one other bullish signal within 4 weeks. "
                "Bullish = ETF/SPY ratio at weekly stage 2-3; basing = stage 1. Stop = the window's lowest low (weekly close)._"]
    text = "\n".join(mdl) + "\n"
    (wdir / "ALERTS.md").write_text(text)
    (out / "LATEST.md").write_text(text)
    res = {"week": str(current.date()), "released": len(releases), "pushed": 0,
           "armed_waiting": len(waiting), "groups_ok": int(len(ok)), "groups": int(len(gdf)), "missing": missing,
           "notes": notes}
    if push:
        title, body = notify.message(str(current.date()), top, len(releases), int(len(ok)), int(len(gdf)))
        res["push"] = notify.push(title, body, link)
        res["pushed"] = len(top) if res["push"].startswith("push sent") else 0
    (out / "RUN.json").write_text(json.dumps(res, indent=1, default=str))
    return res


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="weekscan")
    ap.add_argument("--out")
    ap.add_argument("--no-push", action="store_true")
    ap.add_argument("--seed-weeks", type=int, default=8)
    a = ap.parse_args(argv)
    res = run(out_dir(a.out), push=not a.no_push, seed_weeks=a.seed_weeks)
    print(json.dumps(res, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
