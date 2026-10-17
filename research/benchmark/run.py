"""Benchmark test v1 (research/benchmark/prereg_benchmark_v1.yaml): does the IFI book beat simply holding the market?

  python -m research.benchmark.run        (or Actions -> Research -> step = benchmark)

A measurement: the construction-v1 books (same code, trades and seeds) against SPY buy-and-hold and a SPY 200-day
trend rule, by alpha/beta regression and Sharpe, on the sealed set (primary) and the design data. Nothing is downloaded.

Order: 1 lock · 2 synthetic null (zero alpha) · 3 synthetic power (planted alpha) · 4 pinned snapshots ·
       5 books and benchmarks on design and sealed data · 6 report -> reports/benchmark/BENCHMARK.md
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from research.construction import data as SD
from research.construction import run as CR
from research.exits import data as XD

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PREREG = HERE / "prereg_benchmark_v1.yaml"
LOCK = HERE / "BENCHMARK.lock"
OUT = ROOT / "reports" / "benchmark"
LOCKED_FILES = ["research/benchmark/prereg_benchmark_v1.yaml", "research/benchmark/run.py",
                "research/construction/prereg_construction_v1.yaml", "research/construction/run.py",
                "research/construction/data.py", "research/construction/CONSTRUCTION.lock", "research/exits/data.py",
                "research/exits/synth.py", "research/exits/prereg_exits_v1.yaml", "research/exits/EXITS.lock",
                "research/common.py", "ifi/backtest.py", "ifi/states.py", "ifi/indicators.py", "ifi/pine.py", "ifi/data.py"]
BOOKS = ["B0", "C1", "S20"]


# ------------------------------------------------------------------ lock
def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write_lock() -> str:
    LOCK.write_text("\n".join(f"{_sha(ROOT / f)}  {f}" for f in LOCKED_FILES) + "\n")
    return _sha(LOCK)


def check_lock() -> tuple[dict, str]:
    if not LOCK.exists():
        raise SystemExit("BENCHMARK.lock missing: refusing to run")
    want = dict(reversed(line.split()[:2]) for line in LOCK.read_text().splitlines() if line.strip())
    if sorted(want) != sorted(LOCKED_FILES):
        raise SystemExit(f"BENCHMARK.lock lists {sorted(want)}, expected {sorted(LOCKED_FILES)}")
    bad = [f for f in LOCKED_FILES if _sha(ROOT / f) != want[f]]
    if bad:
        raise SystemExit("Locked benchmark-test files changed after locking: " + ", ".join(bad))
    CR.check_lock()
    return yaml.safe_load(PREREG.read_text()), _sha(LOCK)


# ------------------------------------------------------------------ benchmarks
def trend_positions(close: pd.Series, window: int) -> pd.Series:
    """Position held ON day d: 1 if day d-1's close was above its `window`-day average (known at d-1's close)."""
    sma = close.rolling(window).mean()
    return (close > sma).astype(float).where(sma.notna(), 0.0).shift(1).fillna(0.0)


def bench_daily(price: pd.Series, days: pd.DatetimeIndex, window: int, cost: float) -> pd.DataFrame:
    """Daily returns on the book's calendar: BH (buy and hold) and TR (trend rule, switching costs per side)."""
    pos = trend_positions(price, window)
    r = price.pct_change()
    tr = pos * r - cost * pos.diff().abs().fillna(0.0)
    d = pd.DataFrame(dict(BH=r, TR=tr)).reindex(days)
    return d.fillna(0.0)


def to_monthly(daily: pd.Series) -> pd.Series:
    eq = (1 + daily).cumprod()
    return eq.resample("ME").last().pct_change().dropna()


def ols(y: np.ndarray, X: np.ndarray) -> np.ndarray:
    A = np.column_stack([np.ones(len(y)), X])
    return np.linalg.lstsq(A, y, rcond=None)[0]


