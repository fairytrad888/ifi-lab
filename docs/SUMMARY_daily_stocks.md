# IFI Lab results: daily · stocks
_Run 2026-10-12 16:35 UTC · 61 symbols · 2000-01-03 to 2026-10-12 · split 2015-01-01 · 42 setup×exit tests (Bonferroni-adjusted) · engine v1.1_

> **Survivorship bias:** this stock list was chosen in 2026 from today's large caps, so random long entries earn money too. Judge stock setups by their edge over the random-entry control, not by raw expectancy.

## P1 · Exits × setups (R per trade, after costs)

Random-entry control (same stops and exits), mean expectancy by exit: X1_time10 +0.028R, X2_target2R +0.101R, X3_target3R +0.146R, X4_trendline_trail +0.047R, X5_chandelier3atr +0.133R, X6_partial1R_then_line -0.002R, X7_stage_drop +0.062R

| setup | exit | n | win_rate | avg_win | avg_loss | expectancy | median | exp_w10 | ci_low | ci_low_adj | exp_early | exp_late | exp_symA | exp_symB | random_mean | random_p95 | avg_bars | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 522 | 0.412 | 2.271 | -1.039 | 0.324 | -1.018 | 0.324 | 0.181 | 0.113 | 0.278 | 0.376 | 0.353 | 0.295 | 0.146 | 0.274 | 26.814 | ADOPT |
| E1_trigger_with_trend | X5_chandelier3atr | 524 | 0.433 | 1.673 | -0.776 | 0.285 | -0.261 | 0.270 | 0.140 | 0.051 | 0.210 | 0.369 | 0.381 | 0.187 | 0.133 | 0.287 | 20.010 | REJECT |
| E4_anchor_reclaim | X3_target3R | 3157 | 0.475 | 1.655 | -0.960 | 0.281 | -0.191 | 0.281 | 0.229 | 0.191 | 0.244 | 0.321 | 0.314 | 0.248 | 0.146 | 0.198 | 39.005 | ADOPT |
| E1_trigger_with_trend | X2_target2R | 523 | 0.453 | 1.795 | -1.044 | 0.242 | -1.012 | 0.242 | 0.116 | 0.037 | 0.236 | 0.250 | 0.238 | 0.247 | 0.101 | 0.204 | 21.539 | ADOPT |
| E4_anchor_reclaim | X2_target2R | 3161 | 0.492 | 1.453 | -0.963 | 0.226 | -0.046 | 0.226 | 0.181 | 0.150 | 0.201 | 0.251 | 0.249 | 0.202 | 0.101 | 0.144 | 34.604 | ADOPT |
| E1b_trigger_counter_trend | X3_target3R | 2502 | 0.390 | 2.164 | -1.050 | 0.204 | -1.016 | 0.204 | 0.137 | 0.085 | 0.141 | 0.288 | 0.206 | 0.202 | 0.146 | 0.205 | 26.054 | REJECT |
| E5_score4 | X3_target3R | 5292 | 0.418 | 1.914 | -1.025 | 0.203 | -1.015 | 0.203 | 0.159 | 0.143 | 0.184 | 0.224 | 0.211 | 0.196 | 0.146 | 0.187 | 32.438 | ADOPT |
| E3_stage2_transition | X3_target3R | 2504 | 0.413 | 1.891 | -1.000 | 0.195 | -1.012 | 0.195 | 0.133 | 0.110 | 0.198 | 0.192 | 0.165 | 0.224 | 0.146 | 0.203 | 34.198 | REJECT |
| E3_stage2_transition | X2_target2R | 2536 | 0.446 | 1.619 | -1.003 | 0.166 | -1.007 | 0.166 | 0.109 | 0.085 | 0.171 | 0.161 | 0.145 | 0.187 | 0.101 | 0.150 | 28.849 | ADOPT |
| E5_score4 | X2_target2R | 5594 | 0.452 | 1.607 | -1.023 | 0.166 | -1.008 | 0.166 | 0.130 | 0.101 | 0.146 | 0.187 | 0.174 | 0.158 | 0.101 | 0.133 | 27.846 | ADOPT |
| E1_trigger_with_trend | X1_time10 | 526 | 0.540 | 0.958 | -0.774 | 0.161 | 0.119 | 0.161 | 0.070 | 0.023 | 0.150 | 0.173 | 0.169 | 0.152 | 0.028 | 0.127 | 8.641 | ADOPT |
| E4_anchor_reclaim | X7_stage_drop | 3898 | 0.367 | 1.369 | -0.552 | 0.152 | -0.254 | 0.150 | 0.109 | 0.088 | 0.128 | 0.178 | 0.168 | 0.137 | 0.062 | 0.110 | 23.626 | ADOPT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 2589 | 0.382 | 1.711 | -0.825 | 0.143 | -0.441 | 0.139 | 0.075 | 0.038 | 0.046 | 0.274 | 0.156 | 0.130 | 0.133 | 0.201 | 19.519 | REJECT |
| E5_score4 | X7_stage_drop | 6388 | 0.353 | 1.586 | -0.647 | 0.142 | -0.305 | 0.132 | 0.102 | 0.088 | 0.132 | 0.153 | 0.135 | 0.149 | 0.062 | 0.099 | 22.580 | ADOPT |
| E3_stage2_transition | X5_chandelier3atr | 2855 | 0.394 | 1.379 | -0.666 | 0.139 | -0.277 | 0.134 | 0.090 | 0.057 | 0.130 | 0.150 | 0.102 | 0.177 | 0.133 | 0.199 | 20.642 | REJECT |
| E1b_trigger_counter_trend | X2_target2R | 2508 | 0.426 | 1.729 | -1.051 | 0.133 | -1.012 | 0.133 | 0.075 | 0.040 | 0.070 | 0.217 | 0.149 | 0.118 | 0.101 | 0.149 | 21.077 | REJECT |
| E4_anchor_reclaim | X5_chandelier3atr | 3564 | 0.420 | 1.133 | -0.596 | 0.130 | -0.192 | 0.129 | 0.091 | 0.071 | 0.088 | 0.174 | 0.150 | 0.111 | 0.133 | 0.189 | 21.666 | REJECT |
| E5_score4 | X4_trendline_trail | 6736 | 0.338 | 1.484 | -0.570 | 0.125 | -0.284 | 0.116 | 0.091 | 0.073 | 0.107 | 0.144 | 0.128 | 0.121 | 0.047 | 0.080 | 19.867 | ADOPT |
| E4_anchor_reclaim | X4_trendline_trail | 4272 | 0.336 | 1.284 | -0.474 | 0.116 | -0.251 | 0.114 | 0.081 | 0.053 | 0.087 | 0.146 | 0.125 | 0.107 | 0.047 | 0.087 | 19.744 | ADOPT |
| E5_score4 | X5_chandelier3atr | 6524 | 0.390 | 1.366 | -0.690 | 0.112 | -0.286 | 0.107 | 0.077 | 0.057 | 0.104 | 0.119 | 0.097 | 0.127 | 0.133 | 0.175 | 19.521 | REJECT |
| E3_stage2_transition | X7_stage_drop | 3119 | 0.319 | 1.438 | -0.515 | 0.108 | -0.283 | 0.104 | 0.059 | 0.033 | 0.110 | 0.107 | 0.066 | 0.151 | 0.062 | 0.113 | 18.298 | REJECT |
| E2_exhaustion_confluence | X3_target3R | 1247 | 0.321 | 2.621 | -1.093 | 0.098 | -1.035 | 0.098 | -0.001 | -0.058 | 0.051 | 0.152 | 0.138 | 0.062 | 0.146 | 0.228 | 15.579 | REJECT |
| E3_stage2_transition | X4_trendline_trail | 3124 | 0.288 | 1.279 | -0.386 | 0.093 | -0.223 | 0.088 | 0.050 | 0.031 | 0.081 | 0.107 | 0.068 | 0.118 | 0.047 | 0.090 | 13.756 | ADOPT |
| E2_exhaustion_confluence | X5_chandelier3atr | 1264 | 0.315 | 2.370 | -0.973 | 0.079 | -1.014 | 0.060 | -0.037 | -0.094 | 0.024 | 0.143 | 0.141 | 0.022 | 0.133 | 0.234 | 15.631 | REJECT |
| E4_anchor_reclaim | X6_partial1R_then_line | 4278 | 0.384 | 0.954 | -0.477 | 0.073 | -0.216 | 0.073 | 0.047 | 0.037 | 0.048 | 0.098 | 0.080 | 0.065 | -0.002 | 0.025 | 19.359 | ADOPT |
| E5_score4 | X6_partial1R_then_line | 6825 | 0.412 | 0.977 | -0.575 | 0.064 | -0.210 | 0.063 | 0.041 | 0.019 | 0.048 | 0.081 | 0.068 | 0.059 | -0.002 | 0.020 | 19.060 | ADOPT |
| E1_trigger_with_trend | X7_stage_drop | 554 | 0.442 | 0.477 | -0.265 | 0.063 | -0.047 | 0.060 | -0.000 | -0.038 | 0.022 | 0.109 | 0.038 | 0.089 | 0.062 | 0.182 | 3.605 | REJECT |
| E1_trigger_with_trend | X4_trendline_trail | 554 | 0.444 | 0.453 | -0.261 | 0.056 | -0.045 | 0.053 | -0.003 | -0.035 | 0.005 | 0.114 | 0.039 | 0.074 | 0.047 | 0.157 | 3.177 | REJECT |
| E3_stage2_transition | X1_time10 | 3004 | 0.508 | 0.716 | -0.645 | 0.046 | 0.012 | 0.046 | 0.014 | -0.006 | 0.044 | 0.049 | 0.037 | 0.056 | 0.028 | 0.072 | 9.115 | REJECT |
| E4_anchor_reclaim | X1_time10 | 3961 | 0.525 | 0.632 | -0.603 | 0.045 | 0.040 | 0.045 | 0.020 | 0.009 | 0.016 | 0.074 | 0.050 | 0.040 | 0.028 | 0.066 | 9.306 | REJECT |
| E3_stage2_transition | X6_partial1R_then_line | 3124 | 0.328 | 0.926 | -0.387 | 0.044 | -0.203 | 0.044 | 0.014 | 0.000 | 0.035 | 0.054 | 0.029 | 0.059 | -0.002 | 0.028 | 13.493 | ADOPT |
| E5_score4 | X1_time10 | 7581 | 0.501 | 0.770 | -0.697 | 0.038 | 0.002 | 0.038 | 0.015 | 0.006 | 0.024 | 0.053 | 0.043 | 0.032 | 0.028 | 0.055 | 8.936 | REJECT |
| E2_exhaustion_confluence | X2_target2R | 1252 | 0.378 | 1.905 | -1.097 | 0.037 | -1.029 | 0.037 | -0.045 | -0.087 | -0.007 | 0.088 | 0.045 | 0.030 | 0.101 | 0.172 | 11.586 | REJECT |
| E1b_trigger_counter_trend | X1_time10 | 2601 | 0.483 | 0.958 | -0.823 | 0.036 | -0.046 | 0.036 | -0.007 | -0.038 | 0.007 | 0.076 | 0.038 | 0.035 | 0.028 | 0.075 | 8.339 | REJECT |
| E1_trigger_with_trend | X6_partial1R_then_line | 554 | 0.446 | 0.401 | -0.261 | 0.034 | -0.044 | 0.034 | -0.013 | -0.039 | -0.006 | 0.079 | -0.000 | 0.070 | -0.002 | 0.077 | 3.175 | REJECT |
| E1b_trigger_counter_trend | X7_stage_drop | 2787 | 0.451 | 0.352 | -0.320 | -0.017 | -0.037 | -0.017 | -0.036 | -0.051 | -0.016 | -0.018 | -0.005 | -0.028 | 0.062 | 0.117 | 2.235 | REJECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 2787 | 0.453 | 0.347 | -0.320 | -0.018 | -0.035 | -0.018 | -0.036 | -0.051 | -0.019 | -0.017 | -0.006 | -0.028 | 0.047 | 0.096 | 2.148 | REJECT |
| E1b_trigger_counter_trend | X6_partial1R_then_line | 2787 | 0.456 | 0.339 | -0.320 | -0.020 | -0.034 | -0.020 | -0.037 | -0.051 | -0.019 | -0.020 | -0.010 | -0.029 | -0.002 | 0.031 | 2.148 | REJECT |
| E2_exhaustion_confluence | X7_stage_drop | 1270 | 0.453 | 0.487 | -0.458 | -0.030 | -0.043 | -0.030 | -0.069 | -0.088 | -0.021 | -0.040 | -0.040 | -0.021 | 0.062 | 0.145 | 2.202 | REJECT |
| E2_exhaustion_confluence | X4_trendline_trail | 1270 | 0.452 | 0.474 | -0.458 | -0.037 | -0.046 | -0.037 | -0.073 | -0.091 | -0.034 | -0.040 | -0.043 | -0.031 | 0.047 | 0.125 | 2.095 | REJECT |
| E2_exhaustion_confluence | X6_partial1R_then_line | 1270 | 0.457 | 0.455 | -0.454 | -0.038 | -0.037 | -0.038 | -0.071 | -0.090 | -0.036 | -0.040 | -0.044 | -0.033 | -0.002 | 0.046 | 2.091 | REJECT |
| E2_exhaustion_confluence | X1_time10 | 1264 | 0.392 | 1.384 | -0.968 | -0.047 | -0.747 | -0.049 | -0.122 | -0.165 | -0.041 | -0.053 | -0.016 | -0.076 | 0.028 | 0.096 | 7.112 | REJECT |

