"""E4 exit test v1 runner (research/exits/prereg_exits_v1.yaml).

  python -m research.exits.run                 # uses the committed snapshot (creates it on first run)
  python -m research.exits.run --refresh-data  # download a new frozen snapshot first

Order (each check aborts before the real result it protects):
  1. lock: prereg, exit code, engine and ifi modules match EXITS.lock
  2. engine look-ahead check (events identical on truncated data)
  3. synthetic null (martingale prices): 0 PASS among the 5 exits
  4. synthetic power (persistent trends): X10 must PASS
  5. frozen snapshot (Yahoo only)
  6. Lab parity: X3 from this simulator == ifi/backtest.py X3_target3R, trade by trade, on the real ETFs
  7. the test on real data -> reports/exits/EXITS.md + CSVs
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import zlib
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from ifi import backtest as bt
from research import engine as E
from research.checks import check_no_lookahead
from research.common import Boot
from research.exits import data as D
from research.exits import sim as S
from research.exits.synth import martingale_loader, trend_loader

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PREREG = HERE / "prereg_exits_v1.yaml"
LOCK = HERE / "EXITS.lock"
OUT = ROOT / "reports" / "exits"
LOCKED_FILES = ["research/exits/prereg_exits_v1.yaml", "research/exits/run.py", "research/exits/sim.py",
                "research/exits/data.py", "research/exits/synth.py", "research/engine.py", "research/common.py",
                "research/checks.py", "research/synthetic.py", "ifi/pine.py", "ifi/indicators.py", "ifi/states.py",
                "ifi/data.py", "ifi/backtest.py"]
COMPS = ["X8", "X9", "X10", "X11", "X12"]
PASS = "PASS"


# ------------------------------------------------------------------ lock
def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write_lock() -> str:
    LOCK.write_text("\n".join(f"{_sha(ROOT / f)}  {f}" for f in LOCKED_FILES) + "\n")
    return _sha(LOCK)


def check_lock() -> tuple[dict, str]:
    if not LOCK.exists():
        raise SystemExit("EXITS.lock missing: refusing to run")
    want = dict(reversed(line.split()[:2]) for line in LOCK.read_text().splitlines() if line.strip())
    if sorted(want) != sorted(LOCKED_FILES):
        raise SystemExit(f"EXITS.lock lists {sorted(want)}, expected {sorted(LOCKED_FILES)}")
    bad = [f for f in LOCKED_FILES if _sha(ROOT / f) != want[f]]
    if bad:
        raise SystemExit("Locked exit-test files changed after locking: " + ", ".join(bad))
    return yaml.safe_load(PREREG.read_text()), _sha(LOCK)


# ------------------------------------------------------------------ simulation over a universe
def engine_params(cfg: dict, over: dict | None = None) -> dict:
    P = dict(E.DEFAULTS)
    P.update({k: cfg["params"][k] for k in ("piv", "tol", "xb_warn", "xb_win", "ext_up", "flat", "slope_bars")})
    if over:
        P.update({k: v for k, v in over.items() if k in P})
    return P


def exit_defs(cfg: dict, over: dict | None = None, which: str | None = None) -> dict:
    X = {k: dict(v) for k, v in cfg["exits"].items()}
    if over and which:
        for k, v in over.items():
            if k in X[which]:
                X[which][k] = v
    return X


def load_frames(loader, symbols: list[str], min_bars: int) -> dict:
    F = {}
    for s in symbols:
        df = loader(s)
        if df is None or len(df) < min_bars:
            print("skip", s)
            continue
        F[s] = E.base(df)
    return F


COLS = ["sym", "seed", "t", "date", "kind", "r", "rt", "bars", "why", "e", "exit_i", "exit_date", "entry_date", "path"]
FRAMES_INDEX: dict = {}   # symbol -> DatetimeIndex of its frame (for the mark-to-market portfolio)


def run_universe(F: dict, cfg: dict, P: dict, X: dict, cost: float, kinds=S.KINDS, random_seeds=None,
                 events_cache: dict | None = None, path: bool = False) -> pd.DataFrame:
    """All eligible E4 signals (or random entries) x exits. One row per (symbol, signal bar, exit kind)."""
    start, horizon = pd.Timestamp(cfg["universe"]["start"]), max(v["time_cap"] for v in X.values())
    rows = []
    for s, x in F.items():
        key = (s, P["piv"], P["tol"], P["xb_warn"], P["xb_win"], P["ext_up"], P["flat"])
        if events_cache is not None and key in events_cache:
            ev = events_cache[key]
        else:
            ev = E.events(x, P)
            if events_cache is not None:
                events_cache[key] = ev
        A = S.arrays(x, ev)
        n = len(x)
        if random_seeds is None:
            sig = {0: np.flatnonzero(ev["reclaim"])}
        else:
            # a different random stream per symbol and seed, reproducible across runs and machines
            sig = {sd: np.flatnonzero(bt.random_setup(x, cfg["params"]["random_rate"],
                                                      sd * 100_000 + zlib.crc32(s.encode()) % 100_000).to_numpy())
                   for sd in random_seeds}
        for sd, ts in sig.items():
            for t in ts:
                if t < 250 or x.index[t] < start or t + 1 + horizon >= n:
                    continue
                for k in kinds:
                    res = S.simulate(A, int(t), k, X, P, cost, path=path)
                    if res is None or res["cancelled"]:
                        break
                    rows.append(dict(sym=s, seed=sd, t=int(t), date=x.index[t], kind=k, r=res["r"], rt=res["rt"],
                                     bars=res["bars"], why=res["why"], e=res["e"], exit_i=res["exit_i"],
                                     exit_date=x.index[res["exit_i"]], entry_date=x.index[res["e"]],
                                     path=res.get("path")))
    return pd.DataFrame(rows, columns=COLS)


def paired(tr: pd.DataFrame, k: str) -> pd.DataFrame:
    """Paired by entry: d = total-return R (exit k) - total-return R (X3); dp = the same on price-only R."""
    a = tr[tr["kind"] == k].set_index(["sym", "seed", "t"])
    b = tr[tr["kind"] == "X3"].set_index(["sym", "seed", "t"])
    j = a[["r", "rt", "date"]].join(b[["r", "rt"]], rsuffix="_3", how="inner")
    j["d"] = j["rt"] - j["rt_3"]
    j["dp"] = j["r"] - j["r_3"]
    return j.reset_index()


def portfolio(tr: pd.DataFrame, k: str, cfg: dict, start: float = 100_000.0) -> dict:
    """Fixed-fractional portfolio on DAILY MARK-TO-MARKET equity: open trades are valued at every close
    (total-return R path, dividends included); no-overlap trades per symbol; at most max_open positions;
    a trade exiting on day d frees its slot for an entry on d (as in ifi/backtest.py portfolio()); each new
    position risks risk_pct of the previous close's equity. MAR = CAGR / |max drawdown|."""
    t = tr[(tr["kind"] == k)]
    if t.empty:
        return {}
    seq = S.no_overlap(t).sort_values(["entry_date", "sym"])
    risk_pct, max_open = cfg["params"]["risk_pct"], cfg["params"]["max_open"]
    marks, cal = {}, set()
    for tid, row in seq.iterrows():
        idx = FRAMES_INDEX[row["sym"]][int(row["e"]):int(row["exit_i"]) + 1]
        marks[tid] = dict(zip(idx, row["path"]))
        cal.update(idx)
    by_entry: dict = {}
    for tid, row in seq.iterrows():
        by_entry.setdefault(row["entry_date"], []).append(tid)
    exit_of = seq["exit_date"].to_dict()
    cal = sorted(cal)
    cash, open_, last, taken = start, {}, {}, 0
    curve = [(cal[0] - pd.Timedelta(days=1), start)]   # the starting capital counts as the first high-water mark
    for d in cal:
        equity_prev = cash + sum(amt * last.get(i, 0.0) for i, amt in open_.items())
        for tid in by_entry.get(d, []):
            busy = sum(1 for i in open_ if exit_of[i] > d)
            if busy >= max_open:
                continue
            open_[tid] = risk_pct * equity_prev
            taken += 1
        for i in list(open_):
            if d in marks[i]:
                last[i] = marks[i][d]
            if exit_of[i] == d:
                cash += open_[i] * marks[i][d]
                del open_[i]
        curve.append((d, cash + sum(amt * last.get(i, 0.0) for i, amt in open_.items())))
    cv = pd.Series([v for _, v in curve], index=pd.DatetimeIndex([d for d, _ in curve]))
    years = max((cv.index[-1] - cv.index[0]).days / 365.25, 1e-9)
    cagr = (cv.iloc[-1] / start) ** (1 / years) - 1 if cv.iloc[-1] > 0 else -1.0
    dd = float((cv / cv.cummax() - 1).min())
    return dict(trades=taken, cagr=float(cagr), max_dd=dd, mar=(cagr / -dd) if dd < 0 else np.nan)


