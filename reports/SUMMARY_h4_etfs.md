# IFI Lab results: h4 · etfs
_Run 2026-10-12 16:53 UTC · 16 symbols · 2023-11-10 to 2026-10-12 · split 2025-04-26 · 42 setup×exit tests (Bonferroni-adjusted) · engine v1.1_

## P1 · Exits × setups (R per trade, after costs)

Random-entry control (same stops and exits), mean expectancy by exit: X1_time10 -0.047R, X2_target2R -0.025R, X3_target3R +0.011R, X4_trendline_trail +0.001R, X5_chandelier3atr -0.038R, X6_partial1R_then_line -0.039R, X7_stage_drop -0.005R

| setup | exit | n | win_rate | avg_win | avg_loss | expectancy | median | exp_w10 | ci_low | ci_low_adj | exp_early | exp_late | exp_symA | exp_symB | random_mean | random_p95 | avg_bars | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E1b_trigger_counter_trend | X5_chandelier3atr | 151 | 0.424 | 2.114 | -0.877 | 0.391 | -0.352 | 0.383 | 0.060 | -0.084 | 0.498 | 0.271 | 0.263 | 0.499 | -0.038 | 0.245 | 18.384 | PROMISING (not significant after correction) |
| E1b_trigger_counter_trend | X3_target3R | 148 | 0.432 | 2.334 | -1.114 | 0.377 | -1.036 | 0.377 | 0.084 | -0.109 | 0.573 | 0.165 | 0.300 | 0.441 | 0.011 | 0.251 | 22.311 | PROMISING (not significant after correction) |
| E1_trigger_with_trend | X3_target3R | 40 | 0.425 | 2.190 | -1.094 | 0.302 | -1.031 | 0.302 | -0.230 | -0.492 | 0.457 | 0.174 | 0.272 | 0.334 | 0.011 | 0.452 | 23.975 | INCONCLUSIVE (too few trades) |
| E4_anchor_reclaim | X3_target3R | 178 | 0.483 | 1.513 | -0.930 | 0.251 | -0.061 | 0.251 | 0.047 | -0.082 | 0.073 | 0.406 | 0.281 | 0.225 | 0.011 | 0.218 | 43.101 | PROMISING (not significant after correction) |
| E1_trigger_with_trend | X2_target2R | 41 | 0.488 | 1.691 | -1.136 | 0.243 | -1.016 | 0.243 | -0.196 | -0.487 | 0.488 | 0.032 | 0.209 | 0.279 | -0.025 | 0.345 | 18.707 | INCONCLUSIVE (too few trades) |
| E2_exhaustion_confluence | X1_time10 | 72 | 0.403 | 2.103 | -1.060 | 0.214 | -1.033 | 0.214 | -0.204 | -0.468 | 0.223 | 0.204 | 0.780 | -0.087 | -0.047 | 0.214 | 6.986 | REJECT |
| E1_trigger_with_trend | X1_time10 | 41 | 0.585 | 1.082 | -1.031 | 0.206 | 0.561 | 0.206 | -0.151 | -0.325 | 0.493 | -0.043 | 0.283 | 0.125 | -0.047 | 0.295 | 8.463 | INCONCLUSIVE (too few trades) |
| E1b_trigger_counter_trend | X1_time10 | 153 | 0.529 | 1.200 | -0.918 | 0.203 | 0.101 | 0.203 | -0.023 | -0.120 | 0.392 | -0.015 | 0.083 | 0.307 | -0.047 | 0.128 | 8.098 | UNSTABLE (fails a split half) |
| E4_anchor_reclaim | X2_target2R | 179 | 0.486 | 1.386 | -0.925 | 0.198 | -0.054 | 0.198 | 0.011 | -0.085 | 0.037 | 0.341 | 0.225 | 0.175 | -0.025 | 0.148 | 38.715 | PROMISING (not significant after correction) |
| E1_trigger_with_trend | X5_chandelier3atr | 41 | 0.512 | 1.304 | -0.967 | 0.196 | 0.103 | 0.196 | -0.196 | -0.438 | 0.447 | -0.021 | 0.140 | 0.255 | -0.038 | 0.593 | 17.463 | INCONCLUSIVE (too few trades) |
| E2_exhaustion_confluence | X5_chandelier3atr | 72 | 0.333 | 2.554 | -1.033 | 0.163 | -0.984 | 0.144 | -0.318 | -0.617 | 0.285 | 0.034 | 0.652 | -0.097 | -0.038 | 0.420 | 13.597 | REJECT |
| E1b_trigger_counter_trend | X2_target2R | 148 | 0.432 | 1.745 | -1.114 | 0.122 | -1.036 | 0.122 | -0.114 | -0.294 | 0.279 | -0.048 | 0.062 | 0.172 | -0.025 | 0.166 | 17.486 | REJECT |
| E1_trigger_with_trend | X6_partial1R_then_line | 44 | 0.614 | 0.391 | -0.307 | 0.122 | 0.132 | 0.122 | -0.008 | -0.089 | 0.203 | 0.047 | 0.116 | 0.128 | -0.039 | 0.209 | 3.841 | INCONCLUSIVE (too few trades) |
| E3_stage2_transition | X3_target3R | 151 | 0.424 | 1.620 | -0.992 | 0.115 | -1.016 | 0.115 | -0.121 | -0.236 | 0.221 | 0.007 | 0.187 | 0.042 | 0.011 | 0.226 | 32.881 | REJECT |
| E1_trigger_with_trend | X4_trendline_trail | 44 | 0.591 | 0.398 | -0.326 | 0.102 | 0.117 | 0.102 | -0.039 | -0.135 | 0.176 | 0.034 | 0.119 | 0.084 | 0.001 | 0.455 | 3.864 | INCONCLUSIVE (too few trades) |
| E1_trigger_with_trend | X7_stage_drop | 44 | 0.591 | 0.391 | -0.326 | 0.098 | 0.117 | 0.098 | -0.043 | -0.135 | 0.176 | 0.026 | 0.119 | 0.075 | -0.005 | 0.443 | 3.886 | INCONCLUSIVE (too few trades) |
| E4_anchor_reclaim | X7_stage_drop | 219 | 0.374 | 1.080 | -0.504 | 0.089 | -0.165 | 0.089 | -0.042 | -0.133 | 0.069 | 0.107 | 0.146 | 0.043 | -0.005 | 0.186 | 23.653 | REJECT |
| E4_anchor_reclaim | X4_trendline_trail | 232 | 0.384 | 0.968 | -0.471 | 0.081 | -0.203 | 0.081 | -0.046 | -0.129 | 0.019 | 0.137 | 0.168 | 0.009 | 0.001 | 0.170 | 20.470 | REJECT |
| E4_anchor_reclaim | X6_partial1R_then_line | 232 | 0.427 | 0.834 | -0.481 | 0.080 | -0.137 | 0.080 | -0.024 | -0.072 | 0.047 | 0.111 | 0.146 | 0.026 | -0.039 | 0.071 | 20.284 | PROMISING (not significant after correction) |
| E5_score4 | X2_target2R | 311 | 0.444 | 1.462 | -1.034 | 0.074 | -1.012 | 0.074 | -0.072 | -0.148 | -0.026 | 0.151 | 0.152 | -0.005 | -0.025 | 0.107 | 28.614 | REJECT |
| E3_stage2_transition | X7_stage_drop | 178 | 0.337 | 1.254 | -0.536 | 0.067 | -0.266 | 0.060 | -0.115 | -0.205 | 0.122 | 0.011 | 0.159 | -0.020 | -0.005 | 0.215 | 19.534 | REJECT |
| E3_stage2_transition | X4_trendline_trail | 178 | 0.315 | 1.116 | -0.417 | 0.065 | -0.208 | 0.058 | -0.094 | -0.161 | 0.147 | -0.019 | 0.218 | -0.080 | 0.001 | 0.217 | 15.096 | REJECT |
| E4_anchor_reclaim | X5_chandelier3atr | 211 | 0.427 | 0.867 | -0.533 | 0.064 | -0.119 | 0.064 | -0.052 | -0.121 | 0.098 | 0.035 | 0.115 | 0.023 | -0.038 | 0.203 | 18.839 | REJECT |
| E3_stage2_transition | X2_target2R | 153 | 0.431 | 1.440 | -0.992 | 0.057 | -1.015 | 0.057 | -0.145 | -0.240 | 0.182 | -0.069 | 0.127 | -0.013 | -0.025 | 0.163 | 29.595 | REJECT |
| E4_anchor_reclaim | X1_time10 | 220 | 0.568 | 0.548 | -0.639 | 0.035 | 0.146 | 0.035 | -0.065 | -0.118 | 0.005 | 0.061 | 0.025 | 0.043 | -0.047 | 0.105 | 9.236 | REJECT |
| E2_exhaustion_confluence | X3_target3R | 72 | 0.319 | 2.592 | -1.172 | 0.030 | -1.063 | 0.030 | -0.391 | -0.612 | 0.015 | 0.046 | 0.271 | -0.098 | 0.011 | 0.350 | 13.181 | REJECT |
| E3_stage2_transition | X6_partial1R_then_line | 178 | 0.337 | 0.902 | -0.421 | 0.025 | -0.205 | 0.025 | -0.091 | -0.170 | 0.095 | -0.047 | 0.109 | -0.056 | -0.039 | 0.087 | 15.006 | REJECT |
| E5_score4 | X3_target3R | 300 | 0.397 | 1.621 | -1.025 | 0.025 | -1.024 | 0.025 | -0.136 | -0.227 | -0.090 | 0.116 | 0.091 | -0.042 | 0.011 | 0.179 | 32.450 | REJECT |
| E5_score4 | X6_partial1R_then_line | 379 | 0.425 | 0.838 | -0.608 | 0.007 | -0.224 | 0.007 | -0.080 | -0.138 | 0.040 | -0.017 | 0.064 | -0.044 | -0.039 | 0.055 | 18.657 | REJECT |
| E5_score4 | X4_trendline_trail | 373 | 0.327 | 1.210 | -0.591 | -0.002 | -0.319 | -0.002 | -0.112 | -0.187 | -0.009 | 0.004 | 0.059 | -0.055 | 0.001 | 0.133 | 19.681 | REJECT |
| E3_stage2_transition | X5_chandelier3atr | 169 | 0.391 | 1.056 | -0.683 | -0.004 | -0.241 | -0.004 | -0.159 | -0.252 | 0.083 | -0.088 | 0.073 | -0.079 | -0.038 | 0.236 | 17.970 | REJECT |
| E5_score4 | X7_stage_drop | 362 | 0.329 | 1.290 | -0.638 | -0.004 | -0.339 | -0.004 | -0.136 | -0.213 | 0.016 | -0.020 | 0.038 | -0.042 | -0.005 | 0.140 | 22.108 | REJECT |
| E5_score4 | X1_time10 | 422 | 0.531 | 0.627 | -0.764 | -0.025 | 0.051 | -0.025 | -0.108 | -0.163 | 0.007 | -0.048 | 0.050 | -0.095 | -0.047 | 0.059 | 8.815 | REJECT |
| E3_stage2_transition | X1_time10 | 171 | 0.520 | 0.576 | -0.698 | -0.035 | 0.046 | -0.035 | -0.156 | -0.229 | 0.008 | -0.077 | 0.004 | -0.072 | -0.047 | 0.129 | 8.906 | REJECT |
| E2_exhaustion_confluence | X4_trendline_trail | 72 | 0.444 | 0.438 | -0.493 | -0.079 | -0.059 | -0.079 | -0.223 | -0.291 | -0.043 | -0.117 | 0.009 | -0.126 | 0.001 | 0.346 | 2.556 | REJECT |
| E2_exhaustion_confluence | X6_partial1R_then_line | 72 | 0.444 | 0.431 | -0.493 | -0.082 | -0.059 | -0.082 | -0.225 | -0.291 | -0.050 | -0.116 | 0.005 | -0.129 | -0.039 | 0.163 | 2.556 | REJECT |
| E5_score4 | X5_chandelier3atr | 390 | 0.344 | 1.021 | -0.661 | -0.083 | -0.330 | -0.083 | -0.188 | -0.271 | -0.021 | -0.128 | -0.035 | -0.126 | -0.038 | 0.130 | 16.487 | REJECT |
| E1b_trigger_counter_trend | X6_partial1R_then_line | 163 | 0.454 | 0.260 | -0.385 | -0.092 | -0.038 | -0.092 | -0.173 | -0.255 | -0.104 | -0.078 | -0.131 | -0.060 | -0.039 | 0.093 | 2.061 | REJECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 163 | 0.454 | 0.253 | -0.385 | -0.095 | -0.038 | -0.095 | -0.175 | -0.257 | -0.107 | -0.082 | -0.138 | -0.060 | 0.001 | 0.219 | 2.061 | REJECT |
| E2_exhaustion_confluence | X7_stage_drop | 72 | 0.444 | 0.413 | -0.502 | -0.095 | -0.059 | -0.095 | -0.237 | -0.298 | -0.065 | -0.128 | 0.009 | -0.151 | -0.005 | 0.367 | 2.611 | REJECT |
| E1b_trigger_counter_trend | X7_stage_drop | 163 | 0.454 | 0.251 | -0.385 | -0.096 | -0.038 | -0.096 | -0.177 | -0.258 | -0.109 | -0.082 | -0.140 | -0.060 | -0.005 | 0.217 | 2.080 | REJECT |
| E2_exhaustion_confluence | X2_target2R | 72 | 0.347 | 1.906 | -1.172 | -0.103 | -1.062 | -0.103 | -0.443 | -0.585 | -0.183 | -0.020 | 0.137 | -0.232 | -0.025 | 0.272 | 9.917 | REJECT |

