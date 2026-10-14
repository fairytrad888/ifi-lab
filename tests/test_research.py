"""Research tests: state machines on hand-built cases, look-ahead, bootstrap, lock and fixtures.
Run: python tests/test_research.py   (also works under pytest)"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from research import engine as E  # noqa: E402
from research.checks import check_no_lookahead  # noqa: E402
from research.common import Boot, load_prereg  # noqa: E402

NA = np.nan


def _arr(n, at: dict):
    a = np.full(n, NA)
    for k, v in at.items():
        a[k] = v
    return a


def test_rule3_machine():
    n = 60
    close = np.full(n, 10.5)
    # pivot highs (confirmation bars): 10 -> 10.0, 20 -> 12.0 (higher high: arms the top), 30 -> 11.0 (lower high)
    ph = _arr(n, {10: 10.0, 20: 12.0, 30: 11.0})
    pl = _arr(n, {25: 9.0})
    close[35] = 8.9  # close below the last pivot low after the lower high
    ev, st = E.rule3_events(ph, pl, close)
    assert list(np.flatnonzero(ev)) == [35], np.flatnonzero(ev)
    # no confirmation without a lower high
    ev2, _ = E.rule3_events(_arr(n, {10: 10.0, 20: 12.0}), pl, close)
    assert not ev2.any()
    # no confirmation without a preceding higher high (falling pivot highs only)
    ev3, _ = E.rule3_events(_arr(n, {10: 12.0, 20: 11.0, 30: 10.5}), pl, close)
    assert not ev3.any()
    # a higher high while the Trend line is NOT rising (a bounce inside a decline) does not arm a top
    ev5, _ = E.rule3_events(_arr(n, {10: 10.0, 20: 12.0, 30: 11.0}), pl, close, rising=np.zeros(n, bool))
    assert not ev5.any()
    # after a confirmation the machine re-arms only on a new higher high
    close2 = close.copy()
    close2[50] = 8.0
    ev4, _ = E.rule3_events(_arr(n, {10: 10.0, 20: 12.0, 30: 11.0, 40: 10.8}), pl, close2)
    assert list(np.flatnonzero(ev4)) == [35]
    print("rule 3 machine ok")


def test_floor_machine():
    n = 120
    low = np.full(n, 10.0)
    close = np.full(n, 10.2)
    atr = np.full(n, 0.2)
    rising = np.zeros(n, bool)
    f = lambda idx: np.isin(np.arange(n), idx)
    low[12] = 9.0
    # tier A: washout exit at 10, divergence at 30 (within 40), reclaim at 50
    ent, _ = E.floor_machine(low, close, atr, rising, f([10]), f([30]), f([]), f([50]), 40, 60, 0.25)
    assert ent == [dict(t=50, tier="A", lf=9.0, fstart=10, age=20)], ent
    # divergence 45 bars after the washout exit: outside the 40-bar window -> stays tier B
    ent, _ = E.floor_machine(low, close, atr, rising, f([10]), f([55]), f([]), f([60]), 40, 60, 0.25)
    assert ent[0]["tier"] == "B", ent
    # floor broken by a close below Lf - 0.25 ATR before the reclaim -> reclaim has no floor
    c2 = close.copy()
    c2[40] = 8.9
    ent, _ = E.floor_machine(low, c2, atr, rising, f([10]), f([30]), f([]), f([50]), 40, 60, 0.25)
    assert ent[0]["tier"] == "none", ent
    # a slow grind lower with no new floor evidence breaks the floor (Lf does not follow new lows)
    lg, cg = low.copy(), close.copy()
    for k in range(31, 50):
        lg[k] = 9.0 - 0.05 * (k - 30)
        cg[k] = lg[k] + 0.05
    ent, _ = E.floor_machine(lg, cg, atr, rising, f([10]), f([30]), f([]), f([50]), 40, 60, 0.25)
    assert ent[0]["tier"] == "none", ent
    # a new component during the grind (bar 32, before any break) extends the floor and lowers Lf to the
    # span's low (8.9); the bar-33 close (8.90) is then above Lf - 0.25 ATR, so the reclaim at 34 is tier A
    ent, _ = E.floor_machine(lg, cg, atr, rising, f([10, 32]), f([30]), f([]), f([34]), 40, 60, 0.25)
    assert ent[0]["tier"] == "A" and abs(ent[0]["lf"] - 8.9) < 1e-9, ent
    # without that component the same path breaks at bar 33 and a new tier B floor starts there
    ent, _ = E.floor_machine(lg, cg, atr, rising, f([10, 33]), f([30]), f([]), f([34]), 40, 60, 0.25)
    assert ent[0]["tier"] == "B" and ent[0]["fstart"] == 33, ent
    # floor expires 60 bars after its last component
    ent, _ = E.floor_machine(low, close, atr, rising, f([10]), f([]), f([]), f([75]), 40, 60, 0.25)
    assert ent[0]["tier"] == "none", ent
    ent, _ = E.floor_machine(low, close, atr, rising, f([10]), f([]), f([]), f([70]), 40, 60, 0.25)
    assert ent[0]["tier"] == "B", ent
    # components while the line is rising do not count
    ent, _ = E.floor_machine(low, close, atr, np.ones(n, bool), f([10]), f([30]), f([]), f([50]), 40, 60, 0.25)
    assert ent[0]["tier"] == "none", ent
    # late down-9 alone makes a tier B floor; a floor is consumed by its first reclaim
    ent, _ = E.floor_machine(low, close, atr, rising, f([]), f([]), f([20]), f([30, 35]), 40, 60, 0.25)
    assert [e["tier"] for e in ent] == ["B", "none"], ent
    print("floor machine ok")


def test_breakdown():
    bull = np.array([0, 1, 1, 0, 0, 0, 0, 1, 0, 0], bool)
    close = np.array([5, 5, 5, 4, 3, 2, 1, 5, 4, 3], float)
    lower = np.full(10, 4.5)
    bd, bsb = E.breakdown_bars(bull, close, lower)
    assert list(np.flatnonzero(bd)) == [3, 8], np.flatnonzero(bd)  # re-armed only by the bull bar at 7
    assert bsb[6] == 3 and np.isnan(bsb[2])
    # bull state persisting through and after the break: still only ONE breakdown for that bull run
    bull2 = np.array([0, 1, 1, 1, 1, 1, 1, 1, 0, 1], bool)
    close2 = np.array([5, 5, 4, 4, 5, 4, 3, 5, 5, 4], float)
    bd2, _ = E.breakdown_bars(bull2, close2, lower)
    assert list(np.flatnonzero(bd2)) == [2], np.flatnonzero(bd2)
    print("breakdown ok")


def test_no_lookahead():
    ok, msgs = check_no_lookahead()
    assert ok, msgs
    print("no look-ahead ok:", msgs[-1])


def test_bootstrap():
    rng = np.random.default_rng(1)
    d = pd.bdate_range("2000-01-03", periods=3000)
    a = rng.normal(0.01, 0.05, 3000)
    b = rng.normal(0.0, 0.05, 3000)
    r = Boot(2000, 7, 7).diff(a, d, b, d)
    assert r["lo_adj"] < r["lo"] < r["est"] < r["hi"] < r["hi_adj"]
    assert r["lo"] < 0.01 < r["hi"]
    m = Boot(2000, 7, 7).mean(a, d)
    assert m["lo"] < 0.01 < m["hi"]
    print("bootstrap ok")


def test_lock_and_fixtures():
    cfg, h = load_prereg(check_lock=True)
    fx = yaml.safe_load((ROOT / "research" / "fixtures_scan.yaml").read_text())
    names = set(cfg["universe"]["group_S"] + cfg["universe"]["group_O"])
    for kind in ("reclaim", "r3"):
        for f in fx[kind]:
            assert f["ratio"] in names, f
            assert pd.Timestamp(f["from"]) < pd.Timestamp(f["to"]), f
    for f in fx["parity"]:
        assert f["ratio"] in names and set(f) - {"ratio", "date"} <= {"close", "line", "anchor", "sma200"}, f
    for t in ("T1", "T2", "T3", "T4a", "T4b", "T5", "T6"):
        assert t in cfg["tests"] and t in cfg["relevant"] and t in cfg["gate"]["requires"] and t in cfg["decisions"]
    assert cfg["stats"]["k"] == 7
    print("lock and fixtures ok:", h[:16])


if __name__ == "__main__":
    test_rule3_machine()
    test_floor_machine()
    test_breakdown()
    test_bootstrap()
    test_lock_and_fixtures()
    test_no_lookahead()
    print("all research tests passed")
