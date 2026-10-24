# IFI Lab results: h4 · etfs
_Run 2026-10-24 15:38 UTC · 16 symbols · 2023-11-10 to 2026-10-23 · split 2025-05-02 · 42 setup×exit tests (Bonferroni-adjusted) · engine v1.3.3_

## P1 · Exits × setups (R per trade, after costs)

Random-entry control (same stops and exits), mean expectancy by exit: X1_time10 -0.077R, X2_target2R -0.024R, X3_target3R -0.004R, X4_trendline_trail -0.064R, X5_chandelier3atr -0.041R, X6_partial1R_then_line -0.077R, X7_stage_drop -0.047R

| setup | exit | n | win_rate | avg_win | avg_loss | expectancy | median | exp_w10 | ci_low | ci_low_adj | exp_early | exp_late | exp_symA | exp_symB | random_mean | random_p95 | avg_bars | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E1b_trigger_counter_trend | X5_chandelier3atr | 152 | 0.421 | 2.288 | -0.867 | 0.462 | -0.317 | 0.445 | 0.108 | -0.045 | 0.498 | 0.422 | 0.262 | 0.632 | -0.041 | 0.229 | 19.112 | PROMISING (not significant after correction) |
| E1b_trigger_counter_trend | X3_target3R | 149 | 0.430 | 2.435 | -1.111 | 0.412 | -1.037 | 0.412 | 0.109 | -0.079 | 0.573 | 0.239 | 0.339 | 0.473 | -0.004 | 0.232 | 22.826 | PROMISING (not significant after correction) |
| E1_trigger_with_trend | X3_target3R | 40 | 0.425 | 2.190 | -1.098 | 0.299 | -1.031 | 0.299 | -0.234 | -0.501 | 0.452 | 0.174 | 0.267 | 0.334 | -0.004 | 0.459 | 23.975 | INCONCLUSIVE (too few trades) |
| E4_anchor_reclaim | X3_target3R | 185 | 0.486 | 1.503 | -0.932 | 0.252 | -0.048 | 0.252 | 0.049 | -0.080 | 0.152 | 0.341 | 0.259 | 0.247 | -0.004 | 0.214 | 41.919 | PROMISING (not significant after correction) |
| E1_trigger_with_trend | X2_target2R | 41 | 0.488 | 1.692 | -1.140 | 0.241 | -1.016 | 0.241 | -0.199 | -0.489 | 0.483 | 0.032 | 0.205 | 0.279 | -0.024 | 0.393 | 18.707 | INCONCLUSIVE (too few trades) |
| E4_anchor_reclaim | X2_target2R | 186 | 0.489 | 1.388 | -0.928 | 0.205 | -0.038 | 0.205 | 0.027 | -0.096 | 0.118 | 0.284 | 0.225 | 0.189 | -0.024 | 0.158 | 37.484 | PROMISING (not significant after correction) |
| E1_trigger_with_trend | X1_time10 | 41 | 0.585 | 1.082 | -1.037 | 0.203 | 0.561 | 0.203 | -0.156 | -0.334 | 0.488 | -0.042 | 0.278 | 0.125 | -0.077 | 0.287 | 8.463 | INCONCLUSIVE (too few trades) |
| E1b_trigger_counter_trend | X1_time10 | 154 | 0.532 | 1.187 | -0.918 | 0.203 | 0.121 | 0.203 | -0.022 | -0.136 | 0.392 | -0.013 | 0.084 | 0.307 | -0.077 | 0.118 | 8.110 | UNSTABLE (fails a split half) |
| E2_exhaustion_confluence | X1_time10 | 73 | 0.397 | 2.103 | -1.060 | 0.197 | -1.042 | 0.197 | -0.220 | -0.456 | 0.223 | 0.170 | 0.710 | -0.087 | -0.077 | 0.191 | 6.918 | UNSTABLE (fails a split half) |
| E1_trigger_with_trend | X5_chandelier3atr | 41 | 0.512 | 1.305 | -0.972 | 0.194 | 0.103 | 0.194 | -0.200 | -0.441 | 0.442 | -0.021 | 0.135 | 0.255 | -0.041 | 0.492 | 17.463 | INCONCLUSIVE (too few trades) |
| E2_exhaustion_confluence | X5_chandelier3atr | 73 | 0.329 | 2.593 | -1.033 | 0.159 | -0.992 | 0.140 | -0.323 | -0.597 | 0.285 | 0.029 | 0.548 | -0.056 | -0.041 | 0.322 | 13.753 | REJECT |
| E1b_trigger_counter_trend | X2_target2R | 149 | 0.430 | 1.816 | -1.111 | 0.146 | -1.037 | 0.146 | -0.103 | -0.233 | 0.279 | 0.004 | 0.062 | 0.217 | -0.024 | 0.161 | 17.765 | REJECT |
| E3_stage2_transition | X3_target3R | 153 | 0.425 | 1.654 | -0.989 | 0.134 | -1.013 | 0.134 | -0.096 | -0.222 | 0.186 | 0.080 | 0.195 | 0.072 | -0.004 | 0.231 | 33.484 | REJECT |
| E1_trigger_with_trend | X6_partial1R_then_line | 44 | 0.614 | 0.391 | -0.307 | 0.122 | 0.132 | 0.122 | -0.009 | -0.089 | 0.203 | 0.047 | 0.116 | 0.128 | -0.077 | 0.166 | 3.841 | INCONCLUSIVE (too few trades) |
| E1_trigger_with_trend | X4_trendline_trail | 44 | 0.591 | 0.398 | -0.326 | 0.102 | 0.117 | 0.102 | -0.039 | -0.135 | 0.176 | 0.034 | 0.119 | 0.084 | -0.064 | 0.303 | 3.864 | INCONCLUSIVE (too few trades) |
| E1_trigger_with_trend | X7_stage_drop | 44 | 0.591 | 0.391 | -0.326 | 0.098 | 0.117 | 0.098 | -0.043 | -0.135 | 0.176 | 0.026 | 0.119 | 0.075 | -0.047 | 0.329 | 3.886 | INCONCLUSIVE (too few trades) |
| E4_anchor_reclaim | X7_stage_drop | 227 | 0.366 | 1.132 | -0.501 | 0.096 | -0.166 | 0.096 | -0.049 | -0.121 | 0.111 | 0.083 | 0.158 | 0.047 | -0.047 | 0.116 | 23.154 | REJECT |
| E4_anchor_reclaim | X4_trendline_trail | 240 | 0.383 | 1.007 | -0.471 | 0.096 | -0.190 | 0.096 | -0.035 | -0.085 | 0.070 | 0.120 | 0.183 | 0.026 | -0.064 | 0.104 | 20.212 | REJECT |
| E3_stage2_transition | X7_stage_drop | 181 | 0.343 | 1.289 | -0.527 | 0.095 | -0.252 | 0.088 | -0.083 | -0.178 | 0.129 | 0.060 | 0.171 | 0.021 | -0.047 | 0.142 | 19.895 | REJECT |
| E4_anchor_reclaim | X6_partial1R_then_line | 240 | 0.429 | 0.846 | -0.483 | 0.088 | -0.105 | 0.088 | -0.018 | -0.070 | 0.088 | 0.087 | 0.147 | 0.040 | -0.077 | 0.034 | 20.025 | PROMISING (not significant after correction) |
| E4_anchor_reclaim | X5_chandelier3atr | 219 | 0.429 | 0.893 | -0.534 | 0.078 | -0.099 | 0.078 | -0.042 | -0.097 | 0.131 | 0.033 | 0.128 | 0.040 | -0.041 | 0.177 | 18.521 | REJECT |
| E5_score4 | X2_target2R | 319 | 0.445 | 1.457 | -1.036 | 0.074 | -1.012 | 0.074 | -0.067 | -0.157 | 0.023 | 0.114 | 0.147 | 0.002 | -0.024 | 0.110 | 28.245 | REJECT |
| E3_stage2_transition | X2_target2R | 156 | 0.436 | 1.450 | -0.993 | 0.072 | -0.892 | 0.072 | -0.133 | -0.248 | 0.148 | -0.006 | 0.154 | -0.012 | -0.024 | 0.167 | 29.712 | REJECT |
| E3_stage2_transition | X4_trendline_trail | 181 | 0.315 | 1.125 | -0.414 | 0.071 | -0.208 | 0.063 | -0.088 | -0.168 | 0.146 | -0.008 | 0.209 | -0.064 | -0.064 | 0.127 | 15.188 | REJECT |
| E2_exhaustion_confluence | X3_target3R | 73 | 0.315 | 2.728 | -1.170 | 0.058 | -1.062 | 0.058 | -0.367 | -0.567 | 0.015 | 0.103 | 0.263 | -0.055 | -0.004 | 0.319 | 13.247 | REJECT |
| E4_anchor_reclaim | X1_time10 | 227 | 0.581 | 0.559 | -0.639 | 0.057 | 0.155 | 0.057 | -0.039 | -0.098 | 0.032 | 0.081 | 0.030 | 0.079 | -0.077 | 0.075 | 9.216 | REJECT |
| E3_stage2_transition | X6_partial1R_then_line | 181 | 0.343 | 0.891 | -0.421 | 0.028 | -0.205 | 0.028 | -0.087 | -0.151 | 0.095 | -0.040 | 0.103 | -0.044 | -0.077 | 0.049 | 15.094 | REJECT |
| E5_score4 | X3_target3R | 310 | 0.397 | 1.601 | -1.028 | 0.015 | -1.024 | 0.015 | -0.140 | -0.217 | -0.014 | 0.038 | 0.064 | -0.033 | -0.004 | 0.157 | 31.961 | REJECT |
| E3_stage2_transition | X5_chandelier3atr | 172 | 0.395 | 1.070 | -0.682 | 0.010 | -0.232 | 0.010 | -0.143 | -0.224 | 0.060 | -0.038 | 0.074 | -0.052 | -0.041 | 0.213 | 18.215 | REJECT |
| E5_score4 | X6_partial1R_then_line | 387 | 0.429 | 0.831 | -0.612 | 0.007 | -0.223 | 0.007 | -0.080 | -0.127 | 0.075 | -0.043 | 0.053 | -0.033 | -0.077 | 0.003 | 18.561 | UNSTABLE (fails a split half) |
| E5_score4 | X7_stage_drop | 370 | 0.330 | 1.321 | -0.640 | 0.007 | -0.336 | 0.007 | -0.127 | -0.198 | 0.099 | -0.063 | 0.019 | -0.005 | -0.047 | 0.080 | 21.868 | REJECT |
| E5_score4 | X4_trendline_trail | 381 | 0.331 | 1.212 | -0.593 | 0.004 | -0.319 | 0.004 | -0.122 | -0.175 | 0.068 | -0.045 | 0.035 | -0.024 | -0.064 | 0.064 | 19.517 | REJECT |
| E3_stage2_transition | X1_time10 | 174 | 0.529 | 0.578 | -0.690 | -0.019 | 0.053 | -0.019 | -0.131 | -0.229 | -0.005 | -0.034 | 0.025 | -0.063 | -0.077 | 0.092 | 8.977 | REJECT |
| E5_score4 | X1_time10 | 432 | 0.532 | 0.637 | -0.770 | -0.021 | 0.044 | -0.021 | -0.102 | -0.138 | 0.027 | -0.054 | 0.056 | -0.090 | -0.077 | 0.030 | 8.785 | REJECT |
| E5_score4 | X5_chandelier3atr | 398 | 0.352 | 1.034 | -0.670 | -0.071 | -0.318 | -0.071 | -0.171 | -0.237 | 0.026 | -0.141 | -0.031 | -0.106 | -0.041 | 0.120 | 16.528 | REJECT |
| E2_exhaustion_confluence | X4_trendline_trail | 73 | 0.425 | 0.450 | -0.482 | -0.086 | -0.071 | -0.086 | -0.231 | -0.289 | -0.043 | -0.130 | -0.015 | -0.126 | -0.064 | 0.214 | 2.548 | REJECT |
| E2_exhaustion_confluence | X6_partial1R_then_line | 73 | 0.425 | 0.443 | -0.482 | -0.089 | -0.071 | -0.089 | -0.231 | -0.292 | -0.050 | -0.130 | -0.019 | -0.128 | -0.077 | 0.124 | 2.548 | REJECT |
| E1b_trigger_counter_trend | X6_partial1R_then_line | 165 | 0.455 | 0.259 | -0.391 | -0.096 | -0.038 | -0.096 | -0.178 | -0.231 | -0.104 | -0.086 | -0.138 | -0.060 | -0.077 | 0.054 | 2.061 | REJECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 165 | 0.455 | 0.252 | -0.391 | -0.099 | -0.038 | -0.099 | -0.180 | -0.231 | -0.107 | -0.090 | -0.145 | -0.060 | -0.064 | 0.135 | 2.061 | REJECT |
| E1b_trigger_counter_trend | X7_stage_drop | 165 | 0.455 | 0.250 | -0.391 | -0.100 | -0.038 | -0.100 | -0.181 | -0.231 | -0.109 | -0.090 | -0.147 | -0.060 | -0.047 | 0.140 | 2.079 | REJECT |
| E2_exhaustion_confluence | X7_stage_drop | 73 | 0.425 | 0.424 | -0.491 | -0.102 | -0.071 | -0.102 | -0.241 | -0.298 | -0.065 | -0.141 | -0.015 | -0.150 | -0.047 | 0.249 | 2.603 | REJECT |
| E2_exhaustion_confluence | X2_target2R | 73 | 0.342 | 1.933 | -1.170 | -0.107 | -1.062 | -0.107 | -0.460 | -0.680 | -0.183 | -0.029 | 0.092 | -0.217 | -0.024 | 0.252 | 9.890 | REJECT |

