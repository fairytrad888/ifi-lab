# IFI Lab results: h4 · etfs
_Run 2026-10-31 17:02 UTC · 16 symbols · 2023-11-10 to 2026-10-30 · split 2025-05-05 · 42 setup×exit tests (Bonferroni-adjusted) · engine v1.3.3_

## P1 · Exits × setups (R per trade, after costs)

Random-entry control (same stops and exits), mean expectancy by exit: X1_time10 -0.006R, X2_target2R -0.030R, X3_target3R +0.002R, X4_trendline_trail -0.023R, X5_chandelier3atr +0.046R, X6_partial1R_then_line -0.050R, X7_stage_drop -0.016R

| setup | exit | n | win_rate | avg_win | avg_loss | expectancy | median | exp_w10 | ci_low | ci_low_adj | exp_early | exp_late | exp_symA | exp_symB | random_mean | random_p95 | avg_bars | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E1b_trigger_counter_trend | X5_chandelier3atr | 153 | 0.425 | 2.275 | -0.893 | 0.453 | -0.352 | 0.444 | 0.102 | -0.092 | 0.498 | 0.403 | 0.220 | 0.654 | 0.046 | 0.356 | 19.307 | PROMISING (not significant after correction) |
| E1b_trigger_counter_trend | X3_target3R | 150 | 0.433 | 2.445 | -1.139 | 0.414 | -1.037 | 0.414 | 0.100 | -0.048 | 0.573 | 0.246 | 0.308 | 0.504 | 0.002 | 0.229 | 22.953 | PROMISING (not significant after correction) |
| E1_trigger_with_trend | X3_target3R | 40 | 0.425 | 2.190 | -1.098 | 0.299 | -1.031 | 0.299 | -0.234 | -0.501 | 0.452 | 0.174 | 0.267 | 0.334 | 0.002 | 0.438 | 23.975 | INCONCLUSIVE (too few trades) |
| E4_anchor_reclaim | X3_target3R | 188 | 0.495 | 1.499 | -0.943 | 0.265 | -0.051 | 0.265 | 0.067 | -0.040 | 0.172 | 0.351 | 0.257 | 0.273 | 0.002 | 0.197 | 41.713 | PROMISING (not significant after correction) |
| E1_trigger_with_trend | X2_target2R | 41 | 0.488 | 1.692 | -1.140 | 0.241 | -1.016 | 0.241 | -0.199 | -0.489 | 0.483 | 0.032 | 0.205 | 0.279 | -0.030 | 0.334 | 18.707 | INCONCLUSIVE (too few trades) |
| E4_anchor_reclaim | X2_target2R | 189 | 0.497 | 1.386 | -0.938 | 0.218 | -0.048 | 0.218 | 0.039 | -0.062 | 0.134 | 0.295 | 0.224 | 0.212 | -0.030 | 0.157 | 37.296 | PROMISING (not significant after correction) |
| E1_trigger_with_trend | X1_time10 | 41 | 0.585 | 1.082 | -1.037 | 0.203 | 0.561 | 0.203 | -0.156 | -0.334 | 0.488 | -0.042 | 0.278 | 0.125 | -0.006 | 0.383 | 8.463 | INCONCLUSIVE (too few trades) |
| E2_exhaustion_confluence | X1_time10 | 73 | 0.397 | 2.103 | -1.060 | 0.197 | -1.042 | 0.197 | -0.220 | -0.456 | 0.223 | 0.170 | 0.710 | -0.087 | -0.006 | 0.298 | 6.918 | REJECT |
| E1_trigger_with_trend | X5_chandelier3atr | 41 | 0.512 | 1.305 | -0.972 | 0.194 | 0.103 | 0.194 | -0.200 | -0.441 | 0.442 | -0.021 | 0.135 | 0.255 | 0.046 | 0.718 | 17.463 | INCONCLUSIVE (too few trades) |
| E1b_trigger_counter_trend | X1_time10 | 155 | 0.529 | 1.187 | -0.938 | 0.186 | 0.101 | 0.186 | -0.035 | -0.171 | 0.392 | -0.045 | 0.050 | 0.307 | -0.006 | 0.195 | 8.071 | REJECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 73 | 0.329 | 2.661 | -1.033 | 0.182 | -0.992 | 0.163 | -0.311 | -0.586 | 0.285 | 0.075 | 0.548 | -0.021 | 0.046 | 0.508 | 13.890 | REJECT |
| E3_stage2_transition | X3_target3R | 155 | 0.426 | 1.662 | -0.983 | 0.144 | -1.013 | 0.144 | -0.090 | -0.221 | 0.186 | 0.101 | 0.196 | 0.089 | 0.002 | 0.217 | 33.394 | REJECT |
| E1b_trigger_counter_trend | X2_target2R | 150 | 0.433 | 1.797 | -1.139 | 0.133 | -1.037 | 0.133 | -0.129 | -0.237 | 0.279 | -0.020 | 0.035 | 0.217 | -0.030 | 0.192 | 17.727 | REJECT |
| E1_trigger_with_trend | X6_partial1R_then_line | 44 | 0.614 | 0.391 | -0.307 | 0.122 | 0.132 | 0.122 | -0.009 | -0.089 | 0.203 | 0.047 | 0.116 | 0.128 | -0.050 | 0.190 | 3.841 | INCONCLUSIVE (too few trades) |
| E3_stage2_transition | X7_stage_drop | 183 | 0.344 | 1.302 | -0.524 | 0.105 | -0.248 | 0.098 | -0.079 | -0.168 | 0.129 | 0.080 | 0.169 | 0.041 | -0.016 | 0.173 | 19.918 | REJECT |
| E1_trigger_with_trend | X4_trendline_trail | 44 | 0.591 | 0.398 | -0.326 | 0.102 | 0.117 | 0.102 | -0.039 | -0.135 | 0.176 | 0.034 | 0.119 | 0.084 | -0.023 | 0.386 | 3.864 | INCONCLUSIVE (too few trades) |
| E4_anchor_reclaim | X7_stage_drop | 231 | 0.368 | 1.145 | -0.508 | 0.100 | -0.171 | 0.100 | -0.043 | -0.100 | 0.128 | 0.075 | 0.149 | 0.061 | -0.016 | 0.155 | 23.095 | REJECT |
| E1_trigger_with_trend | X7_stage_drop | 44 | 0.591 | 0.391 | -0.326 | 0.098 | 0.117 | 0.098 | -0.043 | -0.135 | 0.176 | 0.026 | 0.119 | 0.075 | -0.016 | 0.390 | 3.886 | INCONCLUSIVE (too few trades) |
| E4_anchor_reclaim | X4_trendline_trail | 244 | 0.381 | 1.030 | -0.480 | 0.096 | -0.199 | 0.096 | -0.037 | -0.102 | 0.087 | 0.104 | 0.167 | 0.037 | -0.023 | 0.133 | 20.197 | REJECT |
| E4_anchor_reclaim | X6_partial1R_then_line | 244 | 0.426 | 0.864 | -0.493 | 0.086 | -0.137 | 0.086 | -0.016 | -0.072 | 0.099 | 0.073 | 0.133 | 0.047 | -0.050 | 0.050 | 20.012 | PROMISING (not significant after correction) |
| E5_score4 | X2_target2R | 321 | 0.445 | 1.480 | -1.036 | 0.085 | -1.012 | 0.085 | -0.059 | -0.155 | 0.023 | 0.134 | 0.153 | 0.018 | -0.030 | 0.110 | 28.333 | REJECT |
| E3_stage2_transition | X2_target2R | 158 | 0.437 | 1.461 | -0.987 | 0.082 | -0.831 | 0.082 | -0.116 | -0.240 | 0.148 | 0.016 | 0.157 | 0.004 | -0.030 | 0.172 | 29.671 | REJECT |
| E3_stage2_transition | X4_trendline_trail | 183 | 0.317 | 1.132 | -0.413 | 0.077 | -0.208 | 0.070 | -0.085 | -0.173 | 0.146 | 0.007 | 0.205 | -0.049 | -0.023 | 0.158 | 15.208 | REJECT |
| E4_anchor_reclaim | X5_chandelier3atr | 223 | 0.426 | 0.903 | -0.546 | 0.072 | -0.119 | 0.072 | -0.051 | -0.114 | 0.125 | 0.024 | 0.109 | 0.042 | 0.046 | 0.301 | 18.498 | REJECT |
| E2_exhaustion_confluence | X3_target3R | 73 | 0.315 | 2.728 | -1.170 | 0.058 | -1.062 | 0.058 | -0.367 | -0.567 | 0.015 | 0.103 | 0.263 | -0.055 | 0.002 | 0.331 | 13.247 | REJECT |
| E4_anchor_reclaim | X1_time10 | 231 | 0.580 | 0.562 | -0.646 | 0.055 | 0.155 | 0.055 | -0.040 | -0.106 | 0.021 | 0.086 | 0.033 | 0.072 | -0.006 | 0.153 | 9.173 | REJECT |
| E3_stage2_transition | X6_partial1R_then_line | 183 | 0.344 | 0.893 | -0.419 | 0.033 | -0.205 | 0.033 | -0.087 | -0.167 | 0.095 | -0.030 | 0.101 | -0.034 | -0.050 | 0.057 | 15.115 | REJECT |
| E5_score4 | X3_target3R | 312 | 0.397 | 1.626 | -1.028 | 0.027 | -1.024 | 0.027 | -0.134 | -0.205 | -0.014 | 0.059 | 0.069 | -0.015 | 0.002 | 0.154 | 32.064 | REJECT |
| E3_stage2_transition | X5_chandelier3atr | 174 | 0.397 | 1.085 | -0.678 | 0.021 | -0.223 | 0.021 | -0.141 | -0.233 | 0.060 | -0.016 | 0.072 | -0.030 | 0.046 | 0.309 | 18.253 | REJECT |
| E5_score4 | X7_stage_drop | 372 | 0.331 | 1.338 | -0.640 | 0.014 | -0.336 | 0.014 | -0.109 | -0.194 | 0.099 | -0.049 | 0.018 | 0.010 | -0.016 | 0.121 | 21.925 | REJECT |
| E5_score4 | X6_partial1R_then_line | 389 | 0.427 | 0.840 | -0.610 | 0.009 | -0.223 | 0.009 | -0.081 | -0.129 | 0.075 | -0.040 | 0.049 | -0.027 | -0.050 | 0.024 | 18.586 | REJECT |
| E5_score4 | X4_trendline_trail | 383 | 0.329 | 1.234 | -0.592 | 0.008 | -0.319 | 0.008 | -0.103 | -0.186 | 0.068 | -0.036 | 0.034 | -0.014 | -0.023 | 0.096 | 19.538 | REJECT |
| E3_stage2_transition | X1_time10 | 176 | 0.528 | 0.574 | -0.683 | -0.018 | 0.053 | -0.018 | -0.136 | -0.199 | -0.005 | -0.032 | 0.026 | -0.063 | -0.006 | 0.188 | 8.955 | REJECT |
| E5_score4 | X1_time10 | 434 | 0.530 | 0.637 | -0.767 | -0.023 | 0.037 | -0.023 | -0.100 | -0.139 | 0.028 | -0.058 | 0.052 | -0.090 | -0.006 | 0.111 | 8.760 | REJECT |
| E5_score4 | X5_chandelier3atr | 400 | 0.347 | 1.049 | -0.667 | -0.070 | -0.318 | -0.070 | -0.172 | -0.237 | 0.026 | -0.140 | -0.040 | -0.097 | 0.046 | 0.232 | 16.595 | REJECT |
| E2_exhaustion_confluence | X4_trendline_trail | 73 | 0.425 | 0.450 | -0.482 | -0.086 | -0.071 | -0.086 | -0.231 | -0.289 | -0.043 | -0.130 | -0.015 | -0.126 | -0.023 | 0.295 | 2.548 | REJECT |
| E2_exhaustion_confluence | X6_partial1R_then_line | 73 | 0.425 | 0.443 | -0.482 | -0.089 | -0.071 | -0.089 | -0.231 | -0.292 | -0.050 | -0.130 | -0.019 | -0.128 | -0.050 | 0.128 | 2.548 | REJECT |
| E2_exhaustion_confluence | X7_stage_drop | 73 | 0.425 | 0.424 | -0.491 | -0.102 | -0.071 | -0.102 | -0.241 | -0.298 | -0.065 | -0.141 | -0.015 | -0.150 | -0.016 | 0.290 | 2.603 | REJECT |
| E2_exhaustion_confluence | X2_target2R | 73 | 0.342 | 1.933 | -1.170 | -0.107 | -1.062 | -0.107 | -0.460 | -0.680 | -0.183 | -0.029 | 0.092 | -0.217 | -0.030 | 0.252 | 9.890 | REJECT |
| E1b_trigger_counter_trend | X6_partial1R_then_line | 166 | 0.452 | 0.259 | -0.413 | -0.110 | -0.039 | -0.110 | -0.196 | -0.257 | -0.104 | -0.115 | -0.167 | -0.060 | -0.050 | 0.065 | 2.060 | REJECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 166 | 0.452 | 0.252 | -0.413 | -0.113 | -0.039 | -0.113 | -0.198 | -0.258 | -0.107 | -0.119 | -0.174 | -0.060 | -0.023 | 0.179 | 2.060 | REJECT |
| E1b_trigger_counter_trend | X7_stage_drop | 166 | 0.452 | 0.250 | -0.413 | -0.114 | -0.039 | -0.114 | -0.199 | -0.258 | -0.109 | -0.119 | -0.176 | -0.060 | -0.016 | 0.186 | 2.078 | REJECT |

