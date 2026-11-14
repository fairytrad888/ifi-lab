# IFI Lab results: daily · stocks
_Run 2026-11-14 17:48 UTC · 61 symbols · 2000-01-03 to 2026-11-13 · split 2015-01-01 · 42 setup×exit tests (Bonferroni-adjusted) · engine v1.3.3_

> **Survivorship bias:** this stock list was chosen in 2026 from today's large caps, so random long entries earn money too. Judge stock setups by their edge over the random-entry control, not by raw expectancy.

## P1 · Exits × setups (R per trade, after costs)

Random-entry control (same stops and exits), mean expectancy by exit: X1_time10 +0.036R, X2_target2R +0.110R, X3_target3R +0.162R, X4_trendline_trail +0.054R, X5_chandelier3atr +0.143R, X6_partial1R_then_line +0.007R, X7_stage_drop +0.071R

| setup | exit | n | win_rate | avg_win | avg_loss | expectancy | median | exp_w10 | ci_low | ci_low_adj | exp_early | exp_late | exp_symA | exp_symB | random_mean | random_p95 | avg_bars | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 523 | 0.413 | 2.286 | -1.042 | 0.332 | -1.018 | 0.332 | 0.180 | 0.115 | 0.278 | 0.393 | 0.368 | 0.296 | 0.162 | 0.298 | 26.845 | ADOPT |
| E1_trigger_with_trend | X5_chandelier3atr | 525 | 0.434 | 1.675 | -0.776 | 0.288 | -0.259 | 0.274 | 0.142 | 0.054 | 0.210 | 0.376 | 0.384 | 0.191 | 0.143 | 0.296 | 20.065 | REJECT |
| E4_anchor_reclaim | X3_target3R | 3181 | 0.473 | 1.653 | -0.957 | 0.279 | -0.196 | 0.279 | 0.228 | 0.194 | 0.244 | 0.315 | 0.311 | 0.247 | 0.162 | 0.216 | 38.859 | ADOPT |
| E1_trigger_with_trend | X2_target2R | 524 | 0.454 | 1.807 | -1.047 | 0.249 | -1.011 | 0.249 | 0.120 | 0.063 | 0.236 | 0.264 | 0.254 | 0.244 | 0.110 | 0.213 | 21.559 | ADOPT |
| E4_anchor_reclaim | X2_target2R | 3185 | 0.491 | 1.453 | -0.959 | 0.225 | -0.052 | 0.225 | 0.178 | 0.150 | 0.201 | 0.249 | 0.248 | 0.201 | 0.110 | 0.153 | 34.470 | ADOPT |
| E1b_trigger_counter_trend | X3_target3R | 2514 | 0.390 | 2.176 | -1.049 | 0.208 | -1.016 | 0.208 | 0.138 | 0.103 | 0.141 | 0.297 | 0.215 | 0.202 | 0.162 | 0.225 | 26.020 | REJECT |
| E5_score4 | X3_target3R | 5317 | 0.418 | 1.912 | -1.024 | 0.204 | -1.015 | 0.204 | 0.159 | 0.141 | 0.184 | 0.226 | 0.211 | 0.198 | 0.162 | 0.202 | 32.411 | ADOPT |
| E3_stage2_transition | X3_target3R | 2508 | 0.413 | 1.893 | -1.002 | 0.193 | -1.013 | 0.193 | 0.136 | 0.101 | 0.198 | 0.188 | 0.160 | 0.226 | 0.162 | 0.225 | 34.215 | REJECT |
| E5_score4 | X2_target2R | 5620 | 0.452 | 1.607 | -1.022 | 0.166 | -1.008 | 0.166 | 0.131 | 0.113 | 0.146 | 0.188 | 0.173 | 0.159 | 0.110 | 0.141 | 27.816 | ADOPT |
| E3_stage2_transition | X2_target2R | 2540 | 0.446 | 1.620 | -1.005 | 0.165 | -1.008 | 0.165 | 0.108 | 0.080 | 0.171 | 0.159 | 0.142 | 0.187 | 0.110 | 0.157 | 28.854 | ADOPT |
| E1_trigger_with_trend | X1_time10 | 527 | 0.541 | 0.961 | -0.774 | 0.165 | 0.118 | 0.165 | 0.074 | 0.023 | 0.150 | 0.181 | 0.169 | 0.160 | 0.036 | 0.137 | 8.651 | ADOPT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 2601 | 0.381 | 1.737 | -0.824 | 0.152 | -0.440 | 0.149 | 0.091 | 0.040 | 0.046 | 0.296 | 0.170 | 0.136 | 0.143 | 0.213 | 19.555 | REJECT |
| E4_anchor_reclaim | X7_stage_drop | 3922 | 0.367 | 1.366 | -0.551 | 0.152 | -0.254 | 0.150 | 0.109 | 0.077 | 0.128 | 0.177 | 0.167 | 0.136 | 0.071 | 0.114 | 23.566 | ADOPT |
| E5_score4 | X7_stage_drop | 6418 | 0.354 | 1.583 | -0.647 | 0.142 | -0.305 | 0.133 | 0.101 | 0.072 | 0.132 | 0.154 | 0.135 | 0.150 | 0.071 | 0.105 | 22.557 | ADOPT |
| E3_stage2_transition | X5_chandelier3atr | 2859 | 0.393 | 1.383 | -0.666 | 0.139 | -0.283 | 0.133 | 0.086 | 0.055 | 0.130 | 0.149 | 0.098 | 0.180 | 0.143 | 0.208 | 20.651 | REJECT |
| E1b_trigger_counter_trend | X2_target2R | 2520 | 0.426 | 1.734 | -1.051 | 0.136 | -1.012 | 0.136 | 0.079 | 0.051 | 0.070 | 0.223 | 0.153 | 0.120 | 0.110 | 0.158 | 21.037 | REJECT |
| E4_anchor_reclaim | X5_chandelier3atr | 3588 | 0.420 | 1.130 | -0.596 | 0.130 | -0.193 | 0.128 | 0.092 | 0.070 | 0.088 | 0.172 | 0.149 | 0.110 | 0.143 | 0.202 | 21.595 | REJECT |
| E5_score4 | X4_trendline_trail | 6766 | 0.339 | 1.482 | -0.570 | 0.125 | -0.285 | 0.117 | 0.089 | 0.070 | 0.107 | 0.145 | 0.128 | 0.122 | 0.054 | 0.085 | 19.855 | ADOPT |
| E4_anchor_reclaim | X4_trendline_trail | 4296 | 0.337 | 1.280 | -0.474 | 0.116 | -0.250 | 0.114 | 0.077 | 0.063 | 0.087 | 0.146 | 0.126 | 0.107 | 0.054 | 0.094 | 19.707 | ADOPT |
| E5_score4 | X5_chandelier3atr | 6555 | 0.390 | 1.364 | -0.689 | 0.111 | -0.286 | 0.107 | 0.076 | 0.053 | 0.104 | 0.119 | 0.096 | 0.128 | 0.143 | 0.184 | 19.496 | REJECT |
| E3_stage2_transition | X7_stage_drop | 3123 | 0.319 | 1.441 | -0.515 | 0.109 | -0.283 | 0.105 | 0.059 | 0.032 | 0.110 | 0.108 | 0.065 | 0.154 | 0.071 | 0.122 | 18.316 | REJECT |
| E2_exhaustion_confluence | X3_target3R | 1250 | 0.318 | 2.650 | -1.094 | 0.098 | -1.035 | 0.098 | 0.003 | -0.070 | 0.051 | 0.152 | 0.131 | 0.067 | 0.162 | 0.251 | 15.575 | REJECT |
| E3_stage2_transition | X4_trendline_trail | 3128 | 0.287 | 1.286 | -0.387 | 0.093 | -0.223 | 0.089 | 0.050 | 0.023 | 0.081 | 0.108 | 0.066 | 0.121 | 0.054 | 0.100 | 13.769 | REJECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 1267 | 0.313 | 2.427 | -0.975 | 0.088 | -1.014 | 0.069 | -0.029 | -0.108 | 0.024 | 0.162 | 0.143 | 0.037 | 0.143 | 0.240 | 15.687 | REJECT |
| E1_trigger_with_trend | X7_stage_drop | 555 | 0.443 | 0.499 | -0.265 | 0.073 | -0.046 | 0.071 | 0.004 | -0.035 | 0.022 | 0.131 | 0.038 | 0.110 | 0.071 | 0.203 | 3.645 | REJECT |
| E4_anchor_reclaim | X6_partial1R_then_line | 4302 | 0.384 | 0.952 | -0.477 | 0.072 | -0.216 | 0.072 | 0.046 | 0.029 | 0.048 | 0.097 | 0.079 | 0.065 | 0.007 | 0.033 | 19.321 | ADOPT |
| E1_trigger_with_trend | X4_trendline_trail | 555 | 0.445 | 0.476 | -0.261 | 0.067 | -0.044 | 0.064 | -0.000 | -0.043 | 0.005 | 0.137 | 0.039 | 0.096 | 0.054 | 0.168 | 3.218 | REJECT |
| E5_score4 | X6_partial1R_then_line | 6857 | 0.412 | 0.975 | -0.575 | 0.064 | -0.211 | 0.063 | 0.041 | 0.024 | 0.048 | 0.081 | 0.067 | 0.061 | 0.007 | 0.029 | 19.042 | ADOPT |
| E3_stage2_transition | X1_time10 | 3008 | 0.508 | 0.717 | -0.646 | 0.046 | 0.012 | 0.046 | 0.015 | -0.004 | 0.044 | 0.049 | 0.035 | 0.058 | 0.036 | 0.077 | 9.125 | REJECT |
| E3_stage2_transition | X6_partial1R_then_line | 3128 | 0.328 | 0.928 | -0.388 | 0.044 | -0.203 | 0.044 | 0.016 | -0.007 | 0.035 | 0.056 | 0.028 | 0.061 | 0.007 | 0.038 | 13.506 | PROMISING (not significant after correction) |
| E4_anchor_reclaim | X1_time10 | 3985 | 0.524 | 0.631 | -0.602 | 0.044 | 0.040 | 0.044 | 0.020 | 0.004 | 0.016 | 0.073 | 0.049 | 0.039 | 0.036 | 0.071 | 9.299 | REJECT |
| E1_trigger_with_trend | X6_partial1R_then_line | 555 | 0.447 | 0.412 | -0.261 | 0.039 | -0.043 | 0.039 | -0.011 | -0.041 | -0.006 | 0.090 | -0.000 | 0.080 | 0.007 | 0.080 | 3.216 | REJECT |
| E5_score4 | X1_time10 | 7615 | 0.501 | 0.770 | -0.697 | 0.038 | 0.003 | 0.038 | 0.016 | 0.003 | 0.024 | 0.054 | 0.043 | 0.034 | 0.036 | 0.062 | 8.939 | REJECT |
| E1b_trigger_counter_trend | X1_time10 | 2613 | 0.482 | 0.960 | -0.823 | 0.036 | -0.052 | 0.036 | -0.005 | -0.032 | 0.007 | 0.075 | 0.039 | 0.033 | 0.036 | 0.079 | 8.345 | REJECT |
| E2_exhaustion_confluence | X2_target2R | 1255 | 0.375 | 1.919 | -1.098 | 0.034 | -1.029 | 0.034 | -0.048 | -0.091 | -0.007 | 0.081 | 0.038 | 0.030 | 0.110 | 0.179 | 11.582 | REJECT |
| E1b_trigger_counter_trend | X7_stage_drop | 2799 | 0.451 | 0.352 | -0.320 | -0.017 | -0.038 | -0.017 | -0.036 | -0.045 | -0.016 | -0.018 | -0.005 | -0.028 | 0.071 | 0.124 | 2.235 | REJECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 2799 | 0.453 | 0.347 | -0.319 | -0.017 | -0.036 | -0.017 | -0.036 | -0.048 | -0.019 | -0.016 | -0.006 | -0.028 | 0.054 | 0.107 | 2.148 | REJECT |
| E1b_trigger_counter_trend | X6_partial1R_then_line | 2799 | 0.456 | 0.339 | -0.319 | -0.019 | -0.034 | -0.019 | -0.037 | -0.047 | -0.019 | -0.019 | -0.010 | -0.028 | 0.007 | 0.040 | 2.148 | REJECT |
| E2_exhaustion_confluence | X7_stage_drop | 1273 | 0.452 | 0.487 | -0.461 | -0.033 | -0.046 | -0.033 | -0.071 | -0.095 | -0.021 | -0.046 | -0.045 | -0.021 | 0.071 | 0.148 | 2.202 | REJECT |
| E2_exhaustion_confluence | X4_trendline_trail | 1273 | 0.451 | 0.474 | -0.461 | -0.039 | -0.046 | -0.039 | -0.075 | -0.102 | -0.034 | -0.046 | -0.048 | -0.031 | 0.054 | 0.126 | 2.095 | REJECT |
| E2_exhaustion_confluence | X6_partial1R_then_line | 1273 | 0.456 | 0.455 | -0.457 | -0.041 | -0.038 | -0.041 | -0.074 | -0.097 | -0.036 | -0.046 | -0.049 | -0.033 | 0.007 | 0.056 | 2.090 | REJECT |
| E2_exhaustion_confluence | X1_time10 | 1267 | 0.389 | 1.397 | -0.970 | -0.049 | -0.783 | -0.051 | -0.130 | -0.169 | -0.041 | -0.058 | -0.021 | -0.076 | 0.036 | 0.100 | 7.122 | REJECT |

