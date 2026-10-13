# IFI Lab results: daily · etfs
_Run 2026-10-13 17:00 UTC · 17 symbols · 2000-01-03 to 2026-10-13 · split 2015-01-01 · 42 setup×exit tests (Bonferroni-adjusted) · engine v1.3.3_

## P1 · Exits × setups (R per trade, after costs)

Random-entry control (same stops and exits), mean expectancy by exit: X1_time10 +0.025R, X2_target2R +0.093R, X3_target3R +0.138R, X4_trendline_trail +0.008R, X5_chandelier3atr +0.117R, X6_partial1R_then_line -0.013R, X7_stage_drop +0.019R

| setup | exit | n | win_rate | avg_win | avg_loss | expectancy | median | exp_w10 | ci_low | ci_low_adj | exp_early | exp_late | exp_symA | exp_symB | random_mean | random_p95 | avg_bars | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 135 | 0.452 | 2.123 | -1.011 | 0.405 | -1.008 | 0.405 | 0.122 | 0.025 | 0.330 | 0.502 | 0.451 | 0.351 | 0.138 | 0.392 | 28.844 | ADOPT |
| E4_anchor_reclaim | X3_target3R | 885 | 0.507 | 1.563 | -0.951 | 0.325 | 0.036 | 0.325 | 0.228 | 0.170 | 0.213 | 0.447 | 0.296 | 0.364 | 0.138 | 0.239 | 40.850 | ADOPT |
| E1_trigger_with_trend | X2_target2R | 135 | 0.489 | 1.692 | -1.001 | 0.315 | -0.312 | 0.315 | 0.074 | -0.042 | 0.272 | 0.371 | 0.322 | 0.308 | 0.093 | 0.290 | 22.822 | PROMISING (not significant after correction) |
| E1_trigger_with_trend | X1_time10 | 136 | 0.588 | 1.101 | -0.843 | 0.301 | 0.320 | 0.301 | 0.093 | -0.046 | 0.285 | 0.322 | 0.339 | 0.255 | 0.025 | 0.194 | 8.375 | PROMISING (not significant after correction) |
| E4_anchor_reclaim | X2_target2R | 886 | 0.517 | 1.390 | -0.950 | 0.260 | 0.112 | 0.260 | 0.176 | 0.113 | 0.200 | 0.325 | 0.245 | 0.281 | 0.093 | 0.169 | 36.755 | ADOPT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 696 | 0.386 | 1.787 | -0.758 | 0.225 | -0.394 | 0.220 | 0.100 | 0.040 | 0.113 | 0.383 | 0.303 | 0.130 | 0.117 | 0.236 | 21.739 | REJECT |
| E1_trigger_with_trend | X5_chandelier3atr | 135 | 0.481 | 1.295 | -0.784 | 0.217 | -0.037 | 0.217 | 0.017 | -0.109 | 0.190 | 0.252 | 0.243 | 0.187 | 0.117 | 0.392 | 19.837 | REJECT |
| E5_score4 | X3_target3R | 1442 | 0.432 | 1.800 | -0.996 | 0.212 | -1.012 | 0.212 | 0.131 | 0.086 | 0.130 | 0.301 | 0.127 | 0.326 | 0.138 | 0.208 | 34.868 | ADOPT |
| E1b_trigger_counter_trend | X3_target3R | 672 | 0.399 | 2.024 | -1.018 | 0.195 | -1.009 | 0.195 | 0.070 | -0.017 | 0.107 | 0.315 | 0.290 | 0.078 | 0.138 | 0.255 | 28.771 | REJECT |
| E5_score4 | X2_target2R | 1531 | 0.462 | 1.571 | -0.999 | 0.189 | -0.869 | 0.189 | 0.122 | 0.071 | 0.123 | 0.260 | 0.155 | 0.235 | 0.093 | 0.152 | 29.720 | ADOPT |
| E4_anchor_reclaim | X5_chandelier3atr | 1021 | 0.450 | 1.085 | -0.577 | 0.170 | -0.138 | 0.170 | 0.101 | 0.060 | 0.129 | 0.216 | 0.170 | 0.171 | 0.117 | 0.218 | 23.757 | REJECT |
| E4_anchor_reclaim | X7_stage_drop | 1143 | 0.382 | 1.258 | -0.509 | 0.167 | -0.212 | 0.161 | 0.094 | 0.043 | 0.152 | 0.182 | 0.164 | 0.170 | 0.019 | 0.096 | 24.051 | ADOPT |
| E3_stage2_transition | X3_target3R | 655 | 0.424 | 1.722 | -0.996 | 0.158 | -1.010 | 0.158 | 0.036 | -0.032 | 0.129 | 0.188 | 0.098 | 0.235 | 0.138 | 0.253 | 34.656 | REJECT |
| E4_anchor_reclaim | X4_trendline_trail | 1258 | 0.368 | 1.142 | -0.435 | 0.145 | -0.190 | 0.145 | 0.084 | 0.041 | 0.136 | 0.155 | 0.126 | 0.173 | 0.008 | 0.075 | 20.025 | ADOPT |
| E3_stage2_transition | X2_target2R | 660 | 0.445 | 1.533 | -0.994 | 0.132 | -1.008 | 0.132 | 0.030 | -0.046 | 0.102 | 0.164 | 0.092 | 0.182 | 0.093 | 0.178 | 30.602 | REJECT |
| E1b_trigger_counter_trend | X2_target2R | 675 | 0.425 | 1.650 | -1.023 | 0.114 | -1.008 | 0.114 | 0.004 | -0.052 | 0.014 | 0.251 | 0.150 | 0.069 | 0.093 | 0.181 | 24.292 | REJECT |
| E4_anchor_reclaim | X6_partial1R_then_line | 1259 | 0.408 | 0.899 | -0.442 | 0.106 | -0.162 | 0.106 | 0.059 | 0.031 | 0.095 | 0.117 | 0.099 | 0.115 | -0.013 | 0.034 | 19.724 | ADOPT |
| E5_score4 | X5_chandelier3atr | 1785 | 0.412 | 1.167 | -0.662 | 0.091 | -0.230 | 0.091 | 0.039 | 0.009 | 0.048 | 0.136 | 0.060 | 0.134 | 0.117 | 0.200 | 21.082 | REJECT |
| E1b_trigger_counter_trend | X1_time10 | 699 | 0.511 | 0.869 | -0.746 | 0.079 | 0.010 | 0.079 | -0.003 | -0.039 | -0.013 | 0.208 | 0.152 | -0.011 | 0.025 | 0.107 | 8.405 | REJECT |
| E5_score4 | X7_stage_drop | 1793 | 0.360 | 1.320 | -0.633 | 0.070 | -0.307 | 0.066 | 0.010 | -0.023 | 0.037 | 0.105 | 0.029 | 0.128 | 0.019 | 0.080 | 23.042 | REJECT |
| E4_anchor_reclaim | X1_time10 | 1174 | 0.570 | 0.572 | -0.613 | 0.062 | 0.101 | 0.062 | 0.017 | -0.020 | 0.029 | 0.098 | 0.071 | 0.049 | 0.025 | 0.088 | 9.265 | REJECT |
| E3_stage2_transition | X7_stage_drop | 798 | 0.336 | 1.237 | -0.544 | 0.054 | -0.304 | 0.044 | -0.035 | -0.093 | 0.040 | 0.070 | 0.026 | 0.092 | 0.019 | 0.113 | 18.852 | REJECT |
| E5_score4 | X4_trendline_trail | 1896 | 0.358 | 1.182 | -0.575 | 0.053 | -0.283 | 0.053 | 0.001 | -0.026 | 0.026 | 0.082 | 0.009 | 0.116 | 0.008 | 0.061 | 20.122 | REJECT |
| E5_score4 | X1_time10 | 2116 | 0.534 | 0.675 | -0.686 | 0.042 | 0.066 | 0.041 | 0.001 | -0.018 | -0.006 | 0.092 | 0.006 | 0.090 | 0.025 | 0.072 | 8.925 | REJECT |
| E1_trigger_with_trend | X7_stage_drop | 150 | 0.433 | 0.514 | -0.335 | 0.033 | -0.076 | 0.033 | -0.064 | -0.103 | -0.013 | 0.094 | 0.032 | 0.034 | 0.019 | 0.217 | 4.387 | REJECT |
| E3_stage2_transition | X5_chandelier3atr | 737 | 0.392 | 1.168 | -0.702 | 0.031 | -0.306 | 0.023 | -0.050 | -0.121 | -0.014 | 0.079 | 0.001 | 0.072 | 0.117 | 0.232 | 21.822 | REJECT |
| E1_trigger_with_trend | X4_trendline_trail | 150 | 0.433 | 0.506 | -0.334 | 0.030 | -0.072 | 0.030 | -0.066 | -0.107 | -0.019 | 0.095 | 0.035 | 0.023 | 0.008 | 0.220 | 4.120 | REJECT |
| E5_score4 | X6_partial1R_then_line | 1917 | 0.420 | 0.875 | -0.590 | 0.025 | -0.226 | 0.025 | -0.014 | -0.038 | 0.003 | 0.049 | -0.018 | 0.087 | -0.013 | 0.026 | 19.415 | REJECT |
| E1_trigger_with_trend | X6_partial1R_then_line | 150 | 0.433 | 0.457 | -0.334 | 0.009 | -0.072 | 0.009 | -0.073 | -0.115 | -0.032 | 0.063 | 0.008 | 0.009 | -0.013 | 0.115 | 4.120 | REJECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 752 | 0.500 | 0.335 | -0.320 | 0.007 | -0.001 | 0.007 | -0.025 | -0.043 | -0.024 | 0.052 | -0.001 | 0.017 | 0.008 | 0.092 | 2.298 | REJECT |
| E1b_trigger_counter_trend | X6_partial1R_then_line | 752 | 0.500 | 0.329 | -0.315 | 0.007 | -0.001 | 0.007 | -0.024 | -0.041 | -0.023 | 0.050 | -0.003 | 0.019 | -0.013 | 0.047 | 2.298 | REJECT |
| E1b_trigger_counter_trend | X7_stage_drop | 752 | 0.499 | 0.335 | -0.321 | 0.006 | -0.002 | 0.006 | -0.027 | -0.045 | -0.024 | 0.049 | -0.002 | 0.016 | 0.019 | 0.116 | 2.340 | REJECT |
| E3_stage2_transition | X4_trendline_trail | 798 | 0.316 | 0.867 | -0.412 | -0.008 | -0.245 | -0.016 | -0.077 | -0.118 | -0.022 | 0.007 | -0.019 | 0.007 | 0.008 | 0.092 | 13.466 | REJECT |
| E3_stage2_transition | X6_partial1R_then_line | 798 | 0.337 | 0.733 | -0.408 | -0.024 | -0.227 | -0.024 | -0.073 | -0.106 | -0.042 | -0.004 | -0.035 | -0.009 | -0.013 | 0.046 | 13.372 | REJECT |
| E2_exhaustion_confluence | X7_stage_drop | 337 | 0.487 | 0.501 | -0.529 | -0.028 | -0.008 | -0.028 | -0.107 | -0.144 | -0.000 | -0.056 | -0.026 | -0.030 | 0.019 | 0.167 | 2.457 | REJECT |
| E2_exhaustion_confluence | X4_trendline_trail | 337 | 0.490 | 0.480 | -0.532 | -0.036 | -0.007 | -0.036 | -0.113 | -0.157 | -0.017 | -0.056 | -0.042 | -0.026 | 0.008 | 0.148 | 2.288 | REJECT |
| E2_exhaustion_confluence | X6_partial1R_then_line | 337 | 0.496 | 0.449 | -0.517 | -0.039 | -0.001 | -0.039 | -0.110 | -0.144 | -0.021 | -0.057 | -0.054 | -0.013 | -0.013 | 0.081 | 2.288 | REJECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 337 | 0.258 | 2.593 | -0.981 | -0.058 | -1.023 | -0.058 | -0.251 | -0.402 | -0.289 | 0.182 | -0.116 | 0.037 | 0.117 | 0.300 | 14.264 | REJECT |
| E3_stage2_transition | X1_time10 | 770 | 0.484 | 0.559 | -0.688 | -0.084 | -0.033 | -0.084 | -0.139 | -0.170 | -0.114 | -0.051 | -0.102 | -0.059 | 0.025 | 0.102 | 8.878 | REJECT |
| E2_exhaustion_confluence | X3_target3R | 333 | 0.264 | 2.631 | -1.090 | -0.106 | -1.031 | -0.106 | -0.281 | -0.403 | -0.261 | 0.051 | -0.134 | -0.062 | 0.138 | 0.290 | 14.724 | REJECT |
| E2_exhaustion_confluence | X2_target2R | 334 | 0.314 | 1.930 | -1.082 | -0.135 | -1.028 | -0.135 | -0.289 | -0.395 | -0.280 | 0.013 | -0.146 | -0.117 | 0.093 | 0.217 | 11.156 | REJECT |
| E2_exhaustion_confluence | X1_time10 | 337 | 0.356 | 1.298 | -1.013 | -0.190 | -1.021 | -0.190 | -0.330 | -0.398 | -0.355 | -0.019 | -0.202 | -0.171 | 0.025 | 0.130 | 6.537 | REJECT |

