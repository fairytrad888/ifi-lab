"""Stage 2, outcome-blind: does the code see what your eye sees?

Inputs
  eyelab/examples/<RULE>.csv         your labelled cases: symbol,tf,date,label(1 yes / 0 no),source,note
  eyelab/examples/<RULE>_review.csv  optional: your verdicts on blind hits: chart_id,agree(1/0)
Outputs (OUT/fidelity/<RULE>/v<version>/)
  FIDELITY.md, FIDELITY.json    recall on your yes cases, specificity on your no cases, blind agreement, gate
  examples/*.png                every miss, with its symbol and date (you already know these charts)
  blind/sheet_*.png             a random sample of the rule's hits on the dev pool, ticker/dates/prices hidden
  blind/KEY.csv                 chart_id -> symbol, date (look only after you have reviewed the sheets)
No outcome is computed anywhere in this stage (blind mode is on; the engine refuses).
Symbols in your examples that belong to pool A or B are excluded from grading this rule (your eye has seen them).
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from . import guard, ledger
from .charts import render, sheet
from .data import home, pool_of, pool_symbols
from .features import frame
from .guard import CFG, ROOT, out, outdir
from .registry import fires, load_rule, look_ahead_ok, rule_sha


def examples(rule_id: str) -> pd.DataFrame:
    f = ROOT / "examples" / f"{rule_id}.csv"
    if not f.exists():
        return pd.DataFrame(columns=["symbol", "tf", "date", "label", "source", "note"])
    e = pd.read_csv(f, comment="#")
    e["date"] = pd.to_datetime(e["date"])
    return e


def contaminated(rule_id: str) -> set[str]:
    e = examples(rule_id)
    return {s for s in e["symbol"].unique() if pool_of(s) in ("A", "B")} if len(e) else set()


def run(rule_id: str) -> dict:
    if hasattr(load_rule(rule_id), "STUDY"):
        from .study import fidelity as study_fidelity
        return study_fidelity(rule_id)
    guard.enter_blind()
    try:
        return _run(rule_id)
    finally:
        guard.leave_blind()


def _run(rule_id: str) -> dict:
    mod = load_rule(rule_id)
    spec, tf = mod.SPEC, mod.SPEC["timeframe"]
    sha = rule_sha(rule_id)
    fc = CFG["fidelity"]
    tol = fc["tolerance_bars"][tf]
    base = outdir("fidelity", rule_id, f"v{spec['version']}")
    ex = examples(rule_id)
    ex = ex[ex["tf"] == tf] if len(ex) else ex

    # 1. your labelled examples (frames stop `tol` bars after the example date)
    res = []
    for k, r in ex.reset_index(drop=True).iterrows():
        pool = home(r["symbol"])
        x = frame(pool, r["symbol"], tf, "example", until=r["date"], extra_bars=tol)
        if x is None:
            res.append({**r, "fired": np.nan, "note_eyelab": "no data"})
            continue
        f = fires(mod, x)
        i0 = int(x.index.searchsorted(r["date"]))
        win = f.iloc[max(0, i0 - tol): i0 + tol + 1]
        hit = bool(win.any())
        res.append({**r, "fired": hit, "note_eyelab": ""})
        if hit != bool(r["label"]):
            kind = "missed_yes" if r["label"] else "false_fire"
            render(x, min(i0, len(x) - 1), base / "examples" / f"{kind}_{r['symbol']}_{r['date']:%Y%m%d}.png",
                   bars=fc["chart_bars"][tf], blind=False, after=0,
                   title=f"{rule_id} {kind}: {r['symbol']} {r['date']:%Y-%m-%d} (your label {int(r['label'])})",
                   marks=list(np.flatnonzero(f.to_numpy())))
    rd = pd.DataFrame(res)
    yes = rd[rd.get("label", pd.Series(dtype=int)) == 1] if len(rd) else rd
    no = rd[rd.get("label", pd.Series(dtype=int)) == 0] if len(rd) else rd
    recall = float(yes["fired"].mean()) if len(yes) else np.nan
    spec_ = float(1 - no["fired"].mean()) if len(no) else np.nan

    # 2. blind sample of the rule's hits on the dev pool, plus how often it fires
    hits, la_ok, sym_years = [], True, 0.0
    for s in pool_symbols("dev"):
        x = frame("dev", s, tf, "fidelity")
        if x is None:
            continue
        f = fires(mod, x)
        sym_years += len(x) / {"D": 252, "W": 52, "H4": 504}[tf]
        hits += [(s, int(i)) for i in np.flatnonzero(f.to_numpy())]
        if la_ok and s in ("SPY", "XLK", "JPM"):
            la_ok = look_ahead_ok(mod, x)
    rng = np.random.default_rng(int(sha[:8], 16))
    pick = rng.choice(len(hits), size=min(fc["blind_sample"], len(hits)), replace=False) if hits else []
    key, pngs = [], []
    for k, idx in enumerate(sorted(pick)):
        s, i = hits[idx]
        x = frame("dev", s, tf, "fidelity")
        cid = f"{rule_id}-{k + 1:02d}"
        pngs.append(render(x, i, base / "blind" / f"{cid}.png", bars=fc["chart_bars"][tf], blind=True, title=cid))
        key.append({"chart_id": cid, "symbol": s, "date": str(x.index[i])[:16]})
    for j in range(0, len(pngs), 9):
        sheet(pngs[j:j + 9], base / "blind" / f"sheet_{j // 9 + 1}.png")
    pd.DataFrame(key).to_csv(base / "blind" / "KEY.csv", index=False)

    # 3. your verdicts on the blind sheets, if given
    rv = ROOT / "examples" / f"{rule_id}_review.csv"
    agree = n_rev = np.nan
    if rv.exists():
        r = pd.read_csv(rv, comment="#")
        r = r[r["chart_id"].isin([k["chart_id"] for k in key])]
        n_rev = int(len(r))
        agree = float(r["agree"].mean()) if n_rev else np.nan

    gate = bool(len(rd) >= fc["min_examples"] and recall >= fc["min_recall"] and spec_ >= fc["min_specificity"]
                and n_rev == len(key) and len(key) > 0 and agree >= fc["min_blind_agree"] and la_ok)
    meta = {"rule_id": rule_id, "version": spec["version"], "rule_sha": sha, "tf": tf, "examples": int(len(rd)),
            "yes": int(len(yes)), "no": int(len(no)), "recall": recall, "specificity": spec_,
            "blind_hits_total": len(hits), "fires_per_symbol_year": len(hits) / sym_years if sym_years else np.nan,
            "blind_sample": len(key), "blind_reviewed": n_rev, "blind_agree": agree, "look_ahead_ok": la_ok,
            "excluded_from_grading": sorted(contaminated(rule_id)), "gate_passed": gate}
    (base / "FIDELITY.json").write_text(json.dumps(meta, indent=1, default=str))
    rd.to_csv(base / "examples.csv", index=False)
    md = [f"# Fidelity: {rule_id} v{spec['version']} ({spec['name']})", "",
          f"_Outcome-blind. Rule file sha256 `{sha[:16]}`. Timeframe {tf}, tolerance ±{tol} bars._", "",
          f"**Your words:** {spec['eye_description']}", "",
          "| check | value | needed |", "|---|---|---|",
          f"| labelled examples | {len(rd)} ({len(yes)} yes / {len(no)} no) | ≥ {fc['min_examples']} |",
          f"| recall on your yes cases | {recall:.0%} | ≥ {fc['min_recall']:.0%} |" if len(yes) else "| recall | – | |",
          f"| silent on your no cases | {spec_:.0%} | ≥ {fc['min_specificity']:.0%} |" if len(no) else "| specificity | – | |",
          f"| blind sheets reviewed | {n_rev if n_rev == n_rev else 0} of {len(key)} | all |",
          f"| blind agreement | {agree:.0%} | ≥ {fc['min_blind_agree']:.0%} |" if agree == agree else "| blind agreement | not yet reviewed | |",
          f"| look-ahead test | {'ok' if la_ok else 'FAILED'} | ok |", "",
          f"**Gate: {'PASSED: the rule may go to discovery' if gate else 'not passed yet'}**", "",
          f"The rule fires about {meta['fires_per_symbol_year']:.2f} times per symbol-year on the dev pool ({len(hits)} hits).",
          f"Excluded from grading (in your examples and in pool A/B): {', '.join(meta['excluded_from_grading']) or 'none'}."]
    misses = rd[rd["fired"] != rd["label"].astype(bool)] if len(rd) else rd
    if len(misses):
        md += ["", "## Disagreements with your labels", "", "| symbol | date | your label | rule |", "|---|---|---|---|"]
        md += [f"| {m.symbol} | {m.date:%Y-%m-%d} | {int(m.label)} | {'fired' if m.fired else 'silent'} |" for m in misses.itertuples()]
    (base / "FIDELITY.md").write_text("\n".join(md) + "\n")
    ledger.append(stage="fidelity", rule_id=rule_id, version=spec["version"], rule_sha=sha, pool="dev", tf=tf,
                  n_signals=len(hits), looked_at="rule hits and labels only (no outcomes)",
                  result="gate passed" if gate else "gate not passed")
    return meta


def passed(rule_id: str) -> bool:
    mod = load_rule(rule_id)
    f = out("fidelity", rule_id, f"v{mod.SPEC['version']}", "FIDELITY.json")
    if not f.exists():
        return False
    m = json.loads(f.read_text())
    return bool(m.get("gate_passed")) and m.get("rule_sha") == rule_sha(rule_id)
