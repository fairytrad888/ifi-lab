"""Truncation test on real data: nothing at or before a cut week may change when later bars are deleted."""
from __future__ import annotations

import hashlib

import numpy as np
import pandas as pd

from weekscan import scan
from weekscan.run import CFG as WCFG

from . import events

COLS = ["ad_washout", "ad_washout_exit", "ad_flow", "ad_bull_div", "sig_trig_bull", "sig_bull_streak",
        "mx_strong_bull", "tr_nine", "stage", "dist_anchor_atr", "low", "close"]


def _same(a: pd.Series, b: pd.Series) -> bool:
    x = pd.to_numeric(a, errors="coerce").astype(float).to_numpy()
    y = pd.to_numeric(b, errors="coerce").astype(float).to_numpy()
    return len(x) == len(y) and np.allclose(np.nan_to_num(x, nan=-9e99), np.nan_to_num(y, nan=-9e99),
                                            rtol=1e-9, atol=1e-12)


def check(daily: dict, symbols: list[str], prereg: dict, end: str, n_sym: int, cuts: int, seed: int,
          etf_pair: tuple[str, str] = ("XLK", "SMH")) -> dict:
    E = prereg["events"]
    win, pair = E["window_weeks"], E["pair_signals"]
    uc = WCFG["universe"]
    keyed = sorted(symbols, key=lambda s: hashlib.sha256(f"R007-lookahead:{s}".encode()).hexdigest())
    rng = np.random.default_rng(seed)
    tested, bad = 0, []
    fid_bad, fid_weeks, fid_arms = [], 0, 0
    for s in keyed:
        if tested >= n_sym:
            break
        if s not in daily:
            continue
        d = daily[s]
        w = events.weekly(d, end)
        x = scan.read_weekly(w)
        if x is None or len(x) < 300:
            continue
        r = events.records(x, win, pair)
        el = events.eligibility(d, w, uc["min_price"], uc["min_dollar_volume"])
        args = (WCFG["arm_weeks"], WCFG["repeat_block_weeks"], pd.Timestamp("1900-01-01"),
                pd.Timestamp("2100-01-01"), E["min_weekly_bars"])
        ev = events.replay(r, el, True, *args)
        tested += 1
        # fidelity to the live code on real data: arms vs weekscan step (no release), week records vs week_records
        arms_mine = events.replay(r, pd.Series(True, index=r.index), True, WCFG["arm_weeks"], 0,
                                  pd.Timestamp("1900-01-01"), pd.Timestamp("2100-01-01"), 1)
        state, arms_live = {}, []
        for w_ in r.index:
            rec = scan.week_records({s: x}, w_, win, pair)
            state, _, evs = scan.step(state, w_, rec, {s: "G"}, {"G": "neutral"}, {s}, WCFG)
            arms_live += [w_ for e in evs if e["event"].startswith("armed")]
        fid_arms += len(arms_live)
        if [r.index[i] for i in arms_mine] != arms_live:
            fid_bad.append(f"{s}: arms {len(arms_mine)} vs weekscan {len(arms_live)}")
        for c in sorted(rng.integers(150, len(x) - 1, size=cuts)):
            we = x.index[c]
            dt = d[d.index <= we]
            wt = events.weekly(dt, end)
            xt = scan.read_weekly(wt)
            rt = events.records(xt, win, pair)
            elt = events.eligibility(dt, wt, uc["min_price"], uc["min_dollar_volume"])
            evt = events.replay(rt, elt, True, *args)
            ref = scan.week_records({s: x}, x.index[c], win, pair)[s]
            got = r.iloc[c]
            fid_weeks += 1
            if not (bool(got["cond"]) == ref["cond"] and bool(got["new"]) == ref["new"]
                    and abs(got["low"] - ref["low"]) < 1e-9 and int(got["stage"]) == ref["stage"]
                    and [k for k in pair if got[f"f_{k}"] == 1] == ref["signals"]):
                fid_bad.append(f"{s} {x.index[c].date()}: week record differs")
            diffs = [k for k in COLS if not _same(x[k].iloc[:c + 1], xt[k])]
            diffs += [f"rec:{k}" for k in rt.columns if not _same(r[k].iloc[:c + 1], rt[k])]
            if not _same(el.iloc[:c + 1], elt):
                diffs.append("eligible")
            if [i for i in ev if i <= c] != evt:
                diffs.append("events")
            if diffs:
                bad.append({"symbol": s, "cut": str(we.date()), "differs": diffs})
    # group state on two ETFs
    gbad = []
    spy = daily.get(WCFG["benchmark"])
    for e in etf_pair:
        if e not in daily or spy is None:
            continue
        full = scan.group_states({e: events.weekly(daily[e], end)}, events.weekly(spy, end)).get(e)
        if full is None:
            continue
        for c in sorted(rng.integers(150, len(full) - 1, size=cuts)):
            we = full.index[c]
            t = scan.group_states({e: events.weekly(daily[e][daily[e].index <= we], end)},
                                  events.weekly(spy[spy.index <= we], end)).get(e)
            if t is None or not (full.iloc[:c + 1].astype(str).to_numpy() == t.astype(str).to_numpy()).all():
                gbad.append({"etf": e, "cut": str(we.date())})
    return {"symbols_tested": tested, "cuts": cuts, "failures": bad[:30], "n_failures": len(bad),
            "group_state_failures": gbad, "ok": not bad and not gbad,
            "fidelity_weeks": fid_weeks, "fidelity_arms": fid_arms, "fidelity_failures": fid_bad[:30],
            "fidelity_ok": not fid_bad}