# ------------------------------------------------------------------ evaluation
def evaluate(F_etf: dict, F_stk: dict, cfg: dict, tag: str, sens: bool = True) -> dict:
    st, p = cfg["stats"], cfg["params"]
    boots = [Boot(st["reps"], st["seed"], st["k"], st["alpha"], bm) for bm in st["block_months"]]
    P0, X0 = engine_params(cfg), exit_defs(cfg)
    cache_e, cache_s = {}, {}
    FRAMES_INDEX.clear()
    FRAMES_INDEX.update({s_: x_.index for s_, x_ in F_etf.items()})
    te = run_universe(F_etf, cfg, P0, X0, p["cost_etf"], events_cache=cache_e, path=True)
    ts = run_universe(F_stk, cfg, P0, X0, p["cost_stock"], events_cache=cache_s)
    rnd = run_universe(F_etf, cfg, P0, X0, p["cost_etf"], random_seeds=p["random_seeds"], events_cache=cache_e) if tag == "real" else None
    split = pd.Timestamp(cfg["universe"]["split"])
    pf = {k: portfolio(te, k, cfg) for k in S.KINDS}
    res = {}
    for k in COMPS:
        pe, ps = paired(te, k), paired(ts, k)
        be, bs = cmean(boots, pe), cmean(boots, ps)
        bep = cmean(boots, pe, col="dp")
        halves = {}
        for lab, d in (("etf", pe), ("stk", ps)):
            halves[lab] = {h: (float(d[m]["d"].mean()) if m.any() else np.nan, int(m.sum()))
                           for h, m in (("early", d["date"] < split), ("late", d["date"] >= split))} if len(d) else {}
        e_k, e_3 = te[te["kind"] == k], te[te["kind"] == "X3"]
        cap = dict(new=float(e_k["rt"].sum() / max(e_k["bars"].sum(), 1) * 100),
                   base=float(e_3["rt"].sum() / max(e_3["bars"].sum(), 1) * 100))
        did = None
        if rnd is not None and len(rnd):
            pr = paired(rnd, k)
            if len(pr) and len(pe):
                did = boots[0].diff(pe["d"], pe["date"], pr["d"], pr["date"])
                did["rnd_mean"] = float(pr["d"].mean())
        sv = {}
        if sens:
            for name, vals in cfg["sensitivity"][k].items():
                for v in vals:
                    over = {name: v}
                    P1, X1 = engine_params(cfg, over), exit_defs(cfg, over, k)
                    t1 = run_universe(F_etf, cfg, P1, X1, p["cost_etf"], kinds=["X3", k], events_cache=cache_e)
                    d1 = paired(t1, k) if len(t1) else pd.DataFrame(columns=["d"])
                    sv[f"{name}={v}"] = float(d1["d"].mean()) if len(d1) else np.nan
        res[k] = dict(etf=be, stk=bs, etf_price=bep, n_etf=len(pe), n_stk=len(ps), halves=halves, cap=cap, pf_new=pf.get(k, {}),
                      pf_base=pf.get("X3", {}), did=did, sens=sv)
        res[k]["verdict"], res[k]["why"] = verdict(res[k], cfg)
    return dict(res=res, te=te, ts=ts, rnd=rnd, pf=pf)


