# IFI Lab results: daily · etfs
_Run 2026-10-24 15:36 UTC · 17 symbols · 2000-01-03 to 2026-10-23 · split 2015-01-01 · 42 setup×exit tests (Bonferroni-adjusted) · engine v1.3.3_

## P1 · Exits × setups (R per trade, after costs)

Random-entry control (same stops and exits), mean expectancy by exit: X1_time10 +0.001R, X2_target2R +0.072R, X3_target3R +0.107R, X4_trendline_trail -0.007R, X5_chandelier3atr +0.063R, X6_partial1R_then_line -0.014R, X7_stage_drop -0.003R

| setup | exit | n | win_rate | avg_win | avg_loss | expectancy | median | exp_w10 | ci_low | ci_low_adj | exp_early | exp_late | exp_symA | exp_symB | random_mean | random_p95 | avg_bars | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 137 | 0.438 | 2.144 | -0.995 | 0.380 | -1.010 | 0.380 | 0.091 | -0.080 | 0.330 | 0.441 | 0.459 | 0.289 | 0.107 | 0.342 | 28.715 | PROMISING (not significant after correction) |
| E4_anchor_reclaim | X3_target3R | 889 | 0.505 | 1.562 | -0.948 | 0.320 | 0.021 | 0.320 | 0.225 | 0.183 | 0.213 | 0.436 | 0.295 | 0.355 | 0.107 | 0.204 | 40.717 | ADOPT |
| E1_trigger_with_trend | X2_target2R | 137 | 0.482 | 1.718 | -0.998 | 0.311 | -0.338 | 0.311 | 0.069 | -0.068 | 0.272 | 0.358 | 0.332 | 0.286 | 0.072 | 0.269 | 22.657 | PROMISING (not significant after correction) |
| E1_trigger_with_trend | X1_time10 | 138 | 0.580 | 1.106 | -0.844 | 0.286 | 0.295 | 0.286 | 0.074 | -0.040 | 0.285 | 0.288 | 0.338 | 0.227 | 0.001 | 0.181 | 8.362 | PROMISING (not significant after correction) |
| E4_anchor_reclaim | X2_target2R | 890 | 0.515 | 1.389 | -0.947 | 0.255 | 0.079 | 0.255 | 0.173 | 0.123 | 0.200 | 0.315 | 0.243 | 0.272 | 0.072 | 0.151 | 36.640 | ADOPT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 697 | 0.387 | 1.798 | -0.759 | 0.232 | -0.391 | 0.226 | 0.111 | 0.030 | 0.113 | 0.397 | 0.311 | 0.134 | 0.063 | 0.178 | 21.769 | ADOPT |
| E1_trigger_with_trend | X5_chandelier3atr | 137 | 0.474 | 1.319 | -0.786 | 0.213 | -0.045 | 0.213 | -0.005 | -0.126 | 0.190 | 0.241 | 0.251 | 0.169 | 0.063 | 0.308 | 19.723 | REJECT |
| E5_score4 | X3_target3R | 1446 | 0.430 | 1.803 | -0.995 | 0.208 | -1.012 | 0.208 | 0.129 | 0.089 | 0.130 | 0.293 | 0.125 | 0.321 | 0.107 | 0.183 | 34.813 | ADOPT |
| E1b_trigger_counter_trend | X3_target3R | 673 | 0.400 | 2.039 | -1.018 | 0.204 | -1.009 | 0.204 | 0.079 | 0.010 | 0.107 | 0.335 | 0.299 | 0.085 | 0.107 | 0.210 | 28.790 | REJECT |
| E5_score4 | X2_target2R | 1535 | 0.461 | 1.573 | -0.998 | 0.186 | -0.869 | 0.186 | 0.118 | 0.084 | 0.123 | 0.253 | 0.152 | 0.230 | 0.072 | 0.130 | 29.680 | ADOPT |
| E4_anchor_reclaim | X5_chandelier3atr | 1025 | 0.450 | 1.080 | -0.575 | 0.169 | -0.132 | 0.169 | 0.103 | 0.064 | 0.129 | 0.213 | 0.169 | 0.170 | 0.063 | 0.158 | 23.681 | ADOPT |
| E4_anchor_reclaim | X7_stage_drop | 1147 | 0.381 | 1.256 | -0.507 | 0.165 | -0.211 | 0.159 | 0.093 | 0.058 | 0.152 | 0.178 | 0.163 | 0.167 | -0.003 | 0.069 | 23.986 | ADOPT |
| E3_stage2_transition | X3_target3R | 655 | 0.423 | 1.727 | -0.998 | 0.154 | -1.010 | 0.154 | 0.032 | -0.037 | 0.129 | 0.181 | 0.098 | 0.227 | 0.107 | 0.213 | 34.679 | REJECT |
| E4_anchor_reclaim | X4_trendline_trail | 1262 | 0.367 | 1.140 | -0.434 | 0.143 | -0.190 | 0.143 | 0.081 | 0.053 | 0.136 | 0.152 | 0.126 | 0.169 | -0.007 | 0.054 | 19.977 | ADOPT |
| E3_stage2_transition | X2_target2R | 660 | 0.444 | 1.537 | -0.996 | 0.128 | -1.008 | 0.128 | 0.026 | -0.046 | 0.102 | 0.157 | 0.092 | 0.175 | 0.072 | 0.165 | 30.636 | REJECT |
| E1b_trigger_counter_trend | X2_target2R | 676 | 0.426 | 1.657 | -1.023 | 0.119 | -1.008 | 0.119 | 0.016 | -0.056 | 0.014 | 0.262 | 0.160 | 0.069 | 0.072 | 0.165 | 24.286 | REJECT |
| E4_anchor_reclaim | X6_partial1R_then_line | 1263 | 0.409 | 0.894 | -0.441 | 0.105 | -0.161 | 0.105 | 0.058 | 0.029 | 0.095 | 0.115 | 0.099 | 0.113 | -0.014 | 0.028 | 19.676 | ADOPT |
| E5_score4 | X5_chandelier3atr | 1790 | 0.411 | 1.165 | -0.662 | 0.089 | -0.230 | 0.089 | 0.032 | 0.003 | 0.048 | 0.133 | 0.059 | 0.132 | 0.063 | 0.136 | 21.037 | REJECT |
| E1b_trigger_counter_trend | X1_time10 | 700 | 0.511 | 0.875 | -0.747 | 0.082 | 0.011 | 0.082 | 0.007 | -0.039 | -0.013 | 0.216 | 0.157 | -0.010 | 0.001 | 0.076 | 8.419 | UNSTABLE (fails a split half) |
| E5_score4 | X7_stage_drop | 1798 | 0.358 | 1.321 | -0.632 | 0.068 | -0.307 | 0.064 | 0.010 | -0.032 | 0.037 | 0.101 | 0.028 | 0.124 | -0.003 | 0.053 | 22.993 | PROMISING (not significant after correction) |
| E4_anchor_reclaim | X1_time10 | 1178 | 0.570 | 0.571 | -0.611 | 0.062 | 0.097 | 0.061 | 0.015 | -0.032 | 0.029 | 0.098 | 0.071 | 0.049 | 0.001 | 0.061 | 9.247 | PROMISING (not significant after correction) |
| E3_stage2_transition | X7_stage_drop | 798 | 0.336 | 1.237 | -0.544 | 0.054 | -0.304 | 0.044 | -0.035 | -0.093 | 0.040 | 0.070 | 0.026 | 0.092 | -0.003 | 0.082 | 18.852 | REJECT |
| E5_score4 | X4_trendline_trail | 1901 | 0.356 | 1.183 | -0.574 | 0.051 | -0.283 | 0.051 | -0.003 | -0.026 | 0.026 | 0.078 | 0.009 | 0.113 | -0.007 | 0.041 | 20.083 | PROMISING (not significant after correction) |
| E5_score4 | X1_time10 | 2121 | 0.534 | 0.675 | -0.685 | 0.041 | 0.065 | 0.040 | 0.002 | -0.026 | -0.006 | 0.090 | 0.006 | 0.088 | 0.001 | 0.047 | 8.916 | REJECT |
| E3_stage2_transition | X5_chandelier3atr | 737 | 0.392 | 1.168 | -0.702 | 0.031 | -0.306 | 0.023 | -0.050 | -0.121 | -0.014 | 0.079 | 0.001 | 0.072 | 0.063 | 0.171 | 21.822 | REJECT |
| E5_score4 | X6_partial1R_then_line | 1922 | 0.419 | 0.874 | -0.590 | 0.024 | -0.227 | 0.024 | -0.013 | -0.033 | 0.003 | 0.046 | -0.018 | 0.085 | -0.014 | 0.019 | 19.377 | UNSTABLE (fails a split half) |
| E1_trigger_with_trend | X7_stage_drop | 153 | 0.425 | 0.514 | -0.344 | 0.021 | -0.079 | 0.021 | -0.070 | -0.127 | -0.013 | 0.064 | 0.020 | 0.021 | -0.003 | 0.220 | 4.340 | REJECT |
| E1_trigger_with_trend | X4_trendline_trail | 153 | 0.425 | 0.506 | -0.343 | 0.018 | -0.079 | 0.018 | -0.074 | -0.126 | -0.019 | 0.065 | 0.024 | 0.011 | -0.007 | 0.182 | 4.078 | REJECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 753 | 0.499 | 0.335 | -0.320 | 0.007 | -0.002 | 0.007 | -0.025 | -0.049 | -0.024 | 0.051 | -0.001 | 0.017 | -0.007 | 0.075 | 2.297 | REJECT |
| E1b_trigger_counter_trend | X6_partial1R_then_line | 753 | 0.499 | 0.329 | -0.314 | 0.007 | -0.002 | 0.007 | -0.024 | -0.046 | -0.023 | 0.049 | -0.003 | 0.019 | -0.014 | 0.039 | 2.297 | REJECT |
| E1b_trigger_counter_trend | X7_stage_drop | 753 | 0.498 | 0.335 | -0.320 | 0.006 | -0.002 | 0.006 | -0.027 | -0.050 | -0.024 | 0.048 | -0.003 | 0.016 | -0.003 | 0.089 | 2.340 | REJECT |
| E1_trigger_with_trend | X6_partial1R_then_line | 153 | 0.425 | 0.457 | -0.343 | -0.003 | -0.079 | -0.003 | -0.083 | -0.131 | -0.032 | 0.035 | -0.003 | -0.003 | -0.014 | 0.106 | 4.078 | REJECT |
| E3_stage2_transition | X4_trendline_trail | 798 | 0.316 | 0.867 | -0.412 | -0.008 | -0.245 | -0.016 | -0.077 | -0.118 | -0.022 | 0.007 | -0.019 | 0.007 | -0.007 | 0.074 | 13.466 | REJECT |
| E3_stage2_transition | X6_partial1R_then_line | 798 | 0.337 | 0.733 | -0.408 | -0.024 | -0.227 | -0.024 | -0.073 | -0.106 | -0.042 | -0.004 | -0.035 | -0.009 | -0.014 | 0.037 | 13.372 | REJECT |
| E2_exhaustion_confluence | X7_stage_drop | 337 | 0.487 | 0.501 | -0.529 | -0.028 | -0.008 | -0.028 | -0.107 | -0.144 | -0.000 | -0.056 | -0.026 | -0.030 | -0.003 | 0.128 | 2.457 | REJECT |
| E2_exhaustion_confluence | X4_trendline_trail | 337 | 0.490 | 0.480 | -0.532 | -0.036 | -0.007 | -0.036 | -0.113 | -0.157 | -0.017 | -0.056 | -0.042 | -0.026 | -0.007 | 0.119 | 2.288 | REJECT |
| E2_exhaustion_confluence | X6_partial1R_then_line | 337 | 0.496 | 0.449 | -0.517 | -0.039 | -0.001 | -0.039 | -0.110 | -0.144 | -0.021 | -0.057 | -0.054 | -0.013 | -0.014 | 0.066 | 2.288 | REJECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 337 | 0.258 | 2.608 | -0.981 | -0.055 | -1.023 | -0.055 | -0.247 | -0.397 | -0.289 | 0.190 | -0.110 | 0.037 | 0.063 | 0.227 | 14.288 | REJECT |
| E3_stage2_transition | X1_time10 | 770 | 0.484 | 0.559 | -0.688 | -0.084 | -0.033 | -0.084 | -0.139 | -0.170 | -0.114 | -0.051 | -0.102 | -0.059 | 0.001 | 0.074 | 8.878 | REJECT |
| E2_exhaustion_confluence | X3_target3R | 333 | 0.264 | 2.620 | -1.090 | -0.109 | -1.031 | -0.109 | -0.285 | -0.404 | -0.261 | 0.045 | -0.134 | -0.070 | 0.107 | 0.258 | 14.748 | REJECT |
| E2_exhaustion_confluence | X2_target2R | 334 | 0.314 | 1.920 | -1.082 | -0.138 | -1.028 | -0.138 | -0.290 | -0.395 | -0.280 | 0.007 | -0.146 | -0.125 | 0.072 | 0.196 | 11.180 | REJECT |
| E2_exhaustion_confluence | X1_time10 | 337 | 0.356 | 1.298 | -1.013 | -0.190 | -1.021 | -0.190 | -0.330 | -0.398 | -0.355 | -0.019 | -0.202 | -0.171 | 0.001 | 0.111 | 6.537 | REJECT |

