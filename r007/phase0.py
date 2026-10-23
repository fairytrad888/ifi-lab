"""R007 Phase 0: snapshot, symbol sets, events and features, look-ahead, live parity, synthetic power.

No outcome is computed (guard.outcomes_open() must be False). Outputs under OUT:
  PHASE0.md, PHASE0.json, events/<set>.csv.gz (features only), universe_sets.csv, parity/, LEDGER.md, data/
"""
from __future__ import annotations

import json
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from weekscan.run import CFG as WCFG

from . import data, events, guard, lookahead, metric, parity, power, sets

SETS = ["S1", "S2", "S3", "E"]


def _fmt(v, nd=2):
    if v is None or (isinstance(v, float) and v != v):
        return "–"
    if isinstance(v, float):
        return f"{v:.{nd}f}"
    return str(v)


def _md_table(df: pd.DataFrame) -> str:
    cols = [str(c) for c in df.columns]
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(_fmt(v) for v in r.tolist()) + " |")
    return "\n".join(out)


def describe(ev: pd.DataFrame) -> dict:
    d = {}
    ev = ev.copy()
    ev["year"] = ev["week"].str[:4].astype(int)
    d["by_year"] = ev.pivot_table(index="year", columns="set", values="symbol", aggfunc="count", fill_value=0)
    d["by_year"] = d["by_year"].reindex(columns=[s for s in SETS if s in d["by_year"].columns])
    rows = []
    for s in SETS:
        e = ev[ev["set"] == s]
        if e.empty:
            continue
        rows.append({"set": s, "events": len(e), "symbols": e["symbol"].nunique(), "weeks": e["week"].nunique(),
                     "per_week_median": float(e.groupby("week").size().median()),
                     "max_in_a_week": int(e.groupby("week").size().max()),
                     "share_top_10_weeks": float(e.groupby("week").size().nlargest(10).sum() / len(e))})
    d["sets"] = pd.DataFrame(rows)
    s1 = ev[ev["set"].isin(["S1", "S2"])]
    cat = []
    for c in ["group_state", "n_types", "stage", "red_age", "trig2", "leader"]:
        vc = s1[c].astype(str).value_counts(normalize=True).sort_index()
        cat.append({"feature": c, "shares (S1+S2)": ", ".join(f"{k} {v:.0%}" for k, v in vc.items())})
    for c in [k for k in s1.columns if k.startswith("f_")]:
        cat.append({"feature": c, "shares (S1+S2)": f"present {s1[c].mean():.0%}"})
    d["categorical"] = pd.DataFrame(cat)
    num = []
    for c in ["flow_min", "stop_pct", "dist_anchor_atr", "breadth_acc", "breadth_stage2", "w_score"]:
        x = pd.to_numeric(s1[c], errors="coerce")
        q = x.quantile([0.01, 0.25, 0.5, 0.75, 0.99])
        num.append({"feature": c, "missing": float(x.isna().mean()), "p1": q[0.01], "p25": q[0.25],
                    "median": q[0.5], "p75": q[0.75], "p99": q[0.99]})
    d["numeric"] = pd.DataFrame(num)
    numc = ["n_types", "trig2", "red_age", "flow_min", "stage", "breadth_acc", "breadth_stage2", "leader",
            "stop_pct", "dist_anchor_atr"] + [k for k in s1.columns if k.startswith("f_")]
    cm = s1[numc].apply(pd.to_numeric, errors="coerce").corr()
    pairs = [{"a": a, "b": b, "r": cm.loc[a, b]} for i, a in enumerate(numc) for b in numc[i + 1:]
             if abs(cm.loc[a, b]) >= 0.4]
    d["corr"] = pd.DataFrame(sorted(pairs, key=lambda p: -abs(p["r"])))
    return d


def w_tiers(ev: pd.DataFrame) -> dict:
    s1 = ev[ev["set"] == "S1"]
    cuts = metric.tercile_cuts(s1["w_score"].to_numpy())
    out = {"cuts": cuts, "sets": {}}
    for s in ["S1", "S2"]:
        e = ev[ev["set"] == s]
        t = metric.tiers(e["w_score"].to_numpy(), cuts)
        d, h, wl = metric.week_terms(e["week"].to_numpy(), t, np.zeros(len(e)))
        out["sets"][s] = {"A": int((t == 2).sum()), "B": int((t == 1).sum()), "C": int((t == 0).sum()),
                          "weeks_with_A_and_C": int(len(d)), "sum_week_weight": float(h.sum())}
    return out


