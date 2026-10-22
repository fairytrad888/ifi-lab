"""Live reference and parity check.

The reference is the first weekscan-results commit whose state.json is version 2 (the v1.1 trigger) with
last_week = the reference week. From it R007 takes the universe (universe.csv) and the live armed list.
Parity runs the live code itself (weekscan.run.run) on the R007 snapshot, truncated to the live run's 10-year history,
and compares the armed list.
"""
from __future__ import annotations

import io
import json
import os
import shutil
import subprocess

import pandas as pd

from . import guard


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=guard.REPO, capture_output=True, text=True, check=True).stdout


def find_ref(ref: str, week: str, version: int) -> dict:
    lines = _git("log", "--reverse", "--format=%H %cI", ref, "--", "state.json").split("\n")
    for ln in filter(None, lines):
        sha, when = ln.split(" ", 1)
        try:
            st = json.loads(_git("show", f"{sha}:state.json"))
        except Exception:
            continue
        if st.get("version") == version and st.get("last_week") == week:
            uni = pd.read_csv(io.StringIO(_git("show", f"{sha}:universe.csv")))
            try:
                alerts = pd.read_csv(io.StringIO(_git("show", f"{sha}:weeks/{week}/alerts.csv")))
            except Exception:
                alerts = pd.DataFrame()
            return {"sha": sha, "when": when, "state": st, "universe": uni, "alerts": alerts}
    raise RuntimeError(f"no {ref} commit with state v{version} and last_week {week}: stop (parity reference missing)")


def run_live_code(daily: dict[str, pd.DataFrame], universe: pd.DataFrame, when: str, week: str) -> dict:
    from weekscan import run as wrun

    now = pd.Timestamp(when).tz_convert("UTC").to_pydatetime()
    start = pd.Timestamp(now.date()) - pd.DateOffset(years=10)
    end = pd.Timestamp(now.date())               # the live run saw daily bars up to its run date (weeks end at `week`)
    d = {s: df[(df.index >= start) & (df.index <= end)] for s, df in daily.items()}
    d = {s: df for s, df in d.items() if len(df) > 60}
    tmp = guard.out_dir() / "parity" / "run"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    os.environ["WEEKSCAN_OFFLINE"] = "1"
    summary = wrun.run(tmp, push=False, seed_weeks=8, now=now, universe=universe, daily=d)
    st = json.loads((tmp / "state.json").read_text())
    try:                                         # a week with no releases writes an empty alerts.csv
        al = pd.read_csv(tmp / "weeks" / week / "alerts.csv")
    except (FileNotFoundError, pd.errors.EmptyDataError):
        al = pd.DataFrame()
    got_week = summary.get("week") if isinstance(summary, dict) else None
    if got_week != week:
        raise RuntimeError(f"parity run processed week {got_week}, not {week}")
    keep = guard.out_dir() / "parity"
    (keep / "state_r007_replay.json").write_text(json.dumps(st, indent=1))
    shutil.rmtree(tmp)
    return {"state": st, "alerts": al, "summary": {k: v for k, v in summary.items() if k != "notes"}
            if isinstance(summary, dict) else {}}


def compare(live: dict, ours: dict, alerts_live: pd.DataFrame, alerts_ours: pd.DataFrame, tol: float = 0.005) -> dict:
    A, B = live.get("armed", {}), ours.get("armed", {})
    la, lb = set(A), set(B)
    shared = sorted(la & lb)
    union = la | lb
    jac = len(shared) / len(union) if union else 1.0
    wk = sum(A[s]["armed_week"] == B[s]["armed_week"] for s in shared)
    lo = sum(abs(B[s]["low"] / A[s]["low"] - 1) <= tol for s in shared if A[s]["low"])
    rel = sum(bool(A[s]["released"]) == bool(B[s]["released"]) for s in shared)
    n = max(1, len(shared))
    sa = set(alerts_live["symbol"]) if "symbol" in alerts_live else set()
    sb = set(alerts_ours["symbol"]) if "symbol" in alerts_ours else set()
    res = {"live_armed": len(la), "r007_armed": len(lb), "shared": len(shared), "jaccard": round(jac, 4),
           "armed_week_agree": round(wk / n, 4), "low_agree": round(lo / n, 4), "released_agree": round(rel / n, 4),
           "only_live": sorted(la - lb)[:40], "only_r007": sorted(lb - la)[:40],
           "week_alerts_live": len(sa), "week_alerts_r007": len(sb),
           "week_alerts_jaccard": round(len(sa & sb) / len(sa | sb), 4) if (sa | sb) else 1.0}
    res["pass"] = jac >= 0.95 and res["armed_week_agree"] >= 0.95 and res["low_agree"] >= 0.95
    return res


def explain(res: dict, daily: dict[str, pd.DataFrame], when: str) -> dict:
    """How many armed-list mismatches sit near the live eligibility thresholds at the live run date."""
    from weekscan import marketdata as md
    from weekscan.run import CFG as WCFG

    uc = WCFG["universe"]
    day = pd.Timestamp(pd.Timestamp(when).tz_convert("UTC").date())
    syms = list(res.get("only_live", [])) + list(res.get("only_r007", []))
    near = 0
    for s in syms:
        d = daily.get(s)
        if d is None:
            continue
        d = d[d.index <= day]
        if d.empty:
            continue
        px, dv = float(d["close"].iloc[-1]), md.dollar_volume(d)
        if abs(px / uc["min_price"] - 1) <= 0.10 or abs(dv / uc["min_dollar_volume"] - 1) <= 0.25:
            near += 1
    return {"total": len(syms), "near_threshold": near}
