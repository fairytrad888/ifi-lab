# IFI Lab results: daily · etfs
_Run 2026-10-31 17:00 UTC · 17 symbols · 2000-01-03 to 2026-10-30 · split 2015-01-01 · 42 setup×exit tests (Bonferroni-adjusted) · engine v1.3.3_

## P1 · Exits × setups (R per trade, after costs)

Random-entry control (same stops and exits), mean expectancy by exit: X1_time10 +0.004R, X2_target2R +0.074R, X3_target3R +0.114R, X4_trendline_trail -0.005R, X5_chandelier3atr +0.053R, X6_partial1R_then_line -0.019R, X7_stage_drop +0.001R

| setup | exit | n | win_rate | avg_win | avg_loss | expectancy | median | exp_w10 | ci_low | ci_low_adj | exp_early | exp_late | exp_symA | exp_symB | random_mean | random_p95 | avg_bars | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 137 | 0.453 | 2.100 | -1.016 | 0.394 | -1.010 | 0.394 | 0.103 | -0.058 | 0.330 | 0.474 | 0.466 | 0.313 | 0.114 | 0.363 | 28.839 | PROMISING (not significant after correction) |
| E4_anchor_reclaim | X3_target3R | 890 | 0.509 | 1.552 | -0.953 | 0.322 | 0.057 | 0.322 | 0.229 | 0.159 | 0.213 | 0.441 | 0.297 | 0.357 | 0.114 | 0.208 | 40.707 | ADOPT |
| E1_trigger_with_trend | X2_target2R | 137 | 0.489 | 1.707 | -1.007 | 0.320 | -0.312 | 0.320 | 0.080 | -0.056 | 0.272 | 0.379 | 0.332 | 0.306 | 0.074 | 0.285 | 22.723 | PROMISING (not significant after correction) |
| E1_trigger_with_trend | X1_time10 | 138 | 0.587 | 1.095 | -0.853 | 0.290 | 0.295 | 0.290 | 0.081 | -0.039 | 0.285 | 0.297 | 0.338 | 0.235 | 0.004 | 0.187 | 8.399 | PROMISING (not significant after correction) |
| E4_anchor_reclaim | X2_target2R | 891 | 0.519 | 1.381 | -0.952 | 0.258 | 0.135 | 0.258 | 0.172 | 0.122 | 0.200 | 0.320 | 0.246 | 0.274 | 0.074 | 0.154 | 36.635 | ADOPT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 697 | 0.389 | 1.806 | -0.760 | 0.238 | -0.391 | 0.232 | 0.116 | 0.037 | 0.113 | 0.411 | 0.319 | 0.137 | 0.053 | 0.163 | 21.812 | ADOPT |
| E1_trigger_with_trend | X5_chandelier3atr | 137 | 0.482 | 1.316 | -0.793 | 0.223 | -0.037 | 0.223 | 0.004 | -0.115 | 0.190 | 0.264 | 0.258 | 0.184 | 0.053 | 0.297 | 19.832 | REJECT |
| E5_score4 | X3_target3R | 1449 | 0.432 | 1.796 | -0.997 | 0.209 | -1.012 | 0.209 | 0.133 | 0.073 | 0.130 | 0.295 | 0.127 | 0.320 | 0.114 | 0.187 | 34.778 | ADOPT |
| E1b_trigger_counter_trend | X3_target3R | 673 | 0.401 | 2.040 | -1.020 | 0.208 | -1.009 | 0.208 | 0.082 | 0.014 | 0.107 | 0.344 | 0.306 | 0.085 | 0.114 | 0.227 | 28.819 | REJECT |
| E5_score4 | X2_target2R | 1538 | 0.462 | 1.567 | -1.000 | 0.187 | -0.895 | 0.187 | 0.119 | 0.078 | 0.123 | 0.254 | 0.154 | 0.229 | 0.074 | 0.135 | 29.655 | ADOPT |
| E4_anchor_reclaim | X5_chandelier3atr | 1026 | 0.452 | 1.077 | -0.577 | 0.171 | -0.131 | 0.171 | 0.097 | 0.055 | 0.129 | 0.216 | 0.171 | 0.171 | 0.053 | 0.144 | 23.683 | ADOPT |
| E4_anchor_reclaim | X7_stage_drop | 1148 | 0.383 | 1.251 | -0.508 | 0.166 | -0.211 | 0.161 | 0.093 | 0.060 | 0.152 | 0.181 | 0.165 | 0.167 | 0.001 | 0.067 | 23.988 | ADOPT |
| E3_stage2_transition | X3_target3R | 656 | 0.422 | 1.727 | -0.997 | 0.154 | -1.010 | 0.154 | 0.036 | -0.047 | 0.129 | 0.179 | 0.098 | 0.225 | 0.114 | 0.232 | 34.631 | REJECT |
| E4_anchor_reclaim | X4_trendline_trail | 1263 | 0.369 | 1.136 | -0.435 | 0.145 | -0.189 | 0.145 | 0.083 | 0.046 | 0.136 | 0.154 | 0.127 | 0.170 | -0.005 | 0.060 | 19.982 | ADOPT |
| E3_stage2_transition | X2_target2R | 660 | 0.445 | 1.532 | -0.998 | 0.129 | -1.008 | 0.129 | 0.027 | -0.045 | 0.102 | 0.159 | 0.092 | 0.177 | 0.074 | 0.163 | 30.644 | REJECT |
| E1b_trigger_counter_trend | X2_target2R | 676 | 0.428 | 1.655 | -1.025 | 0.120 | -1.008 | 0.120 | 0.017 | -0.054 | 0.014 | 0.266 | 0.162 | 0.069 | 0.074 | 0.162 | 24.300 | REJECT |
| E4_anchor_reclaim | X6_partial1R_then_line | 1264 | 0.411 | 0.892 | -0.442 | 0.106 | -0.160 | 0.106 | 0.060 | 0.031 | 0.095 | 0.118 | 0.101 | 0.114 | -0.019 | 0.024 | 19.681 | ADOPT |
| E5_score4 | X5_chandelier3atr | 1793 | 0.413 | 1.162 | -0.662 | 0.091 | -0.229 | 0.091 | 0.036 | 0.005 | 0.048 | 0.135 | 0.061 | 0.132 | 0.053 | 0.122 | 21.021 | REJECT |
| E1b_trigger_counter_trend | X1_time10 | 700 | 0.513 | 0.873 | -0.748 | 0.083 | 0.014 | 0.083 | 0.007 | -0.038 | -0.013 | 0.218 | 0.159 | -0.010 | 0.004 | 0.077 | 8.426 | UNSTABLE (fails a split half) |
| E5_score4 | X7_stage_drop | 1801 | 0.360 | 1.316 | -0.632 | 0.069 | -0.305 | 0.066 | 0.006 | -0.023 | 0.037 | 0.103 | 0.030 | 0.124 | 0.001 | 0.054 | 22.974 | PROMISING (not significant after correction) |
| E4_anchor_reclaim | X1_time10 | 1179 | 0.571 | 0.571 | -0.612 | 0.063 | 0.102 | 0.062 | 0.016 | -0.008 | 0.029 | 0.100 | 0.073 | 0.050 | 0.004 | 0.063 | 9.260 | PROMISING (not significant after correction) |
| E3_stage2_transition | X7_stage_drop | 799 | 0.335 | 1.237 | -0.543 | 0.054 | -0.298 | 0.044 | -0.032 | -0.076 | 0.040 | 0.070 | 0.026 | 0.091 | 0.001 | 0.079 | 18.831 | REJECT |
| E5_score4 | X4_trendline_trail | 1904 | 0.358 | 1.179 | -0.575 | 0.052 | -0.283 | 0.052 | 0.002 | -0.035 | 0.026 | 0.080 | 0.010 | 0.113 | -0.005 | 0.049 | 20.067 | PROMISING (not significant after correction) |
| E5_score4 | X1_time10 | 2124 | 0.534 | 0.675 | -0.685 | 0.042 | 0.067 | 0.041 | 0.002 | -0.022 | -0.006 | 0.092 | 0.007 | 0.088 | 0.004 | 0.048 | 8.919 | REJECT |
| E3_stage2_transition | X5_chandelier3atr | 738 | 0.392 | 1.168 | -0.701 | 0.031 | -0.303 | 0.022 | -0.054 | -0.107 | -0.014 | 0.079 | 0.001 | 0.071 | 0.053 | 0.161 | 21.795 | REJECT |
| E5_score4 | X6_partial1R_then_line | 1925 | 0.421 | 0.872 | -0.590 | 0.025 | -0.224 | 0.025 | -0.013 | -0.031 | 0.003 | 0.048 | -0.016 | 0.085 | -0.019 | 0.016 | 19.363 | UNSTABLE (fails a split half) |
| E1_trigger_with_trend | X7_stage_drop | 153 | 0.425 | 0.514 | -0.344 | 0.021 | -0.079 | 0.021 | -0.070 | -0.127 | -0.013 | 0.064 | 0.020 | 0.021 | 0.001 | 0.185 | 4.340 | REJECT |
| E1_trigger_with_trend | X4_trendline_trail | 153 | 0.425 | 0.506 | -0.343 | 0.018 | -0.079 | 0.018 | -0.074 | -0.126 | -0.019 | 0.065 | 0.024 | 0.011 | -0.005 | 0.177 | 4.078 | REJECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 753 | 0.499 | 0.335 | -0.320 | 0.007 | -0.002 | 0.007 | -0.025 | -0.049 | -0.024 | 0.051 | -0.001 | 0.017 | -0.005 | 0.071 | 2.297 | REJECT |
| E1b_trigger_counter_trend | X6_partial1R_then_line | 753 | 0.499 | 0.329 | -0.314 | 0.007 | -0.002 | 0.007 | -0.024 | -0.046 | -0.023 | 0.049 | -0.003 | 0.019 | -0.019 | 0.034 | 2.297 | REJECT |
| E1b_trigger_counter_trend | X7_stage_drop | 753 | 0.498 | 0.335 | -0.320 | 0.006 | -0.002 | 0.006 | -0.027 | -0.050 | -0.024 | 0.048 | -0.003 | 0.016 | 0.001 | 0.086 | 2.340 | REJECT |
| E1_trigger_with_trend | X6_partial1R_then_line | 153 | 0.425 | 0.457 | -0.343 | -0.003 | -0.079 | -0.003 | -0.083 | -0.131 | -0.032 | 0.035 | -0.003 | -0.003 | -0.019 | 0.106 | 4.078 | REJECT |
| E3_stage2_transition | X4_trendline_trail | 799 | 0.315 | 0.867 | -0.411 | -0.008 | -0.241 | -0.016 | -0.075 | -0.118 | -0.022 | 0.007 | -0.019 | 0.006 | -0.005 | 0.076 | 13.452 | REJECT |
| E3_stage2_transition | X6_partial1R_then_line | 799 | 0.337 | 0.733 | -0.408 | -0.024 | -0.227 | -0.024 | -0.075 | -0.107 | -0.042 | -0.004 | -0.035 | -0.010 | -0.019 | 0.031 | 13.358 | REJECT |
| E2_exhaustion_confluence | X7_stage_drop | 337 | 0.487 | 0.501 | -0.529 | -0.028 | -0.008 | -0.028 | -0.107 | -0.144 | -0.000 | -0.056 | -0.026 | -0.030 | 0.001 | 0.126 | 2.457 | REJECT |
| E2_exhaustion_confluence | X4_trendline_trail | 337 | 0.490 | 0.480 | -0.532 | -0.036 | -0.007 | -0.036 | -0.113 | -0.157 | -0.017 | -0.056 | -0.042 | -0.026 | -0.005 | 0.112 | 2.288 | REJECT |
| E2_exhaustion_confluence | X6_partial1R_then_line | 337 | 0.496 | 0.449 | -0.517 | -0.039 | -0.001 | -0.039 | -0.110 | -0.144 | -0.021 | -0.057 | -0.054 | -0.013 | -0.019 | 0.059 | 2.288 | REJECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 337 | 0.258 | 2.623 | -0.981 | -0.051 | -1.023 | -0.051 | -0.245 | -0.390 | -0.289 | 0.198 | -0.104 | 0.037 | 0.053 | 0.209 | 14.303 | REJECT |
| E3_stage2_transition | X1_time10 | 771 | 0.484 | 0.559 | -0.687 | -0.084 | -0.034 | -0.084 | -0.135 | -0.171 | -0.114 | -0.051 | -0.102 | -0.059 | 0.004 | 0.075 | 8.869 | REJECT |
| E2_exhaustion_confluence | X3_target3R | 333 | 0.264 | 2.620 | -1.090 | -0.109 | -1.031 | -0.109 | -0.285 | -0.404 | -0.261 | 0.045 | -0.134 | -0.070 | 0.114 | 0.267 | 14.748 | REJECT |
| E2_exhaustion_confluence | X2_target2R | 334 | 0.314 | 1.920 | -1.082 | -0.138 | -1.028 | -0.138 | -0.290 | -0.395 | -0.280 | 0.007 | -0.146 | -0.125 | 0.074 | 0.191 | 11.180 | REJECT |
| E2_exhaustion_confluence | X1_time10 | 337 | 0.356 | 1.298 | -1.013 | -0.190 | -1.021 | -0.190 | -0.330 | -0.398 | -0.355 | -0.019 | -0.202 | -0.171 | 0.004 | 0.117 | 6.537 | REJECT |

