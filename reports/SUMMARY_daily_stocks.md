# IFI Lab results: daily · stocks
_Run 2026-10-12 14:45 UTC · 61 symbols · 2000-01-03 to 2026-10-12 · split 2015-01-01 · 42 setup×exit tests (Bonferroni-adjusted)_

## P1 · Exits × setups (R per trade, after costs)

Random-entry control (same stops and exits), mean expectancy by exit: X1_time10 +0.315R, X2_target2R +0.072R, X3_target3R +0.136R, X4_trendline_trail +0.048R, X5_chandelier3atr +0.258R, X6_partial1R_then_line -0.015R, X7_stage_drop +0.056R

| setup | exit | n | win_rate | avg_win | avg_loss | expectancy | ci_low | ci_low_adj | exp_early | exp_late | exp_symA | exp_symB | random_mean | random_p95 | avg_bars | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 526 | 0.411 | 2.261 | -1.047 | 0.312 | 0.170 | 0.101 | 0.273 | 0.355 | 0.335 | 0.288 | 0.136 | 0.287 | 26.616 | ADOPT |
| E4_anchor_reclaim | X3_target3R | 3160 | 0.475 | 1.655 | -0.961 | 0.281 | 0.227 | 0.198 | 0.243 | 0.320 | 0.313 | 0.248 | 0.136 | 0.202 | 38.969 | ADOPT |
| E1_trigger_with_trend | X5_chandelier3atr | 528 | 0.432 | 1.666 | -0.786 | 0.273 | 0.125 | 0.053 | 0.205 | 0.347 | 0.363 | 0.181 | 0.258 | 0.389 | 19.864 | REJECT |
| E1_trigger_with_trend | X2_target2R | 527 | 0.454 | 1.788 | -1.052 | 0.236 | 0.111 | 0.027 | 0.241 | 0.230 | 0.232 | 0.240 | 0.072 | 0.196 | 21.383 | ADOPT |
| E4_anchor_reclaim | X2_target2R | 3164 | 0.492 | 1.454 | -0.963 | 0.226 | 0.180 | 0.160 | 0.201 | 0.253 | 0.248 | 0.204 | 0.072 | 0.129 | 34.572 | ADOPT |
| E5_score4 | X3_target3R | 5312 | 0.417 | 1.915 | -1.027 | 0.200 | 0.156 | 0.135 | 0.181 | 0.221 | 0.208 | 0.193 | 0.136 | 0.193 | 32.321 | ADOPT |
| E3_stage2_transition | X3_target3R | 2504 | 0.413 | 1.891 | -1.000 | 0.195 | 0.131 | 0.105 | 0.198 | 0.191 | 0.166 | 0.223 | 0.136 | 0.208 | 34.194 | REJECT |
| E1b_trigger_counter_trend | X3_target3R | 2533 | 0.387 | 2.169 | -1.058 | 0.190 | 0.125 | 0.076 | 0.125 | 0.277 | 0.189 | 0.192 | 0.136 | 0.206 | 25.752 | REJECT |
| E3_stage2_transition | X2_target2R | 2536 | 0.446 | 1.619 | -1.003 | 0.166 | 0.112 | 0.082 | 0.171 | 0.160 | 0.146 | 0.186 | 0.072 | 0.133 | 28.845 | ADOPT |
| E5_score4 | X2_target2R | 5615 | 0.451 | 1.607 | -1.025 | 0.162 | 0.128 | 0.105 | 0.143 | 0.183 | 0.170 | 0.154 | 0.072 | 0.115 | 27.747 | ADOPT |
| E4_anchor_reclaim | X7_stage_drop | 3901 | 0.367 | 1.369 | -0.553 | 0.152 | 0.113 | 0.087 | 0.127 | 0.177 | 0.167 | 0.136 | 0.056 | 0.121 | 23.609 | ADOPT |
| E1_trigger_with_trend | X1_time10 | 530 | 0.536 | 0.959 | -0.784 | 0.150 | 0.055 | -0.007 | 0.146 | 0.154 | 0.154 | 0.146 | 0.315 | 0.202 | 8.594 | REJECT |
| E3_stage2_transition | X5_chandelier3atr | 2855 | 0.394 | 1.379 | -0.666 | 0.139 | 0.089 | 0.065 | 0.131 | 0.149 | 0.102 | 0.177 | 0.258 | 1.449 | 20.639 | REJECT |
| E5_score4 | X7_stage_drop | 6411 | 0.353 | 1.588 | -0.651 | 0.138 | 0.099 | 0.071 | 0.127 | 0.151 | 0.130 | 0.147 | 0.056 | 0.110 | 22.511 | ADOPT |
| E4_anchor_reclaim | X5_chandelier3atr | 3567 | 0.420 | 1.138 | -0.597 | 0.131 | 0.092 | 0.076 | 0.088 | 0.176 | 0.153 | 0.109 | 0.258 | 1.199 | 21.650 | REJECT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 2623 | 0.377 | 1.726 | -0.837 | 0.128 | 0.063 | 0.030 | 0.028 | 0.263 | 0.135 | 0.122 | 0.258 | 1.558 | 19.308 | REJECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 1321 | 0.310 | 2.633 | -1.000 | 0.125 | -0.016 | -0.077 | 0.019 | 0.244 | 0.145 | 0.106 | 0.258 | 0.322 | 15.288 | REJECT |
| E4_anchor_reclaim | X4_trendline_trail | 4276 | 0.336 | 1.309 | -0.475 | 0.125 | 0.085 | 0.064 | 0.104 | 0.146 | 0.142 | 0.107 | 0.048 | 0.097 | 19.741 | ADOPT |
| E5_score4 | X4_trendline_trail | 6758 | 0.338 | 1.486 | -0.574 | 0.122 | 0.088 | 0.073 | 0.103 | 0.142 | 0.124 | 0.120 | 0.048 | 0.088 | 19.814 | ADOPT |
| E1b_trigger_counter_trend | X2_target2R | 2540 | 0.423 | 1.731 | -1.059 | 0.120 | 0.065 | 0.024 | 0.054 | 0.208 | 0.133 | 0.108 | 0.072 | 0.135 | 20.827 | REJECT |
| E5_score4 | X5_chandelier3atr | 6544 | 0.389 | 1.369 | -0.693 | 0.109 | 0.073 | 0.053 | 0.101 | 0.117 | 0.093 | 0.125 | 0.258 | 0.751 | 19.471 | REJECT |
| E3_stage2_transition | X7_stage_drop | 3119 | 0.319 | 1.438 | -0.515 | 0.108 | 0.059 | 0.031 | 0.110 | 0.106 | 0.067 | 0.150 | 0.056 | 0.126 | 18.298 | REJECT |
| E3_stage2_transition | X4_trendline_trail | 3124 | 0.288 | 1.279 | -0.387 | 0.092 | 0.049 | 0.021 | 0.081 | 0.106 | 0.068 | 0.117 | 0.048 | 0.109 | 13.756 | REJECT |
| E4_anchor_reclaim | X1_time10 | 3965 | 0.524 | 0.719 | -0.604 | 0.090 | 0.026 | 0.008 | 0.101 | 0.077 | 0.140 | 0.038 | 0.315 | 2.774 | 9.300 | REJECT |
| E4_anchor_reclaim | X6_partial1R_then_line | 4282 | 0.384 | 0.965 | -0.477 | 0.077 | 0.050 | 0.035 | 0.056 | 0.098 | 0.088 | 0.066 | -0.015 | 0.017 | 19.356 | ADOPT |
| E2_exhaustion_confluence | X3_target3R | 1304 | 0.318 | 2.626 | -1.114 | 0.076 | -0.023 | -0.090 | 0.032 | 0.125 | 0.104 | 0.051 | 0.136 | 0.230 | 14.977 | REJECT |
| E5_score4 | X6_partial1R_then_line | 6848 | 0.412 | 0.976 | -0.579 | 0.061 | 0.038 | 0.025 | 0.044 | 0.080 | 0.065 | 0.057 | -0.015 | 0.011 | 19.007 | ADOPT |
| E1_trigger_with_trend | X7_stage_drop | 558 | 0.441 | 0.480 | -0.276 | 0.057 | -0.006 | -0.028 | 0.027 | 0.091 | 0.033 | 0.083 | 0.056 | 0.203 | 3.588 | REJECT |
| E1_trigger_with_trend | X4_trendline_trail | 558 | 0.443 | 0.457 | -0.273 | 0.050 | -0.011 | -0.035 | 0.009 | 0.097 | 0.033 | 0.068 | 0.048 | 0.181 | 3.163 | REJECT |
| E3_stage2_transition | X1_time10 | 3004 | 0.508 | 0.716 | -0.646 | 0.046 | 0.015 | -0.006 | 0.045 | 0.048 | 0.037 | 0.055 | 0.315 | 3.635 | 9.112 | REJECT |
| E3_stage2_transition | X6_partial1R_then_line | 3124 | 0.328 | 0.926 | -0.388 | 0.044 | 0.014 | -0.007 | 0.035 | 0.053 | 0.029 | 0.058 | -0.015 | 0.024 | 13.493 | PROMISING (not significant after correction) |
| E5_score4 | X1_time10 | 7607 | 0.499 | 0.774 | -0.702 | 0.035 | 0.013 | 0.003 | 0.020 | 0.052 | 0.038 | 0.031 | 0.315 | 1.480 | 8.913 | REJECT |
| E1_trigger_with_trend | X6_partial1R_then_line | 558 | 0.444 | 0.404 | -0.273 | 0.028 | -0.019 | -0.044 | -0.002 | 0.062 | -0.006 | 0.064 | -0.015 | 0.069 | 3.161 | REJECT |
| E1b_trigger_counter_trend | X1_time10 | 2634 | 0.477 | 0.974 | -0.837 | 0.027 | -0.018 | -0.049 | -0.009 | 0.076 | 0.026 | 0.028 | 0.315 | 4.127 | 8.265 | REJECT |
| E2_exhaustion_confluence | X2_target2R | 1309 | 0.374 | 1.905 | -1.120 | 0.010 | -0.072 | -0.125 | -0.029 | 0.053 | 0.007 | 0.013 | 0.072 | 0.158 | 11.138 | REJECT |
| E2_exhaustion_confluence | X1_time10 | 1321 | 0.383 | 1.619 | -0.996 | 0.006 | -0.112 | -0.158 | -0.034 | 0.050 | -0.021 | 0.030 | 0.315 | 0.181 | 6.958 | REJECT |
| E1b_trigger_counter_trend | X7_stage_drop | 2828 | 0.449 | 0.364 | -0.342 | -0.025 | -0.046 | -0.058 | -0.028 | -0.021 | -0.013 | -0.036 | 0.056 | 0.134 | 2.223 | REJECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 2828 | 0.450 | 0.359 | -0.341 | -0.026 | -0.047 | -0.058 | -0.031 | -0.019 | -0.014 | -0.037 | 0.048 | 0.105 | 2.137 | REJECT |
| E1b_trigger_counter_trend | X6_partial1R_then_line | 2828 | 0.453 | 0.347 | -0.340 | -0.029 | -0.048 | -0.059 | -0.030 | -0.027 | -0.018 | -0.038 | -0.015 | 0.025 | 2.137 | REJECT |
| E2_exhaustion_confluence | X7_stage_drop | 1327 | 0.448 | 0.568 | -0.515 | -0.030 | -0.077 | -0.098 | -0.019 | -0.042 | -0.061 | -0.002 | 0.056 | 0.161 | 2.168 | REJECT |
| E2_exhaustion_confluence | X4_trendline_trail | 1327 | 0.447 | 0.555 | -0.515 | -0.037 | -0.083 | -0.107 | -0.032 | -0.042 | -0.064 | -0.012 | 0.048 | 0.137 | 2.066 | REJECT |
| E2_exhaustion_confluence | X6_partial1R_then_line | 1327 | 0.452 | 0.500 | -0.510 | -0.053 | -0.093 | -0.118 | -0.049 | -0.059 | -0.071 | -0.037 | -0.015 | 0.040 | 2.061 | REJECT |

