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


def build(frames: dict, log: pd.DataFrame, journal: dict, c: dict, pt: pd.DataFrame | None = None,
          scoreboard: dict | None = None, drift: dict | None = None, alloc_meta: dict | None = None,
          health: dict | None = None, fresh: dict | None = None, c14: dict | None = None, live_ev: dict | None = None):
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
        ev_html = "<table><tr><th>Bar</th><th>TF</th><th>Symbol</th><th style='text-align:left'>Event</th><th>Stage</th><th>Score</th><th>Close</th><th>Stop</th><th>Shares @risk</th><th>R after 10</th></tr>" + "".join(
            f"<tr><td>{pd.Timestamp(str(e.bar)).strftime('%Y-%m-%d' if e.tf == 'daily' else '%Y-%m-%d %H:%M')}</td><td>{e.tf}</td><td><b>{e.symbol}</b></td><td style='text-align:left'>{html.escape(str(e.event))}</td>"
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

    pb_html = "<p class='mut'>No playbook signals yet.</p>"
    if not log.empty and "family" in log and (log["family"] == "Playbook").any():
        pbl = log[log["family"] == "Playbook"].sort_values("bar").tail(15).iloc[::-1]
        def cell(v, d=2):
            return "–" if pd.isna(v) else f"{v:.{d}f}"
        pb_html = ("<table><tr><th>Bar</th><th>TF</th><th>Symbol</th><th style='text-align:left'>Setup</th><th>Entry ~</th>"
                   "<th>Stop</th><th>Target 3R</th><th>Cancel if open &lt;</th><th>Shares @risk</th><th>R after 10</th></tr>" + "".join(
            f"<tr><td>{pd.Timestamp(str(e.bar)):%Y-%m-%d}</td><td>{e.tf}</td><td><b>{e.symbol}</b></td>"
            f"<td style='text-align:left'>{html.escape(str(e.event).replace('Playbook ', ''))}</td><td>{cell(e.close)}</td>"
            f"<td class='dn'>{cell(e.stop)}</td><td class='up'>{cell(getattr(e, 'target', np.nan))}</td>"
            f"<td class='ctx'>{cell(getattr(e, 'cancel_if_open_below', np.nan))}</td><td>{e.shares_1pct}</td>"
            f"<td>{_num(e.r10, 2, 'up' if pd.notna(e.r10) and e.r10 > 0 else 'dn')}</td></tr>" for e in pbl.itertuples()) + "</table>"
                   "<p class='mut'>Daily signals only: setups adopted on both ETFs and stocks. Enter next open; skip if it opens below the cancel level. 4H copies are logged as “4H watch” to build evidence.</p>")

    j_html = "<p class='mut'>Connect a published Google Sheet in config.yaml → journal.trades_csv_url.</p>"
    if journal and journal.get("n"):
        j_html = (f"<p><b>{journal['n']}</b> closed trades · expectancy <b>{journal['expectancy']:+.2f}R</b> · "
                  f"win rate {100*journal['win_rate']:.0f}% · avg win {journal['avg_win'] or 0:+.2f}R · avg loss {journal['avg_loss'] or 0:+.2f}R</p>"
                  + "<table><tr><th>Setup</th><th>n</th><th>Expectancy</th></tr>" + "".join(
                      f"<tr><td>{html.escape(k)}</td><td>{v['n']}</td><td>{v['expectancy']:+.2f}R</td></tr>" for k, v in journal["by_setup"].items()) + "</table>")

    ex = (journal or {}).get("execution") or {}
    if ex.get("matched") is not None and ex.get("journal_trades"):
        def pct(v):
            return "–" if v is None else f"{100*v:.0f}%"
        def rr(v):
            return "–" if v is None else f"{v:+.2f}R"
        j_html += (f"<p class='mut' style='margin-top:10px'><b>Execution vs paper</b> · matched {ex['matched']} of {ex['journal_trades']} trades · "
                   f"signals taken {pct(ex.get('taken_pct'))} · entry slippage {rr(ex.get('avg_entry_slippage_r'))} · "
                   f"result gap vs paper {rr(ex.get('avg_r_gap_vs_paper'))}</p>")

    # ---- forward test: drift banner, scoreboard, paper trades
    drift_html = ""
    bad = {k: v for k, v in (drift or {}).items() if not v.get("ok")}
    if bad:
        drift_html = "<div class='card' style='border-color:var(--dn);margin-top:12px'><b class='dn'>Verdict drift.</b> " + "; ".join(
            f"{html.escape(k)}: ETFs {html.escape(v['etfs'])}, stocks {html.escape(v['stocks'])}" for k, v in bad.items()) + \
            ". A playbook setup no longer passes on both universes. Review before taking new signals.</div>"
    sb_html = "<p class='mut'>Allocation appears after the first backtest and paper trades.</p>"
    if scoreboard and "p_edge" in next(iter(scoreboard.values())):
        def f2(v, d=2, pct=False):
            if v is None or (isinstance(v, float) and np.isnan(v)):
                return "–"
            return f"{100 * v:.{d}f}%" if pct else f"{v:+.{d}f}"
        am = alloc_meta or {}
        sb_html = ("<table><tr><th>Setup</th><th>Risk per trade</th><th>P(edge &gt; 0)</th><th>Estimated edge (R)</th>"
                   "<th>Live trades</th><th>Live R/trade</th><th>Live total R</th><th>Open</th><th>Backtest R (prior)</th>"
                   "<th>Losing streak</th></tr>" + "".join(
            f"<tr><td><b>{html.escape(k.split('_')[0])}</b> {html.escape(' '.join(k.split('_')[1:]))}</td>"
            f"<td><b>{100 * v['risk']:.2f}%</b></td><td>{f2(v['p_edge'], 1, True)}</td><td>{f2(v['posterior_mean'])}</td>"
            f"<td>{v['live_n']}</td><td>{f2(v['live_expectancy'])}</td><td>{f2(v['live_total_r'])}</td><td>{v['open_trades']}</td>"
            f"<td class='mut'>{f2(v['prior_mean'])} (n {v['prior_n']:,})</td>"
            f"<td class='{'dn' if v['streak_flag'] else ''}'>{v['losing_streak']}{' ⚠' if v['streak_flag'] else ''}</td></tr>"
            for k, v in scoreboard.items()) + "</table>"
            f"<p class='mut'>Ladder: the backtest edge × {((c14 or {}).get('allocation') or {}).get('haircut', 0.6)} counts like "
            f"{((c14 or {}).get('allocation') or {}).get('n0', 100)} live trades; live paper trades since "
            f"{c.get('forward_test', {}).get('start', '?')} update it. Risk 0% = paper only. "
            f"Drawdown breaker: <b class='{'up' if am.get('breaker', 'ok') == 'ok' else 'dn'}'>{html.escape(str(am.get('breaker', 'ok')))}</b>"
            f" (live paper drawdown {f2(am.get('live_drawdown'), 1, True)}, backtest maximum at this risk {f2(am.get('ref_drawdown'), 1, True)}"
            "; the reference uses realised exits and a sector cap, so it trips on the early, conservative side)."
            + (" A PAPER ONLY trip stays on until you set safety.breaker_reset in config_v14.yaml." if str(am.get('breaker', '')).startswith('PAPER') else "")
            + "</p>")
    elif scoreboard:
        def f2(v):
            return "–" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{v:+.2f}"
        def pill(s):
            cls = {"ON TRACK": "s3", "WATCH": "s1", "STOP": "s-1"}.get(s, "s0")
            return f'<span class="pill {cls}" style="padding:1px 8px">{html.escape(s)}</span>'
        sb_html = ("<table><tr><th>Setup</th><th>Status</th><th>Live trades</th><th>Live R/trade</th><th>Live 95% range</th>"
                   "<th>Open</th><th>Live total R</th><th>Backtest R/trade</th><th>Backtest CI low</th><th>Pre-live (backfill)</th></tr>" + "".join(
            f"<tr><td><b>{html.escape(k.split('_')[0])}</b> {html.escape(' '.join(k.split('_')[1:]))}</td><td>{pill(v['status'])}</td>"
            f"<td>{v['live_n']}</td><td>{f2(v['live_expectancy'])}</td><td>{f2(v['live_ci_low'])} … {f2(v['live_ci_high'])}</td>"
            f"<td>{v['open_trades']}</td><td>{f2(v['live_total_r'])}</td><td>{f2(v['ref_expectancy'])}</td><td>{f2(v['ref_ci_low'])}</td>"
            f"<td class='mut'>{v['prelive_n']} @ {f2(v['prelive_expectancy'])}</td></tr>" for k, v in scoreboard.items()) + "</table>"
                   f"<p class='mut'>Live = paper trades of Daily playbook signals since {c.get('forward_test', {}).get('start', '?')}, with the exact backtest rules. "
                   "Status needs 20 closed trades: STOP if live R/trade is below 0 and below the backtest CI low; WATCH if only below the CI low.</p>")
    hl_html = "<p class='mut'>Health checks start with live paper trades.</p>"
    if health:
        def pc(v):
            return "–" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{100 * v:.1f}%"

        def ksp(v):
            return "–" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{v:.3f}"
        hl_html = ("<table><tr><th>Setup</th><th>Live signals</th><th>Cancelled (live / pre-live)</th><th>Skipped (live / pre-live)</th>"
                   "<th>Median stop width (live / pre-live)</th><th>Live R vs backtest (KS p)</th></tr>" + "".join(
            f"<tr><td><b>{html.escape(k.split('_')[0])}</b></td><td>{v['live_signals']}</td><td>{pc(v['cancel_live'])} / {pc(v['cancel_pre'])}</td>"
            f"<td>{pc(v['skip_live'])} / {pc(v['skip_pre'])}</td><td>{pc(v['stop_width_live'])} / {pc(v['stop_width_pre'])}</td>"
            f"<td class='{'dn' if v.get('ks_flag') else ''}'>{ksp(v.get('ks_p'))}</td></tr>"
            for k, v in health.items()) + "</table><p class='mut'>These flag data or execution problems, not edge. "
            "The KS comparison starts at 20 live closed trades.</p>")
    ev_live_html = ""
    if live_ev and (live_ev.get("edge") or live_ev.get("books")):
        def fr(v, d=2):
            return "–" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{v:+.{d}f}"
        def fp(v, d=1):
            return "–" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{100 * v:+.{d}f}%"
        e_rows = "".join(
            f"<tr><td style='text-align:left'>{html.escape(x['slice'])}</td><td>{x['n']}</td><td>{fr(x['mean_r'])}</td>"
            f"<td>{x['n_random']}</td><td>{fr(x['random_r'])}</td><td class='{'up' if (x['edge'] or 0) > 0 else 'dn'}'><b>{fr(x['edge'])}</b></td></tr>"
            for x in live_ev.get("edge", []))
        b_rows = "".join(
            f"<tr><td style='text-align:left'><b>{html.escape(k)}</b> {html.escape(str(v.get('name', '')))}</td><td>{fp(v.get('ret'), 2)}</td>"
            f"<td>{v.get('taken', 0)}</td><td>{v.get('skipped', 0)}</td><td>{v.get('open', 0)}</td><td>{fp(v.get('heat'), 2)}</td>"
            f"<td>{fr(v.get('sharpe_monthly'))}</td></tr>" for k, v in (live_ev.get("books") or {}).items())
        r_rows = "".join(
            f"<tr><td><b>{html.escape(r['id'])}</b></td><td>{'<b class=amb>due</b>' if r['due'] else html.escape(r['progress'])}</td>"
            f"<td style='text-align:left' class='mut'>{html.escape(r['what'])}</td></tr>" for r in live_ev.get("reviews", []))
        ev_live_html = (
            "<table><tr><th style='text-align:left'>Closed live trades</th><th>n</th><th>Mean R</th><th>Random n</th><th>Random mean R</th>"
            "<th>Edge over random</th></tr>" + e_rows + "</table>"
            "<p class='mut'>Random entries use the playbook's stop and exit on the same symbols and days: what any long entry earned "
            "from the market. Out of sample, E4 beat them by ~0.09R on new ETFs and ~0.03R on new stocks.</p>"
            "<table><tr><th style='text-align:left'>Shadow book (live paper trades)</th><th>Return</th><th>Taken</th><th>Skipped</th>"
            "<th>Open</th><th>Open risk</th><th>Monthly Sharpe</th></tr>" + b_rows + "</table>"
            "<p class='mut'>Descriptive: your real rule is B0. Monthly Sharpe appears after 6 months. Judged at review R2.</p>"
            + (("<table><tr><th>Review</th><th>Progress</th><th style='text-align:left'>Question</th></tr>" + r_rows + "</table>") if r_rows else ""))
    cand_html = ""
    if c14 and c14.get("candidates"):
        cand_html = ("<table><tr><th>ID</th><th>Lever</th><th style='text-align:left'>Hypothesis</th><th style='text-align:left'>Status</th></tr>" + "".join(
            f"<tr><td><b>{html.escape(str(x['id']))}</b></td><td>{html.escape(str(x['lever']))}</td>"
            f"<td style='text-align:left'>{html.escape(str(x['hypothesis']))}</td><td style='text-align:left' class='mut'>{html.escape(str(x['status']))}</td></tr>"
            for x in c14["candidates"]) + "</table>")
    fresh_html = ""
    if fresh and fresh.get("check_failed"):
        fresh_html = ("<div class='card' style='border-color:var(--amb);margin-top:12px'><b class='amb'>Freshness check did not run.</b> "
                      "SPY hourly bars were unavailable, so daily data may be a session behind.</div>")
    elif fresh and fresh.get("stale"):
        fresh_html = ("<div class='card' style='border-color:var(--amb);margin-top:12px'><b class='amb'>Data stale.</b> "
                      f"The {html.escape(str(fresh.get('expected')))} session has closed but {len(fresh.get('still_stale', []))} symbol(s) still lack it "
                      f"({html.escape(', '.join(fresh.get('still_stale', [])[:10]))}; SPY ends {html.escape(str(fresh.get('spy_last')))}). "
                      "Signals for that day will be processed on the next run (catch-up run at 03:30 UTC).</div>")
    pt_html = "<p class='mut'>No paper trades yet.</p>"
    if pt is not None and not pt.empty:
        show = pt[pt["oos"].astype(bool)] if pt["oos"].astype(bool).any() else pt
        order = {"open": 0, "pending": 1, "closed": 2, "skipped": 3, "cancelled": 4}
        show = show.assign(_o=show["status"].map(order)).sort_values(["_o", "signal_bar"], ascending=[True, False]).head(20)
        def g(v, d=2):
            return "–" if v is None or (isinstance(v, float) and np.isnan(v)) else (f"{v:.{d}f}" if isinstance(v, (int, float)) else str(v))
        pt_html = (f"<p class='mut'>Full universe: {pt['symbol'].nunique()} symbols paper-traded. Your real trades still follow the portfolio caps.</p>"
                   "<table><tr><th>Signal</th><th>Symbol</th><th style='text-align:left'>Setup</th><th>Status</th><th>Fill</th>"
                   "<th>Stop</th><th>Target</th><th>Exit</th><th>R</th></tr>" + "".join(
            f"<tr><td>{pd.Timestamp(r.signal_bar):%Y-%m-%d}</td><td><b>{r.symbol}</b></td><td style='text-align:left'>{html.escape(r.setup.split('_')[0])}</td>"
            f"<td>{html.escape(r.status)}</td><td>{g(getattr(r, 'fill', np.nan))}</td><td class='dn'>{g(getattr(r, 'stop', np.nan))}</td>"
            f"<td class='up'>{g(getattr(r, 'target', np.nan))}</td><td class='mut'>{html.escape('' if pd.isna(getattr(r, 'exit_reason', '')) else str(getattr(r, 'exit_reason', '')))}</td>"
            f"<td>{_num(getattr(r, 'r', np.nan), 2, 'up' if pd.notna(getattr(r, 'r', np.nan)) and getattr(r, 'r', 0) > 0 else 'dn')}</td></tr>"
            for r in show.itertuples()) + "</table>"
                   + ("" if pt["oos"].astype(bool).any() else "<p class='mut'>Showing pre-live (backfilled) paper trades until live signals arrive.</p>"))

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
{fresh_html}{drift_html}
<h2>Allocation (forward test)</h2><div class="card">{sb_html}</div>
{('<h2>Live evidence</h2><div class="card">' + ev_live_html + '</div>') if ev_live_html else ''}
<h2>Playbook signals</h2><div class="card">{pb_html}</div>
<h2>Paper trades</h2><div class="card">{pt_html}</div>
<h2>Process health</h2><div class="card">{hl_html}</div>
{('<h2>Candidates</h2><div class="card">' + cand_html + '</div>') if cand_html else ''}
<h2>Sector Board</h2><div class="card">{board}</div>
<p class="mut">Stage: <span class="pill s3">3</span> above anchor · <span class="pill s2">2</span> above rising Trend line · <span class="pill s1">1</span> exhaustion + higher low · <span class="pill s0">0</span> none · <span class="pill s-1">-1</span> breakdown. Anchor S/R = support/resistance; distance in ATR.</p>
<div class="grid"><div><h2>Rotation map (Daily vs {c['benchmark']})</h2><div class="card">{_rrg_svg(frames, c['watchlist'])}</div></div>
<div><h2>Journal</h2><div class="card">{j_html}</div><h2>Backtest reports</h2><div class="card">{rep_html}</div></div></div>
<h2>Recent events</h2><div class="card">{ev_html}</div>
<h2>Event statistics (from the log)</h2><div class="card">{stats_html}</div>
</main></body></html>"""
    (DOCS / "index.html").write_text(page)
