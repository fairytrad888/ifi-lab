"""v1.4 tests: allocation ladder, safety nets, KS, freshness repair, context tags (no look-ahead),
full-universe paper trades with tags, dashboard. Run: python tests/test_v14.py  (also works under pytest)"""
import math
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ifi import allocation as A  # noqa: E402
from ifi import freshness as F  # noqa: E402
from ifi.states import read  # noqa: E402

C14 = A.cfg14()


def rw(seed, n=1500, start="2020-01-02"):
    rng = np.random.default_rng(seed)
    c = 100 * np.exp(np.cumsum(rng.normal(0.0004, 0.013, n)))
    o = np.r_[c[0], c[:-1]] * np.exp(rng.normal(0, 0.003, n))
    h = np.maximum(o, c) * np.exp(np.abs(rng.normal(0, 0.006, n)))
    l = np.minimum(o, c) * np.exp(-np.abs(rng.normal(0, 0.006, n)))
    return pd.DataFrame(dict(open=o, high=h, low=l, close=c, volume=rng.integers(1e6, 5e6, n).astype(float)),
                        index=pd.bdate_range(start, periods=n))


def test_ladder_math():
    a = C14["allocation"]
    mean, p = A.posterior(0.30, 1.5, 0, 0.0, a)
    m0 = 0.30 * a["haircut"]
    assert abs(mean - m0) < 1e-12 and abs(p - A._phi(m0 / (1.5 / 10))) < 1e-12
    assert A.tier(0.99, 50, a) == 0.0075 and A.tier(0.99, 150, a) == 0.01
    assert A.tier(0.95, 0, a) == 0.0075 and A.tier(0.85, 0, a) == 0.005 and A.tier(0.75, 0, a) == 0.0025 and A.tier(0.5, 0, a) == 0.0
    # live losses pull the estimate down
    m2, p2 = A.posterior(0.30, 1.5, 60, -30.0, a)
    assert m2 < mean and p2 < p
    print("ladder math ok: starting P(edge>0) at +0.30R backtest =", round(p, 3), "->", A.tier(p, 0, a))


def test_calibration_direction():
    """Simulated live sequences: the ladder gives more risk to a real edge than to no edge (design section 3)."""
    a = C14["allocation"]
    rng = np.random.default_rng(3)
    def avg_risk(true_edge, n=150, sims=400):
        out = []
        for _ in range(sims):
            r = rng.normal(true_edge, 1.5, n)
            m, p = A.posterior(0.29, 1.5, n, float(r.sum()), a)
            out.append(A.tier(p, n, a))
        return float(np.mean(out))
    full, none = avg_risk(0.29), avg_risk(0.0)
    assert full > none + 0.002, (full, none)
    print(f"calibration ok: avg risk after 150 live trades {100 * full:.2f}% (edge as backtested) vs {100 * none:.2f}% (no edge)")


def test_streak_and_ks():
    assert A.streak_probability(1, 10, 0.5) > 0.99
    assert A.streak_probability(30, 50, 0.5) < 0.001
    assert A.current_streak(pd.Series([1, -1, 2, -1, -0.5, -1])) == 3
    d, p = A.ks_2samp(np.arange(100.0), np.arange(100.0))
    assert d == 0 and p > 0.99
    rng = np.random.default_rng(1)
    d, p = A.ks_2samp(rng.normal(0, 1, 400), rng.normal(0.6, 1, 400))
    assert p < 1e-6, p
    print("streak and KS ok")


def test_portfolio_drawdown():
    t = pd.DataFrame(dict(setup="E4", status="closed", r=[-1.0, -1.0, 2.0, -1.0],
                          fill_date=pd.to_datetime(["2026-01-02", "2026-01-05", "2026-01-06", "2026-02-02"]),
                          exit_date=pd.to_datetime(["2026-01-03", "2026-01-10", "2026-01-20", "2026-02-10"])))
    dd = A.portfolio_drawdown(t, {"E4": 0.01}, 5)
    assert abs(dd + 0.02) < 1e-12, dd     # -1, -1 -> -2% from the start, then +2 back, then -1
    print("portfolio drawdown ok")


def test_drawdown_weights_and_nan():
    t = pd.DataFrame(dict(setup="E4", status=["closed", "closed", "open"], r=[-1.0, -1.0, np.nan],
                          risk_at_fill=[0.01, np.nan, 0.01],
                          fill_date=pd.to_datetime(["2026-01-02", "2026-01-05", "2026-01-06"]),
                          exit_date=pd.to_datetime(["2026-01-03", "2026-01-10", None])))
    dd = A.portfolio_drawdown(t, {"E4": 0.0025}, 5)
    assert abs(dd + 0.0125) < 1e-12, dd   # 1% at fill, then the fallback 0.25%; a NaN mark counts as 0
    print("drawdown weights at fill and NaN marks ok")


