"""R007 Phase 1: the information gate on S1+S2 (prereg amendment_1.phase1). Runs once.

Outcomes are computed only for S1 and S2 events and their same-week nulls (drawn from S1+S2 stocks).
S3 and E are never scored here. Outputs under OUT:
  PHASE1.md, PHASE1.json, outcomes/S1S2_events.csv.gz, LEDGER.md (appended)
"""
from __future__ import annotations

import io
import json
import os
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from weekscan import scan
from weekscan.run import CFG as WCFG

from . import events, guard, metric, model, outcomes, phase0

JUDGE_SETS = ("S1", "S2")


def _fmt(v, nd=3):
    if v is None or (isinstance(v, float) and v != v):
        return "–"
    if isinstance(v, (bool, np.bool_)):
        return "yes" if v else "no"
    if isinstance(v, (float, np.floating)):
        return f"{v:.{nd}f}"
    return str(v)


def _table(rows: list[dict]) -> str:
    if not rows:
        return "(none)"
    cols = list(rows[0].keys())
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    out += ["| " + " | ".join(_fmt(r[c]) for c in cols) + " |" for r in rows]
    return "\n".join(out)


def check_events(ev: pd.DataFrame, man: dict, log) -> dict:
    """The rebuilt S1/S2 events must equal Phase 0's committed files in every column, from the same snapshot."""
    out = {}
    p0j = guard.out_dir() / "PHASE0.json"
    if p0j.exists():
        sid = json.loads(p0j.read_text())["snapshot"]["id"]
        out["snapshot"] = "same as Phase 0" if sid == man["id"] or man["id"] == "override" else f"DIFFERENT ({sid[:16]})"
    else:
        out["snapshot"] = "PHASE0.json missing"
    for s in JUDGE_SETS:
        f = guard.out_dir() / "events" / f"{s}.csv.gz"
        if not f.exists():
            out[s] = "phase0 file missing"
            continue
        p0 = pd.read_csv(f).reset_index(drop=True)
        mine = ev[ev["set"] == s].reset_index(drop=True)
        mine = pd.read_csv(io.StringIO(mine.to_csv(index=False, float_format="%.6g")))   # same rounding as the file
        bad = [] if len(p0) == len(mine) and list(p0.columns) == list(mine.columns) else ["shape/columns"]
        for c in ([] if bad else p0.columns):
            a, b = p0[c], mine[c]
            if pd.api.types.is_numeric_dtype(a) and pd.api.types.is_numeric_dtype(b):
                ok = np.allclose(a.to_numpy(float), b.to_numpy(float), rtol=1e-5, atol=1e-9, equal_nan=True)
            else:
                ok = (a.astype(str).to_numpy() == b.astype(str).to_numpy()).all()
            if not ok:
                bad.append(c)
        out[s] = "identical" if not bad else f"DIFFERENT: {bad[:8]}"
    if any(v not in ("identical", "same as Phase 0") for v in out.values()):
        raise RuntimeError(f"rebuilt events or snapshot differ from Phase 0 (no outcome computed): {out}")
    log(f"  events identical to Phase 0: {out}")
    return out


def _clean(o):
    """JSON-safe: numpy scalars to Python, NaN/inf to None."""
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


MARKER = "PHASE1.started"


def mark(log=print) -> dict:
    """Written and pushed by its own workflow step before Phase 1 computes anything: the one-time opening of S1+S2."""
    if (guard.out_dir() / MARKER).exists() or (guard.out_dir() / "PHASE1.json").exists():
        raise RuntimeError("Phase 1 was already started or run: it runs once (a crashed run is a deviation to decide)")
    lk = guard.verify_lock()
    if not lk["ok"]:
        raise RuntimeError(f"pre-registration lock broken: {lk}")
    m = {"lock": lk["id"], "utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
         "run_id": os.environ.get("GITHUB_RUN_ID", "local")}
    guard.out(MARKER).write_text(json.dumps(m))
    log(f"Phase 1 marker written: {m}")
    return m


