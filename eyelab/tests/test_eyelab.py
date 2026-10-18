"""Eye Lab tests. Run from the repo root: python eyelab/tests/test_eyelab.py
Synthetic data only (no downloads). Uses a temporary EYELAB_OUT and removes everything it creates."""
from __future__ import annotations

import hashlib
import os
import shutil
import sys
import tempfile
import types
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[2]))
TMP = Path(tempfile.mkdtemp(prefix="eyelab_test_"))
os.environ["EYELAB_OUT"] = str(TMP)

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from eyelab import guard, selftest  # noqa: E402
from eyelab.data import load, pool_symbols, write_snapshot  # noqa: E402

ROOT = guard.ROOT
TEST_RULE = ROOT / "rules" / "T_pipeline.py"


def synth(n=1500, seed=0):
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range("2012-01-02", periods=n)
    c = 50 * np.exp(np.cumsum(rng.normal(0.0003, 0.015, n)))
    o = np.r_[c[0], c[:-1]]
    return pd.DataFrame({"open": o, "high": np.maximum(o, c) * 1.006, "low": np.minimum(o, c) * 0.994, "close": c,
                         "volume": rng.integers(1e5, 1e6, n).astype(float)}, index=idx)


def t_isolation():
    bad = guard.prior_imports()
    assert not bad, f"Eye Lab imports the prior system: {bad}"
    try:
        os.environ["EYELAB_OUT"] = str(guard.REPO / "logs")
        guard.out_dir()
        raise AssertionError("out_dir accepted a path inside the prior system")
    except RuntimeError:
        pass
    finally:
        os.environ["EYELAB_OUT"] = str(TMP)
    print("isolation ok: no prior imports; output outside eyelab/_out inside the repo is refused")


def t_vendor():
    for line in (ROOT / "core" / "VENDOR.sha256").read_text().splitlines():
        sha, name = line.split()
        assert hashlib.sha256((ROOT / "core" / name).read_bytes()).hexdigest() == sha, f"vendored {name} changed"
    print("vendored IFI 2.0 indicator code byte-identical to the freeze")


def t_pools():
    d, a, b = (set(pool_symbols(p)) for p in ("dev", "A", "B"))
    assert len(d) == 78 and not (d & a) and not (d & b) and not (a & b), "pools must be disjoint"
    print(f"pools ok: dev {len(d)}, A {len(a)}, B {len(b)}, disjoint")


def t_access_and_pinning():
    a_sym, b_sym, d_sym = pool_symbols("A")[0], pool_symbols("B")[0], pool_symbols("dev")[0]
    write_snapshot("A", "D", {a_sym: synth()}, [], "synthetic")
    write_snapshot("B", "D", {b_sym: synth(seed=1)}, [], "synthetic")
    write_snapshot("dev", "D", {d_sym: synth(seed=2)}, [], "synthetic")
    assert load("A", a_sym, "D", "discovery") is not None
    for args in (("dev", d_sym, "D", "discovery"), ("A", a_sym, "D", "confirm"), ("B", b_sym, "D", "discovery")):
        try:
            load(*args)
            raise AssertionError(f"access not refused: {args}")
        except PermissionError:
            pass
    try:
        load("B", b_sym, "D", "confirm")
        raise AssertionError("sealed pool B read outside confirm.run")
    except PermissionError:
        pass
    ex = load("dev", d_sym, "D", "example", until=pd.Timestamp("2014-03-03"), extra_bars=2)
    assert ex.index[-1] <= pd.Timestamp("2014-03-06"), "example frame shows bars after the example"
    try:
        load("dev", d_sym, "D", "example")
        raise AssertionError("example frame without `until` accepted")
    except PermissionError:
        pass
    f = TMP / "data" / "A" / "D" / f"{a_sym}.csv.gz"
    raw = f.read_bytes()
    f.write_bytes(raw[:-1] + bytes([raw[-1] ^ 1]))
    try:
        load("A", a_sym, "D", "discovery")
        raise AssertionError("tampered snapshot accepted")
    except RuntimeError:
        pass
    f.write_bytes(raw)
    print("data access ok: dev never graded, A discovery only, B sealed, example frames stop at the example, "
          "snapshots pinned by sha256")


def t_engine():
    r = selftest.run_all()
    for k in ("geometry", "blind", "power", "null"):
        assert r[k]["ok"], f"selftest {k} failed: {r[k]}"
    print(f"engine ok: geometry, blind refusal, power (adv {r['power']['adv']:+.3f}, low {r['power']['lo']:+.3f}), "
          f"null calibration (pass rate {r['null']['pass_rate']:.0%} over {r['null']['worlds']} random worlds, "
          f"mean adv {r['null']['mean_adv']:+.4f})")


def t_look_ahead():
    from eyelab.features import enrich
    from eyelab.registry import look_ahead_ok
    x = enrich(synth(900, seed=5))
    honest = types.SimpleNamespace(signal=lambda x: (x["close"] > x["tr_line"]) & x["tr_line_rising"])
    cheat = types.SimpleNamespace(signal=lambda x: x["close"].shift(-1) > x["close"] * 1.01)
    assert look_ahead_ok(honest, x), "honest rule flagged"
    assert not look_ahead_ok(cheat, x), "look-ahead rule not caught"
    print("look-ahead test ok: honest rule passes, a rule peeking one bar ahead is caught")


