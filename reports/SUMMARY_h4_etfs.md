# IFI Lab results: h4 · etfs
_Run 2026-10-17 15:15 UTC · 16 symbols · 2023-11-10 to 2026-10-16 · split 2025-04-28 · 42 setup×exit tests (Bonferroni-adjusted) · engine v1.3.3_

## P1 · Exits × setups (R per trade, after costs)

Random-entry control (same stops and exits), mean expectancy by exit: X1_time10 -0.015R, X2_target2R -0.018R, X3_target3R +0.005R, X4_trendline_trail -0.027R, X5_chandelier3atr -0.055R, X6_partial1R_then_line -0.054R, X7_stage_drop -0.020R

| setup | exit | n | win_rate | avg_win | avg_loss | expectancy | median | exp_w10 | ci_low | ci_low_adj | exp_early | exp_late | exp_symA | exp_symB | random_mean | random_p95 | avg_bars | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E1b_trigger_counter_trend | X5_chandelier3atr | 152 | 0.421 | 2.233 | -0.876 | 0.433 | -0.354 | 0.422 | 0.087 | -0.068 | 0.498 | 0.361 | 0.241 | 0.597 | -0.055 | 0.281 | 18.658 | PROMISING (not significant after correction) |
| E1b_trigger_counter_trend | X3_target3R | 149 | 0.430 | 2.391 | -1.121 | 0.387 | -1.037 | 0.387 | 0.086 | -0.087 | 0.573 | 0.189 | 0.303 | 0.458 | 0.005 | 0.235 | 22.497 | PROMISING (not significant after correction) |
| E1_trigger_with_trend | X3_target3R | 40 | 0.425 | 2.190 | -1.098 | 0.299 | -1.031 | 0.299 | -0.234 | -0.501 | 0.452 | 0.174 | 0.267 | 0.334 | 0.005 | 0.415 | 23.975 | INCONCLUSIVE (too few trades) |
| E4_anchor_reclaim | X3_target3R | 182 | 0.478 | 1.531 | -0.936 | 0.243 | -0.140 | 0.243 | 0.034 | -0.063 | 0.071 | 0.387 | 0.258 | 0.231 | 0.005 | 0.209 | 42.220 | PROMISING (not significant after correction) |
| E1_trigger_with_trend | X2_target2R | 41 | 0.488 | 1.692 | -1.140 | 0.241 | -1.016 | 0.241 | -0.199 | -0.489 | 0.483 | 0.032 | 0.205 | 0.279 | -0.018 | 0.354 | 18.707 | INCONCLUSIVE (too few trades) |
| E1_trigger_with_trend | X1_time10 | 41 | 0.585 | 1.082 | -1.037 | 0.203 | 0.561 | 0.203 | -0.156 | -0.334 | 0.488 | -0.042 | 0.278 | 0.125 | -0.015 | 0.466 | 8.463 | INCONCLUSIVE (too few trades) |
| E4_anchor_reclaim | X2_target2R | 183 | 0.481 | 1.424 | -0.932 | 0.201 | -0.137 | 0.201 | 0.027 | -0.072 | 0.035 | 0.342 | 0.223 | 0.182 | -0.018 | 0.151 | 37.754 | PROMISING (not significant after correction) |
| E2_exhaustion_confluence | X1_time10 | 73 | 0.397 | 2.103 | -1.060 | 0.197 | -1.042 | 0.197 | -0.220 | -0.456 | 0.223 | 0.170 | 0.710 | -0.087 | -0.015 | 0.325 | 6.918 | REJECT |
| E1b_trigger_counter_trend | X1_time10 | 154 | 0.526 | 1.200 | -0.917 | 0.196 | 0.100 | 0.196 | -0.030 | -0.147 | 0.392 | -0.027 | 0.070 | 0.307 | -0.015 | 0.203 | 8.058 | REJECT |
| E1_trigger_with_trend | X5_chandelier3atr | 41 | 0.512 | 1.305 | -0.972 | 0.194 | 0.103 | 0.194 | -0.200 | -0.441 | 0.442 | -0.021 | 0.135 | 0.255 | -0.055 | 0.639 | 17.463 | INCONCLUSIVE (too few trades) |
| E2_exhaustion_confluence | X5_chandelier3atr | 73 | 0.329 | 2.574 | -1.033 | 0.153 | -0.992 | 0.134 | -0.331 | -0.597 | 0.285 | 0.017 | 0.548 | -0.065 | -0.055 | 0.503 | 13.616 | REJECT |
| E1b_trigger_counter_trend | X2_target2R | 149 | 0.430 | 1.794 | -1.121 | 0.131 | -1.037 | 0.131 | -0.119 | -0.255 | 0.279 | -0.027 | 0.050 | 0.199 | -0.018 | 0.168 | 17.597 | REJECT |
| E3_stage2_transition | X3_target3R | 153 | 0.425 | 1.637 | -0.986 | 0.128 | -1.013 | 0.128 | -0.100 | -0.227 | 0.218 | 0.040 | 0.191 | 0.065 | 0.005 | 0.231 | 33.163 | REJECT |
| E1_trigger_with_trend | X6_partial1R_then_line | 44 | 0.614 | 0.391 | -0.307 | 0.122 | 0.132 | 0.122 | -0.009 | -0.089 | 0.203 | 0.047 | 0.116 | 0.128 | -0.054 | 0.367 | 3.841 | INCONCLUSIVE (too few trades) |
| E1_trigger_with_trend | X4_trendline_trail | 44 | 0.591 | 0.398 | -0.326 | 0.102 | 0.117 | 0.102 | -0.039 | -0.135 | 0.176 | 0.034 | 0.119 | 0.084 | -0.027 | 0.759 | 3.864 | INCONCLUSIVE (too few trades) |
| E1_trigger_with_trend | X7_stage_drop | 44 | 0.591 | 0.391 | -0.326 | 0.098 | 0.117 | 0.098 | -0.043 | -0.135 | 0.176 | 0.026 | 0.119 | 0.075 | -0.020 | 0.827 | 3.886 | INCONCLUSIVE (too few trades) |
| E3_stage2_transition | X7_stage_drop | 181 | 0.343 | 1.273 | -0.527 | 0.089 | -0.252 | 0.082 | -0.087 | -0.184 | 0.143 | 0.036 | 0.171 | 0.010 | -0.020 | 0.277 | 19.729 | REJECT |
| E4_anchor_reclaim | X7_stage_drop | 224 | 0.357 | 1.155 | -0.504 | 0.088 | -0.184 | 0.088 | -0.058 | -0.146 | 0.059 | 0.113 | 0.156 | 0.034 | -0.020 | 0.246 | 23.174 | REJECT |
| E4_anchor_reclaim | X4_trendline_trail | 237 | 0.371 | 1.036 | -0.471 | 0.088 | -0.205 | 0.088 | -0.043 | -0.110 | 0.018 | 0.149 | 0.181 | 0.013 | -0.027 | 0.230 | 20.198 | REJECT |
| E4_anchor_reclaim | X6_partial1R_then_line | 237 | 0.418 | 0.865 | -0.484 | 0.080 | -0.159 | 0.080 | -0.024 | -0.070 | 0.047 | 0.108 | 0.145 | 0.027 | -0.054 | 0.089 | 20.013 | REJECT |
| E4_anchor_reclaim | X5_chandelier3atr | 216 | 0.421 | 0.906 | -0.538 | 0.070 | -0.136 | 0.070 | -0.058 | -0.114 | 0.097 | 0.047 | 0.126 | 0.026 | -0.055 | 0.218 | 18.486 | REJECT |
| E5_score4 | X2_target2R | 318 | 0.443 | 1.451 | -1.030 | 0.070 | -1.011 | 0.070 | -0.078 | -0.189 | -0.026 | 0.142 | 0.141 | -0.000 | -0.018 | 0.114 | 28.044 | REJECT |
| E3_stage2_transition | X2_target2R | 156 | 0.436 | 1.439 | -0.990 | 0.069 | -0.831 | 0.069 | -0.138 | -0.252 | 0.179 | -0.039 | 0.151 | -0.015 | -0.018 | 0.185 | 29.455 | REJECT |
| E3_stage2_transition | X4_trendline_trail | 181 | 0.315 | 1.118 | -0.414 | 0.068 | -0.208 | 0.061 | -0.088 | -0.173 | 0.147 | -0.010 | 0.209 | -0.068 | -0.027 | 0.283 | 15.061 | REJECT |
| E2_exhaustion_confluence | X3_target3R | 73 | 0.315 | 2.728 | -1.170 | 0.058 | -1.062 | 0.058 | -0.367 | -0.567 | 0.015 | 0.103 | 0.263 | -0.055 | 0.005 | 0.339 | 13.247 | REJECT |
| E4_anchor_reclaim | X1_time10 | 224 | 0.571 | 0.563 | -0.638 | 0.048 | 0.141 | 0.048 | -0.052 | -0.116 | 0.004 | 0.085 | 0.027 | 0.065 | -0.015 | 0.165 | 9.156 | REJECT |
| E3_stage2_transition | X6_partial1R_then_line | 181 | 0.343 | 0.888 | -0.421 | 0.028 | -0.205 | 0.028 | -0.086 | -0.151 | 0.095 | -0.039 | 0.103 | -0.045 | -0.054 | 0.110 | 14.967 | REJECT |
| E5_score4 | X3_target3R | 309 | 0.395 | 1.585 | -1.022 | 0.007 | -1.023 | 0.007 | -0.153 | -0.230 | -0.090 | 0.081 | 0.058 | -0.042 | 0.005 | 0.157 | 31.741 | REJECT |
| E5_score4 | X6_partial1R_then_line | 386 | 0.427 | 0.830 | -0.609 | 0.006 | -0.219 | 0.006 | -0.082 | -0.126 | 0.040 | -0.017 | 0.054 | -0.036 | -0.054 | 0.053 | 18.464 | REJECT |
| E3_stage2_transition | X5_chandelier3atr | 172 | 0.395 | 1.055 | -0.682 | 0.005 | -0.232 | 0.005 | -0.148 | -0.227 | 0.083 | -0.068 | 0.074 | -0.063 | -0.055 | 0.300 | 18.041 | REJECT |
| E5_score4 | X4_trendline_trail | 380 | 0.329 | 1.213 | -0.591 | 0.002 | -0.317 | 0.002 | -0.110 | -0.175 | -0.009 | 0.010 | 0.036 | -0.027 | -0.027 | 0.173 | 19.418 | REJECT |
| E5_score4 | X7_stage_drop | 369 | 0.328 | 1.315 | -0.639 | 0.002 | -0.335 | 0.002 | -0.125 | -0.203 | 0.018 | -0.010 | 0.015 | -0.010 | -0.020 | 0.176 | 21.732 | REJECT |
| E5_score4 | X1_time10 | 431 | 0.529 | 0.639 | -0.763 | -0.021 | 0.050 | -0.021 | -0.105 | -0.137 | 0.007 | -0.040 | 0.056 | -0.091 | -0.015 | 0.113 | 8.733 | REJECT |
| E3_stage2_transition | X1_time10 | 174 | 0.529 | 0.575 | -0.690 | -0.021 | 0.053 | -0.021 | -0.134 | -0.229 | 0.008 | -0.049 | 0.025 | -0.067 | -0.015 | 0.178 | 8.937 | REJECT |
| E5_score4 | X5_chandelier3atr | 397 | 0.350 | 1.022 | -0.667 | -0.075 | -0.314 | -0.075 | -0.180 | -0.229 | -0.021 | -0.113 | -0.035 | -0.111 | -0.055 | 0.139 | 16.363 | REJECT |
| E2_exhaustion_confluence | X4_trendline_trail | 73 | 0.425 | 0.450 | -0.482 | -0.086 | -0.071 | -0.086 | -0.231 | -0.289 | -0.043 | -0.130 | -0.015 | -0.126 | -0.027 | 0.565 | 2.548 | REJECT |
| E2_exhaustion_confluence | X6_partial1R_then_line | 73 | 0.425 | 0.443 | -0.482 | -0.089 | -0.071 | -0.089 | -0.231 | -0.292 | -0.050 | -0.130 | -0.019 | -0.128 | -0.054 | 0.236 | 2.548 | REJECT |
| E1b_trigger_counter_trend | X6_partial1R_then_line | 164 | 0.451 | 0.260 | -0.391 | -0.097 | -0.039 | -0.097 | -0.181 | -0.231 | -0.104 | -0.089 | -0.142 | -0.060 | -0.054 | 0.123 | 2.061 | REJECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 164 | 0.451 | 0.253 | -0.391 | -0.100 | -0.039 | -0.100 | -0.182 | -0.232 | -0.107 | -0.093 | -0.148 | -0.060 | -0.027 | 0.300 | 2.061 | REJECT |
| E1b_trigger_counter_trend | X7_stage_drop | 164 | 0.451 | 0.251 | -0.391 | -0.101 | -0.039 | -0.101 | -0.183 | -0.233 | -0.109 | -0.093 | -0.151 | -0.060 | -0.020 | 0.316 | 2.079 | REJECT |
| E2_exhaustion_confluence | X7_stage_drop | 73 | 0.425 | 0.424 | -0.491 | -0.102 | -0.071 | -0.102 | -0.241 | -0.298 | -0.065 | -0.141 | -0.015 | -0.150 | -0.020 | 0.577 | 2.603 | REJECT |
| E2_exhaustion_confluence | X2_target2R | 73 | 0.342 | 1.933 | -1.170 | -0.107 | -1.062 | -0.107 | -0.460 | -0.680 | -0.183 | -0.029 | 0.092 | -0.217 | -0.018 | 0.256 | 9.890 | REJECT |

