# IFI Lab results: daily · etfs
_Run 2026-11-07 17:37 UTC · 17 symbols · 2000-01-03 to 2026-11-06 · split 2015-01-01 · 42 setup×exit tests (Bonferroni-adjusted) · engine v1.3.3_

## P1 · Exits × setups (R per trade, after costs)

Random-entry control (same stops and exits), mean expectancy by exit: X1_time10 +0.049R, X2_target2R +0.112R, X3_target3R +0.161R, X4_trendline_trail +0.013R, X5_chandelier3atr +0.130R, X6_partial1R_then_line -0.004R, X7_stage_drop +0.020R

| setup | exit | n | win_rate | avg_win | avg_loss | expectancy | median | exp_w10 | ci_low | ci_low_adj | exp_early | exp_late | exp_symA | exp_symB | random_mean | random_p95 | avg_bars | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 137 | 0.445 | 2.164 | -1.004 | 0.406 | -1.010 | 0.406 | 0.113 | -0.049 | 0.330 | 0.502 | 0.475 | 0.328 | 0.161 | 0.403 | 28.905 | PROMISING (not significant after correction) |
| E4_anchor_reclaim | X3_target3R | 893 | 0.508 | 1.550 | -0.951 | 0.321 | 0.055 | 0.321 | 0.228 | 0.177 | 0.213 | 0.437 | 0.297 | 0.354 | 0.161 | 0.257 | 40.610 | ADOPT |
| E1_trigger_with_trend | X2_target2R | 137 | 0.482 | 1.729 | -0.995 | 0.318 | -0.312 | 0.318 | 0.078 | -0.060 | 0.272 | 0.374 | 0.332 | 0.301 | 0.112 | 0.327 | 22.759 | REJECT |
| E1_trigger_with_trend | X1_time10 | 138 | 0.587 | 1.094 | -0.853 | 0.290 | 0.295 | 0.290 | 0.079 | -0.039 | 0.285 | 0.296 | 0.338 | 0.234 | 0.049 | 0.234 | 8.413 | PROMISING (not significant after correction) |
| E4_anchor_reclaim | X2_target2R | 894 | 0.518 | 1.382 | -0.950 | 0.257 | 0.132 | 0.257 | 0.173 | 0.121 | 0.200 | 0.319 | 0.248 | 0.271 | 0.112 | 0.197 | 36.550 | ADOPT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 698 | 0.388 | 1.812 | -0.759 | 0.239 | -0.391 | 0.234 | 0.111 | 0.019 | 0.113 | 0.414 | 0.318 | 0.142 | 0.130 | 0.242 | 21.825 | REJECT |
| E1_trigger_with_trend | X5_chandelier3atr | 137 | 0.474 | 1.329 | -0.783 | 0.219 | -0.045 | 0.219 | 0.001 | -0.122 | 0.190 | 0.255 | 0.252 | 0.181 | 0.130 | 0.377 | 19.934 | REJECT |
| E5_score4 | X3_target3R | 1451 | 0.432 | 1.793 | -0.998 | 0.208 | -1.012 | 0.208 | 0.133 | 0.069 | 0.130 | 0.292 | 0.125 | 0.320 | 0.161 | 0.237 | 34.759 | REJECT |
| E1b_trigger_counter_trend | X3_target3R | 674 | 0.401 | 2.042 | -1.019 | 0.207 | -1.009 | 0.207 | 0.077 | -0.008 | 0.107 | 0.343 | 0.305 | 0.086 | 0.161 | 0.272 | 28.797 | REJECT |
| E5_score4 | X2_target2R | 1540 | 0.462 | 1.567 | -1.000 | 0.187 | -0.962 | 0.187 | 0.120 | 0.083 | 0.123 | 0.254 | 0.152 | 0.232 | 0.112 | 0.173 | 29.643 | ADOPT |
| E4_anchor_reclaim | X5_chandelier3atr | 1029 | 0.453 | 1.073 | -0.578 | 0.170 | -0.131 | 0.170 | 0.102 | 0.070 | 0.129 | 0.214 | 0.171 | 0.168 | 0.130 | 0.220 | 23.647 | REJECT |
| E4_anchor_reclaim | X7_stage_drop | 1151 | 0.383 | 1.250 | -0.508 | 0.165 | -0.211 | 0.160 | 0.094 | 0.062 | 0.152 | 0.179 | 0.165 | 0.165 | 0.020 | 0.089 | 23.957 | ADOPT |
| E3_stage2_transition | X3_target3R | 656 | 0.422 | 1.727 | -0.997 | 0.153 | -1.010 | 0.153 | 0.036 | -0.047 | 0.129 | 0.178 | 0.098 | 0.224 | 0.161 | 0.271 | 34.639 | REJECT |
| E4_anchor_reclaim | X4_trendline_trail | 1266 | 0.369 | 1.135 | -0.435 | 0.144 | -0.189 | 0.144 | 0.083 | 0.050 | 0.136 | 0.153 | 0.127 | 0.168 | 0.013 | 0.079 | 19.963 | ADOPT |
| E3_stage2_transition | X2_target2R | 660 | 0.445 | 1.532 | -0.998 | 0.129 | -1.008 | 0.129 | 0.027 | -0.045 | 0.102 | 0.159 | 0.092 | 0.177 | 0.112 | 0.198 | 30.644 | REJECT |
| E1b_trigger_counter_trend | X2_target2R | 677 | 0.427 | 1.656 | -1.024 | 0.120 | -1.008 | 0.120 | 0.017 | -0.054 | 0.014 | 0.265 | 0.162 | 0.069 | 0.112 | 0.197 | 24.278 | REJECT |
| E4_anchor_reclaim | X6_partial1R_then_line | 1267 | 0.411 | 0.892 | -0.443 | 0.106 | -0.160 | 0.106 | 0.060 | 0.026 | 0.095 | 0.119 | 0.102 | 0.113 | -0.004 | 0.037 | 19.662 | ADOPT |
| E5_score4 | X5_chandelier3atr | 1795 | 0.413 | 1.159 | -0.663 | 0.089 | -0.230 | 0.089 | 0.032 | 0.001 | 0.048 | 0.133 | 0.059 | 0.132 | 0.130 | 0.197 | 21.019 | REJECT |
| E1b_trigger_counter_trend | X1_time10 | 701 | 0.514 | 0.871 | -0.748 | 0.083 | 0.016 | 0.083 | 0.001 | -0.046 | -0.013 | 0.218 | 0.159 | -0.009 | 0.049 | 0.132 | 8.421 | REJECT |
| E5_score4 | X7_stage_drop | 1803 | 0.360 | 1.314 | -0.632 | 0.068 | -0.305 | 0.065 | 0.006 | -0.020 | 0.037 | 0.102 | 0.028 | 0.125 | 0.020 | 0.071 | 22.972 | REJECT |
| E4_anchor_reclaim | X1_time10 | 1182 | 0.571 | 0.572 | -0.613 | 0.063 | 0.103 | 0.063 | 0.018 | -0.006 | 0.029 | 0.100 | 0.074 | 0.048 | 0.049 | 0.111 | 9.254 | REJECT |
| E3_stage2_transition | X7_stage_drop | 799 | 0.335 | 1.237 | -0.544 | 0.054 | -0.310 | 0.044 | -0.033 | -0.076 | 0.040 | 0.069 | 0.026 | 0.090 | 0.020 | 0.094 | 18.837 | REJECT |
| E5_score4 | X4_trendline_trail | 1906 | 0.357 | 1.178 | -0.575 | 0.052 | -0.283 | 0.052 | -0.001 | -0.025 | 0.026 | 0.078 | 0.008 | 0.114 | 0.013 | 0.070 | 20.065 | REJECT |
| E5_score4 | X1_time10 | 2126 | 0.535 | 0.674 | -0.686 | 0.041 | 0.067 | 0.041 | 0.002 | -0.025 | -0.006 | 0.092 | 0.006 | 0.089 | 0.049 | 0.098 | 8.922 | REJECT |
| E3_stage2_transition | X5_chandelier3atr | 738 | 0.392 | 1.168 | -0.702 | 0.031 | -0.307 | 0.022 | -0.055 | -0.108 | -0.014 | 0.078 | 0.001 | 0.070 | 0.130 | 0.240 | 21.802 | REJECT |
| E5_score4 | X6_partial1R_then_line | 1927 | 0.421 | 0.872 | -0.591 | 0.025 | -0.224 | 0.025 | -0.014 | -0.035 | 0.003 | 0.048 | -0.018 | 0.086 | -0.004 | 0.030 | 19.361 | REJECT |
| E1_trigger_with_trend | X7_stage_drop | 153 | 0.425 | 0.514 | -0.344 | 0.021 | -0.079 | 0.021 | -0.070 | -0.127 | -0.013 | 0.064 | 0.020 | 0.021 | 0.020 | 0.223 | 4.340 | REJECT |
| E1_trigger_with_trend | X4_trendline_trail | 153 | 0.425 | 0.506 | -0.343 | 0.018 | -0.079 | 0.018 | -0.074 | -0.126 | -0.019 | 0.065 | 0.024 | 0.011 | 0.013 | 0.198 | 4.078 | REJECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 754 | 0.500 | 0.336 | -0.320 | 0.008 | -0.001 | 0.008 | -0.027 | -0.049 | -0.024 | 0.053 | -0.001 | 0.020 | 0.013 | 0.098 | 2.297 | REJECT |
| E1b_trigger_counter_trend | X6_partial1R_then_line | 754 | 0.500 | 0.330 | -0.314 | 0.008 | -0.001 | 0.008 | -0.025 | -0.047 | -0.023 | 0.051 | -0.003 | 0.022 | -0.004 | 0.054 | 2.297 | REJECT |
| E1b_trigger_counter_trend | X7_stage_drop | 754 | 0.499 | 0.336 | -0.320 | 0.007 | -0.002 | 0.007 | -0.028 | -0.049 | -0.024 | 0.050 | -0.003 | 0.018 | 0.020 | 0.103 | 2.340 | REJECT |
| E1_trigger_with_trend | X6_partial1R_then_line | 153 | 0.425 | 0.457 | -0.343 | -0.003 | -0.079 | -0.003 | -0.083 | -0.131 | -0.032 | 0.035 | -0.003 | -0.003 | -0.004 | 0.113 | 4.078 | REJECT |
| E3_stage2_transition | X4_trendline_trail | 799 | 0.315 | 0.867 | -0.412 | -0.008 | -0.249 | -0.016 | -0.076 | -0.118 | -0.022 | 0.006 | -0.019 | 0.005 | 0.013 | 0.091 | 13.454 | REJECT |
| E3_stage2_transition | X6_partial1R_then_line | 799 | 0.337 | 0.733 | -0.408 | -0.024 | -0.227 | -0.024 | -0.076 | -0.108 | -0.042 | -0.005 | -0.035 | -0.010 | -0.004 | 0.050 | 13.360 | REJECT |
| E2_exhaustion_confluence | X7_stage_drop | 337 | 0.487 | 0.501 | -0.529 | -0.028 | -0.008 | -0.028 | -0.107 | -0.144 | -0.000 | -0.056 | -0.026 | -0.030 | 0.020 | 0.142 | 2.457 | REJECT |
| E2_exhaustion_confluence | X4_trendline_trail | 337 | 0.490 | 0.480 | -0.532 | -0.036 | -0.007 | -0.036 | -0.113 | -0.157 | -0.017 | -0.056 | -0.042 | -0.026 | 0.013 | 0.140 | 2.288 | REJECT |
| E2_exhaustion_confluence | X6_partial1R_then_line | 337 | 0.496 | 0.449 | -0.517 | -0.039 | -0.001 | -0.039 | -0.110 | -0.144 | -0.021 | -0.057 | -0.054 | -0.013 | -0.004 | 0.081 | 2.288 | REJECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 337 | 0.258 | 2.618 | -0.981 | -0.052 | -1.023 | -0.052 | -0.245 | -0.393 | -0.289 | 0.195 | -0.106 | 0.037 | 0.130 | 0.297 | 14.318 | REJECT |
| E3_stage2_transition | X1_time10 | 771 | 0.484 | 0.559 | -0.687 | -0.084 | -0.034 | -0.084 | -0.135 | -0.171 | -0.114 | -0.052 | -0.102 | -0.060 | 0.049 | 0.130 | 8.875 | REJECT |
| E2_exhaustion_confluence | X3_target3R | 333 | 0.264 | 2.620 | -1.090 | -0.109 | -1.031 | -0.109 | -0.285 | -0.404 | -0.261 | 0.045 | -0.134 | -0.070 | 0.161 | 0.311 | 14.748 | REJECT |
| E2_exhaustion_confluence | X2_target2R | 334 | 0.314 | 1.920 | -1.082 | -0.138 | -1.028 | -0.138 | -0.290 | -0.395 | -0.280 | 0.007 | -0.146 | -0.125 | 0.112 | 0.233 | 11.180 | REJECT |
| E2_exhaustion_confluence | X1_time10 | 337 | 0.356 | 1.298 | -1.013 | -0.190 | -1.021 | -0.190 | -0.330 | -0.398 | -0.355 | -0.019 | -0.202 | -0.171 | 0.049 | 0.173 | 6.537 | REJECT |

