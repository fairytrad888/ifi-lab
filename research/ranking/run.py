"""Ranking test v1 runner (research/ranking/prereg_ranking_v1.yaml): which E4 signals should take the 5 slots?
The rule tested (F1) skips extended and stage-0 signals so their slots go to better ones.

  python -m research.ranking.run            (or Actions -> Research -> step = ranking)

Order (each check aborts before the real result it protects):
  1. lock: prereg, ranking code, exit simulator, engine and ifi modules match RANKING.lock (and EXITS.lock)
  2. engine look-ahead check (events identical on truncated data)
  3. synthetic nulls (martingale prices; persistent trends with nothing planted): F1 must not PASS
  4. synthetic power (persistent trends, -0.5 R planted on the trades F1 skips): F1 must PASS
  5. frozen snapshot: Yahoo source and the pre-registered manifest prefix (never refreshed here)
  6. baseline parity: the uncapped first-come book equals research/exits/run.py portfolio() exactly
  7. the test on real data -> reports/ranking/RANKING.md + CSVs
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

from research.checks import check_no_lookahead
from research.common import month_ids
from research.exits import data as D
from research.exits import run as XR
from research.exits import sim as S
from research.exits.synth import martingale_loader, trend_loader

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PREREG = HERE / "prereg_ranking_v1.yaml"
LOCK = HERE / "RANKING.lock"
OUT = ROOT / "reports" / "ranking"
LOCKED_FILES = ["research/ranking/prereg_ranking_v1.yaml", "research/ranking/run.py",
                "research/exits/prereg_exits_v1.yaml", "research/exits/run.py", "research/exits/sim.py",
                "research/exits/data.py", "research/exits/synth.py", "research/engine.py", "research/common.py",
                "research/checks.py", "research/synthetic.py", "ifi/pine.py", "ifi/indicators.py", "ifi/states.py",
                "ifi/data.py", "ifi/backtest.py"]
ARMS = ["F1"]
PASS, FAIL, INSUFFICIENT = "PASS", "FAIL", "INSUFFICIENT"


# ------------------------------------------------------------------ lock
def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write_lock() -> str:
    LOCK.write_text("\n".join(f"{_sha(ROOT / f)}  {f}" for f in LOCKED_FILES) + "\n")
    return _sha(LOCK)


def check_lock() -> tuple[dict, dict, str]:
    if not LOCK.exists():
        raise SystemExit("RANKING.lock missing: refusing to run")
    want = dict(reversed(line.split()[:2]) for line in LOCK.read_text().splitlines() if line.strip())
    if sorted(want) != sorted(LOCKED_FILES):
        raise SystemExit(f"RANKING.lock lists {sorted(want)}, expected {sorted(LOCKED_FILES)}")
    bad = [f for f in LOCKED_FILES if _sha(ROOT / f) != want[f]]
    if bad:
        raise SystemExit("Locked ranking-test files changed after locking: " + ", ".join(bad))
    cfgX, _ = XR.check_lock()
    return yaml.safe_load(PREREG.read_text()), cfgX, _sha(LOCK)


# ------------------------------------------------------------------ trades with signal-close features
def features(x: pd.DataFrame, t: int) -> dict:
    """Known at the close of signal bar t; the same formulas as the live paper tags (ifi/allocation.py tags)."""
    c, atr = float(x["close"].iloc[t]), float(x["atr"].iloc[t])
    stop = float(x["low"].iloc[max(0, t - 4):t + 1].min()) - 0.5 * atr
    d = x["dist_anchor_atr"].iloc[t]
    return dict(dist=float(d) if pd.notna(d) else np.nan, stage=int(x["stage"].iloc[t]), width=(c - stop) / c)


def build_trades(F: dict, cfgX: dict, cost: float, random_seeds=None) -> pd.DataFrame:
    """Every E4 signal (or random entry) with its X3 trade, total-return path, features and fill-based stop width."""
    P = XR.engine_params(cfgX)
    X = {"X3": XR.exit_defs(cfgX)["X3"]}
    XR.FRAMES_INDEX.update({s: x.index for s, x in F.items()})
    cache: dict = {}
    tr = XR.run_universe(F, cfgX, P, X, cost, kinds=["X3"], random_seeds=random_seeds, events_cache=cache,
                         path=random_seeds is None)
    if tr.empty:
        return tr
    feats, wfill, arr = [], [], {}
    for r in tr.itertuples():
        x = F[r.sym]
        feats.append(features(x, int(r.t)))
        if r.sym not in arr:
            arr[r.sym] = S.arrays(x, cache[(r.sym, P["piv"], P["tol"], P["xb_warn"], P["xb_win"], P["ext_up"], P["flat"])])
        A = arr[r.sym]
        fill, stop = A["o"][r.e], A["low5"][r.t] - 0.5 * A["atr"][r.t]
        wfill.append((fill - stop) / fill)
    tr = pd.concat([tr.reset_index(drop=True), pd.DataFrame(feats)], axis=1)
    tr["width_fill"] = wfill
    tr["kind"] = "X3"
    return tr


# ------------------------------------------------------------------ the book
class Book:
    """Daily mark-to-market book over one universe's E4 signals, with the Lab's rules (research/exits/run.py
    portfolio()): one open trade per symbol, at most max_open positions, a trade exiting on day d frees its
    slot for an entry on d, each new position risks risk_pct of the previous close's equity. Two additions,
    both pre-registered: the order of same-day entries (priority key, then symbol) and an optional notional cap
    (position value <= cap x equity, so a stop too tight for the risk scales the position down)."""

    def __init__(self, T: pd.DataFrame, risk: float, max_open: int):
        self.T = T.reset_index(drop=True)
        self.risk, self.max_open = risk, max_open
        self.marks, cal = {}, set()
        for i, r in self.T.iterrows():
            idx = XR.FRAMES_INDEX[r["sym"]][int(r["e"]):int(r["exit_i"]) + 1]
            self.marks[i] = dict(zip(idx, r["path"]))
            cal.update(idx)
        self.cal = sorted(cal)         # common calendar: every day any signal's trade is open
        self.wf = self.T["width_fill"].to_numpy(float)
        self.sym, self.t = self.T["sym"].to_numpy(), self.T["t"].to_numpy()
        self.exit_i, self.entry = self.T["exit_i"].to_numpy(), self.T["entry_date"].to_numpy()
        self.exit_d = dict(enumerate(self.T["exit_date"]))

    def sequence(self, keep=None) -> np.ndarray:
        """Lab sequencing per symbol (research/exits/sim.py no_overlap): after a trade, the symbol's next signal
        is taken only from its exit bar onward. Filters apply first, so a filtered signal frees its symbol."""
        idx = np.arange(len(self.T)) if keep is None else np.flatnonzero(np.asarray(keep, bool))
        order = idx[np.lexsort((self.t[idx], self.sym[idx]))]
        out, cur, nxt = [], None, -1
        for i in order:
            if self.sym[i] != cur:
                cur, nxt = self.sym[i], -1
            if self.t[i] >= nxt:
                out.append(i)
                nxt = self.exit_i[i]
        return np.array(out, int)

    def run(self, keep=None, prio=None, cap=None, own_calendar: bool = False, curve: bool = False) -> dict:
        seq = self.sequence(keep)
        pr_ = np.zeros(len(self.T)) if prio is None else np.asarray(prio, float)
        seq = seq[np.lexsort((self.sym[seq], pr_[seq], self.entry[seq]))]     # entry date, then priority, then symbol
        cal = sorted({d for i in seq for d in self.marks[i]}) if own_calendar else self.cal
        by_entry: dict = {}
        for i in seq:
            by_entry.setdefault(self.entry[i], []).append(i)
        by_entry = {pd.Timestamp(k): v for k, v in by_entry.items()}
        exit_of = self.exit_d
        scale = np.minimum(1.0, cap * self.wf / self.risk) if cap else np.ones(len(self.T))
        cash, open_, last, taken, start = 100_000.0, {}, {}, [], 100_000.0
        days, vals, expo = [cal[0] - pd.Timedelta(days=1)], [start], []
        for d in cal:
            equity_prev = cash + sum(amt * last.get(i, 0.0) for i, amt in open_.items())
            for i in by_entry.get(d, ()):
                busy = sum(1 for j in open_ if exit_of[j] > d)
                if busy >= self.max_open:
                    continue
                open_[i] = self.risk * equity_prev * scale[i]
                taken.append(i)
            notional = sum(amt / max(self.wf[i], 1e-9) for i, amt in open_.items())
            for i in list(open_):
                m = self.marks[i].get(d)
                if m is not None:
                    last[i] = m
                if exit_of[i] == d:
                    cash += open_[i] * m
                    del open_[i]
            days.append(d)
            vals.append(cash + sum(amt * last.get(i, 0.0) for i, amt in open_.items()))
            expo.append(notional / max(equity_prev, 1e-9))
        cv = pd.Series(vals, index=pd.DatetimeIndex(days))
        out = dict(trades=len(taken), taken=frozenset(int(i) for i in taken), exposure=float(np.mean(expo)) if expo else np.nan,
                   **mar_of(cv))
        if curve:
            out["curve"] = cv
        return out


def mar_of(cv: pd.Series) -> dict:
    years = max((cv.index[-1] - cv.index[0]).days / 365.25, 1e-9)
    cagr = (cv.iloc[-1] / cv.iloc[0]) ** (1 / years) - 1 if cv.iloc[-1] > 0 else -1.0
    dd = float((cv / cv.cummax() - 1).min())
    return dict(cagr=float(cagr), max_dd=dd, mar=(cagr / -dd) if dd < 0 else np.nan)


def halves(cv: pd.Series, split: pd.Timestamp) -> tuple[float, float]:
    a = cv[cv.index < split]
    b = cv[cv.index >= split]
    if len(a) and len(b):
        b = pd.concat([a.iloc[[-1]], b])      # the second half starts from the first half's last value
    return (mar_of(a)["mar"] if len(a) > 1 else np.nan), (mar_of(b)["mar"] if len(b) > 1 else np.nan)


# ------------------------------------------------------------------ arms and controls
def arm_inputs(T: pd.DataFrame, arm: str, pr: dict) -> tuple:
    """(keep mask, same-day priority). F1 is a filter: keep everything except the signals its rule skips."""
    p = pr["params"]
    if arm != "F1":
        raise ValueError(arm)
    drop = (T["dist"] > p["dist_max"]) | (T["stage"] < p["stage_min"])
    return (~drop).to_numpy(), None


def controls(book: Book, T: pd.DataFrame, arm: str, pr: dict, cap) -> np.ndarray:
    c = pr["controls"]
    rng = np.random.default_rng(c["seed"] + ARMS.index(arm))
    keep, _ = arm_inputs(T, arm, pr)
    out = []
    for _ in range(c["draws"]):
        if keep is None:
            out.append(book.run(prio=rng.random(len(T)), cap=cap)["mar"])
        else:
            share = 1 - keep.mean()
            out.append(book.run(keep=rng.random(len(T)) >= share, cap=cap)["mar"])
    return np.array(out, float)


def boot_dmar(ca: pd.Series, cb: pd.Series, pr: dict) -> tuple[float, float]:
    """Paired calendar-block bootstrap of daily equity returns -> 95% interval of MAR(a) - MAR(b). Report only."""
    p = pr["params"]
    ra, rb = ca.pct_change().iloc[1:].to_numpy(), cb.pct_change().iloc[1:].to_numpy()
    ids = month_ids(ca.index[1:], p["boot_block_months"])
    blocks = [np.flatnonzero(ids == b) for b in np.unique(ids)]
    rng = np.random.default_rng(p["support_seed"])
    out = []
    for _ in range(p["boot_reps"]):
        pick = np.concatenate([blocks[j] for j in rng.integers(0, len(blocks), len(blocks))])
        m = []
        for r in (ra, rb):
            eq = np.cumprod(1 + r[pick])
            yrs = len(pick) / 252
            cagr = eq[-1] ** (1 / yrs) - 1 if eq[-1] > 0 else -1.0
            dd = float((eq / np.maximum.accumulate(np.r_[1.0, eq])[1:] - 1).min())
            m.append(cagr / -dd if dd < 0 else np.nan)
        out.append(m[0] - m[1])
    return float(np.nanquantile(out, 0.025)), float(np.nanquantile(out, 0.975))


def evaluate(Te: pd.DataFrame, Ts: pd.DataFrame, pr: dict, with_boot: bool = False, arms=ARMS) -> dict:
    """The pre-registered gates for each arm. Ts = stocks (primary), Te = ETFs (consistency)."""
    p = pr["params"]
    a_adj = p["alpha"] / p["k"]
    split = pd.Timestamp(p["split"])
    bs, be = Book(Ts, p["risk_pct"], p["max_open"]), Book(Te, p["risk_pct"], p["max_open"])
    cap = p["notional_cap"]
    base = dict(s_cap=bs.run(cap=cap, curve=True), s_unc=bs.run(), e_cap=be.run(cap=cap))
    res = {}
    for arm in arms:
        ks, ps = arm_inputs(Ts, arm, pr)
        ke, pe = arm_inputs(Te, arm, pr)
        s_cap = bs.run(keep=ks, prio=ps, cap=cap, curve=True)
        s_unc = bs.run(keep=ks, prio=ps)
        e_cap = be.run(keep=ke, prio=pe, cap=cap)
        ctrl = controls(bs, Ts, arm, pr, cap)
        q = float(np.nanquantile(ctrl, 1 - a_adj))
        h_arm, h_base = halves(s_cap["curve"], split), halves(base["s_cap"]["curve"], split)
        changed = len(s_cap["taken"] ^ base["s_cap"]["taken"])
        gates = {
            "information": bool(s_cap["mar"] > q),
            "both halves": bool(h_arm[0] - h_base[0] > 0 and h_arm[1] - h_base[1] > 0),
            "sizing (uncapped)": bool(s_unc["mar"] - base["s_unc"]["mar"] > 0),
            "consistency (ETFs)": bool(e_cap["mar"] - base["e_cap"]["mar"] > 0),
        }
        if changed < p["min_changed"]:
            verdict = INSUFFICIENT
        else:
            verdict = PASS if all(gates.values()) else FAIL
        r = dict(verdict=verdict, gates=gates, changed=changed, q=q, ctrl_median=float(np.nanmedian(ctrl)),
                 pct=float(np.mean(ctrl < s_cap["mar"])), s_cap=s_cap, s_unc=s_unc, e_cap=e_cap,
                 halves=h_arm, base_halves=h_base, drop_share=(float(1 - ks.mean()) if ks is not None else None))
        if with_boot:
            r["boot"] = boot_dmar(s_cap["curve"], base["s_cap"]["curve"], pr)
        res[arm] = r
    return dict(res=res, base=base, base_pct=None)


# ------------------------------------------------------------------ synthetic checks
def plant(T: pd.DataFrame, arm: str, pr: dict, delta: float = -0.5) -> pd.DataFrame:
    """Planted effect for the power check: delta R on the trades the arm's hypothesis says are worse."""
    keep, _ = arm_inputs(T, arm, pr)
    bad = pd.Series(~keep, index=T.index)
    T = T.copy()
    paths = []
    for b, path in zip(bad, T["path"]):
        path = np.asarray(path, float)
        if b and len(path):
            path = path + delta * np.linspace(1 / len(path), 1.0, len(path))
        paths.append(path)
    T["path"] = paths
    T.loc[bad, "rt"] = T.loc[bad, "rt"] + delta
    return T


