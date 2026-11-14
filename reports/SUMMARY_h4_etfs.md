# IFI Lab results: h4 · etfs
_Run 2026-11-14 17:48 UTC · 16 symbols · 2023-11-10 to 2026-11-13 · split 2025-05-12 · 42 setup×exit tests (Bonferroni-adjusted) · engine v1.3.3_

## P1 · Exits × setups (R per trade, after costs)

Random-entry control (same stops and exits), mean expectancy by exit: X1_time10 +0.053R, X2_target2R +0.074R, X3_target3R +0.131R, X4_trendline_trail +0.056R, X5_chandelier3atr +0.097R, X6_partial1R_then_line -0.003R, X7_stage_drop +0.063R

| setup | exit | n | win_rate | avg_win | avg_loss | expectancy | median | exp_w10 | ci_low | ci_low_adj | exp_early | exp_late | exp_symA | exp_symB | random_mean | random_p95 | avg_bars | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E1b_trigger_counter_trend | X5_chandelier3atr | 156 | 0.436 | 2.207 | -0.893 | 0.458 | -0.280 | 0.450 | 0.119 | -0.119 | 0.498 | 0.416 | 0.259 | 0.637 | 0.097 | 0.416 | 19.295 | PROMISING (not significant after correction) |
| E1b_trigger_counter_trend | X3_target3R | 153 | 0.444 | 2.402 | -1.139 | 0.435 | -1.036 | 0.435 | 0.135 | -0.018 | 0.573 | 0.295 | 0.325 | 0.532 | 0.131 | 0.371 | 22.837 | PROMISING (not significant after correction) |
| E1_trigger_with_trend | X3_target3R | 40 | 0.425 | 2.189 | -1.098 | 0.299 | -1.031 | 0.299 | -0.234 | -0.501 | 0.452 | 0.174 | 0.267 | 0.334 | 0.131 | 0.594 | 23.975 | INCONCLUSIVE (too few trades) |
| E4_anchor_reclaim | X3_target3R | 190 | 0.479 | 1.580 | -0.939 | 0.267 | -0.070 | 0.267 | 0.076 | -0.028 | 0.197 | 0.335 | 0.281 | 0.256 | 0.131 | 0.342 | 41.568 | REJECT |
| E1_trigger_with_trend | X2_target2R | 41 | 0.488 | 1.691 | -1.140 | 0.241 | -1.016 | 0.241 | -0.199 | -0.489 | 0.483 | 0.032 | 0.204 | 0.279 | 0.074 | 0.473 | 18.707 | INCONCLUSIVE (too few trades) |
| E4_anchor_reclaim | X2_target2R | 191 | 0.487 | 1.445 | -0.933 | 0.225 | -0.054 | 0.225 | 0.050 | -0.072 | 0.161 | 0.287 | 0.214 | 0.234 | 0.074 | 0.244 | 37.257 | REJECT |
| E1_trigger_with_trend | X1_time10 | 41 | 0.585 | 1.082 | -1.037 | 0.203 | 0.561 | 0.203 | -0.156 | -0.334 | 0.488 | -0.043 | 0.278 | 0.125 | 0.053 | 0.438 | 8.463 | INCONCLUSIVE (too few trades) |
| E1b_trigger_counter_trend | X1_time10 | 158 | 0.538 | 1.172 | -0.938 | 0.197 | 0.100 | 0.197 | -0.008 | -0.211 | 0.392 | -0.013 | 0.086 | 0.300 | 0.053 | 0.251 | 8.095 | REJECT |
| E1_trigger_with_trend | X5_chandelier3atr | 41 | 0.512 | 1.304 | -0.972 | 0.194 | 0.103 | 0.194 | -0.200 | -0.441 | 0.442 | -0.021 | 0.135 | 0.255 | 0.097 | 0.661 | 17.463 | INCONCLUSIVE (too few trades) |
| E2_exhaustion_confluence | X1_time10 | 75 | 0.387 | 2.103 | -1.059 | 0.164 | -1.045 | 0.164 | -0.249 | -0.438 | 0.223 | 0.106 | 0.645 | -0.107 | 0.053 | 0.334 | 6.813 | REJECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 75 | 0.320 | 2.648 | -1.033 | 0.145 | -1.042 | 0.126 | -0.355 | -0.561 | 0.285 | 0.008 | 0.489 | -0.049 | 0.097 | 0.551 | 13.693 | REJECT |
| E1b_trigger_counter_trend | X2_target2R | 153 | 0.444 | 1.743 | -1.139 | 0.142 | -1.036 | 0.142 | -0.107 | -0.238 | 0.279 | 0.003 | 0.057 | 0.217 | 0.074 | 0.270 | 17.654 | REJECT |
| E3_stage2_transition | X3_target3R | 154 | 0.416 | 1.713 | -0.986 | 0.136 | -1.016 | 0.136 | -0.097 | -0.244 | 0.186 | 0.085 | 0.182 | 0.088 | 0.131 | 0.367 | 33.669 | REJECT |
| E1_trigger_with_trend | X6_partial1R_then_line | 44 | 0.614 | 0.391 | -0.307 | 0.122 | 0.132 | 0.122 | -0.009 | -0.089 | 0.203 | 0.047 | 0.116 | 0.128 | -0.003 | 0.296 | 3.841 | INCONCLUSIVE (too few trades) |
| E4_anchor_reclaim | X7_stage_drop | 231 | 0.372 | 1.152 | -0.507 | 0.111 | -0.164 | 0.111 | -0.035 | -0.118 | 0.142 | 0.081 | 0.154 | 0.075 | 0.063 | 0.315 | 23.519 | REJECT |
| E4_anchor_reclaim | X4_trendline_trail | 244 | 0.385 | 1.037 | -0.478 | 0.105 | -0.190 | 0.105 | -0.026 | -0.110 | 0.101 | 0.110 | 0.176 | 0.047 | 0.056 | 0.274 | 20.566 | REJECT |
| E1_trigger_with_trend | X4_trendline_trail | 44 | 0.591 | 0.398 | -0.326 | 0.102 | 0.117 | 0.102 | -0.039 | -0.135 | 0.176 | 0.034 | 0.118 | 0.084 | 0.056 | 0.539 | 3.864 | INCONCLUSIVE (too few trades) |
| E1_trigger_with_trend | X7_stage_drop | 44 | 0.591 | 0.391 | -0.326 | 0.098 | 0.117 | 0.098 | -0.043 | -0.135 | 0.176 | 0.027 | 0.118 | 0.075 | 0.063 | 0.572 | 3.886 | INCONCLUSIVE (too few trades) |
| E4_anchor_reclaim | X6_partial1R_then_line | 244 | 0.430 | 0.869 | -0.491 | 0.094 | -0.105 | 0.094 | -0.010 | -0.062 | 0.112 | 0.076 | 0.137 | 0.058 | -0.003 | 0.122 | 20.381 | REJECT |
| E5_score4 | X2_target2R | 324 | 0.438 | 1.521 | -1.022 | 0.093 | -1.012 | 0.093 | -0.054 | -0.154 | 0.029 | 0.143 | 0.157 | 0.029 | 0.074 | 0.202 | 28.290 | REJECT |
| E3_stage2_transition | X7_stage_drop | 181 | 0.331 | 1.328 | -0.534 | 0.084 | -0.256 | 0.076 | -0.095 | -0.211 | 0.129 | 0.037 | 0.136 | 0.032 | 0.063 | 0.357 | 20.215 | REJECT |
| E3_stage2_transition | X2_target2R | 156 | 0.429 | 1.502 | -0.989 | 0.081 | -1.014 | 0.081 | -0.127 | -0.221 | 0.148 | 0.012 | 0.131 | 0.028 | 0.074 | 0.264 | 30.122 | REJECT |
| E4_anchor_reclaim | X5_chandelier3atr | 224 | 0.424 | 0.892 | -0.539 | 0.068 | -0.099 | 0.068 | -0.049 | -0.115 | 0.133 | 0.008 | 0.111 | 0.034 | 0.097 | 0.358 | 18.621 | REJECT |
| E3_stage2_transition | X4_trendline_trail | 181 | 0.309 | 1.133 | -0.411 | 0.067 | -0.208 | 0.060 | -0.089 | -0.172 | 0.146 | -0.015 | 0.201 | -0.066 | 0.056 | 0.349 | 15.436 | REJECT |
| E4_anchor_reclaim | X1_time10 | 233 | 0.571 | 0.571 | -0.650 | 0.047 | 0.151 | 0.047 | -0.047 | -0.124 | 0.047 | 0.047 | 0.034 | 0.057 | 0.053 | 0.213 | 9.193 | REJECT |
| E3_stage2_transition | X6_partial1R_then_line | 181 | 0.337 | 0.902 | -0.417 | 0.028 | -0.205 | 0.028 | -0.096 | -0.154 | 0.095 | -0.042 | 0.096 | -0.040 | -0.003 | 0.149 | 15.343 | REJECT |
| E5_score4 | X3_target3R | 314 | 0.385 | 1.692 | -1.017 | 0.027 | -1.026 | 0.027 | -0.134 | -0.220 | -0.007 | 0.054 | 0.072 | -0.018 | 0.131 | 0.304 | 32.306 | REJECT |
| E2_exhaustion_confluence | X3_target3R | 75 | 0.307 | 2.714 | -1.165 | 0.024 | -1.062 | 0.024 | -0.388 | -0.575 | 0.015 | 0.033 | 0.214 | -0.082 | 0.131 | 0.483 | 12.973 | REJECT |
| E5_score4 | X7_stage_drop | 375 | 0.328 | 1.371 | -0.643 | 0.018 | -0.339 | 0.018 | -0.114 | -0.212 | 0.100 | -0.044 | 0.041 | -0.003 | 0.063 | 0.253 | 22.032 | REJECT |
| E5_score4 | X4_trendline_trail | 386 | 0.326 | 1.258 | -0.593 | 0.011 | -0.331 | 0.011 | -0.109 | -0.184 | 0.070 | -0.033 | 0.059 | -0.031 | 0.056 | 0.236 | 19.588 | REJECT |
| E3_stage2_transition | X5_chandelier3atr | 172 | 0.390 | 1.074 | -0.669 | 0.010 | -0.231 | 0.010 | -0.151 | -0.252 | 0.060 | -0.039 | 0.060 | -0.039 | 0.097 | 0.408 | 18.349 | REJECT |
| E5_score4 | X6_partial1R_then_line | 392 | 0.423 | 0.839 | -0.608 | 0.005 | -0.226 | 0.005 | -0.080 | -0.123 | 0.077 | -0.048 | 0.055 | -0.040 | -0.003 | 0.097 | 18.561 | REJECT |
| E3_stage2_transition | X1_time10 | 174 | 0.534 | 0.568 | -0.694 | -0.020 | 0.058 | -0.020 | -0.137 | -0.185 | -0.005 | -0.035 | 0.012 | -0.052 | 0.053 | 0.242 | 8.966 | REJECT |
| E5_score4 | X1_time10 | 438 | 0.523 | 0.628 | -0.764 | -0.036 | 0.034 | -0.036 | -0.120 | -0.160 | 0.029 | -0.082 | 0.047 | -0.113 | 0.053 | 0.166 | 8.753 | REJECT |
| E5_score4 | X5_chandelier3atr | 403 | 0.340 | 1.044 | -0.664 | -0.084 | -0.339 | -0.084 | -0.190 | -0.234 | 0.027 | -0.162 | -0.044 | -0.119 | 0.097 | 0.296 | 16.543 | REJECT |
| E2_exhaustion_confluence | X4_trendline_trail | 75 | 0.427 | 0.438 | -0.510 | -0.105 | -0.080 | -0.105 | -0.245 | -0.312 | -0.043 | -0.166 | -0.050 | -0.136 | 0.056 | 0.431 | 2.533 | REJECT |
| E2_exhaustion_confluence | X6_partial1R_then_line | 75 | 0.427 | 0.431 | -0.510 | -0.108 | -0.080 | -0.108 | -0.246 | -0.313 | -0.050 | -0.165 | -0.054 | -0.139 | -0.003 | 0.242 | 2.533 | REJECT |
| E1b_trigger_counter_trend | X6_partial1R_then_line | 169 | 0.444 | 0.259 | -0.404 | -0.110 | -0.047 | -0.110 | -0.193 | -0.247 | -0.104 | -0.116 | -0.166 | -0.060 | -0.003 | 0.147 | 2.059 | REJECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 169 | 0.444 | 0.252 | -0.404 | -0.113 | -0.047 | -0.113 | -0.195 | -0.248 | -0.107 | -0.120 | -0.172 | -0.060 | 0.056 | 0.329 | 2.059 | REJECT |
| E1b_trigger_counter_trend | X7_stage_drop | 169 | 0.444 | 0.250 | -0.404 | -0.114 | -0.047 | -0.114 | -0.196 | -0.248 | -0.109 | -0.120 | -0.174 | -0.060 | 0.063 | 0.353 | 2.077 | REJECT |
| E2_exhaustion_confluence | X7_stage_drop | 75 | 0.427 | 0.414 | -0.519 | -0.121 | -0.080 | -0.121 | -0.256 | -0.330 | -0.065 | -0.176 | -0.050 | -0.161 | 0.063 | 0.568 | 2.587 | REJECT |
| E2_exhaustion_confluence | X2_target2R | 75 | 0.333 | 1.933 | -1.165 | -0.132 | -1.061 | -0.132 | -0.476 | -0.620 | -0.183 | -0.083 | 0.050 | -0.234 | 0.074 | 0.340 | 9.707 | REJECT |