### Exit rules ranked (trade-weighted across setups)

| exit | trades | mean_expectancy | random_mean | edge_over_random |
|---|---|---|---|---|
| X3_target3R | 4,138 | 0.205 | 0.114 | 0.091 |
| X2_target2R | 4,236 | 0.161 | 0.074 | 0.087 |
| X5_chandelier3atr | 4,728 | 0.114 | 0.053 | 0.061 |
| X7_stage_drop | 4,991 | 0.071 | 0.001 | 0.071 |
| X4_trendline_trail | 5,209 | 0.052 | -0.005 | 0.058 |
| X6_partial1R_then_line | 5,231 | 0.030 | -0.019 | 0.048 |
| X1_time10 | 5,249 | 0.025 | 0.004 | 0.021 |

## P1b · Sizing (fixed-fractional, max open positions = 5)

| setup | exit | risk_pct | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 0.005 | 0.010 | -0.047 | 0.220 | 130,814 |
| E1_trigger_with_trend | X3_target3R | 0.010 | 0.020 | -0.091 | 0.217 | 167,450 |
| E1_trigger_with_trend | X3_target3R | 0.020 | 0.037 | -0.176 | 0.210 | 258,625 |
| E4_anchor_reclaim | X3_target3R | 0.005 | 0.028 | -0.121 | 0.229 | 208,596 |
| E4_anchor_reclaim | X3_target3R | 0.010 | 0.053 | -0.229 | 0.233 | 403,306 |
| E4_anchor_reclaim | X3_target3R | 0.020 | 0.098 | -0.427 | 0.229 | 1,224,503 |
| E1_trigger_with_trend | X2_target2R | 0.005 | 0.008 | -0.033 | 0.235 | 122,578 |
| E1_trigger_with_trend | X2_target2R | 0.010 | 0.015 | -0.066 | 0.229 | 148,083 |
| E1_trigger_with_trend | X2_target2R | 0.020 | 0.028 | -0.128 | 0.219 | 207,417 |

