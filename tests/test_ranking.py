"""Ranking test v1 unit tests: features match the live tags, no look-ahead, book parity with the exit test,
sequencing, notional cap, filter-before-sequencing, planted effect, bootstrap helper, lock.
Run: python tests/test_ranking.py   (also works under pytest)"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ifi.allocation import tags  # noqa: E402
from research import engine as E  # noqa: E402
from research.exits import run as XR  # noqa: E402
from research.exits import sim as S  # noqa: E402
from research.exits.synth import trend_loader  # noqa: E402
from research.ranking import run as RK  # noqa: E402

PR = yaml.safe_load(RK.PREREG.read_text())
CX = yaml.safe_load(XR.PREREG.read_text())
_T = {}


def trades():
    if not _T:
        L = trend_loader(5)
        F = XR.load_frames(L, ["XLE", "XLK", "XLU", "XLF", "XLI"], 600)
        _T["F"] = F
        _T["T"] = RK.build_trades(F, CX, 0.0005)
    return _T["F"], _T["T"]


def test_prereg_shape():
    assert PR["params"]["k"] == len(RK.ARMS) == 1 and RK.ARMS == ["F1"]
    assert PR["params"]["dist_max"] == 1.5 and PR["params"]["stage_min"] == 1 and PR["params"]["notional_cap"] == 0.2
    assert len(PR["data"]["manifest_prefix"]) == 16
    print("prereg ok: one arm (F1), k = 1, manifest prefix pinned")


def test_features_match_live_tags_and_no_lookahead():
    F, _ = trades()
    x = F["XLE"]
    for t in (700, 1500, 3000, len(x) - 1):
        f = RK.features(x, t)
        g = tags(x, t, "XLE", {}, live=False)
        assert f["stage"] == g["tag_stage"], (t, f, g)
        assert abs(f["width"] - g["tag_stop_width"]) < 1e-4 and (np.isnan(g["tag_dist_anchor_atr"]) or abs(f["dist"] - g["tag_dist_anchor_atr"]) < 1e-4)
    raw = trend_loader(5)("XLE")
    full = E.base(raw)
    for cut in (900, 2000):
        part = E.base(raw.iloc[:cut + 1])
        a, b = RK.features(full, cut), RK.features(part, cut)
        assert a["stage"] == b["stage"] and abs(a["width"] - b["width"]) < 1e-12 and \
            ((np.isnan(a["dist"]) and np.isnan(b["dist"])) or abs(a["dist"] - b["dist"]) < 1e-9), (cut, a, b)
    print("features ok: equal to the live paper tags; identical on truncated data")


def test_sequence_and_parity():
    F, T = trades()
    bk = RK.Book(T, 0.0075, 5)
    assert set(bk.sequence()) == set(S.no_overlap(bk.T).index)
    mine = bk.run(own_calendar=True)
    lab = XR.portfolio(T, "X3", dict(CX, params=dict(CX["params"], risk_pct=0.0075, max_open=5)))
    assert mine["trades"] == lab["trades"] and abs(mine["cagr"] - lab["cagr"]) < 1e-12 and abs(mine["max_dd"] - lab["max_dd"]) < 1e-12
    print(f"book parity ok: {mine['trades']} trades, identical CAGR and drawdown to the exit-test portfolio")


def test_cap_scales_tight_stops():
    F, T = trades()
    bk = RK.Book(T, 0.0075, 5)
    unc, cap = bk.run(), bk.run(cap=0.2)
    assert cap["exposure"] <= unc["exposure"] + 1e-12
    tight = T.copy()
    tight["width_fill"] = 0.01                   # 1% stops: 0.75% risk would need 75% notional; capped at 20%
    cv_u = RK.Book(tight, 0.0075, 5).run(curve=True)["curve"]
    cv_c = RK.Book(tight, 0.0075, 5).run(cap=0.2, curve=True)["curve"]
    ru, rc = cv_u.diff().abs().sum(), cv_c.diff().abs().sum()
    assert rc < ru * (0.2 * 0.01 / 0.0075) * 1.05 + 1e-6 and rc > 0, (ru, rc)
    print("notional cap ok: tight stops are scaled down (1% stop -> 0.267x)")


def test_filter_frees_the_symbol():
    idx = pd.bdate_range("2020-01-01", periods=40)
    XR.FRAMES_INDEX["ZZZ"] = idx
    T = pd.DataFrame(dict(sym="ZZZ", t=[5, 8], e=[6, 9], exit_i=[20, 25], date=[idx[5], idx[8]], entry_date=[idx[6], idx[9]],
                          exit_date=[idx[20], idx[25]], rt=[1.0, 2.0], width_fill=0.05, dist=[2.0, 0.2], stage=3,
                          path=[np.linspace(0.1, 1.0, 15), np.linspace(0.1, 2.0, 17)]))
    bk = RK.Book(T, 0.01, 5)
    assert list(bk.sequence()) == [0]                        # the second signal falls inside the first trade
    keep, _ = RK.arm_inputs(T, "F1", PR)
    assert list(keep) == [False, True]
    assert list(bk.sequence(keep)) == [1]                    # skipping the extended one frees the symbol
    r = bk.run(keep=keep, curve=True)
    assert r["trades"] == 1 and abs(r["curve"].iloc[-1] - 100_000 * 1.02) < 1e-6, r["curve"].iloc[-1]
    print("filter ok: applied before sequencing, a skipped signal frees its symbol")


def test_plant():
    F, T = trades()
    P = RK.plant(T, "F1", PR, -0.5)
    keep, _ = RK.arm_inputs(T, "F1", PR)
    bad = ~keep
    assert np.allclose(P.loc[bad, "rt"], T.loc[bad, "rt"] - 0.5) and np.allclose(P.loc[~bad, "rt"], T.loc[~bad, "rt"])
    for i in np.flatnonzero(bad)[:20]:
        assert abs(P["path"].iloc[i][-1] - (T["path"].iloc[i][-1] - 0.5)) < 1e-12
    print("planted effect ok: -0.5 R on exactly the trades F1 skips, final mark shifted")


def test_block_diff():
    d = pd.bdate_range("2001-01-01", periods=2000)
    rng = np.random.default_rng(0)
    a, b = rng.normal(0.3, 1, 2000), rng.normal(0.0, 1, 2000)
    o = RK.block_diff([(a, d, 1), (b, d, -1)], 6, 2000, 7)
    assert abs(o["est"] - (a.mean() - b.mean())) < 1e-12 and o["lo"] < o["est"] < o["hi"] and o["lo"] > 0
    print("block bootstrap ok")


def test_lock():
    pr, cx, lk = RK.check_lock()
    print("ranking lock ok:", lk[:16])


if __name__ == "__main__":
    test_prereg_shape()
    test_features_match_live_tags_and_no_lookahead()
    test_sequence_and_parity()
    test_cap_scales_tight_stops()
    test_filter_frees_the_symbol()
    test_plant()
    test_block_diff()
    test_lock()
    print("all ranking tests passed")
