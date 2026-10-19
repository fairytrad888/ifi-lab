"""Weekly scan tests (synthetic data only, no downloads). Run from the repo root: python weekscan/tests/test_weekscan.py"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[2]))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from weekscan import marketdata as md  # noqa: E402
from weekscan import scan  # noqa: E402
from weekscan.run import CFG, ROOT, out_dir, run  # noqa: E402
from weekscan.universe import map_etfs, parse_constituents  # noqa: E402

TMP = Path(tempfile.mkdtemp(prefix="weekscan_test_"))
import os  # noqa: E402
os.environ["WEEKSCAN_OFFLINE"] = "1"          # no earnings lookups in tests


def t_isolation():
    import re
    bad = []
    for f in ROOT.rglob("*.py"):
        for n, line in enumerate(f.read_text().splitlines(), 1):
            if re.match(r"^\s*(from|import)\s+(ifi|research|eyelab)(\.|\s|$)", line):
                bad.append(f"{f.name}:{n}")
    assert not bad, bad
    for line in (ROOT / "core" / "VENDOR.sha256").read_text().splitlines():
        sha, name = line.split()
        assert hashlib.sha256((ROOT / "core" / name).read_bytes()).hexdigest() == sha
    try:
        out_dir(str(ROOT.parent / "logs"))
        raise AssertionError("output inside the prior system accepted")
    except RuntimeError:
        pass
    print("isolation ok: no imports of ifi / research / eyelab; vendored IFI 2.0 code byte-identical; output path guarded")


def t_universe():
    html = """<table><tr><th>Symbol</th><th>Security</th><th>GICS Sector</th><th>GICS Sub-Industry</th></tr>
    <tr><td>BRK.B</td><td>Berkshire</td><td>Financials</td><td>Multi-Sector Holdings</td></tr>
    <tr><td>NVDA</td><td>Nvidia</td><td>Information Technology</td><td>Semiconductors</td></tr>
    <tr><td>DUK</td><td>Duke</td><td>Utilities</td><td>Electric Utilities</td></tr></table>"""
    u = map_etfs(parse_constituents(html, "sp500"), CFG)
    assert list(u["symbol"]) == ["BRK-B", "NVDA", "DUK"]
    assert list(u["group_etf"]) == ["XLF", "SMH", "XLU"], list(u["group_etf"])
    assert set(CFG["industry_etfs"].values()) <= {"SMH", "IGV", "XBI", "XPH", "IHI", "IHF", "KRE", "KBE", "KIE", "KCE",
                                                  "XOP", "XES", "XME", "GDX", "SIL", "ITB", "ITA", "IYT", "JETS", "PAVE",
                                                  "XRT", "PEJ", "FDN", "IYZ", "PBJ"}
    print("universe ok: Wikipedia table parsed, tickers in Yahoo form, sub-industry -> industry ETF, else sector ETF")


def t_weeks():
    idx = pd.bdate_range("2026-09-28", "2026-10-15")              # Mon .. Thu
    d = pd.DataFrame({"open": 1.0, "high": 1.1, "low": 0.9, "close": 1.0, "volume": 1.0}, index=idx)
    w_thu = md.weekly(d, datetime(2026, 10, 15, 21, tzinfo=timezone.utc))
    assert w_thu.index[-1] == pd.Timestamp("2026-10-09"), w_thu.index[-1]   # the partial week is dropped
    d2 = pd.DataFrame({"open": 1.0, "high": 1.1, "low": 0.9, "close": 1.0, "volume": 1.0},
                      index=pd.bdate_range("2026-09-28", "2026-10-16"))
    assert md.weekly(d2, datetime(2026, 10, 16, 23, tzinfo=timezone.utc)).index[-1] == pd.Timestamp("2026-10-09")
    assert md.weekly(d2, datetime(2026, 10, 17, 15, tzinfo=timezone.utc)).index[-1] == pd.Timestamp("2026-10-16")
    print("weeks ok: a week counts only from the Saturday after its Friday (no partial bars)")


def t_step():
    cfg = CFG
    W = [pd.Timestamp("2026-08-07") + pd.Timedelta(weeks=k) for k in range(12)]
    rec = lambda acc=False, low=10.0, close=11.0: {"acc": acc, "low": low, "close": close, "stage": 0,  # noqa: E731
                                                   "tag_ad_div": False, "tag_trigger": False}
    g = {"AAA": "XLK", "BBB": "XLE", "CCC": "XLU", "DDD": "XLK"}
    el = set(g)
    st = {}
    # week 0: AAA accumulates in a bullish group -> released now; BBB accumulates in a bearish group -> armed
    st, rel, _ = scan.step(st, W[0], {"AAA": rec(True), "BBB": rec(True), "CCC": rec(), "DDD": rec()}, g,
                           {"XLK": "bullish", "XLE": "bearish", "XLU": "neutral"}, el, cfg)
    assert [r["symbol"] for r in rel] == ["AAA"] and rel[0]["reason"].startswith("accumulation this week")
    # week 3: XLE turns basing -> BBB released, reason says the group turned
    st, rel, _ = scan.step(st, W[3], {"AAA": rec(), "BBB": rec(close=10.5), "CCC": rec(True), "DDD": rec()}, g,
                           {"XLK": "bullish", "XLE": "basing", "XLU": "bearish"}, el, cfg)
    assert [r["symbol"] for r in rel] == ["BBB"] and "turned basing, 3 weeks" in rel[0]["reason"], rel
    # week 4: CCC closes below its accumulation low -> disarmed, never released
    st, rel, ev = scan.step(st, W[4], {"AAA": rec(), "BBB": rec(), "CCC": rec(close=9.0), "DDD": rec()}, g,
                            {"XLK": "bullish", "XLE": "basing", "XLU": "basing"}, el, cfg)
    assert not rel and "CCC" not in st["armed"] and any("disarmed" in e["event"] for e in ev)
    # week 5: AAA accumulates again inside the 8-week block -> suppressed, no second alert
    st, rel, ev = scan.step(st, W[5], {"AAA": rec(True), "BBB": rec(), "CCC": rec(), "DDD": rec(True)}, g,
                            {"XLK": "bullish", "XLE": "neutral", "XLU": "neutral"}, el, cfg)
    assert [r["symbol"] for r in rel] == ["DDD"] and any(e["symbol"] == "AAA" and "suppressed" in e["event"] for e in ev)
    # expiry: an armed stock whose group never qualifies is dropped after 8 weeks
    st2, _, _ = scan.step({}, W[0], {"BBB": rec(True)}, g, {"XLE": "bearish"}, el, cfg)
    st2, _, ev = scan.step(st2, W[9], {"BBB": rec()}, g, {"XLE": "bearish"}, el, cfg)
    assert "BBB" not in st2["armed"] and any("expired" in e["event"] for e in ev)
    # illiquid stocks never arm
    st3, rel, _ = scan.step({}, W[0], {"AAA": rec(True)}, g, {"XLK": "bullish"}, set(), cfg)
    assert not rel and not st3["armed"]
    print("arm and release ok: same-week release, later release when the group turns, disarm on a close below the low, "
          "8-week expiry, 8-week repeat block, liquidity gate")


def _walk(n, seed, drift=0.0003, vol=0.018, start=50.0):
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range(end="2026-10-16", periods=n)
    c = start * np.exp(np.cumsum(rng.normal(drift, vol, n)))
    o = np.r_[c[0], c[:-1]]
    return pd.DataFrame({"open": o, "high": np.maximum(o, c) * 1.008, "low": np.minimum(o, c) * 0.992, "close": c,
                         "volume": rng.integers(2e6, 8e6, n).astype(float)}, index=idx)


def t_end_to_end():
    syms = [f"S{k:02d}" for k in range(30)]
    sectors = ["Information Technology", "Energy", "Utilities"]
    u = pd.DataFrame({"symbol": syms, "name": syms, "sector": [sectors[k % 3] for k in range(30)],
                      "sub_industry": ["Semiconductors" if k % 6 == 0 else "Other" for k in range(30)], "index": "sp500"})
    daily = {s: _walk(1800, k) for k, s in enumerate(syms)}
    for k, e in enumerate(sorted(set(CFG["sector_etfs"].values()) | set(CFG["industry_etfs"].values()))):
        daily[e] = _walk(1800, 100 + k, vol=0.012)
    daily["SPY"] = _walk(1800, 999, vol=0.01, start=400)
    out = Path(os.environ.get("WEEKSCAN_KEEP", TMP / "e2e"))
    out.mkdir()
    now = datetime(2026, 10, 17, 15, tzinfo=timezone.utc)
    r1 = run(out, push=False, now=now, universe=u, daily=daily)
    assert r1["week"] == "2026-10-16" and (out / "LATEST.md").exists() and (out / "state.json").exists()
    assert any("first run" in n for n in r1["notes"])
    g = pd.read_csv(out / "weeks" / "2026-10-16" / "groups.csv")
    assert set(g["state"].dropna()) <= {"bullish", "basing", "neutral", "bearish"} and len(g) >= 11
    r2 = run(out, push=False, now=now, universe=u, daily=daily)
    assert "already processed" in r2["status"]
    log = pd.read_csv(out / "alerts_log.csv") if (out / "alerts_log.csv").exists() else pd.DataFrame()
    st = json.loads((out / "state.json").read_text())
    print(f"end to end ok: {len(syms)} synthetic stocks, {len(g)} groups ({int(g['state'].isin(['bullish', 'basing']).sum())} "
          f"bullish/basing), released this week {r1['released']}, seeded+current log rows {len(log)}, armed {len(st['armed'])}; "
          f"a second run for the same week pushes nothing")


if __name__ == "__main__":
    try:
        for t in (t_isolation, t_universe, t_weeks, t_step, t_end_to_end):
            t()
        print("all weekscan tests passed")
    finally:
        shutil.rmtree(TMP, ignore_errors=True)