def prepare(live_ref: str = "origin/weekscan-results", log=print, daily_override: dict | None = None,
            ref_override: dict | None = None, require_closed: bool = True,
            require_reuse: bool = False) -> tuple[dict, pd.DataFrame, dict, dict, dict]:
    """Lock, live reference, symbol sets and the snapshot (downloaded once). Returns (lock, u, ref, daily, manifest)."""
    if require_closed and guard.outcomes_open():
        raise RuntimeError("Phase 0 must run with outcomes closed")
    lk = guard.verify_lock()
    if not lk["ok"]:
        raise RuntimeError(f"pre-registration lock broken: {lk}")
    log(f"[1/8] lock ok ({lk['id'][:16]})")
    C, P = guard.CFG, guard.PREREG
    L = C["live_ref"]
    ref = ref_override or parity.find_ref(live_ref, L["week"], L["state_version"])
    log(f"[2/8] live reference: {ref['sha'][:12]} ({ref['when']}), universe {len(ref['universe'])}")
    u = sets.assign(ref["universe"], C, P)
    u.to_csv(guard.out("universe_sets.csv"), index=False)
    etfs = sorted(set(WCFG["sector_etfs"].values()) | set(WCFG["industry_etfs"].values()))
    required = etfs + [WCFG["benchmark"]]
    tickers = sorted(set(u["symbol"]) | set(required))
    if daily_override is not None:
        daily, man = daily_override, {"id": "override", "missing": [], "reused": None}
    else:
        if require_reuse and not (guard.out_dir() / "data" / "MANIFEST.json").exists():
            raise RuntimeError("no committed snapshot: later phases never download prices")
        daily, man = data.snapshot(tickers, log, required=required)
    log(f"[3/8] snapshot: {len(daily)} tickers ({'reused' if man.get('reused') else 'new'}), missing {len(man['missing'])}")
    return lk, u, ref, daily, man


def run(live_ref: str = "origin/weekscan-results", log=print, daily_override: dict | None = None,
        ref_override: dict | None = None) -> dict:
    t0 = datetime.now(timezone.utc)
    lk, u, ref, daily, man = prepare(live_ref, log, daily_override, ref_override)
    C, P = guard.CFG, guard.PREREG
    L = C["live_ref"]
    end = C["data"]["end"]
    ev, info = events.build(daily, u, P, end, log)
    if ev.empty:
        raise RuntimeError(f"no events were built (build info {info}): stop")
    (guard.out_dir() / "events").mkdir(exist_ok=True)
    for s in SETS:
        ev[ev["set"] == s].to_csv(guard.out("events", f"{s}.csv.gz"), index=False, float_format="%.6g")
    log(f"[4/8] events: {len(ev)} ({', '.join(f'{s} {int((ev.set == s).sum())}' for s in SETS)})")
    desc = describe(ev)
    wt = w_tiers(ev)
    look = lookahead.check(daily, sorted(u.loc[u["set"].isin(SETS), "symbol"]), P, end,
                           C["lookahead"]["symbols"], C["lookahead"]["cuts_per_symbol"], C["lookahead"]["seed"])
    log(f"[5/8] look-ahead: {'ok' if look['ok'] else 'FAIL'} ({look['symbols_tested']} symbols x {look['cuts']} cuts); "
        f"real-data fidelity to weekscan: {'ok' if look['fidelity_ok'] else 'FAIL'}")
    try:
        mine = parity.run_live_code(daily, ref["universe"], ref["when"], L["week"])
        par = parity.compare(ref["state"], mine["state"], ref["alerts"], mine["alerts"])
        par["mismatch_reasons"] = parity.explain(par, daily, ref["when"])
    except Exception as e:                                            # reported, not hidden
        par = {"pass": False, "error": f"{type(e).__name__}: {e}"}
    log(f"[6/8] live parity: {'ok' if par.get('pass') else 'FAIL'} "
        f"(Jaccard {par.get('jaccard')}, live {par.get('live_armed')}, r007 {par.get('r007_armed')})")
    PW = P["phase0"]["power"]
    halves = P["metric"]["halves"]
    pw = {}
    for s in ["S1", "S2"]:
        e = ev[ev["set"] == s]
        wks = e["week"].to_numpy()
        pw[s] = power.table(wks, PW, halves, 0.15, 0.075) if len(wks) else []
        if len(wks):                                   # reported: model W's own tiers (outcome-free) cluster by week
            tw = metric.tiers(e["w_score"].to_numpy(), tuple(wt["cuts"]))
            pw[f"{s} (W tiers)"] = power.table(wks, PW, halves, 0.15, 0.075, fixed_tiers=tw)
    s1_target = next((r for r in pw.get("S1", []) if abs(r["spread_R"] - PW["target_spread_R"]) < 1e-9), None)
    power_ok = bool(s1_target and s1_target["power"] >= PW["criterion"])
    log(f"[7/8] power at {PW['target_spread_R']}R on S1: {s1_target['power'] if s1_target else None} "
        f"({'ok' if power_ok else 'BELOW CRITERION'})")
    status = {"lock": lk["ok"], "lookahead": look["ok"], "fidelity": look["fidelity_ok"], "parity": bool(par.get("pass")),
              "power": power_ok}
    res = {"run_utc": t0.strftime("%Y-%m-%d %H:%M"), "lock": lk["id"], "live_ref": {"sha": ref["sha"], "when": ref["when"]},
           "snapshot": {"id": man["id"], "tickers": len(daily), "missing": man["missing"], "reused": man.get("reused"),
                        "tickers_with_splits": man.get("tickers_with_splits")},
           "universe": {"total": int(len(u)), **u["set"].value_counts().to_dict()}, "build": info,
           "events": {s: int((ev.set == s).sum()) for s in SETS}, "w_tiers": wt, "lookahead": look, "parity": par,
           "power": pw, "status": status, "phase0_pass": all(status.values())}
    guard.out("PHASE0.json").write_text(json.dumps(res, indent=1, default=str))
    _report(res, desc)
    with guard.out("LEDGER.md").open("a") as f:
        f.write(f"- {res['run_utc']} UTC · Phase 0 · descriptive look: event counts and feature distributions for "
                f"S1, S2, S3, E (no outcomes); look-ahead and live parity; synthetic power on S1/S2 week structure. "
                f"Lock {lk['id'][:16]}.\n")
    log(f"[8/8] written: PHASE0.md, PHASE0.json, events/*.csv.gz · phase0_pass={res['phase0_pass']}")
    return res