### Exit rules ranked (trade-weighted across setups)

| exit | trades | mean_expectancy | random_mean | edge_over_random |
|---|---|---|---|---|
| X3_target3R | 889 | 0.157 | 0.011 | 0.146 |
| X2_target2R | 904 | 0.097 | -0.025 | 0.122 |
| X5_chandelier3atr | 1,034 | 0.057 | -0.038 | 0.095 |
| X1_time10 | 1,079 | 0.043 | -0.047 | 0.090 |
| X4_trendline_trail | 1,062 | 0.012 | 0.001 | 0.011 |
| X7_stage_drop | 1,038 | 0.011 | -0.005 | 0.016 |
| X6_partial1R_then_line | 1,068 | 0.009 | -0.039 | 0.048 |

## P1b · Sizing (fixed-fractional, max open positions = 5)

| setup | exit | risk_pct | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|
| E1b_trigger_counter_trend | X5_chandelier3atr | 0.005 | 0.062 | -0.105 | 0.596 | 117,951 |
| E1b_trigger_counter_trend | X5_chandelier3atr | 0.010 | 0.119 | -0.206 | 0.581 | 136,038 |
| E1b_trigger_counter_trend | X5_chandelier3atr | 0.020 | 0.215 | -0.391 | 0.551 | 170,169 |
| E1b_trigger_counter_trend | X3_target3R | 0.005 | 0.069 | -0.119 | 0.578 | 119,818 |
| E1b_trigger_counter_trend | X3_target3R | 0.010 | 0.130 | -0.226 | 0.575 | 139,546 |
| E1b_trigger_counter_trend | X3_target3R | 0.020 | 0.228 | -0.410 | 0.555 | 174,927 |
| E4_anchor_reclaim | X3_target3R | 0.005 | 0.049 | -0.064 | 0.761 | 113,737 |
| E4_anchor_reclaim | X3_target3R | 0.010 | 0.096 | -0.125 | 0.768 | 128,088 |
| E4_anchor_reclaim | X3_target3R | 0.020 | 0.184 | -0.236 | 0.778 | 158,071 |