## P2 · Market regime (SPY > 200-day average and Trend line rising)

| setup | exit | n_on | exp_on | n_off | exp_off | diff | diff_ci_low | verdict |
|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X4_trendline_trail | 46 | 0.027 | 107 | 0.014 | 0.012 | -0.288 | NO CLEAR EFFECT |
| E1_trigger_with_trend | X5_chandelier3atr | 40 | -0.032 | 97 | 0.328 | -0.360 | -0.994 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 71 | 0.018 | 682 | 0.006 | 0.011 | -0.127 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 63 | 0.104 | 634 | 0.251 | -0.147 | -0.707 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X4_trendline_trail | 29 | -0.127 | 308 | -0.028 | -0.099 | -0.388 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 29 | -0.159 | 308 | -0.040 | -0.118 | -1.062 | NO CLEAR EFFECT |
| E3_stage2_transition | X4_trendline_trail | 476 | 0.063 | 323 | -0.112 | 0.175 | 0.003 | FILTER HELPS |
| E3_stage2_transition | X5_chandelier3atr | 447 | 0.082 | 291 | -0.048 | 0.130 | -0.116 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X4_trendline_trail | 848 | 0.159 | 415 | 0.117 | 0.042 | -0.137 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X5_chandelier3atr | 696 | 0.205 | 330 | 0.099 | 0.106 | -0.087 | NO CLEAR EFFECT |
| E5_score4 | X4_trendline_trail | 1373 | 0.058 | 531 | 0.039 | 0.019 | -0.150 | NO CLEAR EFFECT |
| E5_score4 | X5_chandelier3atr | 1321 | 0.086 | 472 | 0.103 | -0.017 | -0.209 | NO CLEAR EFFECT |

