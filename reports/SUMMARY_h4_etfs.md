# IFI Lab results: h4 · etfs
_Run 2026-11-21 18:53 UTC · 16 symbols · 2023-11-10 to 2026-11-20 · split 2025-05-16 · 42 setup×exit tests (Bonferroni-adjusted) · engine v1.3.3_

## P1 · Exits × setups (R per trade, after costs)

Random-entry control (same stops and exits), mean expectancy by exit: X1_time10 -0.055R, X2_target2R -0.014R, X3_target3R -0.022R, X4_trendline_trail -0.084R, X5_chandelier3atr -0.033R, X6_partial1R_then_line -0.103R, X7_stage_drop -0.080R

| setup | exit | n | win_rate | avg_win | avg_loss | expectancy | median | exp_w10 | ci_low | ci_low_adj | exp_early | exp_late | exp_symA | exp_symB | random_mean | random_p95 | avg_bars | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E1b_trigger_counter_trend | X5_chandelier3atr | 156 | 0.423 | 2.250 | -0.884 | 0.442 | -0.354 | 0.434 | 0.107 | -0.136 | 0.498 | 0.384 | 0.226 | 0.637 | -0.033 | 0.266 | 19.333 | PROMISING (not significant after correction) |
| E1b_trigger_counter_trend | X3_target3R | 153 | 0.425 | 2.508 | -1.135 | 0.413 | -1.037 | 0.413 | 0.114 | -0.025 | 0.573 | 0.250 | 0.278 | 0.532 | -0.022 | 0.218 | 22.935 | PROMISING (not significant after correction) |
| E1_trigger_with_trend | X3_target3R | 40 | 0.425 | 2.189 | -1.098 | 0.299 | -1.031 | 0.299 | -0.234 | -0.501 | 0.452 | 0.174 | 0.267 | 0.334 | -0.022 | 0.386 | 23.975 | INCONCLUSIVE (too few trades) |
| E1_trigger_with_trend | X2_target2R | 41 | 0.488 | 1.691 | -1.140 | 0.241 | -1.016 | 0.241 | -0.199 | -0.489 | 0.483 | 0.032 | 0.204 | 0.279 | -0.014 | 0.370 | 18.707 | INCONCLUSIVE (too few trades) |
| E4_anchor_reclaim | X3_target3R | 190 | 0.468 | 1.585 | -0.960 | 0.232 | -0.170 | 0.232 | 0.031 | -0.080 | 0.196 | 0.268 | 0.270 | 0.200 | -0.022 | 0.182 | 41.779 | PROMISING (not significant after correction) |
| E1_trigger_with_trend | X1_time10 | 41 | 0.585 | 1.082 | -1.037 | 0.203 | 0.561 | 0.203 | -0.156 | -0.334 | 0.488 | -0.043 | 0.278 | 0.125 | -0.055 | 0.334 | 8.463 | INCONCLUSIVE (too few trades) |
| E4_anchor_reclaim | X2_target2R | 191 | 0.482 | 1.440 | -0.954 | 0.199 | -0.112 | 0.199 | 0.020 | -0.107 | 0.160 | 0.237 | 0.203 | 0.196 | -0.014 | 0.160 | 37.419 | PROMISING (not significant after correction) |
| E1_trigger_with_trend | X5_chandelier3atr | 41 | 0.512 | 1.304 | -0.972 | 0.194 | 0.103 | 0.194 | -0.200 | -0.441 | 0.442 | -0.021 | 0.135 | 0.255 | -0.033 | 0.567 | 17.463 | INCONCLUSIVE (too few trades) |
| E1b_trigger_counter_trend | X1_time10 | 158 | 0.525 | 1.199 | -0.926 | 0.190 | 0.100 | 0.190 | -0.012 | -0.219 | 0.392 | -0.027 | 0.072 | 0.300 | -0.055 | 0.142 | 8.108 | UNSTABLE (fails a split half) |
| E2_exhaustion_confluence | X1_time10 | 77 | 0.377 | 2.103 | -1.060 | 0.131 | -1.045 | 0.131 | -0.256 | -0.470 | 0.223 | 0.047 | 0.584 | -0.127 | -0.055 | 0.219 | 6.714 | REJECT |
| E1_trigger_with_trend | X6_partial1R_then_line | 44 | 0.614 | 0.391 | -0.307 | 0.122 | 0.132 | 0.122 | -0.009 | -0.089 | 0.203 | 0.047 | 0.116 | 0.128 | -0.103 | 0.134 | 3.841 | INCONCLUSIVE (too few trades) |
| E1b_trigger_counter_trend | X2_target2R | 153 | 0.425 | 1.819 | -1.135 | 0.120 | -1.037 | 0.120 | -0.128 | -0.251 | 0.279 | -0.042 | 0.010 | 0.217 | -0.014 | 0.184 | 17.752 | REJECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 77 | 0.312 | 2.648 | -1.035 | 0.113 | -1.045 | 0.095 | -0.365 | -0.592 | 0.285 | -0.046 | 0.434 | -0.070 | -0.033 | 0.388 | 13.416 | REJECT |
| E3_stage2_transition | X3_target3R | 155 | 0.406 | 1.718 | -0.993 | 0.109 | -1.019 | 0.109 | -0.123 | -0.275 | 0.186 | 0.031 | 0.175 | 0.041 | -0.022 | 0.212 | 33.555 | REJECT |
| E1_trigger_with_trend | X4_trendline_trail | 44 | 0.591 | 0.398 | -0.326 | 0.102 | 0.117 | 0.102 | -0.039 | -0.135 | 0.176 | 0.034 | 0.118 | 0.084 | -0.084 | 0.299 | 3.864 | INCONCLUSIVE (too few trades) |
| E1_trigger_with_trend | X7_stage_drop | 44 | 0.591 | 0.391 | -0.326 | 0.098 | 0.117 | 0.098 | -0.043 | -0.135 | 0.176 | 0.027 | 0.118 | 0.075 | -0.080 | 0.292 | 3.886 | INCONCLUSIVE (too few trades) |
| E4_anchor_reclaim | X7_stage_drop | 231 | 0.372 | 1.113 | -0.516 | 0.090 | -0.171 | 0.090 | -0.051 | -0.125 | 0.127 | 0.054 | 0.132 | 0.056 | -0.080 | 0.089 | 23.636 | PROMISING (not significant after correction) |
| E4_anchor_reclaim | X4_trendline_trail | 244 | 0.385 | 1.005 | -0.483 | 0.090 | -0.199 | 0.090 | -0.039 | -0.115 | 0.088 | 0.093 | 0.161 | 0.031 | -0.084 | 0.073 | 20.664 | PROMISING (not significant after correction) |
| E5_score4 | X2_target2R | 324 | 0.438 | 1.521 | -1.031 | 0.088 | -1.016 | 0.088 | -0.059 | -0.158 | 0.030 | 0.133 | 0.147 | 0.029 | -0.014 | 0.125 | 28.306 | REJECT |
| E4_anchor_reclaim | X6_partial1R_then_line | 244 | 0.430 | 0.854 | -0.496 | 0.085 | -0.114 | 0.085 | -0.019 | -0.068 | 0.098 | 0.072 | 0.127 | 0.050 | -0.103 | 0.000 | 20.480 | PROMISING (not significant after correction) |
| E3_stage2_transition | X7_stage_drop | 182 | 0.330 | 1.326 | -0.538 | 0.077 | -0.267 | 0.069 | -0.108 | -0.212 | 0.129 | 0.023 | 0.136 | 0.019 | -0.080 | 0.090 | 20.137 | REJECT |
| E3_stage2_transition | X2_target2R | 157 | 0.427 | 1.502 | -0.996 | 0.070 | -1.016 | 0.070 | -0.124 | -0.227 | 0.148 | -0.009 | 0.124 | 0.015 | -0.014 | 0.187 | 29.955 | REJECT |
| E3_stage2_transition | X4_trendline_trail | 182 | 0.308 | 1.133 | -0.413 | 0.063 | -0.208 | 0.055 | -0.102 | -0.169 | 0.146 | -0.023 | 0.201 | -0.073 | -0.084 | 0.109 | 15.368 | REJECT |
| E4_anchor_reclaim | X5_chandelier3atr | 224 | 0.424 | 0.892 | -0.549 | 0.062 | -0.125 | 0.062 | -0.053 | -0.124 | 0.117 | 0.009 | 0.101 | 0.031 | -0.033 | 0.223 | 18.643 | REJECT |
| E4_anchor_reclaim | X1_time10 | 233 | 0.571 | 0.571 | -0.663 | 0.041 | 0.151 | 0.041 | -0.053 | -0.129 | 0.037 | 0.046 | 0.025 | 0.055 | -0.055 | 0.103 | 9.210 | REJECT |
| E3_stage2_transition | X6_partial1R_then_line | 182 | 0.335 | 0.902 | -0.420 | 0.023 | -0.205 | 0.023 | -0.097 | -0.175 | 0.095 | -0.049 | 0.096 | -0.048 | -0.103 | 0.018 | 15.275 | UNSTABLE (fails a split half) |
| E5_score4 | X7_stage_drop | 375 | 0.328 | 1.351 | -0.647 | 0.009 | -0.340 | 0.009 | -0.121 | -0.226 | 0.098 | -0.059 | 0.030 | -0.011 | -0.080 | 0.053 | 22.088 | REJECT |
| E3_stage2_transition | X5_chandelier3atr | 173 | 0.387 | 1.074 | -0.672 | 0.004 | -0.239 | 0.004 | -0.156 | -0.255 | 0.060 | -0.050 | 0.060 | -0.051 | -0.033 | 0.251 | 18.254 | REJECT |
| E5_score4 | X4_trendline_trail | 386 | 0.326 | 1.240 | -0.596 | 0.003 | -0.333 | 0.003 | -0.117 | -0.188 | 0.067 | -0.045 | 0.050 | -0.038 | -0.084 | 0.042 | 19.635 | REJECT |
| E5_score4 | X6_partial1R_then_line | 392 | 0.423 | 0.832 | -0.611 | 0.000 | -0.229 | 0.000 | -0.084 | -0.127 | 0.075 | -0.054 | 0.049 | -0.043 | -0.103 | -0.023 | 18.607 | UNSTABLE (fails a split half) |
| E2_exhaustion_confluence | X3_target3R | 77 | 0.299 | 2.714 | -1.162 | -0.004 | -1.062 | -0.004 | -0.407 | -0.629 | 0.015 | -0.022 | 0.169 | -0.103 | -0.022 | 0.311 | 12.714 | REJECT |
| E5_score4 | X3_target3R | 314 | 0.376 | 1.662 | -1.023 | -0.014 | -1.027 | -0.014 | -0.170 | -0.261 | -0.006 | -0.020 | 0.025 | -0.053 | -0.022 | 0.140 | 32.487 | REJECT |
| E3_stage2_transition | X1_time10 | 175 | 0.531 | 0.568 | -0.698 | -0.025 | 0.053 | -0.025 | -0.148 | -0.198 | -0.005 | -0.046 | 0.012 | -0.063 | -0.055 | 0.137 | 8.926 | REJECT |
| E5_score4 | X1_time10 | 438 | 0.523 | 0.628 | -0.769 | -0.039 | 0.034 | -0.039 | -0.122 | -0.163 | 0.029 | -0.086 | 0.043 | -0.113 | -0.055 | 0.060 | 8.760 | REJECT |
| E5_score4 | X5_chandelier3atr | 403 | 0.340 | 1.044 | -0.668 | -0.086 | -0.342 | -0.086 | -0.193 | -0.234 | 0.025 | -0.166 | -0.049 | -0.119 | -0.033 | 0.158 | 16.551 | REJECT |
| E1b_trigger_counter_trend | X6_partial1R_then_line | 169 | 0.444 | 0.259 | -0.404 | -0.110 | -0.047 | -0.110 | -0.193 | -0.247 | -0.104 | -0.116 | -0.166 | -0.060 | -0.103 | 0.026 | 2.059 | REJECT |
| E2_exhaustion_confluence | X4_trendline_trail | 77 | 0.429 | 0.436 | -0.524 | -0.112 | -0.080 | -0.112 | -0.251 | -0.333 | -0.043 | -0.176 | -0.036 | -0.156 | -0.084 | 0.210 | 2.506 | REJECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 169 | 0.444 | 0.252 | -0.404 | -0.113 | -0.047 | -0.113 | -0.195 | -0.248 | -0.107 | -0.120 | -0.172 | -0.060 | -0.084 | 0.107 | 2.059 | REJECT |
| E1b_trigger_counter_trend | X7_stage_drop | 169 | 0.444 | 0.250 | -0.404 | -0.114 | -0.047 | -0.114 | -0.196 | -0.248 | -0.109 | -0.120 | -0.174 | -0.060 | -0.080 | 0.100 | 2.077 | REJECT |
| E2_exhaustion_confluence | X6_partial1R_then_line | 77 | 0.429 | 0.429 | -0.524 | -0.115 | -0.080 | -0.115 | -0.253 | -0.332 | -0.050 | -0.176 | -0.040 | -0.159 | -0.103 | 0.090 | 2.506 | REJECT |
| E2_exhaustion_confluence | X7_stage_drop | 77 | 0.429 | 0.412 | -0.532 | -0.128 | -0.080 | -0.128 | -0.266 | -0.343 | -0.065 | -0.186 | -0.036 | -0.180 | -0.080 | 0.183 | 2.558 | REJECT |
| E2_exhaustion_confluence | X2_target2R | 77 | 0.325 | 1.933 | -1.161 | -0.157 | -1.061 | -0.157 | -0.480 | -0.641 | -0.183 | -0.132 | 0.010 | -0.252 | -0.014 | 0.255 | 9.532 | REJECT |