### Exit rules ranked (trade-weighted across setups)

| exit | trades | mean_expectancy | random_mean | edge_over_random |
|---|---|---|---|---|
| X3_target3R | 15,293 | 0.214 | 0.162 | 0.052 |
| X2_target2R | 15,644 | 0.165 | 0.110 | 0.055 |
| X5_chandelier3atr | 17,395 | 0.129 | 0.143 | -0.013 |
| X7_stage_drop | 18,090 | 0.100 | 0.071 | 0.029 |
| X4_trendline_trail | 18,817 | 0.084 | 0.054 | 0.030 |
| X6_partial1R_then_line | 18,914 | 0.043 | 0.007 | 0.035 |
| X1_time10 | 19,015 | 0.038 | 0.036 | 0.003 |

## P1b · Sizing (fixed-fractional, max open positions = 5)

| setup | exit | risk_pct | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 0.005 | 0.022 | -0.100 | 0.219 | 178,097 |
| E1_trigger_with_trend | X3_target3R | 0.010 | 0.042 | -0.191 | 0.218 | 297,676 |
| E1_trigger_with_trend | X3_target3R | 0.020 | 0.075 | -0.349 | 0.216 | 697,220 |
| E1_trigger_with_trend | X5_chandelier3atr | 0.005 | 0.020 | -0.080 | 0.254 | 171,618 |
| E1_trigger_with_trend | X5_chandelier3atr | 0.010 | 0.039 | -0.157 | 0.248 | 277,484 |
| E1_trigger_with_trend | X5_chandelier3atr | 0.020 | 0.071 | -0.298 | 0.237 | 620,685 |
| E4_anchor_reclaim | X3_target3R | 0.005 | 0.032 | -0.103 | 0.309 | 231,812 |
| E4_anchor_reclaim | X3_target3R | 0.010 | 0.062 | -0.197 | 0.313 | 498,580 |
| E4_anchor_reclaim | X3_target3R | 0.020 | 0.115 | -0.361 | 0.320 | 1,880,045 |

