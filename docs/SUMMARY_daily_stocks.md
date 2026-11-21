# IFI Lab results: daily · stocks
_Run 2026-11-21 18:52 UTC · 61 symbols · 2000-01-03 to 2026-11-20 · split 2015-01-01 · 42 setup×exit tests (Bonferroni-adjusted) · engine v1.3.3_

> **Survivorship bias:** this stock list was chosen in 2026 from today's large caps, so random long entries earn money too. Judge stock setups by their edge over the random-entry control, not by raw expectancy.

## P1 · Exits × setups (R per trade, after costs)

Random-entry control (same stops and exits), mean expectancy by exit: X1_time10 +0.046R, X2_target2R +0.113R, X3_target3R +0.164R, X4_trendline_trail +0.066R, X5_chandelier3atr +0.154R, X6_partial1R_then_line +0.013R, X7_stage_drop +0.081R

| setup | exit | n | win_rate | avg_win | avg_loss | expectancy | median | exp_w10 | ci_low | ci_low_adj | exp_early | exp_late | exp_symA | exp_symB | random_mean | random_p95 | avg_bars | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 523 | 0.409 | 2.301 | -1.042 | 0.326 | -1.019 | 0.326 | 0.174 | 0.108 | 0.278 | 0.379 | 0.355 | 0.296 | 0.164 | 0.297 | 26.862 | ADOPT |
| E1_trigger_with_trend | X5_chandelier3atr | 525 | 0.432 | 1.683 | -0.777 | 0.286 | -0.264 | 0.272 | 0.140 | 0.053 | 0.210 | 0.371 | 0.380 | 0.191 | 0.154 | 0.296 | 20.074 | REJECT |
| E4_anchor_reclaim | X3_target3R | 3182 | 0.471 | 1.658 | -0.959 | 0.275 | -0.219 | 0.275 | 0.222 | 0.190 | 0.244 | 0.306 | 0.305 | 0.244 | 0.164 | 0.217 | 38.885 | ADOPT |
| E1_trigger_with_trend | X2_target2R | 524 | 0.452 | 1.815 | -1.047 | 0.247 | -1.011 | 0.247 | 0.118 | 0.061 | 0.236 | 0.260 | 0.250 | 0.244 | 0.113 | 0.218 | 21.569 | ADOPT |
| E4_anchor_reclaim | X2_target2R | 3186 | 0.489 | 1.456 | -0.961 | 0.221 | -0.078 | 0.221 | 0.175 | 0.147 | 0.201 | 0.241 | 0.244 | 0.198 | 0.113 | 0.156 | 34.490 | ADOPT |
| E1b_trigger_counter_trend | X3_target3R | 2515 | 0.387 | 2.185 | -1.049 | 0.203 | -1.017 | 0.203 | 0.136 | 0.084 | 0.141 | 0.285 | 0.208 | 0.199 | 0.164 | 0.225 | 26.027 | REJECT |
| E5_score4 | X3_target3R | 5317 | 0.416 | 1.918 | -1.024 | 0.201 | -1.015 | 0.201 | 0.155 | 0.137 | 0.184 | 0.219 | 0.207 | 0.194 | 0.164 | 0.206 | 32.436 | REJECT |
| E3_stage2_transition | X3_target3R | 2511 | 0.411 | 1.897 | -1.002 | 0.191 | -1.013 | 0.191 | 0.126 | 0.086 | 0.198 | 0.183 | 0.156 | 0.225 | 0.164 | 0.225 | 34.186 | REJECT |
| E5_score4 | X2_target2R | 5620 | 0.451 | 1.610 | -1.022 | 0.164 | -1.009 | 0.164 | 0.128 | 0.111 | 0.146 | 0.183 | 0.170 | 0.157 | 0.113 | 0.145 | 27.835 | ADOPT |
| E3_stage2_transition | X2_target2R | 2543 | 0.445 | 1.622 | -1.005 | 0.163 | -1.008 | 0.163 | 0.112 | 0.082 | 0.171 | 0.155 | 0.140 | 0.186 | 0.113 | 0.164 | 28.829 | REJECT |
| E1_trigger_with_trend | X1_time10 | 527 | 0.539 | 0.965 | -0.775 | 0.163 | 0.118 | 0.163 | 0.072 | 0.022 | 0.150 | 0.176 | 0.165 | 0.160 | 0.046 | 0.146 | 8.660 | ADOPT |
| E4_anchor_reclaim | X7_stage_drop | 3923 | 0.366 | 1.368 | -0.552 | 0.150 | -0.256 | 0.147 | 0.108 | 0.082 | 0.128 | 0.173 | 0.165 | 0.135 | 0.081 | 0.129 | 23.585 | ADOPT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 2602 | 0.379 | 1.738 | -0.825 | 0.147 | -0.446 | 0.144 | 0.083 | 0.045 | 0.046 | 0.284 | 0.162 | 0.133 | 0.154 | 0.223 | 19.570 | REJECT |
| E5_score4 | X7_stage_drop | 6419 | 0.353 | 1.584 | -0.647 | 0.140 | -0.305 | 0.131 | 0.101 | 0.081 | 0.132 | 0.150 | 0.133 | 0.148 | 0.081 | 0.119 | 22.571 | ADOPT |
| E3_stage2_transition | X5_chandelier3atr | 2862 | 0.392 | 1.381 | -0.666 | 0.137 | -0.284 | 0.132 | 0.089 | 0.052 | 0.130 | 0.146 | 0.097 | 0.178 | 0.154 | 0.220 | 20.637 | REJECT |
| E1b_trigger_counter_trend | X2_target2R | 2521 | 0.424 | 1.740 | -1.051 | 0.132 | -1.012 | 0.132 | 0.077 | 0.045 | 0.070 | 0.215 | 0.148 | 0.118 | 0.113 | 0.163 | 21.041 | REJECT |
| E4_anchor_reclaim | X5_chandelier3atr | 3589 | 0.419 | 1.131 | -0.596 | 0.127 | -0.197 | 0.126 | 0.088 | 0.071 | 0.088 | 0.167 | 0.146 | 0.109 | 0.154 | 0.213 | 21.612 | REJECT |
| E5_score4 | X4_trendline_trail | 6767 | 0.338 | 1.483 | -0.570 | 0.124 | -0.285 | 0.115 | 0.089 | 0.073 | 0.107 | 0.142 | 0.127 | 0.121 | 0.066 | 0.099 | 19.867 | ADOPT |
| E4_anchor_reclaim | X4_trendline_trail | 4297 | 0.335 | 1.283 | -0.474 | 0.115 | -0.252 | 0.112 | 0.077 | 0.057 | 0.087 | 0.143 | 0.124 | 0.106 | 0.066 | 0.107 | 19.722 | ADOPT |
| E5_score4 | X5_chandelier3atr | 6556 | 0.389 | 1.365 | -0.689 | 0.110 | -0.287 | 0.105 | 0.074 | 0.053 | 0.104 | 0.115 | 0.094 | 0.126 | 0.154 | 0.198 | 19.504 | REJECT |
| E3_stage2_transition | X7_stage_drop | 3126 | 0.319 | 1.440 | -0.516 | 0.108 | -0.284 | 0.103 | 0.058 | 0.032 | 0.110 | 0.105 | 0.064 | 0.152 | 0.081 | 0.137 | 18.307 | REJECT |
| E2_exhaustion_confluence | X3_target3R | 1250 | 0.318 | 2.650 | -1.096 | 0.097 | -1.035 | 0.097 | 0.002 | -0.071 | 0.051 | 0.150 | 0.131 | 0.065 | 0.164 | 0.249 | 15.578 | REJECT |
| E3_stage2_transition | X4_trendline_trail | 3131 | 0.287 | 1.285 | -0.387 | 0.092 | -0.223 | 0.088 | 0.051 | 0.029 | 0.081 | 0.106 | 0.065 | 0.120 | 0.066 | 0.116 | 13.763 | REJECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 1267 | 0.313 | 2.423 | -0.976 | 0.086 | -1.014 | 0.067 | -0.030 | -0.109 | 0.024 | 0.158 | 0.141 | 0.036 | 0.154 | 0.246 | 15.700 | REJECT |
| E4_anchor_reclaim | X6_partial1R_then_line | 4303 | 0.383 | 0.954 | -0.477 | 0.071 | -0.218 | 0.071 | 0.046 | 0.031 | 0.048 | 0.095 | 0.078 | 0.064 | 0.013 | 0.040 | 19.333 | ADOPT |
| E1_trigger_with_trend | X7_stage_drop | 555 | 0.443 | 0.493 | -0.265 | 0.071 | -0.046 | 0.068 | 0.002 | -0.037 | 0.022 | 0.127 | 0.038 | 0.105 | 0.081 | 0.209 | 3.654 | REJECT |
| E1_trigger_with_trend | X4_trendline_trail | 555 | 0.445 | 0.470 | -0.261 | 0.064 | -0.044 | 0.062 | -0.001 | -0.044 | 0.005 | 0.132 | 0.039 | 0.091 | 0.066 | 0.188 | 3.227 | REJECT |
| E5_score4 | X6_partial1R_then_line | 6858 | 0.411 | 0.976 | -0.575 | 0.063 | -0.213 | 0.063 | 0.039 | 0.027 | 0.048 | 0.079 | 0.066 | 0.060 | 0.013 | 0.035 | 19.054 | ADOPT |
| E3_stage2_transition | X1_time10 | 3011 | 0.507 | 0.717 | -0.646 | 0.046 | 0.011 | 0.046 | 0.014 | -0.004 | 0.044 | 0.047 | 0.034 | 0.057 | 0.046 | 0.086 | 9.122 | REJECT |
| E3_stage2_transition | X6_partial1R_then_line | 3131 | 0.328 | 0.927 | -0.388 | 0.044 | -0.203 | 0.044 | 0.015 | -0.001 | 0.035 | 0.054 | 0.028 | 0.060 | 0.013 | 0.045 | 13.500 | REJECT |
| E4_anchor_reclaim | X1_time10 | 3986 | 0.523 | 0.632 | -0.603 | 0.043 | 0.038 | 0.043 | 0.019 | -0.003 | 0.016 | 0.070 | 0.047 | 0.039 | 0.046 | 0.081 | 9.309 | REJECT |
| E1_trigger_with_trend | X6_partial1R_then_line | 555 | 0.447 | 0.409 | -0.261 | 0.038 | -0.043 | 0.038 | -0.012 | -0.042 | -0.006 | 0.088 | -0.000 | 0.078 | 0.013 | 0.086 | 3.225 | REJECT |
| E5_score4 | X1_time10 | 7616 | 0.501 | 0.771 | -0.697 | 0.038 | 0.001 | 0.038 | 0.016 | 0.005 | 0.024 | 0.053 | 0.042 | 0.033 | 0.046 | 0.071 | 8.943 | REJECT |
| E1b_trigger_counter_trend | X1_time10 | 2614 | 0.480 | 0.961 | -0.825 | 0.034 | -0.057 | 0.034 | -0.010 | -0.045 | 0.007 | 0.069 | 0.037 | 0.031 | 0.046 | 0.091 | 8.350 | REJECT |
| E2_exhaustion_confluence | X2_target2R | 1255 | 0.375 | 1.919 | -1.100 | 0.033 | -1.029 | 0.033 | -0.049 | -0.092 | -0.007 | 0.080 | 0.038 | 0.029 | 0.113 | 0.185 | 11.585 | REJECT |
| E1b_trigger_counter_trend | X7_stage_drop | 2800 | 0.451 | 0.352 | -0.320 | -0.017 | -0.038 | -0.017 | -0.036 | -0.044 | -0.016 | -0.018 | -0.005 | -0.028 | 0.081 | 0.139 | 2.235 | REJECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 2800 | 0.453 | 0.347 | -0.320 | -0.018 | -0.036 | -0.018 | -0.036 | -0.045 | -0.019 | -0.016 | -0.007 | -0.028 | 0.066 | 0.116 | 2.148 | REJECT |
| E1b_trigger_counter_trend | X6_partial1R_then_line | 2800 | 0.456 | 0.339 | -0.319 | -0.019 | -0.034 | -0.019 | -0.037 | -0.044 | -0.019 | -0.019 | -0.010 | -0.028 | 0.013 | 0.048 | 2.147 | REJECT |
| E2_exhaustion_confluence | X7_stage_drop | 1273 | 0.452 | 0.487 | -0.461 | -0.033 | -0.046 | -0.033 | -0.071 | -0.095 | -0.021 | -0.046 | -0.045 | -0.021 | 0.081 | 0.169 | 2.202 | REJECT |
| E2_exhaustion_confluence | X4_trendline_trail | 1273 | 0.451 | 0.474 | -0.461 | -0.039 | -0.046 | -0.039 | -0.075 | -0.102 | -0.034 | -0.046 | -0.048 | -0.031 | 0.066 | 0.146 | 2.095 | REJECT |
| E2_exhaustion_confluence | X6_partial1R_then_line | 1273 | 0.456 | 0.455 | -0.457 | -0.041 | -0.038 | -0.041 | -0.074 | -0.097 | -0.036 | -0.046 | -0.049 | -0.033 | 0.013 | 0.060 | 2.090 | REJECT |
| E2_exhaustion_confluence | X1_time10 | 1267 | 0.389 | 1.397 | -0.971 | -0.050 | -0.797 | -0.051 | -0.130 | -0.169 | -0.041 | -0.059 | -0.021 | -0.077 | 0.046 | 0.110 | 7.125 | REJECT |