def cmean(boots: list, d: pd.DataFrame, col: str = "d") -> dict:
    """Mean paired difference with the MOST CONSERVATIVE CI over the block lengths (widest interval)."""
    if d is None or not len(d):
        return dict(est=np.nan, lo=np.nan, hi=np.nan, lo_adj=np.nan, hi_adj=np.nan)
    rs = [b.mean(d[col], d["date"]) for b in boots]
    return dict(est=rs[0]["est"], lo=min(r["lo"] for r in rs), hi=max(r["hi"] for r in rs),
                lo_adj=min(r["lo_adj"] for r in rs), hi_adj=max(r["hi_adj"] for r in rs))


def verdict(r: dict, cfg: dict) -> tuple[str, list[str]]:
    st = cfg["stats"]
    hv = [v for u in ("etf", "stk") for v in r["halves"].get(u, {}).values()]
    if r["n_etf"] < st["min_n"] or r["n_stk"] < st["min_n"] or len(hv) < 4 or any(n < st["min_n_half"] for _, n in hv):
        return "INSUFFICIENT", ["below the minimum number of paired trades"]
    if r["etf"]["hi_adj"] < 0:
        return "OPPOSITE", ["ETF adjusted CI entirely below 0 (worse than X3)"]
    why = []
    if not r["etf"]["lo_adj"] > 0:
        why.append("ETF adjusted CI includes 0")
    if not r["stk"]["lo_adj"] > 0:
        why.append("stock adjusted CI includes 0")
    if not all(m > 0 for m, _ in hv):
        why.append("a time half is not positive")
    if not r["cap"]["new"] >= r["cap"]["base"]:
        why.append("R per 100 bars below X3")
    mn, mb = r["pf_new"].get("mar", np.nan), r["pf_base"].get("mar", np.nan)
    if np.isnan(mn) or np.isnan(mb):
        why.append("portfolio MAR not computable (no drawdown or no trades)")
    elif not mn >= mb:
        why.append("portfolio MAR below X3")
    if why:
        return "FAIL", why
    bad = [k for k, v in r["sens"].items() if not v > 0]
    if bad:
        return "FRAGILE", ["neighbour(s) not positive: " + ", ".join(bad)]
    return PASS, []