## P2 · Market regime (SPY > 200-day average and Trend line rising)

| setup | exit | n_on | exp_on | n_off | exp_off | diff | diff_ci_low | verdict |
|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X4_trendline_trail | 18 | 0.196 | 26 | 0.037 | 0.159 | -0.285 | NO CLEAR EFFECT |
| E1_trigger_with_trend | X5_chandelier3atr | 15 | 0.355 | 26 | 0.104 | 0.251 | -0.964 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 40 | -0.193 | 123 | -0.063 | -0.130 | -0.519 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 34 | 0.309 | 117 | 0.415 | -0.106 | -1.192 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X4_trendline_trail | 27 | -0.250 | 45 | 0.023 | -0.273 | -0.690 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 27 | -0.136 | 45 | 0.342 | -0.478 | -2.012 | NO CLEAR EFFECT |
| E3_stage2_transition | X4_trendline_trail | 116 | -0.028 | 62 | 0.239 | -0.267 | -1.012 | NO CLEAR EFFECT |
| E3_stage2_transition | X5_chandelier3atr | 110 | -0.074 | 59 | 0.127 | -0.201 | -0.768 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X4_trendline_trail | 169 | -0.024 | 63 | 0.362 | -0.386 | -0.866 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X5_chandelier3atr | 153 | -0.041 | 58 | 0.341 | -0.382 | -0.863 | NO CLEAR EFFECT |
| E5_score4 | X4_trendline_trail | 282 | -0.136 | 91 | 0.415 | -0.551 | -1.084 | NO CLEAR EFFECT |
| E5_score4 | X5_chandelier3atr | 296 | -0.151 | 94 | 0.129 | -0.280 | -0.718 | NO CLEAR EFFECT |

## P4 · Portfolio heat (E1b_trigger_counter_trend + X5_chandelier3atr)

| rule | cagr | max_dd | mar | final |
|---|---|---|---|---|
| No sector cap | 0.072 | -0.211 | 0.340 | 120,780 |
| Max 1 open per sector | 0.072 | -0.211 | 0.340 | 120,780 |

---
**How to read verdicts.** ADOPT = ≥ min trades, bootstrap CI above 0 after correcting for the number of tests, positive in both time halves and both symbol halves, and better than random entries with the same exits. PROMISING = everything except significance. UNSTABLE = fails a half. REJECT = not positive or not better than random.