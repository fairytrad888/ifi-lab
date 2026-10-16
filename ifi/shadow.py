"""v1.5 live evidence (Oct 16, 2026), after construction test v1 (FAIL) and the first out-of-sample check of E4/E1.

Descriptive only: nothing here changes a signal, a size or the real book.

  random control  every symbol in the forward universe also gets random entries (~1 per 40 bars, 5 fixed seeds) with
                  the playbook's stop and exit, from the forward-test start. Live setup R minus live random R is the
                  live edge beyond market drift (out of sample, about 45% of the backtest edge survived, and on new
                  stocks E4 beat random entries by only ~0.03R).
  shadow books    the live paper trades replayed through three books: B0 (5 slots x 0.75%, the current rule), C1 (every
                  signal at 0.10%, cash-limited) and S20 (20 slots x 0.1875%). A row per session is kept in
                  logs/shadow_books.csv, so the construction question can be judged live at review R2.
  reviews         pre-registered live checkpoints (config_v14.yaml reviews) with their progress.
"""
from __future__ import annotations

import zlib

import numpy as np
import pandas as pd

from . import backtest as bt
from .data import ROOT

RANDOM = ROOT / "logs" / "random_control.csv"
SHADOW = ROOT / "logs" / "shadow_books.csv"


def random_control(frames: dict, c: dict, c14: dict) -> pd.DataFrame:
    """Random-entry trades with the playbook exit, entries from the forward-test start (fixed per symbol and seed;
    numpy's generator gives the same draws for past bars as the history grows)."""
    lc = c14.get("live_controls", {})
    rate, seeds = lc.get("random_rate", 0.025), lc.get("random_seeds", [1, 2, 3, 4, 5])
    start = pd.Timestamp(str(c.get("forward_test", {}).get("start", "2100-01-01")))
    ex = f"X3_target{c.get('playbook', {}).get('target_r', 3)}R"
    etfs = set(c["etfs"])
    ext = set(c.get("_extended", []))
    rows = []
    for (tf, sym), x in frames.items():
        if tf != "daily" or x is None or len(x) < 300:
            continue
        cost = c["costs"]["etf"] if sym in etfs else c["costs"]["stock"]
        first = int(np.searchsorted(x.index.values, np.datetime64(start)))
        for sd in seeds:
            ent = bt.random_setup(x, rate, sd * 100_000 + zlib.crc32(sym.encode()) % 100_000)
            ent.iloc[:first] = False
            if not ent.any():
                continue
            for t in bt.simulate(sym, x, ent, "random", ex, cost):
                if t.entry_date < start:
                    continue
                rows.append(dict(symbol=sym, seed=sd, universe="etf" if sym in etfs else "stock",
                                 group="extended" if sym in ext else "core", fill_date=t.entry_date,
                                 exit_date=pd.NaT if t.reason == "open_at_end" else t.exit_date,
                                 status="open" if t.reason == "open_at_end" else "closed", r=round(t.r, 3)))
    rc = pd.DataFrame(rows, columns=["symbol", "seed", "universe", "group", "fill_date", "exit_date", "status", "r"])
    RANDOM.parent.mkdir(parents=True, exist_ok=True)
    rc.to_csv(RANDOM, index=False)
    return rc


def live_edge(pt: pd.DataFrame, rc: pd.DataFrame) -> list[dict]:
    """Closed live trades: setup mean R vs random-entry mean R, by setup x universe, by group, and overall."""
    if pt is None or pt.empty:
        return []
    live = pt[pt["oos"].astype(bool) & (pt["status"] == "closed")]
    rcc = rc[rc["status"] == "closed"] if len(rc) else rc
    out = []
    def add(label, a, b):
        ma = float(a["r"].mean()) if len(a) else np.nan
        mb = float(b["r"].mean()) if len(b) else np.nan
        out.append(dict(slice=label, n=int(len(a)), mean_r=ma, n_random=int(len(b)), random_r=mb,
                        edge=ma - mb if len(a) and len(b) else np.nan))
    for su in sorted(live["setup"].unique()) if len(live) else []:
        a = live[live["setup"] == su]
        add(f"{su.split('_')[0]} all", a, rcc)
        for uni in ("etf", "stock"):
            add(f"{su.split('_')[0]} {uni}s", a[a["universe"] == uni], rcc[rcc["universe"] == uni] if len(rcc) else rcc)
    if "group" in live:
        for g in ("core", "extended"):
            add(f"all setups, {g} symbols", live[live["group"] == g], rcc[rcc["group"] == g] if len(rcc) else rcc)
    add("all setups", live, rcc)
    return out


