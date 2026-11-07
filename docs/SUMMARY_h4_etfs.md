# IFI Lab results: h4 · etfs
_Run 2026-11-07 17:38 UTC · 16 symbols · 2023-11-10 to 2026-11-06 · split 2025-05-09 · 42 setup×exit tests (Bonferroni-adjusted) · engine v1.3.3_

## P1 · Exits × setups (R per trade, after costs)

Random-entry control (same stops and exits), mean expectancy by exit: X1_time10 -0.046R, X2_target2R -0.013R, X3_target3R +0.017R, X4_trendline_trail -0.044R, X5_chandelier3atr +0.003R, X6_partial1R_then_line -0.077R, X7_stage_drop -0.041R

| setup | exit | n | win_rate | avg_win | avg_loss | expectancy | median | exp_w10 | ci_low | ci_low_adj | exp_early | exp_late | exp_symA | exp_symB | random_mean | random_p95 | avg_bars | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E1b_trigger_counter_trend | X5_chandelier3atr | 154 | 0.429 | 2.246 | -0.893 | 0.452 | -0.317 | 0.444 | 0.108 | -0.098 | 0.498 | 0.403 | 0.241 | 0.637 | 0.003 | 0.255 | 19.364 | PROMISING (not significant after correction) |
| E1b_trigger_counter_trend | X3_target3R | 151 | 0.430 | 2.508 | -1.130 | 0.436 | -1.037 | 0.436 | 0.131 | -0.028 | 0.573 | 0.294 | 0.325 | 0.532 | 0.017 | 0.236 | 22.954 | PROMISING (not significant after correction) |
| E1_trigger_with_trend | X3_target3R | 40 | 0.425 | 2.189 | -1.098 | 0.299 | -1.031 | 0.299 | -0.234 | -0.501 | 0.452 | 0.174 | 0.267 | 0.334 | 0.017 | 0.465 | 23.975 | INCONCLUSIVE (too few trades) |
| E4_anchor_reclaim | X3_target3R | 188 | 0.484 | 1.560 | -0.957 | 0.261 | -0.090 | 0.261 | 0.057 | -0.069 | 0.197 | 0.325 | 0.285 | 0.241 | 0.017 | 0.212 | 41.777 | PROMISING (not significant after correction) |
| E1_trigger_with_trend | X2_target2R | 41 | 0.488 | 1.691 | -1.140 | 0.241 | -1.016 | 0.241 | -0.199 | -0.489 | 0.483 | 0.032 | 0.204 | 0.279 | -0.013 | 0.369 | 18.707 | INCONCLUSIVE (too few trades) |
| E4_anchor_reclaim | X2_target2R | 189 | 0.492 | 1.428 | -0.952 | 0.219 | -0.054 | 0.219 | 0.035 | -0.046 | 0.161 | 0.277 | 0.217 | 0.221 | -0.013 | 0.175 | 37.471 | PROMISING (not significant after correction) |
| E1_trigger_with_trend | X1_time10 | 41 | 0.585 | 1.082 | -1.037 | 0.203 | 0.561 | 0.203 | -0.156 | -0.334 | 0.488 | -0.043 | 0.278 | 0.125 | -0.046 | 0.324 | 8.463 | INCONCLUSIVE (too few trades) |
| E1_trigger_with_trend | X5_chandelier3atr | 41 | 0.512 | 1.304 | -0.972 | 0.194 | 0.103 | 0.194 | -0.200 | -0.441 | 0.442 | -0.021 | 0.135 | 0.255 | 0.003 | 0.520 | 17.463 | INCONCLUSIVE (too few trades) |
| E1b_trigger_counter_trend | X1_time10 | 156 | 0.532 | 1.187 | -0.938 | 0.193 | 0.121 | 0.193 | -0.033 | -0.150 | 0.392 | -0.028 | 0.073 | 0.300 | -0.046 | 0.150 | 8.077 | UNSTABLE (fails a split half) |
| E2_exhaustion_confluence | X1_time10 | 74 | 0.392 | 2.103 | -1.059 | 0.180 | -1.043 | 0.180 | -0.234 | -0.441 | 0.223 | 0.137 | 0.645 | -0.087 | -0.046 | 0.241 | 6.851 | REJECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 74 | 0.324 | 2.648 | -1.033 | 0.161 | -1.017 | 0.142 | -0.334 | -0.515 | 0.285 | 0.036 | 0.489 | -0.028 | 0.003 | 0.378 | 13.824 | REJECT |
| E1b_trigger_counter_trend | X2_target2R | 151 | 0.430 | 1.819 | -1.130 | 0.139 | -1.037 | 0.139 | -0.098 | -0.219 | 0.279 | -0.006 | 0.050 | 0.217 | -0.013 | 0.184 | 17.702 | REJECT |
| E3_stage2_transition | X3_target3R | 154 | 0.416 | 1.702 | -0.983 | 0.132 | -1.016 | 0.132 | -0.101 | -0.245 | 0.186 | 0.078 | 0.184 | 0.078 | 0.017 | 0.247 | 33.474 | REJECT |
| E1_trigger_with_trend | X6_partial1R_then_line | 44 | 0.614 | 0.391 | -0.307 | 0.122 | 0.132 | 0.122 | -0.009 | -0.089 | 0.203 | 0.047 | 0.116 | 0.128 | -0.077 | 0.184 | 3.841 | INCONCLUSIVE (too few trades) |
| E1_trigger_with_trend | X4_trendline_trail | 44 | 0.591 | 0.398 | -0.326 | 0.102 | 0.117 | 0.102 | -0.039 | -0.135 | 0.176 | 0.034 | 0.118 | 0.084 | -0.044 | 0.350 | 3.864 | INCONCLUSIVE (too few trades) |
| E4_anchor_reclaim | X7_stage_drop | 229 | 0.376 | 1.115 | -0.513 | 0.098 | -0.165 | 0.098 | -0.042 | -0.112 | 0.142 | 0.055 | 0.146 | 0.059 | -0.041 | 0.135 | 23.489 | REJECT |
| E1_trigger_with_trend | X7_stage_drop | 44 | 0.591 | 0.391 | -0.326 | 0.098 | 0.117 | 0.098 | -0.043 | -0.135 | 0.176 | 0.027 | 0.118 | 0.075 | -0.041 | 0.403 | 3.886 | INCONCLUSIVE (too few trades) |
| E4_anchor_reclaim | X4_trendline_trail | 242 | 0.388 | 1.003 | -0.484 | 0.094 | -0.199 | 0.094 | -0.031 | -0.096 | 0.101 | 0.086 | 0.168 | 0.031 | -0.044 | 0.126 | 20.512 | REJECT |
| E5_score4 | X2_target2R | 322 | 0.441 | 1.517 | -1.031 | 0.093 | -1.014 | 0.093 | -0.048 | -0.122 | 0.029 | 0.143 | 0.162 | 0.025 | -0.013 | 0.126 | 28.394 | REJECT |
| E4_anchor_reclaim | X6_partial1R_then_line | 242 | 0.434 | 0.853 | -0.497 | 0.089 | -0.114 | 0.089 | -0.013 | -0.057 | 0.112 | 0.066 | 0.134 | 0.051 | -0.077 | 0.033 | 20.326 | PROMISING (not significant after correction) |
| E3_stage2_transition | X7_stage_drop | 181 | 0.331 | 1.316 | -0.534 | 0.079 | -0.256 | 0.072 | -0.098 | -0.213 | 0.129 | 0.028 | 0.136 | 0.024 | -0.041 | 0.151 | 20.105 | REJECT |
| E3_stage2_transition | X2_target2R | 156 | 0.429 | 1.492 | -0.987 | 0.078 | -1.014 | 0.078 | -0.128 | -0.226 | 0.148 | 0.006 | 0.133 | 0.020 | -0.013 | 0.175 | 30.013 | REJECT |
| E4_anchor_reclaim | X5_chandelier3atr | 222 | 0.428 | 0.892 | -0.546 | 0.069 | -0.109 | 0.069 | -0.053 | -0.108 | 0.133 | 0.009 | 0.113 | 0.034 | 0.003 | 0.224 | 18.725 | REJECT |
| E3_stage2_transition | X4_trendline_trail | 181 | 0.309 | 1.130 | -0.411 | 0.066 | -0.208 | 0.059 | -0.091 | -0.173 | 0.146 | -0.017 | 0.201 | -0.068 | -0.044 | 0.148 | 15.381 | REJECT |
| E4_anchor_reclaim | X1_time10 | 231 | 0.576 | 0.571 | -0.662 | 0.048 | 0.155 | 0.048 | -0.048 | -0.128 | 0.047 | 0.049 | 0.035 | 0.058 | -0.046 | 0.105 | 9.212 | REJECT |
| E2_exhaustion_confluence | X3_target3R | 74 | 0.311 | 2.714 | -1.167 | 0.039 | -1.062 | 0.039 | -0.374 | -0.591 | 0.015 | 0.062 | 0.214 | -0.062 | 0.017 | 0.339 | 13.095 | REJECT |
| E3_stage2_transition | X6_partial1R_then_line | 181 | 0.337 | 0.901 | -0.417 | 0.027 | -0.205 | 0.027 | -0.097 | -0.154 | 0.095 | -0.043 | 0.096 | -0.041 | -0.077 | 0.048 | 15.287 | REJECT |
| E5_score4 | X3_target3R | 312 | 0.388 | 1.661 | -1.026 | 0.016 | -1.026 | 0.016 | -0.145 | -0.229 | -0.007 | 0.035 | 0.064 | -0.031 | 0.017 | 0.167 | 32.269 | REJECT |
| E5_score4 | X7_stage_drop | 373 | 0.327 | 1.359 | -0.645 | 0.010 | -0.340 | 0.010 | -0.120 | -0.205 | 0.100 | -0.057 | 0.038 | -0.014 | -0.041 | 0.102 | 22.024 | REJECT |
| E3_stage2_transition | X5_chandelier3atr | 172 | 0.390 | 1.074 | -0.669 | 0.010 | -0.231 | 0.010 | -0.151 | -0.252 | 0.060 | -0.039 | 0.060 | -0.039 | 0.003 | 0.241 | 18.349 | REJECT |
| E5_score4 | X4_trendline_trail | 384 | 0.326 | 1.250 | -0.595 | 0.005 | -0.333 | 0.005 | -0.118 | -0.183 | 0.070 | -0.043 | 0.056 | -0.039 | -0.044 | 0.085 | 19.594 | REJECT |
| E5_score4 | X6_partial1R_then_line | 390 | 0.423 | 0.837 | -0.610 | 0.002 | -0.229 | 0.002 | -0.081 | -0.124 | 0.077 | -0.053 | 0.054 | -0.044 | -0.077 | 0.011 | 18.562 | REJECT |
| E3_stage2_transition | X1_time10 | 174 | 0.534 | 0.568 | -0.694 | -0.020 | 0.058 | -0.020 | -0.137 | -0.185 | -0.005 | -0.035 | 0.012 | -0.052 | -0.046 | 0.138 | 8.966 | REJECT |
| E5_score4 | X1_time10 | 436 | 0.525 | 0.628 | -0.770 | -0.036 | 0.034 | -0.036 | -0.119 | -0.170 | 0.029 | -0.081 | 0.050 | -0.113 | -0.046 | 0.067 | 8.759 | REJECT |
| E5_score4 | X5_chandelier3atr | 401 | 0.342 | 1.044 | -0.667 | -0.082 | -0.339 | -0.082 | -0.186 | -0.238 | 0.027 | -0.161 | -0.041 | -0.119 | 0.003 | 0.162 | 16.589 | REJECT |
| E2_exhaustion_confluence | X4_trendline_trail | 74 | 0.432 | 0.438 | -0.507 | -0.098 | -0.075 | -0.098 | -0.243 | -0.326 | -0.043 | -0.154 | -0.050 | -0.126 | -0.044 | 0.232 | 2.541 | REJECT |
| E2_exhaustion_confluence | X6_partial1R_then_line | 74 | 0.432 | 0.431 | -0.507 | -0.101 | -0.075 | -0.101 | -0.243 | -0.328 | -0.050 | -0.153 | -0.054 | -0.129 | -0.077 | 0.138 | 2.541 | REJECT |
| E1b_trigger_counter_trend | X6_partial1R_then_line | 167 | 0.449 | 0.259 | -0.410 | -0.110 | -0.040 | -0.110 | -0.194 | -0.247 | -0.104 | -0.115 | -0.166 | -0.060 | -0.077 | 0.060 | 2.060 | REJECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 167 | 0.449 | 0.252 | -0.410 | -0.113 | -0.040 | -0.113 | -0.196 | -0.251 | -0.107 | -0.119 | -0.173 | -0.060 | -0.044 | 0.153 | 2.060 | REJECT |
| E1b_trigger_counter_trend | X7_stage_drop | 167 | 0.449 | 0.250 | -0.410 | -0.114 | -0.040 | -0.114 | -0.197 | -0.251 | -0.109 | -0.119 | -0.175 | -0.060 | -0.041 | 0.156 | 2.078 | REJECT |
| E2_exhaustion_confluence | X7_stage_drop | 74 | 0.432 | 0.414 | -0.516 | -0.114 | -0.075 | -0.114 | -0.256 | -0.334 | -0.065 | -0.164 | -0.050 | -0.151 | -0.041 | 0.284 | 2.595 | REJECT |
| E2_exhaustion_confluence | X2_target2R | 74 | 0.338 | 1.933 | -1.167 | -0.120 | -1.062 | -0.120 | -0.462 | -0.687 | -0.183 | -0.057 | 0.050 | -0.217 | -0.013 | 0.286 | 9.784 | REJECT |