### Exit rules ranked (trade-weighted across setups)

| exit | trades | mean_expectancy | random_mean | edge_over_random |
|---|---|---|---|---|
| X3_target3R | 15,224 | 0.214 | 0.146 | 0.068 |
| X2_target2R | 15,574 | 0.165 | 0.101 | 0.064 |
| X5_chandelier3atr | 17,320 | 0.128 | 0.133 | -0.005 |
| X7_stage_drop | 18,016 | 0.099 | 0.062 | 0.037 |
| X4_trendline_trail | 18,743 | 0.083 | 0.047 | 0.036 |
| X6_partial1R_then_line | 18,838 | 0.042 | -0.002 | 0.044 |
| X1_time10 | 18,937 | 0.038 | 0.028 | 0.010 |

## P1b · Sizing (fixed-fractional, max open positions = 5)

| setup | exit | risk_pct | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 0.005 | 0.021 | -0.100 | 0.209 | 173,428 |
| E1_trigger_with_trend | X3_target3R | 0.010 | 0.040 | -0.191 | 0.208 | 282,603 |
| E1_trigger_with_trend | X3_target3R | 0.020 | 0.071 | -0.349 | 0.205 | 631,438 |
| E1_trigger_with_trend | X5_chandelier3atr | 0.005 | 0.021 | -0.076 | 0.279 | 175,047 |
| E1_trigger_with_trend | X5_chandelier3atr | 0.010 | 0.040 | -0.147 | 0.275 | 288,394 |
| E1_trigger_with_trend | X5_chandelier3atr | 0.020 | 0.074 | -0.275 | 0.268 | 668,005 |
| E4_anchor_reclaim | X3_target3R | 0.005 | 0.029 | -0.095 | 0.308 | 216,848 |
| E4_anchor_reclaim | X3_target3R | 0.010 | 0.057 | -0.186 | 0.305 | 437,625 |
| E4_anchor_reclaim | X3_target3R | 0.020 | 0.106 | -0.350 | 0.301 | 1,463,850 |

