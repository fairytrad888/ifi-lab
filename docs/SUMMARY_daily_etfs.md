# IFI Lab results: daily · etfs
_Run 2026-10-17 15:14 UTC · 17 symbols · 2000-01-03 to 2026-10-16 · split 2015-01-01 · 42 setup×exit tests (Bonferroni-adjusted) · engine v1.3.3_

## P1 · Exits × setups (R per trade, after costs)

Random-entry control (same stops and exits), mean expectancy by exit: X1_time10 +0.023R, X2_target2R +0.091R, X3_target3R +0.126R, X4_trendline_trail +0.012R, X5_chandelier3atr +0.104R, X6_partial1R_then_line -0.011R, X7_stage_drop +0.018R

| setup | exit | n | win_rate | avg_win | avg_loss | expectancy | median | exp_w10 | ci_low | ci_low_adj | exp_early | exp_late | exp_symA | exp_symB | random_mean | random_p95 | avg_bars | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 136 | 0.449 | 2.100 | -1.016 | 0.381 | -1.011 | 0.381 | 0.095 | -0.059 | 0.330 | 0.446 | 0.450 | 0.302 | 0.126 | 0.381 | 28.757 | PROMISING (not significant after correction) |
| E4_anchor_reclaim | X3_target3R | 886 | 0.505 | 1.569 | -0.948 | 0.322 | 0.021 | 0.322 | 0.229 | 0.153 | 0.213 | 0.441 | 0.296 | 0.358 | 0.126 | 0.226 | 40.819 | ADOPT |
| E1_trigger_with_trend | X2_target2R | 136 | 0.485 | 1.702 | -1.007 | 0.307 | -0.328 | 0.307 | 0.063 | -0.072 | 0.272 | 0.352 | 0.321 | 0.292 | 0.091 | 0.300 | 22.735 | PROMISING (not significant after correction) |
| E1_trigger_with_trend | X1_time10 | 137 | 0.584 | 1.110 | -0.853 | 0.293 | 0.314 | 0.293 | 0.093 | -0.042 | 0.285 | 0.304 | 0.338 | 0.240 | 0.023 | 0.209 | 8.394 | PROMISING (not significant after correction) |
| E4_anchor_reclaim | X2_target2R | 887 | 0.514 | 1.395 | -0.948 | 0.257 | 0.081 | 0.257 | 0.176 | 0.131 | 0.200 | 0.319 | 0.244 | 0.274 | 0.091 | 0.174 | 36.729 | ADOPT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 696 | 0.388 | 1.792 | -0.760 | 0.230 | -0.394 | 0.225 | 0.104 | 0.043 | 0.113 | 0.393 | 0.309 | 0.132 | 0.104 | 0.215 | 21.760 | ADOPT |
| E1_trigger_with_trend | X5_chandelier3atr | 136 | 0.478 | 1.305 | -0.793 | 0.210 | -0.041 | 0.210 | 0.003 | -0.109 | 0.190 | 0.235 | 0.242 | 0.173 | 0.104 | 0.362 | 19.772 | REJECT |
| E5_score4 | X3_target3R | 1443 | 0.430 | 1.808 | -0.995 | 0.209 | -1.012 | 0.209 | 0.131 | 0.091 | 0.130 | 0.296 | 0.126 | 0.321 | 0.126 | 0.202 | 34.857 | ADOPT |
| E1b_trigger_counter_trend | X3_target3R | 672 | 0.400 | 2.028 | -1.020 | 0.200 | -1.009 | 0.200 | 0.075 | -0.012 | 0.107 | 0.326 | 0.297 | 0.080 | 0.126 | 0.236 | 28.793 | REJECT |
| E5_score4 | X2_target2R | 1532 | 0.460 | 1.576 | -0.998 | 0.187 | -0.871 | 0.187 | 0.119 | 0.072 | 0.123 | 0.255 | 0.154 | 0.231 | 0.091 | 0.149 | 29.713 | ADOPT |
| E4_anchor_reclaim | X5_chandelier3atr | 1022 | 0.449 | 1.085 | -0.576 | 0.170 | -0.135 | 0.170 | 0.103 | 0.060 | 0.129 | 0.215 | 0.169 | 0.171 | 0.104 | 0.202 | 23.737 | REJECT |
| E4_anchor_reclaim | X7_stage_drop | 1144 | 0.380 | 1.262 | -0.508 | 0.165 | -0.213 | 0.160 | 0.093 | 0.062 | 0.152 | 0.179 | 0.164 | 0.167 | 0.018 | 0.091 | 24.037 | ADOPT |
| E3_stage2_transition | X3_target3R | 655 | 0.423 | 1.727 | -0.996 | 0.155 | -1.010 | 0.155 | 0.033 | -0.035 | 0.129 | 0.183 | 0.098 | 0.229 | 0.126 | 0.239 | 34.666 | REJECT |
| E4_anchor_reclaim | X4_trendline_trail | 1259 | 0.366 | 1.144 | -0.434 | 0.144 | -0.191 | 0.144 | 0.079 | 0.046 | 0.136 | 0.152 | 0.126 | 0.170 | 0.012 | 0.085 | 20.014 | ADOPT |
| E3_stage2_transition | X2_target2R | 660 | 0.444 | 1.537 | -0.995 | 0.129 | -1.008 | 0.129 | 0.027 | -0.047 | 0.102 | 0.158 | 0.092 | 0.176 | 0.091 | 0.181 | 30.615 | REJECT |
| E1b_trigger_counter_trend | X2_target2R | 675 | 0.427 | 1.653 | -1.025 | 0.118 | -1.008 | 0.118 | 0.007 | -0.049 | 0.014 | 0.260 | 0.157 | 0.069 | 0.091 | 0.179 | 24.307 | REJECT |
| E4_anchor_reclaim | X6_partial1R_then_line | 1260 | 0.408 | 0.898 | -0.441 | 0.105 | -0.162 | 0.105 | 0.059 | 0.036 | 0.095 | 0.116 | 0.099 | 0.114 | -0.011 | 0.033 | 19.712 | ADOPT |
| E5_score4 | X5_chandelier3atr | 1786 | 0.411 | 1.168 | -0.662 | 0.090 | -0.230 | 0.090 | 0.032 | 0.007 | 0.048 | 0.135 | 0.059 | 0.134 | 0.104 | 0.176 | 21.074 | REJECT |
| E1b_trigger_counter_trend | X1_time10 | 699 | 0.512 | 0.874 | -0.748 | 0.083 | 0.012 | 0.083 | 0.002 | -0.033 | -0.013 | 0.218 | 0.158 | -0.010 | 0.023 | 0.106 | 8.422 | REJECT |
| E5_score4 | X7_stage_drop | 1794 | 0.358 | 1.325 | -0.632 | 0.068 | -0.307 | 0.065 | 0.006 | -0.014 | 0.037 | 0.102 | 0.028 | 0.126 | 0.018 | 0.075 | 23.035 | REJECT |
| E4_anchor_reclaim | X1_time10 | 1175 | 0.569 | 0.572 | -0.612 | 0.062 | 0.100 | 0.061 | 0.016 | -0.013 | 0.029 | 0.098 | 0.071 | 0.049 | 0.023 | 0.089 | 9.259 | REJECT |
| E3_stage2_transition | X7_stage_drop | 798 | 0.336 | 1.237 | -0.544 | 0.054 | -0.304 | 0.044 | -0.035 | -0.093 | 0.040 | 0.070 | 0.026 | 0.092 | 0.018 | 0.104 | 18.852 | REJECT |
| E5_score4 | X4_trendline_trail | 1897 | 0.356 | 1.186 | -0.574 | 0.052 | -0.283 | 0.052 | -0.002 | -0.027 | 0.026 | 0.079 | 0.009 | 0.114 | 0.012 | 0.070 | 20.116 | REJECT |
| E5_score4 | X1_time10 | 2117 | 0.534 | 0.676 | -0.685 | 0.041 | 0.065 | 0.041 | 0.002 | -0.028 | -0.006 | 0.092 | 0.006 | 0.090 | 0.023 | 0.072 | 8.923 | REJECT |
| E3_stage2_transition | X5_chandelier3atr | 737 | 0.392 | 1.168 | -0.702 | 0.031 | -0.306 | 0.023 | -0.050 | -0.121 | -0.014 | 0.079 | 0.001 | 0.072 | 0.104 | 0.215 | 21.822 | REJECT |
| E5_score4 | X6_partial1R_then_line | 1918 | 0.419 | 0.876 | -0.590 | 0.024 | -0.227 | 0.024 | -0.015 | -0.036 | 0.003 | 0.047 | -0.018 | 0.086 | -0.011 | 0.024 | 19.409 | UNSTABLE (fails a split half) |
| E1_trigger_with_trend | X7_stage_drop | 152 | 0.428 | 0.514 | -0.346 | 0.022 | -0.079 | 0.022 | -0.077 | -0.121 | -0.013 | 0.066 | 0.020 | 0.023 | 0.018 | 0.236 | 4.355 | REJECT |
| E1_trigger_with_trend | X4_trendline_trail | 152 | 0.428 | 0.506 | -0.345 | 0.019 | -0.076 | 0.019 | -0.079 | -0.123 | -0.019 | 0.068 | 0.024 | 0.013 | 0.012 | 0.220 | 4.092 | REJECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 752 | 0.500 | 0.335 | -0.320 | 0.007 | -0.001 | 0.007 | -0.025 | -0.043 | -0.024 | 0.052 | -0.001 | 0.017 | 0.012 | 0.106 | 2.298 | REJECT |
| E1b_trigger_counter_trend | X6_partial1R_then_line | 752 | 0.500 | 0.329 | -0.315 | 0.007 | -0.001 | 0.007 | -0.024 | -0.041 | -0.023 | 0.050 | -0.003 | 0.019 | -0.011 | 0.046 | 2.298 | REJECT |
| E1b_trigger_counter_trend | X7_stage_drop | 752 | 0.499 | 0.335 | -0.321 | 0.006 | -0.002 | 0.006 | -0.027 | -0.045 | -0.024 | 0.049 | -0.002 | 0.016 | 0.018 | 0.112 | 2.340 | REJECT |
| E1_trigger_with_trend | X6_partial1R_then_line | 152 | 0.428 | 0.457 | -0.345 | -0.002 | -0.076 | -0.002 | -0.088 | -0.127 | -0.032 | 0.037 | -0.003 | -0.001 | -0.011 | 0.118 | 4.092 | REJECT |
| E3_stage2_transition | X4_trendline_trail | 798 | 0.316 | 0.867 | -0.412 | -0.008 | -0.245 | -0.016 | -0.077 | -0.118 | -0.022 | 0.007 | -0.019 | 0.007 | 0.012 | 0.101 | 13.466 | REJECT |
| E3_stage2_transition | X6_partial1R_then_line | 798 | 0.337 | 0.733 | -0.408 | -0.024 | -0.227 | -0.024 | -0.073 | -0.106 | -0.042 | -0.004 | -0.035 | -0.009 | -0.011 | 0.046 | 13.372 | REJECT |
| E2_exhaustion_confluence | X7_stage_drop | 337 | 0.487 | 0.501 | -0.529 | -0.028 | -0.008 | -0.028 | -0.107 | -0.144 | -0.000 | -0.056 | -0.026 | -0.030 | 0.018 | 0.161 | 2.457 | REJECT |
| E2_exhaustion_confluence | X4_trendline_trail | 337 | 0.490 | 0.480 | -0.532 | -0.036 | -0.007 | -0.036 | -0.113 | -0.157 | -0.017 | -0.056 | -0.042 | -0.026 | 0.012 | 0.141 | 2.288 | REJECT |
| E2_exhaustion_confluence | X6_partial1R_then_line | 337 | 0.496 | 0.449 | -0.517 | -0.039 | -0.001 | -0.039 | -0.110 | -0.144 | -0.021 | -0.057 | -0.054 | -0.013 | -0.011 | 0.071 | 2.288 | REJECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 337 | 0.258 | 2.602 | -0.981 | -0.056 | -1.023 | -0.056 | -0.248 | -0.400 | -0.289 | 0.187 | -0.112 | 0.037 | 0.104 | 0.273 | 14.273 | REJECT |
| E3_stage2_transition | X1_time10 | 770 | 0.484 | 0.559 | -0.688 | -0.084 | -0.033 | -0.084 | -0.139 | -0.170 | -0.114 | -0.051 | -0.102 | -0.059 | 0.023 | 0.101 | 8.878 | REJECT |
| E2_exhaustion_confluence | X3_target3R | 333 | 0.264 | 2.621 | -1.090 | -0.109 | -1.031 | -0.109 | -0.284 | -0.404 | -0.261 | 0.046 | -0.134 | -0.069 | 0.126 | 0.299 | 14.733 | REJECT |
| E2_exhaustion_confluence | X2_target2R | 334 | 0.314 | 1.921 | -1.082 | -0.138 | -1.028 | -0.138 | -0.290 | -0.395 | -0.280 | 0.008 | -0.146 | -0.124 | 0.091 | 0.224 | 11.165 | REJECT |
| E2_exhaustion_confluence | X1_time10 | 337 | 0.356 | 1.298 | -1.013 | -0.190 | -1.021 | -0.190 | -0.330 | -0.398 | -0.355 | -0.019 | -0.202 | -0.171 | 0.023 | 0.145 | 6.537 | REJECT |