### Exit rules ranked (trade-weighted across setups)

| exit | trades | mean_expectancy | random_mean | edge_over_random |
|---|---|---|---|---|
| X3_target3R | 4,122 | 0.205 | 0.138 | 0.067 |
| X2_target2R | 4,221 | 0.161 | 0.093 | 0.069 |
| X5_chandelier3atr | 4,711 | 0.112 | 0.117 | -0.005 |
| X7_stage_drop | 4,973 | 0.072 | 0.019 | 0.053 |
| X4_trendline_trail | 5,191 | 0.053 | 0.008 | 0.045 |
| X6_partial1R_then_line | 5,213 | 0.030 | -0.013 | 0.042 |
| X1_time10 | 5,232 | 0.025 | 0.025 | 0.000 |

## P1b · Sizing (fixed-fractional, max open positions = 5)

| setup | exit | risk_pct | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 0.005 | 0.010 | -0.047 | 0.220 | 130,746 |
| E1_trigger_with_trend | X3_target3R | 0.010 | 0.020 | -0.091 | 0.217 | 167,292 |
| E1_trigger_with_trend | X3_target3R | 0.020 | 0.037 | -0.176 | 0.210 | 258,228 |
| E4_anchor_reclaim | X3_target3R | 0.005 | 0.027 | -0.128 | 0.210 | 203,766 |
| E4_anchor_reclaim | X3_target3R | 0.010 | 0.052 | -0.242 | 0.214 | 385,587 |
| E4_anchor_reclaim | X3_target3R | 0.020 | 0.095 | -0.457 | 0.208 | 1,127,188 |
| E1_trigger_with_trend | X2_target2R | 0.005 | 0.008 | -0.033 | 0.229 | 121,955 |
| E1_trigger_with_trend | X2_target2R | 0.010 | 0.015 | -0.066 | 0.224 | 146,596 |
| E1_trigger_with_trend | X2_target2R | 0.020 | 0.027 | -0.128 | 0.214 | 203,347 |