# ------------------------------------------------------------------ Lab parity
def lab_parity(F: dict, cfg: dict) -> tuple[bool, str]:
    """X3 from this simulator vs ifi/backtest.py X3_target3R: same trades, same R (all history, Lab sequencing)."""
    P, X, cost = engine_params(cfg), exit_defs(cfg), cfg["params"]["cost_etf"]
    total, bad = 0, []
    for s, x in F.items():
        ev = E.events(x, P)
        e4 = bt.setups(x)["E4_anchor_reclaim"].to_numpy()
        if not np.array_equal(e4, ev["reclaim"]):
            bad.append(f"{s}: E4 signals differ from the engine's reclaims")
            continue
        lab = bt.simulate(s, x, pd.Series(e4, index=x.index), "E4", "X3_target3R", cost=cost)
        A = S.arrays(x, ev)
        line = x["tr_line"].to_numpy()
        rows = []
        for t in np.flatnonzero(e4):
            if t >= len(x) - 2 or np.isnan(line[t]):
                continue
            r = S.simulate(A, int(t), "X3", X, P, cost)
            if r and not r["cancelled"]:
                rows.append(dict(sym=s, t=int(t), r=r["r"], exit_i=r["exit_i"], e=r["e"]))
        mine = S.no_overlap(pd.DataFrame(rows)) if rows else pd.DataFrame(columns=["e", "r"])
        a = [(x.index[int(e)], round(r_, 9)) for e, r_ in zip(mine["e"], mine["r"])]
        b = [(tr.entry_date, round(tr.r, 9)) for tr in lab]
        total += len(b)
        if a != b:
            bad.append(f"{s}: {len(a)} vs {len(b)} trades or R differ")
    ok = not bad
    return ok, (f"{total} Lab X3 trades reproduced exactly across {len(F)} ETFs (covers entries, stop, target, "
                "time cap, costs and sequencing; X8-X12 logic is covered by the hand-built unit tests and the "
                "truncation test)" if ok else "; ".join(bad[:5]))