### Exit rules ranked (trade-weighted across setups)

| exit | trades | mean_expectancy | random_mean | edge_over_random |
|---|---|---|---|---|
| X3_target3R | 910 | 0.164 | -0.004 | 0.168 |
| X2_target2R | 924 | 0.105 | -0.024 | 0.129 |
| X5_chandelier3atr | 1,055 | 0.076 | -0.041 | 0.117 |
| X1_time10 | 1,101 | 0.050 | -0.077 | 0.127 |
| X7_stage_drop | 1,060 | 0.021 | -0.047 | 0.068 |
| X4_trendline_trail | 1,084 | 0.018 | -0.064 | 0.082 |
| X6_partial1R_then_line | 1,090 | 0.011 | -0.077 | 0.088 |

## P1b · Sizing (fixed-fractional, max open positions = 5)

| setup | exit | risk_pct | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|
| E1b_trigger_counter_trend | X5_chandelier3atr | 0.005 | 0.054 | -0.103 | 0.525 | 115,692 |
| E1b_trigger_counter_trend | X5_chandelier3atr | 0.010 | 0.103 | -0.198 | 0.522 | 131,085 |
| E1b_trigger_counter_trend | X5_chandelier3atr | 0.020 | 0.183 | -0.362 | 0.505 | 158,907 |
| E1b_trigger_counter_trend | X3_target3R | 0.005 | 0.070 | -0.119 | 0.588 | 120,467 |
| E1b_trigger_counter_trend | X3_target3R | 0.010 | 0.134 | -0.226 | 0.591 | 141,352 |
| E1b_trigger_counter_trend | X3_target3R | 0.020 | 0.239 | -0.411 | 0.581 | 180,712 |
| E4_anchor_reclaim | X3_target3R | 0.005 | 0.042 | -0.070 | 0.604 | 111,944 |
| E4_anchor_reclaim | X3_target3R | 0.010 | 0.082 | -0.135 | 0.607 | 124,151 |
| E4_anchor_reclaim | X3_target3R | 0.020 | 0.156 | -0.255 | 0.612 | 148,825 |