### Exit rules ranked (trade-weighted across setups)

| exit | trades | mean_expectancy | random_mean | edge_over_random |
|---|---|---|---|---|
| X3_target3R | 4,133 | 0.203 | 0.107 | 0.096 |
| X2_target2R | 4,232 | 0.159 | 0.072 | 0.088 |
| X5_chandelier3atr | 4,723 | 0.112 | 0.063 | 0.049 |
| X7_stage_drop | 4,986 | 0.071 | -0.003 | 0.074 |
| X4_trendline_trail | 5,204 | 0.052 | -0.007 | 0.058 |
| X6_partial1R_then_line | 5,226 | 0.029 | -0.014 | 0.043 |
| X1_time10 | 5,244 | 0.024 | 0.001 | 0.023 |

## P1b · Sizing (fixed-fractional, max open positions = 5)

| setup | exit | risk_pct | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 0.005 | 0.010 | -0.047 | 0.212 | 129,522 |
| E1_trigger_with_trend | X3_target3R | 0.010 | 0.019 | -0.091 | 0.209 | 164,205 |
| E1_trigger_with_trend | X3_target3R | 0.020 | 0.035 | -0.176 | 0.201 | 248,972 |
| E4_anchor_reclaim | X3_target3R | 0.005 | 0.028 | -0.121 | 0.232 | 210,237 |
| E4_anchor_reclaim | X3_target3R | 0.010 | 0.054 | -0.229 | 0.236 | 409,333 |
| E4_anchor_reclaim | X3_target3R | 0.020 | 0.099 | -0.427 | 0.232 | 1,257,584 |
| E1_trigger_with_trend | X2_target2R | 0.005 | 0.008 | -0.033 | 0.228 | 121,812 |
| E1_trigger_with_trend | X2_target2R | 0.010 | 0.015 | -0.066 | 0.222 | 146,258 |
| E1_trigger_with_trend | X2_target2R | 0.020 | 0.027 | -0.128 | 0.212 | 202,446 |