## P2 · Market regime (SPY > 200-day average and Trend line rising)

| setup | exit | n_on | exp_on | n_off | exp_off | diff | diff_ci_low | verdict |
|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X4_trendline_trail | 43 | 0.069 | 107 | 0.014 | 0.054 | -0.234 | NO CLEAR EFFECT |
| E1_trigger_with_trend | X5_chandelier3atr | 38 | -0.067 | 97 | 0.328 | -0.395 | -1.068 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 70 | 0.021 | 682 | 0.006 | 0.015 | -0.102 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 62 | -0.035 | 634 | 0.251 | -0.286 | -0.741 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X4_trendline_trail | 29 | -0.127 | 308 | -0.028 | -0.099 | -0.388 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 29 | -0.249 | 308 | -0.040 | -0.209 | -1.062 | NO CLEAR EFFECT |
| E3_stage2_transition | X4_trendline_trail | 475 | 0.063 | 323 | -0.112 | 0.175 | 0.000 | FILTER HELPS |
| E3_stage2_transition | X5_chandelier3atr | 446 | 0.083 | 291 | -0.048 | 0.131 | -0.113 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X4_trendline_trail | 844 | 0.160 | 414 | 0.116 | 0.044 | -0.139 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X5_chandelier3atr | 692 | 0.205 | 329 | 0.098 | 0.107 | -0.090 | NO CLEAR EFFECT |
| E5_score4 | X4_trendline_trail | 1368 | 0.058 | 528 | 0.040 | 0.019 | -0.141 | NO CLEAR EFFECT |
| E5_score4 | X5_chandelier3atr | 1316 | 0.086 | 469 | 0.105 | -0.019 | -0.182 | NO CLEAR EFFECT |

