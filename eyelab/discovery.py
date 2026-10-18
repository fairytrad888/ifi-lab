"""Stages 3 and 5: measure a rule's process advantage on a pool.

discovery (pool A): exploratory. Every run of a new rule version is a counted variant in the ledger.
confirm   (pool B): the single pre-registered test of a locked rule version (see confirm.py).
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from . import engine, ledger
from .data import pool_symbols
from .features import frame
from .fidelity import contaminated, passed
from .guard import CFG, ROOT, out, outdir
from .registry import fires, load_rule, rule_sha, units

ETFS = {s.strip() for s in (ROOT / "pools" / "etfs.txt").read_text().splitlines() if s.strip() and not s.startswith("#")}


def measure(rule_id: str, pool: str, purpose: str) -> tuple[pd.DataFrame, dict]:
    mod = load_rule(rule_id)
    tf, direction = mod.SPEC["timeframe"], mod.SPEC["direction"]
    excl = contaminated(rule_id)
    frames, sig, unit, regime = {}, {}, {}, {}
    for s in pool_symbols(pool):
        if s in excl:
            continue
        x = frame(pool, s, tf, purpose)
        if x is None:
            continue
        frames[s], sig[s], unit[s] = x, fires(mod, x), units(mod, x)
        regime[s] = x["spy_trend_up"]
    df = engine.evaluate(frames, sig, unit, tf, direction)
    if len(df):
        df["regime_up"] = [bool(regime[s].get(d, False)) for s, d in zip(df["symbol"], df["date"])]
        df["etf"] = df["symbol"].isin(ETFS)
        df["year"] = pd.to_datetime(df["date"]).dt.year
    info = {"symbols": len(frames), "excluded": sorted(excl), "tf": tf, "direction": direction}
    return df, info


def _fmt(b: dict, pct: bool = False) -> str:
    if not b or b.get("n", 0) < 2:
        return "–"
    f = (lambda v: f"{v * 100:+.1f} pts") if pct else (lambda v: f"{v:+.3f}")
    return f"{f(b['mean'])} ({f(b['lo'])} to {f(b['hi'])})"


def report(rule_id: str, df: pd.DataFrame, info: dict, stage: str, pool: str, extra: list[str] | None = None) -> list[str]:
    mod = load_rule(rule_id)
    tf = info["tf"]
    summ = engine.summarize(df, tf) if len(df) else {}
    pm = CFG["primary"]["metric"]
    md = [f"# {stage.title()}: {rule_id} v{mod.SPEC['version']} ({mod.SPEC['name']}) on pool {pool}", "",
          f"_Rule sha256 `{rule_sha(rule_id)[:16]}` · timeframe {tf} · {info['direction']} · {info['symbols']} symbols · "
          f"{len(df)} signals with complete outcomes · entry next open · unit = the rule's 1R distance_", "",
          f"**Your words:** {mod.SPEC['eye_description']}", ""]
    md += extra or []
    md += ["## Process advantage (signal minus matched nulls)", "",
           "| metric | signal | cross null (same day) | time null (same symbol) | advantage vs cross (95%) | advantage vs time (95%) |",
           "|---|---|---|---|---|---|"]
    for nm, v in summ.items():
        pct = nm.startswith("fp")
        val = (lambda z: f"{z:.1%}") if pct else (lambda z: f"{z:+.3f}u")
        md.append(f"| {nm}{' (primary)' if nm == pm else ''} | {val(v['signal'])} | {val(v['cross'])} | {val(v['time'])} | "
                  f"{_fmt(v['adv_cross'], pct)} | {_fmt(v['adv_time'], pct)} |")
    md += ["", "_fp1: reached +1u before -1u within the horizon; fp2: +2u before -1u. fwdh: close h bars later minus entry, in u. "
               "Intervals: bootstrap over calendar months._", ""]
    if len(df):
        md += ["## Where it holds (primary metric, advantage vs cross null)", "", "| slice | n | advantage (95%) |", "|---|---|---|"]
        col = f"{pm}_adv_cross"
        cl = lambda d: pd.to_datetime(d["date"]).dt.to_period("M").astype(str).to_numpy()  # noqa: E731
        sp = engine.halves_split(df)
        slices = [(f"first half (before {sp:%Y-%m})", df[pd.to_datetime(df["date"]) < sp]),
                  (f"second half (from {sp:%Y-%m})", df[pd.to_datetime(df["date"]) >= sp]),
                  ("SPY trend up", df[df["regime_up"]]), ("SPY trend not up", df[~df["regime_up"]]),
                  ("ETFs", df[df["etf"]]), ("stocks", df[~df["etf"]])]
        for name, d in slices:
            b = engine.cluster_boot(d[col].to_numpy(), cl(d)) if len(d) > 1 else {}
            md.append(f"| {name} | {len(d)} | {_fmt(b, True)} |")
        yr = df.groupby("year")[col].agg(["count", "mean"])
        md += ["", "By year: " + " · ".join(f"{y} {r['mean'] * 100:+.0f} ({int(r['count'])})" for y, r in yr.iterrows()), ""]
    return md


def run(rule_id: str, force: bool = False) -> dict:
    mod = load_rule(rule_id)
    if mod.SPEC["status"] == "demo":
        raise PermissionError(f"{rule_id} is a demo rule: self-test only")
    if hasattr(mod, "STUDY"):
        from .study import discovery as study_discovery
        return study_discovery(rule_id, force=force)
    if not passed(rule_id) and not force:
        raise PermissionError(f"{rule_id}: fidelity gate not passed for this rule version; run fidelity first "
                              "(or --force, which the ledger records)")
    sha = rule_sha(rule_id)
    df, info = measure(rule_id, "A", "discovery")
    tf = info["tf"]
    pm = CFG["primary"]["metric"]
    v = ledger.variants_tried(rule_id) + (0 if any(r["rule_sha"] == sha[:16] and r["stage"] == "discovery"
                                                     for r in ledger.rows()) else 1)
    verdict, plan = "NO SIGNALS", {}
    if len(df) > 1:
        pv = engine.primary_verdict(df, tf)
        b = pv["main"]
        nB = len(pool_symbols("B"))
        expect_B = len(df) / max(info["symbols"], 1) * nB
        need = engine.n_needed(b["mean"], b.get("sd", np.nan), b.get("deff", np.nan))
        plan = {"expected_pool_B_signals": round(expect_B), "signals_needed_at_this_effect": None if np.isinf(need) else round(need)}
        if b["lo"] > 0 and need <= expect_B:
            verdict = "PROMISING: advantage clear of zero and pool B is large enough to confirm it"
        elif b["lo"] > 0:
            verdict = "PROMISING BUT SMALL: clear of zero here, pool B is likely too small to confirm it"
        elif b["mean"] > 0:
            verdict = "WEAK: positive but not clear of zero"
        else:
            verdict = "NO ADVANTAGE"
    extra = [f"**Discovery reading: {verdict}** (descriptive; the decision is the confirmation on sealed pool B)", "",
             f"Versions of {rule_id} measured on pool A so far, including this one: **{v}**. "
             "Each extra version tried raises the chance that one looks good by luck; the ledger keeps the count.", ""]
    if plan:
        extra += [f"Planning: pool B should give about {plan['expected_pool_B_signals']} signals; at this effect a "
                  f"confirmation needs about {plan['signals_needed_at_this_effect'] or '∞'}.", ""]
    md = report(rule_id, df, info, "discovery", "A", extra)
    base = outdir("discovery", rule_id, sha[:16])
    (base / "DISCOVERY.md").write_text("\n".join(md) + "\n")
    df.to_csv(base / "signals.csv", index=False)
    meta = {"rule_id": rule_id, "version": mod.SPEC["version"], "rule_sha": sha, "signals": int(len(df)),
            "verdict": verdict, "variants_tried": v, **plan, **info}
    (base / "DISCOVERY.json").write_text(json.dumps(meta, indent=1, default=str))
    ledger.append(stage="discovery", rule_id=rule_id, version=mod.SPEC["version"], rule_sha=sha, pool="A", tf=tf,
                  n_signals=len(df), looked_at=f"all outcomes on pool A ({pm} primary)", result=verdict.split(":")[0],
                  note="FORCED without fidelity gate" if force and not passed(rule_id) else "")
    return meta