def test_breaker_latch():
    import copy
    import json
    import yaml
    c = yaml.safe_load((ROOT / "config.yaml").read_text())
    tmp = Path(tempfile.mkdtemp())
    old = A.ALLOC, A.RISK_AT_FILL
    A.ALLOC, A.RISK_AT_FILL = tmp / "alloc.json", tmp / "raf.json"
    try:
        A.ALLOC.write_text(json.dumps(dict(board={}, portfolio=dict(breaker="PAPER ONLY (drawdown beyond 1.5x the backtest maximum)",
                                                                   tripped_utc="2026-10-01 00:00"))))
        out = A.ladder(pd.DataFrame(), c, C14)
        assert out["_portfolio"]["breaker"].startswith("PAPER ONLY") and out["_portfolio"]["multiplier"] == 0.0
        assert all(v["risk"] == 0 for k, v in out.items() if not k.startswith("_"))
        early = copy.deepcopy(C14); early["safety"]["breaker_reset"] = "2026-09-30"
        assert A.ladder(pd.DataFrame(), c, early)["_portfolio"]["breaker"].startswith("PAPER ONLY")   # reset before the trip: still latched
        A.ALLOC.write_text(json.dumps(dict(board={}, portfolio=dict(breaker="PAPER ONLY (x)", tripped_utc="2026-10-01 00:00"))))
        ok = copy.deepcopy(C14); ok["safety"]["breaker_reset"] = "2026-10-02"
        out = A.ladder(pd.DataFrame(), c, ok)
        assert out["_portfolio"]["breaker"] == "ok" and out["_portfolio"]["tripped_utc"] is None
    finally:
        A.ALLOC, A.RISK_AT_FILL = old
    print("breaker latch ok (holds until breaker_reset on or after the trip)")


def test_freshness():
    tmp = Path(tempfile.mkdtemp())
    old_dir, old_state = F.DAILY_DIR, F.STATE
    F.DAILY_DIR, F.STATE = tmp, tmp / "fresh.json"
    try:
        for s, last in (("SPY", "2026-10-14"), ("AAA", "2026-10-13"), ("BBB", "2026-10-13")):
            idx = pd.bdate_range(end=last, periods=5)
            df = pd.DataFrame(dict(open=1.0, high=1.0, low=1.0, close=1.0, volume=1.0), index=idx)
            df.index.name = "date"
            df.to_csv(tmp / f"{s}.csv")
        hourly = lambda: pd.DataFrame({"close": [1.0, 1.0]}, index=pd.DatetimeIndex(
            ["2026-10-14 15:30", "2026-10-15 09:30"]).tz_localize("America/New_York"))
        def recent(stale):
            row = pd.DataFrame(dict(open=2.0, high=2.0, low=2.0, close=2.0, volume=2.0), index=pd.DatetimeIndex(["2026-10-14"]))
            return {"AAA": row}
        # 01:00 UTC Oct 15: Oct 14 has closed; Oct 15 is trading but not complete
        rep = F.ensure(["SPY", "AAA", "BBB"], now=pd.Timestamp("2026-10-15 01:00", tz="UTC"), hourly=hourly, recent=recent)
        assert rep["expected"] == "2026-10-14", rep
        assert rep["stale_before"] == ["AAA", "BBB"] and rep["repaired"] == ["AAA"] and rep["still_stale"] == ["BBB"], rep
        assert rep["stale"] and "BBB" in F.banner_line(rep)
        assert pd.read_csv(tmp / "AAA.csv", index_col=0).index[-1] == "2026-10-14"
        # before the close the newest completed session is the previous day
        assert F.expected_session(pd.Timestamp("2026-10-14 18:00", tz="UTC"), hourly()) is None or \
            str(F.expected_session(pd.Timestamp("2026-10-14 18:00", tz="UTC"), hourly()).date()) < "2026-10-14"
        # no network: report, never raise
        rep2 = F.ensure(["SPY"], now=pd.Timestamp("2026-10-15 01:00", tz="UTC"), hourly=lambda: (_ for _ in ()).throw(OSError("offline")))
        assert rep2["expected"] is None and "offline" in rep2["error"] and not rep2["stale"] and rep2["check_failed"]
        assert "could not run" in F.banner_line(rep2), F.banner_line(rep2)
    finally:
        F.DAILY_DIR, F.STATE = old_dir, old_state
    print("freshness ok (detect, repair, flag, offline)")