### Exit rules ranked (trade-weighted across setups)

| exit | trades | mean_expectancy | random_mean | edge_over_random |
|---|---|---|---|---|
| X3_target3R | 15,339 | 0.208 | 0.136 | 0.072 |
| X2_target2R | 15,691 | 0.159 | 0.072 | 0.087 |
| X5_chandelier3atr | 17,438 | 0.128 | 0.258 | -0.131 |
| X7_stage_drop | 18,144 | 0.096 | 0.056 | 0.040 |
| X4_trendline_trail | 18,871 | 0.082 | 0.048 | 0.034 |
| X1_time10 | 19,061 | 0.048 | 0.315 | -0.267 |
| X6_partial1R_then_line | 18,967 | 0.039 | -0.015 | 0.055 |

## P1b · Sizing (fixed-fractional, max open positions = 5)

| setup | exit | risk_pct | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 0.005 | 0.019 | -0.100 | 0.195 | 167,081 |
| E1_trigger_with_trend | X3_target3R | 0.010 | 0.037 | -0.191 | 0.193 | 262,581 |
| E1_trigger_with_trend | X3_target3R | 0.020 | 0.066 | -0.349 | 0.188 | 546,945 |
| E4_anchor_reclaim | X3_target3R | 0.005 | 0.032 | -0.141 | 0.224 | 229,835 |
| E4_anchor_reclaim | X3_target3R | 0.010 | 0.061 | -0.264 | 0.232 | 490,610 |
| E4_anchor_reclaim | X3_target3R | 0.020 | 0.115 | -0.463 | 0.248 | 1,827,428 |
| E1_trigger_with_trend | X5_chandelier3atr | 0.005 | 0.020 | -0.078 | 0.258 | 169,666 |
| E1_trigger_with_trend | X5_chandelier3atr | 0.010 | 0.038 | -0.151 | 0.253 | 271,011 |
| E1_trigger_with_trend | X5_chandelier3atr | 0.020 | 0.069 | -0.284 | 0.242 | 590,269 |