## P2 · Market regime (SPY > 200-day average and Trend line rising)

| setup | exit | n_on | exp_on | n_off | exp_off | diff | diff_ci_low | verdict |
|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X4_trendline_trail | 236 | 0.043 | 318 | 0.066 | -0.023 | -0.211 | NO CLEAR EFFECT |
| E1_trigger_with_trend | X5_chandelier3atr | 225 | 0.063 | 299 | 0.452 | -0.388 | -0.834 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 743 | 0.004 | 2044 | -0.026 | 0.030 | -0.028 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 691 | 0.171 | 1898 | 0.132 | 0.038 | -0.189 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X4_trendline_trail | 313 | -0.076 | 957 | -0.024 | -0.052 | -0.159 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 310 | -0.048 | 954 | 0.121 | -0.169 | -0.537 | NO CLEAR EFFECT |
| E3_stage2_transition | X4_trendline_trail | 1868 | 0.088 | 1256 | 0.100 | -0.011 | -0.145 | NO CLEAR EFFECT |
| E3_stage2_transition | X5_chandelier3atr | 1708 | 0.158 | 1147 | 0.111 | 0.047 | -0.098 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X4_trendline_trail | 2602 | 0.126 | 1670 | 0.102 | 0.024 | -0.084 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X5_chandelier3atr | 2215 | 0.137 | 1349 | 0.119 | 0.019 | -0.100 | NO CLEAR EFFECT |
| E5_score4 | X4_trendline_trail | 4444 | 0.142 | 2292 | 0.092 | 0.050 | -0.063 | NO CLEAR EFFECT |
| E5_score4 | X5_chandelier3atr | 4404 | 0.126 | 2120 | 0.082 | 0.043 | -0.066 | NO CLEAR EFFECT |

## P3 · Earnings drift (stocks)

| test | n | mean | mean_vs_spy | hit_vs_spy | ci_low |
|---|---|---|---|---|---|
| Positive earnings gap → hold 20 bars | 749 | 0.017 | 0.010 | 0.531 |  |
| IFI setups ≤20 bars after positive gap (R, X4) | 796 | 0.174 |  |  | 0.088 |
| Same setups at other times (R, X4) | 17947 | 0.079 |  |  | 0.062 |

## P4 · Portfolio heat (E1_trigger_with_trend + X3_target3R)

| rule | cagr | max_dd | mar | final |
|---|---|---|---|---|
| No sector cap | 0.040 | -0.191 | 0.209 | 283,977 |
| Max 1 open per sector | 0.043 | -0.166 | 0.258 | 305,853 |

---
**How to read verdicts.** ADOPT = ≥ min trades, bootstrap CI above 0 after correcting for the number of tests, positive in both time halves and both symbol halves, and better than random entries with the same exits. PROMISING = everything except significance. UNSTABLE = fails a half. REJECT = not positive or not better than random.