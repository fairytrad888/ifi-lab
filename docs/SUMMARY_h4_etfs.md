# IFI Lab results: h4 · etfs
_Run 2026-10-13 17:07 UTC · 16 symbols · 2023-11-10 to 2026-10-13 · split 2025-04-27 · 42 setup×exit tests (Bonferroni-adjusted) · engine v1.3.3_

## P1 · Exits × setups (R per trade, after costs)

Random-entry control (same stops and exits), mean expectancy by exit: X1_time10 -0.015R, X2_target2R +0.012R, X3_target3R +0.055R, X4_trendline_trail -0.060R, X5_chandelier3atr -0.030R, X6_partial1R_then_line -0.076R, X7_stage_drop -0.061R

| setup | exit | n | win_rate | avg_win | avg_loss | expectancy | median | exp_w10 | ci_low | ci_low_adj | exp_early | exp_late | exp_symA | exp_symB | random_mean | random_p95 | avg_bars | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E1b_trigger_counter_trend | X5_chandelier3atr | 151 | 0.424 | 2.124 | -0.876 | 0.395 | -0.352 | 0.387 | 0.065 | -0.082 | 0.498 | 0.280 | 0.263 | 0.507 | -0.030 | 0.229 | 18.450 | PROMISING (not significant after correction) |
| E1b_trigger_counter_trend | X3_target3R | 148 | 0.432 | 2.334 | -1.118 | 0.375 | -1.036 | 0.375 | 0.080 | -0.114 | 0.573 | 0.160 | 0.295 | 0.440 | 0.055 | 0.297 | 22.392 | PROMISING (not significant after correction) |
| E1_trigger_with_trend | X3_target3R | 40 | 0.425 | 2.189 | -1.098 | 0.299 | -1.031 | 0.299 | -0.234 | -0.501 | 0.452 | 0.174 | 0.267 | 0.334 | 0.055 | 0.522 | 23.975 | INCONCLUSIVE (too few trades) |
| E4_anchor_reclaim | X3_target3R | 177 | 0.486 | 1.515 | -0.941 | 0.252 | -0.068 | 0.252 | 0.054 | -0.061 | 0.071 | 0.411 | 0.277 | 0.230 | 0.055 | 0.272 | 42.842 | REJECT |
| E1_trigger_with_trend | X2_target2R | 41 | 0.488 | 1.691 | -1.140 | 0.241 | -1.016 | 0.241 | -0.199 | -0.489 | 0.483 | 0.032 | 0.204 | 0.279 | 0.012 | 0.394 | 18.707 | INCONCLUSIVE (too few trades) |
| E2_exhaustion_confluence | X1_time10 | 72 | 0.403 | 2.103 | -1.060 | 0.214 | -1.033 | 0.214 | -0.204 | -0.468 | 0.223 | 0.204 | 0.780 | -0.087 | -0.015 | 0.291 | 6.986 | REJECT |
| E1_trigger_with_trend | X1_time10 | 41 | 0.585 | 1.082 | -1.037 | 0.203 | 0.561 | 0.203 | -0.156 | -0.334 | 0.488 | -0.043 | 0.278 | 0.125 | -0.015 | 0.373 | 8.463 | INCONCLUSIVE (too few trades) |
| E4_anchor_reclaim | X2_target2R | 178 | 0.489 | 1.392 | -0.937 | 0.201 | -0.061 | 0.201 | 0.016 | -0.073 | 0.035 | 0.350 | 0.223 | 0.183 | 0.012 | 0.191 | 38.483 | PROMISING (not significant after correction) |
| E1b_trigger_counter_trend | X1_time10 | 153 | 0.529 | 1.193 | -0.918 | 0.199 | 0.101 | 0.199 | -0.025 | -0.126 | 0.392 | -0.023 | 0.083 | 0.300 | -0.015 | 0.195 | 8.098 | UNSTABLE (fails a split half) |
| E1_trigger_with_trend | X5_chandelier3atr | 41 | 0.512 | 1.304 | -0.972 | 0.194 | 0.103 | 0.194 | -0.200 | -0.441 | 0.442 | -0.021 | 0.135 | 0.255 | -0.030 | 0.457 | 17.463 | INCONCLUSIVE (too few trades) |
| E2_exhaustion_confluence | X5_chandelier3atr | 72 | 0.333 | 2.549 | -1.032 | 0.161 | -0.984 | 0.142 | -0.318 | -0.617 | 0.285 | 0.030 | 0.648 | -0.097 | -0.030 | 0.350 | 13.653 | REJECT |
| E3_stage2_transition | X3_target3R | 151 | 0.430 | 1.612 | -0.994 | 0.128 | -1.015 | 0.128 | -0.103 | -0.234 | 0.218 | 0.036 | 0.192 | 0.061 | 0.055 | 0.294 | 32.921 | REJECT |
| E1b_trigger_counter_trend | X2_target2R | 148 | 0.432 | 1.758 | -1.118 | 0.126 | -1.036 | 0.126 | -0.109 | -0.297 | 0.279 | -0.041 | 0.071 | 0.171 | 0.012 | 0.206 | 17.554 | REJECT |
| E1_trigger_with_trend | X6_partial1R_then_line | 44 | 0.614 | 0.391 | -0.307 | 0.122 | 0.132 | 0.122 | -0.009 | -0.089 | 0.203 | 0.047 | 0.116 | 0.128 | -0.076 | 0.152 | 3.841 | INCONCLUSIVE (too few trades) |
| E4_anchor_reclaim | X7_stage_drop | 216 | 0.375 | 1.117 | -0.502 | 0.105 | -0.165 | 0.105 | -0.040 | -0.121 | 0.059 | 0.147 | 0.175 | 0.047 | -0.061 | 0.105 | 23.782 | PROMISING (not significant after correction) |
| E4_anchor_reclaim | X4_trendline_trail | 229 | 0.389 | 1.002 | -0.470 | 0.102 | -0.195 | 0.102 | -0.030 | -0.108 | 0.018 | 0.180 | 0.200 | 0.021 | -0.060 | 0.094 | 20.690 | PROMISING (not significant after correction) |
| E1_trigger_with_trend | X4_trendline_trail | 44 | 0.591 | 0.398 | -0.326 | 0.102 | 0.117 | 0.102 | -0.039 | -0.135 | 0.176 | 0.034 | 0.118 | 0.084 | -0.060 | 0.293 | 3.864 | INCONCLUSIVE (too few trades) |
| E1_trigger_with_trend | X7_stage_drop | 44 | 0.591 | 0.391 | -0.326 | 0.098 | 0.117 | 0.098 | -0.043 | -0.135 | 0.176 | 0.027 | 0.118 | 0.075 | -0.061 | 0.321 | 3.886 | INCONCLUSIVE (too few trades) |
| E4_anchor_reclaim | X6_partial1R_then_line | 229 | 0.432 | 0.851 | -0.480 | 0.095 | -0.108 | 0.095 | -0.008 | -0.064 | 0.047 | 0.140 | 0.165 | 0.038 | -0.076 | 0.025 | 20.502 | PROMISING (not significant after correction) |
| E3_stage2_transition | X7_stage_drop | 178 | 0.343 | 1.271 | -0.536 | 0.083 | -0.254 | 0.076 | -0.103 | -0.194 | 0.143 | 0.022 | 0.158 | 0.010 | -0.061 | 0.119 | 19.702 | REJECT |
| E4_anchor_reclaim | X5_chandelier3atr | 210 | 0.429 | 0.892 | -0.533 | 0.078 | -0.109 | 0.078 | -0.050 | -0.112 | 0.097 | 0.061 | 0.138 | 0.029 | -0.030 | 0.189 | 18.857 | REJECT |
| E3_stage2_transition | X4_trendline_trail | 178 | 0.320 | 1.106 | -0.416 | 0.071 | -0.207 | 0.064 | -0.090 | -0.153 | 0.147 | -0.007 | 0.216 | -0.070 | -0.060 | 0.112 | 15.112 | REJECT |
| E5_score4 | X2_target2R | 313 | 0.435 | 1.470 | -1.008 | 0.068 | -1.011 | 0.068 | -0.074 | -0.188 | -0.026 | 0.141 | 0.142 | -0.005 | 0.012 | 0.143 | 28.294 | REJECT |
| E3_stage2_transition | X2_target2R | 153 | 0.438 | 1.427 | -0.994 | 0.066 | -1.013 | 0.066 | -0.142 | -0.286 | 0.179 | -0.048 | 0.125 | 0.005 | 0.012 | 0.207 | 29.621 | REJECT |
| E4_anchor_reclaim | X1_time10 | 219 | 0.571 | 0.565 | -0.644 | 0.046 | 0.151 | 0.046 | -0.049 | -0.109 | 0.004 | 0.082 | 0.041 | 0.050 | -0.015 | 0.152 | 9.242 | REJECT |
| E3_stage2_transition | X6_partial1R_then_line | 178 | 0.343 | 0.892 | -0.420 | 0.030 | -0.204 | 0.030 | -0.092 | -0.137 | 0.095 | -0.037 | 0.108 | -0.048 | -0.076 | 0.045 | 15.022 | REJECT |
| E2_exhaustion_confluence | X3_target3R | 72 | 0.319 | 2.587 | -1.172 | 0.029 | -1.063 | 0.029 | -0.394 | -0.613 | 0.015 | 0.043 | 0.266 | -0.098 | 0.055 | 0.406 | 13.236 | REJECT |
| E5_score4 | X3_target3R | 304 | 0.385 | 1.632 | -1.006 | 0.009 | -1.024 | 0.009 | -0.160 | -0.248 | -0.090 | 0.086 | 0.065 | -0.047 | 0.055 | 0.216 | 31.931 | REJECT |
| E3_stage2_transition | X5_chandelier3atr | 169 | 0.396 | 1.047 | -0.680 | 0.005 | -0.223 | 0.005 | -0.148 | -0.218 | 0.083 | -0.070 | 0.073 | -0.062 | -0.030 | 0.233 | 18.006 | REJECT |
| E5_score4 | X4_trendline_trail | 376 | 0.324 | 1.235 | -0.592 | 0.001 | -0.319 | 0.001 | -0.115 | -0.193 | -0.009 | 0.008 | 0.057 | -0.049 | -0.060 | 0.070 | 19.511 | REJECT |
| E5_score4 | X7_stage_drop | 365 | 0.323 | 1.344 | -0.642 | -0.000 | -0.339 | -0.000 | -0.134 | -0.210 | 0.018 | -0.013 | 0.037 | -0.033 | -0.061 | 0.065 | 21.841 | REJECT |
| E5_score4 | X6_partial1R_then_line | 382 | 0.421 | 0.829 | -0.605 | -0.000 | -0.223 | -0.000 | -0.088 | -0.143 | 0.040 | -0.029 | 0.058 | -0.052 | -0.076 | 0.007 | 18.463 | REJECT |
| E3_stage2_transition | X1_time10 | 171 | 0.526 | 0.572 | -0.694 | -0.028 | 0.046 | -0.028 | -0.150 | -0.231 | 0.008 | -0.063 | 0.005 | -0.060 | -0.015 | 0.173 | 8.906 | REJECT |
| E5_score4 | X1_time10 | 427 | 0.518 | 0.631 | -0.749 | -0.035 | 0.029 | -0.035 | -0.118 | -0.162 | 0.007 | -0.063 | 0.049 | -0.111 | -0.015 | 0.114 | 8.714 | REJECT |
| E2_exhaustion_confluence | X4_trendline_trail | 72 | 0.444 | 0.438 | -0.493 | -0.079 | -0.059 | -0.079 | -0.223 | -0.291 | -0.043 | -0.117 | 0.009 | -0.126 | -0.060 | 0.211 | 2.556 | REJECT |
| E2_exhaustion_confluence | X6_partial1R_then_line | 72 | 0.444 | 0.431 | -0.493 | -0.082 | -0.059 | -0.082 | -0.225 | -0.291 | -0.050 | -0.116 | 0.005 | -0.129 | -0.076 | 0.110 | 2.556 | REJECT |
| E5_score4 | X5_chandelier3atr | 393 | 0.338 | 1.032 | -0.661 | -0.088 | -0.336 | -0.088 | -0.189 | -0.257 | -0.021 | -0.135 | -0.036 | -0.135 | -0.030 | 0.119 | 16.361 | REJECT |
| E1b_trigger_counter_trend | X6_partial1R_then_line | 163 | 0.454 | 0.260 | -0.385 | -0.092 | -0.038 | -0.092 | -0.173 | -0.255 | -0.104 | -0.078 | -0.131 | -0.060 | -0.076 | 0.055 | 2.061 | REJECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 163 | 0.454 | 0.253 | -0.385 | -0.095 | -0.038 | -0.095 | -0.175 | -0.257 | -0.107 | -0.082 | -0.138 | -0.060 | -0.060 | 0.118 | 2.061 | REJECT |
| E2_exhaustion_confluence | X7_stage_drop | 72 | 0.444 | 0.414 | -0.502 | -0.095 | -0.059 | -0.095 | -0.237 | -0.298 | -0.065 | -0.128 | 0.009 | -0.151 | -0.061 | 0.253 | 2.611 | REJECT |
| E1b_trigger_counter_trend | X7_stage_drop | 163 | 0.454 | 0.251 | -0.385 | -0.096 | -0.038 | -0.096 | -0.177 | -0.258 | -0.109 | -0.082 | -0.140 | -0.060 | -0.061 | 0.132 | 2.080 | REJECT |
| E2_exhaustion_confluence | X2_target2R | 72 | 0.347 | 1.905 | -1.172 | -0.104 | -1.062 | -0.104 | -0.443 | -0.585 | -0.183 | -0.020 | 0.137 | -0.232 | 0.012 | 0.282 | 9.944 | REJECT |

