# IFI Lab results: daily · etfs
_Run 2026-11-14 17:47 UTC · 17 symbols · 2000-01-03 to 2026-11-13 · split 2015-01-01 · 42 setup×exit tests (Bonferroni-adjusted) · engine v1.3.3_

## P1 · Exits × setups (R per trade, after costs)

Random-entry control (same stops and exits), mean expectancy by exit: X1_time10 +0.024R, X2_target2R +0.090R, X3_target3R +0.119R, X4_trendline_trail +0.009R, X5_chandelier3atr +0.083R, X6_partial1R_then_line -0.002R, X7_stage_drop +0.010R

| setup | exit | n | win_rate | avg_win | avg_loss | expectancy | median | exp_w10 | ci_low | ci_low_adj | exp_early | exp_late | exp_symA | exp_symB | random_mean | random_p95 | avg_bars | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 138 | 0.449 | 2.130 | -1.006 | 0.403 | -1.009 | 0.403 | 0.125 | -0.009 | 0.330 | 0.492 | 0.475 | 0.322 | 0.119 | 0.367 | 28.746 | PROMISING (not significant after correction) |
| E4_anchor_reclaim | X3_target3R | 893 | 0.510 | 1.554 | -0.953 | 0.324 | 0.060 | 0.324 | 0.233 | 0.180 | 0.213 | 0.445 | 0.302 | 0.356 | 0.119 | 0.211 | 40.649 | ADOPT |
| E1_trigger_with_trend | X2_target2R | 138 | 0.486 | 1.704 | -0.997 | 0.315 | -0.282 | 0.315 | 0.080 | -0.052 | 0.272 | 0.366 | 0.332 | 0.294 | 0.090 | 0.294 | 22.645 | PROMISING (not significant after correction) |
| E1_trigger_with_trend | X1_time10 | 139 | 0.590 | 1.081 | -0.853 | 0.288 | 0.277 | 0.288 | 0.094 | -0.022 | 0.285 | 0.292 | 0.338 | 0.231 | 0.024 | 0.210 | 8.367 | PROMISING (not significant after correction) |
| E4_anchor_reclaim | X2_target2R | 894 | 0.519 | 1.384 | -0.952 | 0.260 | 0.138 | 0.260 | 0.176 | 0.122 | 0.200 | 0.326 | 0.251 | 0.273 | 0.090 | 0.167 | 36.584 | ADOPT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 699 | 0.388 | 1.823 | -0.758 | 0.243 | -0.390 | 0.238 | 0.107 | 0.046 | 0.113 | 0.422 | 0.322 | 0.145 | 0.083 | 0.196 | 21.827 | ADOPT |
| E1_trigger_with_trend | X5_chandelier3atr | 138 | 0.478 | 1.309 | -0.785 | 0.216 | -0.041 | 0.216 | 0.009 | -0.112 | 0.190 | 0.249 | 0.252 | 0.176 | 0.083 | 0.345 | 19.841 | REJECT |
| E5_score4 | X3_target3R | 1451 | 0.433 | 1.796 | -0.999 | 0.211 | -1.012 | 0.211 | 0.136 | 0.071 | 0.130 | 0.298 | 0.128 | 0.323 | 0.119 | 0.194 | 34.787 | ADOPT |
| E1b_trigger_counter_trend | X3_target3R | 675 | 0.401 | 2.038 | -1.018 | 0.209 | -1.009 | 0.209 | 0.085 | 0.005 | 0.107 | 0.346 | 0.307 | 0.087 | 0.119 | 0.227 | 28.781 | REJECT |
| E5_score4 | X2_target2R | 1540 | 0.463 | 1.569 | -1.001 | 0.188 | -0.962 | 0.188 | 0.122 | 0.086 | 0.123 | 0.258 | 0.155 | 0.233 | 0.090 | 0.147 | 29.666 | ADOPT |
| E4_anchor_reclaim | X5_chandelier3atr | 1029 | 0.453 | 1.075 | -0.578 | 0.171 | -0.131 | 0.171 | 0.103 | 0.071 | 0.129 | 0.216 | 0.172 | 0.169 | 0.083 | 0.175 | 23.662 | REJECT |
| E4_anchor_reclaim | X7_stage_drop | 1151 | 0.384 | 1.255 | -0.509 | 0.168 | -0.211 | 0.163 | 0.098 | 0.066 | 0.152 | 0.185 | 0.169 | 0.167 | 0.010 | 0.079 | 23.987 | ADOPT |
| E3_stage2_transition | X3_target3R | 656 | 0.422 | 1.727 | -0.998 | 0.153 | -1.010 | 0.153 | 0.035 | -0.047 | 0.129 | 0.178 | 0.098 | 0.223 | 0.119 | 0.228 | 34.646 | REJECT |
| E4_anchor_reclaim | X4_trendline_trail | 1266 | 0.370 | 1.139 | -0.435 | 0.146 | -0.189 | 0.146 | 0.086 | 0.052 | 0.136 | 0.158 | 0.130 | 0.170 | 0.009 | 0.071 | 19.987 | ADOPT |
| E3_stage2_transition | X2_target2R | 660 | 0.445 | 1.532 | -0.998 | 0.129 | -1.008 | 0.129 | 0.027 | -0.045 | 0.102 | 0.159 | 0.092 | 0.177 | 0.090 | 0.178 | 30.644 | REJECT |
| E1b_trigger_counter_trend | X2_target2R | 678 | 0.428 | 1.654 | -1.023 | 0.122 | -1.007 | 0.122 | 0.016 | -0.042 | 0.014 | 0.268 | 0.163 | 0.071 | 0.090 | 0.175 | 24.261 | REJECT |
| E4_anchor_reclaim | X6_partial1R_then_line | 1267 | 0.411 | 0.896 | -0.443 | 0.108 | -0.160 | 0.108 | 0.062 | 0.029 | 0.095 | 0.122 | 0.104 | 0.114 | -0.002 | 0.041 | 19.686 | ADOPT |
| E5_score4 | X5_chandelier3atr | 1795 | 0.413 | 1.161 | -0.663 | 0.090 | -0.230 | 0.090 | 0.033 | 0.002 | 0.048 | 0.134 | 0.060 | 0.132 | 0.083 | 0.152 | 21.028 | REJECT |
| E1b_trigger_counter_trend | X1_time10 | 702 | 0.513 | 0.873 | -0.747 | 0.084 | 0.014 | 0.084 | 0.009 | -0.047 | -0.013 | 0.220 | 0.159 | -0.007 | 0.024 | 0.105 | 8.420 | REJECT |
| E5_score4 | X7_stage_drop | 1803 | 0.361 | 1.318 | -0.633 | 0.070 | -0.305 | 0.067 | 0.010 | -0.019 | 0.037 | 0.106 | 0.030 | 0.127 | 0.010 | 0.063 | 22.994 | PROMISING (not significant after correction) |
| E4_anchor_reclaim | X1_time10 | 1182 | 0.571 | 0.573 | -0.613 | 0.064 | 0.103 | 0.064 | 0.019 | -0.004 | 0.029 | 0.102 | 0.075 | 0.049 | 0.024 | 0.088 | 9.261 | REJECT |
| E3_stage2_transition | X7_stage_drop | 799 | 0.335 | 1.237 | -0.543 | 0.054 | -0.310 | 0.044 | -0.033 | -0.076 | 0.040 | 0.069 | 0.026 | 0.091 | 0.010 | 0.089 | 18.839 | REJECT |
| E5_score4 | X4_trendline_trail | 1906 | 0.358 | 1.181 | -0.575 | 0.053 | -0.283 | 0.053 | 0.001 | -0.024 | 0.026 | 0.082 | 0.010 | 0.116 | 0.009 | 0.062 | 20.081 | REJECT |
| E5_score4 | X1_time10 | 2126 | 0.535 | 0.675 | -0.686 | 0.042 | 0.067 | 0.041 | 0.002 | -0.024 | -0.006 | 0.092 | 0.006 | 0.090 | 0.024 | 0.068 | 8.927 | REJECT |
| E3_stage2_transition | X5_chandelier3atr | 738 | 0.392 | 1.168 | -0.702 | 0.030 | -0.307 | 0.022 | -0.055 | -0.108 | -0.014 | 0.077 | 0.001 | 0.070 | 0.083 | 0.196 | 21.809 | REJECT |
| E5_score4 | X6_partial1R_then_line | 1927 | 0.421 | 0.874 | -0.591 | 0.026 | -0.224 | 0.026 | -0.013 | -0.034 | 0.003 | 0.050 | -0.017 | 0.087 | -0.002 | 0.034 | 19.374 | REJECT |
| E1_trigger_with_trend | X7_stage_drop | 154 | 0.429 | 0.511 | -0.344 | 0.023 | -0.079 | 0.023 | -0.075 | -0.110 | -0.013 | 0.068 | 0.020 | 0.026 | 0.010 | 0.209 | 4.325 | REJECT |
| E1_trigger_with_trend | X4_trendline_trail | 154 | 0.429 | 0.504 | -0.343 | 0.020 | -0.076 | 0.020 | -0.077 | -0.115 | -0.019 | 0.069 | 0.024 | 0.016 | 0.009 | 0.195 | 4.065 | REJECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 755 | 0.499 | 0.336 | -0.319 | 0.008 | -0.002 | 0.008 | -0.026 | -0.049 | -0.024 | 0.053 | -0.001 | 0.019 | 0.009 | 0.093 | 2.297 | REJECT |
| E1b_trigger_counter_trend | X6_partial1R_then_line | 755 | 0.499 | 0.330 | -0.314 | 0.008 | -0.002 | 0.008 | -0.026 | -0.045 | -0.023 | 0.050 | -0.003 | 0.021 | -0.002 | 0.050 | 2.297 | REJECT |
| E1b_trigger_counter_trend | X7_stage_drop | 755 | 0.498 | 0.336 | -0.320 | 0.007 | -0.002 | 0.007 | -0.027 | -0.052 | -0.024 | 0.050 | -0.003 | 0.018 | 0.010 | 0.089 | 2.339 | REJECT |
| E1_trigger_with_trend | X6_partial1R_then_line | 154 | 0.429 | 0.455 | -0.343 | -0.001 | -0.076 | -0.001 | -0.084 | -0.116 | -0.032 | 0.039 | -0.003 | 0.002 | -0.002 | 0.122 | 4.065 | REJECT |
| E3_stage2_transition | X4_trendline_trail | 799 | 0.315 | 0.867 | -0.412 | -0.008 | -0.249 | -0.016 | -0.076 | -0.118 | -0.022 | 0.006 | -0.019 | 0.005 | 0.009 | 0.092 | 13.454 | REJECT |
| E3_stage2_transition | X6_partial1R_then_line | 799 | 0.337 | 0.733 | -0.408 | -0.024 | -0.227 | -0.024 | -0.076 | -0.108 | -0.042 | -0.005 | -0.035 | -0.010 | -0.002 | 0.053 | 13.360 | REJECT |
| E2_exhaustion_confluence | X7_stage_drop | 337 | 0.487 | 0.501 | -0.529 | -0.028 | -0.008 | -0.028 | -0.107 | -0.144 | -0.000 | -0.056 | -0.026 | -0.030 | 0.010 | 0.141 | 2.457 | REJECT |
| E2_exhaustion_confluence | X4_trendline_trail | 337 | 0.490 | 0.480 | -0.532 | -0.036 | -0.007 | -0.036 | -0.113 | -0.157 | -0.017 | -0.056 | -0.042 | -0.026 | 0.009 | 0.133 | 2.288 | REJECT |
| E2_exhaustion_confluence | X6_partial1R_then_line | 337 | 0.496 | 0.449 | -0.517 | -0.039 | -0.001 | -0.039 | -0.110 | -0.144 | -0.021 | -0.057 | -0.054 | -0.013 | -0.002 | 0.085 | 2.288 | REJECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 337 | 0.258 | 2.633 | -0.981 | -0.048 | -1.023 | -0.048 | -0.244 | -0.385 | -0.289 | 0.204 | -0.099 | 0.037 | 0.083 | 0.245 | 14.332 | REJECT |
| E3_stage2_transition | X1_time10 | 771 | 0.484 | 0.559 | -0.687 | -0.084 | -0.034 | -0.084 | -0.135 | -0.171 | -0.114 | -0.051 | -0.102 | -0.059 | 0.024 | 0.098 | 8.879 | REJECT |
| E2_exhaustion_confluence | X3_target3R | 333 | 0.264 | 2.620 | -1.090 | -0.109 | -1.031 | -0.109 | -0.285 | -0.404 | -0.261 | 0.045 | -0.134 | -0.070 | 0.119 | 0.273 | 14.748 | REJECT |
| E2_exhaustion_confluence | X2_target2R | 334 | 0.314 | 1.920 | -1.082 | -0.138 | -1.028 | -0.138 | -0.290 | -0.395 | -0.280 | 0.007 | -0.146 | -0.125 | 0.090 | 0.207 | 11.180 | REJECT |
| E2_exhaustion_confluence | X1_time10 | 337 | 0.356 | 1.298 | -1.013 | -0.190 | -1.021 | -0.190 | -0.330 | -0.398 | -0.355 | -0.019 | -0.202 | -0.171 | 0.024 | 0.138 | 6.537 | REJECT |

