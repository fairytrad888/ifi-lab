"""Step 0 gate: does the Daily RATIO state predict the ratio's forward relative return?

Answered before any ratio rule (R1-R3) is built. Pre-registered (Oct 14, 2026):
  universe  Group S: 11 sector SPDRs / SPY; Group O: SMH, XBI, IWM, RSP, QQQ, GLD, TLT / SPY
  bars      TradingView-style ratio bars: O1/O2, H1/H2, L1/L2, C1/C2 (no volume -> time-weighted anchors)
  states    IFI 2.0 definitions on the ratio, known at the close of day t (no look-ahead)
  outcome   log ratio return from close t to close t+h, minus the average of all ratios that day\n            (peer-relative; removes the shared SPY shock). h = 5, 10, 20; primary = 20
  CI        block bootstrap by 3-calendar-month blocks (all ratios move together inside a block), 2,000 reps
  primary   7 tests, Bonferroni-adjusted 95% (two-sided alpha 0.05/7)

  P1 stage 3 minus stage -1          (expected > 0: trend persistence)
  P2 Trend line rising minus falling (expected > 0)
  P3 HH+HL minus LH+LL structure     (expected > 0)
  P4 above minus below active anchor (expected > 0)
  P5 within 10 bars after a washout exit minus no recent washout (expected > 0: accumulation -> bounce)
  P6 pullback to the Trend line inside a HH+HL uptrend minus all days (expected > 0: R2's foundation)
  P7 cross-sectional rank IC of stage vs forward 20-day return, sampled every 20 days (expected > 0)

  pass      adjusted CI excludes 0 in the expected direction AND same sign in both time halves
            (2000-2014 / 2015-) AND in both groups (S and O)

  python -m research.run --step step0   # lock check, frozen data snapshot, write reports/research/STEP0.md
  python -m research.step0 --synthetic  # pipeline test on random walks (must show no information)
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from ifi import pine as p
from ifi.states import read, _bars_since

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "research"
GROUP_S = ["XLB", "XLC", "XLE", "XLF", "XLI", "XLK", "XLP", "XLRE", "XLU", "XLV", "XLY"]
GROUP_O = ["SMH", "XBI", "IWM", "RSP", "QQQ", "GLD", "TLT"]
BENCH = "SPY"
HORIZONS = (5, 10, 20)
PRIMARY_H = 20
SPLIT = pd.Timestamp("2015-01-01")
START = pd.Timestamp("2000-01-01")
N_PRIMARY = 7
REPS = 2000


# ------------------------------------------------------------------ data
def ratio_bars(a: pd.DataFrame, b: pd.DataFrame) -> pd.DataFrame:
    j = a.index.intersection(b.index)
    a, b = a.loc[j], b.loc[j]
    r = pd.DataFrame({k: a[k] / b[k] for k in ("open", "high", "low", "close")}, index=j)
    r["high"] = r[["open", "high", "low", "close"]].max(axis=1)
    r["low"] = r[["open", "high", "low", "close"]].min(axis=1)
    r["volume"] = 0.0
    return r.replace([np.inf, -np.inf], np.nan).dropna()


def states(r: pd.DataFrame, num_close: pd.Series) -> pd.DataFrame:
    x = read(r)
    out = pd.DataFrame(index=x.index)
    out["stage"] = x["stage"]
    out["line_up"] = x["tr_line_rising"].astype(bool)
    out["above_anchor"] = x["chk2_above_anchor"].astype(bool)
    ph, pl = p.pivot_high(x["high"], 3, 3), p.pivot_low(x["low"], 3, 3)
    last_ph, last_pl = ph.ffill(), pl.ffill()
    prev_ph = ph.dropna().shift(1).reindex(x.index).ffill()
    prev_pl = pl.dropna().shift(1).reindex(x.index).ffill()
    up = (last_ph > prev_ph) & (last_pl > prev_pl)
    dn = (last_ph < prev_ph) & (last_pl < prev_pl)
    out["structure"] = np.select([up, dn], ["up", "down"], "mixed")
    bs_exit = _bars_since(x["ad_washout_exit"])
    out["phase"] = np.select([x["ad_washout"].astype(bool), bs_exit <= 10], ["washout", "post_exit"], "none")
    touch = x["low"] <= x["tr_line"] + 0.25 * x["atr"]
    recent_touch = touch.rolling(3, min_periods=1).max().astype(bool)
    out["pullback_up"] = up & out["line_up"] & recent_touch
    for h in HORIZONS:
        out[f"f{h}"] = np.log(x["close"].shift(-h) / x["close"])
        out[f"n{h}"] = np.log(num_close.reindex(x.index).shift(-h) / num_close.reindex(x.index))
    out = out.iloc[250:]  # indicator warm-up
    return out[out.index >= START]


def build_panel(load_fn) -> pd.DataFrame:
    bench = load_fn(BENCH)
    rows = []
    for g, names in (("S", GROUP_S), ("O", GROUP_O)):
        for s in names:
            a = load_fn(s)
            if a is None or bench is None or len(a) < 600:
                print("skip", s)
                continue
            st = states(ratio_bars(a, bench), a["close"])
            st["ratio"], st["group"] = s, g
            rows.append(st)
    panel = pd.concat(rows)
    panel.index.name = "date"
    panel = panel.reset_index()
    # Every ratio shares SPY in its denominator, so one SPY move shifts all ratios together. Measure each
    # ratio's forward return against the average of the other ratios on the same date (peer-relative), which
    # removes that common shock. Raw values are kept as r{h}; the numerator price (n{h}) stays absolute.
    for h in HORIZONS:
        panel[f"r{h}"] = panel[f"f{h}"]
        panel[f"f{h}"] = panel[f"f{h}"] - panel.groupby("date")[f"f{h}"].transform("mean")
    return panel


# ------------------------------------------------------------------ statistics
BLOCK_MONTHS = 3  # calendar blocks for the bootstrap (prereg stats.block_months; set by research/run.py)


def _block_ids(dates: pd.Series) -> np.ndarray:
    return (dates.dt.year.to_numpy() * 12 + dates.dt.month.to_numpy() - 1) // BLOCK_MONTHS


def boot_diff(df: pd.DataFrame, mask_a: pd.Series, mask_b: pd.Series, col: str, rng) -> dict:
    """Mean(col | A) - Mean(col | B), calendar-block bootstrap across the whole panel."""
    d = df[[col]].copy()
    d["a"], d["b"] = mask_a.to_numpy(), mask_b.to_numpy()
    d = d.dropna(subset=[col])
    d["blk"] = _block_ids(df.loc[d.index, "date"])
    g = d.groupby("blk")
    sa = g.apply(lambda z: z.loc[z["a"], col].sum()).to_numpy()
    na = g["a"].sum().to_numpy()
    sb = g.apply(lambda z: z.loc[z["b"], col].sum()).to_numpy()
    nb = g["b"].sum().to_numpy()
    est = sa.sum() / max(na.sum(), 1) - sb.sum() / max(nb.sum(), 1)
    k = len(sa)
    idx = rng.integers(0, k, size=(REPS, k))
    bs = sa[idx].sum(1) / np.maximum(na[idx].sum(1), 1) - sb[idx].sum(1) / np.maximum(nb[idx].sum(1), 1)
    a2 = 0.05 / N_PRIMARY
    return dict(est=est, n_a=int(na.sum()), n_b=int(nb.sum()),
                lo=float(np.quantile(bs, 0.025)), hi=float(np.quantile(bs, 0.975)),
                lo_adj=float(np.quantile(bs, a2 / 2)), hi_adj=float(np.quantile(bs, 1 - a2 / 2)))


def ic_series(df: pd.DataFrame, col: str, step: int = 20) -> pd.Series:
    days = np.sort(df["date"].unique())[::step]
    sub = df[df["date"].isin(days)].dropna(subset=[col])
    out = {}
    for d, z in sub.groupby("date"):
        if len(z) >= 8 and z["stage"].nunique() > 1:
            out[d] = z["stage"].rank().corr(z[col].rank())
    return pd.Series(out)


def ic_stats(s: pd.Series) -> dict:
    s = s.dropna()
    t = s.mean() / (s.std(ddof=1) / np.sqrt(len(s))) if len(s) > 2 else np.nan
    return dict(ic=float(s.mean()), t=float(t), n=int(len(s)))


TESTS = [
    ("P1", "stage 3 vs stage -1", lambda d: d["stage"] == 3, lambda d: d["stage"] == -1),
    ("P2", "Trend line rising vs falling", lambda d: d["line_up"], lambda d: ~d["line_up"]),
    ("P3", "HH+HL vs LH+LL", lambda d: d["structure"] == "up", lambda d: d["structure"] == "down"),
    ("P4", "above vs below anchor", lambda d: d["above_anchor"], lambda d: ~d["above_anchor"]),
    ("P5", "<=10 bars after washout exit vs no washout", lambda d: d["phase"] == "post_exit", lambda d: d["phase"] == "none"),
    ("P6", "pullback to line in HH+HL uptrend vs all days", lambda d: d["pullback_up"], lambda d: pd.Series(True, index=d.index)),
]


def evaluate(panel: pd.DataFrame, seed: int = 7) -> tuple[pd.DataFrame, dict]:
    rng = np.random.default_rng(seed)
    rows = []
    early, late = panel["date"] < SPLIT, panel["date"] >= SPLIT
    gs, go = panel["group"] == "S", panel["group"] == "O"
    for tid, name, fa, fb in TESTS:
        A, B = fa(panel), fb(panel)
        for h in HORIZONS:
            for kind in ("f", "n"):
                col = f"{kind}{h}"
                full = boot_diff(panel, A, B, col, rng)
                parts = {}
                for lab, m in (("early", early), ("late", late), ("S", gs), ("O", go)):
                    sub = panel[m]
                    parts[lab] = boot_diff(sub, fa(sub), fb(sub), col, rng)["est"]
                rows.append(dict(test=tid, name=name, h=h, measure="ratio" if kind == "f" else "numerator price",
                                 diff_pct=100 * full["est"], ci_lo=100 * full["lo"], ci_hi=100 * full["hi"],
                                 ci_lo_adj=100 * full["lo_adj"], n_a=full["n_a"], n_b=full["n_b"],
                                 early=100 * parts["early"], late=100 * parts["late"],
                                 S=100 * parts["S"], O=100 * parts["O"]))
    res = pd.DataFrame(rows)
    res["pass_"] = (res["ci_lo_adj"] > 0) & (res["early"] > 0) & (res["late"] > 0) & (res["S"] > 0) & (res["O"] > 0)
    res["opposite"] = (res["ci_hi"] < 0) & (res["early"] < 0) & (res["late"] < 0)
    ic = {}
    for lab, m in (("all", slice(None)), ("early", panel["date"] < SPLIT), ("late", panel["date"] >= SPLIT)):
        ic[lab] = ic_stats(ic_series(panel[m] if lab != "all" else panel, f"f{PRIMARY_H}"))
    from scipy.stats import norm
    crit = norm.ppf(1 - 0.05 / N_PRIMARY / 2)
    ic["pass"] = bool(ic["all"]["t"] > crit and ic["early"]["ic"] > 0 and ic["late"]["ic"] > 0)
    ic["crit_t"] = float(crit)
    return res, ic


def decide(res: pd.DataFrame, ic: dict) -> list[str]:
    prim = res[(res["h"] == PRIMARY_H) & (res["measure"] == "ratio")].set_index("test")
    trend = [t for t in ("P1", "P2", "P3", "P4") if prim.loc[t, "pass_"]]
    lines = []
    lines.append(f"- Trend-state information (P1-P4): {'YES: ' + ', '.join(trend) if trend else 'NO'}")
    lines.append(f"- Accumulation-bounce information (P5): {'YES' if prim.loc['P5', 'pass_'] else 'NO'}")
    lines.append(f"- Pullback-in-uptrend information (P6): {'YES' if prim.loc['P6', 'pass_'] else 'NO'}")
    lines.append(f"- Cross-sectional ranking (P7 IC): {'YES' if ic['pass'] else 'NO'} "
                 f"(IC {ic['all']['ic']:+.3f}, t {ic['all']['t']:.2f}, needs > {ic['crit_t']:.2f})")
    nxt = []
    if trend or prim.loc["P6", "pass_"]:
        nxt.append("Step 1 starts with R2 (trend continuation / pullback support)")
    if prim.loc["P5", "pass_"]:
        nxt.append("R1 and R3 (accumulation / 9-count reversals) are built")
    else:
        nxt.append("R1 and R3 are NOT built yet (no accumulation-bounce information); they stay as chart context")
    if ic["pass"]:
        nxt.append("the ratio stage enters the alignment score as a ranking input")
    if not (trend or prim.loc["P6", "pass_"] or prim.loc["P5", "pass_"] or ic["pass"]):
        nxt = ["STOP: Daily ratio states carry no measurable information at 5-20 days. Ratio rules are not built; "
               "ratios remain context. Effort moves to E4 on prices, exits/allocation, and the forecast ledger."]
    return lines + ["", "**Decision:** " + "; ".join(nxt) + "."]


def current_states(panel_full: pd.DataFrame) -> pd.DataFrame:
    last = panel_full.sort_values("date").groupby("ratio").tail(1)
    return last[["ratio", "group", "date", "stage", "line_up", "structure", "above_anchor", "phase", "pullback_up"]]


def report(res: pd.DataFrame, ic: dict, cur: pd.DataFrame, panel: pd.DataFrame, title: str) -> str:
    fmt = lambda v: f"{v:+.2f}"
    md = [f"# {title}", "",
          f"_{panel['ratio'].nunique()} ratios · {panel['date'].min():%Y-%m-%d} to {panel['date'].max():%Y-%m-%d} · "
          f"{len(panel):,} ratio-days · {BLOCK_MONTHS}-month block bootstrap, Bonferroni k={N_PRIMARY}_", "",
          "## Gate", ""] + decide(res, ic) + ["", "## Primary results (h = 20 bars, ratio, % difference in forward return)", "",
          "| test | comparison | diff % | 95% CI | adj. CI low | n (A / B) | 2000-14 | 2015- | sectors | others | pass |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    prim = res[(res["h"] == PRIMARY_H) & (res["measure"] == "ratio")]
    for r in prim.itertuples():
        md.append(f"| {r.test} | {r.name} | {fmt(r.diff_pct)} | {fmt(r.ci_lo)} … {fmt(r.ci_hi)} | {fmt(r.ci_lo_adj)} | "
                  f"{r.n_a:,} / {r.n_b:,} | {fmt(r.early)} | {fmt(r.late)} | {fmt(r.S)} | {fmt(r.O)} | "
                  f"{'PASS' if r.pass_ else ('opposite' if r.opposite else '–')} |")
    md += ["", f"P7 rank IC (stage vs 20-bar forward return): all {ic['all']['ic']:+.3f} (t {ic['all']['t']:.2f}, "
           f"{ic['all']['n']} dates) · 2000-14 {ic['early']['ic']:+.3f} · 2015- {ic['late']['ic']:+.3f} · "
           f"{'PASS' if ic['pass'] else 'no pass'}", "",
           "## All horizons and the tradeable version (numerator ETF price, same dates)", "",
           "| test | h | measure | diff % | 95% CI | pass |", "|---|---|---|---|---|---|"]
    for r in res.itertuples():
        md.append(f"| {r.test} | {r.h} | {r.measure} | {fmt(r.diff_pct)} | {fmt(r.ci_lo)} … {fmt(r.ci_hi)} | "
                  f"{'PASS' if r.pass_ else '–'} |")
    md += ["", "## Current ratio states (last completed bar)", "",
           "| ratio | group | date | stage | line | structure | anchor | phase | pullback in uptrend |",
           "|---|---|---|---|---|---|---|---|---|"]
    for r in cur.itertuples():
        md.append(f"| {r.ratio}/SPY | {r.group} | {r.date:%Y-%m-%d} | {r.stage} | {'▲' if r.line_up else '▼'} | "
                  f"{r.structure} | {'above' if r.above_anchor else 'below'} | {r.phase} | {'yes' if r.pullback_up else ''} |")
    return "\n".join(md) + "\n"


def gate(res: pd.DataFrame, ic: dict) -> dict:
    """Machine-readable Step 0 result for the Step 1 gate (primary: h = 20, ratio)."""
    prim = res[(res["h"] == PRIMARY_H) & (res["measure"] == "ratio")].set_index("test")
    passed = {t: bool(prim.loc[t, "pass_"]) for t in prim.index}
    passed["P7"] = bool(ic["pass"])
    return dict(passed=passed, stop=not any(passed.values()))


def run(load_fn, title: str, out_name: str, gate_name: str | None = None) -> tuple[pd.DataFrame, dict]:
    panel = build_panel(load_fn)
    cur = current_states(panel)
    ev = panel.dropna(subset=[f"f{PRIMARY_H}"])
    res, ic = evaluate(ev)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / out_name).write_text(report(res, ic, cur, ev, title))
    res.to_csv(OUT / out_name.replace(".md", ".csv"), index=False)
    if gate_name:
        import json
        (OUT / gate_name).write_text(json.dumps(gate(res, ic), indent=1))
    print((OUT / out_name).read_text()[:2500])
    return res, ic


def _synthetic_loader(seed=3):
    rng = np.random.default_rng(seed)
    days = pd.bdate_range("1998-01-01", "2026-10-09")
    cache = {}

    def f(sym):
        if sym not in cache:
            c = 100 * np.exp(np.cumsum(rng.normal(0.0003, 0.012, len(days))))
            o = c * np.exp(rng.normal(0, 0.003, len(c)))
            hi = np.maximum(o, c) * np.exp(np.abs(rng.normal(0, 0.006, len(c))))
            lo = np.minimum(o, c) * np.exp(-np.abs(rng.normal(0, 0.006, len(c))))
            cache[sym] = pd.DataFrame({"open": o, "high": hi, "low": lo, "close": c, "volume": 1e6}, index=days)
        return cache[sym]
    return f


if __name__ == "__main__":
    # Normally run through research/run.py (lock check, frozen snapshot, Step 1 gate). Direct use:
    ap = argparse.ArgumentParser()
    ap.add_argument("--synthetic", action="store_true")
    a = ap.parse_args()
    if a.synthetic:
        run(_synthetic_loader(), "Step 0 pipeline check on random walks (should show NO information)", "STEP0_synthetic.md")
    else:
        from research.common import load_snapshot
        run(load_snapshot, "Step 0: does the Daily ratio state carry information?", "STEP0.md", "STEP0_gate.json")
