"""Ratio-flip study family (R001-R004): bullish confluence on a downtrending ratio (ETF / SPY).

Ratio      symbol / SPY daily, TradingView-style bars (O1/O2, H1/H2, L1/L2, C1/C2, highs and lows clamped);
           no volume, so Trend anchors are time-weighted, as on TradingView.
Signals    S1 Signals bull trigger (△n)        sig_trig_bull (n = sig_bull_streak)
           S2 A&D accumulation bar (green)     ad_washout_exit
           S3 A&D bullish divergence (green ▲) ad_bull_div
           S4 Matrix bullish divergence (◆)    mx_strong_bull
Context    the ratio is in a downtrend: Trend line falling and stage <= 1 on the event bar
Event      tier k: the bar on which the number of distinct signal types seen in the last 10 bars first reaches k
           (k = 2 and k = 3), in context, with no event of the same tier in the 10 bars before
Outcomes   O1 up9   an up-9 completes within 20 bars before any close below the event low (lowest low of the
                    10-bar window)                                                     <- primary
           O2 flip  a close above the key level (last confirmed 5/5 pivot high before the event) before a close
                    below the event low, within 60 bars
           O3       ratio and numerator: +k ATR before -1 ATR (k = 1, 2, 3) within 40 bars from the next open
Conditions C1..C7 (below); combos K1..K3 are separate pre-registered tests (R002-R004).
Cut points C4 and C7 were fixed on Oct 18, 2026 from the distribution of events on the dev ratios (13 sector and
industry ETFs vs SPY, 2000-2026), before any outcome of any event was computed.
"""
from __future__ import annotations

import csv

import numpy as np
import pandas as pd

from ..core import pine as p
from ..guard import ROOT

WINDOW = 10
H_UP9, H_FLIP, H_LADDER = 20, 60, 40
MAX_H = max(H_UP9, H_FLIP, H_LADDER) + 1
CLASSES = ("sector", "industry", "country")

# fixed from dev-pool event distributions (outcome-blind), see module docstring
ANGLE_CUT = 2.54    # C4: WT1 - WT2 at the event bar, top tercile (67th percentile of 1,375 dev events)
ROOM_CUT = 4.88     # C7: (key level - close) / ATR, at or below the median (1,371 dev events with a key level above)

COND_TEXT = {
    "C1": "at least 2 completed down-9s since the ratio was last in stage 3",
    "C2": "a down-9 completed within the last 10 bars",
    "C3": "a Signals trigger #1 (first of its oversold visit) in the window",
    "C4": "angle: WT1 - WT2 at the event bar in the top third",
    "C5": "accumulation cluster: at least 2 A&D washout exits within 15 bars",
    "C6": "depth: lowest WT1 in the window at or below -63",
    "C7": "room: key level within the median ATR distance above the close",
}
COMBOS = {
    "K1": ("C1", "C3", "C4"),       # >=2 down-9 cycles + trigger #1 + steep angle
    "K2": ("C2", "C5", "S1"),       # fresh 9 + accumulation cluster + a trigger in the window
    "K3": ("C1", "C6", "C7"),       # >=2 cycles + deep WT1 + room to the key level
}


def etf_universe(pool_syms: list[str]) -> list[str]:
    cls = {r["symbol"]: r["class"] for r in csv.DictReader((ROOT / "pools" / "etf_classes.csv").open())}
    return [s for s in pool_syms if cls.get(s) in CLASSES]


def ratio_bars(a: pd.DataFrame, b: pd.DataFrame) -> pd.DataFrame:
    j = a.index.intersection(b.index)
    a, b = a.loc[j], b.loc[j]
    r = pd.DataFrame({k: a[k] / b[k] for k in ("open", "high", "low", "close")}, index=j)
    r["high"] = r[["open", "high", "low", "close"]].max(axis=1)
    r["low"] = r[["open", "high", "low", "close"]].min(axis=1)
    r["volume"] = 0.0
    return r.replace([np.inf, -np.inf], np.nan).dropna()


def _since(mask: np.ndarray) -> np.ndarray:
    out = np.full(len(mask), np.inf)
    last = None
    for i, m in enumerate(mask):
        if m:
            last = i
        if last is not None:
            out[i] = i - last
    return out