### Exit rules ranked (trade-weighted across setups)

| exit | trades | mean_expectancy | random_mean | edge_over_random |
|---|---|---|---|---|
| X3_target3R | 4,125 | 0.203 | 0.126 | 0.077 |
| X2_target2R | 4,224 | 0.160 | 0.091 | 0.068 |
| X5_chandelier3atr | 4,714 | 0.112 | 0.104 | 0.008 |
| X7_stage_drop | 4,977 | 0.071 | 0.018 | 0.053 |
| X4_trendline_trail | 5,195 | 0.052 | 0.012 | 0.040 |
| X6_partial1R_then_line | 5,217 | 0.029 | -0.011 | 0.040 |
| X1_time10 | 5,235 | 0.025 | 0.023 | 0.001 |

## P1b · Sizing (fixed-fractional, max open positions = 5)

| setup | exit | risk_pct | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 0.005 | 0.010 | -0.047 | 0.208 | 128,764 |
| E1_trigger_with_trend | X3_target3R | 0.010 | 0.019 | -0.091 | 0.204 | 162,351 |
| E1_trigger_with_trend | X3_target3R | 0.020 | 0.035 | -0.176 | 0.197 | 243,722 |
| E4_anchor_reclaim | X3_target3R | 0.005 | 0.028 | -0.127 | 0.218 | 207,523 |
| E4_anchor_reclaim | X3_target3R | 0.010 | 0.053 | -0.248 | 0.214 | 399,155 |
| E4_anchor_reclaim | X3_target3R | 0.020 | 0.097 | -0.465 | 0.209 | 1,199,433 |
| E1_trigger_with_trend | X2_target2R | 0.005 | 0.007 | -0.033 | 0.216 | 120,629 |
| E1_trigger_with_trend | X2_target2R | 0.010 | 0.014 | -0.066 | 0.211 | 143,506 |
| E1_trigger_with_trend | X2_target2R | 0.020 | 0.026 | -0.128 | 0.201 | 195,263 |