def measure(book_m: pd.Series, bm: pd.DataFrame, p: dict) -> dict:
    """Alpha/beta and Sharpe comparisons on aligned monthly rows, with a paired moving-block bootstrap."""
    j = pd.concat([book_m.rename("book"), bm["BH"], bm["TR"]], axis=1, join="inner").dropna()
    y, s, t = j["book"].to_numpy(), j["BH"].to_numpy(), j["TR"].to_numpy()
    c1 = ols(y, s[:, None])
    c2 = ols(y, np.column_stack([s, t]))
    out = dict(months=int(len(j)), alpha1=12 * c1[0], beta1=c1[1], alpha2=12 * c2[0], beta2_spy=c2[1], beta2_tr=c2[2],
               sh_book=CR.sharpe(y), sh_bh=CR.sharpe(s), sh_tr=CR.sharpe(t),
               resid_vol=float(np.std(y - np.column_stack([np.ones(len(y)), s, t]) @ c2, ddof=3) * np.sqrt(12)))
    n, b = len(y), p["boot_block_months"]
    if n < 2 * b:
        return dict(out, a2_lo=np.nan, a2_hi=np.nan, p_tr=np.nan, p_bh=np.nan)
    rng = np.random.default_rng(p["boot_seed"])
    nb = int(np.ceil(n / b))
    a2, dtr, dbh = np.empty(p["boot_reps"]), np.empty(p["boot_reps"]), np.empty(p["boot_reps"])
    for k in range(p["boot_reps"]):
        st = rng.integers(0, n - b + 1, nb)
        idx = (st[:, None] + np.arange(b)).ravel()[:n]
        yy, ss, tt = y[idx], s[idx], t[idx]
        a2[k] = 12 * ols(yy, np.column_stack([ss, tt]))[0]
        sb = CR.sharpe(yy)
        dtr[k], dbh[k] = sb - CR.sharpe(tt), sb - CR.sharpe(ss)
    return dict(out, a2_lo=float(np.quantile(a2, 0.025)), a2_hi=float(np.quantile(a2, 0.975)),
                p_tr=float(np.mean(dtr > 0)), p_bh=float(np.mean(dbh > 0)))


def matched(book_daily: pd.Series, bench: pd.DataFrame) -> dict:
    """CAGR and max drawdown of each benchmark scaled to the book's daily volatility (same days)."""
    out = {}
    vb = book_daily.std()
    for k, s in (("book", book_daily), ("BH", bench["BH"]), ("TR", bench["TR"])):
        w = 1.0 if k == "book" else (vb / s.std() if s.std() > 0 else np.nan)
        eq = (1 + w * s).cumprod()
        yrs = max((eq.index[-1] - eq.index[0]).days / 365.25, 1e-9)
        out[k] = dict(scale=float(w), cagr=float(eq.iloc[-1] ** (1 / yrs) - 1), dd=float((eq / eq.cummax() - 1).min()))
    return out


def verdict(m: dict, p: dict) -> tuple[str, dict]:
    g = dict(A=bool(m["a2_lo"] > 0), B=bool(m["p_tr"] >= p["p_min"]), C=bool(m["p_bh"] >= p["p_min"]))
    v = "EDGE" if g["A"] and g["B"] else ("PARTIAL" if g["A"] or g["B"] else "NO_EDGE_BEYOND_BENCHMARKS")
    return v, g


# ------------------------------------------------------------------ one dataset
def evaluate(T: pd.DataFrame, frames: dict, spy: pd.DataFrame, cpr: dict, p: dict) -> dict:
    book = CR.Book(T, frames)
    kw = lambda d: {k: d[k] for k in ("slots", "risk", "cash", "day_cap") if k in d}
    B = dict(cpr["books"], **cpr["books"]["reported_only"])
    days = book.days
    px = spy["close"].astype(float)
    bd = bench_daily(px, days, p["tr_window"], p["tr_cost"])
    bm = pd.DataFrame({k: to_monthly(bd[k]) for k in ("BH", "TR")})
    tot = None
    if "adjclose" in spy and spy["adjclose"].notna().any():
        bdt = bench_daily(spy["adjclose"].astype(float), days, p["tr_window"], p["tr_cost"])
        tot = pd.DataFrame({k: to_monthly(bdt[k]) for k in ("BH", "TR")})
    res = {}
    for name in BOOKS:
        n_orders = cpr["params"]["b0_orders"] if name == "B0" else cpr["params"]["other_orders"]
        o, _ = CR.median_path(book, n_orders, **kw(B[name]))
        cv = o["curve"]
        daily = cv.pct_change().reindex(days).fillna(0.0)
        m = measure(o["monthly"], bm, p)
        r = dict(m, book=o, matched=matched(daily, bd), name=B[name]["name"])
        if tot is not None:
            j = pd.concat([o["monthly"].rename("b"), tot["BH"]], axis=1, join="inner").dropna()
            c = ols(j["b"].to_numpy(), j["BH"].to_numpy()[:, None])
            r["alpha1_total"], r["beta1_total"] = 12 * c[0], c[1]
        res[name] = r
    return dict(res=res, n_trades=len(T), mean_r=float(T["r"].mean()), start=str(days[0].date()), end=str(days[-1].date()))