## P2 · Market regime (SPY > 200-day average and Trend line rising)

| setup | exit | n_on | exp_on | n_off | exp_off | diff | diff_ci_low | verdict |
|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X4_trendline_trail | 18 | 0.196 | 26 | 0.037 | 0.159 | -0.285 | NO CLEAR EFFECT |
| E1_trigger_with_trend | X5_chandelier3atr | 15 | 0.355 | 26 | 0.101 | 0.254 | -0.962 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 40 | -0.197 | 125 | -0.068 | -0.129 | -0.524 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 34 | 0.637 | 118 | 0.411 | 0.225 | -1.053 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X4_trendline_trail | 28 | -0.255 | 45 | 0.019 | -0.274 | -0.670 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 28 | -0.204 | 45 | 0.385 | -0.590 | -2.057 | NO CLEAR EFFECT |
| E3_stage2_transition | X4_trendline_trail | 118 | -0.022 | 63 | 0.245 | -0.267 | -1.047 | NO CLEAR EFFECT |
| E3_stage2_transition | X5_chandelier3atr | 112 | -0.056 | 60 | 0.134 | -0.189 | -0.789 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X4_trendline_trail | 172 | -0.017 | 68 | 0.380 | -0.397 | -0.948 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X5_chandelier3atr | 156 | -0.034 | 63 | 0.356 | -0.390 | -0.897 | NO CLEAR EFFECT |
| E5_score4 | X4_trendline_trail | 285 | -0.124 | 96 | 0.381 | -0.505 | -1.061 | NO CLEAR EFFECT |
| E5_score4 | X5_chandelier3atr | 300 | -0.134 | 98 | 0.123 | -0.257 | -0.663 | NO CLEAR EFFECT |