### Exit rules ranked (trade-weighted across setups)

| exit | trades | mean_expectancy | random_mean | edge_over_random |
|---|---|---|---|---|
| X3_target3R | 4,144 | 0.205 | 0.161 | 0.044 |
| X2_target2R | 4,242 | 0.161 | 0.112 | 0.049 |
| X5_chandelier3atr | 4,734 | 0.113 | 0.130 | -0.017 |
| X7_stage_drop | 4,997 | 0.071 | 0.020 | 0.051 |
| X4_trendline_trail | 5,215 | 0.052 | 0.013 | 0.039 |
| X6_partial1R_then_line | 5,237 | 0.030 | -0.004 | 0.033 |
| X1_time10 | 5,255 | 0.025 | 0.049 | -0.023 |

## P1b · Sizing (fixed-fractional, max open positions = 5)

| setup | exit | risk_pct | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 0.005 | 0.011 | -0.047 | 0.227 | 131,888 |
| E1_trigger_with_trend | X3_target3R | 0.010 | 0.020 | -0.091 | 0.223 | 170,150 |
| E1_trigger_with_trend | X3_target3R | 0.020 | 0.038 | -0.176 | 0.216 | 266,673 |
| E4_anchor_reclaim | X3_target3R | 0.005 | 0.028 | -0.141 | 0.200 | 211,580 |
| E4_anchor_reclaim | X3_target3R | 0.010 | 0.054 | -0.273 | 0.200 | 414,871 |
| E4_anchor_reclaim | X3_target3R | 0.020 | 0.100 | -0.497 | 0.201 | 1,294,740 |
| E1_trigger_with_trend | X2_target2R | 0.005 | 0.008 | -0.033 | 0.233 | 122,386 |
| E1_trigger_with_trend | X2_target2R | 0.010 | 0.015 | -0.066 | 0.228 | 147,628 |
| E1_trigger_with_trend | X2_target2R | 0.020 | 0.028 | -0.128 | 0.217 | 206,193 |