# ------------------------------------------------------------------ report
def _f(v, fmt="{:+.3f}"):
    return "n/a" if v is None or (isinstance(v, float) and np.isnan(v)) else fmt.format(v)


def summary_table(tr: pd.DataFrame) -> list[str]:
    md = ["| exit | trades | mean R (with dividends) | mean R (price only) | win % | median R | mean bars | R per 100 bars | exit reasons |",
          "|---|---|---|---|---|---|---|---|---|"]
    for k in S.KINDS:
        t = tr[tr["kind"] == k]
        if t.empty:
            continue
        md.append(f"| {k} {cfg_names.get(k, '')} | {len(t):,} | {t['rt'].mean():+.3f} | {t['r'].mean():+.3f} | {100 * (t['rt'] > 0).mean():.0f} | "
                  f"{t['rt'].median():+.2f} | {t['bars'].mean():.0f} | {t['rt'].sum() / max(t['bars'].sum(), 1) * 100:+.2f} | "
                  + ", ".join(f"{a} {b}" for a, b in t["why"].value_counts().items()) + " |")
    return md


cfg_names: dict = {}


def report(out: dict, cfg: dict, meta: dict) -> str:
    R = out["res"]
    md = ["# E4 exit test v1 (pre-registered)", "",
          f"_Run {meta['run_utc']} · commit `{meta['commit'][:10]}` · lock `{meta['lock'][:16]}` · snapshot cutoff "
          f"{meta['cutoff']} (manifest `{meta['manifest'][:16]}`) · {meta['n_etf']} ETFs, {meta['n_stk']} stocks · "
          f"Bonferroni k = {cfg['stats']['k']} · {cfg['stats']['reps']:,} draws; CI = widest of {cfg['stats']['block_months']}-month blocks · "
          f"{meta['versions']}_", "", "## Validity", "", "| check | result |", "|---|---|"]
    md += [f"| {a} | {b} |" for a, b in meta["validity"]]
    md += ["", "## Verdicts (each exit vs X3 = 3R target / 60 bars, paired on the same E4 entries)", "",
           "dR = difference in R per trade, dividends received during the hold included (price-only dR shown too). "
           "Portfolio MAR uses daily mark-to-market equity.", "",
           "| exit | ETF trades | ETF dR | adj. CI | price-only dR | ETF 2000-14 · 2015- | stock dR | stock adj. CI | stock halves | "
           "R/100 bars (exit vs X3) | portfolio MAR (exit vs X3) | random-entry dR · E4 minus random (95% CI) | verdict |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for k in COMPS:
        r = R[k]
        he, hs = r["halves"].get("etf", {}), r["halves"].get("stk", {})
        did = r["did"]
        dtxt = (f"{did['rnd_mean']:+.3f} · {did['est']:+.3f} ({did['lo']:+.3f} … {did['hi']:+.3f})"
                + (" beyond drift" if did["lo"] > 0 else "")) if did else "n/a"
        why = f" ({'; '.join(r['why'])})" if r["why"] else ""
        md.append(f"| {k} {cfg_names[k]} | {r['n_etf']:,} | {_f(r['etf']['est'])} | {_f(r['etf']['lo_adj'])} … {_f(r['etf']['hi_adj'])} | "
                  f"{_f(r['etf_price']['est'])} | "
                  f"{_f(he.get('early', (np.nan,))[0])} · {_f(he.get('late', (np.nan,))[0])} | {_f(r['stk']['est'])} | "
                  f"{_f(r['stk']['lo_adj'])} … {_f(r['stk']['hi_adj'])} | {_f(hs.get('early', (np.nan,))[0])} · {_f(hs.get('late', (np.nan,))[0])} | "
                  f"{r['cap']['new']:+.2f} vs {r['cap']['base']:+.2f} | {_f(r['pf_new'].get('mar'), '{:.2f}')} vs "
                  f"{_f(r['pf_base'].get('mar'), '{:.2f}')} | {dtxt} | **{r['verdict']}**{why} |")
    passed = [k for k in COMPS if R[k]["verdict"] == PASS]
    md += ["", "## Decision (written before the results)", ""]
    if passed:
        best = max(passed, key=lambda k: R[k]["pf_new"].get("mar", -np.inf))
        md.append(f"- **{best} ({cfg_names[best]})** has the highest ETF portfolio MAR among the passing exits. "
                  + cfg["decisions"]["pass"])
    else:
        md.append("- No exit passed. " + cfg["decisions"]["fail"])
    md += ["", "## Exits on E4 entries: ETFs", ""] + summary_table(out["te"])
    md += ["", "## Exits on E4 entries: stocks (survivorship-biased list; replication only)", ""] + summary_table(out["ts"])
    md += ["", "## Portfolio check (ETFs, no-overlap trades, 0.75% risk, max 5 open, daily mark-to-market, dividends included)", "",
           "| exit | trades | CAGR | max drawdown | MAR |", "|---|---|---|---|---|"]
    for k in S.KINDS:
        pf = out["pf"].get(k, {})
        if pf:
            md.append(f"| {k} {cfg_names[k]} | {pf['trades']:,} | {100 * pf['cagr']:.1f}% | {100 * pf['max_dd']:.1f}% | {pf['mar']:.2f} |")
    md += ["", "## Sensitivity (ETF mean dR at each neighbour; a PASS needs every one > 0)", "", "| exit | neighbour | dR |", "|---|---|---|"]
    for k in COMPS:
        for nm, v in R[k]["sens"].items():
            md.append(f"| {k} | {nm} | {_f(v)} |")
    if out["rnd"] is not None and len(out["rnd"]):
        md += ["", "## Random-entry control (ETFs, same exits; how much of an exit's gain any long entry would get)", ""]
        md += summary_table(out["rnd"])
    return "\n".join(md) + "\n"


# ------------------------------------------------------------------ main
def _commit() -> str:
    if os.environ.get("GITHUB_SHA"):
        return os.environ["GITHUB_SHA"]
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return "local"


def _versions() -> str:
    import matplotlib, numpy, pandas, scipy  # noqa: E401
    return (f"Python {sys.version.split()[0]}, pandas {pandas.__version__}, numpy {numpy.__version__}, "
            f"scipy {scipy.__version__}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh-data", action="store_true")
    a = ap.parse_args()
    cfg, lock = check_lock()
    cfg_names.update({k: v["name"] for k, v in cfg["exits"].items()})
    print(f"[1/7] lock ok ({lock})")
    validity = [("Lock (prereg, exit code, engine, ifi modules)", f"ok `{lock[:16]}`")]
    ok, msgs = check_no_lookahead(engine_params(cfg))
    print("[2/7] look-ahead:", "ok" if ok else "FAILED", msgs[-1])
    if not ok:
        print("ABORT: look-ahead check failed")
        return 1
    validity.append(("Engine look-ahead (truncation)", "ok: " + msgs[-1]))
    U = cfg["universe"]
    n_syn = 30  # synthetic checks use the 17 ETF names and the first 30 stock names
    for name, loader, need in (("null (martingale prices)", martingale_loader(3), None),
                               ("power (persistent trends)", trend_loader(5), "X10")):
        Fe = load_frames(loader, U["etfs"], U["min_bars"])
        Fs = load_frames(loader, U["stocks"][:n_syn], U["min_bars"])
        o = evaluate(Fe, Fs, cfg, tag="synthetic")
        v = {k: o["res"][k]["verdict"] for k in COMPS}
        if need is None:
            ok = not any(x == PASS for x in v.values())
        else:
            ok = v[need] == PASS
        print(f"[{3 if need is None else 4}/7] {name}:", "ok" if ok else "FAILED", v)
        if not ok:
            print("ABORT: synthetic", name, "check failed")
            return 1
        validity.append((f"Synthetic {name}", "ok: " + ", ".join(f"{k} {x}" for k, x in v.items())
                         + ("" if need is None else f" (required: {need} PASS)")))
    syms = U["etfs"] + U["stocks"]
    if a.refresh_data or D.manifest() is None:
        man = D.make_snapshot(syms)
        print(f"[5/7] new snapshot, cutoff {man['cutoff']}, {len(man['files'])} symbols")
    man = D.manifest()
    if man.get("source") != D.SOURCE:
        print(f"ABORT: the exit-test snapshot is not Yahoo market data (source: {man.get('source')}). "
              "Delete research/exits/snapshot and run with refresh_data.")
        return 1
    missing = [s for s in syms if s not in man["files"]]
    print(f"[5/7] snapshot cutoff {man['cutoff']} · manifest {D.manifest_hash()[:16]} · missing: {missing or 'none'}")
    validity.append(("Frozen snapshot", f"cutoff {man['cutoff']} · {len(man['files'])} symbols · missing: {', '.join(missing) or 'none'}"))
    Fe = load_frames(D.load, U["etfs"], U["min_bars"])
    Fs = load_frames(D.load, U["stocks"], U["min_bars"])
    no_div = [s_ for s_, x_ in {**Fe, **Fs}.items() if "adjclose" not in x_.columns or x_["adjclose"].isna().all()]
    if no_div:
        print("ABORT: no Adj Close (dividend data) for", no_div, "- the pre-registered measure needs it")
        return 1
    validity.append(("Dividend data (Adj Close)", f"present for all {len(Fe) + len(Fs)} symbols"))
    ok, msg = lab_parity(Fe, cfg)
    print("[6/7] Lab parity:", "ok" if ok else "FAILED", msg)
    if not ok:
        print("ABORT: the simulator does not reproduce the Lab's X3 trades")
        return 1
    validity.append(("Lab parity (X3 vs ifi/backtest.py X3_target3R)", "ok: " + msg))
    out = evaluate(Fe, Fs, cfg, tag="real")
    OUT.mkdir(parents=True, exist_ok=True)
    meta = dict(run_utc=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"), commit=_commit(), lock=lock,
                cutoff=man["cutoff"], manifest=D.manifest_hash(), n_etf=len(Fe), n_stk=len(Fs), versions=_versions(),
                validity=validity)
    (OUT / "EXITS.md").write_text(report(out, cfg, meta))
    out["te"].to_csv(OUT / "EXITS_trades_etf.csv", index=False)
    out["ts"].to_csv(OUT / "EXITS_trades_stocks.csv", index=False)
    rows = []
    for k in COMPS:
        r = out["res"][k]
        rows.append(dict(exit=k, verdict=r["verdict"], why="; ".join(r["why"]), n_etf=r["n_etf"], etf_dR=r["etf"]["est"],
                         etf_lo_adj=r["etf"]["lo_adj"], etf_hi_adj=r["etf"]["hi_adj"], n_stk=r["n_stk"], stk_dR=r["stk"]["est"],
                         stk_lo_adj=r["stk"]["lo_adj"], r100_new=r["cap"]["new"], r100_x3=r["cap"]["base"],
                         mar_new=r["pf_new"].get("mar"), mar_x3=r["pf_base"].get("mar")))
    pd.DataFrame(rows).to_csv(OUT / "EXITS_results.csv", index=False)
    (OUT / "EXITS_meta.json").write_text(json.dumps(dict(meta, verdicts={k: out["res"][k]["verdict"] for k in COMPS}),
                                                    indent=1, default=str))
    print("[7/7] written:", {k: out["res"][k]["verdict"] for k in COMPS})
    return 0


if __name__ == "__main__":
    if "--write-lock" in sys.argv:
        print("lock", write_lock())
        sys.exit(0)
    sys.exit(main())