def null_pool(daily: dict, u: pd.DataFrame, end: str, prereg: dict, weeks: set) -> dict:
    """week -> list of (symbol, stop) for S1+S2 stocks eligible that week with a group (events removed later)."""
    E = prereg["events"]
    uc = WCFG["universe"]
    etfs = sorted(set(WCFG["sector_etfs"].values()) | set(WCFG["industry_etfs"].values()))
    spy_w = events.weekly(daily[WCFG["benchmark"]], end)
    gser = scan.group_states({e: events.weekly(daily[e], end) for e in etfs if e in daily}, spy_w)
    group_of = events.group_map(u, gser)
    pool: dict = {w: [] for w in weeks}
    for s in sorted(u.loc[u["set"].isin(JUDGE_SETS), "symbol"]):
        if s not in daily or s not in group_of:
            continue
        w = events.weekly(daily[s], end)
        x = scan.read_weekly(w)
        if x is None:
            continue
        r = events.records(x, E["window_weeks"], E["pair_signals"])
        el = events.eligibility(daily[s], w, uc["min_price"], uc["min_dollar_volume"]).reindex(r.index).fillna(False)
        for wk in r.index[el.to_numpy(dtype=bool)]:
            if wk in pool:
                pool[wk].append((s, float(r.at[wk, "low"])))
    return pool