## P2 · Market regime (SPY > 200-day average and Trend line rising)

| setup | exit | n_on | exp_on | n_off | exp_off | diff | diff_ci_low | verdict |
|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X4_trendline_trail | 46 | 0.027 | 107 | 0.014 | 0.012 | -0.288 | NO CLEAR EFFECT |
| E1_trigger_with_trend | X5_chandelier3atr | 40 | -0.046 | 97 | 0.328 | -0.374 | -1.002 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 71 | 0.018 | 683 | 0.007 | 0.010 | -0.125 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 63 | 0.118 | 635 | 0.251 | -0.133 | -0.690 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X4_trendline_trail | 29 | -0.127 | 308 | -0.028 | -0.099 | -0.388 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 29 | -0.174 | 308 | -0.040 | -0.134 | -1.062 | NO CLEAR EFFECT |
| E3_stage2_transition | X4_trendline_trail | 476 | 0.062 | 323 | -0.112 | 0.175 | 0.002 | FILTER HELPS |
| E3_stage2_transition | X5_chandelier3atr | 447 | 0.082 | 291 | -0.048 | 0.130 | -0.117 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X4_trendline_trail | 848 | 0.158 | 418 | 0.116 | 0.043 | -0.135 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X5_chandelier3atr | 696 | 0.204 | 333 | 0.097 | 0.107 | -0.087 | NO CLEAR EFFECT |
| E5_score4 | X4_trendline_trail | 1373 | 0.056 | 533 | 0.040 | 0.016 | -0.147 | NO CLEAR EFFECT |
| E5_score4 | X5_chandelier3atr | 1321 | 0.085 | 474 | 0.102 | -0.017 | -0.227 | NO CLEAR EFFECT |