### Exit rules ranked (trade-weighted across setups)

| exit | trades | mean_expectancy | random_mean | edge_over_random |
|---|---|---|---|---|
| X3_target3R | 926 | 0.173 | 0.131 | 0.042 |
| X2_target2R | 940 | 0.114 | 0.074 | 0.040 |
| X5_chandelier3atr | 1,071 | 0.069 | 0.097 | -0.029 |
| X1_time10 | 1,119 | 0.039 | 0.053 | -0.015 |
| X7_stage_drop | 1,075 | 0.022 | 0.063 | -0.042 |
| X4_trendline_trail | 1,099 | 0.018 | 0.056 | -0.038 |
| X6_partial1R_then_line | 1,105 | 0.008 | -0.003 | 0.011 |

## P1b · Sizing (fixed-fractional, max open positions = 5)

| setup | exit | risk_pct | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|
| E1b_trigger_counter_trend | X5_chandelier3atr | 0.005 | 0.080 | -0.106 | 0.754 | 124,214 |
| E1b_trigger_counter_trend | X5_chandelier3atr | 0.010 | 0.155 | -0.203 | 0.764 | 150,063 |
| E1b_trigger_counter_trend | X5_chandelier3atr | 0.020 | 0.286 | -0.374 | 0.766 | 203,256 |
| E1b_trigger_counter_trend | X3_target3R | 0.005 | 0.076 | -0.119 | 0.642 | 122,949 |
| E1b_trigger_counter_trend | X3_target3R | 0.010 | 0.147 | -0.226 | 0.649 | 146,992 |
| E1b_trigger_counter_trend | X3_target3R | 0.020 | 0.266 | -0.410 | 0.649 | 194,259 |
| E4_anchor_reclaim | X3_target3R | 0.005 | 0.041 | -0.069 | 0.591 | 111,933 |
| E4_anchor_reclaim | X3_target3R | 0.010 | 0.080 | -0.135 | 0.594 | 124,102 |
| E4_anchor_reclaim | X3_target3R | 0.020 | 0.152 | -0.255 | 0.596 | 148,584 |