def test_tags_no_lookahead():
    df, spy = rw(1), rw(2)
    x, sx = read(df, spy), read(spy)
    i = 1200
    full = A.tags(x, i, "AAA", dict(spy=sx))
    cut = A.tags(read(df.iloc[:i + 1], spy.iloc[:i + 1]), i, "AAA", dict(spy=read(spy.iloc[:i + 1])))
    for k, v in full.items():
        same = (v == cut[k]) or (isinstance(v, float) and isinstance(cut[k], float) and (math.isnan(v) and math.isnan(cut[k]) or abs(v - cut[k]) < 1e-9))
        assert same, (k, v, cut[k])
    print("context tags ok:", len(full), "tags, identical on truncated data")


def test_paper_trades_full_universe_and_dashboard():
    import yaml
    from ifi import forward as fw
    from ifi.dashboard import build
    c = yaml.safe_load((ROOT / "config.yaml").read_text())
    c = dict(c, forward_test=dict(c.get("forward_test", {}), start="2025-01-01"), etfs=["AAA"])
    spy = read(rw(9))
    frames = {("daily", s): read(rw(k), rw(9)) for k, s in enumerate(["AAA", "BBB", "CCC"], start=10)}
    frames[("daily", "SPY")] = spy
    orig_paper, orig_alloc, orig_health, orig_raf, orig_sent = fw.PAPER, A.ALLOC, A.HEALTH, A.RISK_AT_FILL, fw.SENT
    tmp = Path(tempfile.mkdtemp())
    fw.PAPER, A.ALLOC, A.HEALTH, A.RISK_AT_FILL, fw.SENT = tmp / "pt.csv", tmp / "alloc.json", tmp / "health.json", tmp / "raf.json", tmp / "sent.json"
    import ifi.dashboard as dsh
    orig_docs, dsh.DOCS = dsh.DOCS, tmp / "docs"
    try:
        pt = fw.paper_trades(pd.DataFrame(), frames, c, dict(spy=spy, h4={}))
        assert len(pt) and {"universe", "tag_stage", "tag_stop_width", "tag_signals_same_day"} <= set(pt.columns)
        assert set(pt["universe"]) <= {"etf", "stock"} and (pt[pt["symbol"] == "AAA"]["universe"] == "etf").all()
        full = A.ladder(pt, c, C14)
        board = {k: v for k, v in full.items() if not k.startswith("_")}
        hl = A.health(pt, c, C14)
        assert all(0 <= v["risk"] <= 0.01 for v in board.values())
        build(frames, pd.DataFrame(), {}, c, pt, board, {}, alloc_meta=full["_portfolio"], health=hl,
              fresh=dict(stale=True, expected="2026-10-14", spy_last="2026-10-13", still_stale=["BBB"]), c14=C14)
        page = (tmp / "docs" / "index.html").read_text()
        for s_ in ("Allocation (forward test)", "Process health", "Candidates", "Data stale"):
            assert s_ in page, s_
    finally:
        fw.PAPER, A.ALLOC, A.HEALTH, A.RISK_AT_FILL, fw.SENT, dsh.DOCS = orig_paper, orig_alloc, orig_health, orig_raf, orig_sent, orig_docs
    print("full-universe paper trades with tags, ladder, health and dashboard ok:", len(pt), "paper rows")


def test_block_streak_keeps_clustering():
    """A history with bad-market clusters: the block bootstrap sees long streaks as more likely than i.i.d. odds,
    so a normal bad-market streak is not flagged (v1.4.1)."""
    rng = np.random.default_rng(4)
    regimes = np.repeat(rng.random(60) < 0.25, 50)                 # 25% of 50-trade stretches are bad markets
    losses = np.where(regimes, rng.random(3000) < 0.8, rng.random(3000) < 0.45)
    p_win = 1 - losses.mean()
    p_iid = A.streak_probability(12, 50, p_win)
    p_blk = A.streak_probability_block(12, 50, losses, 20)
    assert p_blk > 5 * p_iid and p_iid < 0.01, (p_iid, p_blk)
    assert np.isnan(A.streak_probability_block(5, 20, losses[:30], 20))   # too short a history: caller falls back
    print(f"block streak ok: P(12 losses in a row within 50) i.i.d. {p_iid:.4f} vs block bootstrap {p_blk:.3f}")


