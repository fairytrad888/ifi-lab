"""Template for a rule built from an eye-level signal. Copy to eyelab/rules/R<NNN>_<short_name>.py.

Write the rule so it reads like the eye description. Use only bars up to t (no .shift(-k), no centred windows):
the look-ahead test deletes future bars and fails the rule if any signal or unit changes.

Columns available in x (one row per bar; the IFI 2.0 reading, as on your TradingView charts):
  price      open high low close volume atr sma50 sma200 hh20 ll20 bar
  Trend      tr_line tr_line_rising tr_anchor tr_anchor_is_support tr_state_up tr_count tr_count_dir tr_nine
             tr_count_failed
  A&D        ad_flow ad_washout ad_washout_exit ad_washout_no ad_bull_div ad_bear_div ad_range_pos100
  Signals    sig_wt1 sig_wt2 sig_channel sig_trig_bull sig_trig_bear sig_bull_streak sig_bear_streak sig_zone
  Matrix     mx_rsi mx_kdj_j mx_tsi mx_bull_votes mx_bear_votes mx_strong_bull mx_strong_bear
  Reading    chk1_higher_low chk2_above_anchor chk3_signals chk4_rsi chk5_washout_done score stage trend200_up
             rvol dist_anchor_atr dist_line_atr swing_low stop_suggest
  Relative   rs rs_ratio rs_mom rrg (vs SPY) spy_close spy_trend_up
Bump "version" every time the logic changes: each version is a separate, counted variant.
"""

SPEC = {
    "id": "R001_example",               # must equal the file name
    "version": 1,
    "name": "Short name",
    "eye_description": "Your words, as you said them: what you see on the chart that makes this a signal.",
    "timeframe": "D",                   # D, W or H4 (H4 history is about 2 years)
    "direction": "long",                # long or short
    "status": "draft",                  # draft -> fidelity_passed -> discovery -> locked -> confirmed / rejected
    "source": "screenshot / examples / verbal",
    "invalidation": "What would make you say the signal failed (used to define the 1R unit).",
}


def signal(x):
    """True on the bar the signal is complete (known at its close)."""
    return (x["close"] > x["tr_anchor"]) & (x["close"].shift(1) <= x["tr_anchor"].shift(1))


def unit(x):
    """Optional: the 1R distance in price at bar t, from your invalidation level. Default: 1 x ATR(14)."""
    return (x["close"] - x["low"].rolling(5).min() + 0.25 * x["atr"]).clip(lower=0.5 * x["atr"])