# ------------------------------------------------------------------ supporting per-trade checks
def block_diff(groups: list[tuple[np.ndarray, np.ndarray, float]], bm: int, reps: int, seed: int) -> dict:
    """sum_g sign_g * mean(values_g), groups resampled jointly by calendar blocks; unadjusted 95% interval."""
    ids_all = np.concatenate([month_ids(d, bm) for _, d, _ in groups])
    blocks = np.unique(ids_all)
    pos = {b: i for i, b in enumerate(blocks)}
    K = len(blocks)
    est, sums = 0.0, []
    for v, d, sgn in groups:
        v = np.asarray(v, float)
        ok = ~np.isnan(v)
        ix = np.array([pos[m] for m in month_ids(np.asarray(d)[ok], bm)], int)
        if not ok.any():
            return dict(est=np.nan, lo=np.nan, hi=np.nan, n=[len(g[0]) for g in groups])
        est += sgn * v[ok].mean()
        sums.append((np.bincount(ix, v[ok], K), np.bincount(ix, None, K), sgn))
    rng = np.random.default_rng(seed)
    W = np.zeros((reps, K))
    draw = rng.integers(0, K, size=(reps, K))
    for j in range(K):
        np.add.at(W, (np.arange(reps), draw[:, j]), 1)
    tot = np.zeros(reps)
    for s_, n_, sgn in sums:
        den = W @ n_
        with np.errstate(invalid="ignore", divide="ignore"):
            tot += sgn * np.where(den > 0, (W @ s_) / den, np.nan)
    return dict(est=float(est), lo=float(np.nanquantile(tot, 0.025)), hi=float(np.nanquantile(tot, 0.975)),
                n=[int((~np.isnan(np.asarray(g[0], float))).sum()) for g in groups])