### Exit rules ranked (trade-weighted across setups)

| exit | trades | mean_expectancy | random_mean | edge_over_random |
|---|---|---|---|---|
| X3_target3R | 892 | 0.153 | 0.055 | 0.098 |
| X2_target2R | 905 | 0.098 | 0.012 | 0.086 |
| X5_chandelier3atr | 1,036 | 0.060 | -0.030 | 0.089 |
| X1_time10 | 1,083 | 0.041 | -0.015 | 0.056 |
| X7_stage_drop | 1,038 | 0.019 | -0.061 | 0.080 |
| X4_trendline_trail | 1,062 | 0.018 | -0.060 | 0.078 |
| X6_partial1R_then_line | 1,068 | 0.011 | -0.076 | 0.087 |

## P1b · Sizing (fixed-fractional, max open positions = 5)

| setup | exit | risk_pct | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|
| E1b_trigger_counter_trend | X5_chandelier3atr | 0.005 | 0.063 | -0.105 | 0.604 | 118,208 |
| E1b_trigger_counter_trend | X5_chandelier3atr | 0.010 | 0.121 | -0.206 | 0.589 | 136,630 |
| E1b_trigger_counter_trend | X5_chandelier3atr | 0.020 | 0.219 | -0.391 | 0.560 | 171,647 |
| E1b_trigger_counter_trend | X3_target3R | 0.005 | 0.068 | -0.119 | 0.573 | 119,682 |
| E1b_trigger_counter_trend | X3_target3R | 0.010 | 0.129 | -0.226 | 0.571 | 139,239 |
| E1b_trigger_counter_trend | X3_target3R | 0.020 | 0.225 | -0.410 | 0.550 | 174,200 |
| E4_anchor_reclaim | X3_target3R | 0.005 | 0.042 | -0.069 | 0.605 | 111,823 |
| E4_anchor_reclaim | X3_target3R | 0.010 | 0.082 | -0.135 | 0.609 | 123,884 |
| E4_anchor_reclaim | X3_target3R | 0.020 | 0.156 | -0.254 | 0.613 | 148,180 |