### Exit rules ranked (trade-weighted across setups)

| exit | trades | mean_expectancy | random_mean | edge_over_random |
|---|---|---|---|---|
| X3_target3R | 4,146 | 0.206 | 0.119 | 0.088 |
| X2_target2R | 4,244 | 0.162 | 0.090 | 0.072 |
| X5_chandelier3atr | 4,736 | 0.115 | 0.083 | 0.032 |
| X7_stage_drop | 4,999 | 0.073 | 0.010 | 0.063 |
| X4_trendline_trail | 5,217 | 0.053 | 0.009 | 0.044 |
| X6_partial1R_then_line | 5,239 | 0.030 | -0.002 | 0.033 |
| X1_time10 | 5,257 | 0.026 | 0.024 | 0.002 |

## P1b · Sizing (fixed-fractional, max open positions = 5)

| setup | exit | risk_pct | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 0.005 | 0.011 | -0.047 | 0.226 | 131,814 |
| E1_trigger_with_trend | X3_target3R | 0.010 | 0.020 | -0.091 | 0.223 | 169,968 |
| E1_trigger_with_trend | X3_target3R | 0.020 | 0.038 | -0.176 | 0.216 | 266,146 |
| E4_anchor_reclaim | X3_target3R | 0.005 | 0.029 | -0.141 | 0.204 | 214,237 |
| E4_anchor_reclaim | X3_target3R | 0.010 | 0.055 | -0.273 | 0.203 | 425,208 |
| E4_anchor_reclaim | X3_target3R | 0.020 | 0.102 | -0.497 | 0.205 | 1,358,217 |
| E1_trigger_with_trend | X2_target2R | 0.005 | 0.008 | -0.033 | 0.232 | 122,316 |
| E1_trigger_with_trend | X2_target2R | 0.010 | 0.015 | -0.066 | 0.227 | 147,465 |
| E1_trigger_with_trend | X2_target2R | 0.020 | 0.028 | -0.128 | 0.217 | 205,757 |