## P2 · Market regime (SPY > 200-day average and Trend line rising)

| setup | exit | n_on | exp_on | n_off | exp_off | diff | diff_ci_low | verdict |
|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X4_trendline_trail | 45 | 0.030 | 107 | 0.014 | 0.015 | -0.283 | NO CLEAR EFFECT |
| E1_trigger_with_trend | X5_chandelier3atr | 39 | -0.084 | 97 | 0.328 | -0.412 | -1.035 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 70 | 0.021 | 682 | 0.006 | 0.015 | -0.102 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 62 | 0.014 | 634 | 0.251 | -0.237 | -0.712 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X4_trendline_trail | 29 | -0.127 | 308 | -0.028 | -0.099 | -0.388 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 29 | -0.222 | 308 | -0.040 | -0.182 | -1.062 | NO CLEAR EFFECT |
| E3_stage2_transition | X4_trendline_trail | 475 | 0.063 | 323 | -0.112 | 0.175 | 0.000 | FILTER HELPS |
| E3_stage2_transition | X5_chandelier3atr | 446 | 0.083 | 291 | -0.048 | 0.131 | -0.113 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X4_trendline_trail | 845 | 0.157 | 414 | 0.116 | 0.042 | -0.131 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X5_chandelier3atr | 693 | 0.204 | 329 | 0.098 | 0.106 | -0.099 | NO CLEAR EFFECT |
| E5_score4 | X4_trendline_trail | 1369 | 0.057 | 528 | 0.040 | 0.017 | -0.143 | NO CLEAR EFFECT |
| E5_score4 | X5_chandelier3atr | 1317 | 0.085 | 469 | 0.105 | -0.020 | -0.209 | NO CLEAR EFFECT |

