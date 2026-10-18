"""Event studies (rules with STUDY = "ratio_flip"): events, structural outcomes, nulls, condition lifts.

A study rule file defines SPEC, STUDY, HYPOTHESES = [(name, tier), ...] (the first one is primary) and BLIND
(which events the blind review samples). The pipeline is the same as for simple rules:
fidelity (outcome-blind) -> discovery (pool A) -> lock -> confirmation (pool B, opened once).
Comparisons
  base      events of a tier vs the context null (random days of the same ratio in the same downtrend context)
            and the cross null (same day, other ratios in context)
  C / K     lift = P(outcome | event and condition) - P(outcome | event and not condition), same tier
Inference: bootstrap over calendar months; one-sided p; Holm across the rule's hypotheses.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from . import guard, ledger
from .charts import render, sheet
from .data import load, pool_symbols
from .features import enrich
from .guard import CFG, ROOT, out, outdir
from .registry import load_rule, rule_sha
from .studies import ratio_flip as RF

M = CFG["nulls"]["per_signal"]


# ----------------------------------------------------------------------------- frames
def frames_for(pool: str, purpose: str, syms: list[str] | None = None, jitter: float = 0.0, seed: int = 0):
    bench = load("bench", "SPY", "D", purpose)
    if bench is None:
        raise RuntimeError("benchmark SPY not in the snapshot")
    rng = np.random.default_rng(seed)
    syms = syms if syms is not None else RF.etf_universe(pool_symbols(pool))
    fr, nums = {}, {}
    for s in syms:
        a = load(pool, s, "D", purpose)
        if a is None:
            continue
        a = a[a.index >= CFG["history_start"]]
        b = bench
        if jitter:
            f1 = np.exp(rng.normal(0, jitter, (len(a), 1)))
            a = a.copy()
            a[["open", "high", "low", "close"]] = a[["open", "high", "low", "close"]].to_numpy() * f1
            b = bench.copy()
            b[["open", "high", "low", "close"]] = b[["open", "high", "low", "close"]].to_numpy() * \
                np.exp(rng.normal(0, jitter, (len(b), 1)))
        r = RF.ratio_bars(a, b)
        if len(r) < 400:
            continue
        x = RF.annotate(enrich(r, b))
        fr[s] = x
        u = RF.atr(a).to_numpy()
        nums[s] = {"o": a["open"].to_numpy(float), "h": a["high"].to_numpy(float), "l": a["low"].to_numpy(float),
                   "u": u, "pos": {d: k for k, d in enumerate(a.index)}}
    return fr, nums


# ----------------------------------------------------------------------------- events and nulls
def collect(fr: dict, nums: dict, seed: int | None = None) -> pd.DataFrame:
    guard_outcomes()
    rng = np.random.default_rng(CFG["nulls"]["seed"] if seed is None else seed)
    cache: dict = {}

    def oc(s, i):
        k = (s, i)
        if k not in cache:
            cache[k] = RF.outcomes(fr[s], i, nums.get(s))
        return cache[k]

    ctx_bars, by_date = {}, {}
    for s, x in fr.items():
        n = len(x)
        ok = x["context"].to_numpy() & (x["bar"].to_numpy() >= 250) & (np.arange(n) < n - RF.MAX_H - 1)
        ctx_bars[s] = np.flatnonzero(ok)
        for i in ctx_bars[s]:
            by_date.setdefault(x.index[i], []).append((s, int(i)))
    conds = list(RF.COND_TEXT) + ["S1"] + list(RF.COMBOS)
    rows = []
    for s, x in fr.items():
        for tier in (2, 3):
            for i in np.flatnonzero(x[f"e{tier}"].to_numpy()):
                o = oc(s, int(i))
                if o is None:
                    continue
                row = {"symbol": s, "date": x.index[i], "bar": int(i), "tier": tier,
                       "regime_up": bool(x["spy_trend_up"].iloc[i]), **{c: bool(x[c].iloc[i]) for c in conds},
                       "down9_cycles": int(x["down9_cycles"].iloc[i]), "angle": float(x["angle"].iloc[i]),
                       "room": float(x["room"].iloc[i]), **o}
                cb = ctx_bars[s]
                tn = rng.choice(cb, size=M, replace=len(cb) < M) if len(cb) else []
                tv = [oc(s, int(t)) for t in tn]
                pool = [q for q in by_date.get(x.index[i], []) if q[0] != s]
                cv = [oc(*pool[k]) for k in rng.choice(len(pool), size=M, replace=len(pool) < M)] if pool else []
                for nm in RF.OUTCOMES:
                    t_ = [v[nm] for v in tv if v is not None and np.isfinite(v.get(nm, np.nan))]
                    c_ = [v[nm] for v in cv if v is not None and np.isfinite(v.get(nm, np.nan))]
                    row[f"{nm}_ctx"] = float(np.mean(t_)) if t_ else np.nan
                    row[f"{nm}_cross"] = float(np.mean(c_)) if c_ else np.nan
                rows.append(row)
    return pd.DataFrame(rows)


def guard_outcomes():
    if guard.is_blind():
        raise PermissionError("blind mode: outcomes are never computed during fidelity work")


# ----------------------------------------------------------------------------- inference
def _months(d):
    return pd.to_datetime(d).dt.to_period("M").astype(str).to_numpy()


def mean_boot(v, cl, B=None, seed=None) -> dict:
    v = np.asarray(v, float)
    ok = np.isfinite(v)
    v, cl = v[ok], np.asarray(cl)[ok]
    if len(v) < 5:
        return {"n": int(len(v)), "mean": float(v.mean()) if len(v) else np.nan, "lo": np.nan, "hi": np.nan, "p": np.nan}
    B = B or CFG["inference"]["boot"]
    rng = np.random.default_rng(CFG["inference"]["seed"] if seed is None else seed)
    keys, inv = np.unique(cl, return_inverse=True)
    s, c = np.bincount(inv, weights=v), np.bincount(inv).astype(float)
    d = rng.integers(0, len(keys), size=(B, len(keys)))
    m = s[d].sum(1) / c[d].sum(1)
    return {"n": int(len(v)), "mean": float(v.mean()), "lo": float(np.quantile(m, .025)), "hi": float(np.quantile(m, .975)),
            "p": float((m <= 0).mean())}


def lift_boot(v, mask, cl, B=None, seed=None) -> dict:
    v, mask = np.asarray(v, float), np.asarray(mask, bool)
    ok = np.isfinite(v)
    v, mask, cl = v[ok], mask[ok], np.asarray(cl)[ok]
    nC, nN = int(mask.sum()), int((~mask).sum())
    res = {"n_c": nC, "n_not": nN, "p_c": float(v[mask].mean()) if nC else np.nan,
           "p_not": float(v[~mask].mean()) if nN else np.nan}
    res["lift"] = res["p_c"] - res["p_not"]
    if nC < 10 or nN < 10:
        return {**res, "lo": np.nan, "hi": np.nan, "p": np.nan}
    B = B or CFG["inference"]["boot"]
    rng = np.random.default_rng(CFG["inference"]["seed"] if seed is None else seed)
    keys, inv = np.unique(cl, return_inverse=True)
    sC = np.bincount(inv, weights=v * mask, minlength=len(keys))
    cC = np.bincount(inv, weights=mask.astype(float), minlength=len(keys))
    sN = np.bincount(inv, weights=v * ~mask, minlength=len(keys))
    cN = np.bincount(inv, weights=(~mask).astype(float), minlength=len(keys))
    d = rng.integers(0, len(keys), size=(B, len(keys)))
    with np.errstate(invalid="ignore", divide="ignore"):
        L = sC[d].sum(1) / cC[d].sum(1) - sN[d].sum(1) / cN[d].sum(1)
    L = L[np.isfinite(L)]
    return {**res, "lo": float(np.quantile(L, .025)), "hi": float(np.quantile(L, .975)), "p": float((L <= 0).mean())}


def holm(ps: list[float], alpha: float = 0.05) -> list[bool]:
    idx = [i for i in np.argsort([p if p == p else 1.0 for p in ps])]
    ok, m, alive = [False] * len(ps), len(ps), True
    for r, i in enumerate(idx):
        p = ps[i]
        if alive and p == p and p <= alpha / (m - r):
            ok[i] = True
        else:
            alive = False
    return ok


def test_hypotheses(df: pd.DataFrame, hyps: list, outcome: str) -> list[dict]:
    res = []
    for name, tier in hyps:
        d = df[df["tier"] == tier]
        cl = _months(d["date"]) if len(d) else np.array([])
        if name == "base":
            b = mean_boot((d[outcome] - d[f"{outcome}_ctx"]).to_numpy(), cl)
            x = mean_boot((d[outcome] - d[f"{outcome}_cross"]).to_numpy(), cl)
            res.append({"hyp": "base", "tier": tier, "n": b["n"], "event": float(d[outcome].mean()) if len(d) else np.nan,
                        "ctx": float(d[f"{outcome}_ctx"].mean()) if len(d) else np.nan, "adv_ctx": b,
                        "adv_cross": x, "p": b["p"]})
        else:
            L = lift_boot(d[outcome].to_numpy(), d[name].to_numpy(), cl)
            sub = d[d[name]]
            adv = mean_boot((sub[outcome] - sub[f"{outcome}_ctx"]).to_numpy(), _months(sub["date"])) if len(sub) else {}
            res.append({"hyp": name, "tier": tier, **L, "adv_ctx": adv})
    passed = holm([r["p"] for r in res])
    for r, ok in zip(res, passed):
        r["holm_pass"] = bool(ok)
    return res


# ----------------------------------------------------------------------------- reports
def _pct(v):
    return "–" if v is None or v != v else f"{v * 100:.0f}%"


def _pts(b):
    if not b or b.get("lo") is None or b.get("lo") != b.get("lo"):
        return "–"
    m = b.get("mean", b.get("lift"))
    return f"{m * 100:+.1f} pts ({b['lo'] * 100:+.1f} to {b['hi'] * 100:+.1f})"


def report(mod, df: pd.DataFrame, res: list[dict], stage: str, pool: str, extra: list[str], stab: dict | None,
           sec: list[dict] | None = None) -> str:
    spec = mod.SPEC
    po = mod.PRIMARY
    md = [f"# {stage.title()}: {spec['id']} v{spec['version']} ({spec['name']}) on pool {pool}", "",
          f"_Rule sha256 `{rule_sha(spec['id'])[:16]}` · ETF/SPY ratios ({', '.join(RF.CLASSES)}) · "
          f"{df['symbol'].nunique() if len(df) else 0} ratios · events with complete outcomes: tier 2 = "
          f"{int((df['tier'] == 2).sum()) if len(df) else 0}, tier 3 = {int((df['tier'] == 3).sum()) if len(df) else 0}_", "",
          f"**Your words:** {spec['eye_description']}", "", f"**Primary outcome:** {po} · " + {
              "o1_up9": "an up-9 completes within 20 bars before a close below the event low"}.get(po, po), ""]
    md += extra
    md += ["## Pre-registered hypotheses (Holm across this test)", "",
           "| hypothesis | tier | n with / without | P(outcome) with / without | lift (95%) | one-sided p | Holm | with-condition events vs context null |",
           "|---|---|---|---|---|---|---|---|"]
    for r in res:
        if r["hyp"] == "base":
            md.append(f"| events vs context null | {r['tier']} of 4 | {r['n']} | {_pct(r['event'])} vs {_pct(r['ctx'])} | "
                      f"{_pts(r['adv_ctx'])} | {r['p']:.3f} | {'pass' if r['holm_pass'] else '–'} | cross null {_pts(r['adv_cross'])} |")
        else:
            label = RF.COND_TEXT.get(r["hyp"]) or " + ".join(RF.COND_TEXT.get(c, "a trigger in the window") for c in RF.COMBOS.get(r["hyp"], ()))
            md.append(f"| {r['hyp']}: {label} | {r['tier']} of 4 | {r['n_c']} / {r['n_not']} | {_pct(r['p_c'])} / {_pct(r['p_not'])} | "
                      f"{_pts(r)} | {r['p'] if r['p'] == r['p'] else float('nan'):.3f} | {'pass' if r['holm_pass'] else '–'} | {_pts(r['adv_ctx'])} |")
    if sec:
        md += ["", "## Secondary (descriptive, not part of the verdict)", "",
               "| item | tier | n with / without | P with / without | lift or advantage (95%) |", "|---|---|---|---|---|"]
        for r in sec:
            if r["hyp"] == "base":
                md.append(f"| events vs context null | {r['tier']} | {r['n']} | {_pct(r['event'])} vs {_pct(r['ctx'])} | {_pts(r['adv_ctx'])} |")
            else:
                md.append(f"| {r['hyp']} | {r['tier']} | {r['n_c']} / {r['n_not']} | {_pct(r['p_c'])} / {_pct(r['p_not'])} | {_pts(r)} |")
    if len(df):
        md += ["", "## All outcomes by tier (descriptive)", "", "| outcome | tier 2 events | context null | tier 3 events | context null |", "|---|---|---|---|---|"]
        for nm in RF.OUTCOMES:
            vals = []
            for t in (2, 3):
                d = df[df["tier"] == t]
                vals += [_pct(d[nm].mean()), _pct(d[f"{nm}_ctx"].mean())]
            md.append(f"| {nm} | " + " | ".join(vals) + " |")
        md += ["", "_o1_up9: up-9 within 20 bars before the event low breaks · o2_flip: close above the key level (last lower high) "
                   "before the event low breaks, 60 bars · o3: +k ATR before -1 ATR within 40 bars, on the ratio and on the ETF itself._", ""]
        d = df[df["tier"] == 2]
        if len(d):
            sp = pd.to_datetime(d["date"]).sort_values().iloc[len(d) // 2]
            md += ["## Primary outcome, tier 2, by slice", "", "| slice | n | P | context null |", "|---|---|---|---|"]
            for name, q in ((f"first half (before {sp:%Y-%m})", d[pd.to_datetime(d["date"]) < sp]),
                            (f"second half (from {sp:%Y-%m})", d[pd.to_datetime(d["date"]) >= sp]),
                            ("SPY trend up", d[d["regime_up"]]), ("SPY trend not up", d[~d["regime_up"]])):
                md.append(f"| {name} | {len(q)} | {_pct(q[po].mean())} | {_pct(q[f'{po}_ctx'].mean())} |")
            md.append("")
    if stab:
        md += ["## Stability under ±0.01% price jitter (does a tiny data difference change the event or a condition?)", "",
               "| item | share unchanged |", "|---|---|"] + [f"| {k} | {_pct(v)} |" for k, v in stab.items()] + [""]
    return "\n".join(md) + "\n"


def stability(fr: dict, pool: str, purpose: str) -> dict:
    fj, _ = frames_for(pool, purpose, syms=list(fr), jitter=1e-4, seed=11)
    out, same_ev = {}, {2: [], 3: []}
    conds = list(RF.COND_TEXT) + list(RF.COMBOS)
    agree = {c: [] for c in conds}
    for s, x in fr.items():
        y = fj.get(s)
        if y is None:
            continue
        for t in (2, 3):
            ev = np.flatnonzero(x[f"e{t}"].to_numpy())
            ej = set(np.flatnonzero(y[f"e{t}"].to_numpy()))
            for i in ev:
                hit = bool({i - 1, i, i + 1} & ej)
                same_ev[t].append(hit)
                if hit:
                    for c in conds:
                        agree[c].append(bool(x[c].iloc[i]) == bool(y[c].iloc[i]))
    for t in (2, 3):
        out[f"tier {t} events"] = float(np.mean(same_ev[t])) if same_ev[t] else np.nan
    for c in conds:
        out[c] = float(np.mean(agree[c])) if agree[c] else np.nan
    return out


# ----------------------------------------------------------------------------- stages
def fidelity(rule_id: str) -> dict:
    guard.enter_blind()
    try:
        return _fidelity(rule_id)
    finally:
        guard.leave_blind()


def _fidelity(rule_id: str) -> dict:
    from .fidelity import examples
    mod = load_rule(rule_id)
    spec, sha, fc = mod.SPEC, rule_sha(rule_id), CFG["fidelity"]
    tol = fc["tolerance_bars"]["D"]
    base = outdir("fidelity", rule_id, f"v{spec['version']}")
    fr, _ = frames_for("dev", "fidelity")
    # look-ahead: events and conditions on bars <= c unchanged when later bars are deleted
    la_ok = True
    bench = load("bench", "SPY", "D", "fidelity")
    for s in list(fr)[:3]:
        a = load("dev", s, "D", "fidelity")
        a = a[a.index >= CFG["history_start"]]
        r = RF.ratio_bars(a, bench)
        full = fr[s]
        cols = ["e2", "e3"] + list(RF.COND_TEXT) + list(RF.COMBOS)
        for c in np.random.default_rng(5).integers(400, len(r) - 1, size=3):
            xt = RF.annotate(enrich(r.iloc[:c + 1], bench))
            if not xt[cols].equals(full[cols].iloc[:c + 1]):
                la_ok = False
    # your examples (symbol = the ETF; the ratio is ETF / SPY)
    ex = examples(rule_id)
    res = []
    for _, e in ex.iterrows():
        s = e["symbol"]
        if s not in fr:
            res.append({**e, "fired": np.nan})
            continue
        x = fr[s]
        i0 = int(x.index.searchsorted(e["date"]))
        w = x.iloc[max(0, i0 - tol): i0 + tol + 1]
        hit = bool(mod.blind_mask(w).any())
        res.append({**e, "fired": hit})
    rd = pd.DataFrame(res)
    yes = rd[rd["label"] == 1] if len(rd) else rd
    no = rd[rd["label"] == 0] if len(rd) else rd
    recall = float(yes["fired"].mean()) if len(yes) else np.nan
    specif = float(1 - no["fired"].mean()) if len(no) else np.nan
    # blind sample of events on the dev ratios
    hits = []
    for s, x in fr.items():
        m = mod.blind_mask(x).to_numpy() & (x["bar"].to_numpy() >= 250)
        hits += [(s, int(i)) for i in np.flatnonzero(m)]
    rng = np.random.default_rng(int(sha[:8], 16))
    pick = sorted(rng.choice(len(hits), size=min(fc["blind_sample"], len(hits)), replace=False)) if hits else []
    key, pngs = [], []
    for k, idx in enumerate(pick):
        s, i = hits[idx]
        cid = f"{rule_id.split('_')[0]}-{k + 1:02d}"
        pngs.append(render(fr[s], i, base / "blind" / f"{cid}.png", bars=fc["chart_bars"]["D"], blind=True, title=cid))
        x = fr[s]
        key.append({"chart_id": cid, "ratio": f"{s}/SPY", "date": str(x.index[i])[:10], "tier": int(x["n_types"].iloc[i]),
                    **{c: bool(x[c].iloc[i]) for c in list(RF.COND_TEXT) + list(RF.COMBOS)}})
    for j in range(0, len(pngs), 9):
        sheet(pngs[j:j + 9], base / "blind" / f"sheet_{j // 9 + 1}.png")
    pd.DataFrame(key).to_csv(base / "blind" / "KEY.csv", index=False)
    rv = ROOT / "examples" / f"{rule_id}_review.csv"
    agree = n_rev = np.nan
    if rv.exists():
        r = pd.read_csv(rv, comment="#")
        r = r[r["chart_id"].isin([k["chart_id"] for k in key])]
        n_rev, agree = int(len(r)), (float(r["agree"].mean()) if len(r) else np.nan)
    ex_ok = (len(rd) == 0) or ((not len(yes) or recall >= fc["min_recall"]) and (not len(no) or specif >= fc["min_specificity"]))
    gate = bool(la_ok and ex_ok and len(key) > 0 and n_rev == len(key) and agree >= fc["min_blind_agree"])
    yrs = sum(len(x) for x in fr.values()) / 252
    meta = {"rule_id": rule_id, "version": spec["version"], "rule_sha": sha, "ratios": len(fr), "events_dev": len(hits),
            "events_per_ratio_year": len(hits) / yrs if yrs else np.nan, "examples": int(len(rd)), "recall": recall,
            "specificity": specif, "blind_sample": len(key), "blind_reviewed": n_rev, "blind_agree": agree,
            "look_ahead_ok": la_ok, "gate_passed": gate}
    (base / "FIDELITY.json").write_text(json.dumps(meta, indent=1, default=str))
    rd.to_csv(base / "examples.csv", index=False)
    md = [f"# Fidelity: {rule_id} v{spec['version']} ({spec['name']})", "",
          f"_Outcome-blind · {len(fr)} dev ratios · {len(hits)} events ({meta['events_per_ratio_year']:.2f} per ratio-year)_", "",
          f"**Your words:** {spec['eye_description']}", "",
          f"- Examples: {len(rd)} · recall {_pct(recall)} · silent on no-cases {_pct(specif)}",
          f"- Blind sheets: {len(key)} charts · reviewed {0 if n_rev != n_rev else n_rev} · agreement {_pct(agree)} (need ≥ {fc['min_blind_agree']:.0%})",
          f"- Look-ahead test: {'ok' if la_ok else 'FAILED'}", "",
          f"**Gate: {'PASSED' if gate else 'not passed yet'}**"]
    (base / "FIDELITY.md").write_text("\n".join(md) + "\n")
    ledger.append(stage="fidelity", rule_id=rule_id, version=spec["version"], rule_sha=sha, pool="dev", tf="D",
                  n_signals=len(hits), looked_at="events and conditions only (no outcomes)",
                  result="gate passed" if gate else "gate not passed")
    return meta


def discovery(rule_id: str, force: bool = False) -> dict:
    from .fidelity import passed
    mod = load_rule(rule_id)
    if not passed(rule_id) and not force:
        raise PermissionError(f"{rule_id}: fidelity gate not passed for this rule version (or --force, which the ledger records)")
    sha = rule_sha(rule_id)
    fr, nums = frames_for("A", "discovery")
    df = collect(fr, nums)
    res = test_hypotheses(df, mod.HYPOTHESES, mod.PRIMARY)
    stab = stability(fr, "A", "discovery")
    prim = res[0]
    carried = [[r["hyp"], r["tier"]] for r in res if r["holm_pass"]] if mod.CARRY == "holm_pass" else [list(h) for h in mod.HYPOTHESES[:1]]
    v = ledger.variants_tried(rule_id) + (0 if any(r["rule_sha"] == sha[:16] and r["stage"] == "discovery" for r in ledger.rows()) else 1)
    extra = [f"**Primary ({prim['hyp']}, tier {prim['tier']}):** one-sided p = {prim['p']:.3f}, "
             f"{'clears' if prim['holm_pass'] else 'does not clear'} the bar on pool A.", "",
             f"Carried to confirmation if locked: {', '.join(f'{h} (tier {t})' for h, t in carried) or 'nothing'}. "
             f"Versions of {rule_id} measured so far: **{v}**.", ""]
    base = outdir("discovery", rule_id, sha[:16])
    sec = test_hypotheses(df, mod.SECONDARY, mod.PRIMARY) if mod.SECONDARY else []
    (base / "DISCOVERY.md").write_text(report(mod, df, res, "discovery", "A", extra, stab, sec))
    df.to_csv(base / "events.csv", index=False)
    meta = {"rule_id": rule_id, "version": mod.SPEC["version"], "rule_sha": sha, "events": int(len(df)), "results": res,
            "carried": carried, "stability": stab, "variants_tried": v}
    (base / "DISCOVERY.json").write_text(json.dumps(meta, indent=1, default=str))
    ledger.append(stage="discovery", rule_id=rule_id, version=mod.SPEC["version"], rule_sha=sha, pool="A", tf="D",
                  n_signals=len(df), looked_at=f"all outcomes on pool A ETF ratios ({mod.PRIMARY} primary)",
                  result=f"primary p={prim['p']:.3f}", note="FORCED without fidelity gate" if force and not passed(rule_id) else "")
    return {k: meta[k] for k in ("rule_id", "events", "carried", "variants_tried")} | {"primary": prim}


def carried(rule_id: str) -> list:
    sha = rule_sha(rule_id)
    f = out("discovery", rule_id, sha[:16], "DISCOVERY.json")
    return json.loads(f.read_text())["carried"] if f.exists() else []


def confirm(rule_id: str, lk: dict) -> dict:
    mod = load_rule(rule_id)
    fr, nums = frames_for("B", "confirm")
    df = collect(fr, nums)
    hyps = [tuple(h) for h in lk["hypotheses"]]
    res = test_hypotheses(df, hyps, mod.PRIMARY)
    ok = [r["holm_pass"] and (r["hyp"] == "base" or (r.get("adv_ctx") or {}).get("mean", -1) > 0) for r in res]
    verdict = "CONFIRMED" if res and all(ok) else ("PARTLY CONFIRMED" if any(ok) else "NOT CONFIRMED")
    extra = [f"**Verdict: {verdict}** · locked hypotheses: {', '.join(f'{h} (tier {t})' for h, t in hyps)}. "
             "Each must clear Holm (one-sided 5%) and, for a condition, its events must also beat the context null.", ""]
    base = outdir("confirm", rule_id, f"v{mod.SPEC['version']}")
    sec = test_hypotheses(df, mod.SECONDARY, mod.PRIMARY) if mod.SECONDARY else []
    (base / "CONFIRM.md").write_text(report(mod, df, res, "confirmation", "B", extra, None, sec))
    df.to_csv(base / "events.csv", index=False)
    meta = {"rule_id": rule_id, "version": mod.SPEC["version"], "verdict": verdict, "events": int(len(df)), "results": res}
    (base / "CONFIRM.json").write_text(json.dumps(meta, indent=1, default=str))
    return meta