# ------------------------------------------------------------------ synthetic checks
def synthetic(p: dict) -> tuple[bool, list]:
    rng = np.random.default_rng(23)
    n_days = p["synthetic_months"] * 21
    days = pd.bdate_range("2000-01-03", periods=n_days)
    drift = np.where(np.cumsum(rng.random(n_days) < 1 / 250) % 2 == 0, 0.0006, -0.0004)
    px = pd.Series(100 * np.exp(np.cumsum(drift + rng.normal(0, 0.011, n_days))), index=days)
    bd = bench_daily(px, days, p["tr_window"], p["tr_cost"])
    bm = pd.DataFrame({k: to_monthly(bd[k]) for k in ("BH", "TR")})
    msgs, ok = [], True
    for label, alpha, need in (("null (zero alpha)", 0.0, False), ("power (planted alpha 4%/yr)", p["power_alpha"], True)):
        noise = pd.Series(np.random.default_rng(29).normal(0, 0.015, len(bm)), index=bm.index)
        book_m = p["null_beta"] * bm["BH"] + alpha / 12 + noise
        m = measure(book_m, bm, p)
        a_pass = m["a2_lo"] > 0
        good = a_pass == need
        ok &= good
        print(f"[{2 if not need else 3}/6] synthetic {label}:", "ok" if good else "FAILED",
              f"alpha {100 * m['alpha2']:+.2f}% (95% {100 * m['a2_lo']:+.2f} to {100 * m['a2_hi']:+.2f}), beta {m['beta2_spy']:.2f}")
        msgs.append((f"Synthetic {label}", ("ok: " if good else "FAILED: ") + f"alpha {100 * m['alpha2']:+.2f}% a year "
                     f"(95% {100 * m['a2_lo']:+.2f} to {100 * m['a2_hi']:+.2f}), beta {m['beta2_spy']:.2f}; required: gate A "
                     + ("passes" if need else "does not pass")))
    return ok, msgs


# ------------------------------------------------------------------ report
def _p(v, d=1):
    return "–" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{100 * v:+.{d}f}%"


def _f(v, d=2):
    return "–" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{v:.{d}f}"


