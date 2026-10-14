"""Input diagnostics for the research gates: computes NO forward returns and tests NO rule.

Checks that the frozen snapshot and the engine's ratio states match what was seen on TradingView:
  1. TradingView parity: close, Trend line, anchor and 200-bar average against values read from screenshots
  2. Definition audit: the reclaims (Trend 2.0 E4 markers) and rule 3 tops logged by eye in the scan must be
     found by the engine; misses show the nearest engine event and the pivot highs behind rule 3
  3. Data integrity and state summary per ratio (history, gaps, share of days per stage, event counts)
  4. One chart per audit event (reports/research/diagnose/), to compare with TradingView by eye

  python -m research.diagnose      (or Actions -> Research -> step = diagnose)

It reads the locked engine through the same lock check as the gates, but is itself only a reporting tool:
nothing here feeds a verdict.
"""
from __future__ import annotations

import sys

import numpy as np
import pandas as pd
import yaml

from research import engine as E
from research import step1
from research.common import OUT, RESEARCH, load_prereg, load_snapshot, manifest_hash, snapshot_manifest

DIAG = OUT / "diagnose"


def collect(U: dict, P: dict) -> dict:
    ent, r3, evs = [], [], {}
    for s, u in U.items():
        x = u["x"]
        ev = E.events(x, P)
        evs[s] = ev
        for e in ev["entries"]:
            ent.append(dict(ratio=s, i=e["t"], date=x.index[e["t"]], tier=e["tier"], lf=e["lf"]))
        for i in np.flatnonzero(ev["r3"]):
            r3.append(dict(ratio=s, i=int(i), date=x.index[i]))
    cols_e, cols_r = ["ratio", "i", "date", "tier", "lf"], ["ratio", "i", "date"]
    return dict(entries=pd.DataFrame(ent, columns=cols_e), r3=pd.DataFrame(r3, columns=cols_r), events=evs)


def nearest(src: pd.DataFrame, ratio: str, a: pd.Timestamp, b: pd.Timestamp, x: pd.DataFrame, bars: int = 40) -> str:
    d = src[src["ratio"] == ratio]
    if d.empty:
        return "none"
    ia, ib = x.index.searchsorted(a), x.index.searchsorted(b)
    d = d[(d["i"] >= ia - bars) & (d["i"] <= ib + bars)]
    if d.empty:
        return f"none within {bars} bars"
    gap = np.minimum(np.abs(d["i"] - ia), np.abs(d["i"] - ib))
    r = d.loc[gap.idxmin()]
    side = "before" if r["i"] < ia else "after"
    return f"{r['date']:%Y-%m-%d} ({int(gap.min())} bars {side})" + (f" tier {r['tier']}" if "tier" in r else "")


def pivot_context(ev: dict, x: pd.DataFrame, b: pd.Timestamp, lookback: int = 80) -> str:
    """Pivot highs confirmed in the bars before the window end: value, higher-high?, line rising?"""
    ib = min(x.index.searchsorted(b), len(x) - 1)
    out, prev = [], np.nan
    for i in range(max(0, ib - lookback - 60), ib + 1):
        v = ev["ph"][i]
        if not np.isnan(v):
            if i >= ib - lookback:
                hh = "HH" if (not np.isnan(prev) and v > prev) else "LH" if not np.isnan(prev) else "first"
                out.append(f"{x.index[i]:%m-%d} {v:.4f} {hh}{'' if ev['rising'][i] else ' (line not rising)'}")
            prev = v
    return "; ".join(out) if out else "no pivot highs"


def summary(U: dict, C: dict) -> pd.DataFrame:
    rows = []
    for s, u in U.items():
        x, ev = u["x"], C["events"][s]
        gaps = x.index.to_series().diff().dt.days
        st = x["stage"].iloc[250:]
        en = C["entries"][C["entries"]["ratio"] == s]
        rows.append(dict(ratio=f"{s}/SPY", group=u["group"], first=f"{x.index[0]:%Y-%m-%d}", last=f"{x.index[-1]:%Y-%m-%d}",
                         bars=len(x), gaps_over_5d=int((gaps > 5).sum()), max_gap_d=int(gaps.max()),
                         stage3=100 * (st == 3).mean(), stage2=100 * (st == 2).mean(), stage_m1=100 * (st == -1).mean(),
                         line_rising=100 * np.nanmean(ev["rising"][250:]), flat=100 * np.nanmean(ev["flat"][250:]),
                         reclaims=len(en), tierA=int((en["tier"] == "A").sum()), tierB=int((en["tier"] == "B").sum()),
                         r3=int((C["r3"]["ratio"] == s).sum()), washout_exits=int(ev["wexit"].sum()),
                         bull_divs=int(ev["bdiv"].sum()), warnings=int(ev["warn"].sum())))
    return pd.DataFrame(rows)