## P4 · Portfolio heat (E1_trigger_with_trend + X3_target3R)

| rule | cagr | max_dd | mar | final |
|---|---|---|---|---|
| No sector cap | 0.015 | -0.069 | 0.219 | 148,396 |
| Max 1 open per sector | 0.015 | -0.069 | 0.219 | 148,396 |

## P6 · Playbook portfolio (E4_anchor_reclaim + E1_trigger_with_trend, exit X3_target3R, 1 per symbol, 1 per sector, max 5 open)

| risk | trades | trades_per_year | expectancy | win_rate | longest_losing_streak | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|---|---|---|
| 0.50% | 947 | 35.331 | 0.350 | 0.505 | 28 | 0.033 | -0.122 | 0.268 | 236,734 |
| 0.75% | 947 | 35.331 | 0.350 | 0.505 | 28 | 0.048 | -0.178 | 0.270 | 352,562 |
| 1.00% | 947 | 35.331 | 0.350 | 0.505 | 28 | 0.063 | -0.231 | 0.272 | 514,369 |

---
**How to read verdicts.** ADOPT = ≥ min trades, bootstrap CI above 0 after correcting for the number of tests, positive in both time halves and both symbol halves, and better than random entries with the same exits. PROMISING = everything except significance. UNSTABLE = fails a half. REJECT = not positive or not better than random.