## P2 · Market regime (SPY > 200-day average and Trend line rising)

| setup | exit | n_on | exp_on | n_off | exp_off | diff | diff_ci_low | verdict |
|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X4_trendline_trail | 18 | 0.196 | 26 | 0.037 | 0.159 | -0.285 | NO CLEAR EFFECT |
| E1_trigger_with_trend | X5_chandelier3atr | 15 | 0.355 | 26 | 0.100 | 0.255 | -0.962 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 41 | -0.246 | 128 | -0.070 | -0.176 | -0.555 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 35 | 0.540 | 121 | 0.434 | 0.105 | -1.087 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X4_trendline_trail | 29 | -0.287 | 46 | 0.009 | -0.297 | -0.693 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 29 | -0.234 | 46 | 0.383 | -0.617 | -1.976 | NO CLEAR EFFECT |
| E3_stage2_transition | X4_trendline_trail | 118 | -0.033 | 63 | 0.255 | -0.288 | -1.106 | NO CLEAR EFFECT |
| E3_stage2_transition | X5_chandelier3atr | 112 | -0.063 | 60 | 0.147 | -0.211 | -0.749 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X4_trendline_trail | 173 | -0.015 | 71 | 0.398 | -0.412 | -1.008 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X5_chandelier3atr | 158 | -0.052 | 66 | 0.355 | -0.406 | -0.861 | NO CLEAR EFFECT |
| E5_score4 | X4_trendline_trail | 287 | -0.118 | 99 | 0.383 | -0.501 | -1.099 | NO CLEAR EFFECT |
| E5_score4 | X5_chandelier3atr | 302 | -0.147 | 101 | 0.107 | -0.255 | -0.702 | NO CLEAR EFFECT |