### Exit rules ranked (trade-weighted across setups)

| exit | trades | mean_expectancy | random_mean | edge_over_random |
|---|---|---|---|---|
| X3_target3R | 15,298 | 0.211 | 0.164 | 0.047 |
| X2_target2R | 15,649 | 0.163 | 0.113 | 0.050 |
| X5_chandelier3atr | 17,401 | 0.127 | 0.154 | -0.027 |
| X7_stage_drop | 18,096 | 0.098 | 0.081 | 0.017 |
| X4_trendline_trail | 18,823 | 0.083 | 0.066 | 0.017 |
| X6_partial1R_then_line | 18,920 | 0.042 | 0.013 | 0.029 |
| X1_time10 | 19,021 | 0.037 | 0.046 | -0.009 |

## P1b · Sizing (fixed-fractional, max open positions = 5)

| setup | exit | risk_pct | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 0.005 | 0.021 | -0.100 | 0.212 | 175,132 |
| E1_trigger_with_trend | X3_target3R | 0.010 | 0.040 | -0.191 | 0.211 | 287,979 |
| E1_trigger_with_trend | X3_target3R | 0.020 | 0.073 | -0.349 | 0.208 | 653,634 |
| E1_trigger_with_trend | X5_chandelier3atr | 0.005 | 0.020 | -0.080 | 0.251 | 170,751 |
| E1_trigger_with_trend | X5_chandelier3atr | 0.010 | 0.038 | -0.157 | 0.245 | 274,684 |
| E1_trigger_with_trend | X5_chandelier3atr | 0.020 | 0.070 | -0.298 | 0.234 | 608,166 |
| E4_anchor_reclaim | X3_target3R | 0.005 | 0.030 | -0.132 | 0.230 | 223,461 |
| E4_anchor_reclaim | X3_target3R | 0.010 | 0.059 | -0.257 | 0.228 | 461,705 |
| E4_anchor_reclaim | X3_target3R | 0.020 | 0.109 | -0.474 | 0.229 | 1,592,095 |