## P4 · Portfolio heat (E1b_trigger_counter_trend + X5_chandelier3atr)

| rule | cagr | max_dd | mar | final |
|---|---|---|---|---|
| No sector cap | 0.101 | -0.171 | 0.588 | 130,357 |
| Max 1 open per sector | 0.101 | -0.171 | 0.588 | 130,357 |

## P6 · Playbook portfolio (E4_anchor_reclaim + E1_trigger_with_trend, exit X3_target3R, 1 per symbol, 1 per sector, max 5 open)

| risk | trades | trades_per_year | expectancy | win_rate | longest_losing_streak | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|---|---|---|
| 0.50% | 205 | 74.727 | 0.286 | 0.483 | 13 | 0.078 | -0.075 | 1.031 | 122,766 |
| 0.75% | 205 | 74.727 | 0.286 | 0.483 | 13 | 0.116 | -0.111 | 1.043 | 135,125 |
| 1.00% | 205 | 74.727 | 0.286 | 0.483 | 13 | 0.154 | -0.146 | 1.055 | 148,098 |

---
**How to read verdicts.** ADOPT = ≥ min trades, bootstrap CI above 0 after correcting for the number of tests, positive in both time halves and both symbol halves, and better than random entries with the same exits. PROMISING = everything except significance. UNSTABLE = fails a half. REJECT = not positive or not better than random.