## P4 · Portfolio heat (E1b_trigger_counter_trend + X5_chandelier3atr)

| rule | cagr | max_dd | mar | final |
|---|---|---|---|---|
| No sector cap | 0.082 | -0.156 | 0.524 | 124,725 |
| Max 1 open per sector | 0.082 | -0.156 | 0.524 | 124,725 |

## P6 · Playbook portfolio (E4_anchor_reclaim + E1_trigger_with_trend, exit X3_target3R, 1 per symbol, 1 per sector, max 5 open)

| risk | trades | trades_per_year | expectancy | win_rate | longest_losing_streak | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|---|---|---|
| 0.50% | 210 | 74.978 | 0.298 | 0.476 | 13 | 0.067 | -0.080 | 0.831 | 119,835 |
| 0.75% | 210 | 74.978 | 0.298 | 0.476 | 13 | 0.099 | -0.118 | 0.838 | 130,353 |
| 1.00% | 210 | 74.978 | 0.298 | 0.476 | 13 | 0.131 | -0.155 | 0.844 | 141,218 |

---
**How to read verdicts.** ADOPT = ≥ min trades, bootstrap CI above 0 after correcting for the number of tests, positive in both time halves and both symbol halves, and better than random entries with the same exits. PROMISING = everything except significance. UNSTABLE = fails a half. REJECT = not positive or not better than random.