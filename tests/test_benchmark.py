"""Benchmark test v1 unit tests: trend rule without look-ahead and with switch costs, OLS and alpha recovery,
matched-volatility scaling, verdict logic, prereg, lock.  Run: python tests/test_benchmark.py (also under pytest)"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from research.benchmark import run as BM  # noqa: E402

PR = yaml.safe_load(BM.PREREG.read_text())
P = PR["params"]


def _px(n=1500, seed=3):
    rng = np.random.default_rng(seed)
    d = pd.bdate_range("2001-01-02", periods=n)
    return pd.Series(100 * np.exp(np.cumsum(rng.normal(0.0003, 0.012, n))), index=d)


def test_prereg():
    assert PR["books"]["primary"] == "B0" and PR["params"]["tr_window"] == 200 and PR["params"]["p_min"] == 0.95
    assert set(PR["verdict"]) >= {"EDGE", "PARTIAL", "NO_EDGE_BEYOND_BENCHMARKS"}
    print("prereg ok")


def test_trend_rule_no_lookahead_and_costs():
    px = _px()
    full = BM.trend_positions(px, 200)
    for cut in (400, 900, 1400):
        part = BM.trend_positions(px.iloc[:cut + 1], 200)
        assert (full.iloc[:cut + 1] == part).all(), cut
    assert (full.iloc[:200] == 0).all()
    bd = BM.bench_daily(px, px.index, 200, 0.0005)
    r = px.pct_change().fillna(0.0)
    sw = full.diff().abs().fillna(0.0)
    assert np.allclose(bd["TR"], full * r - 0.0005 * sw)
    assert np.allclose(bd["BH"], r)
    print(f"trend rule ok: positions use only past closes; {int(sw.sum())} switches charged")


def test_alpha_recovery_and_matched():
    px = _px(6300, 5)
    bd = BM.bench_daily(px, px.index, 200, 0.0005)
    bm = pd.DataFrame({k: BM.to_monthly(bd[k]) for k in ("BH", "TR")})
    exact = BM.measure(0.5 * bm["BH"] + 0.2 * bm["TR"] + 0.03 / 12, bm, dict(P, boot_reps=50))
    assert abs(exact["alpha2"] - 0.03) < 1e-9 and abs(exact["beta2_spy"] - 0.5) < 1e-9 and abs(exact["beta2_tr"] - 0.2) < 1e-9
    noise = pd.Series(np.random.default_rng(2).normal(0, 0.01, len(bm)), index=bm.index)   # alpha SE here ~0.9%/yr
    m = BM.measure(0.5 * bm["BH"] + 0.2 * bm["TR"] + 0.03 / 12 + noise, bm, dict(P, boot_reps=1000))
    assert abs(m["beta2_spy"] - 0.5) < 0.06 and abs(m["beta2_tr"] - 0.2) < 0.1 and abs(m["alpha2"] - 0.03) < 0.027, m
    assert m["a2_lo"] < m["alpha2"] < m["a2_hi"] and 0 <= m["p_tr"] <= 1
    daily = 0.5 * bd["BH"]
    mt = BM.matched(daily, bd)
    assert abs(mt["BH"]["scale"] - 0.5) < 1e-9 and abs(mt["BH"]["cagr"] - mt["book"]["cagr"]) < 1e-9
    print(f"alpha recovery ok: alpha {100 * m['alpha2']:.2f}% (planted 3%), betas {m['beta2_spy']:.2f}/{m['beta2_tr']:.2f}")


def test_verdict():
    base = dict(a2_lo=-0.01, p_tr=0.5, p_bh=0.5)
    assert BM.verdict(base, P)[0] == "NO_EDGE_BEYOND_BENCHMARKS"
    assert BM.verdict(dict(base, a2_lo=0.001), P)[0] == "PARTIAL"
    assert BM.verdict(dict(base, p_tr=0.96), P)[0] == "PARTIAL"
    assert BM.verdict(dict(base, a2_lo=0.001, p_tr=0.96), P)[0] == "EDGE"
    print("verdict logic ok")


def test_synthetic_checks():
    ok, msgs = BM.synthetic(P)
    assert ok, msgs


def test_lock():
    pr, lk = BM.check_lock()
    print("benchmark lock ok:", lk[:16])


if __name__ == "__main__":
    test_prereg()
    test_trend_rule_no_lookahead_and_costs()
    test_alpha_recovery_and_matched()
    test_verdict()
    test_synthetic_checks()
    test_lock()
    print("all benchmark tests passed")