def dataset_md(title: str, ev: dict) -> list[str]:
    md = [f"## {title}", "", f"_{ev['n_trades']:,} E4/E1 trades (mean {ev['mean_r']:+.3f} R) · {ev['start']} to {ev['end']} · monthly returns_", "",
          "| book | Sharpe book | Sharpe SPY | Sharpe trend rule | P(book > trend) | P(book > SPY) | alpha vs SPY (a year) | beta | "
          "alpha vs SPY + trend | 95% interval | residual vol |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for k, r in ev["res"].items():
        md.append(f"| {k} {r['name']} | {_f(r['sh_book'])} | {_f(r['sh_bh'])} | {_f(r['sh_tr'])} | {_f(r['p_tr'], 3)} | {_f(r['p_bh'], 3)} | "
                  f"{_p(r['alpha1'], 2)} | {_f(r['beta1'])} | {_p(r['alpha2'], 2)} | {_p(r['a2_lo'], 2)} to {_p(r['a2_hi'], 2)} | {_p(r['resid_vol'], 1)} |")
    md += ["", "Same risk: each benchmark scaled to the book's daily volatility.", "",
           "| book | book CAGR / max DD | SPY at the same volatility | trend rule at the same volatility |", "|---|---|---|---|"]
    for k, r in ev["res"].items():
        mt = r["matched"]
        md.append(f"| {k} | {_p(mt['book']['cagr'])} / {_p(mt['book']['dd'])} | {_p(mt['BH']['cagr'])} / {_p(mt['BH']['dd'])} (×{mt['BH']['scale']:.2f}) | "
                  f"{_p(mt['TR']['cagr'])} / {_p(mt['TR']['dd'])} (×{mt['TR']['scale']:.2f}) |")
    if any("alpha1_total" in r for r in ev["res"].values()):
        md += ["", "Total-return SPY (dividends included; the books' R is price only, so this is harsher on the books): alpha vs SPY "
               + ", ".join(f"{k} {_p(r.get('alpha1_total'), 2)} (beta {_f(r.get('beta1_total'))})" for k, r in ev["res"].items()) + "."]
    return md


def report(sealed: dict, design: dict, v: str, g: dict, pr: dict, meta: dict) -> str:
    md = ["# Benchmark test v1: does the IFI book beat simply holding the market?", "",
          f"_Run {meta['run_utc']} · commit `{meta['commit']}` · lock `{meta['lock'][:16]}` · sealed manifest `{meta['sealed'][:16]}` · "
          f"design manifest `{meta['design'][:16]}` · returns price only, idle cash 0%_", "",
          "Pre-registered in `research/benchmark/prereg_benchmark_v1.yaml`. A measurement: the construction-v1 books (same trades, "
          "same seeds) against SPY buy-and-hold and a SPY 200-day trend rule. It selects no rule.", "",
          "## Validity", "", "| check | result |", "|---|---|"] + [f"| {a} | {b} |" for a, b in meta["validity"]]
    yn = lambda b: "yes" if b else "no"
    r = sealed["res"]["B0"]
    md += ["", "## Verdict (sealed set, the real rule B0)", "",
           "| verdict | A: alpha beyond SPY and trend (95% low > 0) | B: beats the trend rule (P ≥ 0.95) | C: beats buy-and-hold (P ≥ 0.95) |",
           "|---|---|---|---|",
           f"| **{v}** | {yn(g['A'])} ({_p(r['alpha2'], 2)}, 95% {_p(r['a2_lo'], 2)} to {_p(r['a2_hi'], 2)}) | {yn(g['B'])} (P {r['p_tr']:.3f}) | "
           f"{yn(g['C'])} (P {r['p_bh']:.3f}) |", "", pr["decisions"][v], ""]
    md += dataset_md("Sealed set (out of sample)", sealed) + [""] + dataset_md("Design data (working history; the book was built here)", design)
    md += ["", "_Alpha: annualized intercept of monthly book returns regressed on SPY (and, beyond, on the trend rule). "
           "A book that only holds the market part of the time shows a low beta and an alpha near zero._"]
    return "\n".join(md) + "\n"


def _commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return "unknown"


def main() -> int:
    pr, lock = check_lock()
    p = pr["params"]
    print(f"[1/6] lock ok ({lock})")
    validity = [("Lock (prereg, benchmark and construction code, data modules; construction and exit locks too)", f"ok `{lock[:16]}`")]
    ok, m = synthetic(p)
    validity += m
    if not ok:
        print("ABORT: synthetic check failed")
        return 1
    dm, sm = XD.manifest(), SD.manifest()
    if dm is None or not XD.manifest_hash().startswith(pr["data"]["design"]["manifest_prefix"]):
        print("ABORT: the design snapshot is not the pinned one")
        return 1
    if sm is None or not SD.manifest_hash().startswith(pr["data"]["sealed"]["manifest_prefix"]):
        print("ABORT: the sealed snapshot is not the pinned one")
        return 1
    print(f"[4/6] snapshots ok: design {XD.manifest_hash()[:16]}, sealed {SD.manifest_hash()[:16]}")
    validity.append(("Pinned snapshots (nothing downloaded)", f"design `{XD.manifest_hash()[:16]}` · sealed `{SD.manifest_hash()[:16]}`"))
    cpr = yaml.safe_load(CR.PREREG.read_text())
    spy = XD.load("SPY")
    WU = yaml.safe_load((ROOT / "research" / "exits" / "prereg_exits_v1.yaml").read_text())["universe"]
    Td, Fd = CR.build_trades(XD.load, WU["etfs"] + WU["stocks"], set(WU["etfs"]), cpr)
    design = evaluate(Td, Fd, spy, cpr, p)
    U = cpr["sealed_universe"]
    Ts, Fs = CR.build_trades(SD.load, U["etfs"] + U["stocks"], set(U["etfs"]), cpr)
    sealed = evaluate(Ts, Fs, spy, cpr, p)
    v, g = verdict(sealed["res"]["B0"], p)
    for lab, ev in (("design", design), ("sealed", sealed)):
        r = ev["res"]["B0"]
        print(f"[5/6] {lab} B0: Sharpe {r['sh_book']:.2f} vs SPY {r['sh_bh']:.2f} vs trend {r['sh_tr']:.2f}; alpha vs SPY+trend "
              f"{100 * r['alpha2']:+.2f}% (95% {100 * r['a2_lo']:+.2f} to {100 * r['a2_hi']:+.2f}), beta {r['beta1']:.2f}")
    OUT.mkdir(parents=True, exist_ok=True)
    meta = dict(run_utc=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"), commit=_commit(), lock=lock,
                sealed=SD.manifest_hash(), design=XD.manifest_hash(), validity=validity)
    (OUT / "BENCHMARK.md").write_text(report(sealed, design, v, g, pr, meta))
    rows = [dict(dataset=lab, book=k, **{f: r[f] for f in ("months", "sh_book", "sh_bh", "sh_tr", "p_tr", "p_bh", "alpha1", "beta1",
                                                            "alpha2", "a2_lo", "a2_hi", "beta2_spy", "beta2_tr", "resid_vol")})
            for lab, ev in (("sealed", sealed), ("design", design)) for k, r in ev["res"].items()]
    pd.DataFrame(rows).to_csv(OUT / "BENCHMARK_results.csv", index=False)
    (OUT / "BENCHMARK_meta.json").write_text(json.dumps(dict({k: v_ for k, v_ in meta.items() if k != "validity"}, validity=validity,
                                                             verdict=v, gates=g), indent=1, default=str))
    print("[6/6] written:", v, g)
    return 0


if __name__ == "__main__":
    sys.exit(main())
