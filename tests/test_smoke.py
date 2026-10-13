"""Smoke tests: indicators compute on real sample data, and a pure random walk shows no edge
(an edge on random data would mean look-ahead bias in the engine). Run: python tests/test_smoke.py"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ifi import backtest as bt  # noqa: E402
from ifi.indicators import signals  # noqa: E402
from ifi.states import read  # noqa: E402


def sample():
    df = pd.read_csv(ROOT / "tests" / "fixtures" / "GOOG.csv", index_col=0, parse_dates=True)
    df.columns = [c.lower() for c in df.columns]
    return df


def random_walk(seed, n=3000):
    rng = np.random.default_rng(seed)
    c = 100 * np.exp(np.cumsum(rng.normal(0, 0.012, n)))
    o = np.r_[c[0], c[:-1]] * np.exp(rng.normal(0, 0.002, n))
    h = np.maximum(o, c) * np.exp(np.abs(rng.normal(0, 0.006, n)))
    l = np.minimum(o, c) * np.exp(-np.abs(rng.normal(0, 0.006, n)))
    return pd.DataFrame(dict(open=o, high=h, low=l, close=c, volume=rng.integers(1e6, 5e6, n)),
                        index=pd.bdate_range("2005-01-03", periods=n))


def test_indicators():
    x = read(sample())
    last = x.iloc[-1]
    for col in ("ad_flow", "sig_wt1", "sig_channel", "mx_rsi", "tr_line", "tr_anchor", "atr"):
        assert np.isfinite(last[col]), col
    assert x["score"].between(0, 5).all()
    s1, s2 = signals(sample(), False), signals(sample(), True)
    assert (s2["trig_bull"] & ~s1["trig_bull"]).sum() == 0, "2.0 triggers must be a subset of 1.0 triggers"
    print("indicators ok · 1.0 bullish triggers that were bearish crosses:",
          int((s1["trig_bull"] & ~s2["trig_bull"]).sum()), "of", int(s1["trig_bull"].sum()))


def test_no_lookahead():
    rs = []
    for k in range(6):
        x = read(random_walk(k))
        for name, ent in bt.setups(x).items():
            for ex in ("X2_target2R", "X4_trendline_trail"):
                rs += [t.r for t in bt.simulate(f"RW{k}", x, ent, name, ex, cost=0.0)]
    m = bt.metrics(np.array(rs))
    print(f"random-walk check: n={m['n']} expectancy={m['expectancy']:+.3f}R CI=({m['ci_low']:+.3f},{m['ci_high']:+.3f})")
    assert m["ci_low"] < 0.05, "positive edge on a random walk -> look-ahead bias"


# Values read from TradingView (IFI 1.0, 4H) on the bar each fixture ends with. SMH was ~6 min before its
# bar closed, so its tolerances are tight; XLF/XLU were mid-bar, so only the slow Trend line is held tight.
GOLDEN = {
    "SMH": dict(tol=dict(tr_line=0.1, sig_wt1=0.5, sig_wt2=0.5, sig_channel=0.5, mx_rsi=0.5),
                tv=dict(tr_line=603.86, sig_wt1=15.37, sig_wt2=30.73, sig_channel=6.05, mx_rsi=45.88)),
    "XLF": dict(tol=dict(tr_line=0.05, sig_wt1=2.0, sig_wt2=2.0, sig_channel=2.0),
                tv=dict(tr_line=54.69, sig_wt1=-17.64, sig_wt2=-29.26, sig_channel=-29.03)),
    "XLU": dict(tol=dict(tr_line=0.05, sig_wt1=2.0, sig_wt2=2.0),
                tv=dict(tr_line=40.85, sig_wt1=32.16, sig_wt2=28.62)),
}


def test_parity_with_tradingview():
    from ifi.indicators import compute_all
    for sym, g in GOLDEN.items():
        df = pd.read_csv(ROOT / "tests" / "fixtures" / f"{sym}_4h_golden.csv", index_col=0, parse_dates=True)
        last = compute_all(df, v2=False).iloc[-1]
        for k, tv in g["tv"].items():
            diff = abs(last[k] - tv)
            assert diff <= g["tol"][k], f"parity drift {sym} {k}: python {last[k]:.3f} vs TradingView {tv} (diff {diff:.3f})"
    print("parity with TradingView ok:", ", ".join(GOLDEN))


if __name__ == "__main__":
    test_parity_with_tradingview()
    test_indicators()
    test_no_lookahead()
    print("all smoke tests passed")