## P2 · Market regime (SPY > 200-day average and Trend line rising)

| setup | exit | n_on | exp_on | n_off | exp_off | diff | diff_ci_low | verdict |
|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X4_trendline_trail | 236 | 0.062 | 319 | 0.066 | -0.004 | -0.188 | NO CLEAR EFFECT |
| E1_trigger_with_trend | X5_chandelier3atr | 225 | 0.072 | 300 | 0.447 | -0.375 | -0.823 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 747 | 0.004 | 2053 | -0.025 | 0.029 | -0.033 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 695 | 0.200 | 1907 | 0.128 | 0.072 | -0.162 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X4_trendline_trail | 314 | -0.086 | 959 | -0.024 | -0.062 | -0.170 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 311 | -0.014 | 956 | 0.119 | -0.133 | -0.493 | NO CLEAR EFFECT |
| E3_stage2_transition | X4_trendline_trail | 1869 | 0.090 | 1262 | 0.096 | -0.006 | -0.134 | NO CLEAR EFFECT |
| E3_stage2_transition | X5_chandelier3atr | 1709 | 0.157 | 1153 | 0.108 | 0.049 | -0.104 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X4_trendline_trail | 2608 | 0.126 | 1689 | 0.098 | 0.028 | -0.070 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X5_chandelier3atr | 2221 | 0.136 | 1368 | 0.113 | 0.023 | -0.086 | NO CLEAR EFFECT |
| E5_score4 | X4_trendline_trail | 4452 | 0.142 | 2315 | 0.089 | 0.053 | -0.052 | NO CLEAR EFFECT |
| E5_score4 | X5_chandelier3atr | 4412 | 0.125 | 2144 | 0.078 | 0.046 | -0.062 | NO CLEAR EFFECT |