## P4 · Portfolio heat (E1_trigger_with_trend + X3_target3R)

| rule | cagr | max_dd | mar | final |
|---|---|---|---|---|
| No sector cap | 0.015 | -0.069 | 0.219 | 148,276 |
| Max 1 open per sector | 0.015 | -0.069 | 0.219 | 148,276 |

## P6 · Playbook portfolio (E4_anchor_reclaim + E1_trigger_with_trend, exit X3_target3R, 1 per symbol, 1 per sector, max 5 open)

| risk | trades | trades_per_year | expectancy | win_rate | longest_losing_streak | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|---|---|---|
| 0.50% | 942 | 35.206 | 0.353 | 0.503 | 28 | 0.034 | -0.122 | 0.280 | 245,430 |
| 0.75% | 942 | 35.206 | 0.353 | 0.503 | 28 | 0.050 | -0.178 | 0.282 | 371,992 |
| 1.00% | 942 | 35.206 | 0.353 | 0.503 | 28 | 0.066 | -0.231 | 0.285 | 552,176 |

---
**How to read verdicts.** ADOPT = ≥ min trades, bootstrap CI above 0 after correcting for the number of tests, positive in both time halves and both symbol halves, and better than random entries with the same exits. PROMISING = everything except significance. UNSTABLE = fails a half. REJECT = not positive or not better than random.