def supporting(Ts: pd.DataFrame, Rs: pd.DataFrame, pr: dict) -> dict:
    p = pr["params"]
    bm, reps, seed = p["boot_block_months"], p["support_reps"], p["support_seed"]
    L = S.no_overlap(Ts)
    out = {}
    hi, lo_ = L[L["dist"] > p["dist_max"]], L[L["dist"] <= p["dist_max"]]
    out["C5"] = block_diff([(hi["rt"], hi["date"], 1), (lo_["rt"], lo_["date"], -1)], bm, reps, seed)
    s0, s1 = L[L["stage"] < p["stage_min"]], L[L["stage"] >= p["stage_min"]]
    out["C6"] = block_diff([(s0["rt"], s0["date"], 1), (s1["rt"], s1["date"], -1)], bm, reps, seed)
    cuts = np.quantile(L["width"], [0.2, 0.8])
    R = pd.concat([S.no_overlap(g) for _, g in Rs.groupby("seed")]) if len(Rs) else Rs
    en, ew = L[L["width"] <= cuts[0]], L[L["width"] >= cuts[1]]
    rn, rw = R[R["width"] <= cuts[0]], R[R["width"] >= cuts[1]]
    out["C3b"] = block_diff([(en["rt"], en["date"], 1), (ew["rt"], ew["date"], -1),
                             (rn["rt"], rn["date"], -1), (rw["rt"], rw["date"], 1)], bm, reps, seed)
    out["C3b"]["parts"] = dict(e4_narrow=float(en["rt"].mean()), e4_wide=float(ew["rt"].mean()),
                               rnd_narrow=float(rn["rt"].mean()), rnd_wide=float(rw["rt"].mean()),
                               cut_narrow=float(cuts[0]), cut_wide=float(cuts[1]))
    out["C5"]["parts"] = dict(above=float(hi["rt"].mean()), below=float(lo_["rt"].mean()))
    out["C6"]["parts"] = dict(stage0=float(s0["rt"].mean()), stage1plus=float(s1["rt"].mean()))
    return out