### Exit rules ranked (trade-weighted across setups)

| exit | trades | mean_expectancy | random_mean | edge_over_random |
|---|---|---|---|---|
| X3_target3R | 906 | 0.155 | 0.005 | 0.150 |
| X2_target2R | 920 | 0.099 | -0.018 | 0.117 |
| X5_chandelier3atr | 1,051 | 0.067 | -0.055 | 0.122 |
| X1_time10 | 1,097 | 0.046 | -0.015 | 0.061 |
| X7_stage_drop | 1,055 | 0.016 | -0.020 | 0.036 |
| X4_trendline_trail | 1,079 | 0.015 | -0.027 | 0.042 |
| X6_partial1R_then_line | 1,085 | 0.008 | -0.054 | 0.062 |

## P1b · Sizing (fixed-fractional, max open positions = 5)

| setup | exit | risk_pct | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|
| E1b_trigger_counter_trend | X5_chandelier3atr | 0.005 | 0.050 | -0.103 | 0.484 | 114,316 |
| E1b_trigger_counter_trend | X5_chandelier3atr | 0.010 | 0.094 | -0.198 | 0.478 | 128,068 |
| E1b_trigger_counter_trend | X5_chandelier3atr | 0.020 | 0.165 | -0.362 | 0.457 | 152,056 |
| E1b_trigger_counter_trend | X3_target3R | 0.005 | 0.064 | -0.119 | 0.539 | 118,519 |
| E1b_trigger_counter_trend | X3_target3R | 0.010 | 0.122 | -0.226 | 0.538 | 136,952 |
| E1b_trigger_counter_trend | X3_target3R | 0.020 | 0.214 | -0.411 | 0.521 | 170,260 |
| E4_anchor_reclaim | X3_target3R | 0.005 | 0.038 | -0.070 | 0.541 | 110,588 |
| E4_anchor_reclaim | X3_target3R | 0.010 | 0.073 | -0.135 | 0.541 | 121,197 |
| E4_anchor_reclaim | X3_target3R | 0.020 | 0.137 | -0.255 | 0.539 | 141,983 |