### Exit rules ranked (trade-weighted across setups)

| exit | trades | mean_expectancy | random_mean | edge_over_random |
|---|---|---|---|---|
| X3_target3R | 919 | 0.169 | 0.017 | 0.152 |
| X2_target2R | 933 | 0.113 | -0.013 | 0.126 |
| X5_chandelier3atr | 1,064 | 0.069 | 0.003 | 0.066 |
| X1_time10 | 1,112 | 0.039 | -0.046 | 0.085 |
| X7_stage_drop | 1,068 | 0.016 | -0.041 | 0.057 |
| X4_trendline_trail | 1,092 | 0.014 | -0.044 | 0.057 |
| X6_partial1R_then_line | 1,098 | 0.006 | -0.077 | 0.083 |

## P1b · Sizing (fixed-fractional, max open positions = 5)

| setup | exit | risk_pct | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|
| E1b_trigger_counter_trend | X5_chandelier3atr | 0.005 | 0.065 | -0.119 | 0.547 | 119,254 |
| E1b_trigger_counter_trend | X5_chandelier3atr | 0.010 | 0.125 | -0.230 | 0.542 | 138,916 |
| E1b_trigger_counter_trend | X5_chandelier3atr | 0.020 | 0.226 | -0.427 | 0.529 | 176,783 |
| E1b_trigger_counter_trend | X3_target3R | 0.005 | 0.080 | -0.119 | 0.672 | 123,954 |
| E1b_trigger_counter_trend | X3_target3R | 0.010 | 0.154 | -0.226 | 0.682 | 149,292 |
| E1b_trigger_counter_trend | X3_target3R | 0.020 | 0.281 | -0.410 | 0.686 | 199,896 |
| E4_anchor_reclaim | X3_target3R | 0.005 | 0.037 | -0.069 | 0.533 | 110,649 |
| E4_anchor_reclaim | X3_target3R | 0.010 | 0.072 | -0.135 | 0.532 | 121,261 |
| E4_anchor_reclaim | X3_target3R | 0.020 | 0.134 | -0.255 | 0.525 | 141,786 |