def fixture_charts(U: dict, C: dict, fx: dict) -> list[str]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    DIAG.mkdir(parents=True, exist_ok=True)
    for f in DIAG.glob("*.png"):
        f.unlink()
    names = []
    for kind in ("reclaim", "r3"):
        for f in fx.get(kind, []):
            s = f["ratio"]
            if s not in U:
                continue
            x, ev = U[s]["x"], C["events"][s]
            a_, b_ = pd.Timestamp(f["from"]), pd.Timestamp(f["to"])
            ia, ib = x.index.searchsorted(a_), x.index.searchsorted(b_)
            if ia >= len(x):
                continue
            lo, hi = max(0, ia - 90), min(len(x), ib + 40)
            k = np.arange(lo, hi)
            xs = x.iloc[lo:hi]
            fig, ax = plt.subplots(figsize=(10, 4.2), dpi=80)
            ax.axvspan(ia, min(ib, len(x) - 1), color="#fbbc04", alpha=0.15, label="logged window")
            ax.vlines(k, xs["low"], xs["high"], color="#9aa0a6", lw=0.6)
            ax.plot(k, xs["close"], color="#202124", lw=1.0, label="close")
            ln, rising = xs["tr_line"].to_numpy(), ev["rising"][lo:hi]
            ax.plot(k, np.where(rising, ln, np.nan), color="#188038", lw=1.4, label="Trend line (rising)")
            ax.plot(k, np.where(~rising, ln, np.nan), color="#d93025", lw=1.4, label="Trend line (not rising)")
            ax.plot(k, xs["tr_anchor"], color="#5f6368", lw=1.0, ls="--", label="anchor")
            ph = ev["ph"][lo:hi]
            m = ~np.isnan(ph)
            piv = E.DEFAULTS["piv"]
            ax.scatter(k[m] - piv, ph[m], marker="_", color="#e37400", s=60, label="pivot high (at pivot bar)")
            en = C["entries"][(C["entries"]["ratio"] == s) & C["entries"]["i"].between(lo, hi - 1)]
            ax.scatter(en["i"], x["close"].to_numpy()[en["i"]], marker="o", facecolors="none", edgecolors="#9334e6", s=60,
                       label="engine reclaim")
            r3 = C["r3"][(C["r3"]["ratio"] == s) & C["r3"]["i"].between(lo, hi - 1)]
            ax.scatter(r3["i"], x["close"].to_numpy()[r3["i"]], marker="x", color="#d93025", s=60, label="engine rule 3")
            ax.set_title(f"{s}/SPY · logged {kind} {f['from']} … {f['to']} · {f['note']}", fontsize=9)
            ax.legend(fontsize=6, loc="upper left", ncol=4)
            ax.set_xticks(k[::20])
            ax.set_xticklabels([f"{d:%Y-%m-%d}" for d in x.index[lo:hi][::20]], fontsize=6, rotation=0)
            fig.tight_layout()
            name = f"{kind}_{s}_{f['from']}.png"
            fig.savefig(DIAG / name)
            plt.close(fig)
            names.append(name)
    return names