## P4 · Portfolio heat (E1_trigger_with_trend + X3_target3R)

| rule | cagr | max_dd | mar | final |
|---|---|---|---|---|
| No sector cap | 0.014 | -0.069 | 0.206 | 144,942 |
| Max 1 open per sector | 0.014 | -0.069 | 0.206 | 144,942 |

## P6 · Playbook portfolio (E4_anchor_reclaim + E1_trigger_with_trend, exit X3_target3R, 1 per symbol, 1 per sector, max 5 open)

| risk | trades | trades_per_year | expectancy | win_rate | longest_losing_streak | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|---|---|---|
| 0.50% | 944 | 35.270 | 0.348 | 0.501 | 28 | 0.033 | -0.122 | 0.269 | 237,431 |
| 0.75% | 944 | 35.270 | 0.348 | 0.501 | 28 | 0.048 | -0.178 | 0.271 | 354,185 |
| 1.00% | 944 | 35.270 | 0.348 | 0.501 | 28 | 0.063 | -0.231 | 0.274 | 517,647 |

---
**How to read verdicts.** ADOPT = ≥ min trades, bootstrap CI above 0 after correcting for the number of tests, positive in both time halves and both symbol halves, and better than random entries with the same exits. PROMISING = everything except significance. UNSTABLE = fails a half. REJECT = not positive or not better than random.