### Exit rules ranked (trade-weighted across setups)

| exit | trades | mean_expectancy | random_mean | edge_over_random |
|---|---|---|---|---|
| X3_target3R | 929 | 0.142 | -0.022 | 0.164 |
| X2_target2R | 943 | 0.099 | -0.014 | 0.113 |
| X5_chandelier3atr | 1,074 | 0.061 | -0.033 | 0.094 |
| X1_time10 | 1,122 | 0.033 | -0.055 | 0.088 |
| X7_stage_drop | 1,078 | 0.012 | -0.080 | 0.092 |
| X4_trendline_trail | 1,102 | 0.010 | -0.084 | 0.094 |
| X6_partial1R_then_line | 1,108 | 0.003 | -0.103 | 0.105 |

## P1b · Sizing (fixed-fractional, max open positions = 5)

| setup | exit | risk_pct | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|
| E1b_trigger_counter_trend | X5_chandelier3atr | 0.005 | 0.075 | -0.106 | 0.708 | 122,755 |
| E1b_trigger_counter_trend | X5_chandelier3atr | 0.010 | 0.145 | -0.203 | 0.716 | 146,701 |
| E1b_trigger_counter_trend | X5_chandelier3atr | 0.020 | 0.266 | -0.374 | 0.712 | 194,910 |
| E1b_trigger_counter_trend | X3_target3R | 0.005 | 0.069 | -0.119 | 0.584 | 120,910 |
| E1b_trigger_counter_trend | X3_target3R | 0.010 | 0.132 | -0.226 | 0.586 | 142,207 |
| E1b_trigger_counter_trend | X3_target3R | 0.020 | 0.235 | -0.410 | 0.575 | 182,029 |
| E4_anchor_reclaim | X3_target3R | 0.005 | 0.032 | -0.069 | 0.464 | 109,357 |
| E4_anchor_reclaim | X3_target3R | 0.010 | 0.062 | -0.135 | 0.459 | 118,463 |
| E4_anchor_reclaim | X3_target3R | 0.020 | 0.114 | -0.255 | 0.446 | 135,420 |