## P2 · Market regime (SPY > 200-day average and Trend line rising)

| setup | exit | n_on | exp_on | n_off | exp_off | diff | diff_ci_low | verdict |
|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X4_trendline_trail | 18 | 0.196 | 26 | 0.037 | 0.159 | -0.285 | NO CLEAR EFFECT |
| E1_trigger_with_trend | X5_chandelier3atr | 15 | 0.355 | 26 | 0.100 | 0.255 | -0.962 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 40 | -0.193 | 123 | -0.063 | -0.130 | -0.519 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 34 | 0.327 | 117 | 0.415 | -0.088 | -1.178 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X4_trendline_trail | 27 | -0.250 | 45 | 0.023 | -0.273 | -0.690 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 27 | -0.140 | 45 | 0.342 | -0.482 | -2.011 | NO CLEAR EFFECT |
| E3_stage2_transition | X4_trendline_trail | 116 | -0.019 | 62 | 0.239 | -0.257 | -1.032 | NO CLEAR EFFECT |
| E3_stage2_transition | X5_chandelier3atr | 110 | -0.060 | 59 | 0.126 | -0.186 | -0.789 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X4_trendline_trail | 168 | -0.019 | 61 | 0.437 | -0.456 | -1.032 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X5_chandelier3atr | 153 | -0.039 | 57 | 0.392 | -0.431 | -0.980 | NO CLEAR EFFECT |
| E5_score4 | X4_trendline_trail | 284 | -0.135 | 92 | 0.419 | -0.554 | -1.168 | NO CLEAR EFFECT |
| E5_score4 | X5_chandelier3atr | 299 | -0.157 | 94 | 0.129 | -0.286 | -0.722 | NO CLEAR EFFECT |

