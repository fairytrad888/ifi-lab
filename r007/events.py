"""R007 events and features (no outcomes).

Events reuse the live weekly scan's definitions (weekscan.scan): the v1.1 condition (red A&D bar + a pair signal in a
4-week window), the arm / disarm / expiry logic without release, and the group, breadth and score inputs. Everything
is computed from bars up to the event week; the Phase 0 truncation test checks this on real data.
"""
from __future__ import annotations

from datetime import datetime, time, timedelta, timezone

import numpy as np
import pandas as pd
import yaml

from weekscan import scan
from weekscan.marketdata import weekly as _md_weekly
from weekscan.run import CFG as WCFG
from weekscan.universe import map_etfs

FEATURES = ["n_types", "f_signals_trigger", "f_ad_divergence", "f_matrix_divergence", "f_down9",
            "f_accumulation_exit", "trig2", "red_age", "flow_min", "stage", "group_state", "breadth_acc",
            "breadth_stage2", "leader", "stop_pct", "dist_anchor_atr"]


def weekly(d: pd.DataFrame, end: str) -> pd.DataFrame:
    """Weekly bars ending Friday, up to and including the week of `end` (as weekscan, run the next day)."""
    now = datetime.combine(pd.Timestamp(end).date() + timedelta(days=1), time(0), tzinfo=timezone.utc)
    return _md_weekly(d, now)


def records(x: pd.DataFrame, window: int, pair: list[str]) -> pd.DataFrame:
    """Vectorized weekscan.scan.week_records for every week, plus the R007 tag columns."""
    red = x["ad_washout"].astype(bool)
    flags = {k: scan._flag(x, k) for k in pair}

    def roll(s: pd.Series) -> pd.Series:
        return s.astype(bool).astype(int).rolling(window, min_periods=1).max().astype(bool)

    seen = {k: roll(f) for k, f in flags.items()}
    any_seen = pd.concat(seen.values(), axis=1).any(axis=1)
    any_now = pd.concat([f.astype(bool) for f in flags.values()], axis=1).any(axis=1)
    r = pd.DataFrame(index=x.index)
    r["cond"] = roll(red) & any_seen
    r["new"] = red | any_now
    r["low"] = x["low"].rolling(window, min_periods=1).min()
    r["close"] = x["close"]
    r["stage"] = x["stage"].astype(int)
    for k in pair:
        r[f"f_{k}"] = seen[k].astype(int)
    r["n_types"] = np.minimum(pd.concat(seen.values(), axis=1).sum(axis=1), 3).astype(int)
    pos = np.arange(len(x), dtype=float)
    last_red = pd.Series(np.where(red.to_numpy(), pos, np.nan), index=x.index).ffill().to_numpy()
    age = pos - last_red
    r["red_age"] = np.where(age < window, age, np.nan)
    r["flow_min"] = x["ad_flow"].rolling(window, min_periods=1).min()
    trig = flags["signals_trigger"].astype(bool) if "signals_trigger" in flags else pd.Series(False, index=x.index)
    streak = x["sig_bull_streak"].where(trig).ffill(limit=window - 1)
    r["trig2"] = (streak >= 2).astype(int)
    r["dist_anchor_atr"] = x["dist_anchor_atr"]
    r["acc8"] = (x["ad_washout"].astype(bool) | x["ad_washout_exit"].astype(bool)).astype(int).rolling(
        8, min_periods=1).max().astype(bool)
    return r


def eligibility(daily: pd.DataFrame, wk: pd.DataFrame, min_price: float, min_dv: float) -> pd.Series:
    """Point-in-time: the price floor uses the price as it traded then (split-adjusted close x later split factor);
    dollar volume is unchanged by splits (price / k x volume x k)."""
    dv = (daily["close"] * daily["volume"]).rolling(20, min_periods=20).mean()
    dvw = dv.resample("W-FRI").last().reindex(wk.index)
    if "split_factor" in daily.columns:
        fw = daily["split_factor"].resample("W-FRI").last().reindex(wk.index).fillna(1.0)
    else:
        fw = pd.Series(1.0, index=wk.index)
    return ((wk["close"] * fw >= min_price) & (dvw >= min_dv)).fillna(False).astype(bool)


def _weeks(a: pd.Timestamp, b: pd.Timestamp) -> int:
    return int(round((b - a).days / 7))


def replay(rec: pd.DataFrame, elig: pd.Series, has_group: bool, arm_weeks: int, block_weeks: int,
           ev_from: pd.Timestamp, ev_to: pd.Timestamp, min_bars: int) -> list[int]:
    """weekscan.scan.step for one stock without release; returns the positions of R007 events."""
    weeks = rec.index
    cond, new = rec["cond"].to_numpy(), rec["new"].to_numpy()
    low, close = rec["low"].to_numpy(), rec["close"].to_numpy()
    el = elig.reindex(weeks).fillna(False).to_numpy(dtype=bool)
    armed_w, armed_low, last_ev, out = None, np.nan, None, []
    for i, w in enumerate(weeks):
        if armed_w is not None:
            if close[i] < armed_low or _weeks(armed_w, w) > arm_weeks:
                armed_w = None
        if cond[i] and el[i] and has_group:
            if armed_w is not None:
                armed_low = min(armed_low, low[i])
            elif new[i]:
                armed_w, armed_low = w, low[i]
                if (ev_from <= w <= ev_to and i >= min_bars - 1
                        and (last_ev is None or _weeks(last_ev, w) >= block_weeks)):
                    out.append(i)
                    last_ev = w
    return out