## P2 · Market regime (SPY > 200-day average and Trend line rising)

| setup | exit | n_on | exp_on | n_off | exp_off | diff | diff_ci_low | verdict |
|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X4_trendline_trail | 18 | 0.196 | 26 | 0.037 | 0.159 | -0.285 | NO CLEAR EFFECT |
| E1_trigger_with_trend | X5_chandelier3atr | 15 | 0.355 | 26 | 0.100 | 0.255 | -0.962 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 41 | -0.246 | 126 | -0.069 | -0.177 | -0.566 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 35 | 0.540 | 119 | 0.426 | 0.113 | -1.039 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X4_trendline_trail | 29 | -0.287 | 45 | 0.023 | -0.311 | -0.744 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 29 | -0.234 | 45 | 0.415 | -0.649 | -2.073 | NO CLEAR EFFECT |
| E3_stage2_transition | X4_trendline_trail | 118 | -0.033 | 63 | 0.252 | -0.285 | -1.100 | NO CLEAR EFFECT |
| E3_stage2_transition | X5_chandelier3atr | 112 | -0.063 | 60 | 0.147 | -0.211 | -0.749 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X4_trendline_trail | 173 | -0.022 | 69 | 0.385 | -0.407 | -0.952 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X5_chandelier3atr | 158 | -0.052 | 64 | 0.368 | -0.419 | -0.888 | NO CLEAR EFFECT |
| E5_score4 | X4_trendline_trail | 287 | -0.124 | 97 | 0.389 | -0.513 | -1.036 | NO CLEAR EFFECT |
| E5_score4 | X5_chandelier3atr | 302 | -0.147 | 99 | 0.116 | -0.263 | -0.624 | NO CLEAR EFFECT |

