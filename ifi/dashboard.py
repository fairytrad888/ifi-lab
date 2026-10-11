"""Static dashboard (docs/index.html) for GitHub Pages: Sector Board, rotation map, events, statistics, journal."""
from __future__ import annotations

import html
import shutil
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from .data import ROOT

DOCS = ROOT / "docs"

CSS = """
:root{--bg:#fbfbfa;--fg:#1d1d1b;--mut:#6b6b66;--line:#e4e3df;--card:#fff;--up:#1a7f4b;--dn:#c0392b;--amb:#b7791f;--ctx:#8a8a85}
@media (prefers-color-scheme:dark){:root{--bg:#141413;--fg:#ecebe6;--mut:#9c9b95;--line:#2c2c2a;--card:#1c1c1b;--up:#3fbf7f;--dn:#ef6b5b;--amb:#e0a84a;--ctx:#7d7c77}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,sans-serif}
main{max-width:1200px;margin:0 auto;padding:20px 16px 60px}h1{font-size:22px;margin:0 0 4px}h2{font-size:16px;margin:28px 0 8px}
.mut{color:var(--mut)}.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px;overflow-x:auto}
table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}th,td{padding:6px 8px;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap}
th{font-weight:600;color:var(--mut);font-size:12px}td:first-child,th:first-child{text-align:left}
.up{color:var(--up)}.dn{color:var(--dn)}.amb{color:var(--amb)}.ctx{color:var(--ctx)}
.pill{display:inline-block;min-width:22px;padding:1px 6px;border-radius:999px;font-weight:600;text-align:center}
.s3{background:color-mix(in srgb,var(--up) 28%,transparent)}.s2{background:color-mix(in srgb,var(--up) 14%,transparent)}
.s1{background:color-mix(in srgb,var(--amb) 18%,transparent)}.s0{background:color-mix(in srgb,var(--ctx) 14%,transparent)}.s-1{background:color-mix(in srgb,var(--dn) 20%,transparent)}
.grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px}@media(max-width:860px){.grid{grid-template-columns:1fr}}
svg text{fill:var(--mut);font-size:11px}
"""


def _pill(v):
    try:
        v = int(v)
    except Exception:
        return "–"
    return f'<span class="pill s{v}">{v}</span>'


def _num(v, d=1, cls=""):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "–"
    return f'<span class="{cls}">{v:.{d}f}</span>'


def _next_earnings(sym):
    f = ROOT / "data" / "earnings" / f"{sym}.csv"
    if not f.exists():
        return ""
    try:
        e = pd.read_csv(f, index_col=0, parse_dates=True)
        fut = e.index[e.index >= pd.Timestamp.today().normalize()]
        return f"{fut.min():%b %d}" if len(fut) else ""
    except Exception:
        return ""


def _rrg_svg(frames, syms):
    pts = []
    for s in syms:
        x = frames.get(("daily", s))
        if x is None or "rs_ratio" not in x:
            continue
        t = x[["rs_ratio", "rs_mom"]].dropna().iloc[-10:]
        if len(t):
            pts.append((s, t))
    if not pts:
        return "<p class='mut'>No relative-strength data.</p>"
    allv = pd.concat([t for _, t in pts])
    span = max(abs(allv["rs_ratio"] - 100).max(), abs(allv["rs_mom"] - 100).max(), 1.0) * 1.15
    W = H = 360
    sx = lambda v: W / 2 + (v - 100) / span * (W / 2 - 20)
    sy = lambda v: H / 2 - (v - 100) / span * (H / 2 - 20)
    out = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Relative rotation map">',
           f'<line x1="{W/2}" y1="0" x2="{W/2}" y2="{H}" stroke="currentColor" opacity=".15"/>',
           f'<line x1="0" y1="{H/2}" x2="{W}" y2="{H/2}" stroke="currentColor" opacity=".15"/>',
           f'<text x="{W-8}" y="14" text-anchor="end">Leading</text><text x="{W-8}" y="{H-6}" text-anchor="end">Weakening</text>',
           f'<text x="8" y="{H-6}">Lagging</text><text x="8" y="14">Improving</text>']
    for s, t in pts:
        last = t.iloc[-1]
        col = ("var(--up)" if last.rs_ratio >= 100 and last.rs_mom >= 100 else "var(--amb)" if last.rs_ratio >= 100
               else "var(--dn)" if last.rs_mom < 100 else "var(--ctx)")
        path = " ".join(f"{sx(a):.1f},{sy(b):.1f}" for a, b in zip(t.rs_ratio, t.rs_mom))
        out.append(f'<polyline points="{path}" fill="none" stroke="{col}" stroke-width="1.5" opacity=".55"/>')
        out.append(f'<circle cx="{sx(last.rs_ratio):.1f}" cy="{sy(last.rs_mom):.1f}" r="4" fill="{col}"/>')
        out.append(f'<text x="{sx(last.rs_ratio)+6:.1f}" y="{sy(last.rs_mom)+4:.1f}" style="fill:var(--fg)">{html.escape(s)}</text>')
    out.append("</svg>")
    return "".join(out)