## P2 · Market regime (SPY > 200-day average and Trend line rising)

| setup | exit | n_on | exp_on | n_off | exp_off | diff | diff_ci_low | verdict |
|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X4_trendline_trail | 240 | 0.030 | 318 | 0.066 | -0.036 | -0.206 | NO CLEAR EFFECT |
| E1_trigger_with_trend | X5_chandelier3atr | 229 | 0.039 | 299 | 0.452 | -0.413 | -0.822 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 749 | -0.003 | 2079 | -0.034 | 0.031 | -0.034 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 696 | 0.158 | 1927 | 0.117 | 0.041 | -0.161 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X4_trendline_trail | 329 | -0.051 | 998 | -0.032 | -0.020 | -0.166 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 326 | 0.077 | 995 | 0.141 | -0.063 | -0.548 | NO CLEAR EFFECT |
| E3_stage2_transition | X4_trendline_trail | 1869 | 0.088 | 1255 | 0.100 | -0.012 | -0.140 | NO CLEAR EFFECT |
| E3_stage2_transition | X5_chandelier3atr | 1709 | 0.157 | 1146 | 0.112 | 0.045 | -0.104 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X4_trendline_trail | 2603 | 0.140 | 1673 | 0.101 | 0.040 | -0.084 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X5_chandelier3atr | 2215 | 0.141 | 1352 | 0.115 | 0.025 | -0.096 | NO CLEAR EFFECT |
| E5_score4 | X4_trendline_trail | 4453 | 0.141 | 2305 | 0.085 | 0.056 | -0.053 | NO CLEAR EFFECT |
| E5_score4 | X5_chandelier3atr | 4415 | 0.125 | 2129 | 0.076 | 0.049 | -0.053 | NO CLEAR EFFECT |

## P3 · Earnings drift (stocks)

| test | n | mean | mean_vs_spy | hit_vs_spy | ci_low |
|---|---|---|---|---|---|
| Positive earnings gap → hold 20 bars | 752 | 0.017 | 0.010 | 0.532 |  |
| IFI setups ≤20 bars after positive gap (R, X4) | 800 | 0.169 |  |  | 0.081 |
| Same setups at other times (R, X4) | 18071 | 0.078 |  |  | 0.061 |

## P4 · Portfolio heat (E1_trigger_with_trend + X3_target3R)

| rule | cagr | max_dd | mar | final |
|---|---|---|---|---|
| No sector cap | 0.036 | -0.191 | 0.189 | 257,609 |
| Max 1 open per sector | 0.043 | -0.166 | 0.257 | 304,146 |

---
**How to read verdicts.** ADOPT = ≥ min trades, bootstrap CI above 0 after correcting for the number of tests, positive in both time halves and both symbol halves, and better than random entries with the same exits. PROMISING = everything except significance. UNSTABLE = fails a half. REJECT = not positive or not better than random.