## P4 · Portfolio heat (E1b_trigger_counter_trend + X5_chandelier3atr)

| rule | cagr | max_dd | mar | final |
|---|---|---|---|---|
| No sector cap | 0.067 | -0.176 | 0.384 | 120,047 |
| Max 1 open per sector | 0.067 | -0.176 | 0.384 | 120,047 |

## P6 · Playbook portfolio (E4_anchor_reclaim + E1_trigger_with_trend, exit X3_target3R, 1 per symbol, 1 per sector, max 5 open)

| risk | trades | trades_per_year | expectancy | win_rate | longest_losing_streak | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|---|---|---|
| 0.50% | 208 | 74.776 | 0.294 | 0.481 | 13 | 0.076 | -0.080 | 0.945 | 122,535 |
| 0.75% | 208 | 74.776 | 0.294 | 0.481 | 13 | 0.113 | -0.118 | 0.955 | 134,674 |
| 1.00% | 208 | 74.776 | 0.294 | 0.481 | 13 | 0.150 | -0.155 | 0.964 | 147,342 |

---
**How to read verdicts.** ADOPT = ≥ min trades, bootstrap CI above 0 after correcting for the number of tests, positive in both time halves and both symbol halves, and better than random entries with the same exits. PROMISING = everything except significance. UNSTABLE = fails a half. REJECT = not positive or not better than random.