def build(frames: dict, log: pd.DataFrame, journal: dict, c: dict):
    DOCS.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    rows = []
    for s in c["watchlist"]:
        d, h = frames.get(("daily", s)), frames.get(("h4", s))
        if d is None:
            continue
        r = d.iloc[-1]
        rh = h.iloc[-1] if h is not None else None
        wno = int(d["ad_washout_no"].iloc[-20:].max())
        streak = int(d["sig_bull_streak"].iloc[-20:].max())
        last_ev = ""
        if not log.empty:
            le = log[(log.symbol == s)].tail(1)
            if len(le):
                last_ev = f"{le.iloc[0].event} ({pd.Timestamp(le.iloc[0].bar):%m-%d}, {le.iloc[0].tf})"
        rows.append(
            f"<tr><td><b>{s}</b></td><td>{_pill(r.stage)}</td><td>{int(r.score)}/5</td>"
            f"<td>{_pill(rh.stage) if rh is not None else '–'}</td><td>{f'{int(rh.score)}/5' if rh is not None else '–'}</td>"
            f"<td class='{'up' if r.tr_line_rising else 'dn'}'>{'▲' if r.tr_line_rising else '▼'}</td>"
            f"<td>{_num(r.dist_anchor_atr, 1)} <span class='ctx'>{'S' if r.tr_anchor_is_support else 'R'}</span></td>"
            f"<td>{_num(r.mx_rsi, 0, 'up' if r.mx_rsi > 60 else 'dn' if r.mx_rsi < 40 else '')}</td>"
            f"<td>{_num(r.sig_wt1, 0)}</td><td class='amb'>{'#'+str(wno) if wno else ''}</td>"
            f"<td>{streak or ''}</td><td>{r.get('rrg', '')}</td><td>{_num(r.rvol, 2)}</td>"
            f"<td class='ctx'>{_next_earnings(s)}</td><td style='text-align:left' class='mut'>{html.escape(last_ev)}</td></tr>")
    board = ("<table><tr><th>Symbol</th><th>D stage</th><th>D score</th><th>4H stage</th><th>4H score</th><th>Line</th>"
             "<th>Anchor (ATR)</th><th>RSI</th><th>WT1</th><th>Washout</th><th>Trig streak</th><th>Rotation</th>"
             "<th>RVOL</th><th>Earnings</th><th style='text-align:left'>Last event</th></tr>" + "".join(rows) + "</table>")

    ev_html = "<p class='mut'>No events logged yet.</p>"
    stats_html = "<p class='mut'>Statistics appear once logged events are 5–10 bars old.</p>"
    if not log.empty:
        recent = log.sort_values("bar").tail(40).iloc[::-1]
        ev_html = "<table><tr><th>Bar</th><th>TF</th><th>Symbol</th><th style='text-align:left'>Event</th><th>Stage</th><th>Score</th><th>Close</th><th>Stop</th><th>Shares @1%</th><th>R after 10</th></tr>" + "".join(
            f"<tr><td>{pd.Timestamp(e.bar):%Y-%m-%d %H:%M}</td><td>{e.tf}</td><td><b>{e.symbol}</b></td><td style='text-align:left'>{html.escape(str(e.event))}</td>"
            f"<td>{_pill(e.stage)}</td><td>{e.score}</td><td>{e.close:.2f}</td><td>{_num(e.stop, 2)}</td><td>{e.shares_1pct}</td>"
            f"<td>{_num(e.r10, 2, 'up' if pd.notna(e.r10) and e.r10 > 0 else 'dn')}</td></tr>"
            for e in recent.itertuples()) + "</table>"
        done = log.dropna(subset=["rel10"]) if "rel10" in log else pd.DataFrame()
        if not done.empty:
            g = done.groupby(["tf", "family"]).agg(n=("rel10", "size"), ret10=("ret10", "mean"), rel10=("rel10", "mean"),
                                                   hit=("rel10", lambda v: (v > 0).mean()), r10=("r10", "mean"),
                                                   mfe=("mfe10_r", "mean"), mae=("mae10_r", "mean")).reset_index()
            g = g[g.n >= 5].sort_values(["tf", "rel10"], ascending=[True, False])
            stats_html = ("<table><tr><th>TF</th><th style='text-align:left'>Event</th><th>n</th><th>Avg 10-bar return</th><th>vs SPY</th>"
                          "<th>Beat SPY</th><th>Avg R (close, 10 bars)</th><th>Avg best R</th><th>Avg worst R</th></tr>" + "".join(
                f"<tr><td>{r.tf}</td><td style='text-align:left'>{html.escape(r.family)}</td><td>{r.n}</td>"
                f"<td>{_num(100*r.ret10, 2)}%</td><td>{_num(100*r.rel10, 2, 'up' if r.rel10 > 0 else 'dn')}%</td>"
                f"<td>{_num(100*r.hit, 0)}%</td><td>{_num(r.r10, 2)}</td><td>{_num(r.mfe, 2)}</td><td>{_num(r.mae, 2)}</td></tr>"
                for r in g.itertuples()) + "</table><p class='mut'>Descriptive only: overlapping events, no costs. Decisions come from the backtest reports.</p>")

    j_html = "<p class='mut'>Connect a published Google Sheet in config.yaml → journal.trades_csv_url.</p>"
    if journal and journal.get("n"):
        j_html = (f"<p><b>{journal['n']}</b> closed trades · expectancy <b>{journal['expectancy']:+.2f}R</b> · "
                  f"win rate {100*journal['win_rate']:.0f}% · avg win {journal['avg_win'] or 0:+.2f}R · avg loss {journal['avg_loss'] or 0:+.2f}R</p>"
                  + "<table><tr><th>Setup</th><th>n</th><th>Expectancy</th></tr>" + "".join(
                      f"<tr><td>{html.escape(k)}</td><td>{v['n']}</td><td>{v['expectancy']:+.2f}R</td></tr>" for k, v in journal["by_setup"].items()) + "</table>")

    reports = sorted((ROOT / "reports").glob("SUMMARY_*.md"))
    for rp in reports:
        shutil.copy(rp, DOCS / rp.name)
    rep_html = " · ".join(f'<a href="{rp.name}">{rp.stem.replace("SUMMARY_", "").replace("_", " ")}</a>' for rp in reports) or "<span class='mut'>No backtest run yet.</span>"

    spy = frames.get(("daily", c["benchmark"]))
    regime = ""
    if spy is not None:
        sr = spy.iloc[-1]
        on = bool(sr.close > spy.close.rolling(200).mean().iloc[-1] and sr.tr_line_rising)
        regime = (f"Market regime: <b class='{'up' if on else 'dn'}'>{'risk-on' if on else 'caution'}</b> "
                  f"(SPY stage {int(sr.stage)}, line {'▲' if sr.tr_line_rising else '▼'}, {'above' if on else 'check'} 200-day)")
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>IFI Board</title><style>{CSS}</style></head><body><main>
<h1>IFI Board</h1><div class="mut">Updated {now:%Y-%m-%d %H:%M} UTC · {regime}</div>
<h2>Sector Board</h2><div class="card">{board}</div>
<p class="mut">Stage: <span class="pill s3">3</span> above anchor · <span class="pill s2">2</span> above rising Trend line · <span class="pill s1">1</span> exhaustion + higher low · <span class="pill s0">0</span> none · <span class="pill s-1">-1</span> breakdown. Anchor S/R = support/resistance; distance in ATR.</p>
<div class="grid"><div><h2>Rotation map (Daily vs {c['benchmark']})</h2><div class="card">{_rrg_svg(frames, c['watchlist'])}</div></div>
<div><h2>Journal</h2><div class="card">{j_html}</div><h2>Backtest reports</h2><div class="card">{rep_html}</div></div></div>
<h2>Recent events</h2><div class="card">{ev_html}</div>
<h2>Event statistics (from the log)</h2><div class="card">{stats_html}</div>
</main></body></html>"""
    (DOCS / "index.html").write_text(page)
