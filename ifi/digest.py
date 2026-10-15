"""v1.4.1 alert log and nightly digest: the machine-readable state a reader (or a scheduled Claude brief) needs.

  logs/alerts.jsonl  every alert a run produced, whether or not a phone push is configured (NTFY_TOPIC);
                     one JSON record per run that had alerts, newest last, the last 500 runs kept
  logs/digest.json   the latest state in one small file: data freshness, allocation board and breaker,
                     process health, open / pending / recently closed paper trades with their tags and the
                     F1 view (would the pre-registered skip rule skip it; descriptive until it passes),
                     new playbook signals, candidates, research verdicts

The repo is public: tickers, prices and statistics only, never account details.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from .data import ROOT

ALERTS = ROOT / "logs" / "alerts.jsonl"
DIGEST = ROOT / "logs" / "digest.json"
KEEP_RUNS = 500
F1_DIST, F1_STAGE = 1.5, 1        # research/ranking/prereg_ranking_v1.yaml (F1): skip dist > 1.5 ATR or stage < 1


def _clean(o):
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(o) else round(float(o), 4)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (pd.Timestamp, datetime)):
        return None if pd.isna(o) else str(o)[:16]
    if o is pd.NaT:
        return None
    return o


def alert_text(c: dict, new_rows: list[dict], extra: list[str] | None = None) -> list[str]:
    """The alert lines of a run (the same lines ntfy receives)."""
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
    return list(extra or []) + lines


def log_alerts(lines: list[str], now: pd.Timestamp | None = None) -> None:
    if not lines:
        return
    now = now or pd.Timestamp.now(tz="UTC")
    old = ALERTS.read_text().splitlines() if ALERTS.exists() else []
    old.append(json.dumps(dict(utc=now.strftime("%Y-%m-%d %H:%M"), lines=lines)))
    ALERTS.parent.mkdir(parents=True, exist_ok=True)
    ALERTS.write_text("\n".join(old[-KEEP_RUNS:]) + "\n")


def recent_alerts(days: int = 7, now: pd.Timestamp | None = None) -> list[dict]:
    if not ALERTS.exists():
        return []
    now = now or pd.Timestamp.now(tz="UTC")
    out = []
    for ln in ALERTS.read_text().splitlines():
        try:
            rec = json.loads(ln)
        except ValueError:
            continue
        if pd.Timestamp(rec["utc"], tz="UTC") >= now - pd.Timedelta(days=days):
            out.append(rec)
    return out


def f1_view(row) -> str | None:
    """Would the pre-registered F1 rule skip this E4 signal? Descriptive until the ranking test passes."""
    if not str(row.get("setup", "")).startswith("E4"):
        return None
    d, s = row.get("tag_dist_anchor_atr"), row.get("tag_stage")
    if d is None or s is None or (isinstance(d, float) and np.isnan(d)) or (isinstance(s, float) and np.isnan(s)):
        return "unknown"
    return "skip" if (float(d) > F1_DIST or int(s) < F1_STAGE) else "take"


def _trade(r: pd.Series) -> dict:
    keys = ["symbol", "setup", "universe", "signal_bar", "status", "fill_date", "fill", "stop", "target", "exit_date",
            "exit_reason", "r", "cancel_if_open_below", "tag_stage", "tag_dist_anchor_atr", "tag_stop_width",
            "tag_spy_trend200", "tag_signals_same_day"]
    d = {k: r.get(k) for k in keys if k in r.index}
    d["setup"] = str(d.get("setup", "")).split("_")[0]
    d["f1_view"] = f1_view(r)
    return d


def research_verdicts() -> dict:
    out = {}
    for name, f in (("exits_v1", ROOT / "reports" / "exits" / "EXITS_meta.json"),
                    ("ranking_v1", ROOT / "reports" / "ranking" / "RANKING_meta.json")):
        if f.exists():
            try:
                m = json.loads(f.read_text())
                out[name] = dict(verdicts=m.get("verdicts"), run_utc=m.get("run_utc"))
            except ValueError:
                pass
    out["profile"] = (ROOT / "reports" / "profile" / "E4_PROFILE.md").exists()
    return out


def write_digest(pt: pd.DataFrame, board: dict, pmeta: dict, health: dict, fresh: dict, c14: dict,
                 new_rows: list[dict], lines: list[str], now: pd.Timestamp | None = None) -> dict:
    now = now or pd.Timestamp.now(tz="UTC")
    live = pt[pt["oos"].astype(bool)] if not pt.empty and "oos" in pt else pd.DataFrame()
    def pick(status, n=None):
        if live.empty:
            return []
        d = live[live["status"] == status]
        if status == "closed":
            d = d.assign(_x=pd.to_datetime(d["exit_date"].astype(str), errors="coerce")).sort_values("_x")
            d = d.tail(n or len(d))
        return [_trade(r) for _, r in d.iterrows()]
    out = dict(
        generated_utc=now.strftime("%Y-%m-%d %H:%M"),
        what="IFI Lab nightly digest (public repo: tickers and statistics only)",
        freshness={k: fresh.get(k) for k in ("expected", "stale", "still_stale", "check_failed", "spy_last")},
        allocation={k: {f: v.get(f) for f in ("risk", "p_edge", "posterior_mean", "live_n", "live_expectancy", "live_total_r",
                                              "open_trades", "losing_streak", "streak_p", "streak_flag", "streak_method", "prior_mean")}
                    for k, v in board.items()},
        portfolio=pmeta,
        health={k: {f: v.get(f) for f in ("live_signals", "skip_live", "skip_pre", "stop_width_live", "stop_width_pre", "ks_p", "ks_flag")}
                for k, v in health.items()},
        paper=dict(open=pick("open"), pending=pick("pending"), closed_recent=pick("closed", 10),
                   live_closed_n=int((live["status"] == "closed").sum()) if not live.empty else 0,
                   live_signals_n=int(len(live)), universe_rows=int(len(pt))),
        playbook_new=[{k: r.get(k) for k in ("symbol", "tf", "event", "close", "stop", "target", "cancel_if_open_below")}
                      for r in new_rows if r.get("family") == "Playbook"],
        alerts_this_run=lines,
        alerts_last_7d=sum(len(r["lines"]) for r in recent_alerts(7, now)),
        candidates=c14.get("candidates", []),
        research=research_verdicts(),
        f1_rule="F1 (ranking test v1, pre-registered): skip E4 signals more than 1.5 ATR above the anchor or at IFI stage < 1. "
                "f1_view is descriptive until that test passes.",
    )
    DIGEST.parent.mkdir(parents=True, exist_ok=True)
    DIGEST.write_text(json.dumps(_clean(out), indent=1))
    return out
