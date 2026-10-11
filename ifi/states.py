"""Per-bar reading of the IFI set: the 0-5 checklist, stage, volume tag, relative strength, RRG quadrant.

All rules are the ones written down before the October sweep (see IFI_2.0 docs); nothing here is fitted.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import pine as p
from .indicators import compute_all


def _bars_since(mask: pd.Series) -> pd.Series:
    out = np.full(len(mask), np.nan)
    last = None
    m = mask.to_numpy(dtype=bool)
    for i in range(len(m)):
        if m[i]:
            last = i
        if last is not None:
            out[i] = i - last
    return pd.Series(out, index=mask.index)


def session_rvol(df: pd.DataFrame, n: int = 20) -> pd.Series:
    """Volume vs the average of the same session slot (4H) or of prior days (daily)."""
    if "slot" in df:
        return df.groupby("slot")["volume"].transform(lambda v: v / v.shift(1).rolling(n, min_periods=5).mean())
    return df["volume"] / df["volume"].shift(1).rolling(n, min_periods=5).mean()


def read(df: pd.DataFrame, bench: pd.DataFrame | None = None) -> pd.DataFrame:
    x = compute_all(df)
    c = x["close"]

    # check 1: latest confirmed swing low (3/3) is higher than the previous one
    pl = p.pivot_low(x["low"], 3, 3)
    last_pl = pl.ffill()
    prev_pl = pl.dropna().shift(1).reindex(x.index).ffill()
    x["chk1_higher_low"] = (last_pl > prev_pl).fillna(False)

    # check 2: close above the active Trend anchor
    x["chk2_above_anchor"] = (c > x["tr_anchor"]).fillna(False)

    # check 3: a bullish trigger in the last 20 bars that held (no close below its bar's low), or WT1 above channel
    trig = x["sig_trig_bull"]
    bs_trig = _bars_since(trig)
    trig_low = x["low"].where(trig).ffill()
    # lowest close since the last trigger
    mc = np.full(len(x), np.nan)
    cur = np.nan
    tv, cv = trig.to_numpy(), c.to_numpy()
    for i in range(len(x)):
        if tv[i]:
            cur = cv[i]
        elif not np.isnan(cur):
            cur = min(cur, cv[i])
        mc[i] = cur
    held = (bs_trig <= 20) & (pd.Series(mc, index=x.index) >= trig_low)
    x["chk3_signals"] = (held | (x["sig_wt1"] > x["sig_channel"])).fillna(False)

    # check 4: RSI held 40 after the last push above 60 (within 30 bars), or Matrix bullish divergence within 10 bars
    rsi = x["mx_rsi"]
    bs60 = _bars_since(rsi > 60)
    mr = np.full(len(x), np.nan)
    cur = np.nan
    rv, pv = rsi.to_numpy(), (rsi > 60).to_numpy()
    for i in range(len(x)):
        if pv[i]:
            cur = rv[i]
        elif not np.isnan(cur):
            cur = min(cur, rv[i])
        mr[i] = cur
    hold40 = (bs60 <= 30) & (pd.Series(mr, index=x.index) >= 40)
    div = _bars_since(x["mx_strong_bull"]) <= 10
    x["chk4_rsi"] = (hold40 | div).fillna(False)

    # check 5: a washout happened in the last 60 bars and none in the last 10
    bs_wash = _bars_since(x["ad_washout"])
    x["chk5_washout_done"] = ((bs_wash >= 10) & (bs_wash <= 60)).fillna(False)

    checks = ["chk1_higher_low", "chk2_above_anchor", "chk3_signals", "chk4_rsi", "chk5_washout_done"]
    x["score"] = x[checks].sum(axis=1)

    # stage ladder
    nine_dn = _bars_since(x["tr_nine"] == -1) <= 15
    wash_exit = _bars_since(x["ad_washout_exit"]) <= 15
    stage1 = (nine_dn | wash_exit) & x["chk1_higher_low"]
    stage2 = (c > x["tr_line"]) & x["tr_line_rising"]
    stage3 = stage2 & x["chk2_above_anchor"]
    lower_low = (last_pl < prev_pl).fillna(False)
    breakdown = (c < x["tr_line"]) & ~x["tr_line_rising"] & lower_low
    x["stage"] = np.select([stage3, stage2, stage1, breakdown], [3, 2, 1, -1], 0)

    # slow trend reference (standard: above a rising 200-bar average). The IFI Trend line is too fast for this
    # role: it is always falling when WT1 is below -50, so it can never label an oversold trigger "with trend".
    sma200 = p.sma(c, 200)
    x["trend200_up"] = ((c > sma200) & (sma200 > sma200.shift(20))).fillna(False)

    # volume and distances
    x["rvol"] = session_rvol(df)
    x["dist_anchor_atr"] = (c - x["tr_anchor"]) / x["atr"]
    x["dist_line_atr"] = (c - x["tr_line"]) / x["atr"]
    x["swing_low"] = last_pl
    x["stop_suggest"] = x["low"].rolling(5).min() - 0.5 * x["atr"]

    # relative strength vs benchmark + RRG-style quadrant
    if bench is not None:
        b = bench["close"].reindex(x.index).ffill()
        rs = 100 * c / b
        rs_ratio = 100 * rs / p.ema(rs, 40)
        rs_mom = 100 * rs_ratio / p.ema(rs_ratio, 10)
        x["rs"], x["rs_ratio"], x["rs_mom"] = rs, rs_ratio, rs_mom
        x["rrg"] = np.select(
            [(rs_ratio >= 100) & (rs_mom >= 100), (rs_ratio >= 100) & (rs_mom < 100),
             (rs_ratio < 100) & (rs_mom < 100), (rs_ratio < 100) & (rs_mom >= 100)],
            ["Leading", "Weakening", "Lagging", "Improving"], "")
    return x


EVENT_COLS = {
    "ad_washout_exit": "Washout exit",
    "ad_bull_div": "A&D bull divergence",
    "ad_bear_div": "A&D bear divergence",
    "sig_trig_bull": "Bull trigger",
    "sig_trig_bear": "Bear trigger",
    "mx_strong_bull": "Matrix bull divergence",
    "mx_strong_bear": "Matrix bear divergence",
}


def events_on_bar(x: pd.DataFrame, i: int = -1) -> list[str]:
    """Human-readable events on bar i (default: last bar)."""
    row = x.iloc[i]
    prev = x.iloc[i - 1] if len(x) > 1 else row
    ev = []
    for col, name in EVENT_COLS.items():
        if bool(row.get(col, False)):
            if col == "ad_washout_exit":
                name += f" #{int(row['ad_washout_no'])}"
            if col == "sig_trig_bull":
                name += f" (streak {int(row['sig_bull_streak'])}, {'with' if row['trend200_up'] else 'counter'}-trend)"
            if col == "sig_trig_bear":
                name += f" (streak {int(row['sig_bear_streak'])})"
            ev.append(name)
    if row["tr_nine"] == 1:
        ev.append("Up 9 complete")
    if row["tr_nine"] == -1:
        ev.append("Down 9 complete")
    if row["stage"] != prev["stage"]:
        ev.append(f"Stage {int(prev['stage'])} -> {int(row['stage'])}")
    if bool(row["tr_line_rising"]) != bool(prev["tr_line_rising"]):
        ev.append("Trend line turned " + ("up" if row["tr_line_rising"] else "down"))
    if bool(row["chk2_above_anchor"]) and not bool(prev["chk2_above_anchor"]):
        ev.append("Anchor reclaimed")
    if not bool(row["chk2_above_anchor"]) and bool(prev["chk2_above_anchor"]):
        ev.append("Anchor lost")
    return ev
