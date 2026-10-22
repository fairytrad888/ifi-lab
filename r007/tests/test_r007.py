"""R007 tests (synthetic data only; no network). Run: python r007/tests/test_r007.py"""
from __future__ import annotations

import ast
import json
import os
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
_TMP = tempfile.mkdtemp(prefix="r007test_")
os.environ["R007_OUT"] = _TMP                     # outside the repository
os.environ["WEEKSCAN_OFFLINE"] = "1"
os.environ.pop("R007_PHASE", None)

from weekscan import scan                          # noqa: E402
from weekscan.run import CFG as WCFG               # noqa: E402

from r007 import events, guard, lookahead, metric, outcomes, parity, power, sets   # noqa: E402

END = guard.CFG["data"]["end"]


def synth_daily(seed: int, start="2003-01-01", end=END, base=50.0, ipo=None) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range(start, end)
    if ipo:
        idx = idx[idx >= pd.Timestamp(ipo)]
    n = len(idx)
    regime = np.repeat(rng.normal(0.0003, 0.0015, n // 120 + 1), 120)[:n]
    vol = np.repeat(rng.uniform(0.012, 0.03, n // 60 + 1), 60)[:n]
    r = regime + vol * rng.standard_t(5, n) / 1.3
    c = base * np.exp(np.cumsum(r))
    o = c * np.exp(rng.normal(0, 0.004, n))
    h = np.maximum(o, c) * np.exp(np.abs(rng.normal(0, 0.008, n)))
    lo = np.minimum(o, c) * np.exp(-np.abs(rng.normal(0, 0.008, n)))
    v = rng.integers(800_000, 3_000_000, n).astype(float)
    return pd.DataFrame({"open": o, "high": h, "low": lo, "close": c, "volume": v}, index=idx)


def synth_market(n_stocks=40):
    secs = list(WCFG["sector_etfs"].keys())
    subs = {"Information Technology": "Semiconductors", "Financials": "Regional Banks", "Energy": "Integrated Oil & Gas"}
    rows, daily = [], {}
    for k in range(n_stocks):
        s = f"S{k:03d}"
        sec = secs[k % len(secs)]
        rows.append({"symbol": s, "name": s, "sector": sec, "sub_industry": subs.get(sec, "Other") if k % 2 else "Other",
                     "index": "sp500"})
        daily[s] = synth_daily(100 + k, ipo="2012-06-01" if k == 7 else None)
    for k, s in enumerate(["AAPL", "JPM"]):                       # excluded names (X)
        rows.append({"symbol": s, "name": s, "sector": secs[k], "sub_industry": "Other", "index": "sp500"})
        daily[s] = synth_daily(900 + k)
    etfs = sorted(set(WCFG["sector_etfs"].values()) | set(WCFG["industry_etfs"].values()))
    for k, e in enumerate(etfs):
        daily[e] = synth_daily(500 + k, ipo="2015-10-08" if e == "XLRE" else ("2018-06-19" if e == "XLC" else None))
    daily["SPY"] = synth_daily(7, base=100.0)
    return pd.DataFrame(rows), daily


def t_lock():
    v = guard.verify_lock()
    assert v["ok"], v
    print(f"lock ok: {v['id'][:16]}")


def t_records_parity(daily):
    P = guard.PREREG["events"]
    n = 0
    for s in ["S000", "S003", "S011"]:
        x = scan.read_weekly(events.weekly(daily[s], END))
        r = events.records(x, P["window_weeks"], P["pair_signals"])
        for w in x.index[::3]:
            ref = scan.week_records({s: x}, w, P["window_weeks"], P["pair_signals"])[s]
            got = r.loc[w]
            assert bool(got["cond"]) == ref["cond"] and bool(got["new"]) == ref["new"], (s, w)
            assert abs(got["low"] - ref["low"]) < 1e-12 and got["stage"] == ref["stage"]
            seen = [k for k in P["pair_signals"] if got[f"f_{k}"] == 1]
            assert seen == ref["signals"], (s, w, seen, ref["signals"])
            n += 1
    print(f"records ok: vectorized == weekscan week_records on {n} weeks")


def t_replay_vs_step(daily):
    P = guard.PREREG["events"]
    tot = 0
    for s in ["S000", "S005", "S012", "S020"]:
        x = scan.read_weekly(events.weekly(daily[s], END))
        r = events.records(x, P["window_weeks"], P["pair_signals"])
        el = pd.Series(True, index=r.index)
        mine = events.replay(r, el, True, WCFG["arm_weeks"], 0, pd.Timestamp("1900-01-01"),
                             pd.Timestamp("2100-01-01"), 1)
        state, arms = {}, []
        for w in r.index:
            rec = scan.week_records({s: x}, w, P["window_weeks"], P["pair_signals"])
            state, _, ev = scan.step(state, w, rec, {s: "G"}, {"G": "neutral"}, {s}, WCFG)
            arms += [w for e in ev if e["event"].startswith("armed")]
        assert [r.index[i] for i in mine] == arms, (s, len(mine), len(arms))
        tot += len(arms)
    print(f"replay ok: arms match weekscan step without release ({tot} arms)")


def t_replay_rules():
    idx = pd.date_range("2010-01-01", periods=30, freq="W-FRI")
    r = pd.DataFrame({"cond": False, "new": False, "low": 10.0, "close": 12.0}, index=idx)
    r.loc[idx[2], ["cond", "new"]] = True                       # arm (event)
    r.loc[idx[3], ["cond", "low"]] = [True, 9.0]                # widen low while armed
    r.loc[idx[5], "close"] = 9.5                                # holds the widened low (9.0)
    r.loc[idx[6], "close"] = 8.9                                # close below 9.0: disarm
    r.loc[idx[7], ["cond", "new"]] = True                       # re-arm 5 weeks later: repeat-blocked
    r.loc[idx[20], ["cond", "new"]] = True                      # expired at week 16; new event after the block
    el = pd.Series(True, index=idx)
    ev = events.replay(r, el, True, 8, 8, idx[0], idx[-1], 1)
    assert ev == [2, 20], ev
    assert events.replay(r, el, False, 8, 8, idx[0], idx[-1], 1) == []
    assert events.replay(r, el, True, 8, 8, idx[0], idx[-1], 10) == [20]
    print("replay rules ok: arm, widen, disarm, repeat block, min bars, no group")


def t_lookahead(daily):
    syms = [f"S{k:03d}" for k in range(8)]
    res = lookahead.check(daily, syms, guard.PREREG, END, 6, 3, 1)
    assert res["ok"] and res["symbols_tested"] == 6, res
    print(f"look-ahead ok: {res['symbols_tested']} symbols x {res['cuts']} cuts identical; group states identical")


def t_outcomes():
    T = guard.PREREG["trade"]
    idx = pd.bdate_range("2020-01-01", periods=200)
    base = pd.DataFrame({"open": 100.0, "high": 101.0, "low": 99.0, "close": 100.0, "volume": 1e6}, index=idx)
    we = idx[30]                                                # event week end (a day in the index)
    atr = pd.Series(2.0, index=idx)

    def go(mod, stop=95.0):
        d = base.copy()
        mod(d)
        d.attrs["synthetic"] = True
        return outcomes.trade(d, we, stop, T, "2030-01-01", synthetic=True, atr=atr)

    def hit_target(d):
        d.iloc[35, d.columns.get_loc("high")] = 111.0
    r = go(hit_target)
    c = T["cost_per_side"]
    assert r["exit_reason"] == "target" and abs(r["R"] - (110 - 100 - c * 210) / 5) < 1e-12 and r["O2"] == 1

    def both(d):
        d.iloc[35, d.columns.get_loc("high")] = 111.0
        d.iloc[35, d.columns.get_loc("low")] = 94.0
    assert go(both)["exit_reason"] == "stop"

    def gap(d):
        d.iloc[40, d.columns.get_loc("open")] = 90.0
        d.iloc[40, d.columns.get_loc("low")] = 89.0
    g = go(gap)
    assert g["exit_reason"] == "gap below stop" and g["R"] < -1.25 and g["O3"] == 1
    cap = go(lambda d: None)
    assert cap["exit_reason"] == "time cap" and cap["O2"] == 0
    assert go(lambda d: None, stop=100.5)["skip"] == "entry open <= stop"
    assert go(lambda d: None, stop=99.5)["skip"] == "risk < 0.5 ATR"
    for kw in ({}, {"synthetic": True}):                       # real data, or the flag without synthetic data
        try:
            outcomes.trade(base, we, 95.0, T, "2030-01-01", **kw)
            raise AssertionError("real-data outcome allowed in Phase 0")
        except RuntimeError:
            pass
    print("outcomes ok: target, same-day stop first, gap tail, time cap, skips; real-data outcomes refused")


def t_metric():
    wk = np.array(["2010-01-01"] * 4 + ["2010-01-08"] * 3 + ["2010-01-15"] * 2)
    tier = np.array([2, 0, 0, 1, 2, 2, 0, 2, 1])
    y = np.array([2.0, -1, 2, 5, -1, 2, -1, 9, 9])
    d, h, _ = metric.week_terms(wk, tier, y)
    # week 1: A mean 2, C mean 0.5, h = 1*2/3; week 2: A mean 0.5, C -1, h = 2*1/3; week 3 has no C
    assert np.allclose(d, [1.5, 1.5]) and np.allclose(h, [2 / 3, 2 / 3])
    assert abs(metric.spread(d, h) - 1.5) < 1e-12
    assert metric.holm({"W": 0.01, "L": 0.04}, 0.05) == {"W": True, "L": True}
    assert metric.holm({"W": 0.03, "L": 0.04}, 0.05) == {"W": False, "L": False}
    assert metric.holm({"W": 0.02, "L": 0.2}, 0.05) == {"W": True, "L": False}
    print("metric ok: within-week spread, weights, Holm")


def t_power():
    rng = np.random.default_rng(3)
    weeks = pd.date_range("2008-01-04", "2026-03-27", freq="W-FRI")
    w = np.repeat(weeks.to_numpy(), rng.poisson(5, len(weeks)))
    halves = guard.PREREG["metric"]["halves"]
    hi = power.simulate(w, 0.45, 60, 300, 1, 0.4, 0.15, halves, 0.15, 0.075)
    nul = power.simulate(w, 0.0, 100, 300, 2, 0.4, 0.15, halves, 0.15, 0.075)
    assert hi["power"] >= 0.9, hi
    assert nul["power"] <= 0.12 and nul["gate_pass"] <= 0.05, nul
    print(f"power ok: planted 0.45R power {hi['power']:.2f}; null false-positive {nul['power']:.2f}, gate {nul['gate_pass']:.2f}")


def t_sets(u):
    a = sets.assign(u, guard.CFG, guard.PREREG)
    b = sets.assign(u.sample(frac=1, random_state=1), guard.CFG, guard.PREREG)
    assert a.set_index("symbol")["set"].to_dict() == b.set_index("symbol")["set"].to_dict()
    assert set(a.loc[a["symbol"].isin(["AAPL", "JPM"]), "set"]) == {"X"}
    dual = pd.DataFrame({"symbol": ["GOOG", "GOOGL", "FOX", "FOXA", "ZZZ"], "sector": ["Communication Services"] * 5,
                         "name": ["Alphabet Inc. (Class C)", "Alphabet Inc. (Class A)", "Fox Corporation (Class B)",
                                  "Fox Corporation (Class A)", "Zeta Co"]})
    dm = sets.assign(dual, guard.CFG, guard.PREREG).set_index("symbol")["set"].to_dict()
    assert dm["GOOG"] == "X" and dm["GOOGL"] == "X" and dm["FOXA"] == "XD" and dm["FOX"] in ("S1", "S2", "S3", "E"), dm
    big = pd.DataFrame({"symbol": [f"Z{k:04d}" for k in range(2000)], "sector": ["Tech"] * 1000 + ["Fin"] * 1000})
    sh = sets.assign(big, guard.CFG, guard.PREREG)["set"].value_counts(normalize=True).to_dict()
    assert abs(sh["S1"] - 0.40) < 0.01 and abs(sh["S2"] - 0.40) < 0.01 and abs(sh["S3"] - 0.15) < 0.01 \
        and abs(sh["E"] - 0.05) < 0.01, sh
    print(f"sets ok: deterministic, excluded -> X, share classes -> XD, shares S1 {sh['S1']:.2f} S2 {sh['S2']:.2f} S3 {sh['S3']:.2f} E {sh['E']:.2f}")


def t_parity_compare():
    A = {"armed": {"X": {"armed_week": "2026-10-09", "low": 10.0, "released": True},
                   "Y": {"armed_week": "2026-10-16", "low": 20.0, "released": False}}}
    B = {"armed": {"X": {"armed_week": "2026-10-09", "low": 10.02, "released": True},
                   "Y": {"armed_week": "2026-10-16", "low": 20.0, "released": False},
                   "Z": {"armed_week": "2026-10-16", "low": 5.0, "released": False}}}
    r = parity.compare(A, B, pd.DataFrame({"symbol": ["X"]}), pd.DataFrame({"symbol": ["X"]}))
    assert r["shared"] == 2 and abs(r["jaccard"] - 2 / 3) < 1e-3 and r["low_agree"] == 1.0 and not r["pass"]
    assert parity.compare(A, A, pd.DataFrame(), pd.DataFrame())["pass"]
    print("parity compare ok")


def t_isolation():
    for f in sorted((REPO / "r007").glob("*.py")):
        tree = ast.parse(f.read_text())
        for node in ast.walk(tree):
            mods = []
            if isinstance(node, ast.Import):
                mods = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                mods = [node.module]
            for m in mods:
                assert m.split(".")[0] not in guard.PRIOR_PACKAGES, (f.name, m)
    old = os.environ["R007_OUT"]
    os.environ["R007_OUT"] = str(REPO / "weekscan")
    try:
        guard.out_dir()
        raise AssertionError("output inside the repository was allowed")
    except RuntimeError:
        pass
    finally:
        os.environ["R007_OUT"] = old
    assert not guard.outcomes_open() and guard.OPEN_PHASES == ()
    print("isolation ok: no prior-system imports, output outside the repo, outcomes closed")


def t_end_to_end(u, daily):
    from r007 import phase0
    when = "2026-10-20T16:05:00+00:00"
    live = parity.run_live_code(daily, u, when, guard.CFG["live_ref"]["week"])
    ref = {"sha": "synthetic000000", "when": when, "state": live["state"], "universe": u, "alerts": live["alerts"]}
    PW = guard.PREREG["phase0"]["power"]
    keep = dict(PW)
    PW.update({"reps": 20, "boot": 200})
    LA = guard.CFG["lookahead"]
    keep_la = dict(LA)
    LA.update({"symbols": 4, "cuts_per_symbol": 2})
    try:
        res = phase0.run(log=lambda *a: None, daily_override=daily, ref_override=ref)
    finally:
        PW.clear(); PW.update(keep)
        LA.clear(); LA.update(keep_la)
    assert res["status"]["lock"] and res["status"]["lookahead"] and res["status"]["parity"], res["status"]
    assert sum(res["events"].values()) > 0
    ev = pd.concat([pd.read_csv(Path(_TMP) / "events" / f"{s}.csv.gz") for s in ["S1", "S2", "S3", "E"]])
    assert not ev["symbol"].isin(["AAPL", "JPM"]).any()
    assert not any(c in ev.columns for c in ["R", "O1", "O2", "O3", "exit", "entry"])
    assert ev["week"].min() >= "2008-01-04" and ev["week"].max() <= "2026-03-27"
    md = (Path(_TMP) / "PHASE0.md").read_text()
    assert "No outcome was computed" in md
    print(f"phase0 ok: {len(ev)} synthetic events, parity Jaccard {res['parity']['jaccard']}, no outcome columns")


def t_splits_and_snapshot(daily):
    from r007 import data
    idx = pd.bdate_range("2015-01-01", periods=10)
    sp = pd.Series(0.0, index=idx)
    sp.iloc[4] = 10.0                                            # 10:1 split on day 5
    f = data.split_factor(sp)
    assert list(f) == [10.0] * 4 + [1.0] * 6, list(f)
    # price floor: split-adjusted $3 before a later 10:1 split traded at $30 -> eligible; $3 after it -> not
    d = synth_daily(42, start="2014-01-01", end="2016-12-30")
    d[["open", "high", "low", "close"]] = 3.0
    d["volume"] = 1e8
    d["split_factor"] = np.where(d.index < pd.Timestamp("2016-01-01"), 10.0, 1.0)
    w = events.weekly(d, "2016-12-30")
    el = events.eligibility(d, w, 5.0, 20e6)
    assert el[w.index < pd.Timestamp("2015-12-25")].iloc[5:].all() and not el[w.index > pd.Timestamp("2016-01-08")].any()
    # snapshot: written once with a manifest, reused and verified; a missing required ticker writes nothing
    sub = {k: daily[k] for k in ["S000", "S001", "SPY"]}
    old = os.environ["R007_OUT"]
    os.environ["R007_OUT"] = tempfile.mkdtemp(prefix="r007snap_")
    try:
        try:
            data.snapshot(["S000", "SPY", "XLK"], log=lambda *a: None, required=["SPY", "XLK"],
                          fetch=lambda t, a, b, c: ({k: sub[k] for k in t if k in sub}, [k for k in t if k not in sub]))
            raise AssertionError("snapshot written without a required ticker")
        except RuntimeError:
            pass
        assert not (guard.out_dir() / "data" / "MANIFEST.json").exists()
        got, man = data.snapshot(["S000", "S001", "SPY"], log=lambda *a: None, required=["SPY"],
                                 fetch=lambda t, a, b, c: ({k: sub[k] for k in t}, []))
        again, man2 = data.snapshot(["S000", "S001", "SPY"], log=lambda *a: None,
                                    fetch=lambda *a: (_ for _ in ()).throw(AssertionError("re-downloaded")))
        assert man2["reused"] and man2["id"] == man["id"] and np.allclose(again["S000"]["close"], got["S000"]["close"])
        f0 = guard.out_dir() / "data" / "daily" / "S000.csv.gz"
        f0.write_bytes(f0.read_bytes()[:-5])
        try:
            data.snapshot(["S000"], log=lambda *a: None)
            raise AssertionError("tampered snapshot accepted")
        except RuntimeError:
            pass
    finally:
        os.environ["R007_OUT"] = old
    from datetime import datetime, timezone
    assert guard.overlaps_guard(datetime(2026, 10, 24, 13, 0, tzinfo=timezone.utc), 150)      # Saturday: reaches 15:00
    assert guard.overlaps_guard(datetime(2026, 10, 22, 14, 0, tzinfo=timezone.utc), 150) is None  # Thursday 14:00
    print("splits and snapshot ok: point-in-time price floor, write once, reuse verified, tamper and missing refused; "
          "guard horizon ok")


if __name__ == "__main__":
    u, daily = synth_market()
    t_lock()
    t_records_parity(daily)
    t_replay_vs_step(daily)
    t_replay_rules()
    t_lookahead(daily)
    t_outcomes()
    t_splits_and_snapshot(daily)
    t_metric()
    t_power()
    t_sets(u)
    t_parity_compare()
    t_isolation()
    t_end_to_end(u, daily)
    print("all r007 tests passed")