### Exit rules ranked (trade-weighted across setups)

| exit | trades | mean_expectancy | random_mean | edge_over_random |
|---|---|---|---|---|
| X3_target3R | 918 | 0.173 | 0.002 | 0.171 |
| X2_target2R | 932 | 0.111 | -0.030 | 0.141 |
| X5_chandelier3atr | 1,064 | 0.077 | 0.046 | 0.031 |
| X1_time10 | 1,110 | 0.046 | -0.006 | 0.052 |
| X7_stage_drop | 1,069 | 0.024 | -0.016 | 0.040 |
| X4_trendline_trail | 1,093 | 0.018 | -0.023 | 0.041 |
| X6_partial1R_then_line | 1,099 | 0.010 | -0.050 | 0.060 |

## P1b · Sizing (fixed-fractional, max open positions = 5)

| setup | exit | risk_pct | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|
| E1b_trigger_counter_trend | X5_chandelier3atr | 0.005 | 0.054 | -0.104 | 0.520 | 115,807 |
| E1b_trigger_counter_trend | X5_chandelier3atr | 0.010 | 0.103 | -0.200 | 0.517 | 131,378 |
| E1b_trigger_counter_trend | X5_chandelier3atr | 0.020 | 0.184 | -0.366 | 0.502 | 159,785 |
| E1b_trigger_counter_trend | X3_target3R | 0.005 | 0.067 | -0.119 | 0.562 | 119,640 |
| E1b_trigger_counter_trend | X3_target3R | 0.010 | 0.127 | -0.226 | 0.560 | 139,267 |
| E1b_trigger_counter_trend | X3_target3R | 0.020 | 0.222 | -0.410 | 0.542 | 174,719 |
| E4_anchor_reclaim | X3_target3R | 0.005 | 0.056 | -0.065 | 0.871 | 116,307 |
| E4_anchor_reclaim | X3_target3R | 0.010 | 0.111 | -0.126 | 0.887 | 133,877 |
| E4_anchor_reclaim | X3_target3R | 0.020 | 0.218 | -0.238 | 0.914 | 172,352 |