## P3 · Earnings drift (stocks)

| test | n | mean | mean_vs_spy | hit_vs_spy | ci_low |
|---|---|---|---|---|---|
| Positive earnings gap → hold 20 bars | 751 | 0.016 | 0.010 | 0.531 |  |
| IFI setups ≤20 bars after positive gap (R, X4) | 805 | 0.165 |  |  | 0.083 |
| Same setups at other times (R, X4) | 18018 | 0.079 |  |  | 0.062 |

## P4 · Portfolio heat (E1_trigger_with_trend + X3_target3R)

| rule | cagr | max_dd | mar | final |
|---|---|---|---|---|
| No sector cap | 0.031 | -0.146 | 0.215 | 229,039 |
| Max 1 open per sector | 0.034 | -0.127 | 0.269 | 245,304 |

## P6 · Playbook portfolio (E4_anchor_reclaim + E1_trigger_with_trend, exit X3_target3R, 1 per symbol, 1 per sector, max 5 open)

| risk | trades | trades_per_year | expectancy | win_rate | longest_losing_streak | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|---|---|---|
| 0.50% | 1278 | 47.578 | 0.280 | 0.460 | 14 | 0.043 | -0.078 | 0.554 | 312,158 |
| 0.75% | 1278 | 47.578 | 0.280 | 0.460 | 14 | 0.064 | -0.115 | 0.560 | 535,627 |
| 1.00% | 1278 | 47.578 | 0.280 | 0.460 | 14 | 0.085 | -0.151 | 0.567 | 902,185 |

## E6 · Playbook E4 after a positive earnings gap (stocks)

| group | n | expectancy | ci_low | verdict |
|---|---|---|---|---|
| E4 ≤20 bars after positive gap | 201 | 0.422 |  |  |
| E4 at other times | 2981 | 0.265 |  |  |
| Difference (95% CI low) | 3182 | 0.157 | -0.014 | NO CLEAR EFFECT |

---
**How to read verdicts.** ADOPT = ≥ min trades, bootstrap CI above 0 after correcting for the number of tests, positive in both time halves and both symbol halves, and better than random entries with the same exits. PROMISING = everything except significance. UNSTABLE = fails a half. REJECT = not positive or not better than random.