## P2 · Market regime (SPY > 200-day average and Trend line rising)

| setup | exit | n_on | exp_on | n_off | exp_off | diff | diff_ci_low | verdict |
|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X4_trendline_trail | 46 | 0.027 | 107 | 0.014 | 0.012 | -0.288 | NO CLEAR EFFECT |
| E1_trigger_with_trend | X5_chandelier3atr | 40 | -0.068 | 97 | 0.328 | -0.396 | -1.010 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 71 | 0.018 | 682 | 0.006 | 0.011 | -0.127 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 63 | 0.037 | 634 | 0.251 | -0.214 | -0.738 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X4_trendline_trail | 29 | -0.127 | 308 | -0.028 | -0.099 | -0.388 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 29 | -0.204 | 308 | -0.040 | -0.164 | -1.062 | NO CLEAR EFFECT |
| E3_stage2_transition | X4_trendline_trail | 475 | 0.063 | 323 | -0.112 | 0.175 | 0.000 | FILTER HELPS |
| E3_stage2_transition | X5_chandelier3atr | 446 | 0.083 | 291 | -0.048 | 0.131 | -0.113 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X4_trendline_trail | 848 | 0.157 | 414 | 0.116 | 0.041 | -0.146 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X5_chandelier3atr | 696 | 0.203 | 329 | 0.098 | 0.105 | -0.095 | NO CLEAR EFFECT |
| E5_score4 | X4_trendline_trail | 1372 | 0.056 | 529 | 0.038 | 0.018 | -0.140 | NO CLEAR EFFECT |
| E5_score4 | X5_chandelier3atr | 1320 | 0.085 | 470 | 0.102 | -0.018 | -0.212 | NO CLEAR EFFECT |