# ------------------------------------------------------------------ report
def _f(v, d=3, pct=False):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "–"
    return f"{100 * v:.1f}%" if pct else f"{v:+.{d}f}"


def report(out: dict, sup: dict, comb: dict, pr: dict, meta: dict) -> str:
    res, base = out["res"], out["base"]
    p = pr["params"]
    md = ["# Ranking test v1: which E4 signals should take the 5 slots?", "",
          f"_Run {meta['run_utc']} · commit `{meta['commit']}` · lock `{meta['lock'][:16]}` · snapshot cutoff {meta['cutoff']} "
          f"(manifest `{meta['manifest'][:16]}`) · {meta['n_stk']} stocks (primary) + {meta['n_etf']} ETFs (consistency) · "
          f"risk {100 * p['risk_pct']:.2f}%, max {p['max_open']} open, notional cap {100 * p['notional_cap']:.0f}% per position_", "",
          "Pre-registered in `research/ranking/prereg_ranking_v1.yaml`. The hypotheses came from the ETF profile, so ETFs "
          "only have to agree in sign; the stock universe, whose context slices were never inspected, is the evidence.", "",
          "## Validity", "", "| check | result |", "|---|---|"]
    md += [f"| {a} | {b} |" for a, b in meta["validity"]]
    md += ["", "## Verdict", "", "| arm | rule | verdict | information | both halves | sizing (uncapped) | consistency (ETFs) | stock trades changed |",
           "|---|---|---|---|---|---|---|---|"]
    rules = {"F1": f"skip signals more than {p['dist_max']} ATR above the anchor or at stage < {p['stage_min']}"}
    yn = lambda b: "yes" if b else "no"
    for a in ARMS:
        r = res[a]
        g = r["gates"]
        md.append(f"| {a} | {rules[a]} | **{r['verdict']}** | {yn(g['information'])} | {yn(g['both halves'])} | "
                  f"{yn(g['sizing (uncapped)'])} | {yn(g['consistency (ETFs)'])} | {r['changed']} |")
    md += ["", "Design note: same-day ranking arms were dropped before this run because the synthetic power check showed they "
           "cannot move portfolio MAR (see design_history in the pre-registration).",
           "", "## Stocks, capped (the primary book)", "",
           "| book | trades | CAGR | max drawdown | MAR | avg exposure | MAR 2000-14 | MAR 2015- | random-control median MAR | control quantile to beat | arm percentile in controls |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    b = base["s_cap"]
    bh = halves(b["curve"], pd.Timestamp(p["split"]))
    md.append(f"| baseline (first-come) | {b['trades']:,} | {_f(b['cagr'], pct=True)} | {_f(b['max_dd'], pct=True)} | {b['mar']:.3f} | "
              f"{_f(b['exposure'], pct=True)} | {bh[0]:.3f} | {bh[1]:.3f} | – | – | – |")
    for a in ARMS:
        r = res[a]
        s = r["s_cap"]
        md.append(f"| {a} | {s['trades']:,} | {_f(s['cagr'], pct=True)} | {_f(s['max_dd'], pct=True)} | {s['mar']:.3f} | "
                  f"{_f(s['exposure'], pct=True)} | {r['halves'][0]:.3f} | {r['halves'][1]:.3f} | {r['ctrl_median']:.3f} | {r['q']:.3f} | {100 * r['pct']:.1f}% |")
    if any("boot" in res[a] for a in ARMS):
        md += ["", "Paired calendar-block bootstrap of daily returns (6-month blocks; reported, not gating): 95% interval of arm MAR − baseline MAR:"]
        md += [f"- {a}: {_f(res[a]['boot'][0])} to {_f(res[a]['boot'][1])}" for a in ARMS if "boot" in res[a]]
    md += ["", f"F1 skips {100 * res['F1']['drop_share']:.1f}% of stock E4 signals; its control skips the same share at random "
           f"({pr['controls']['draws']} draws)."]
    md += ["", "## Sign checks: uncapped stocks, capped ETFs, and one combined book (78 symbols)", "",
           "| book | baseline MAR | " + " | ".join(ARMS) + " |", "|---|---|" + "---|" * len(ARMS)]
    md.append(f"| stocks, uncapped | {base['s_unc']['mar']:.3f} | " + " | ".join(f"{res[a]['s_unc']['mar']:.3f}" for a in ARMS) + " |")
    md.append(f"| ETFs, capped | {base['e_cap']['mar']:.3f} | " + " | ".join(f"{res[a]['e_cap']['mar']:.3f}" for a in ARMS) + " |")
    if comb:
        md.append(f"| combined, capped (report only) | {comb['base']['mar']:.3f} | " + " | ".join(f"{comb[a]['mar']:.3f}" for a in ARMS) + " |")
        md.append(f"| combined, capped: CAGR / max DD | {_f(comb['base']['cagr'], pct=True)} / {_f(comb['base']['max_dd'], pct=True)} | "
                  + " | ".join(f"{_f(comb[a]['cagr'], pct=True)} / {_f(comb[a]['max_dd'], pct=True)}" for a in ARMS) + " |")
    md += ["", "## Supporting per-trade checks (stocks, one open trade per symbol; unadjusted 95% intervals; not gating)", "",
           "| check | measure | estimate | 95% interval | parts |", "|---|---|---|---|---|"]
    c5, c6, c3 = sup["C5"], sup["C6"], sup["C3b"]
    md.append(f"| C5 | mean R (dist > {p['dist_max']}) − mean R (dist ≤ {p['dist_max']}) | {_f(c5['est'])} | {_f(c5['lo'])} to {_f(c5['hi'])} | "
              f"{_f(c5['parts']['above'])} (n {c5['n'][0]}) vs {_f(c5['parts']['below'])} (n {c5['n'][1]}) |")
    md.append(f"| C6 | mean R (stage < {p['stage_min']}) − mean R (stage ≥ {p['stage_min']}) | {_f(c6['est'])} | {_f(c6['lo'])} to {_f(c6['hi'])} | "
              f"{_f(c6['parts']['stage0'])} (n {c6['n'][0]}) vs {_f(c6['parts']['stage1plus'])} (n {c6['n'][1]}) |")
    pt = c3["parts"]
    md.append(f"| C3b | (E4 narrow − wide) − (random narrow − wide) | {_f(c3['est'])} | {_f(c3['lo'])} to {_f(c3['hi'])} | "
              f"E4 {_f(pt['e4_narrow'])} / {_f(pt['e4_wide'])}; random {_f(pt['rnd_narrow'])} / {_f(pt['rnd_wide'])}; "
              f"narrow ≤ {100 * pt['cut_narrow']:.1f}%, wide ≥ {100 * pt['cut_wide']:.1f}% of price |")
    passed = [a for a in ARMS if res[a]["verdict"] == PASS]
    md += ["", "## Decision", ""]
    if passed:
        md.append(pr["decisions"]["pass"])
    else:
        md.append(pr["decisions"]["fail"])
    return "\n".join(md) + "\n"


def _commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return "unknown"


# ------------------------------------------------------------------ main
def synthetic_checks(pr: dict, cfgX: dict) -> tuple[bool, list]:
    U, msgs = cfgX["universe"], []
    worlds = {}
    for name, loader in (("martingale prices", martingale_loader(3)), ("persistent trends", trend_loader(5))):
        Fe = XR.load_frames(loader, U["etfs"], U["min_bars"])
        Fs = XR.load_frames(loader, U["stocks"], U["min_bars"])
        worlds[name] = (build_trades(Fe, cfgX, cfgX["params"]["cost_etf"]), build_trades(Fs, cfgX, cfgX["params"]["cost_stock"]))
    v = {}
    for name, (Te, Ts) in worlds.items():
        v[name] = evaluate(Te, Ts, pr)["res"]["F1"]["verdict"]
    ok_null = not any(x == PASS for x in v.values())
    print("[3/7] synthetic nulls:", "ok" if ok_null else "FAILED", v)
    msgs.append(("Synthetic nulls (nothing planted)", ("ok: " if ok_null else "FAILED: ") + ", ".join(f"{k}: F1 {x}" for k, x in v.items())
                 + " (required: no PASS)"))
    if not ok_null:
        return False, msgs
    d = pr["params"]["power_delta"]
    Te, Ts = worlds["persistent trends"]
    o = evaluate(plant(Te, "F1", pr, d), plant(Ts, "F1", pr, d), pr)["res"]["F1"]
    ok_pow = o["verdict"] == PASS
    print(f"[4/7] synthetic power ({d:+.1f} R planted on the skipped trades):", "ok" if ok_pow else "FAILED", o["verdict"],
          f"(percentile in controls {100 * o['pct']:.1f}%)")
    msgs.append((f"Synthetic power (persistent trends, {d:+.1f} R planted on the trades F1 skips)",
                 ("ok: " if ok_pow else "FAILED: ") + f"F1 {o['verdict']}, percentile in random-drop controls {100 * o['pct']:.1f}% (required: PASS)"))
    return ok_pow, msgs


def main() -> int:
    pr, cfgX, lock = check_lock()
    print(f"[1/7] lock ok ({lock})")
    validity = [("Lock (prereg, ranking code, exit simulator, engine, ifi modules; exit lock too)", f"ok `{lock[:16]}`")]
    ok, msgs = check_no_lookahead(XR.engine_params(cfgX))
    print("[2/7] look-ahead:", "ok" if ok else "FAILED", msgs[-1])
    if not ok:
        print("ABORT: look-ahead check failed")
        return 1
    validity.append(("Engine look-ahead (truncation)", "ok: " + msgs[-1]))
    ok, m = synthetic_checks(pr, cfgX)
    validity += m
    if not ok:
        print("ABORT: synthetic check failed")
        return 1
    man = D.manifest()
    mh = D.manifest_hash()
    if man is None or man.get("source") != D.SOURCE or not mh.startswith(pr["data"]["manifest_prefix"]):
        print(f"ABORT: the snapshot is not the pre-registered one (source {None if man is None else man.get('source')}, "
              f"manifest {mh[:16]}, expected {pr['data']['manifest_prefix']})")
        return 1
    U = cfgX["universe"]
    print(f"[5/7] snapshot ok: cutoff {man['cutoff']} · manifest {mh[:16]}")
    validity.append(("Frozen snapshot (pre-registered manifest)", f"cutoff {man['cutoff']} · manifest `{mh[:16]}`"))
    Fe = XR.load_frames(D.load, U["etfs"], U["min_bars"])
    Fs = XR.load_frames(D.load, U["stocks"], U["min_bars"])
    XR.FRAMES_INDEX.clear()
    Te = build_trades(Fe, cfgX, cfgX["params"]["cost_etf"])
    Ts = build_trades(Fs, cfgX, cfgX["params"]["cost_stock"])
    Rs = build_trades(Fs, cfgX, cfgX["params"]["cost_stock"], random_seeds=cfgX["params"]["random_seeds"])
    p = pr["params"]
    mine = Book(Ts, p["risk_pct"], p["max_open"]).run(own_calendar=True)
    cX = dict(cfgX, params=dict(cfgX["params"], risk_pct=p["risk_pct"], max_open=p["max_open"]))
    lab = XR.portfolio(Ts, "X3", cX)
    same = (mine["trades"] == lab["trades"] and abs(mine["cagr"] - lab["cagr"]) < 1e-12 and abs(mine["max_dd"] - lab["max_dd"]) < 1e-12)
    msg = f"stocks: {mine['trades']} trades, CAGR {100 * mine['cagr']:.3f}%, max DD {100 * mine['max_dd']:.3f}% in both"
    print("[6/7] baseline parity:", "ok" if same else "FAILED", msg if same else (mine, lab))
    if not same:
        print("ABORT: the book does not reproduce the exit test's portfolio")
        return 1
    validity.append(("Baseline parity (uncapped first-come = research/exits/run.py portfolio())", "ok: " + msg))
    out = evaluate(Te, Ts, pr, with_boot=True)
    sup = supporting(Ts, Rs, pr)
    Tc = pd.concat([Te, Ts], ignore_index=True)
    bc = Book(Tc, p["risk_pct"], p["max_open"])
    comb = {"base": bc.run(cap=p["notional_cap"])}
    for a in ARMS:
        k, pri = arm_inputs(Tc, a, pr)
        comb[a] = bc.run(keep=k, prio=pri, cap=p["notional_cap"])
    OUT.mkdir(parents=True, exist_ok=True)
    meta = dict(run_utc=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"), commit=_commit(), lock=lock,
                cutoff=man["cutoff"], manifest=mh, n_etf=len(Fe), n_stk=len(Fs), validity=validity)
    (OUT / "RANKING.md").write_text(report(out, sup, comb, pr, meta))
    cols = ["sym", "date", "entry_date", "exit_date", "rt", "r", "why", "dist", "stage", "width", "width_fill"]
    pd.concat([Te.assign(universe="etf"), Ts.assign(universe="stock")])[["universe"] + cols].to_csv(OUT / "RANKING_signals.csv", index=False)
    verdicts = {a: out["res"][a]["verdict"] for a in ARMS}
    (OUT / "RANKING_meta.json").write_text(json.dumps(dict(meta, verdicts=verdicts), indent=1, default=str))
    print("[7/7] written:", verdicts)
    return 0


if __name__ == "__main__":
    sys.exit(main())
