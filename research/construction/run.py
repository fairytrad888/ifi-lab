"""Book construction test v1 (research/construction/prereg_construction_v1.yaml): how should the proven edge be deployed?

  python -m research.construction.run        (or Actions -> Research -> step = construction)

Order (each check aborts before what it protects):
  1. lock: prereg + construction code + the Lab and research modules it uses match CONSTRUCTION.lock (and EXITS.lock)
  2. synthetic null (martingale prices): C1 must not PASS
  3. synthetic power (persistent trends, independent symbols): C1 must PASS
  4. design data (working history, pinned exit-test snapshot, daily marks): INFORMATION and BOTH HALVES must hold,
     else ABORT without opening the sealed set
  5. sealed set: downloaded once (first run that gets here), then reused; never refreshed
  6. the test on the sealed set -> reports/construction/CONSTRUCTION.md + CSVs
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import zlib
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from ifi import backtest as bt
from ifi.states import read
from research.construction import data as SD
from research.exits import data as XD
from research.exits.synth import martingale_loader, trend_loader

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PREREG = HERE / "prereg_construction_v1.yaml"
LOCK = HERE / "CONSTRUCTION.lock"
OUT = ROOT / "reports" / "construction"
LOCKED_FILES = ["research/construction/prereg_construction_v1.yaml", "research/construction/run.py",
                "research/construction/data.py", "research/exits/data.py", "research/exits/synth.py",
                "research/exits/prereg_exits_v1.yaml",
                "research/exits/EXITS.lock", "research/common.py", "ifi/backtest.py", "ifi/states.py",
                "ifi/indicators.py", "ifi/pine.py", "ifi/data.py"]
DESIGN_MANIFEST = "a3609f3fec828066"
SETUPS = ["E4_anchor_reclaim", "E1_trigger_with_trend"]
EXIT = "X3_target3R"
PASS, FAIL, INSUFFICIENT = "PASS", "FAIL", "INSUFFICIENT"


# ------------------------------------------------------------------ lock
def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write_lock() -> str:
    LOCK.write_text("\n".join(f"{_sha(ROOT / f)}  {f}" for f in LOCKED_FILES) + "\n")
    return _sha(LOCK)


def check_lock() -> tuple[dict, str]:
    if not LOCK.exists():
        raise SystemExit("CONSTRUCTION.lock missing: refusing to run")
    want = dict(reversed(line.split()[:2]) for line in LOCK.read_text().splitlines() if line.strip())
    if sorted(want) != sorted(LOCKED_FILES):
        raise SystemExit(f"CONSTRUCTION.lock lists {sorted(want)}, expected {sorted(LOCKED_FILES)}")
    bad = [f for f in LOCKED_FILES if _sha(ROOT / f) != want[f]]
    if bad:
        raise SystemExit("Locked construction-test files changed after locking: " + ", ".join(bad))
    return yaml.safe_load(PREREG.read_text()), _sha(LOCK)


# ------------------------------------------------------------------ trades (the Lab's own definitions)
def build_trades(loader, symbols: list[str], etfs: set, pr: dict, random_seeds=None) -> tuple[pd.DataFrame, dict]:
    """E4/E1 (or random-entry) trades with the X3 exit, exactly as ifi/run_backtests.py makes them, plus daily marks.
    Returns (trades, frames). Marks: (close - fill)/risk - cost*(fill + close)/risk, equal to R on the exit day."""
    tr = pr["trades"]
    rows, frames = [], {}
    for s in symbols:
        df = loader(s)
        if df is None or len(df) < 400:
            continue
        x = read(df[["open", "high", "low", "close", "volume"]])
        x = x[x.index >= tr["start"]]
        if len(x) <= 300:
            continue
        frames[s] = x
        cost = tr["costs"]["etf"] if s in etfs else tr["costs"]["stock"]
        if random_seeds is None:
            ent = {su: e for su, e in bt.setups(x).items() if su in SETUPS}
        else:
            ent = {f"random{sd}": bt.random_setup(x, pr["params"]["random_rate"], sd * 100_000 + zlib.crc32(s.encode()) % 100_000)
                   for sd in random_seeds}
        o, c = x["open"].to_numpy(), x["close"].to_numpy()
        for su, e in ent.items():
            for t in bt.simulate(s, x, e, su, EXIT, cost):
                i0, i1 = x.index.get_loc(t.entry_date), x.index.get_loc(t.exit_date)
                fill = o[i0]
                risk = t.risk_pct * fill
                m = (c[i0:i1 + 1] - fill) / risk - cost * (fill + c[i0:i1 + 1]) / risk
                m[-1] = t.r
                rows.append(dict(symbol=s, setup=su, universe="etf" if s in etfs else "stock", entry_date=t.entry_date,
                                 exit_date=t.exit_date, r=t.r, width=t.risk_pct, fill=fill, risk_ps=risk, reason=t.reason,
                                 marks=m, mdates=x.index[i0:i1 + 1].values))
    T = pd.DataFrame(rows)
    if len(T):
        T = T.sort_values(["entry_date", "setup", "symbol"], kind="mergesort").reset_index(drop=True)
    return T, frames


# ------------------------------------------------------------------ the book (daily mark-to-market)
class Book:
    """Daily MTM book. A new position risks `risk` x the previous close's equity (or, with whole shares, the largest
    whole number of shares within that risk; below one share it is skipped). A trade exiting on day d frees its slot
    for entries on d. Skips: slots full, day cap reached, or total position value would exceed cash x equity."""

    def __init__(self, T: pd.DataFrame, frames: dict):
        self.T = T
        days = sorted({d for x in frames.values() for d in x.index if d >= T["entry_date"].min()})
        self.days = pd.DatetimeIndex(days)
        pos = {d: k for k, d in enumerate(days)}
        self.e = np.array([pos[d] for d in T["entry_date"]])
        self.x = np.array([pos[d] for d in T["exit_date"]])
        self.r = T["r"].to_numpy(float)
        self.w = T["width"].to_numpy(float)
        self.fill = T["fill"].to_numpy(float)
        self.rps = T["risk_ps"].to_numpy(float)
        # marks aligned to the book's calendar (a symbol with a missing day keeps its last mark)
        idx = pd.Index(self.days)
        self.m = []
        for k, (mk, md) in enumerate(zip(T["marks"], T["mdates"])):
            arr = np.full(self.x[k] - self.e[k] + 1, np.nan)
            arr[idx.get_indexer(pd.DatetimeIndex(md)) - self.e[k]] = mk
            self.m.append(pd.Series(arr).ffill().to_numpy())
        self.base_order = np.arange(len(T))
        self.n_years = (self.days[-1] - self.days[0]).days / 365.25

    def run(self, slots=None, risk=0.0075, cash=1.0, seed=None, day_cap=None, account=None) -> dict:
        n = len(self.r)
        order = self.base_order if seed is None else np.lexsort((np.random.default_rng(seed).random(n), self.e))
        by_e: dict = {}
        for i in order:
            by_e.setdefault(self.e[i], []).append(i)
        by_x: dict = {}
        start = float(account) if account else 100_000.0
        cashv, open_, notional, taken = start, {}, 0.0, 0
        eq_prev = start
        vals = np.empty(len(self.days))
        pos_n = np.empty(len(self.days))
        heat = np.empty(len(self.days))
        for k in range(len(self.days)):
            for i in by_x.pop(k, ()):
                a = open_.pop(i)
                cashv += a * self.r[i]
                notional -= a / self.w[i]
            nt = 0
            for i in by_e.get(k, ()):
                if slots is not None and len(open_) >= slots:
                    break
                if day_cap is not None and nt >= day_cap:
                    break
                a = risk * eq_prev
                if account:
                    sh = np.floor(a / self.rps[i])
                    if sh < 1:
                        continue
                    a = sh * self.rps[i]
                if notional + a / self.w[i] > cash * eq_prev + 1e-9:
                    continue
                open_[i] = a
                notional += a / self.w[i]
                taken += 1
                nt += 1
                by_x.setdefault(self.x[i], []).append(i)
            for i in by_x.pop(k, ()):                    # positions that exit on their own entry day
                a = open_.pop(i)
                cashv += a * self.r[i]
                notional -= a / self.w[i]
            eq = cashv + sum(a * self.m[i][k - self.e[i]] for i, a in open_.items())
            vals[k] = eq
            pos_n[k] = len(open_)
            heat[k] = sum(open_.values()) / eq if eq > 0 else np.nan
            eq_prev = eq
        cv = pd.Series(np.r_[start, vals], index=pd.DatetimeIndex(np.r_[self.days[:1] - pd.Timedelta(days=1), self.days]))
        return stats(cv, dict(taken=taken, share=taken / n if n else np.nan, trades_yr=taken / self.n_years,
                              pos_avg=float(pos_n.mean()), pos_max=int(pos_n.max()), heat_avg=float(np.nanmean(heat)),
                              heat_max=float(np.nanmax(heat))))


def monthly(cv: pd.Series) -> pd.Series:
    return cv.resample("ME").last().pct_change().dropna()


def sharpe(r) -> float:
    r = np.asarray(r, float)
    sd = r.std(ddof=1) if len(r) > 1 else np.nan
    return float(r.mean() / sd * np.sqrt(12)) if sd and sd > 0 else np.nan


def stats(cv: pd.Series, extra: dict, split: str = "2015-01-01") -> dict:
    yrs = max((cv.index[-1] - cv.index[0]).days / 365.25, 1e-9)
    cagr = (cv.iloc[-1] / cv.iloc[0]) ** (1 / yrs) - 1 if cv.iloc[-1] > 0 else -1.0
    dd = float((cv / cv.cummax() - 1).min())
    mr = monthly(cv)
    s = pd.Timestamp(split)
    return dict(extra, cagr=float(cagr), max_dd=dd, mar=float(cagr / -dd) if dd < 0 else np.nan, sharpe=sharpe(mr),
                sharpe_h1=sharpe(mr[mr.index < s]), sharpe_h2=sharpe(mr[mr.index >= s]),
                worst_month=float(mr.min()) if len(mr) else np.nan, months=int(len(mr)), curve=cv, monthly=mr)


def median_path(book: Book, n_orders: int, **kw) -> tuple[dict, list[float]]:
    """The path with the median Sharpe across seeded random same-day orders (prereg: books/order)."""
    runs = [book.run(seed=s_, **kw) for s_ in range(n_orders)]
    sh = [o["sharpe"] for o in runs]
    i = int(np.argsort(sh)[len(sh) // 2])
    return runs[i], sh


def boot_sharpe(a: pd.Series, b: pd.Series, reps: int, block: int, seed: int) -> tuple[float, float, float]:
    """Paired moving-block bootstrap of two monthly return series -> P(Sharpe a - Sharpe b > 0), 5th and 95th pct."""
    j = pd.concat([a, b], axis=1, join="inner").dropna()
    x, y = j.iloc[:, 0].to_numpy(), j.iloc[:, 1].to_numpy()
    n = len(x)
    if n < 2 * block:
        return np.nan, np.nan, np.nan
    nb = int(np.ceil(n / block))
    rng = np.random.default_rng(seed)
    out = np.empty(reps)
    for k in range(reps):
        st = rng.integers(0, n - block + 1, nb)
        idx = (st[:, None] + np.arange(block)).ravel()[:n]
        out[k] = sharpe(x[idx]) - sharpe(y[idx])
    return float(np.mean(out > 0)), float(np.quantile(out, 0.05)), float(np.quantile(out, 0.95))


def frontier(book: Book, ladder: list[float], n_orders: int = 5, **kw) -> list[dict]:
    """Each risk on the ladder: medians over seeded orders of CAGR, MTM max drawdown, Sharpe and signals taken."""
    out = []
    for r_ in ladder:
        runs = [book.run(seed=s_, risk=r_, **kw) for s_ in range(n_orders)]
        med = lambda k: float(np.median([o[k] for o in runs]))
        out.append(dict(risk=r_, cagr=med("cagr"), dd=med("max_dd"), sharpe=med("sharpe"), share=med("share")))
    return out


def matched(front: list[dict], target: float) -> dict | None:
    """The largest risk on the ladder whose median max drawdown is no deeper than the target."""
    ok = [f for f in front if f["dd"] >= target]
    return max(ok, key=lambda f: f["risk"]) if ok else None


# ------------------------------------------------------------------ evaluation of one universe
def evaluate(T: pd.DataFrame, frames: dict, pr: dict, full: bool = True) -> dict:
    p, B = pr["params"], pr["books"]
    book = Book(T, frames)
    kw = lambda d: {k: d[k] for k in ("slots", "risk", "cash", "day_cap") if k in d}
    b0, b0_sh = median_path(book, p["b0_orders"], **kw(B["B0"]))
    c1, c1_sh = median_path(book, p["other_orders"], **kw(B["C1"]))
    prob, lo, hi = boot_sharpe(c1["monthly"], b0["monthly"], p["boot_reps"], p["boot_block_months"], p["boot_seed"])
    gates = {"information": bool(prob >= p["p_min"]),
             "both halves": bool(c1["sharpe_h1"] - b0["sharpe_h1"] > 0 and c1["sharpe_h2"] - b0["sharpe_h2"] > 0),
             "edge present": bool(c1["sharpe"] > 0 and T["r"].mean() > 0)}
    if len(T) < p["min_trades"] or c1["months"] < p["min_months"]:
        verdict = INSUFFICIENT
    else:
        verdict = PASS if all(gates.values()) else FAIL
    out = dict(verdict=verdict, gates=gates, p=prob, d_lo=lo, d_hi=hi, b0=b0, c1=c1, b0_band=(float(np.quantile(b0_sh, .1)), float(np.quantile(b0_sh, .9))),
               c1_band=(float(np.quantile(c1_sh, .1)), float(np.quantile(c1_sh, .9))), n_trades=len(T), mean_r=float(T["r"].mean()))
    if full:
        rep = {}
        for k, d in B["reported_only"].items():
            o, sh_ = median_path(book, p["other_orders"], **kw(d))
            pk, _, _ = boot_sharpe(o["monthly"], b0["monthly"], p["boot_reps"], p["boot_block_months"], p["boot_seed"])
            rep[k] = dict(o, p=pk, name=d["name"])
        out["reported"] = rep
        fr = {lab: frontier(book, p["risk_ladder"], **d) for lab, d in
              (("5 slots", dict(slots=5)), ("every signal", {}), ("every signal, max 2 new a day", dict(day_cap=2)))}
        out["frontier"] = fr
        out["matched"] = {(t, lab): matched(f, t) for t in p["matched_dd"] for lab, f in fr.items()}
        ws = {}
        for acct in p["accounts"]:
            o, _ = median_path(book, p["other_orders"], account=acct, **kw(B["C1"]))
            ws[acct] = o
        out["whole_shares"] = ws
    return out


def regime_months(spy: pd.DataFrame) -> pd.Series:
    """True for months that START with SPY below a falling 200-day average (state at the previous month's last close)."""
    c = spy["close"]
    sma = c.rolling(200).mean()
    state = (c < sma) & (sma < sma.shift(20))
    me = state.resample("ME").last().shift(1)
    return me.dropna().astype(bool)


def lab_parity(Td: pd.DataFrame) -> str:
    """Informational: the design trades rebuilt from the frozen snapshot vs the Lab's own trade files (reports/results)."""
    parts = []
    for uni in ("etfs", "stocks"):
        f = ROOT / "reports" / "results" / f"trades_daily_{uni}.csv.gz"
        if f.exists():
            d = pd.read_csv(f, parse_dates=["entry_date"])
            parts.append(d[(d["exit_rule"] == EXIT) & d["setup"].isin(SETUPS)])
    if not parts:
        return "Lab trade files not found (skipped)"
    L = pd.concat(parts)
    key = lambda d: set(zip(d["symbol"], d["setup"], pd.to_datetime(d["entry_date"]).dt.strftime("%Y-%m-%d")))
    a, b = key(Td), key(L)
    lr = L.set_index([L["symbol"], L["setup"], L["entry_date"].dt.strftime("%Y-%m-%d")])["r"]
    tr = Td.set_index([Td["symbol"], Td["setup"], Td["entry_date"].dt.strftime("%Y-%m-%d")])["r"]
    both = lr.index.intersection(tr.index)
    same_r = int((np.abs(lr.loc[both].groupby(level=[0, 1, 2]).first() - tr.loc[both].groupby(level=[0, 1, 2]).first()) < 1e-6).sum())
    return (f"{len(a & b):,} of {len(b):,} Lab E4/E1 trades have the same entry here ({len(a - b):,} only here); "
            f"{same_r:,} of those have the same R to 1e-6 (informational: the Lab files may come from a different data date)")


def setup_table(T: pd.DataFrame, R: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (uni, su), g in T.groupby(["universe", "setup"]):
        rr = R[R["universe"] == uni]["r"] if len(R) else pd.Series(dtype=float)
        rows.append(dict(universe=uni, setup=su, trades=len(g), mean_r=g["r"].mean(), win=(g["r"] > 0).mean(),
                         random_r=rr.mean() if len(rr) else np.nan, edge=g["r"].mean() - (rr.mean() if len(rr) else np.nan)))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ report
def _p(v, d=1):
    return "–" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{100 * v:.{d}f}%"


def _f(v, d=2):
    return "–" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{v:.{d}f}"


def book_rows(res: dict, pr: dict) -> list[str]:
    rows = [("B0", pr["books"]["B0"]["name"], res["b0"], None), ("C1", pr["books"]["C1"]["name"], res["c1"], res["p"])]
    rows += [(k, v["name"], v, v["p"]) for k, v in res.get("reported", {}).items()]
    md = ["| book | rule | Sharpe | Sharpe 2000–14 | Sharpe 2015– | P(beats B0) | CAGR | max DD | MAR | worst month | trades/yr | signals taken | positions avg / max | heat avg / max |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for k, name, o, pb in rows:
        md.append(f"| {k} | {name} | {_f(o['sharpe'])} | {_f(o['sharpe_h1'])} | {_f(o['sharpe_h2'])} | {'–' if pb is None else _f(pb, 3)} | "
                  f"{_p(o['cagr'])} | {_p(o['max_dd'])} | {_f(o['mar'])} | {_p(o['worst_month'])} | {o['trades_yr']:.0f} | {_p(o['share'], 0)} | "
                  f"{o['pos_avg']:.1f} / {o['pos_max']} | {_p(o['heat_avg'])} / {_p(o['heat_max'])} |")
    return md


def matched_rows(res: dict) -> list[str]:
    md = ["| max drawdown target | book | risk per trade | CAGR | max DD | Sharpe | signals taken |", "|---|---|---|---|---|---|---|"]
    for (t, lab), v in res["matched"].items():
        if v is None:
            md.append(f"| {_p(t, 0)} | {lab} | not reachable on the ladder | – | – | – | – |")
        else:
            md.append(f"| {_p(t, 0)} | {lab} | {_p(v['risk'], 3)} | {_p(v['cagr'])} | {_p(v['dd'])} | {_f(v['sharpe'])} | {_p(v['share'], 0)} |")
    return md


def frontier_rows(res: dict) -> list[str]:
    labs = list(res["frontier"])
    md = ["| risk per trade | " + " | ".join(f"{l}: CAGR / max DD / Sharpe" for l in labs) + " |", "|---|" + "---|" * len(labs)]
    for k, f0 in enumerate(res["frontier"][labs[0]]):
        cells = []
        for l in labs:
            f = res["frontier"][l][k]
            cells.append(f"{_p(f['cagr'])} / {_p(f['dd'])} / {_f(f['sharpe'])}")
        md.append(f"| {_p(f0['risk'], 3)} | " + " | ".join(cells) + " |")
    return md


def report(sealed: dict, design: dict, meta: dict, pr: dict, extras: dict) -> str:
    md = ["# Book construction test v1: how should the proven edge be deployed?", "",
          f"_Run {meta['run_utc']} · commit `{meta['commit']}` · lock `{meta['lock'][:16]}` · sealed snapshot cutoff {meta['sealed_cutoff']} "
          f"(manifest `{meta['sealed_manifest'][:16]}`, created {meta['sealed_created']}) · design data: exit-test snapshot `{DESIGN_MANIFEST}`_", "",
          "Pre-registered in `research/construction/prereg_construction_v1.yaml`. The confirmation runs on a **sealed set** of symbols no IFI "
          "test had used. Both books trade exactly the same E4/E1 signals with the Lab's 3R exit; only the deployment differs.", "",
          "## Validity", "", "| check | result |", "|---|---|"]
    md += [f"| {a} | {b} |" for a, b in meta["validity"]]
    s = sealed
    yn = lambda b: "yes" if b else "no"
    md += ["", "## Verdict (sealed set)", "",
           "| comparison | verdict | information (P ≥ 0.95) | both halves | edge present |", "|---|---|---|---|---|",
           f"| C1 vs B0 | **{s['verdict']}** | {yn(s['gates']['information'])} (P = {s['p']:.3f}) | {yn(s['gates']['both halves'])} | {yn(s['gates']['edge present'])} |", "",
           f"Bootstrap of Sharpe C1 − B0: 5th to 95th percentile {s['d_lo']:+.2f} to {s['d_hi']:+.2f}. "
           f"B0 Sharpe across its {pr['params']['b0_orders']} random same-day orders: {s['b0_band'][0]:.2f} to {s['b0_band'][1]:.2f} (10th–90th pct); "
           f"C1: {s['c1_band'][0]:.2f} to {s['c1_band'][1]:.2f}.", "",
           f"## Books on the sealed set ({s['n_trades']:,} E4/E1 trades, mean {s['mean_r']:+.3f} R)", ""]
    md += book_rows(s, pr)
    md += ["", "## Same drawdown, different return (sealed set, daily marks)", ""] + matched_rows(s) + \
          ["", "_The largest risk on the ladder whose median max drawdown is no deeper than the target. The full ladder is below._", "",
           "### Risk ladder (sealed set): medians over 5 random orders", ""] + frontier_rows(s)
    md += ["", "## Whole shares (C1 at 0.10% risk, sealed set)", "", "| account | signals taken | Sharpe | CAGR | max DD |", "|---|---|---|---|---|"]
    for acct, o in s["whole_shares"].items():
        md.append(f"| ${acct:,} | {_p(o['share'], 0)} | {_f(o['sharpe'])} | {_p(o['cagr'])} | {_p(o['max_dd'])} |")
    md += ["", "_A position smaller than one share is skipped. Fractional shares (if your broker offers them) remove this limit._"]
    if extras.get("regime") is not None:
        g = extras["regime"]
        md += ["", "## Bad-market months (sealed set; reported, not gating)", "",
               "| months | count | B0 mean monthly return | C1 mean monthly return |", "|---|---|---|---|"]
        for lab, row in g.items():
            md.append(f"| {lab} | {row['n']} | {_p(row['b0'], 2)} | {_p(row['c1'], 2)} |")
        md += ["", "_Bad-market month: starts with SPY below a falling 200-day average (state at the previous month's last close)._"]
    st = extras.get("setups")
    if st is not None and len(st):
        md += ["", "## E4 and E1 on new symbols (first out-of-sample check of the setups; reported, not gating)", "",
               "| universe | setup | trades | mean R | win rate | random-entry mean R (same exit) | setup minus random |", "|---|---|---|---|---|---|---|"]
        for r_ in st.itertuples():
            md.append(f"| {r_.universe} | {r_.setup[:2]} | {r_.trades:,} | {r_.mean_r:+.3f} | {_p(r_.win, 0)} | {_f(r_.random_r, 3)} | {_f(r_.edge, 3)} |")
    d = design
    md += ["", "## Design data (working history, daily marks): the finding the sealed set was asked to confirm", "",
           f"Gate check: information P = {d['p']:.3f}, both halves {yn(d['gates']['both halves'])}, edge present {yn(d['gates']['edge present'])} "
           f"({d['n_trades']:,} trades, mean {d['mean_r']:+.3f} R).", ""]
    md += book_rows(d, pr)
    if "matched" in d:
        md += [""] + matched_rows(d) + ["", "### Risk ladder (design data)", ""] + frontier_rows(d)
    md += ["", "## Decision", "", pr["decisions"]["pass"] if s["verdict"] == PASS else pr["decisions"]["fail"]]
    return "\n".join(md) + "\n"


def _commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return "unknown"


# ------------------------------------------------------------------ main
def synthetic(pr: dict) -> tuple[bool, list]:
    U = pr["sealed_universe"]
    syms, etfs = U["etfs"] + U["stocks"], set(U["etfs"])
    msgs, ok = [], True
    for name, loader, need in (("null (martingale prices)", martingale_loader(3), False),
                               ("power (persistent trends, independent symbols)", trend_loader(5), True)):
        T, F = build_trades(loader, syms, etfs, pr)
        res = evaluate(T, F, pr, full=False)
        good = (res["verdict"] == PASS) if need else (res["verdict"] != PASS)
        ok &= good
        step = 2 if not need else 3
        print(f"[{step}/6] synthetic {name}:", "ok" if good else "FAILED", res["verdict"], f"P={res['p']:.3f}",
              f"C1 Sharpe {res['c1']['sharpe']:.2f} vs B0 {res['b0']['sharpe']:.2f}")
        msgs.append((f"Synthetic {name}", ("ok: " if good else "FAILED: ") + f"C1 {res['verdict']} (P {res['p']:.3f}; Sharpe C1 "
                     f"{res['c1']['sharpe']:.2f} vs B0 {res['b0']['sharpe']:.2f}; required: {'PASS' if need else 'no PASS'})"))
        if not good:
            break
    return ok, msgs


def main() -> int:
    pr, lock = check_lock()
    print(f"[1/6] lock ok ({lock})")
    validity = [("Lock (prereg, construction code, Lab and research modules; exit lock too)", f"ok `{lock[:16]}`")]
    ok, m = synthetic(pr)
    validity += m
    if not ok:
        print("ABORT: synthetic check failed")
        return 1
    man = XD.manifest()
    if man is None or man.get("source") != XD.SOURCE or not XD.manifest_hash().startswith(DESIGN_MANIFEST):
        print(f"ABORT: the design snapshot is not the pinned one ({XD.manifest_hash()[:16]})")
        return 1
    WU = yaml.safe_load((ROOT / "research" / "exits" / "prereg_exits_v1.yaml").read_text())["universe"]   # locked
    Td, Fd = build_trades(XD.load, WU["etfs"] + WU["stocks"], set(WU["etfs"]), pr)
    par = lab_parity(Td)
    print("      design trades vs Lab files:", par)
    validity.append(("Design trades vs the Lab's trade files (informational)", par))
    design = evaluate(Td, Fd, pr, full=True)
    dg = design["gates"]
    print(f"[4/6] design data: P={design['p']:.3f} halves={dg['both halves']} edge={dg['edge present']} "
          f"(C1 Sharpe {design['c1']['sharpe']:.2f} vs B0 {design['b0']['sharpe']:.2f})")
    validity.append(("Design data (working history, daily marks)", f"{'ok' if dg['information'] and dg['both halves'] else 'FAILED'}: "
                     f"P {design['p']:.3f}, both halves {dg['both halves']}; Sharpe C1 {design['c1']['sharpe']:.2f} vs B0 {design['b0']['sharpe']:.2f}"))
    if not (dg["information"] and dg["both halves"]):
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "CONSTRUCTION_ABORT.md").write_text(
            "# Construction test v1: aborted at the design-data check\n\nThe realized-equity finding did not survive daily marks on the "
            "working history, so the sealed set was NOT opened (it stays unused).\n\n" + "\n".join(book_rows(design, pr)) + "\n")
        print("ABORT: the design-data check failed; the sealed set was not opened")
        return 1
    U = pr["sealed_universe"]
    syms = U["etfs"] + U["stocks"]
    if SD.manifest() is None:
        smf = SD.make_snapshot(syms)
        print(f"[5/6] sealed snapshot created: cutoff {smf['cutoff']}, {len(smf['files'])} of {len(syms)} symbols")
    smf = SD.manifest()
    if smf.get("source") != XD.SOURCE:
        print("ABORT: the sealed snapshot is not Yahoo market data")
        return 1
    missing = [s for s in syms if s not in smf["files"]]
    print(f"[5/6] sealed snapshot: cutoff {smf['cutoff']} · manifest {SD.manifest_hash()[:16]} · missing {missing or 'none'}")
    validity.append(("Sealed snapshot (opened once)", f"created {smf['created_utc']} · cutoff {smf['cutoff']} · {len(smf['files'])} symbols · "
                     f"missing: {', '.join(missing) or 'none'}"))
    Ts, Fs = build_trades(SD.load, syms, set(U["etfs"]), pr)
    sealed = evaluate(Ts, Fs, pr, full=True)
    Rs, _ = build_trades(SD.load, syms, set(U["etfs"]), pr, random_seeds=pr["params"]["random_seeds"])
    extras = dict(setups=setup_table(Ts, Rs))
    spy = XD.load("SPY")
    if spy is not None:
        reg = regime_months(spy)
        j = pd.concat([sealed["b0"]["monthly"].rename("b0"), sealed["c1"]["monthly"].rename("c1"), reg.rename("bad")], axis=1, join="inner")
        extras["regime"] = {lab: dict(n=int(len(g)), b0=float(g["b0"].mean()), c1=float(g["c1"].mean()))
                            for lab, g in (("bad-market months", j[j["bad"]]), ("other months", j[~j["bad"]]))}
    OUT.mkdir(parents=True, exist_ok=True)
    meta = dict(run_utc=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"), commit=_commit(), lock=lock,
                sealed_cutoff=smf["cutoff"], sealed_manifest=SD.manifest_hash(), sealed_created=smf["created_utc"], validity=validity)
    (OUT / "CONSTRUCTION.md").write_text(report(sealed, design, meta, pr, extras))
    for lab, T in (("sealed", Ts), ("design", Td)):
        T.drop(columns=["marks", "mdates"]).to_csv(OUT / f"CONSTRUCTION_trades_{lab}.csv", index=False)
    (OUT / "CONSTRUCTION_meta.json").write_text(json.dumps(dict(
        {k: v for k, v in meta.items() if k != "validity"}, validity=validity, verdict=sealed["verdict"], p=sealed["p"],
        gates=sealed["gates"], design_p=design["p"]), indent=1, default=str))
    print("[6/6] written:", sealed["verdict"], f"P={sealed['p']:.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