## P4 · Portfolio heat (E1b_trigger_counter_trend + X5_chandelier3atr)

| rule | cagr | max_dd | mar | final |
|---|---|---|---|---|
| No sector cap | 0.056 | -0.160 | 0.354 | 116,181 |
| Max 1 open per sector | 0.056 | -0.160 | 0.354 | 116,181 |

## P6 · Playbook portfolio (E4_anchor_reclaim + E1_trigger_with_trend, exit X3_target3R, 1 per symbol, 1 per sector, max 5 open)

| risk | trades | trades_per_year | expectancy | win_rate | longest_losing_streak | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|---|---|---|
| 0.50% | 197 | 72.608 | 0.287 | 0.482 | 13 | 0.079 | -0.075 | 1.042 | 122,781 |
| 0.75% | 197 | 72.608 | 0.287 | 0.482 | 13 | 0.117 | -0.111 | 1.054 | 135,147 |
| 1.00% | 197 | 72.608 | 0.287 | 0.482 | 13 | 0.156 | -0.146 | 1.066 | 148,131 |

---
**How to read verdicts.** ADOPT = ≥ min trades, bootstrap CI above 0 after correcting for the number of tests, positive in both time halves and both symbol halves, and better than random entries with the same exits. PROMISING = everything except significance. UNSTABLE = fails a half. REJECT = not positive or not better than random.