## P2 · Market regime (SPY > 200-day average and Trend line rising)

| setup | exit | n_on | exp_on | n_off | exp_off | diff | diff_ci_low | verdict |
|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X4_trendline_trail | 18 | 0.196 | 26 | 0.037 | 0.159 | -0.285 | NO CLEAR EFFECT |
| E1_trigger_with_trend | X5_chandelier3atr | 15 | 0.355 | 26 | 0.100 | 0.255 | -0.962 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 41 | -0.246 | 128 | -0.070 | -0.176 | -0.555 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 35 | 0.540 | 121 | 0.414 | 0.126 | -1.064 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X4_trendline_trail | 29 | -0.287 | 48 | -0.007 | -0.281 | -0.649 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 29 | -0.234 | 48 | 0.322 | -0.556 | -2.063 | NO CLEAR EFFECT |
| E3_stage2_transition | X4_trendline_trail | 118 | -0.033 | 64 | 0.239 | -0.273 | -1.081 | NO CLEAR EFFECT |
| E3_stage2_transition | X5_chandelier3atr | 112 | -0.063 | 61 | 0.128 | -0.191 | -0.749 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X4_trendline_trail | 173 | -0.023 | 71 | 0.366 | -0.388 | -0.980 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X5_chandelier3atr | 158 | -0.052 | 66 | 0.334 | -0.386 | -0.826 | NO CLEAR EFFECT |
| E5_score4 | X4_trendline_trail | 287 | -0.125 | 99 | 0.376 | -0.502 | -1.104 | NO CLEAR EFFECT |
| E5_score4 | X5_chandelier3atr | 302 | -0.147 | 101 | 0.098 | -0.245 | -0.692 | NO CLEAR EFFECT |

