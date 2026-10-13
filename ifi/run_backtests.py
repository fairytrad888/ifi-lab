"""Run the pre-registered experiment queue and write reports/SUMMARY.md.

Priority order (pre-identified):
  P1  Exits & sizing     : every setup x every exit rule, vs a random-entry control
  P2  Market regime      : do setups improve when SPY is in an uptrend?
  P3  Earnings drift     : positive earnings gaps alone, and IFI setups after them (stocks)
  P4  Portfolio heat     : does capping one position per sector reduce drawdown?

Usage:  python -m ifi.run_backtests [--tf daily|h4] [--universe etfs|stocks|all] [--quick]
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from . import backtest as bt
from .data import load, ROOT
from .states import read, _bars_since

REPORTS = ROOT / "reports"
RESULTS = REPORTS / "results"


def cfg() -> dict:
    return yaml.safe_load((ROOT / "config.yaml").read_text())


def universe(c: dict, which: str) -> tuple[list[str], dict[str, str]]:
    sector_of = {}
    stocks = []
    for sec, names in c["stocks"].items():
        for s in names:
            stocks.append(s)
            sector_of[s] = sec
    for e in c["etfs"]:
        sector_of.setdefault(e, e)
    syms = {"etfs": c["etfs"], "stocks": stocks, "all": c["etfs"] + stocks}[which]
    return syms, sector_of


def load_reads(syms: list[str], tf: str, bench_sym: str, start: str) -> tuple[dict[str, pd.DataFrame], pd.DataFrame | None]:
    bench = load(bench_sym, tf)
    out = {}
    for s in syms:
        df = load(s, tf)
        if df is None or len(df) < 400:
            continue
        x = read(df, bench)
        x = x[x.index >= start]
        if len(x) > 300:
            out[s] = x
    bx = read(bench, None) if bench is not None else None
    return out, bx


def run_combo(reads, setup_fn, exit_rule, cost_of):
    trades = []
    for s, x in reads.items():
        ent = setup_fn(s, x)
        trades += bt.simulate(s, x, ent, getattr(setup_fn, "label", "custom"), exit_rule, cost_of(s))
    return pd.DataFrame([t.__dict__ for t in trades])


def summarize(df: pd.DataFrame, split_date: str, sym_half: set, n_tests: int, rand_ref=None, min_trades=100) -> dict:
    if df.empty:
        return dict(n=0, verdict="INCONCLUSIVE (no trades)")
    r = df["r"].to_numpy()
    m = bt.metrics(r)
    adj = bt.metrics(r, alpha=0.05 / max(n_tests, 1))
    m["ci_low_adj"] = adj["ci_low"]
    halves = [
        bt.metrics(df.loc[df.entry_date < split_date, "r"].to_numpy()),
        bt.metrics(df.loc[df.entry_date >= split_date, "r"].to_numpy()),
        bt.metrics(df.loc[df.symbol.isin(sym_half), "r"].to_numpy()),
        bt.metrics(df.loc[~df.symbol.isin(sym_half), "r"].to_numpy()),
    ]
    m["exp_early"], m["exp_late"], m["exp_symA"], m["exp_symB"] = [h.get("expectancy", np.nan) for h in halves]
    m["avg_bars"] = df["bars"].mean()
    ref = None
    if rand_ref is not None and len(rand_ref.get("pool", [])):
        rng = np.random.default_rng(11)
        pool = rand_ref["pool"]
        ref = {"p95": float(np.quantile(rng.choice(pool, size=(1000, len(r))).mean(axis=1), 0.95))}
        m["random_p95"] = ref["p95"]
    m["verdict"] = bt.verdict(m, halves, ref, n_tests, min_trades)
    return m


def fmt_table(rows: list[dict], cols: list[str]) -> str:
    def f(v):
        if isinstance(v, float):
            if np.isnan(v):
                return "–"
            return f"{v:.3f}" if abs(v) < 100 else f"{v:,.0f}"
        return str(v)
    head = "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n"
    return head + "\n".join("| " + " | ".join(f(r.get(c, "")) for c in cols) + " |" for r in rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tf", default="daily")
    ap.add_argument("--universe", default="etfs")
    ap.add_argument("--quick", action="store_true", help="fewer random seeds / bootstrap for a fast smoke run")
    a = ap.parse_args()
    c = cfg()
    T = c["testing"]
    RESULTS.mkdir(parents=True, exist_ok=True)
    syms, sector_of = universe(c, a.universe)
    reads, bx = load_reads(syms, a.tf, c["benchmark"], T["start"])
    if not reads:
        raise SystemExit("No data found. Run: python -m ifi.update_data")
    etfset = set(c["etfs"])
    cost_of = lambda s: c["costs"]["etf"] if s in etfset else c["costs"]["stock"]
    ordered = sorted(reads)
    sym_half = set(ordered[::2])
    split = T["split_date"] if a.tf == "daily" else str(pd.Timestamp(min(x.index[0] for x in reads.values())) +
                                                          (pd.Timestamp(max(x.index[-1] for x in reads.values())) -
                                                           pd.Timestamp(min(x.index[0] for x in reads.values()))) / 2)[:10]
    min_tr = T["min_trades"] if a.tf == "daily" else 50
    seeds = 2 if a.quick else T["random_seeds"]
    exits = list(bt.EXITS)
    setup_names = list(bt.setups(next(iter(reads.values()))).keys())
    n_tests = len(exits) * len(setup_names)
    lines = [f"# IFI Lab results: {a.tf} · {a.universe}",
             f"_Run {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC} · {len(reads)} symbols · "
             f"{min(x.index[0] for x in reads.values()):%Y-%m-%d} to {max(x.index[-1] for x in reads.values()):%Y-%m-%d} · "
             f"split {split} · {n_tests} setup×exit tests (Bonferroni-adjusted) · engine v1.3.1_", ""]
    if a.universe in ("stocks", "all"):
        lines += ["> **Survivorship bias:** this stock list was chosen in 2026 from today's large caps, so random long entries "
                  "earn money too. Judge stock setups by their edge over the random-entry control, not by raw expectancy.", ""]

    # ---------------- P1 random-entry control per exit (pooled across seeds)
    rand_pool = {}
    for ex in exits:
        rs = []
        for sd in range(seeds):
            def fn(s, x, sd=sd):
                return bt.random_setup(x, T["random_rate"], seed=abs(hash((s, sd))) % 2**32)
            fn.label = "random"
            d = run_combo(reads, fn, ex, cost_of)
            if not d.empty:
                rs.append(d["r"].to_numpy())
        rand_pool[ex] = np.concatenate(rs) if rs else np.array([])
    rand_ref = {ex: dict(mean=float(v.mean()) if len(v) else np.nan, pool=v) for ex, v in rand_pool.items()}
    # ---------------- P1 setups x exits
    p1_rows = []
    all_trades = []
    cache = {s: bt.setups(x) for s, x in reads.items()}
    for su in setup_names:
        for ex in exits:
            def fn(s, x, su=su):
                return cache[s][su]
            fn.label = su
            d = run_combo(reads, fn, ex, cost_of)
            if not d.empty:
                all_trades.append(d)
            m = summarize(d, split, sym_half, n_tests, rand_ref[ex], min_tr)
            p1_rows.append(dict(setup=su, exit=ex, **m, random_mean=rand_ref[ex]["mean"]))
    p1 = pd.DataFrame(p1_rows)
    p1.to_csv(RESULTS / f"P1_{a.tf}_{a.universe}.csv", index=False)
    if all_trades:
        pd.concat(all_trades).to_csv(RESULTS / f"trades_{a.tf}_{a.universe}.csv.gz", index=False, compression="gzip")
    top = p1.sort_values("expectancy", ascending=False)
    lines += ["## P1 · Exits × setups (R per trade, after costs)", "",
              "Random-entry control (same stops and exits), mean expectancy by exit: " +
              ", ".join(f"{k} {v['mean']:+.3f}R" for k, v in rand_ref.items()), "",
              fmt_table(top.to_dict("records"), ["setup", "exit", "n", "win_rate", "avg_win", "avg_loss", "expectancy", "median", "exp_w10",
                                                 "ci_low", "ci_low_adj", "exp_early", "exp_late", "exp_symA", "exp_symB",
                                                 "random_mean", "random_p95", "avg_bars", "verdict"]), ""]
    # exit ranking averaged across setups (what exits contribute regardless of entry)
    ex_rank = p1.groupby("exit").apply(lambda g: pd.Series({
        "mean_expectancy": np.average(g["expectancy"], weights=g["n"]) if g["n"].sum() else np.nan,
        "random_mean": rand_ref[g.name]["mean"], "trades": g["n"].sum()}), include_groups=False).reset_index()
    ex_rank["edge_over_random"] = ex_rank["mean_expectancy"] - ex_rank["random_mean"]
    lines += ["### Exit rules ranked (trade-weighted across setups)", "",
              fmt_table(ex_rank.sort_values("mean_expectancy", ascending=False).to_dict("records"),
                        ["exit", "trades", "mean_expectancy", "random_mean", "edge_over_random"]), ""]

    # ---------------- P1b sizing for the best 3 combos with enough trades
    best = top[top["n"] >= min_tr].head(3)
    trades_all = pd.concat(all_trades) if all_trades else pd.DataFrame()
    size_rows = []
    for _, b in best.iterrows():
        d = trades_all[(trades_all.setup == b.setup) & (trades_all.exit_rule == b.exit)]
        for rp in (0.005, 0.01, 0.02):
            pm = bt.portfolio(d, rp, c["risk"]["max_open"])
            size_rows.append(dict(setup=b.setup, exit=b.exit, **pm))
    if size_rows:
        lines += ["## P1b · Sizing (fixed-fractional, max open positions = %d)" % c["risk"]["max_open"], "",
                  fmt_table(size_rows, ["setup", "exit", "risk_pct", "cagr", "max_dd", "mar", "final"]), ""]

    # ---------------- P2 regime filter (SPY above 200-day SMA and its Trend line rising)
    if bx is not None:
        regime = ((bx["close"] > bx["close"].rolling(200).mean()) & bx["tr_line_rising"]).astype(bool)
        p2_rows = []
        for su in setup_names:
            for ex in ("X4_trendline_trail", "X5_chandelier3atr"):
                d = trades_all[(trades_all.setup == su) & (trades_all.exit_rule == ex)] if not trades_all.empty else pd.DataFrame()
                if d.empty:
                    continue
                on = d["entry_date"].map(lambda t: bool(regime.asof(t)) if t >= regime.index[0] else False)
                m_on, m_off = bt.metrics(d.loc[on, "r"].to_numpy()), bt.metrics(d.loc[~on, "r"].to_numpy())
                rng = np.random.default_rng(3)
                ron, roff = d.loc[on, "r"].to_numpy(), d.loc[~on, "r"].to_numpy()
                diff_lo = np.nan
                if len(ron) > 5 and len(roff) > 5:
                    diffs = [rng.choice(ron, len(ron)).mean() - rng.choice(roff, len(roff)).mean() for _ in range(2000)]
                    diff_lo = float(np.quantile(diffs, 0.05 / (2 * len(setup_names) * 2)))  # Bonferroni over P2 rows
                p2_rows.append(dict(setup=su, exit=ex, n_on=m_on.get("n", 0), exp_on=m_on.get("expectancy", np.nan),
                                    n_off=m_off.get("n", 0), exp_off=m_off.get("expectancy", np.nan),
                                    diff=(m_on.get("expectancy", np.nan) - m_off.get("expectancy", np.nan)),
                                    diff_ci_low=diff_lo,
                                    verdict="FILTER HELPS" if diff_lo > 0 else ("NO CLEAR EFFECT" if not np.isnan(diff_lo) else "TOO FEW")))
        pd.DataFrame(p2_rows).to_csv(RESULTS / f"P2_{a.tf}_{a.universe}.csv", index=False)
        lines += ["## P2 · Market regime (SPY > 200-day average and Trend line rising)", "",
                  fmt_table(p2_rows, ["setup", "exit", "n_on", "exp_on", "n_off", "exp_off", "diff", "diff_ci_low", "verdict"]), ""]

    # ---------------- P3 earnings drift (stocks with earnings files)
    edir = ROOT / "data" / "earnings"
    p3_rows = []
    if edir.exists() and a.tf == "daily":
        gap_trades, after, other = [], [], []
        for s, x in reads.items():
            f = edir / f"{s}.csv"
            if not f.exists():
                continue
            e = pd.read_csv(f, index_col=0, parse_dates=True)
            sp = "surprisepct" if "surprisepct" in e else next((k for k in e.columns if "surprise" in k), None)
            if sp is None:
                continue
            gap = x["open"] / x["close"].shift(1) - 1
            react = pd.Series(False, index=x.index)
            for d0, row in e.iterrows():
                if pd.isna(row[sp]) or row[sp] <= 0:
                    continue
                win = x.index[(x.index >= d0)][:2]
                if len(win) == 0:
                    continue
                dd = max(win, key=lambda d: abs(gap.get(d, 0)))
                if gap.get(dd, 0) > 0.02 and x.at[dd, "close"] > x.at[dd, "open"]:
                    react.at[dd] = True
            # (a) drift: buy the reaction-day close, hold 20 bars, % return and vs SPY
            b = bx["close"].reindex(x.index).ffill() if bx is not None else None
            for d in react[react].index:
                i = x.index.get_loc(d)
                if i + 20 < len(x):
                    ret = x["close"].iloc[i + 20] / x["close"].iloc[i] - 1
                    rel = ret - (b.iloc[i + 20] / b.iloc[i] - 1) if b is not None else np.nan
                    gap_trades.append(dict(symbol=s, date=d, ret20=ret, rel20=rel))
            # (b) IFI setups within 20 bars after a positive reaction vs other times (X4 exit)
            near = _bars_since(react) <= 20
            if not trades_all.empty:
                d = trades_all[(trades_all.symbol == s) & (trades_all.exit_rule == "X4_trendline_trail")]
                for _, t in d.iterrows():
                    sig_day = x.index[max(x.index.get_loc(t.entry_date) - 1, 0)]
                    (after if bool(near.get(sig_day, False)) else other).append(t.r)
        g = pd.DataFrame(gap_trades)
        if not g.empty:
            g.to_csv(RESULTS / "P3_earnings_gaps.csv", index=False)
            p3_rows.append(dict(test="Positive earnings gap → hold 20 bars", n=len(g),
                                mean=g["ret20"].mean(), mean_vs_spy=g["rel20"].mean(),
                                hit_vs_spy=(g["rel20"] > 0).mean()))
        ma, mo = bt.metrics(np.array(after)), bt.metrics(np.array(other))
        if ma.get("n", 0):
            p3_rows.append(dict(test="IFI setups ≤20 bars after positive gap (R, X4)", n=ma["n"], mean=ma["expectancy"],
                                ci_low=ma["ci_low"]))
        if mo.get("n", 0):
            p3_rows.append(dict(test="Same setups at other times (R, X4)", n=mo["n"], mean=mo["expectancy"], ci_low=mo["ci_low"]))
        if p3_rows:
            lines += ["## P3 · Earnings drift (stocks)", "",
                      fmt_table(p3_rows, ["test", "n", "mean", "mean_vs_spy", "hit_vs_spy", "ci_low"]), ""]

    # ---------------- P4 portfolio heat (one open position per sector vs unlimited)
    if len(best):
        b = best.iloc[0]
        d = trades_all[(trades_all.setup == b.setup) & (trades_all.exit_rule == b.exit)].sort_values("entry_date")
        free = bt.portfolio(d, c["risk"]["risk_per_trade"], c["risk"]["max_open"])
        kept, open_until = [], {}
        for _, t in d.iterrows():
            sec = sector_of.get(t.symbol, t.symbol)
            if open_until.get(sec, pd.Timestamp.min) > t.entry_date:
                continue
            kept.append(t)
            open_until[sec] = t.exit_date
        capped = bt.portfolio(pd.DataFrame(kept), c["risk"]["risk_per_trade"], c["risk"]["max_open"]) if kept else {}
        lines += [f"## P4 · Portfolio heat ({b.setup} + {b.exit})", "",
                  fmt_table([dict(rule="No sector cap", **free), dict(rule="Max 1 open per sector", **capped)],
                            ["rule", "cagr", "max_dd", "mar", "final"]), ""]

    # ---------------- P6 playbook portfolio (adopted setups, one exit, one position per symbol, sector cap)
    pb = c.get("playbook", {})
    tgt = f"X{2 if pb.get('target_r', 3) == 2 else 3}_target{pb.get('target_r', 3)}R"
    if pb.get("setups") and not trades_all.empty:
        d = trades_all[trades_all.setup.isin(pb["setups"]) & (trades_all.exit_rule == tgt)].sort_values("entry_date")
        kept, busy_sym, busy_sec = [], {}, {}
        for _, t in d.iterrows():
            sec = sector_of.get(t.symbol, t.symbol)
            if busy_sym.get(t.symbol, pd.Timestamp.min) > t.entry_date or busy_sec.get(sec, pd.Timestamp.min) > t.entry_date:
                continue
            kept.append(t)
            busy_sym[t.symbol] = busy_sec[sec] = t.exit_date
        k = pd.DataFrame(kept)
        if not k.empty:
            rr = k["r"].to_numpy()
            streak = cur = 0
            for v in rr:
                cur = cur + 1 if v <= 0 else 0
                streak = max(streak, cur)
            years = (k.exit_date.max() - k.entry_date.min()).days / 365.25
            rows6 = []
            for rp in (0.005, 0.0075, 0.01):
                pm = bt.portfolio(k, rp, c["risk"]["max_open"])
                rows6.append(dict(risk=f"{rp:.2%}", trades=len(k), trades_per_year=len(k) / max(years, 1e-9),
                                  expectancy=rr.mean(), win_rate=(rr > 0).mean(), longest_losing_streak=streak, **(pm or {"risk_pct": rp})))
            lines += [f"## P6 · Playbook portfolio ({' + '.join(pb['setups'])}, exit {tgt}, 1 per symbol, 1 per sector, max {c['risk']['max_open']} open)", "",
                      fmt_table(rows6, ["risk", "trades", "trades_per_year", "expectancy", "win_rate", "longest_losing_streak",
                                        "cagr", "max_dd", "mar", "final"]), ""]
            k.to_csv(RESULTS / f"P6_playbook_{a.tf}_{a.universe}.csv", index=False)

    # ---------------- E6 earnings: playbook E4 within 20 bars after a positive earnings gap vs other times (stocks)
    if edir.exists() and a.tf == "daily" and not trades_all.empty:
        near_r, other_r = [], []
        d = trades_all[(trades_all.setup == "E4_anchor_reclaim") & (trades_all.exit_rule == tgt)]
        for s, x in reads.items():
            f = edir / f"{s}.csv"
            if not f.exists():
                continue
            e = pd.read_csv(f, index_col=0, parse_dates=True)
            sp = next((k for k in e.columns if "surprise" in k), None)
            if sp is None:
                continue
            gap = x["open"] / x["close"].shift(1) - 1
            react = pd.Series(False, index=x.index)
            for d0, row in e.iterrows():
                if pd.isna(row[sp]) or row[sp] <= 0:
                    continue
                win = x.index[x.index >= d0][:2]
                if len(win):
                    dd = max(win, key=lambda q: abs(gap.get(q, 0)))
                    if gap.get(dd, 0) > 0.02 and x.at[dd, "close"] > x.at[dd, "open"]:
                        react.at[dd] = True
            near = _bars_since(react) <= 20
            for _, t in d[d.symbol == s].iterrows():
                i = x.index.get_loc(t.entry_date)
                (near_r if bool(near.iloc[max(i - 1, 0)]) else other_r).append(t.r)
        if len(near_r) > 5 and len(other_r) > 5:
            rng = np.random.default_rng(5)
            a_, b_ = np.array(near_r), np.array(other_r)
            diffs = [rng.choice(a_, len(a_)).mean() - rng.choice(b_, len(b_)).mean() for _ in range(2000)]
            lo = float(np.quantile(diffs, 0.025))
            lines += ["## E6 · Playbook E4 after a positive earnings gap (stocks)", "",
                      fmt_table([dict(group="E4 ≤20 bars after positive gap", n=len(a_), expectancy=a_.mean()),
                                 dict(group="E4 at other times", n=len(b_), expectancy=b_.mean()),
                                 dict(group="Difference (95% CI low)", n=len(a_) + len(b_), expectancy=a_.mean() - b_.mean(), ci_low=lo,
                                      verdict="EARNINGS CONTEXT HELPS" if lo > 0 else "NO CLEAR EFFECT")],
                                ["group", "n", "expectancy", "ci_low", "verdict"]), ""]

    lines += ["---", "**How to read verdicts.** ADOPT = ≥ min trades, bootstrap CI above 0 after correcting for the number of tests, "
              "positive in both time halves and both symbol halves, and better than random entries with the same exits. "
              "PROMISING = everything except significance. UNSTABLE = fails a half. REJECT = not positive or not better than random."]
    out = REPORTS / f"SUMMARY_{a.tf}_{a.universe}.md"
    out.write_text("\n".join(lines))
    (REPORTS / "latest.json").write_text(json.dumps({"tf": a.tf, "universe": a.universe, "file": out.name,
                                                      "run": datetime.now(timezone.utc).isoformat()}))
    print(out.read_text()[:3000])


if __name__ == "__main__":
    main()