def annotate(x: pd.DataFrame) -> pd.DataFrame:
    """Signal types, context, events, conditions and the key level: all known at the close of each bar."""
    x = x.copy()
    types = pd.DataFrame({"S1": x["sig_trig_bull"], "S2": x["ad_washout_exit"], "S3": x["ad_bull_div"],
                          "S4": x["mx_strong_bull"]}).fillna(False).astype(int)
    seen = types.rolling(WINDOW, min_periods=1).max()
    n = seen.sum(axis=1)
    x["n_types"] = n
    for c in types:
        x[f"seen_{c}"] = seen[c].astype(bool)
    x["context"] = (~x["tr_line_rising"].astype(bool)) & (x["stage"] <= 1)
    for k in (2, 3):
        first = (n >= k) & (n.shift(1, fill_value=0) < k) & x["context"]
        ev = first.to_numpy().copy()
        last = -10_000
        for i in np.flatnonzero(ev):
            if i - last <= WINDOW:
                ev[i] = False
            else:
                last = i
        x[f"e{k}"] = ev
    x["event_low"] = x["low"].rolling(WINDOW, min_periods=1).min()
    x["key_level"] = p.pivot_high(x["high"], 5, 5).ffill()
    # conditions
    st3 = (x["stage"] == 3).to_numpy()
    d9 = (x["tr_nine"] == -1).to_numpy()
    cyc, c = np.zeros(len(x), int), 0
    for i in range(len(x)):
        if st3[i]:
            c = 0
        if d9[i]:
            c += 1
        cyc[i] = c
    x["down9_cycles"] = cyc
    x["C1"] = cyc >= 2
    x["C2"] = _since(d9) <= WINDOW
    t1 = (x["sig_trig_bull"].astype(bool) & (x["sig_bull_streak"] == 1)).astype(int)
    x["C3"] = t1.rolling(WINDOW, min_periods=1).max().astype(bool)
    x["angle"] = x["sig_wt1"] - x["sig_wt2"]
    x["C4"] = x["angle"] >= (ANGLE_CUT if ANGLE_CUT is not None else np.inf)
    x["C5"] = x["ad_washout_exit"].astype(int).rolling(15, min_periods=1).sum() >= 2
    x["wt1_min"] = x["sig_wt1"].rolling(WINDOW, min_periods=1).min()
    x["C6"] = x["wt1_min"] <= -63
    x["room"] = (x["key_level"] - x["close"]) / x["atr"]
    x["C7"] = (x["room"] > 0) & (x["room"] <= (ROOM_CUT if ROOM_CUT is not None else -np.inf))
    x["S1"] = x["seen_S1"]
    for k, parts in COMBOS.items():
        x[k] = np.logical_and.reduce([x[c].astype(bool).to_numpy() for c in parts])
    return x


def atr(df: pd.DataFrame, n: int = 14) -> pd.Series:
    pc = df["close"].shift(1)
    tr = pd.concat([df["high"] - df["low"], (df["high"] - pc).abs(), (df["low"] - pc).abs()], axis=1).max(axis=1)
    return tr.rolling(n, min_periods=n).mean()


def _ladder(o, h, l, j, u, n_bars, k):
    if not (np.isfinite(u) and u > 0):
        return np.nan
    entry = o[j]
    hs, ls = h[j:j + n_bars], l[j:j + n_bars]
    win, loss = hs >= entry + k * u, ls <= entry - u
    wi = int(np.argmax(win)) if win.any() else n_bars
    li = int(np.argmax(loss)) if loss.any() else n_bars
    return 1.0 if wi < li else 0.0


def outcomes(x: pd.DataFrame, i: int, num: dict | None = None) -> dict | None:
    """Outcomes of an event (or null) on bar i. None when fewer than MAX_H bars follow."""
    n = len(x)
    if i + MAX_H >= n or i < 250:
        return None
    c, nine = x["close"].to_numpy(), x["tr_nine"].to_numpy()
    lo = float(x["event_low"].iloc[i])
    out = {}
    r = 0.0
    for t in range(i + 1, i + 1 + H_UP9):
        if c[t] < lo:
            break
        if nine[t] == 1:
            r = 1.0
            break
    out["o1_up9"] = r
    K = float(x["key_level"].iloc[i])
    if np.isfinite(K) and K > c[i]:
        r = 0.0
        for t in range(i + 1, i + 1 + H_FLIP):
            if c[t] < lo:
                break
            if c[t] > K:
                r = 1.0
                break
        out["o2_flip"] = r
    else:
        out["o2_flip"] = np.nan
    o, h, l = (x[k].to_numpy() for k in ("open", "high", "low"))
    u = float(x["atr"].iloc[i])
    for k in (1, 2, 3):
        out[f"o3_ratio_{k}"] = _ladder(o, h, l, i + 1, u, H_LADDER, k)
    if num is not None:
        j = num["pos"].get(x.index[i])
        for k in (1, 2, 3):
            out[f"o3_symbol_{k}"] = (_ladder(num["o"], num["h"], num["l"], j + 1, num["u"][j], H_LADDER, k)
                                     if j is not None and j + H_LADDER < len(num["o"]) else np.nan)
    return out


OUTCOMES = ["o1_up9", "o2_flip"] + [f"o3_ratio_{k}" for k in (1, 2, 3)] + [f"o3_symbol_{k}" for k in (1, 2, 3)]