def group_map(u: pd.DataFrame, gser: dict) -> dict[str, str]:
    """As weekscan.run: the industry ETF if it has a state series, else the sector ETF."""
    cols = [c for c in ["symbol", "name", "sector", "sub_industry", "index"] if c in u.columns]
    m = map_etfs(u[cols].copy(), WCFG).set_index("symbol")
    out = {}
    for s, row in m.iterrows():
        g = row["group_etf"]
        if g not in gser:
            g = row["sector_etf"]
        if g in gser:
            out[s] = g
    return out


def w_score(ev: pd.DataFrame) -> pd.Series:
    w = WCFG["score"]
    gs = ev["group_state"].map({"bullish": w["bullish"], "basing": w["basing"]}).fillna(0.0)
    sc = gs + w["breadth_accumulation"] * ev["breadth_acc"].fillna(0.0) \
        + w["breadth_stage2"] * ev["breadth_stage2"].fillna(0.0) \
        + w["leader"] * (ev["leader"] == 1).astype(float) \
        + w["per_signal_type"] * np.minimum(ev["n_types"], w["max_signal_types"]) \
        + np.where(ev["stop_pct"] > w["wide_stop_pct"], w["wide_stop_penalty"], 0.0)
    return sc.round(3)


def build(daily: dict[str, pd.DataFrame], u: pd.DataFrame, prereg: dict, end: str,
          log=print) -> tuple[pd.DataFrame, dict]:
    """All R007 events with features. u: universe with symbol, name, sector, sub_industry, index, set."""
    E = prereg["events"]
    window, pair = E["window_weeks"], E["pair_signals"]
    ev_from, ev_to = (pd.Timestamp(d) for d in E["event_weeks"])
    uc = WCFG["universe"]
    etfs = sorted(set(WCFG["sector_etfs"].values()) | set(WCFG["industry_etfs"].values()))
    spy_w = weekly(daily[WCFG["benchmark"]], end)
    etf_w = {e: weekly(daily[e], end) for e in etfs if e in daily}
    gser = scan.group_states(etf_w, spy_w)
    group_of = group_map(u, gser)
    info = {"etfs_with_state": len(gser), "stocks": 0, "no_group": 0, "short_history": 0, "no_data": 0}
    recs, eligs, wks = {}, {}, {}
    acc_sum, st2_sum, cnt = {}, {}, {}
    for k, s in enumerate(u["symbol"]):
        if s not in daily:
            info["no_data"] += 1
            continue
        w = weekly(daily[s], end)
        x = scan.read_weekly(w)
        if x is None:
            info["short_history"] += 1
            continue
        r = records(x, window, pair)
        recs[s], wks[s] = r, w
        eligs[s] = eligibility(daily[s], w, uc["min_price"], uc["min_dollar_volume"])
        g = group_of.get(s)
        if g is None:
            info["no_group"] += 1
        else:
            for d_, v in ((acc_sum, r["acc8"].astype(float)), (st2_sum, (r["stage"] >= 2).astype(float)),
                          (cnt, pd.Series(1.0, index=r.index))):
                d_[g] = v if g not in d_ else d_[g].add(v, fill_value=0.0)
        info["stocks"] += 1
        if (k + 1) % 250 == 0:
            log(f"  read {k + 1}/{len(u)}")
    breadth = {g: pd.DataFrame({"breadth_acc": acc_sum[g] / cnt[g], "breadth_stage2": st2_sum[g] / cnt[g]})
               for g in cnt}
    sets = u.set_index("symbol")["set"].to_dict()
    rows = []
    for s, r in recs.items():
        if sets.get(s, "X") not in ("S1", "S2", "S3", "E"):
            continue                                   # excluded stocks (X, XD) only feed breadth
        g = group_of.get(s)
        pos = replay(r, eligs[s], g is not None, WCFG["arm_weeks"], WCFG["repeat_block_weeks"],
                     ev_from, ev_to, E["min_weekly_bars"])
        if not pos:
            continue
        lr = None
        if g in etf_w:
            lr = scan.read_weekly(scan.ratio_bars(wks[s], etf_w[g]))
        for i in pos:
            wk_ = r.index[i]
            row = {"symbol": s, "set": sets[s], "week": wk_.date().isoformat(), "group": g}
            for c in ["close", "low", "stage", "n_types", "trig2", "red_age", "flow_min", "dist_anchor_atr"] + \
                     [f"f_{k}" for k in pair]:
                row[c] = r[c].iloc[i]
            row["stop_pct"] = (row["close"] - row["low"]) / row["close"] if row["close"] else np.nan
            st = gser[g].get(wk_) if g in gser else None
            row["group_state"] = st if isinstance(st, str) else "missing"
            b = breadth.get(g)
            row["breadth_acc"] = b["breadth_acc"].get(wk_, np.nan) if b is not None else np.nan
            row["breadth_stage2"] = b["breadth_stage2"].get(wk_, np.nan) if b is not None else np.nan
            row["leader"] = (int(lr.loc[wk_, "stage"] >= 1) if lr is not None and wk_ in lr.index else np.nan)
            rows.append(row)
    ev = pd.DataFrame(rows)
    if len(ev):
        ev["w_score"] = w_score(ev)
        ev = ev.sort_values(["week", "symbol"]).reset_index(drop=True)
    info["groups"] = len(breadth)
    return ev, info


def load_prereg(path) -> dict:
    return yaml.safe_load(open(path).read())