def test_digest_and_alert_log():
    import json
    import yaml
    from ifi import digest as G
    from ifi import forward as fw
    c = yaml.safe_load((ROOT / "config.yaml").read_text())
    c = dict(c, forward_test=dict(c.get("forward_test", {}), start="2025-01-01"), etfs=["AAA"])
    spy = read(rw(9))
    frames = {("daily", s): read(rw(k), rw(9)) for k, s in enumerate(["AAA", "BBB"], start=10)}
    tmp = Path(tempfile.mkdtemp())
    saved = fw.PAPER, A.ALLOC, A.HEALTH, A.RISK_AT_FILL, fw.SENT, G.ALERTS, G.DIGEST
    fw.PAPER, A.ALLOC, A.HEALTH, A.RISK_AT_FILL, fw.SENT = tmp / "pt.csv", tmp / "a.json", tmp / "h.json", tmp / "r.json", tmp / "s.json"
    G.ALERTS, G.DIGEST = tmp / "alerts.jsonl", tmp / "digest.json"
    try:
        pt = fw.paper_trades(pd.DataFrame(), frames, c, dict(spy=spy, h4={}))
        full = A.ladder(pt, c, C14)
        board = {k: v for k, v in full.items() if not k.startswith("_")}
        hl = A.health(pt, c, C14)
        now = pd.Timestamp("2026-10-16 22:30", tz="UTC")
        for k in range(3):
            G.log_alerts([f"line {k}"], now - pd.Timedelta(days=10 * (2 - k)))
        G.log_alerts([], now)                                          # no lines: nothing written
        assert len(G.ALERTS.read_text().splitlines()) == 3
        assert [r["lines"] for r in G.recent_alerts(7, now)] == [["line 2"]]
        new_rows = [dict(family="Playbook", symbol="AAA", tf="daily", event="E4 anchor reclaim", close=10.0, stop=9.0,
                         target=13.0, shares_1pct=100, cancel_if_open_below=9.5)]
        lines = G.alert_text(c, new_rows, ["⚠ test"])
        assert lines[0] == "⚠ test" and lines[1].startswith("★ AAA daily")
        G.write_digest(pt, board, full["_portfolio"], hl, dict(expected="2026-10-16", stale=False), C14, new_rows, lines, now)
        d = json.loads(G.DIGEST.read_text())
        for k in ("freshness", "allocation", "portfolio", "health", "paper", "playbook_new", "alerts_this_run", "candidates", "research"):
            assert k in d, k
        assert d["playbook_new"][0]["symbol"] == "AAA" and d["alerts_last_7d"] == 1
        views = {t["f1_view"] for grp in ("open", "closed_recent", "pending") for t in d["paper"][grp] if t["setup"] == "E4"}
        assert views <= {"take", "skip", "unknown"}
        assert G.f1_view(pd.Series(dict(setup="E4_anchor_reclaim", tag_dist_anchor_atr=2.0, tag_stage=3))) == "skip"
        assert G.f1_view(pd.Series(dict(setup="E4_anchor_reclaim", tag_dist_anchor_atr=0.4, tag_stage=0))) == "skip"
        assert G.f1_view(pd.Series(dict(setup="E4_anchor_reclaim", tag_dist_anchor_atr=0.4, tag_stage=2))) == "take"
        assert G.f1_view(pd.Series(dict(setup="E1_trigger_with_trend", tag_dist_anchor_atr=3.0, tag_stage=2))) is None
        json.dumps(d)
    finally:
        fw.PAPER, A.ALLOC, A.HEALTH, A.RISK_AT_FILL, fw.SENT, G.ALERTS, G.DIGEST = saved
    print("alert log and digest ok:", len(d["paper"]["open"]), "open,", d["paper"]["live_closed_n"], "live closed")