def _book(live: pd.DataFrame, slots, risk: float, cash: float, start: float = 100_000.0) -> dict:
    """Replay live paper trades in fill order (then setup, symbol). Fixed fractional of the starting equity."""
    t = live.sort_values(["fill_date", "setup", "symbol"], kind="mergesort")
    open_: list = []          # (exit_date or NaT, risk amount, notional)
    taken, realized, open_mark, heat, notional = [], 0.0, 0.0, 0.0, 0.0
    for r in t.itertuples():
        open_ = [o for o in open_ if not (pd.notna(o[0]) and o[0] <= r.fill_date)]
        if slots is not None and len(open_) >= slots:
            continue
        w = (r.fill - r.stop) / r.fill if r.fill and r.fill > r.stop else np.nan
        a = risk * start
        nv = a / w if w and w > 0 else np.inf
        if cash is not None and sum(o[2] for o in open_) + nv > cash * start:
            continue
        open_.append((r.exit_date if r.status == "closed" else pd.NaT, a, nv))
        taken.append(r)
    for r in taken:
        a = risk * start
        if r.status == "closed":
            realized += a * r.r
        else:
            open_mark += a * (r.r if pd.notna(r.r) else 0.0)
            heat += a
            w = (r.fill - r.stop) / r.fill
            notional += a / w if w > 0 else 0.0
    eq = start + realized + open_mark
    return dict(taken=len(taken), skipped=int(len(t) - len(taken)), open=int(sum(1 for r in taken if r.status == "open")),
                equity=eq, ret=eq / start - 1, heat=heat / start, notional=notional / start)


def shadow_books(pt: pd.DataFrame, c14: dict, session: str) -> dict:
    """Book states today; appends/replaces this session's rows in logs/shadow_books.csv."""
    books = c14.get("shadow_books", {})
    if pt is None or pt.empty or not books:
        return {}
    live = pt[pt["oos"].astype(bool) & pt["status"].isin(["open", "closed"])].copy()
    for col in ("fill_date", "exit_date"):
        live[col] = pd.to_datetime(live[col].astype(str), format="ISO8601", errors="coerce")
    live = live.dropna(subset=["fill_date", "fill", "stop"])
    out = {k: dict(_book(live, b.get("slots"), b["risk"], b.get("cash", 1.0)), name=b.get("name", k)) for k, b in books.items()}
    rows = pd.DataFrame([dict(session=session, book=k, **{f: v[f] for f in ("equity", "ret", "taken", "skipped", "open", "heat")})
                         for k, v in out.items()])
    old = pd.read_csv(SHADOW) if SHADOW.exists() else pd.DataFrame(columns=rows.columns)
    old = old[old["session"].astype(str) != session]
    SHADOW.parent.mkdir(parents=True, exist_ok=True)
    pd.concat([old, rows], ignore_index=True).to_csv(SHADOW, index=False)
    hist = pd.concat([old, rows], ignore_index=True)
    for k in out:
        h = hist[hist["book"] == k].sort_values("session")
        out[k]["sessions"] = int(len(h))
        eq = h.set_index(pd.to_datetime(h["session"]))["equity"]
        m = eq.resample("ME").last().pct_change().dropna()
        out[k]["months"] = int(len(m))
        out[k]["sharpe_monthly"] = float(m.mean() / m.std() * np.sqrt(12)) if len(m) >= 6 and m.std() > 0 else np.nan
    return out


def review_progress(pt: pd.DataFrame, c14: dict, today: pd.Timestamp) -> list[dict]:
    live = pt[pt["oos"].astype(bool) & (pt["status"] == "closed")] if pt is not None and not pt.empty else pd.DataFrame()
    out = []
    for rv in c14.get("reviews", []):
        need = rv.get("closed_trades")
        cur = None
        if need:
            q = live
            if rv.get("setup"):
                q = q[q["setup"] == rv["setup"]] if len(q) else q
            if rv.get("universe"):
                q = q[q["universe"] == rv["universe"]] if len(q) else q
            cur = int(len(q))
        due_date = pd.Timestamp(rv["date"]) if rv.get("date") else None
        due = (need is None or (cur is not None and cur >= need)) and (due_date is None or today >= due_date)
        out.append(dict(id=rv["id"], what=rv["what"], progress=(f"{cur}/{need} closed" if need else "")
                        + (f"{' · ' if need else ''}date {rv['date']}" if rv.get("date") else ""), due=bool(due)))
    return out
