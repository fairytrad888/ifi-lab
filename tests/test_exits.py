"""Exit-test unit tests: hand-built trades for every exit, Lab parity, truncation, lock.
Run: python tests/test_exits.py   (also works under pytest)"""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from research import engine as E  # noqa: E402
from research.exits import run as R  # noqa: E402
from research.exits import sim as S  # noqa: E402
from research.exits.synth import martingale_loader, trend_loader  # noqa: E402

NA = np.nan
X = {"X3": dict(target_r=3.0, time_cap=60), "X8": dict(target_r=3.0, chandelier_atr=3.0, time_cap=250),
     "X9": dict(target_r=3.0, time_cap=40), "X10": dict(time_cap=250), "X11": dict(time_cap=250),
     "X12": dict(target_r=3.0, time_cap=60)}
P = dict(piv=3, xb_warn=2, xb_win=20)


def book(n=80, base=10.0):
    """Flat market: entry signal at t=10, fill 10.0 at bar 11, stop 9.0 (5-bar low 9.5 - 0.5*ATR 1.0) -> 1R = 1.0."""
    o = np.full(n, base)
    h = np.full(n, base + 0.2)
    l = np.full(n, base - 0.2)
    c = np.full(n, base)
    l[6:11] = 9.5
    A = dict(o=o, h=h, l=l, c=c, a=np.ones(n), atr=np.full(n, 1.0), low5=None, ph=np.full(n, NA), pl=np.full(n, NA),
             last_pl=np.full(n, NA), breakdown=np.zeros(n, bool), warn_cum=np.zeros(n, int), n=n)
    return A


def fin(A):
    A["low5"] = np.array([np.min(A["l"][max(0, i - 4):i + 1]) for i in range(A["n"])])
    return A


def run(A, kind, cost=0.0):
    return S.simulate(fin(A), 10, kind, X, P, cost)


def test_x3_target_stop_time():
    A = book()
    A["h"][20] = 13.5
    r = run(A, "X3")
    assert r["why"] == "target" and abs(r["r"] - 3.0) < 1e-12 and r["exit_i"] == 20, r
    A = book()
    A["h"][20], A["l"][20] = 13.5, 8.5          # stop and target in one bar: stop first
    r = run(A, "X3")
    assert r["why"] == "stop" and abs(r["r"] + 1.0) < 1e-12, r
    A = book()
    A["o"][15], A["l"][15] = 8.0, 7.9           # gap through the stop fills at the open
    r = run(A, "X3")
    assert r["why"] == "stop_gap" and abs(r["r"] + 2.0) < 1e-12, r
    A = book()
    A["c"][70] = 10.5
    r = run(A, "X3")                            # nothing hits: time exit at the close of bar 11 + 59 = 70
    assert r["why"] == "time" and r["exit_i"] == 70 and abs(r["r"] - 0.5) < 1e-12, r
    r = run(book(), "X9")
    assert r["why"] == "time" and r["exit_i"] == 50, r
    print("X3 / X9 ok")


def test_x8_partial_then_trail():
    A = book(120)
    A["h"][20] = 13.0                           # 3R hit: half banked at 13 (+1.5R)
    A["h"][21:30] = 16.0                        # highest high 16 -> trail 16 - 3 = 13
    A["c"][21:30] = 15.0
    A["o"][21:30] = 15.0
    A["l"][21:30] = 14.0
    A["o"][30], A["h"][30], A["l"][30], A["c"][30] = 13.5, 13.6, 12.5, 12.8   # trail at 13 hit inside the bar
    r = run(A, "X8")
    assert r["why"] == "trail" and r["exit_i"] == 30, r
    assert abs(r["r"] - (0.5 * 3.0 + 0.5 * 3.0)) < 1e-12, r
    print("X8 ok")


def test_x10_x11_x12():
    A = book(120)
    A["c"][12:40] = np.linspace(10.2, 12.0, 28)
    A["h"][12:40] = A["c"][12:40] + 0.1
    A["ph"][25] = 12.5                          # pivot at bar 22 (>= entry bar 11): the peak
    A["ph"][33] = 12.2                          # lower pivot high
    A["pl"][30] = 11.5
    A["c"][36] = 11.4                           # close below the last pivot low -> exit next open (37)
    A["o"][37] = 11.3
    r = run(A, "X10")
    assert r["why"] == "rule3" and r["exit_i"] == 37 and abs(r["r"] - 1.3) < 1e-9, r
    r12 = run(A, "X12")
    assert r12["why"] == "rule3" and r12["exit_i"] == 37, r12
    B = book(120)
    B["c"][12:40] = 11.0
    B["breakdown"][25] = True
    B["warn_cum"][:] = np.cumsum(np.isin(np.arange(120), [15, 20]).astype(int))
    B["o"][26] = 10.8
    r = run(B, "X11")
    assert r["why"] == "fast" and r["exit_i"] == 26 and abs(r["r"] - 0.8) < 1e-9, r
    C = book(120)
    C["c"][12:40] = 11.0
    C["breakdown"][25] = True
    C["warn_cum"][:] = np.cumsum(np.isin(np.arange(120), [20]).astype(int))   # only 1 warning -> no fast exit
    r = run(C, "X11")
    assert r["why"] != "fast", r
    print("X10 / X11 / X12 ok")