## P2 · Market regime (SPY > 200-day average and Trend line rising)

| setup | exit | n_on | exp_on | n_off | exp_off | diff | diff_ci_low | verdict |
|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X4_trendline_trail | 18 | 0.196 | 26 | 0.037 | 0.159 | -0.285 | NO CLEAR EFFECT |
| E1_trigger_with_trend | X5_chandelier3atr | 15 | 0.355 | 26 | 0.101 | 0.254 | -0.962 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 41 | -0.250 | 125 | -0.068 | -0.182 | -0.618 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 35 | 0.579 | 118 | 0.415 | 0.164 | -1.102 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X4_trendline_trail | 28 | -0.255 | 45 | 0.019 | -0.274 | -0.670 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 28 | -0.204 | 45 | 0.422 | -0.627 | -2.116 | NO CLEAR EFFECT |
| E3_stage2_transition | X4_trendline_trail | 120 | -0.020 | 63 | 0.261 | -0.280 | -1.074 | NO CLEAR EFFECT |
| E3_stage2_transition | X5_chandelier3atr | 114 | -0.047 | 60 | 0.151 | -0.198 | -0.777 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X4_trendline_trail | 175 | -0.023 | 69 | 0.396 | -0.419 | -0.971 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X5_chandelier3atr | 159 | -0.049 | 64 | 0.371 | -0.420 | -0.902 | NO CLEAR EFFECT |
| E5_score4 | X4_trendline_trail | 287 | -0.120 | 96 | 0.392 | -0.512 | -1.090 | NO CLEAR EFFECT |
| E5_score4 | X5_chandelier3atr | 302 | -0.135 | 98 | 0.129 | -0.263 | -0.611 | NO CLEAR EFFECT |