## P2 · Market regime (SPY > 200-day average and Trend line rising)

| setup | exit | n_on | exp_on | n_off | exp_off | diff | diff_ci_low | verdict |
|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X4_trendline_trail | 236 | 0.067 | 319 | 0.066 | 0.001 | -0.188 | NO CLEAR EFFECT |
| E1_trigger_with_trend | X5_chandelier3atr | 225 | 0.072 | 300 | 0.450 | -0.378 | -0.826 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 747 | 0.004 | 2052 | -0.025 | 0.029 | -0.026 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 695 | 0.208 | 1906 | 0.132 | 0.076 | -0.129 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X4_trendline_trail | 314 | -0.086 | 959 | -0.024 | -0.062 | -0.170 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 311 | -0.009 | 956 | 0.120 | -0.129 | -0.493 | NO CLEAR EFFECT |
| E3_stage2_transition | X4_trendline_trail | 1868 | 0.091 | 1260 | 0.097 | -0.006 | -0.136 | NO CLEAR EFFECT |
| E3_stage2_transition | X5_chandelier3atr | 1708 | 0.158 | 1151 | 0.110 | 0.049 | -0.108 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X4_trendline_trail | 2607 | 0.127 | 1689 | 0.100 | 0.027 | -0.080 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X5_chandelier3atr | 2220 | 0.137 | 1368 | 0.117 | 0.020 | -0.104 | NO CLEAR EFFECT |
| E5_score4 | X4_trendline_trail | 4452 | 0.143 | 2314 | 0.092 | 0.051 | -0.048 | NO CLEAR EFFECT |
| E5_score4 | X5_chandelier3atr | 4412 | 0.125 | 2143 | 0.082 | 0.043 | -0.062 | NO CLEAR EFFECT |

