# E4 exit test v1 (pre-registered)

_Run 2026-10-15 00:40 UTC · commit `17c15dd3ed` · lock `c52713bc9d3e2f85` · snapshot cutoff 2026-10-14 (manifest `a3609f3fec828066`) · 17 ETFs, 61 stocks · Bonferroni k = 5 · 5,000 draws; CI = widest of [6, 12]-month blocks · Python 3.12.15, pandas 3.0.6, numpy 2.5.4, scipy 1.18.1_

## Validity

| check | result |
|---|---|
| Lock (prereg, exit code, engine, ifi modules) | ok `c52713bc9d3e2f85` |
| Engine look-ahead (truncation) | ok: identical events at 3 cut points on 2 synthetic markets (1093 events in the last full run) |
| Synthetic null (martingale prices) | ok: X8 FAIL, X9 FAIL, X10 FAIL, X11 FAIL, X12 FAIL |
| Synthetic power (persistent trends) | ok: X8 FAIL, X9 OPPOSITE, X10 PASS, X11 PASS, X12 FAIL (required: X10 PASS) |
| Frozen snapshot | cutoff 2026-10-14 · 78 symbols · missing: none |
| Dividend data (Adj Close) | present for all 78 symbols |
| Lab parity (X3 vs ifi/backtest.py X3_target3R) | ok: 912 Lab X3 trades reproduced exactly across 17 ETFs (covers entries, stop, target, time cap, costs and sequencing; X8-X12 logic is covered by the hand-built unit tests and the truncation test) |

## Verdicts (each exit vs X3 = 3R target / 60 bars, paired on the same E4 entries)

dR = difference in R per trade, dividends received during the hold included (price-only dR shown too). Portfolio MAR uses daily mark-to-market equity.

| exit | ETF trades | ETF dR | adj. CI | price-only dR | ETF 2000-14 · 2015- | stock dR | stock adj. CI | stock halves | R/100 bars (exit vs X3) | portfolio MAR (exit vs X3) | random-entry dR · E4 minus random (95% CI) | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| X8 Half off at 3R, chandelier stop on the rest | 1,518 | +0.192 | -0.018 … +0.443 | +0.145 | +0.246 · +0.124 | +0.183 | +0.057 … +0.320 | +0.183 · +0.183 | +0.81 vs +1.07 | 0.21 vs 0.27 | +0.104 · +0.088 (-0.019 … +0.205) | **FAIL** (ETF adjusted CI includes 0; R per 100 bars below X3; portfolio MAR below X3) |
| X9 3R target, 40-bar time cap | 1,518 | -0.077 | -0.162 … +0.017 | -0.063 | -0.030 · -0.136 | -0.059 | -0.101 … -0.020 | -0.061 · -0.057 | +1.11 vs +1.07 | 0.23 vs 0.27 | -0.034 · -0.043 (-0.096 … +0.011) | **FAIL** (ETF adjusted CI includes 0; stock adjusted CI includes 0; a time half is not positive; portfolio MAR below X3) |
| X10 Structural: hold until rule 3 confirms | 1,518 | -0.033 | -0.202 … +0.165 | -0.058 | +0.067 · -0.158 | +0.057 | -0.035 … +0.172 | +0.016 · +0.103 | +0.78 vs +1.07 | 0.18 vs 0.27 | -0.014 · -0.019 (-0.112 … +0.076) | **FAIL** (ETF adjusted CI includes 0; stock adjusted CI includes 0; a time half is not positive; R per 100 bars below X3; portfolio MAR below X3) |
| X11 Fast: line break after stacked warnings, else rule 3 | 1,518 | -0.038 | -0.212 … +0.178 | -0.047 | +0.078 · -0.182 | +0.007 | -0.071 … +0.096 | -0.019 · +0.036 | +0.93 vs +1.07 | 0.22 vs 0.27 | -0.019 · -0.019 (-0.114 … +0.079) | **FAIL** (ETF adjusted CI includes 0; stock adjusted CI includes 0; a time half is not positive; R per 100 bars below X3; portfolio MAR below X3) |
| X12 Hybrid: 3R target and 60-bar cap, but exit on rule 3 if it comes first | 1,518 | -0.070 | -0.155 … +0.006 | -0.059 | -0.012 · -0.141 | -0.045 | -0.082 … -0.007 | -0.043 · -0.047 | +1.03 vs +1.07 | 0.24 vs 0.27 | -0.037 · -0.032 (-0.073 … +0.006) | **FAIL** (ETF adjusted CI includes 0; stock adjusted CI includes 0; a time half is not positive; R per 100 bars below X3; portfolio MAR below X3) |

## Decision (written before the results)

- No exit passed. X3 stays. The exit question is closed for this cycle (no re-test of these definitions on this data).

## Exits on E4 entries: ETFs

| exit | trades | mean R (with dividends) | mean R (price only) | win % | median R | mean bars | R per 100 bars | exit reasons |
|---|---|---|---|---|---|---|---|---|
| X3 3R target, 60-bar time cap (current playbook, baseline) | 1,518 | +0.389 | +0.324 | 49 | -0.12 | 37 | +1.07 | stop 632, time 570, target 216, stop_gap 100 |
| X8 Half off at 3R, chandelier stop on the rest | 1,518 | +0.580 | +0.469 | 39 | -0.91 | 72 | +0.81 | stop 782, trail 455, stop_gap 144, time 69, trail_gap 68 |
| X9 3R target, 40-bar time cap | 1,518 | +0.312 | +0.261 | 51 | +0.05 | 28 | +1.11 | time 731, stop 547, target 146, stop_gap 94 |
| X10 Structural: hold until rule 3 confirms | 1,518 | +0.356 | +0.266 | 44 | -0.28 | 46 | +0.78 | rule3 966, stop 472, stop_gap 77, time 3 |
| X11 Fast: line break after stacked warnings, else rule 3 | 1,518 | +0.351 | +0.277 | 46 | -0.14 | 38 | +0.93 | rule3 609, fast 427, stop 420, stop_gap 62 |
| X12 Hybrid: 3R target and 60-bar cap, but exit on rule 3 if it comes first | 1,518 | +0.319 | +0.265 | 47 | -0.14 | 31 | +1.03 | rule3 509, stop 452, time 292, target 195, stop_gap 70 |