## P4 · Portfolio heat (E1b_trigger_counter_trend + X5_chandelier3atr)

| rule | cagr | max_dd | mar | final |
|---|---|---|---|---|
| No sector cap | 0.098 | -0.162 | 0.606 | 129,719 |
| Max 1 open per sector | 0.098 | -0.162 | 0.606 | 129,719 |

## P6 · Playbook portfolio (E4_anchor_reclaim + E1_trigger_with_trend, exit X3_target3R, 1 per symbol, 1 per sector, max 5 open)

| risk | trades | trades_per_year | expectancy | win_rate | longest_losing_streak | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|---|---|---|
| 0.50% | 208 | 75.294 | 0.297 | 0.490 | 13 | 0.074 | -0.075 | 0.979 | 121,746 |
| 0.75% | 208 | 75.294 | 0.297 | 0.490 | 13 | 0.110 | -0.111 | 0.989 | 133,500 |
| 1.00% | 208 | 75.294 | 0.297 | 0.490 | 13 | 0.146 | -0.146 | 0.999 | 145,806 |

---
**How to read verdicts.** ADOPT = ≥ min trades, bootstrap CI above 0 after correcting for the number of tests, positive in both time halves and both symbol halves, and better than random entries with the same exits. PROMISING = everything except significance. UNSTABLE = fails a half. REJECT = not positive or not better than random.