## P2 · Market regime (SPY > 200-day average and Trend line rising)

| setup | exit | n_on | exp_on | n_off | exp_off | diff | diff_ci_low | verdict |
|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X4_trendline_trail | 46 | 0.027 | 108 | 0.017 | 0.009 | -0.280 | NO CLEAR EFFECT |
| E1_trigger_with_trend | X5_chandelier3atr | 40 | -0.050 | 98 | 0.325 | -0.375 | -1.033 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 71 | 0.018 | 684 | 0.007 | 0.011 | -0.131 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 63 | 0.155 | 636 | 0.252 | -0.097 | -0.663 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X4_trendline_trail | 29 | -0.127 | 308 | -0.028 | -0.099 | -0.388 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 29 | -0.127 | 308 | -0.040 | -0.086 | -1.062 | NO CLEAR EFFECT |
| E3_stage2_transition | X4_trendline_trail | 476 | 0.062 | 323 | -0.112 | 0.175 | 0.002 | FILTER HELPS |
| E3_stage2_transition | X5_chandelier3atr | 447 | 0.081 | 291 | -0.048 | 0.129 | -0.118 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X4_trendline_trail | 848 | 0.160 | 418 | 0.119 | 0.041 | -0.138 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X5_chandelier3atr | 696 | 0.205 | 333 | 0.099 | 0.106 | -0.090 | NO CLEAR EFFECT |
| E5_score4 | X4_trendline_trail | 1373 | 0.057 | 533 | 0.044 | 0.013 | -0.149 | NO CLEAR EFFECT |
| E5_score4 | X5_chandelier3atr | 1321 | 0.085 | 474 | 0.104 | -0.019 | -0.228 | NO CLEAR EFFECT |