## P3 · Earnings drift (stocks)

| test | n | mean | mean_vs_spy | hit_vs_spy | ci_low |
|---|---|---|---|---|---|
| Positive earnings gap → hold 20 bars | 750 | 0.016 | 0.010 | 0.531 |  |
| IFI setups ≤20 bars after positive gap (R, X4) | 804 | 0.166 |  |  | 0.082 |
| Same setups at other times (R, X4) | 18013 | 0.080 |  |  | 0.062 |

## P4 · Portfolio heat (E1_trigger_with_trend + X3_target3R)

| rule | cagr | max_dd | mar | final |
|---|---|---|---|---|
| No sector cap | 0.032 | -0.146 | 0.222 | 234,839 |
| Max 1 open per sector | 0.035 | -0.127 | 0.277 | 251,516 |

## P6 · Playbook portfolio (E4_anchor_reclaim + E1_trigger_with_trend, exit X3_target3R, 1 per symbol, 1 per sector, max 5 open)

| risk | trades | trades_per_year | expectancy | win_rate | longest_losing_streak | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|---|---|---|
| 0.50% | 1276 | 47.538 | 0.282 | 0.462 | 14 | 0.044 | -0.078 | 0.558 | 314,293 |
| 0.75% | 1276 | 47.538 | 0.282 | 0.462 | 14 | 0.065 | -0.115 | 0.564 | 540,677 |
| 1.00% | 1276 | 47.538 | 0.282 | 0.462 | 14 | 0.086 | -0.150 | 0.571 | 912,549 |

## E6 · Playbook E4 after a positive earnings gap (stocks)

| group | n | expectancy | ci_low | verdict |
|---|---|---|---|---|
| E4 ≤20 bars after positive gap | 200 | 0.434 |  |  |
| E4 at other times | 2981 | 0.269 |  |  |
| Difference (95% CI low) | 3181 | 0.165 | -0.014 | NO CLEAR EFFECT |

---
**How to read verdicts.** ADOPT = ≥ min trades, bootstrap CI above 0 after correcting for the number of tests, positive in both time halves and both symbol halves, and better than random entries with the same exits. PROMISING = everything except significance. UNSTABLE = fails a half. REJECT = not positive or not better than random.