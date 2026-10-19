"""Weekly scan logic (pure functions; no downloads, no files).

Sector state  each sector / industry ETF's ratio to SPY on weekly bars, IFI stage at the week's close:
              2-3 bullish · 1 basing · 0 neutral · -1 bearish
Stock signal  the weekly IFI A&D accumulation bar (washout exit) at the week's close
Arm/release   an accumulation bar arms the stock for `arm_weeks` while weekly closes hold above that bar's low.
              It is released (one alert) when its group ETF is bullish or basing: in the same week, or later
              when the group turns. Repeat alerts for a stock are blocked for `repeat_block_weeks`.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .core.states import read

STATE_OF_STAGE = {3: "bullish", 2: "bullish", 1: "basing", 0: "neutral", -1: "bearish"}


def ratio_bars(a: pd.DataFrame, b: pd.DataFrame) -> pd.DataFrame:
    j = a.index.intersection(b.index)
    a, b = a.loc[j], b.loc[j]
    r = pd.DataFrame({k: a[k] / b[k] for k in ("open", "high", "low", "close")}, index=j)
    r["high"] = r[["open", "high", "low", "close"]].max(axis=1)
    r["low"] = r[["open", "high", "low", "close"]].min(axis=1)
    r["volume"] = 0.0
    return r.replace([np.inf, -np.inf], np.nan).dropna()


def read_weekly(w: pd.DataFrame) -> pd.DataFrame | None:
    if w is None or len(w) < 80:
        return None
    return read(w[["open", "high", "low", "close", "volume"]])


def group_states(etf_weekly: dict[str, pd.DataFrame], spy_w: pd.DataFrame) -> dict[str, pd.Series]:
    """ETF -> weekly series of 'bullish' / 'basing' / 'neutral' / 'bearish' (ratio to SPY)."""
    out = {}
    for e, w in etf_weekly.items():
        x = read_weekly(ratio_bars(w, spy_w))
        if x is not None:
            out[e] = x["stage"].map(STATE_OF_STAGE)
    return out


def stock_reads(stock_weekly: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    out = {}
    for s, w in stock_weekly.items():
        x = read_weekly(w)
        if x is not None:
            out[s] = x
    return out


def week_records(reads: dict[str, pd.DataFrame], week: pd.Timestamp, tags_weeks: int) -> dict[str, dict]:
    """Per stock at `week`: accumulation flag, that bar's low, close, tags, stage."""
    recs = {}
    for s, x in reads.items():
        if week not in x.index:
            continue
        i = x.index.get_loc(week)
        lo = max(0, i - tags_weeks + 1)
        recs[s] = {"acc": bool(x["ad_washout_exit"].iloc[i]), "low": float(x["low"].iloc[i]),
                   "close": float(x["close"].iloc[i]), "stage": int(x["stage"].iloc[i]),
                   "tag_ad_div": bool(x["ad_bull_div"].iloc[lo:i + 1].any()),
                   "tag_trigger": bool(x["sig_trig_bull"].iloc[lo:i + 1].any())}
    return recs


def breadth(reads: dict[str, pd.DataFrame], members: dict[str, list[str]], week: pd.Timestamp, weeks: int) -> dict:
    """Group -> share of members with an accumulation bar in the last `weeks` weeks, and share at stage >= 2."""
    out = {}
    for g, syms in members.items():
        acc = st2 = n = 0
        for s in syms:
            x = reads.get(s)
            if x is None or week not in x.index:
                continue
            i = x.index.get_loc(week)
            n += 1
            acc += bool(x["ad_washout_exit"].iloc[max(0, i - weeks + 1):i + 1].any())
            st2 += int(x["stage"].iloc[i]) >= 2
        out[g] = {"n": n, "acc_share": acc / n if n else np.nan, "stage2_share": st2 / n if n else np.nan}
    return out


def _weeks_between(a: str, b: pd.Timestamp) -> int:
    return int(round((b - pd.Timestamp(a)).days / 7))


def step(state: dict, week: pd.Timestamp, recs: dict[str, dict], group_of: dict[str, str],
         gstate: dict[str, str], eligible: set[str], cfg: dict) -> tuple[dict, list[dict], list[dict]]:
    """Advance the arm/release state by one completed week. Returns (state, releases, log events)."""
    arm_w, block_w = cfg["arm_weeks"], cfg["repeat_block_weeks"]
    ok_states = set(cfg["qualifying_states"])
    armed, alerted = dict(state.get("armed", {})), dict(state.get("alerted", {}))
    wk = str(week.date())
    events, releases = [], []
    # 1. disarm: low broken on a weekly close, or expired
    for s, a in list(armed.items()):
        r = recs.get(s)
        age = _weeks_between(a["armed_week"], week)
        if r is None:
            continue
        if r["close"] < a["low"]:
            events.append({"week": wk, "symbol": s, "event": "disarmed: weekly close below the accumulation low"})
            armed.pop(s)
        elif age > arm_w:
            events.append({"week": wk, "symbol": s, "event": f"expired after {arm_w} weeks"})
            armed.pop(s)
    # 2. arm: a new accumulation bar this week (re-arms with the new low)
    for s, r in recs.items():
        if r["acc"] and s in eligible and s in group_of:
            armed[s] = {"armed_week": wk, "low": r["low"], "group": group_of[s], "released": False,
                        "tag_ad_div": r["tag_ad_div"], "tag_trigger": r["tag_trigger"]}
            events.append({"week": wk, "symbol": s, "event": "armed: weekly accumulation bar"})
    # 3. release: the group ETF is bullish or basing
    for s, a in armed.items():
        if a["released"]:
            continue
        g = a["group"]
        st = gstate.get(g)
        if st not in ok_states:
            continue
        a["released"] = True
        age = _weeks_between(a["armed_week"], week)
        why = (f"accumulation this week in a {st} group" if age == 0
               else f"group turned {st}, {age} week{'s' if age != 1 else ''} after the accumulation")
        last = alerted.get(s)
        if last is not None and _weeks_between(last, week) < block_w:
            events.append({"week": wk, "symbol": s, "event": f"suppressed (alerted {last}): {why}"})
            continue
        r = recs.get(s, {})
        releases.append({"week": wk, "symbol": s, "group": g, "group_state": st, "reason": why,
                         "armed_week": a["armed_week"], "acc_low": a["low"], "close": r.get("close", np.nan),
                         "tag_ad_div": a["tag_ad_div"] or r.get("tag_ad_div", False),
                         "tag_trigger": a["tag_trigger"] or r.get("tag_trigger", False)})
        alerted[s] = wk
        events.append({"week": wk, "symbol": s, "event": f"released: {why}"})
    return {"armed": armed, "alerted": alerted, "last_week": wk}, releases, events


def score(rel: dict, br: dict, leader: bool | None, cfg: dict) -> float:
    w = cfg["score"]
    sc = w["bullish"] if rel["group_state"] == "bullish" else w["basing"]
    b = br.get(rel["group"], {})
    sc += w["breadth_accumulation"] * np.nan_to_num(b.get("acc_share", 0.0))
    sc += w["breadth_stage2"] * np.nan_to_num(b.get("stage2_share", 0.0))
    sc += w["leader"] * bool(leader)
    sc += w["tag_ad_divergence"] * bool(rel["tag_ad_div"]) + w["tag_signals_trigger"] * bool(rel["tag_trigger"])
    stop = (rel["close"] - rel["acc_low"]) / rel["close"] if rel["close"] else np.nan
    rel["stop_pct"] = float(stop)
    if stop == stop and stop > w["wide_stop_pct"]:
        sc += w["wide_stop_penalty"]
    return float(round(sc, 3))