## P4 · Portfolio heat (E1_trigger_with_trend + X3_target3R)

| rule | cagr | max_dd | mar | final |
|---|---|---|---|---|
| No sector cap | 0.016 | -0.069 | 0.225 | 150,207 |
| Max 1 open per sector | 0.016 | -0.069 | 0.225 | 150,207 |

## P6 · Playbook portfolio (E4_anchor_reclaim + E1_trigger_with_trend, exit X3_target3R, 1 per symbol, 1 per sector, max 5 open)

| risk | trades | trades_per_year | expectancy | win_rate | longest_losing_streak | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|---|---|---|
| 0.50% | 949 | 35.380 | 0.352 | 0.505 | 28 | 0.035 | -0.122 | 0.286 | 251,364 |
| 0.75% | 949 | 35.380 | 0.352 | 0.505 | 28 | 0.052 | -0.178 | 0.289 | 385,171 |
| 1.00% | 949 | 35.380 | 0.352 | 0.505 | 28 | 0.068 | -0.231 | 0.292 | 577,659 |

---
**How to read verdicts.** ADOPT = ≥ min trades, bootstrap CI above 0 after correcting for the number of tests, positive in both time halves and both symbol halves, and better than random entries with the same exits. PROMISING = everything except significance. UNSTABLE = fails a half. REJECT = not positive or not better than random.