## P4 · Portfolio heat (E1_trigger_with_trend + X3_target3R)

| rule | cagr | max_dd | mar | final |
|---|---|---|---|---|
| No sector cap | 0.015 | -0.069 | 0.211 | 146,218 |
| Max 1 open per sector | 0.015 | -0.069 | 0.211 | 146,218 |

## P6 · Playbook portfolio (E4_anchor_reclaim + E1_trigger_with_trend, exit X3_target3R, 1 per symbol, 1 per sector, max 5 open)

| risk | trades | trades_per_year | expectancy | win_rate | longest_losing_streak | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|---|---|---|
| 0.50% | 946 | 35.319 | 0.347 | 0.501 | 28 | 0.034 | -0.122 | 0.277 | 243,544 |
| 0.75% | 946 | 35.319 | 0.347 | 0.501 | 28 | 0.050 | -0.178 | 0.279 | 367,658 |
| 1.00% | 946 | 35.319 | 0.347 | 0.501 | 28 | 0.065 | -0.231 | 0.282 | 543,518 |

---
**How to read verdicts.** ADOPT = ≥ min trades, bootstrap CI above 0 after correcting for the number of tests, positive in both time halves and both symbol halves, and better than random entries with the same exits. PROMISING = everything except significance. UNSTABLE = fails a half. REJECT = not positive or not better than random.