def _report(res: dict, desc: dict) -> None:
    L = []
    st = res["status"]
    L.append("# R007 Phase 0: events, features and checks (no outcomes)\n")
    L.append(f"_Run {res['run_utc']} UTC · lock `{res['lock'][:16]}` · live reference `{res['live_ref']['sha'][:12]}` "
             f"({res['live_ref']['when']}) · snapshot `{str(res['snapshot']['id'])[:16]}`_\n")
    L.append(f"**Phase 0: {'PASS' if res['phase0_pass'] else 'NOT PASSED'}** · lock {'ok' if st['lock'] else 'FAIL'} · "
             f"look-ahead {'ok' if st['lookahead'] else 'FAIL'} · fidelity {'ok' if st['fidelity'] else 'FAIL'} · "
             f"live parity {'ok' if st['parity'] else 'FAIL'} · "
             f"power {'ok' if st['power'] else 'below criterion'}\n")
    L.append("No outcome was computed. Phase 1 (S1 gate) needs its own deploy and an explicit go.\n")
    U = res["universe"]
    L.append("## 1. Universe and snapshot")
    L.append(f"- Universe {U['total']} (live list): " + ", ".join(f"{k} {U.get(k, 0)}" for k in ["S1", "S2", "S3", "E", "X", "XD"]) +
             " (X = excluded, already used by IFI tests; XD = second share class of a company).")
    sn = res["snapshot"]
    L.append(f"- Snapshot: {sn['tickers']} tickers, {len(sn['missing'])} missing"
             f"{' (' + ', '.join(sn['missing'][:20]) + ')' if sn['missing'] else ''}; reused: {sn['reused']}; "
             f"tickers with a later split (price floor made point-in-time): {sn.get('tickers_with_splits')}.")
    b = res["build"]
    L.append(f"- Build: {b['stocks']} stocks read, {b['short_history']} too short, {b['no_data']} without data, "
             f"{b['no_group']} without a group; {b['etfs_with_state']} group ETFs with a state series.\n")
    L.append("## 2. Events")
    L.append(_md_table(desc["sets"]) + "\n")
    L.append("Events per year:\n")
    L.append(_md_table(desc["by_year"].reset_index()) + "\n")
    L.append("## 3. Features (S1 + S2, no outcomes)")
    L.append(_md_table(desc["categorical"]) + "\n")
    L.append(_md_table(desc["numeric"]) + "\n")
    if len(desc["corr"]):
        L.append("Feature pairs with |r| >= 0.4:\n")
        L.append(_md_table(desc["corr"]) + "\n")
    wt = res["w_tiers"]
    L.append(f"**Model W tier cut points** (terciles of S1 W scores): {wt['cuts'][0]:.3f} / {wt['cuts'][1]:.3f}\n")
    L.append(_md_table(pd.DataFrame([{"set": s, **v} for s, v in wt["sets"].items()])) + "\n")
    lk = res["lookahead"]
    L.append("## 4. Look-ahead (truncation) and fidelity to the weekly scan on real data")
    L.append(f"- {lk['symbols_tested']} symbols x {lk['cuts']} cuts: {'identical' if lk['ok'] else 'DIFFERENCES'}; "
             f"group-state failures {len(lk['group_state_failures'])}.")
    L.append(f"- Fidelity on the same symbols: week records vs weekscan `week_records` at {lk['fidelity_weeks']} weeks, "
             f"arms vs weekscan `step` ({lk['fidelity_arms']} arms): {'identical' if lk['fidelity_ok'] else 'DIFFERENCES'}"
             f"{': ' + '; '.join(lk['fidelity_failures'][:10]) if lk['fidelity_failures'] else ''}.")
    L.append("- Not covered by truncation (by design): Yahoo's split adjustment (handled by the split factor in the price "
             "floor; all other inputs are ratios) and weekscan's bad-tick filter, which removes one-bar spikes of 40%+ "
             "that fully reverse on the next bar.")
    for f in lk["failures"][:10]:
        L.append(f"  - {f['symbol']} {f['cut']}: {', '.join(f['differs'][:8])}")
    L.append("")
    p = res["parity"]
    L.append("## 5. Live parity (weekscan code on the R007 snapshot vs the live armed list)")
    if "error" in p:
        L.append(f"- ERROR: {p['error']}\n")
    else:
        L.append(f"- Armed: live {p['live_armed']}, R007 replay {p['r007_armed']}, shared {p['shared']}, "
                 f"Jaccard {p['jaccard']}; among shared: armed week {p['armed_week_agree']:.1%}, "
                 f"low {p['low_agree']:.1%}, released {p['released_agree']:.1%}. "
                 f"Week alerts: live {p['week_alerts_live']}, R007 {p['week_alerts_r007']}, Jaccard {p['week_alerts_jaccard']}.")
        L.append(f"- Only live: {', '.join(p['only_live']) or '–'}")
        L.append(f"- Only R007: {', '.join(p['only_r007']) or '–'}")
        mr = p.get("mismatch_reasons", {})
        if mr:
            L.append(f"- Mismatches near the eligibility thresholds at the live run date (price within 10% of $5 or "
                     f"dollar volume within 25% of $20M, where intraday vs end-of-day data can flip them): "
                     f"{mr.get('near_threshold', 0)} of {mr.get('total', 0)}.")
        L.append("")
    L.append("## 6. Synthetic power (real event weeks, random tiers, planted A-C spread)")
    for s, rows in res["power"].items():
        if rows:
            df = pd.DataFrame(rows)[["spread_R", "events", "weeks_with_events", "power", "power_holm_worst",
                                     "gate_pass", "mean_est", "sd_est"]]
            L.append(f"**{s}**\n")
            L.append(_md_table(df) + "\n")
    L.append("`power` = P(one-sided p < 0.05); `power_holm_worst` = P(p < 0.025); `gate_pass` = the full Phase 1 rule "
             "(p < 0.05, spread >= 0.15R, each half >= 0.075R); at a true spread of exactly 0.15R the point rule alone "
             "passes about half the time, so read `gate_pass` for the chance that Phase 1 passes at each true spread. "
             "Criterion: power >= 0.80 at 0.15R on S1 with random "
             "thirds. The `(W tiers)` tables use model W's actual tiers, which involve no outcome; they show how much "
             "power is lost when a model's tiers cluster by week (reported, not judged).\n")
    guard.out("PHASE0.md").write_text("\n".join(L))