def test_lab_parity_and_truncation():
    cfg, _ = R.check_lock()
    L = trend_loader(9)
    F = R.load_frames(L, ["AAA", "BBB", "CCC"], 600)
    ok, msg = R.lab_parity(F, cfg)
    assert ok, msg
    # truncation: a trade that has exited is unchanged when the data is cut 2 bars after its exit
    Pm = R.engine_params(cfg)
    Xm = R.exit_defs(cfg)
    x = F["AAA"]
    ev = E.events(x, Pm)
    A = S.arrays(x, ev)
    checked = 0
    for t in np.flatnonzero(ev["reclaim"])[5:40:5]:
        for k in ("X10", "X11", "X8"):
            full = S.simulate(A, int(t), k, Xm, Pm, 0.0005)
            if not full or full["cancelled"] or full["why"] == "open_at_end":
                continue
            cut = full["exit_i"] + 2
            xc = E.base(L("AAA").iloc[:cut])
            evc = E.events(xc, Pm)
            part = S.simulate(S.arrays(xc, evc), int(t), k, Xm, Pm, 0.0005)
            assert abs(part["r"] - full["r"]) < 1e-12 and part["exit_i"] == full["exit_i"], (k, t, full, part)
            checked += 1
    assert checked >= 6, checked
    print("Lab parity ok:", msg, "| truncation ok on", checked, "trades")


def test_dividends_and_path():
    A = book()
    A["c"][70] = 10.5
    A["a"][25:] = 1.02                          # a 2% dividend goes ex on bar 25 during the hold
    r = S.simulate(fin(A), 10, "X3", X, P, 0.0, path=True)
    assert abs(r["r"] - 0.5) < 1e-12 and abs(r["rt"] - (10.5 * 1.02 - 10.0)) < 1e-12, r
    assert len(r["path"]) == r["bars"] == 60 and abs(r["path"][-1] - r["rt"]) < 1e-12, r
    assert abs(r["path"][20] - (10.0 * 1.02 - 10.0)) < 1e-12        # bar 31 marked with the dividend credited
    print("dividends and marked path ok")


def test_mtm_portfolio():
    import pandas as pd
    cfg, _ = R.check_lock()
    idx = pd.bdate_range("2010-01-04", periods=40)
    rows = []
    for k in range(7):                          # 7 symbols enter the same day: only max_open = 5 are taken
        sym = f"S{k}"
        R.FRAMES_INDEX[sym] = idx
        path = np.r_[np.linspace(-0.5, 1.0, 9), 1.0]
        rows.append(dict(sym=sym, seed=0, t=2, date=idx[2], kind="X3", r=1.0, rt=1.0, bars=10, why="time", e=3,
                         exit_i=12, exit_date=idx[12], entry_date=idx[3], path=path))
    pf = R.portfolio(pd.DataFrame(rows, columns=R.COLS), "X3", cfg)
    assert pf["trades"] == 5, pf
    # 5 trades x 0.75% risk x -0.5R at the worst mark = -1.875% drawdown, final +3.75%
    assert abs(pf["max_dd"] + 5 * 0.0075 * 0.5) < 1e-9, pf
    print("mark-to-market portfolio ok")


def test_yahoo_parsing():
    """The snapshot downloader keeps Adj Close from yfinance's multi-ticker frame (yf.download is faked)."""
    import sys as _sys
    import types

    import pandas as pd
    from research.exits import data as Dm
    idx = pd.bdate_range("2020-01-01", periods=5)
    cols = pd.MultiIndex.from_product([["AAA", "BBB"], ["Open", "High", "Low", "Close", "Adj Close", "Volume"]])
    raw = pd.DataFrame(np.tile([10, 11, 9, 10.5, 10.2, 1000], (5, 2)).astype(float), index=idx, columns=cols)
    fake = types.SimpleNamespace(download=lambda *a, **k: raw)
    real = _sys.modules.get("yfinance")
    _sys.modules["yfinance"] = fake
    try:
        got = Dm._yahoo(["AAA", "BBB", "CCC"])
    finally:
        if real is not None:
            _sys.modules["yfinance"] = real
        else:
            del _sys.modules["yfinance"]
    assert set(got) == {"AAA", "BBB"} and list(got["AAA"].columns) == ["open", "high", "low", "close", "volume", "adjclose"], got
    assert abs(got["AAA"]["adjclose"].iloc[0] - 10.2) < 1e-12
    print("Yahoo parsing ok (Adj Close kept)")


def test_lock():
    cfg, fp = R.check_lock()
    assert cfg["stats"]["k"] == len(cfg["stats"]["comparisons"]) == 5
    print("exit lock ok:", fp[:16])


if __name__ == "__main__":
    test_x3_target_stop_time()
    test_x8_partial_then_trail()
    test_x10_x11_x12()
    test_dividends_and_path()
    test_mtm_portfolio()
    test_yahoo_parsing()
    test_lock()
    test_lab_parity_and_truncation()
    print("all exit tests passed")