def main() -> int:
    cfg, lock = load_prereg(check_lock=True)
    man = snapshot_manifest()
    if man is None or not str(man.get("source", "")).startswith("Yahoo"):
        print("ABORT: no Yahoo snapshot committed (run the Research workflow with step = all first).")
        return 1
    P = dict(E.DEFAULTS, **cfg["thresholds"])
    fx = yaml.safe_load((RESEARCH / "fixtures_scan.yaml").read_text())
    U = step1.load_universe(load_snapshot, cfg)
    C = collect(U, P)
    par_share, par_rows = step1.parity(U, fx, cfg["validity"]["parity_tol"])
    aud_share, aud_rows = step1.definition_audit(C, U, fx)
    for r in aud_rows:
        if r["found"] is False:
            x = U[r["ratio"]]["x"]
            src = C["entries"] if r["kind"] == "reclaim" else C["r3"]
            r["nearest"] = nearest(src, r["ratio"], pd.Timestamp(r["from"]), pd.Timestamp(r["to"]), x)
            if r["kind"] == "r3":
                r["pivots"] = pivot_context(C["events"][r["ratio"]], x, pd.Timestamp(r["to"]))
    summ = summary(U, C)
    charts = fixture_charts(U, C, fx)

    v = cfg["validity"]
    md = ["# Research diagnostics (inputs only: no forward returns, no rule tested)", "",
          f"_Snapshot cutoff {man['cutoff']} · manifest `{manifest_hash()[:16]}` · lock `{lock[:16]}` · "
          f"thresholds v{cfg['version']} base set_", "",
          "## 1. TradingView parity", "",
          f"Matched **{100 * par_share:.0f}%** within {100 * v['parity_tol']:.1f}% (Step 1 requires {100 * v['parity_min']:.0f}%).", "",
          "| ratio | date | field | TradingView | Python | difference |", "|---|---|---|---|---|---|"]
    for p_ in par_rows:
        py = "n/a" if np.isnan(p_["py"]) else "%.4f" % p_["py"]
        diff = "n/a" if p_["ok"] is None else ("%.2f%%" % (100 * p_["rel"])) + ("" if p_["ok"] else " ✗")
        md.append(f"| {p_['ratio']} | {p_['date']} | {p_['field']} | {p_['tv']:.4f} | {py} | {diff} |")
    md += ["", "## 2. Definition audit", "",
           f"Found **{100 * aud_share:.0f}%** (Step 1 requires {100 * v['definition_audit_min']:.0f}%): "
           f"{step1.audit_by_kind(aud_rows)}.", "",
           "| kind | ratio | logged window | found | engine dates in window | if missed: nearest engine event (±40 bars) | note |",
           "|---|---|---|---|---|---|---|"]
    for a in aud_rows:
        f = "n/a" if a["found"] is None else ("yes" if a["found"] else "**no**")
        md.append(f"| {a['kind']} | {a['ratio']} | {a['from']} … {a['to']} | {f} | {a['dates']} | {a.get('nearest', '')} | {a['note']} |")
    miss3 = [a for a in aud_rows if a["kind"] == "r3" and a["found"] is False]
    if miss3:
        md += ["", "**Rule 3 misses: pivot highs before each window end** (a top arms only on a higher high while "
               "the line is rising, then needs a lower high and a close below the last pivot low)", ""]
        md += [f"- {a['ratio']} {a['from']}…{a['to']}: {a['pivots']}" for a in miss3]
    md += ["", "## 3. Data and state summary (after the 250-bar warm-up)", "",
           "| ratio | group | first | last | bars | gaps >5d | max gap (d) | stage 3 % | stage 2 % | stage −1 % | line rising % | flat % | reclaims | tier A | tier B | rule 3 | washout exits | bull divs | warnings |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in summ.itertuples():
        md.append(f"| {r.ratio} | {r.group} | {r.first} | {r.last} | {r.bars} | {r.gaps_over_5d} | {r.max_gap_d} | {r.stage3:.0f} | "
                  f"{r.stage2:.0f} | {r.stage_m1:.0f} | {r.line_rising:.0f} | {r.flat:.0f} | {r.reclaims} | {r.tierA} | {r.tierB} | "
                  f"{r.r3} | {r.washout_exits} | {r.bull_divs} | {r.warnings} |")
    md += ["", "## 4. Charts of every logged event (compare with TradingView)", "",
           "Yellow band = the window logged by eye; purple circle = engine reclaim; red x = engine rule 3; "
           "orange dash = pivot high at its pivot bar.", ""]
    md += [f"- [{n}](diagnose/{n})" for n in charts]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "DIAGNOSE.md").write_text("\n".join(md) + "\n")
    summ.to_csv(OUT / "DIAGNOSE_summary.csv", index=False)
    pd.DataFrame(aud_rows).to_csv(OUT / "DIAGNOSE_audit.csv", index=False)
    pd.DataFrame(par_rows).to_csv(OUT / "DIAGNOSE_parity.csv", index=False)
    print(f"diagnostics written: parity {100 * par_share:.0f}% · audit {100 * aud_share:.0f}% "
          f"({step1.audit_by_kind(aud_rows)}) · {len(charts)} charts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