## P4 · Portfolio heat (E1b_trigger_counter_trend + X5_chandelier3atr)

| rule | cagr | max_dd | mar | final |
|---|---|---|---|---|
| No sector cap | 0.075 | -0.156 | 0.480 | 122,580 |
| Max 1 open per sector | 0.075 | -0.156 | 0.480 | 122,580 |

## P6 · Playbook portfolio (E4_anchor_reclaim + E1_trigger_with_trend, exit X3_target3R, 1 per symbol, 1 per sector, max 5 open)

| risk | trades | trades_per_year | expectancy | win_rate | longest_losing_streak | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|---|---|---|
| 0.50% | 210 | 74.468 | 0.267 | 0.467 | 13 | 0.057 | -0.080 | 0.716 | 117,076 |
| 0.75% | 210 | 74.468 | 0.267 | 0.467 | 13 | 0.085 | -0.118 | 0.718 | 125,881 |
| 1.00% | 210 | 74.468 | 0.267 | 0.467 | 13 | 0.112 | -0.155 | 0.719 | 134,800 |

---
**How to read verdicts.** ADOPT = ≥ min trades, bootstrap CI above 0 after correcting for the number of tests, positive in both time halves and both symbol halves, and better than random entries with the same exits. PROMISING = everything except significance. UNSTABLE = fails a half. REJECT = not positive or not better than random.