def run(live_ref: str = "origin/weekscan-results", log=print, daily_override: dict | None = None,
        ref_override: dict | None = None) -> dict:
    t0 = datetime.now(timezone.utc)
    if not guard.outcomes_open():
        raise RuntimeError("Phase 1 needs R007_PHASE=1 (outcomes open for S1+S2 only)")
    if (guard.out_dir() / "PHASE1.json").exists():
        raise RuntimeError("Phase 1 has already run (PHASE1.json exists): it runs once")
    mk = guard.out_dir() / MARKER
    if not mk.exists():
        raise RuntimeError("Phase 1 marker missing: the marker step must run (and be pushed) first")
    mrk = json.loads(mk.read_text())
    if mrk.get("run_id") != os.environ.get("GITHUB_RUN_ID", "local"):
        raise RuntimeError(f"Phase 1 marker belongs to another run ({mrk}): it runs once")
    lk, u, ref, daily, man = phase0.prepare(live_ref, log, daily_override, ref_override, require_closed=False,
                                            require_reuse=daily_override is None)
    if mrk.get("lock") != lk["id"]:
        raise RuntimeError("lock changed since the marker")
    C, P = guard.CFG, guard.PREREG
    A = P["amendment_1"]
    assert tuple(A["phase1"]["set"]) == JUDGE_SETS
    end = C["data"]["end"]
    ev_all, info = events.build(daily, u, P, end, log)
    integ = check_events(ev_all, man, log)
    ev = ev_all[ev_all["set"].isin(JUDGE_SETS)].reset_index(drop=True)
    set_of = u.set_index("symbol")["set"].to_dict()
    assert set(ev["set"]) <= set(JUDGE_SETS)
    log(f"[4/8] judge events: {len(ev)} ({', '.join(f'{s} {int((ev.set == s).sum())}' for s in JUDGE_SETS)})")

    # null pool first (outcome-free): every event needs same-week candidates, else stop before any outcome
    weeks = set(pd.to_datetime(ev["week"]))
    pool = null_pool(daily, u, end, P, weeks)
    ev_by_week = ev.groupby("week")["symbol"].apply(set).to_dict()
    cands = {}
    for wk_s, syms in ev_by_week.items():
        cands[wk_s] = sorted(c for c in pool.get(pd.Timestamp(wk_s), []) if c[0] not in syms)
    cover = float(np.mean([len(cands[w]) > 0 for w in ev["week"]]))
    log(f"  null candidates: median {int(np.median([len(v) for v in cands.values()]))} per week; "
        f"events covered {cover:.1%}")
    if cover < 0.90:
        raise RuntimeError(f"null pool covers only {cover:.1%} of events (< 90%): stop before any outcome")

    # outcomes: events, then 5 same-week nulls per event from S1+S2 stocks without an event that week
    T, cut = P["trade"], P["trade"]["outcome_cutoff"]
    atr_cache: dict = {}

    def trade(sym, week, stop):
        if set_of.get(sym) not in JUDGE_SETS:
            raise RuntimeError(f"{sym} is not in S1/S2: refused")
        if sym not in atr_cache:
            atr_cache[sym] = outcomes.wilder_atr(daily[sym][daily[sym].index <= pd.Timestamp(cut)])
        return outcomes.trade(daily[sym], week, stop, T, cut, atr=atr_cache[sym])

    res = [trade(r.symbol, r.week, float(r.low)) for r in ev.itertuples()]
    ev["skip"] = [r.get("skip") for r in res]
    for k in ["R", "O2", "O3", "exit_reason", "entry_date", "exit_date"]:
        ev[k] = [r.get(k, np.nan) if r.get("skip") is None else np.nan for r in res]
    log(f"[5/8] event outcomes: {int(ev['skip'].isna().sum())} traded, {int(ev['skip'].notna().sum())} skipped")
    rng = np.random.default_rng(P["null_trades"]["seed"])
    ncache: dict = {}
    null_R = []
    for r in ev.itertuples():
        cand = cands[r.week]
        if not cand:
            null_R.append(np.nan)
            continue
        pick = rng.choice(len(cand), size=min(P["null_trades"]["per_event"], len(cand)), replace=False)
        vals = []
        for i in sorted(pick):
            s, stop = cand[i]
            key = (s, r.week)
            if key not in ncache:
                ncache[key] = trade(s, r.week, stop)
            if ncache[key].get("skip") is None:
                vals.append(ncache[key]["R"])
        null_R.append(float(np.mean(vals)) if vals else np.nan)
    ev["null_R"] = null_R
    log(f"[6/8] nulls: {len(ncache)} null trades")

    # models and tiers (traded events only)
    tr = ev[ev["skip"].isna()].reset_index(drop=True)
    halves = P["metric"]["halves"]
    seed, draws = 20261022, 2000
    w_cuts = metric.tercile_cuts(ev["w_score"].to_numpy())          # all S1+S2 events, outcome-free
    ev["tier_W"] = metric.tiers(ev["w_score"].to_numpy(), w_cuts)
    tr["tier_W"] = metric.tiers(tr["w_score"].to_numpy(), w_cuts)
    sk = ev[ev["skip"].notna()].reset_index(drop=True)
    L = model.oof(tr, tr["O2"].to_numpy(float), extra=sk)
    tr["p_L"], tr["tier_L"] = L["p"], L["tier"]
    sk_tier_L = L["extra_tier"]
    results = {}
    for m in ["W", "L"]:
        results[m] = metric.evaluate(tr["week"].to_numpy(), tr[f"tier_{m}"].to_numpy(), tr["R"].to_numpy(float),
                                     halves, draws, seed)
    holm = metric.holm({m: results[m]["p"] for m in results}, 0.05)
    G = {}
    for m, r_ in results.items():
        g = metric.gate(r_, 0.10, 0.05)
        G[m] = {"holm_p_ok": holm[m], **g, "pass": bool(holm[m] and g["spread_ok"] and g["halves_ok"])}
    passed = [m for m in G if G[m]["pass"]]
    log(f"[7/8] gate: " + ", ".join(f"{m} spread {results[m]['spread']:.3f}R p {results[m]['p']:.4f} "
                                    f"{'PASS' if G[m]['pass'] else 'fail'}" for m in results))

    def tier_rows(m):
        rows = []
        for t, name in [(2, "A"), (1, "B"), (0, "C")]:
            e = tr[tr[f"tier_{m}"] == t]
            n_sk = int((ev.loc[ev["skip"].notna(), "tier_W"] == t).sum()) if m == "W" else int((sk_tier_L == t).sum())
            rows.append({"tier": name, "traded": len(e), "skipped": n_sk,
                         "mean_R": float(e["R"].mean()), "hit_2R_first": float(e["O2"].mean()),
                         "tail_le_-1.25R": float(e["O3"].mean()), "mean_null_R": float(e["null_R"].mean()),
                         "R_minus_null": float((e["R"] - e["null_R"]).mean())})
        return rows

    tiers = {m: tier_rows(m) for m in results}
    (guard.out_dir() / "outcomes").mkdir(exist_ok=True)
    cols = ["symbol", "set", "week", "group", "w_score", "tier_W", "skip", "entry_date", "exit_date", "exit_reason",
            "R", "O2", "O3", "null_R"]
    out_ev = ev[cols].merge(tr[["symbol", "week", "p_L", "tier_L"]], on=["symbol", "week"], how="left")
    out_ev.to_csv(guard.out("outcomes", "S1S2_events.csv.gz"), index=False, float_format="%.6g")
    decision = (f"Phase 1 PASSED for {', '.join(passed)}: next is the Phase 3 book on S1+S2 (out-of-fold tiers) and the "
                f"one-time S3 sanity check (each needs its own deploy and go)." if passed else
                "Phase 1 FAILED for both models: per the pre-registration, size flat; the weekly-scan score orders alerts "
                "for reading only; S3 and E stay unused; R007 closes; no R008.")
    J = {"run_utc": t0.strftime("%Y-%m-%d %H:%M"), "lock": lk["id"], "snapshot": man["id"], "integrity": integ,
         "events": {"judge": len(ev), "traded": len(tr), "skipped": int(ev["skip"].notna().sum()),
                    "skip_reasons": ev["skip"].value_counts().to_dict()},
         "null": {"trades": len(ncache), "events_without_null": int(ev["null_R"].isna().sum()), "pool_coverage": cover},
         "w_cuts": w_cuts, "results": results, "gate": G, "passed": passed, "tiers": tiers,
         "L": {"chosen_C": {str(k): v["C"] for k, v in L["chosen"].items()}, "logloss_model": L["logloss_model"],
               "logloss_base": L["logloss_base"], "loo": L["loo"]},
         "base": {"mean_R": float(tr["R"].mean()), "hit_2R_first": float(tr["O2"].mean()),
                  "mean_null_R": float(tr["null_R"].mean())},
         "decision": decision}
    J = _clean(J)
    guard.out("PHASE1.json").write_text(json.dumps(J, indent=1))
    _report(J, L["calibration"])
    with guard.out("LEDGER.md").open("a") as f:
        f.write(f"- {J['run_utc']} UTC · Phase 1 · OPENED S1+S2 outcomes ({len(tr)} traded events, {len(ncache)} null "
                f"trades); gate: {', '.join(f'{m} ' + ('pass' if G[m]['pass'] else 'fail') for m in G)}. "
                f"Lock {lk['id'][:16]}. S3 and E untouched.\n")
    log(f"[8/8] written: PHASE1.md, PHASE1.json, outcomes/S1S2_events.csv.gz · passed={passed}")
    return J