## P2 · Market regime (SPY > 200-day average and Trend line rising)

| setup | exit | n_on | exp_on | n_off | exp_off | diff | diff_ci_low | verdict |
|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X4_trendline_trail | 18 | 0.196 | 26 | 0.037 | 0.159 | -0.285 | NO CLEAR EFFECT |
| E1_trigger_with_trend | X5_chandelier3atr | 15 | 0.355 | 26 | 0.101 | 0.254 | -0.962 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 40 | -0.197 | 124 | -0.069 | -0.128 | -0.540 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 34 | 0.533 | 118 | 0.404 | 0.129 | -1.083 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X4_trendline_trail | 28 | -0.255 | 45 | 0.019 | -0.274 | -0.670 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 28 | -0.204 | 45 | 0.375 | -0.580 | -2.026 | NO CLEAR EFFECT |
| E3_stage2_transition | X4_trendline_trail | 118 | -0.024 | 63 | 0.240 | -0.264 | -1.047 | NO CLEAR EFFECT |
| E3_stage2_transition | X5_chandelier3atr | 112 | -0.062 | 60 | 0.129 | -0.191 | -0.797 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X4_trendline_trail | 172 | -0.021 | 65 | 0.378 | -0.399 | -0.966 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X5_chandelier3atr | 156 | -0.039 | 60 | 0.353 | -0.392 | -0.886 | NO CLEAR EFFECT |
| E5_score4 | X4_trendline_trail | 285 | -0.126 | 95 | 0.388 | -0.514 | -1.064 | NO CLEAR EFFECT |
| E5_score4 | X5_chandelier3atr | 300 | -0.141 | 97 | 0.126 | -0.266 | -0.681 | NO CLEAR EFFECT |

