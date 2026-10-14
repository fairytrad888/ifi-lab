"""Step 1: pre-registered tests T1-T6 of IFI ratio rules v2.1 (research/prereg_v21.yaml).

Run through research/run.py, which checks the pre-registration lock, the look-ahead test and the
synthetic null before any real result is produced.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
import pandas as pd

from ifi.indicators import trend as trend_ind
from ifi.states import read
from research import engine as E
from research.common import OUT, Boot, ratio_bars, universe

HORIZONS = (20, 40, 60)
TEST_IDS = ["T1", "T2", "T3", "T4a", "T4b", "T5", "T6"]
PASS_LABELS = ("PASS", "PASS-TRADEABLE", "PASS-CONTEXT")


# ------------------------------------------------------------------ data assembly
def load_universe(loader, cfg: dict) -> dict:
    gs, go, bench = universe(cfg)
    b = loader(bench)
    U = {}
    for g, names in (("S", gs), ("O", go)):
        for s in names:
            a = loader(s)
            if a is None or b is None or len(a) < cfg["universe"]["min_bars"]:
                print("skip", s)
                continue
            r = ratio_bars(a, b)
            x = E.base(r)
            num = a.reindex(x.index)
            U[s] = dict(x=x, num=num, group=g)
    return U


def build_panel(U: dict, cfg: dict) -> pd.DataFrame:
    start = pd.Timestamp(cfg["universe"]["start"])
    rows = []
    for s, u in U.items():
        x, nm = u["x"], u["num"]
        df = pd.DataFrame(index=x.index)
        for h in HORIZONS:
            df[f"g{h}"] = np.log(x["close"].shift(-h) / x["open"].shift(-1))
            df[f"n{h}"] = np.log(nm["close"].shift(-h) / nm["open"].shift(-1))
        df["ratio"], df["group"], df["i"] = s, u["group"], np.arange(len(x))
        df = df.iloc[250:]
        rows.append(df[df.index >= start])
    P = pd.concat(rows)
    P.index.name = "date"
    P = P.reset_index()
    for h in HORIZONS:
        P[f"g{h}"] = P[f"g{h}"] - P.groupby("date")[f"g{h}"].transform("mean")
    split = pd.Timestamp(cfg["universe"]["split"])
    P["half"] = np.where(P["date"] < split, "early", "late")
    return P


def macro_regime(loader, cfg: dict, dates: pd.DatetimeIndex) -> pd.Series:
    """Regime id per date: 2 * (US10Y Trend line above its value 10 bars ago) + (SPY stage >= 2)."""
    tnx = loader(cfg["universe"]["macro"][0])
    spy = loader(cfg["universe"]["benchmark"])
    line = trend_ind(tnx)["line"]
    rates_up = (line > line.shift(10)).astype(float).where(line.shift(10).notna())
    spy_ok = (read(spy)["stage"] >= 2).astype(float)
    reg = 2 * rates_up.reindex(dates, method="ffill") + spy_ok.reindex(dates, method="ffill")
    return reg


def m_tables(panel: pd.DataFrame) -> dict:
    """Average peer-relative g20 per (ratio, regime) estimated on each half and on all data."""
    d = panel.dropna(subset=["g20", "regime"])
    out = {}
    for lab, m in (("early", d["half"] == "early"), ("late", d["half"] == "late"), ("all", slice(None))):
        out[lab] = d[m].groupby(["ratio", "regime"])["g20"].mean()
    return out


def m_for(tables: dict, ratio: str, regime: float, half: str) -> float:
    """Cross-fitted: an event in one half uses M estimated on the OTHER half."""
    train = "late" if half == "early" else "early"
    try:
        return float(tables[train].loc[(ratio, regime)])
    except KeyError:
        return np.nan


# ------------------------------------------------------------------ one parameter set
def run_params(U: dict, panel: pd.DataFrame, P: dict, want_trades: bool = True) -> dict:
    ent, r3, stk, tch, trd = [], [], [], [], []
    evs = {}
    late_n = 0
    for s, u in U.items():
        x = u["x"]
        ev = E.events(x, P)
        evs[s] = ev
        dates = x.index
        for e in ev["entries"]:
            ent.append(dict(ratio=s, i=e["t"], tier=e["tier"], lf=e["lf"]))
            # T4 needs every exit to have its full horizon: entries closer than max_hold_struct bars to the
            # data end are left out by DATE (not by how they turned out), and counted in the report
            if want_trades and e["tier"] in ("A", "B") and e["t"] + 1 + P["max_hold_struct"] >= len(x):
                late_n += 1
                continue
            if want_trades and e["tier"] in ("A", "B"):
                row = dict(ratio=s, i=e["t"], tier=e["tier"])
                ok = True
                for kind in ("3R", "A", "B"):
                    res = E.simulate(x, ev, e["t"], e["lf"], kind, P, u["num"])
                    if res is None or res.get("cancelled"):
                        ok = False
                        break
                    row[f"r_{kind}"], row[f"rn_{kind}"] = res["r"], res.get("rn", np.nan)
                    row[f"bars_{kind}"], row[f"why_{kind}"] = res["bars"], res["reason"]
                if ok:
                    row["unresolved"] = any(row[f"why_{k}"] == "open_at_end" for k in ("3R", "A", "B"))
                    trd.append(row)
        for i in np.flatnonzero(ev["r3"]):
            r3.append(dict(ratio=s, i=int(i)))
        for i in np.flatnonzero(ev["stack"]):
            stk.append(dict(ratio=s, i=int(i)))
        for i in np.flatnonzero(ev["touch_rise"] | ev["touch_flat"]):
            tch.append(dict(ratio=s, i=int(i), kind="rise" if ev["touch_rise"][i] else "flat", held=ev["held"][i]))
    key = panel.set_index(["ratio", "i"])
    cols = ["date", "group", "half", "g20", "g40", "g60", "n20", "n40", "n60", "regime"]

    def attach(rows, own):
        df = pd.DataFrame(rows, columns=["ratio", "i", *own]) if not rows else pd.DataFrame(rows)
        out = df.join(key[cols], on=["ratio", "i"], how="inner")
        return out.reset_index(drop=True)

    trade_cols = ["tier", "unresolved"] + [f"{a}_{k}" for k in ("3R", "A", "B") for a in ("r", "rn", "bars", "why")]
    trades = attach(trd, trade_cols)
    return dict(entries=attach(ent, ["tier", "lf"]), r3=attach(r3, []), stack=attach(stk, []),
                touch=attach(tch, ["kind", "held"]), trades=trades, late=late_n,
                unresolved=int(trades["unresolved"].astype(bool).sum()), events=evs)


# ------------------------------------------------------------------ test samples
def samples(tid: str, D: dict, panel: pd.DataFrame, mt: dict | None) -> dict:
    """Return the tested comparison: kind 'diff' (A vs B) or 'paired' (mean of d)."""
    en, tr = D["entries"], D["trades"]
    if tid == "T1":
        A = en[en["tier"] == "A"]
        return dict(kind="diff", A=A, B=panel, col="g40", ncol="n40", sign=1)
    if tid == "T2":
        return dict(kind="diff", A=en[en["tier"] == "A"], B=en[en["tier"] == "B"], col="g40", ncol="n40", sign=1)
    if tid == "T3":
        return dict(kind="diff", A=D["r3"], B=panel, col="g20", ncol=None, sign=-1)
    if tid in ("T4a", "T4b"):
        k = "A" if tid == "T4a" else "B"
        t = tr.copy()
        t["d"] = t[f"r_{k}"] - t["r_3R"]
        t["dn"] = t[f"rn_{k}"] - t["rn_3R"]
        return dict(kind="paired", A=t, col="d", ncol="dn", sign=1, exit=k)
    if tid == "T5":
        tc = D["touch"]
        return dict(kind="diff", A=tc[tc["kind"] == "rise"], B=tc[tc["kind"] == "flat"], col="g20", ncol="n20", sign=1)
    if tid == "T6":
        e = en[en["tier"].isin(["A", "B"])].copy()
        e["M"] = [m_for(mt, r, g, h) for r, g, h in zip(e["ratio"], e["regime"], e["half"])]
        e = e.dropna(subset=["M"])
        return dict(kind="diff", A=e[e["M"] > 0], B=e[e["M"] <= 0], col="g40", ncol="n40", sign=1)
    raise KeyError(tid)


def _point(S: dict, mA=None, mB=None) -> tuple[float, int, int]:
    A = S["A"] if mA is None else S["A"][mA(S["A"])]
    va = A[S["col"]].dropna()
    if S["kind"] == "paired":
        return (float(va.mean()) if len(va) else np.nan), len(va), 0
    B = S["B"] if mB is None else S["B"][mB(S["B"])]
    vb = B[S["col"]].dropna()
    if not len(va) or not len(vb):
        return np.nan, len(va), len(vb)
    return float(va.mean() - vb.mean()), len(va), len(vb)


SUBSETS = {
    "early": lambda d: d["half"] == "early", "late": lambda d: d["half"] == "late",
    "S": lambda d: d["group"] == "S", "O": lambda d: d["group"] == "O",
}


def full_stats(tid: str, S: dict, boot: Boot, cfg: dict) -> dict:
    st = cfg["stats"]
    A = S["A"].dropna(subset=[S["col"]])
    if S["kind"] == "paired":
        res = boot.mean(A[S["col"]], A["date"])
    else:
        B = S["B"].dropna(subset=[S["col"]])
        res = boot.diff(A[S["col"]], A["date"], B[S["col"]], B["date"])
    res["sub"] = {}
    for lab, f in SUBSETS.items():
        est, na, nb = _point(S, f, f)
        res["sub"][lab] = dict(est=est, n_a=na, n_b=nb)
    # tradeable version (numerator ETF price), unadjusted 95%
    if S.get("ncol"):
        An = S["A"].dropna(subset=[S["ncol"]])
        if S["kind"] == "paired":
            rn = boot.mean(An[S["ncol"]], An["date"])
        else:
            Bn = S["B"].dropna(subset=[S["ncol"]])
            rn = boot.diff(An[S["ncol"]], An["date"], Bn[S["ncol"]], Bn["date"])
        res["num"] = dict(est=rn["est"], lo=rn["lo"], hi=rn["hi"])
    if S["kind"] == "paired":
        t = S["A"]
        k = S["exit"]
        res["capital"] = dict(new=float(t[f"r_{k}"].sum() / max(t[f"bars_{k}"].sum(), 1) * 100),
                              base=float(t["r_3R"].sum() / max(t["bars_3R"].sum(), 1) * 100))
    # sample-size rule
    if tid == "T6":
        enough = res["n_a"] >= st["min_n_t6"] and res["n_b"] >= st["min_n_t6"]
    else:
        enough = res["n_a"] >= st["min_n"]
    enough = enough and all(v["n_a"] >= st["min_n_sub"] for v in res["sub"].values())
    if S["kind"] == "diff" and tid in ("T2", "T5", "T6"):
        enough = enough and all(v["n_b"] >= st["min_n_sub"] for v in res["sub"].values())
    res["enough"] = bool(enough)
    return res


def verdict(tid: str, res: dict, sens: dict, sign: int, test_cfg: dict) -> tuple[str, list[str]]:
    why = []
    if not res["enough"]:
        return "INSUFFICIENT", ["sample below the pre-registered minimum"]
    lo, hi = res["lo_adj"], res["hi_adj"]
    adj_ok = lo > 0 if sign > 0 else hi < 0
    opposite = hi < 0 if sign > 0 else lo > 0
    if opposite:
        return "OPPOSITE", ["adjusted CI excludes 0 in the wrong direction"]
    if any(np.isnan(v["est"]) for v in res["sub"].values()):
        return "INSUFFICIENT", ["a half or group has no events"]
    subs_ok = all(np.sign(v["est"]) == sign for v in res["sub"].values())
    sens_nan = [k for k, v in sens.items() if np.isnan(v)]
    sens_bad = [k for k, v in sens.items() if not np.isnan(v) and np.sign(v) != sign]
    cap_ok = True
    if test_cfg.get("capital_check"):
        cap_ok = res["capital"]["new"] >= res["capital"]["base"]
    if not adj_ok:
        why.append("adjusted CI includes 0")
    if not subs_ok:
        why.append("a half or group points the other way")
    if not cap_ok:
        why.append("R per 100 bars below X-3R")
    if why:
        return "FAIL", why
    if sens_bad or sens_nan:
        return "FRAGILE", ([("neighbour(s) flip sign: " + ", ".join(sens_bad))] if sens_bad else []) + \
            ([("neighbour(s) with no events: " + ", ".join(sens_nan))] if sens_nan else [])
    if not test_cfg.get("numerator"):
        return "PASS", []
    n = res.get("num", {})
    trad = (n.get("lo", np.nan) > 0) if sign > 0 else (n.get("hi", np.nan) < 0)
    return ("PASS-TRADEABLE" if trad else "PASS-CONTEXT"), ([] if trad else ["numerator-price CI includes 0"])


# ------------------------------------------------------------------ secondary comparisons (base set, unadjusted)
def secondary(D: dict, panel: pd.DataFrame, boot: Boot) -> list[dict]:
    en, r3, stk, tc, tr = D["entries"], D["r3"], D["stack"], D["touch"], D["trades"]
    out = []

    def add(test, label, A, B, col):
        A, B = A.dropna(subset=[col]), B.dropna(subset=[col])
        if len(A) and len(B):
            r = boot.diff(A[col], A["date"], B[col], B["date"])
            out.append(dict(test=test, comparison=label, measure=col, est=r["est"], lo=r["lo"], hi=r["hi"],
                            n_a=r["n_a"], n_b=r["n_b"]))

    tA, tB, tN = en[en["tier"] == "A"], en[en["tier"] == "B"], en[en["tier"] == "none"]
    add("T1", "tier A - reclaims with no floor", tA, tN, "g40")
    add("T1", "tier B - all days", tB, panel, "g40")
    add("T1", "no-floor reclaims - all days", tN, panel, "g40")
    add("T1", "tier A - all days (60 bars)", tA, panel, "g60")
    add("T3", "rule 3 - warning stacks (no lower low yet)", r3, stk, "g20")
    add("T3", "warning stacks - all days", stk, panel, "g20")
    add("T3", "rule 3 - all days (40 bars)", r3, panel, "g40")
    add("T5", "rising-line touches - all days (20 bars)", tc[tc["kind"] == "rise"], panel, "g20")
    add("T5", "flat-line touches - all days (20 bars)", tc[tc["kind"] == "flat"], panel, "g20")
    add("T5", "rising-line touches - flat-line touches (40 bars)", tc[tc["kind"] == "rise"], tc[tc["kind"] == "flat"], "g40")
    if len(tr):
        d = tr.assign(d=tr["r_B"] - tr["r_A"]).dropna(subset=["d"])
        r = boot.mean(d["d"], d["date"])
        out.append(dict(test="T4", comparison="X-B - X-A (paired R)", measure="R", est=r["est"], lo=r["lo"], hi=r["hi"],
                        n_a=r["n_a"], n_b=0))
    return out


def exit_table(tr: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for tier in ("A", "B", "all"):
        t = tr if tier == "all" else tr[tr["tier"] == tier]
        for k, name in (("3R", "X-3R"), ("A", "X-A"), ("B", "X-B")):
            if not len(t):
                continue
            r = t[f"r_{k}"]
            rows.append(dict(tier=tier, exit=name, n=len(t), mean_r=r.mean(), win=(r > 0).mean(), median_r=r.median(),
                             mean_bars=t[f"bars_{k}"].mean(), r_per_100=r.sum() / max(t[f"bars_{k}"].sum(), 1) * 100,
                             num_mean_r=t[f"rn_{k}"].mean(),
                             reasons=", ".join(f"{a} {b}" for a, b in t[f"why_{k}"].value_counts().items())))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ validity: definition audit and parity
def definition_audit(D: dict, U: dict, fx: dict) -> tuple[float, list[dict]]:
    rows = []
    en = D["entries"]
    r3 = D["r3"]
    for kind, src in (("reclaim", en), ("r3", r3)):
        for f in fx.get(kind, []):
            if f["ratio"] not in U:
                rows.append(dict(kind=kind, **f, found=None, dates=""))
                continue
            d = src[(src["ratio"] == f["ratio"]) & (src["date"] >= pd.Timestamp(f["from"])) & (src["date"] <= pd.Timestamp(f["to"]))]
            if pd.Timestamp(f["to"]) > U[f["ratio"]]["x"].index[-1]:
                rows.append(dict(kind=kind, **f, found=None, dates="beyond data"))
                continue
            rows.append(dict(kind=kind, **f, found=bool(len(d)),
                             dates=", ".join(f"{t:%Y-%m-%d}" + (f" ({tt})" if kind == "reclaim" else "")
                                             for t, tt in zip(d["date"], d["tier"] if kind == "reclaim" else [""] * len(d)))))
    checked = [r for r in rows if r["found"] is not None]
    share = sum(r["found"] for r in checked) / max(len(checked), 1)
    return share, rows


def parity(U: dict, fx: dict, tol: float) -> tuple[float, list[dict]]:
    rows = []
    fmap = dict(close="close", line="tr_line", anchor="tr_anchor", sma200="sma200")
    for f in fx.get("parity", []):
        s, d = f["ratio"], pd.Timestamp(f["date"])
        if s not in U or d not in U[s]["x"].index:
            for k in fmap:
                if k in f:
                    rows.append(dict(ratio=s, date=f["date"], field=k, tv=f[k], py=np.nan, rel=np.nan, ok=None))
            continue
        row = U[s]["x"].loc[d]
        for k, col in fmap.items():
            if k in f:
                py = float(row[col])
                rel = abs(py / f[k] - 1)
                rows.append(dict(ratio=s, date=f["date"], field=k, tv=f[k], py=py, rel=rel, ok=bool(rel <= tol)))
    checked = [r for r in rows if r["ok"] is not None]
    share = sum(r["ok"] for r in checked) / max(len(checked), 1)
    return share, rows


# ------------------------------------------------------------------ live states
def live_states(U: dict, D: dict, P: dict, regime: pd.Series, mt: dict) -> pd.DataFrame:
    rows = []
    for s, u in U.items():
        x, ev = u["x"], D["events"][s]
        i = len(x) - 1
        fs, rs = ev["floor_state"], ev["r3_state"]
        reg = regime.get(x.index[i], np.nan)
        try:
            M = float(mt["all"].loc[(s, reg)])
        except KeyError:
            M = np.nan
        slope = ev["slope"][i]
        lo = max(0, i - P["xb_win"] + 1)
        rows.append(dict(
            ratio=f"{s}/SPY", date=f"{x.index[i]:%Y-%m-%d}", close=x["close"].iloc[i], line=x["tr_line"].iloc[i],
            line_state="rising" if ev["rising"][i] else ("flat" if ev["flat"][i] else "falling"),
            anchor=x["tr_anchor"].iloc[i], anchor_role="support" if x["tr_anchor_is_support"].iloc[i] else "resistance",
            bull_trend=bool(ev["bull"][i]),
            floor=(f"tier {fs['tier']} · Lf {fs['lf']:.4f} · {fs['since_last_component']} bars since last part"
                   if fs["active"] else "none"),
            rule3=("armed: lower high in, confirms on a close < %.4f" % rs["trigger_level"] if rs["peak"] is not None and rs["lower_high"]
                   else ("watching (peak %.4f)" % rs["peak"] if rs["peak"] is not None else "not armed")),
            warnings_20=int(ev["warn"][lo:i + 1].sum()), slope_atr=slope,
            regime={0: "rates down · SPY weak", 1: "rates down · SPY ok", 2: "rates up · SPY weak",
                    3: "rates up · SPY ok"}.get(reg, "n/a"),
            M_pct=100 * M if not np.isnan(M) else np.nan))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ audit sheets
def audit_sheets(U: dict, D: dict, out_dir: Path, per_type: int = 6, seed: int = 7) -> list[str]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    out_dir.mkdir(parents=True, exist_ok=True)
    for f in out_dir.glob("*.png"):
        f.unlink()
    rng = np.random.default_rng(seed)
    en = D["entries"]
    picks = [("entryA", en[en["tier"] == "A"]), ("entryB", en[en["tier"] == "B"]), ("entry_nofloor", en[en["tier"] == "none"]),
             ("rule3", D["r3"]), ("warnstack", D["stack"]),
             ("touch_rising", D["touch"][D["touch"]["kind"] == "rise"]), ("touch_flat", D["touch"][D["touch"]["kind"] == "flat"])]
    names = []
    for lab, df in picks:
        if not len(df):
            continue
        sel = df.iloc[rng.choice(len(df), size=min(per_type, len(df)), replace=False)]
        for r in sel.itertuples():
            x, ev = U[r.ratio]["x"], D["events"][r.ratio]
            t = int(r.i)
            a, b = max(0, t - 140), min(len(x), t + 61)
            xs = x.iloc[a:b]
            k = np.arange(a, b)
            fig, ax = plt.subplots(figsize=(10, 4.2), dpi=80)
            ax.vlines(k, xs["low"], xs["high"], color="#9aa0a6", lw=0.6)
            ax.plot(k, xs["close"], color="#202124", lw=1.0, label="close")
            ln = xs["tr_line"].to_numpy()
            rising = ev["rising"][a:b]
            ax.plot(k, np.where(rising, ln, np.nan), color="#188038", lw=1.4, label="Trend line (rising)")
            ax.plot(k, np.where(~rising, ln, np.nan), color="#d93025", lw=1.4, label="Trend line (not rising)")
            ax.plot(k, xs["tr_anchor"], color="#5f6368", lw=1.0, ls="--", label="anchor")
            m = ev["wexit"][a:b]
            ax.scatter(k[m], xs["low"].to_numpy()[m], marker="^", color="#1e8e3e", s=28, label="washout exit", zorder=3)
            m = ev["bdiv"][a:b]
            ax.scatter(k[m], xs["low"].to_numpy()[m] * 0.995, marker="D", color="#1a73e8", s=20, label="bull divergence", zorder=3)
            m = ev["warn"][a:b]
            ax.scatter(k[m], xs["high"].to_numpy()[m] * 1.005, marker="v", color="#e37400", s=24, label="warning", zorder=3)
            if hasattr(r, "lf") and not pd.isna(getattr(r, "lf", np.nan)):
                ax.axhline(r.lf, color="#1a73e8", lw=0.8, ls=":", label="floor low")
            ax.axvline(t, color="#9334e6", lw=1.0)
            ax.set_title(f"{r.ratio}/SPY · {lab} · {x.index[t]:%Y-%m-%d}", fontsize=10)
            ax.legend(fontsize=6, loc="upper left", ncol=4)
            ax.set_xticks(k[::40])
            ax.set_xticklabels([f"{d:%Y-%m}" for d in x.index[a:b][::40]], fontsize=7)
            fig.tight_layout()
            name = f"{lab}_{r.ratio}_{x.index[t]:%Y%m%d}.png"
            fig.savefig(out_dir / name)
            plt.close(fig)
            names.append(name)
    return names


# ------------------------------------------------------------------ the whole step
def param_sets(cfg: dict) -> list[tuple[str, object, dict]]:
    base = dict(E.DEFAULTS)
    base.update(cfg["thresholds"])
    sets = [("base", None, base)]
    for k, vals in cfg["sensitivity"].items():
        for v in vals:
            P = dict(base)
            P[k] = v
            sets.append((k, v, P))
    return sets


def run_step1(loader, cfg: dict, allowed: list[str], tag: str = "real", sheets: bool = False,
              fixtures: dict | None = None) -> dict:
    st = cfg["stats"]
    boot = Boot(st["reps"], st["seed"], st["k"], st["alpha"], st["block_months"])
    U = load_universe(loader, cfg)
    panel = build_panel(U, cfg)
    reg = macro_regime(loader, cfg, pd.DatetimeIndex(sorted(panel["date"].unique())))
    panel["regime"] = panel["date"].map(reg)
    mt = m_tables(panel)
    sets = param_sets(cfg)
    base = sets[0][2]
    D0 = run_params(U, panel, base)
    # each neighbour parameter set is computed once and shared by every test it can move
    cache = {}
    for name, val, P in sets[1:]:
        users = [t for t in allowed if name in cfg["relevant"][t]]
        if users:
            cache[(name, val)] = run_params(U, panel, P, want_trades=any(t.startswith("T4") for t in users))
    results, sens_rows = {}, []
    for tid in allowed:
        S = samples(tid, D0, panel, mt)
        res = full_stats(tid, S, boot, cfg)
        sens = {}
        for name, val, P in sets[1:]:
            if name in cfg["relevant"][tid]:
                est, _, _ = _point(samples(tid, cache[(name, val)], panel, mt))
                sens[f"{name}={val}"] = est
                sens_rows.append(dict(test=tid, param=name, value=val, est=est))
        sign = S["sign"]
        v, why = verdict(tid, res, sens, sign, cfg["tests"][tid])
        results[tid] = dict(res=res, sens=sens, verdict=v, why=why, sign=sign)
    out = dict(U=U, panel=panel, D=D0, results=results, sens=pd.DataFrame(sens_rows), regime=reg, mt=mt, base=base,
               boot=boot)
    if tag == "real":
        out["secondary"] = secondary(D0, panel, boot)
        out["exits"] = exit_table(D0["trades"])
        out["live"] = live_states(U, D0, base, reg, mt)
        if fixtures is not None:
            out["audit_share"], out["audit_rows"] = definition_audit(D0, U, fixtures)
            out["parity_share"], out["parity_rows"] = parity(U, fixtures, cfg["validity"]["parity_tol"])
        if sheets:
            out["sheets"] = audit_sheets(U, D0, OUT / "audit")
    return out


def count_passes(out: dict) -> int:
    return sum(r["verdict"] in PASS_LABELS for r in out["results"].values())


# ------------------------------------------------------------------ report
def _pct(v, scale=100):
    return "n/a" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{scale * v:+.2f}"


def write_report(out: dict, cfg: dict, meta: dict, allowed: list[str], blocked: dict) -> str:
    R = out["results"]
    panel, D = out["panel"], out["D"]
    unit = {"T1": "%", "T2": "%", "T3": "%", "T4a": "R", "T4b": "R", "T5": "%", "T6": "%"}
    scale = {"%": 100, "R": 1, "pp": 100}
    md = ["# Step 1: IFI ratio rules v2.1, pre-registered tests", "",
          f"_Run {meta['run_utc']} · commit `{meta['commit'][:10]}` · prereg sha256 `{meta['prereg'][:16]}` · "
          f"data snapshot cutoff {meta['cutoff']} (manifest `{meta['manifest'][:16]}`) · "
          f"{panel['ratio'].nunique()} ratios · {panel['date'].min():%Y-%m-%d} to {panel['date'].max():%Y-%m-%d} · "
          f"Bonferroni k = {cfg['stats']['k']} · {cfg['stats']['reps']:,} bootstrap draws in {cfg['stats']['block_months']}-month blocks · "
          f"{meta.get('versions', '')}_", "",
          "## Validity", "",
          "| check | result | required |", "|---|---|---|"]
    for row in meta["validity"]:
        md.append(f"| {row[0]} | {row[1]} | {row[2]} |")
    md += ["", f"**Run status: {meta['status']}**", ""]
    md += ["## Verdicts", "",
           "| test | question | n (A / B) | estimate | adjusted CI | 2000-14 · 2015- | sectors · others | numerator | verdict |",
           "|---|---|---|---|---|---|---|---|---|"]
    for tid in TEST_IDS:
        if tid not in R:
            md.append(f"| {tid} | {cfg['tests'][tid]['question']} | | | | | | | NOT RUN ({blocked.get(tid, 'Step 0 gate')}) |")
            continue
        r = R[tid]["res"]
        u = unit[tid]
        sc = scale[u]
        sub = r["sub"]
        num = r.get("num")
        nums = f"{sc * num['est']:+.2f} ({sc * num['lo']:+.2f} … {sc * num['hi']:+.2f})" if num else "n/a"
        why = f" ({'; '.join(R[tid]['why'])})" if R[tid]["why"] else ""
        md.append(f"| {tid} | {cfg['tests'][tid]['question']} | {r['n_a']:,} / {r['n_b']:,} | {sc * r['est']:+.2f} {u} | "
                  f"{sc * r['lo_adj']:+.2f} … {sc * r['hi_adj']:+.2f} | {sc * sub['early']['est']:+.2f} · {sc * sub['late']['est']:+.2f} | "
                  f"{sc * sub['S']['est']:+.2f} · {sc * sub['O']['est']:+.2f} | {nums} | **{R[tid]['verdict']}**{why} |")
    md += ["", "Estimates: T1, T2, T6 = difference in 40-bar peer-relative ratio return (%); T3 = 20-bar (%), expected negative; "
           "T4 = paired difference in R per trade; T5 = difference in 20-bar peer-relative return after first touches of the line (%). "
           "Numerator = the same comparison on the numerator ETF's own price (unadjusted 95% CI).", ""]
    md += ["## Decisions (written before the results)", ""]
    sec = {(x_["test"], x_["comparison"]): x_ for x_ in out.get("secondary", [])}
    for tid in TEST_IDS:
        if tid in R:
            ok = R[tid]["verdict"] in PASS_LABELS
            md.append(f"- **{tid} {R[tid]['verdict']}:** {cfg['decisions'][tid]['pass' if ok else 'fail']}"
                      + resolve(tid, ok, R, sec))
    md += ["", "## Secondary comparisons (unadjusted 95% CI, for interpretation only)", "",
           "| test | comparison | measure | estimate | 95% CI | n (A / B) |", "|---|---|---|---|---|---|"]
    for s in out.get("secondary", []):
        sc = 1 if s["measure"] == "R" else 100
        md.append(f"| {s['test']} | {s['comparison']} | {s['measure']} | {sc * s['est']:+.2f} | {sc * s['lo']:+.2f} … {sc * s['hi']:+.2f} | "
                  f"{s['n_a']:,} / {s['n_b']:,} |")
    md += ["", "## Sensitivity (point estimate at each neighbour; a PASS needs the same sign everywhere)", "",
           "| test | parameter | value | estimate |", "|---|---|---|---|"]
    for s in out["sens"].itertuples():
        sc = scale[unit[s.test]]
        md.append(f"| {s.test} | {s.param} | {s.value} | {_pct(s.est, sc)} |")
    if len(out.get("exits", [])):
        md += ["", "## Exits on rule 2 trades (ratio R after costs)", "",
               "| tier | exit | trades | mean R | win % | median R | mean bars | R per 100 bars | numerator mean R | exit reasons |",
               "|---|---|---|---|---|---|---|---|---|---|"]
        for e in out["exits"].itertuples():
            md.append(f"| {e.tier} | {e.exit} | {e.n} | {e.mean_r:+.3f} | {100 * e.win:.0f} | {e.median_r:+.2f} | {e.mean_bars:.0f} | "
                      f"{e.r_per_100:+.2f} | {e.num_mean_r:+.3f} | {e.reasons} |")
    tc = D["touch"]
    if len(tc):
        md += ["", "## How first touches held over the next 10 bars (observation 2, descriptive)", "",
               "| line | touches | held at the line | held at the gray anchor | failed |", "|---|---|---|---|---|"]
        for k, lab in (("rise", "rising (bull trend)"), ("flat", "flat")):
            h_ = tc[(tc["kind"] == k)]["held"].dropna()
            if len(h_):
                md.append(f"| {lab} | {len(h_):,} | {100 * (h_ == 0).mean():.0f}% | {100 * (h_ == 1).mean():.0f}% | {100 * (h_ == 2).mean():.0f}% |")
    en = D["entries"]
    md += ["", "## Event counts (base thresholds)", "",
           f"Tier A entries {int((en['tier'] == 'A').sum())} · tier B {int((en['tier'] == 'B').sum())} · reclaims with no floor "
           f"{int((en['tier'] == 'none').sum())} · rule 3 confirmations {len(D['r3'])} · warning stacks {len(D['stack'])} · "
           f"rising-line touches {int((D['touch']['kind'] == 'rise').sum())} · flat-line touches {int((D['touch']['kind'] == 'flat').sum())} · "
           f"simulated rule 2 trades {len(D['trades'])} ({D['late']} entries within {out['base']['max_hold_struct']} bars of the data end "
           f"left out of T4 by date; open at the data end: {D['unresolved']})", ""]
    if "audit_rows" in out:
        md += ["## Definition audit (eye-logged scan events the engine must find)", "",
               f"Found {100 * out['audit_share']:.0f}% (required {100 * cfg['validity']['definition_audit_min']:.0f}%): "
               f"{audit_by_kind(out['audit_rows'])}. A miss is evidence about a definition or a date read by eye, "
               "never a reason to tune a threshold.", "",
               "| kind | ratio | window | found | engine dates | note |", "|---|---|---|---|---|---|"]
        for a in out["audit_rows"]:
            f = "n/a" if a["found"] is None else ("yes" if a["found"] else "**no**")
            md.append(f"| {a['kind']} | {a['ratio']} | {a['from']} … {a['to']} | {f} | {a['dates']} | {a['note']} |")
        md += ["", "## TradingView parity (values read from IFI 2.0 screenshots)", "",
               f"Matched {100 * out['parity_share']:.0f}% within {100 * cfg['validity']['parity_tol']:.1f}% "
               f"(required {100 * cfg['validity']['parity_min']:.0f}%).", "",
               "| ratio | date | field | TradingView | Python | difference |", "|---|---|---|---|---|---|"]
        for p_ in out["parity_rows"]:
            py = "n/a" if np.isnan(p_["py"]) else "%.4f" % p_["py"]
            diff = "n/a" if p_["ok"] is None else ("%.2f%%" % (100 * p_["rel"])) + ("" if p_["ok"] else " ✗")
            md.append(f"| {p_['ratio']} | {p_['date']} | {p_['field']} | {p_['tv']:.4f} | {py} | {diff} |")
    if "live" in out:
        md += ["", "## Live states (last completed bar, base thresholds)", "",
               "| ratio | date | close | line | line state | anchor | role | bull trend | floor | rule 3 | warnings (20) | macro regime | M (20-bar %) |",
               "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for l_ in out["live"].itertuples():
            md.append(f"| {l_.ratio} | {l_.date} | {l_.close:.4f} | {l_.line:.4f} | {l_.line_state} | {l_.anchor:.4f} | {l_.anchor_role} | "
                      f"{'yes' if l_.bull_trend else ''} | {l_.floor} | {l_.rule3} | {l_.warnings_20} | {l_.regime} | "
                      f"{'n/a' if np.isnan(l_.M_pct) else '%+.2f' % l_.M_pct} |")
    if out.get("sheets"):
        md += ["", "## Event audit sheets", "",
               "Random events per type (fixed seed). Open each and check the engine marked what your eye would mark.", ""]
        md += [f"- [{n}](audit/{n})" for n in out["sheets"]]
    return "\n".join(md) + "\n"


def resolve(tid: str, ok: bool, R: dict, sec: dict) -> str:
    """Apply the conditional parts of the pre-registered decisions."""
    if tid == "T2" and not ok:
        b = sec.get(("T1", "tier B - all days"))
        if b is None:
            return ""
        return " → **tiers merge**" if b["lo"] > 0 else " → **tier B dropped**"
    if tid == "T4b":
        a_ok = R.get("T4a", {}).get("verdict") in PASS_LABELS
        if ok and a_ok:
            d = sec.get(("T4", "X-B - X-A (paired R)"))
            return (" → **X-B used**" if d and d["est"] > 0 else " → **X-A used**") + " (both passed)"
        if ok:
            return " → **X-B used** (X-A did not pass)"
    return ""


def audit_by_kind(rows: list[dict]) -> str:
    parts = []
    for kind, lab in (("reclaim", "reclaims (Trend 2.0 E4 markers)"), ("r3", "rule 3 tops (eye-dated)")):
        c = [r for r in rows if r["kind"] == kind and r["found"] is not None]
        if c:
            parts.append(f"{lab} {sum(r['found'] for r in c)}/{len(c)}")
    return " · ".join(parts)


def save_tables(out: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for tid, r in out["results"].items():
        res = r["res"]
        rows.append(dict(test=tid, verdict=r["verdict"], why="; ".join(r["why"]), est=res["est"], lo=res["lo"], hi=res["hi"],
                         lo_adj=res["lo_adj"], hi_adj=res["hi_adj"], n_a=res["n_a"], n_b=res["n_b"],
                         early=res["sub"]["early"]["est"], late=res["sub"]["late"]["est"], S=res["sub"]["S"]["est"],
                         O=res["sub"]["O"]["est"], num_est=res.get("num", {}).get("est"), num_lo=res.get("num", {}).get("lo"),
                         num_hi=res.get("num", {}).get("hi")))
    pd.DataFrame(rows).to_csv(OUT / "STEP1_results.csv", index=False)
    out["sens"].to_csv(OUT / "STEP1_sensitivity.csv", index=False)
    D = out["D"]
    keep = ["ratio", "date", "group", "tier", "lf", "g20", "g40", "g60", "n40", "regime"]
    D["entries"][[c for c in keep if c in D["entries"]]].to_csv(OUT / "STEP1_entries.csv", index=False)
    D["trades"].drop(columns=["i"], errors="ignore").to_csv(OUT / "STEP1_trades.csv", index=False)
    D["r3"][["ratio", "date", "group", "g20", "g40"]].to_csv(OUT / "STEP1_rule3.csv", index=False)
    D["touch"][["ratio", "date", "group", "kind", "held", "g20", "g40"]].to_csv(OUT / "STEP1_touches.csv", index=False)
    if "live" in out:
        out["live"].to_csv(OUT / "STEP1_live_states.csv", index=False)