## P4 · Portfolio heat (E1_trigger_with_trend + X3_target3R)

| rule | cagr | max_dd | mar | final |
|---|---|---|---|---|
| No sector cap | 0.016 | -0.069 | 0.225 | 150,084 |
| Max 1 open per sector | 0.016 | -0.069 | 0.225 | 150,084 |

## P6 · Playbook portfolio (E4_anchor_reclaim + E1_trigger_with_trend, exit X3_target3R, 1 per symbol, 1 per sector, max 5 open)

| risk | trades | trades_per_year | expectancy | win_rate | longest_losing_streak | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|---|---|---|
| 0.50% | 950 | 35.392 | 0.354 | 0.505 | 28 | 0.034 | -0.122 | 0.278 | 244,764 |
| 0.75% | 950 | 35.392 | 0.354 | 0.505 | 28 | 0.050 | -0.178 | 0.281 | 370,426 |
| 1.00% | 950 | 35.392 | 0.354 | 0.505 | 28 | 0.065 | -0.231 | 0.283 | 548,971 |

---
**How to read verdicts.** ADOPT = ≥ min trades, bootstrap CI above 0 after correcting for the number of tests, positive in both time halves and both symbol halves, and better than random entries with the same exits. PROMISING = everything except significance. UNSTABLE = fails a half. REJECT = not positive or not better than random.