## P4 · Portfolio heat (E1b_trigger_counter_trend + X5_chandelier3atr)

| rule | cagr | max_dd | mar | final |
|---|---|---|---|---|
| No sector cap | 0.093 | -0.171 | 0.541 | 127,522 |
| Max 1 open per sector | 0.093 | -0.171 | 0.541 | 127,522 |

## P6 · Playbook portfolio (E4_anchor_reclaim + E1_trigger_with_trend, exit X3_target3R, 1 per symbol, 1 per sector, max 5 open)

| risk | trades | trades_per_year | expectancy | win_rate | longest_losing_streak | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|---|---|---|
| 0.50% | 202 | 74.151 | 0.278 | 0.475 | 13 | 0.070 | -0.075 | 0.922 | 120,104 |
| 0.75% | 202 | 74.151 | 0.278 | 0.475 | 13 | 0.104 | -0.111 | 0.930 | 130,815 |
| 1.00% | 202 | 74.151 | 0.278 | 0.475 | 13 | 0.137 | -0.146 | 0.937 | 141,919 |

---
**How to read verdicts.** ADOPT = ≥ min trades, bootstrap CI above 0 after correcting for the number of tests, positive in both time halves and both symbol halves, and better than random entries with the same exits. PROMISING = everything except significance. UNSTABLE = fails a half. REJECT = not positive or not better than random.