def test_v15_live_evidence():
    """Shadow books, random-entry control, live edge, review progress, extended-universe labels and dashboard."""
    import json
    import yaml
    from ifi import forward as fw
    from ifi import shadow as SH
    import ifi.dashboard as dsh
    c = yaml.safe_load((ROOT / "config.yaml").read_text())
    c = dict(c, forward_test=dict(c.get("forward_test", {}), start="2024-06-01"), etfs=["AAA"], _extended=["BBB"])
    frames = {("daily", s): read(rw(k), rw(9)) for k, s in enumerate(["AAA", "BBB", "CCC"], start=10)}
    tmp = Path(tempfile.mkdtemp())
    saved = fw.PAPER, A.ALLOC, A.HEALTH, A.RISK_AT_FILL, fw.SENT, SH.RANDOM, SH.SHADOW, dsh.DOCS
    fw.PAPER, A.ALLOC, A.HEALTH, A.RISK_AT_FILL, fw.SENT = tmp / "pt.csv", tmp / "a.json", tmp / "h.json", tmp / "r.json", tmp / "s.json"
    SH.RANDOM, SH.SHADOW, dsh.DOCS = tmp / "rc.csv", tmp / "sb.csv", tmp / "docs"
    try:
        pt = fw.paper_trades(pd.DataFrame(), frames, c, dict(spy=read(rw(9)), h4={}))
        assert set(pt["group"]) <= {"core", "extended"} and (pt[pt["symbol"] == "BBB"]["group"] == "extended").all()
        rc = SH.random_control(frames, c, C14)
        assert len(rc) and (pd.to_datetime(rc["fill_date"]) >= "2024-06-01").all()
        # the same past random entries when the history is one bar shorter (generator prefix is stable)
        short = {k: v.iloc[:-1] for k, v in frames.items()}
        rc2 = SH.random_control(short, c, C14)
        a = set(zip(rc["symbol"], rc["seed"], rc["fill_date"].astype(str)))
        b = set(zip(rc2["symbol"], rc2["seed"], rc2["fill_date"].astype(str)))
        assert b <= a, "random entries changed when the history grew"
        ed = SH.live_edge(pt, rc)
        assert ed and ed[-1]["slice"] == "all setups"
        books = SH.shadow_books(pt, C14, "2026-10-16")
        assert set(books) == {"B0", "C1", "S20"} and books["B0"]["taken"] <= books["S20"]["taken"]
        SH.shadow_books(pt, C14, "2026-10-16")                     # same session again: replaced, not appended
        assert len(pd.read_csv(SH.SHADOW)) == 3
        rv = SH.review_progress(pt, C14, pd.Timestamp("2026-10-16"))
        assert [r["id"] for r in rv] == ["R1", "R2", "R3"] and not any(r["due"] for r in rv)
        rv_due = SH.review_progress(pt, dict(C14, reviews=[dict(id="X", closed_trades=1, what="q")]), pd.Timestamp("2026-10-16"))
        assert rv_due[0]["due"] == (int((pt["oos"].astype(bool) & (pt["status"] == "closed")).sum()) >= 1)
        full = A.ladder(pt, c, C14)
        dsh.build(frames, pd.DataFrame(), {}, c, pt, {k: v for k, v in full.items() if not k.startswith("_")}, {},
                  alloc_meta=full["_portfolio"], health=A.health(pt, c, C14), fresh={}, c14=C14,
                  live_ev=dict(edge=ed, books=books, reviews=rv))
        assert "Live evidence" in (tmp / "docs" / "index.html").read_text()
    finally:
        fw.PAPER, A.ALLOC, A.HEALTH, A.RISK_AT_FILL, fw.SENT, SH.RANDOM, SH.SHADOW, dsh.DOCS = saved
    print(f"v1.5 live evidence ok: {len(rc)} random-control trades, books taken " + str({k: v['taken'] for k, v in books.items()}))


def test_v15_book_rules():
    from ifi import shadow as SH
    d = pd.to_datetime
    live = pd.DataFrame(dict(symbol=list("ABCDEFG"), setup="E4_anchor_reclaim",
                             fill_date=d(["2026-10-13"] * 6 + ["2026-10-20"]), exit_date=d(["2026-10-15"] + [None] * 6),
                             status=["closed"] + ["open"] * 6, r=[2.0, 0.5, -0.5, 0.1, 0.2, 0.3, 1.0],
                             fill=100.0, stop=95.0))
    b0 = SH._book(live, 5, 0.0075, 1.0)
    assert b0["taken"] == 6 and b0["skipped"] == 1            # 5 on Oct 13; A closed Oct 15 frees a slot for G on Oct 20
    assert abs(b0["equity"] - (100_000 + 750 * (2.0 + 0.5 - 0.5 + 0.1 + 0.2 + 1.0))) < 1e-6
    c1 = SH._book(live, None, 0.001, 1.0)
    assert c1["taken"] == 7                                   # 0.1% risk / 5% stop = 2% notional each
    tight = SH._book(live, None, 0.01, 0.5)                   # 1% / 5% = 20% notional: two fit under 50%
    assert tight["taken"] == 3                                 # 2 on Oct 13, then A's exit frees room for G
    print("v1.5 shadow book rules ok (slots, cash, exits free capacity)")


if __name__ == "__main__":
    test_ladder_math()
    test_calibration_direction()
    test_streak_and_ks()
    test_portfolio_drawdown()
    test_drawdown_weights_and_nan()
    test_breaker_latch()
    test_freshness()
    test_tags_no_lookahead()
    test_paper_trades_full_universe_and_dashboard()
    test_block_streak_keeps_clustering()
    test_digest_and_alert_log()
    test_v15_live_evidence()
    test_v15_book_rules()
    print("all v1.4 tests passed")