def _report(J: dict, cal: pd.DataFrame) -> None:
    L = ["# R007 Phase 1: information gate on S1+S2\n"]
    L.append(f"_Run {J['run_utc']} UTC · lock `{J['lock'][:16]}` · snapshot `{J['snapshot'][:16]}` · "
             f"events identical to Phase 0: {J['integrity']}_\n")
    L.append(f"**{J['decision']}**\n")
    e = J["events"]
    L.append(f"Judge events {e['judge']}: traded {e['traded']}, skipped {e['skipped']} ({e['skip_reasons']}). "
             f"Null trades {J['null']['trades']}; events without a null {J['null']['events_without_null']}.\n")
    b = J["base"]
    L.append(f"All traded events: mean R {b['mean_R']:.3f}, +2R-first rate {b['hit_2R_first']:.1%}; "
             f"same-week null mean R {b['mean_null_R']:.3f}.\n")
    L.append("## 1. Gate (each model: Holm one-sided p < 0.05 across W and L, spread >= 0.10R, each half >= 0.05R)\n")
    rows = []
    for m, r in J["results"].items():
        g = J["gate"][m]
        rows.append({"model": m, "A-C spread (R)": r["spread"], "90% CI low": r["lo90"], "90% CI high": r["hi90"],
                     "p (one-sided)": r["p"], "weeks": r["weeks"], "2008-16": r["halves"][0], "2017-26": r["halves"][1],
                     "Holm p ok": g["holm_p_ok"], "spread ok": g["spread_ok"], "halves ok": g["halves_ok"],
                     "PASS": g["pass"]})
    L.append(_table(rows) + "\n")
    L.append(f"Model W tier cut points (terciles of all S1+S2 W scores): {J['w_cuts'][0]:.3f} / {J['w_cuts'][1]:.3f}\n")
    for m in ["W", "L"]:
        L.append(f"## 2{'a' if m == 'W' else 'b'}. Tiers, model {m}\n")
        L.append(_table(J["tiers"][m]) + "\n")
    Lm = J["L"]
    L.append("## 3. Model L details (descriptive)\n")
    L.append(f"- Chosen C per block (2008-11, 2012-15, 2016-18, 2019-21, 2022-26): {Lm['chosen_C']}")
    L.append(f"- Out-of-fold log-loss {Lm['logloss_model']:.4f} vs constant training base rate {Lm['logloss_base']:.4f} "
             f"(gain {Lm['logloss_base'] - Lm['logloss_model']:+.4f}; positive = the tags carry information).")
    L.append("- Leave-one-out (out-of-fold log-loss increase when the input is dropped; positive = the input helps):\n")
    L.append(_table([{"input": k, "logloss change": v} for k, v in sorted(Lm["loo"].items(), key=lambda kv: -kv[1])]) + "\n")
    L.append("Calibration by decile of the out-of-fold probability:\n")
    L.append(_table(cal.to_dict("records")) + "\n")
    L.append("Reading notes: the gate compares tiers within the same week, so market timing cancels. `R_minus_null` "
             "is each event's R minus the mean R of 5 random same-week, same-rule trades on S1+S2 stocks without an "
             "event (reported, not judged). Survivorship (today's constituents) flatters levels; the halves rule "
             "guards the ranking. Model L's time blocks have no gap, so 26-week outcomes of late-December training "
             "events overlap the next block's first weeks; the within-week comparison largely cancels this.\n")
    guard.out("PHASE1.md").write_text("\n".join(L))