def t_pipeline():
    from eyelab import confirm, discovery, fidelity, ledger
    from eyelab.data import write_snapshot as ws
    syms_a, syms_b, syms_d = pool_symbols("A")[:8], pool_symbols("B")[:8], pool_symbols("dev")[:3]
    ws("bench", "D", {"SPY": synth(seed=99)}, [], "synthetic")
    ws("A", "D", {s: synth(seed=10 + k) for k, s in enumerate(syms_a)}, [], "synthetic")
    ws("B", "D", {s: synth(seed=40 + k) for k, s in enumerate(syms_b)}, [], "synthetic")
    ws("dev", "D", {s: synth(seed=70 + k) for k, s in enumerate(syms_d)}, [], "synthetic")
    TEST_RULE.write_text('SPEC = {"id": "T_pipeline", "version": 1, "name": "test", "eye_description": "test", '
                         '"timeframe": "D", "direction": "long", "status": "draft"}\n'
                         'def signal(x):\n    a = x["close"] > x["sma50"]\n    return a & ~a.shift(1, fill_value=True)\n')
    try:
        meta = fidelity.run("T_pipeline")
        assert not meta["gate_passed"] and (TMP / "fidelity" / "T_pipeline" / "v1" / "blind" / "KEY.csv").exists()
        try:
            discovery.run("T_pipeline")
            raise AssertionError("discovery ran without the fidelity gate")
        except PermissionError:
            pass
        d = discovery.run("T_pipeline", force=True)
        assert d["signals"] > 20, d
        assert "FORCED" in ledger.rows()[-1]["note"]
        try:
            discovery.run("R000_demo", force=True)
            raise AssertionError("demo rule graded")
        except PermissionError:
            pass
        lk = confirm.lock("T_pipeline")
        try:
            confirm.lock("T_pipeline")
            raise AssertionError("re-lock accepted")
        except PermissionError:
            pass
        c = confirm.run("T_pipeline")
        assert c["verdict"] in ("CONFIRMED", "NOT CONFIRMED") and c["signals"] > 20
        try:
            confirm.run("T_pipeline")
            raise AssertionError("second opening of pool B accepted")
        except PermissionError:
            pass
        TEST_RULE.write_text(TEST_RULE.read_text() + "# changed\n")
        try:
            confirm.run("T_pipeline")
            raise AssertionError("confirm ran on a rule changed after its lock")
        except PermissionError:
            pass
        stages = [r["stage"] for r in ledger.rows()]
        assert stages.count("discovery") == 1 and "lock" in stages and "confirm" in stages
    finally:
        TEST_RULE.unlink(missing_ok=True)
        for p in (ROOT / "rules" / "__pycache__").glob("T_pipeline*"):
            p.unlink()
    print(f"pipeline ok: fidelity (blind) -> discovery gated -> lock {lk['lock_sha'][:12]} -> confirm once "
          f"({c['signals']} signals, {c['verdict']}); re-lock, second opening and post-lock edits refused")


def t_study():
    """Ratio-flip study (R002) end to end on synthetic ETFs: fidelity -> discovery -> lock -> confirm once."""
    from eyelab import confirm, discovery, fidelity
    from eyelab.data import write_snapshot as ws
    from eyelab.studies import ratio_flip as RF
    dev = RF.etf_universe(pool_symbols("dev"))[:3]
    a_ = RF.etf_universe(pool_symbols("A"))[:5]
    b_ = RF.etf_universe(pool_symbols("B"))[:5]
    assert len(dev) == 3 and len(a_) == 5 and len(b_) == 5
    ws("bench", "D", {"SPY": synth(2600, seed=99)}, [], "synthetic")
    for pool, syms, off in (("dev", dev, 200), ("A", a_, 300), ("B", b_, 400)):
        ws(pool, "D", {s: synth(2600, seed=off + k) for k, s in enumerate(syms)}, [], "synthetic")
    rid = "R002_k1_cycles_trig1_angle"
    m = fidelity.run(rid)
    assert m["look_ahead_ok"] and not m["gate_passed"] and m["events_dev"] >= 0, m
    d = discovery.run(rid, force=True)
    assert d["events"] > 50, d
    lk = confirm.lock(rid)
    assert lk["hypotheses"] == [["K1", 2]], lk
    c = confirm.run(rid)
    assert c["verdict"] in ("CONFIRMED", "PARTLY CONFIRMED", "NOT CONFIRMED") and c["events"] > 50
    try:
        confirm.run(rid)
        raise AssertionError("second opening accepted")
    except PermissionError:
        pass
    print(f"ratio-flip study ok: look-ahead clean on events and conditions; discovery {d['events']} events on "
          f"{len(a_)} synthetic ETF ratios; lock carries {lk['hypotheses']}; confirmation {c['events']} events, {c['verdict']}")


def t_lift_calibration():
    """Condition-lift test: about 5% false positives with no effect; a planted +12 pt lift is found."""
    from eyelab.study import lift_boot
    rng = np.random.default_rng(3)
    months = np.array([f"m{k}" for k in rng.integers(0, 240, 1500)])
    fp = 0
    for k in range(60):
        c = rng.random(1500) < 0.3
        v = (rng.random(1500) < 0.4).astype(float)
        fp += lift_boot(v, c, months, B=500, seed=k)["p"] < 0.05
    c = rng.random(1500) < 0.3
    v = (rng.random(1500) < 0.4 + 0.12 * c).astype(float)
    pw = lift_boot(v, c, months, B=1000)
    assert fp / 60 <= 0.12 and pw["p"] < 0.05, (fp, pw)
    print(f"lift test ok: false-positive rate {fp / 60:.0%} over 60 null worlds; planted +12 pts found (p {pw['p']:.3f})")


if __name__ == "__main__":
    try:
        for t in (t_isolation, t_vendor, t_pools, t_access_and_pinning, t_engine, t_look_ahead, t_pipeline, t_lift_calibration, t_study):
            t()
        print("all eyelab tests passed")
    finally:
        shutil.rmtree(TMP, ignore_errors=True)
