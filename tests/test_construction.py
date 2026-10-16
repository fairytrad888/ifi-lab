"""Construction test v1 unit tests: trades equal the Lab's, marks end at R, book accounting, slots, day cap, cash rule,
whole shares, same-day exits, bootstrap, regime months without look-ahead, sealed universe rule, lock.
Run: python tests/test_construction.py   (also works under pytest)"""
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ifi import backtest as bt  # noqa: E402
from ifi.states import read  # noqa: E402
from research.construction import run as C  # noqa: E402
from research.exits.synth import trend_loader  # noqa: E402

PR = yaml.safe_load(C.PREREG.read_text())


def test_prereg_and_sealed_rule():
    U = PR["sealed_universe"]
    assert len(U["etfs"]) == 38 and len(U["stocks"]) == 54 and len(set(U["etfs"] + U["stocks"])) == 92
    W = yaml.safe_load((ROOT / "research" / "exits" / "prereg_exits_v1.yaml").read_text())["universe"]
    c = yaml.safe_load((ROOT / "config.yaml").read_text())
    used = set(W["etfs"]) | set(W["stocks"]) | set(c["etfs"]) | {s for v in c["stocks"].values() for s in v}
    assert not used & set(U["etfs"] + U["stocks"]), "sealed set overlaps the working universe"
    B = PR["books"]
    assert B["B0"]["slots"] == 5 and B["B0"]["risk"] == 0.0075 and B["C1"]["slots"] is None and B["C1"]["risk"] == 0.001
    assert PR["params"]["p_min"] == 0.95 and PR["trades"]["setups"] == C.SETUPS
    print("prereg ok: 92 sealed symbols, none in the working universe; B0 5 x 0.75%, C1 every signal at 0.10%")


def test_trades_equal_lab_and_marks():
    L = trend_loader(5)
    T, F = C.build_trades(L, ["AAA", "BBB", "CCC"], {"AAA"}, PR)
    for s in ("AAA", "BBB", "CCC"):
        x = read(L(s)[["open", "high", "low", "close", "volume"]])
        x = x[x.index >= "2000-01-01"]
        cost = 0.0005 if s == "AAA" else 0.0010
        lab = [t for su, e in bt.setups(x).items() if su in C.SETUPS for t in bt.simulate(s, x, e, su, C.EXIT, cost)]
        mine = T[T["symbol"] == s]
        assert len(lab) == len(mine)
        assert np.allclose(sorted(t.r for t in lab), sorted(mine["r"]))
    for row in T.head(50).itertuples():
        assert abs(row.marks[-1] - row.r) < 1e-12 and len(row.marks) == len(row.mdates)
    print(f"trades ok: {len(T)} trades identical to ifi/backtest.py; every mark path ends at the trade's R")


def _toy(n_days=30):
    days = pd.bdate_range("2020-01-01", periods=n_days)
    frames = {"X": pd.DataFrame(index=days)}
    rows = []
    def add(e, x, r, width=0.05, fill=100.0):
        m = np.linspace(r / (x - e + 1), r, x - e + 1)
        rows.append(dict(symbol="X", setup="E4_anchor_reclaim", universe="stock", entry_date=days[e], exit_date=days[x], r=r,
                         width=width, fill=fill, risk_ps=fill * width, reason="t", marks=m, mdates=days[e:x + 1].values))
    return days, frames, rows, add


def test_book_accounting_slots_daycap_cash_shares():
    days, frames, rows, add = _toy()
    add(1, 5, 2.0)
    add(1, 8, -1.0)
    add(2, 2, -1.0)                 # exits on its entry day
    add(3, 10, 1.0)
    add(6, 12, 0.5)
    T = pd.DataFrame(rows)
    bk = C.Book(T, frames)
    o = bk.run(risk=0.01, cash=100)
    assert o["taken"] == 5 and abs(o["curve"].iloc[-1] - 100_000 * (1 + 0.01 * 1.5)) < 60  # compounding: close to 1.5R x 1%
    o1 = bk.run(slots=1, risk=0.01, cash=100)
    assert o1["pos_max"] == 1 and o1["taken"] == 2            # (1,5), then (6,12) once it has exited
    o2 = bk.run(day_cap=1, risk=0.01, cash=100)
    assert o2["taken"] == 4                                     # the second entry on day 1 is skipped
    o3 = bk.run(risk=0.01, cash=0.25)                           # 1% risk / 5% stop = 20% notional: only one at a time
    assert o3["pos_max"] == 1
    T2 = T.assign(fill=1000.0, risk_ps=1000.0 * 0.05)            # one share risks $50
    o4 = C.Book(T2, frames).run(risk=0.001, cash=100, account=25_000)   # 0.1% of 25k = $25 < one share: all skipped
    assert o4["taken"] == 0
    o5 = C.Book(T2, frames).run(risk=0.001, cash=100, account=100_000)  # $100 -> 2 shares
    assert o5["taken"] == 5
    print("book ok: accounting, slots, day cap, cash rule, whole shares, same-day exits")


def test_bootstrap_and_regime():
    rng = np.random.default_rng(0)
    idx = pd.date_range("2001-01-31", periods=240, freq="ME")
    a = pd.Series(rng.normal(0.01, 0.02, 240), index=idx)
    p_same, _, _ = C.boot_sharpe(a, a, 500, 6, 7)
    p_up, lo, _ = C.boot_sharpe(a * 0.5 + 0.004, a, 500, 6, 7)      # same noise scaled down + a mean bump: higher Sharpe
    assert p_same == 0.0 and p_up > 0.99 and lo > 0
    d = pd.bdate_range("2005-01-03", periods=900)
    c = pd.Series(np.r_[np.linspace(100, 200, 600), np.linspace(200, 120, 300)], index=d)
    reg = C.regime_months(pd.DataFrame({"close": c}))
    cut = C.regime_months(pd.DataFrame({"close": c[c.index <= "2007-06-15"]}))
    common = cut.index[:-1]
    assert (reg.loc[common] == cut.loc[common]).all() and reg.iloc[-1] and not reg.iloc[0]
    print("bootstrap and regime months ok (no look-ahead)")


def test_lab_parity_helper():
    tmp = Path(tempfile.mkdtemp())
    (tmp / "reports" / "results").mkdir(parents=True)
    lab = pd.DataFrame(dict(symbol=["A", "A"], setup=C.SETUPS, exit_rule=C.EXIT, entry_date=["2020-01-02", "2020-02-03"], r=[1.0, -1.0]))
    lab.to_csv(tmp / "reports" / "results" / "trades_daily_etfs.csv.gz", index=False, compression="gzip")
    old = C.ROOT
    C.ROOT = tmp
    try:
        Td = pd.DataFrame(dict(symbol=["A", "A"], setup=C.SETUPS, entry_date=pd.to_datetime(["2020-01-02", "2020-03-02"]), r=[1.0, 0.5]))
        msg = C.lab_parity(Td)
        assert msg.startswith("1 of 2") and "1 of those" in msg, msg
    finally:
        C.ROOT = old
    print("Lab parity helper ok")


def test_lock():
    pr, lk = C.check_lock()
    print("construction lock ok:", lk[:16])


if __name__ == "__main__":
    test_prereg_and_sealed_rule()
    test_trades_equal_lab_and_marks()
    test_book_accounting_slots_daycap_cash_shares()
    test_bootstrap_and_regime()
    test_lab_parity_helper()
    test_lock()
    print("all construction tests passed")
