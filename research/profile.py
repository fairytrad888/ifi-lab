"""E4 profile (Path A): a DESCRIPTIVE report of the proven edge, E4 entry + X3 exit (3R target, 60 bars).

No rule is tested and nothing here changes the playbook. Every slice is a measurement of the past; a pattern
seen here is a hypothesis for a future pre-registered test (preferably confirmed on the live paper log).

Data: the frozen exit-test snapshot (research/exits/snapshot: 17 ETFs + 61 stocks, Yahoo, with dividends).
Trades: the Lab's exact sequencing (one open trade per symbol), simulated with research/exits/sim.py, whose
X3 reproduces ifi/backtest.py trade for trade.

  python -m research.profile          (or Actions -> Research -> step = profile)
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from ifi import backtest as bt
from ifi.allocation import tags
from research import engine as E
from research.exits import data as D
from research.exits import run as XR
from research.exits import sim as S

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "profile"
RISKS = (0.005, 0.0075, 0.01)


def mfe_mae(A: dict, e: int, j: int, fill: float, risk: float) -> tuple[float, float]:
    hi, lo = np.max(A["h"][e:j + 1]), np.min(A["l"][e:j + 1])
    return (hi - fill) / risk, (lo - fill) / risk


def build(cfg: dict) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    U = cfg["universe"]
    P = XR.engine_params(cfg)
    X = {"X3": XR.exit_defs(cfg)["X3"]}   # only X3: trades need 60 bars, so entries run to the data end
    rows, rnd_rows, frames = [], [], {}
    for uni, syms, cost in (("ETF", U["etfs"], cfg["params"]["cost_etf"]), ("stock", U["stocks"], cfg["params"]["cost_stock"])):
        F = XR.load_frames(D.load, syms, U["min_bars"])
        frames.update(F)
        spy = F.get("SPY") if "SPY" in F else frames.get("SPY")
        XR.FRAMES_INDEX.update({s: x.index for s, x in F.items()})
        cache = {}
        tr = XR.run_universe(F, cfg, P, X, cost, kinds=["X3"], events_cache=cache, path=True)
        seq = S.no_overlap(tr) if len(tr) else tr
        for r in seq.itertuples():
            x = F[r.sym]
            ev = cache[(r.sym, P["piv"], P["tol"], P["xb_warn"], P["xb_win"], P["ext_up"], P["flat"])]
            A = S.arrays(x, ev)
            fill = A["o"][r.e]
            stop = A["low5"][r.t] - 0.5 * A["atr"][r.t]
            risk = fill - stop
            mfe, mae = mfe_mae(A, r.e, r.exit_i, fill, risk)
            tg = tags(x, int(r.t), r.sym, dict(spy=spy))
            rows.append(dict(universe=uni, sym=r.sym, date=r.date, entry_date=r.entry_date, exit_date=r.exit_date,
                             r=r.r, rt=r.rt, bars=r.bars, why=r.why, risk_pct=risk / fill, mfe=mfe, mae=mae, e=r.e,
                             exit_i=r.exit_i, path=r.path, t=r.t, **tg))
        rnd = XR.run_universe(F, cfg, P, X, cost, kinds=["X3"], random_seeds=cfg["params"]["random_seeds"], events_cache=cache)
        if len(rnd):
            # same Lab sequencing as E4 (one open trade per symbol), applied within each random seed
            rnd = pd.concat([S.no_overlap(g) for _, g in rnd.groupby("seed")]) if "seed" in rnd else S.no_overlap(rnd)
            rnd_rows.append(rnd.assign(universe=uni))
    T = pd.DataFrame(rows)
    T["kind"] = "X3"
    R = pd.concat(rnd_rows) if rnd_rows else pd.DataFrame()
    return T, R, frames


def longest_streak(r: np.ndarray) -> int:
    best = cur = 0
    for v in r:
        cur = cur + 1 if v <= 0 else 0
        best = max(best, cur)
    return best


def boot_streak(r: np.ndarray, window: int = 100, reps: int = 4000, seed: int = 7) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    s = [longest_streak(rng.choice(r, window)) for _ in range(reps)]
    return float(np.quantile(s, 0.95)), float(np.quantile(s, 0.99))


def underwater_days(cv: pd.Series) -> int:
    peak = cv.cummax()
    under = cv < peak
    best = cur = 0
    last = None
    for d, u in under.items():
        if u:
            cur = cur + ((d - last).days if last is not None else 0)
            best = max(best, cur)
        else:
            cur = 0
        last = d
    return int(best)


def portfolio_rows(T: pd.DataFrame, cfg: dict) -> list[dict]:
    out = []
    for rp in RISKS:
        c2 = dict(cfg, params=dict(cfg["params"], risk_pct=rp))
        pf = XR.portfolio(T.assign(kind="X3"), "X3", c2)
        out.append(dict(risk=f"{100 * rp:.2f}%", **pf))
    return out


def fmt(v, d=3, pct=False):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "–"
    return f"{100 * v:.{d}f}%" if pct else f"{v:+.{d}f}" if isinstance(v, float) else str(v)


PCT_COLS = {"win", "width"}


def table(df: pd.DataFrame, cols: list[str], heads: list[str]) -> list[str]:
    md = ["| " + " | ".join(heads) + " |", "|" + "---|" * len(heads)]
    for r in df[cols].itertuples(index=False):
        cells = []
        for col, x in zip(cols, r):
            if isinstance(x, str):
                cells.append(x)
            elif isinstance(x, (int, np.integer)):
                cells.append(f"{x:,}")
            elif col in PCT_COLS:
                cells.append(f"{100 * float(x):.1f}%")
            else:
                cells.append(fmt(float(x), 3))
        md.append("| " + " | ".join(cells) + " |")
    return md


def summary(g: pd.DataFrame) -> dict:
    r = g["rt"].to_numpy(float)
    w, l_ = r[r > 0], r[r <= 0]
    return dict(n=len(r), mean=float(r.mean()) if len(r) else np.nan, mean_price=float(g["r"].mean()) if len(r) else np.nan,
                win=float((r > 0).mean()) if len(r) else np.nan, avg_win=float(w.mean()) if len(w) else np.nan,
                avg_loss=float(l_.mean()) if len(l_) else np.nan, median=float(np.median(r)) if len(r) else np.nan,
                pf=float(w.sum() / -l_.sum()) if l_.sum() < 0 else np.nan)


def slice_table(T: pd.DataFrame, col: str, bins=None, labels=None) -> pd.DataFrame:
    v = T[col]
    if bins is not None:
        v = pd.cut(v, bins=bins, labels=labels, include_lowest=True)
    g = T.assign(_k=v).dropna(subset=["_k"]).groupby("_k", observed=True)
    return pd.DataFrame([dict(group=str(k), **summary(d)) for k, d in g])


def report(T: pd.DataFrame, R: pd.DataFrame, cfg: dict, meta: dict) -> str:
    md = ["# E4 profile: the proven edge, measured (descriptive only)", "",
          f"_Run {meta['run_utc']} · snapshot cutoff {meta['cutoff']} (manifest `{meta['manifest'][:16]}`) · E4 entry + X3 exit "
          "(3R target, 60 bars) · Lab sequencing (one open trade per symbol) · R includes dividends unless marked price-only_", "",
          "**Nothing here is a test.** Every split below is a description of the past. A pattern worth acting on becomes a "
          "pre-registered hypothesis, ideally confirmed on the live paper log first. With dozens of slices, some will look "
          "different by chance alone.", ""]
    # 1 headline
    md += ["## 1. Headline", "",
           "| universe | trades | trades/yr | mean R | mean R (price only) | win % | avg win | avg loss | median R | profit factor | random-entry mean R (same exit) | E4 minus random |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for uni in ("ETF", "stock"):
        g = T[T["universe"] == uni]
        if g.empty:
            continue
        s = summary(g)
        yrs = max((g["exit_date"].max() - g["entry_date"].min()).days / 365.25, 1e-9)
        rr = R[R["universe"] == uni]["rt"].mean() if len(R) else np.nan
        md.append(f"| {uni} | {s['n']:,} | {s['n'] / yrs:.1f} | {fmt(s['mean'])} | {fmt(s['mean_price'])} | {100 * s['win']:.0f} | "
                  f"{fmt(s['avg_win'], 2)} | {fmt(s['avg_loss'], 2)} | {fmt(s['median'], 2)} | {s['pf']:.2f} | {fmt(rr)} | {fmt(s['mean'] - rr)} |")
    md += ["", "_Random entries (5 seeds per symbol, ~1 per 40 bars) with the same stop, exit and one-trade-per-symbol sequencing show how much of the mean R any "
           "long entry would earn from drift; the difference is the part that comes from the E4 entry itself._", ""]
    # 2 over time
    md += ["## 2. Over time (ETFs)", ""]
    E_ = T[T["universe"] == "ETF"].copy()
    E_["year"] = pd.to_datetime(E_["entry_date"]).dt.year
    yr = pd.DataFrame([dict(group=str(y), **summary(d)) for y, d in E_.groupby("year")])
    md += table(yr, ["group", "n", "mean", "win", "median"], ["year", "trades", "mean R", "win share", "median R"])
    if len(yr) >= 6:
        y = yr["group"].astype(int).to_numpy(float)
        slope = np.polyfit(y, yr["mean"].to_numpy(float), 1)[0]
        md += ["", f"Linear trend of the yearly mean: {slope:+.4f} R per year (descriptive; yearly means are noisy)."]
    for lab, m in (("2000-2014", E_["year"] < 2015), ("2015-", E_["year"] >= 2015)):
        s = summary(E_[m])
        md.append(f"- {lab}: {s['n']} trades, mean {fmt(s['mean'])} R, win {100 * s['win']:.0f}%")
    # 3 distribution
    md += ["", "## 3. Shape of the results (ETFs)", ""]
    r = E_["rt"].to_numpy(float)
    q = np.quantile(r, [0.05, 0.25, 0.5, 0.75, 0.95])
    md += [f"- R percentiles 5/25/50/75/95: {' / '.join(f'{v:+.2f}' for v in q)}",
           f"- Exit reasons: " + ", ".join(f"{k} {v} ({100 * v / len(E_):.0f}%)" for k, v in E_["why"].value_counts().items()),
           f"- Mean R by exit reason: " + ", ".join(f"{k} {fmt(v, 2)}" for k, v in E_.groupby("why")["rt"].mean().items()),
           f"- Losers that were at least +1R at some point: {100 * ((E_['rt'] <= 0) & (E_['mfe'] >= 1)).sum() / max((E_['rt'] <= 0).sum(), 1):.0f}% of losers",
           f"- Winners that were at -0.5R or worse at some point: {100 * ((E_['rt'] > 0) & (E_['mae'] <= -0.5)).sum() / max((E_['rt'] > 0).sum(), 1):.0f}% of winners",
           f"- Average holding: {E_['bars'].mean():.0f} bars (winners {E_[E_['rt'] > 0]['bars'].mean():.0f}, losers {E_[E_['rt'] <= 0]['bars'].mean():.0f})",
           "", "_Best and worst points during a trade (MFE/MAE) use daily highs and lows, price only (no dividends)._"]
    # 4 streaks and portfolio
    seqr = E_.sort_values("exit_date")["rt"].to_numpy(float)
    p95, p99 = boot_streak(seqr)
    md += ["", "## 4. Streaks and portfolio (ETFs)", "",
           f"- Longest losing streak in the full history: {longest_streak(seqr)} trades",
           f"- Longest losing streak to expect within any 100 trades (bootstrap): 95th percentile {p95:.0f}, 99th {p99:.0f}", "",
           "| risk per trade | trades taken (max 5 open) | CAGR | max drawdown | MAR |", "|---|---|---|---|---|"]
    for pr in portfolio_rows(E_, cfg):
        md.append(f"| {pr['risk']} | {pr.get('trades', 0):,} | {fmt(pr.get('cagr'), 1, True)} | {fmt(pr.get('max_dd'), 1, True)} | "
                  f"{pr.get('mar', float('nan')):.2f} |")
    md += ["", "_Daily mark-to-market equity, dividends included. The drawdown scales roughly with risk; MAR barely changes, "
           "because risk size doesn't change the edge._"]
    # 5 stops and gaps
    md += ["", "## 5. Stops, gaps and stop width (ETFs)", ""]
    gap = E_[E_["why"] == "stop_gap"]
    md += [f"- Stops filled through a gap: {len(gap)} ({100 * len(gap) / len(E_):.1f}% of trades), mean {fmt(gap['rt'].mean(), 2)} R "
           f"(worst {gap['rt'].min():+.2f} R)" if len(gap) else "- No gap stops", ""]
    E_["width_q"] = pd.qcut(E_["risk_pct"], 5, labels=["1 narrowest", "2", "3", "4", "5 widest"])
    w = pd.DataFrame([dict(group=str(k), width=float(d["risk_pct"].median()), **summary(d)) for k, d in E_.groupby("width_q", observed=True)])
    md += table(w, ["group", "width", "n", "mean", "win"], ["stop width quintile", "median stop width (% of price)", "trades", "mean R", "win share"])
    # 6 symbols
    md += ["", "## 6. By symbol (ETFs)", ""]
    bs = pd.DataFrame([dict(group=s, **summary(d)) for s, d in E_.groupby("sym")]).sort_values("mean", ascending=False)
    md += table(bs, ["group", "n", "mean", "win"], ["ETF", "trades", "mean R", "win share"])
    md += ["", "_Per-symbol samples are small (about 30-60 trades); differences between symbols are mostly noise._"]
    # 7 clustering
    md += ["", "## 7. Clustering (ETFs)", ""]
    d_ = pd.to_datetime(E_["entry_date"])
    near = np.array([((d_ - d).abs() <= pd.Timedelta(days=3)).sum() - 1 for d in d_])
    E_["cluster"] = np.where(near >= 2, "3+ entries within 3 days", np.where(near == 1, "2 entries within 3 days", "alone"))
    cl = pd.DataFrame([dict(group=k, **summary(g)) for k, g in E_.groupby("cluster")])
    md += table(cl, ["group", "n", "mean", "win"], ["entry clustering", "trades", "mean R", "win share"])
    md += ["", "_Clustered entries usually share one market move: their results are correlated, so 5 open positions "
           "entered in the same week are closer to one bet than five._"]
    # 8 context at entry
    md += ["", "## 8. Context at the signal bar (ETFs; hypothesis-generating only)", ""]
    ctx = [("tag_trend200", None, None, "price above a rising 200-day average"),
           ("tag_spy_trend200", None, None, "SPY above a rising 200-day average"),
           ("tag_stage", None, None, "IFI stage"),
           ("tag_atr_pctile", [0, 1 / 3, 2 / 3, 1], ["low", "mid", "high"], "ATR percentile (250 bars)"),
           ("tag_dist_anchor_atr", [-np.inf, 0.5, 1.5, np.inf], ["< 0.5", "0.5-1.5", "> 1.5"], "distance above the anchor (ATR)"),
           ("tag_bars_since_washout_exit", [0, 20, 60, np.inf], ["<= 20", "21-60", "> 60"], "bars since the last washout exit")]
    n_slices = 0
    for col, bins, labels, name in ctx:
        if col not in E_:
            continue
        t_ = slice_table(E_, col, bins, labels)
        n_slices += len(t_)
        md += [f"**{name}**", ""] + table(t_, ["group", "n", "mean", "win"], ["group", "trades", "mean R", "win share"]) + [""]
    md += [f"_{n_slices} groups shown. At this many, a difference of about ±0.2 R between groups of ~200 trades can appear by chance._"]
    return "\n".join(md) + "\n"


def main() -> int:
    cfg, _ = XR.check_lock()   # same engine and simulator as the locked exit test
    man = D.manifest()
    if man is None or man.get("source") != D.SOURCE:
        print("ABORT: no Yahoo exit-test snapshot (run the Research workflow with step = exits first)")
        return 1
    T, R, _ = build(cfg)
    OUT.mkdir(parents=True, exist_ok=True)
    meta = dict(run_utc=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"), cutoff=man["cutoff"], manifest=D.manifest_hash())
    (OUT / "E4_PROFILE.md").write_text(report(T, R, cfg, meta))
    T.drop(columns=["path"]).to_csv(OUT / "E4_trades.csv", index=False)
    print("E4 profile written:", len(T), "trades")
    return 0


if __name__ == "__main__":
    sys.exit(main())