## Exits on E4 entries: stocks (survivorship-biased list; replication only)

| exit | trades | mean R (with dividends) | mean R (price only) | win % | median R | mean bars | R per 100 bars | exit reasons |
|---|---|---|---|---|---|---|---|---|
| X3 3R target, 60-bar time cap (current playbook, baseline) | 5,194 | +0.295 | +0.245 | 45 | -0.70 | 35 | +0.84 | stop 2218, time 1765, target 829, stop_gap 382 |
| X8 Half off at 3R, chandelier stop on the rest | 5,194 | +0.478 | +0.388 | 38 | -0.95 | 67 | +0.71 | stop 2740, trail 1433, stop_gap 486, time 290, trail_gap 245 |
| X9 3R target, 40-bar time cap | 5,194 | +0.236 | +0.195 | 49 | -0.11 | 27 | +0.87 | time 2347, stop 1948, target 554, stop_gap 345 |
| X10 Structural: hold until rule 3 confirms | 5,194 | +0.352 | +0.282 | 41 | -0.40 | 43 | +0.81 | rule3 3187, stop 1710, stop_gap 289, time 8 |
| X11 Fast: line break after stacked warnings, else rule 3 | 5,194 | +0.302 | +0.245 | 43 | -0.26 | 36 | +0.84 | rule3 2086, stop 1533, fast 1315, stop_gap 259, time 1 |
| X12 Hybrid: 3R target and 60-bar cap, but exit on rule 3 if it comes first | 5,194 | +0.250 | +0.206 | 44 | -0.31 | 29 | +0.85 | rule3 1731, stop 1652, time 789, target 748, stop_gap 274 |

## Portfolio check (ETFs, no-overlap trades, 0.75% risk, max 5 open, daily mark-to-market, dividends included)

| exit | trades | CAGR | max drawdown | MAR |
|---|---|---|---|---|
| X3 3R target, 60-bar time cap (current playbook, baseline) | 475 | 5.0% | -18.4% | 0.27 |
| X8 Half off at 3R, chandelier stop on the rest | 285 | 4.6% | -21.6% | 0.21 |
| X9 3R target, 40-bar time cap | 516 | 3.8% | -16.4% | 0.23 |
| X10 Structural: hold until rule 3 confirms | 448 | 4.1% | -22.8% | 0.18 |
| X11 Fast: line break after stacked warnings, else rule 3 | 483 | 4.5% | -20.3% | 0.22 |
| X12 Hybrid: 3R target and 60-bar cap, but exit on rule 3 if it comes first | 514 | 4.3% | -17.7% | 0.24 |

## Sensitivity (ETF mean dR at each neighbour; a PASS needs every one > 0)

| exit | neighbour | dR |
|---|---|---|
| X8 | chandelier_atr=2.5 | +0.173 |
| X8 | chandelier_atr=3.5 | +0.198 |
| X9 | time_cap=30 | -0.136 |
| X9 | time_cap=50 | -0.050 |
| X10 | piv=5 | +0.124 |
| X11 | piv=5 | +0.017 |
| X11 | tol=0.0 | -0.074 |
| X11 | tol=0.5 | -0.037 |
| X11 | xb_warn=1 | -0.105 |
| X11 | xb_warn=3 | -0.017 |
| X11 | xb_win=30 | -0.064 |
| X11 | ext_up=1.5 | -0.038 |
| X11 | ext_up=2.5 | -0.041 |
| X12 | piv=5 | -0.024 |

## Random-entry control (ETFs, same exits; how much of an exit's gain any long entry would get)

| exit | trades | mean R (with dividends) | mean R (price only) | win % | median R | mean bars | R per 100 bars | exit reasons |
|---|---|---|---|---|---|---|---|---|
| X3 3R target, 60-bar time cap (current playbook, baseline) | 11,398 | +0.159 | +0.109 | 35 | -1.02 | 23 | +0.70 | stop 6212, target 2324, time 1861, stop_gap 1001 |
| X8 Half off at 3R, chandelier stop on the rest | 11,398 | +0.263 | +0.187 | 31 | -1.02 | 38 | +0.68 | stop 6702, trail 3029, stop_gap 1112, trail_gap 403, time 152 |
| X9 3R target, 40-bar time cap | 11,398 | +0.125 | +0.082 | 38 | -1.01 | 19 | +0.67 | stop 5843, time 2732, target 1884, stop_gap 939 |
| X10 Structural: hold until rule 3 confirms | 11,398 | +0.145 | +0.054 | 31 | -1.01 | 32 | +0.46 | stop 5754, rule3 4708, stop_gap 928, time 8 |
| X11 Fast: line break after stacked warnings, else rule 3 | 11,398 | +0.140 | +0.066 | 33 | -0.96 | 27 | +0.52 | stop 5338, rule3 2990, fast 2258, stop_gap 812 |
| X12 Hybrid: 3R target and 60-bar cap, but exit on rule 3 if it comes first | 11,398 | +0.121 | +0.077 | 35 | -0.97 | 20 | +0.61 | stop 5407, target 2152, rule3 2146, stop_gap 857, time 836 |
