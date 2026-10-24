# IFI Lab results: daily · stocks
_Run 2026-10-24 15:37 UTC · 61 symbols · 2000-01-03 to 2026-10-23 · split 2015-01-01 · 42 setup×exit tests (Bonferroni-adjusted) · engine v1.3.3_

> **Survivorship bias:** this stock list was chosen in 2026 from today's large caps, so random long entries earn money too. Judge stock setups by their edge over the random-entry control, not by raw expectancy.

## P1 · Exits × setups (R per trade, after costs)

Random-entry control (same stops and exits), mean expectancy by exit: X1_time10 +0.051R, X2_target2R +0.128R, X3_target3R +0.190R, X4_trendline_trail +0.084R, X5_chandelier3atr +0.167R, X6_partial1R_then_line +0.023R, X7_stage_drop +0.099R

| setup | exit | n | win_rate | avg_win | avg_loss | expectancy | median | exp_w10 | ci_low | ci_low_adj | exp_early | exp_late | exp_symA | exp_symB | random_mean | random_p95 | avg_bars | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 522 | 0.410 | 2.301 | -1.040 | 0.330 | -1.018 | 0.330 | 0.185 | 0.116 | 0.278 | 0.388 | 0.364 | 0.296 | 0.190 | 0.312 | 26.864 | ADOPT |
| E1_trigger_with_trend | X5_chandelier3atr | 524 | 0.433 | 1.695 | -0.777 | 0.294 | -0.261 | 0.279 | 0.151 | 0.066 | 0.210 | 0.387 | 0.391 | 0.195 | 0.167 | 0.320 | 20.061 | REJECT |
| E4_anchor_reclaim | X3_target3R | 3164 | 0.474 | 1.656 | -0.959 | 0.280 | -0.198 | 0.280 | 0.228 | 0.192 | 0.244 | 0.317 | 0.312 | 0.247 | 0.190 | 0.244 | 38.974 | ADOPT |
| E1_trigger_with_trend | X2_target2R | 523 | 0.451 | 1.812 | -1.044 | 0.244 | -1.012 | 0.244 | 0.117 | 0.034 | 0.236 | 0.254 | 0.245 | 0.244 | 0.128 | 0.238 | 21.579 | ADOPT |
| E4_anchor_reclaim | X2_target2R | 3168 | 0.491 | 1.455 | -0.962 | 0.225 | -0.050 | 0.225 | 0.180 | 0.147 | 0.201 | 0.250 | 0.249 | 0.201 | 0.128 | 0.172 | 34.575 | ADOPT |
| E1b_trigger_counter_trend | X3_target3R | 2504 | 0.389 | 2.184 | -1.050 | 0.209 | -1.016 | 0.209 | 0.140 | 0.096 | 0.141 | 0.300 | 0.214 | 0.205 | 0.190 | 0.250 | 26.079 | REJECT |
| E5_score4 | X3_target3R | 5299 | 0.418 | 1.914 | -1.025 | 0.204 | -1.015 | 0.204 | 0.160 | 0.136 | 0.184 | 0.224 | 0.211 | 0.196 | 0.190 | 0.230 | 32.441 | REJECT |
| E3_stage2_transition | X3_target3R | 2506 | 0.413 | 1.892 | -1.001 | 0.194 | -1.013 | 0.194 | 0.132 | 0.097 | 0.198 | 0.189 | 0.161 | 0.225 | 0.190 | 0.251 | 34.208 | REJECT |
| E5_score4 | X2_target2R | 5602 | 0.452 | 1.608 | -1.023 | 0.166 | -1.008 | 0.166 | 0.132 | 0.110 | 0.146 | 0.188 | 0.174 | 0.158 | 0.128 | 0.160 | 27.844 | ADOPT |
| E3_stage2_transition | X2_target2R | 2538 | 0.446 | 1.620 | -1.005 | 0.166 | -1.008 | 0.166 | 0.109 | 0.087 | 0.171 | 0.160 | 0.143 | 0.188 | 0.128 | 0.177 | 28.853 | REJECT |
| E1_trigger_with_trend | X1_time10 | 526 | 0.540 | 0.965 | -0.774 | 0.165 | 0.119 | 0.165 | 0.073 | 0.026 | 0.150 | 0.181 | 0.169 | 0.160 | 0.051 | 0.154 | 8.663 | ADOPT |
| E4_anchor_reclaim | X7_stage_drop | 3905 | 0.367 | 1.368 | -0.552 | 0.152 | -0.254 | 0.149 | 0.108 | 0.079 | 0.128 | 0.177 | 0.168 | 0.136 | 0.099 | 0.149 | 23.608 | ADOPT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 2591 | 0.381 | 1.729 | -0.825 | 0.148 | -0.443 | 0.144 | 0.081 | 0.033 | 0.046 | 0.286 | 0.163 | 0.134 | 0.167 | 0.234 | 19.550 | REJECT |
| E5_score4 | X7_stage_drop | 6400 | 0.353 | 1.586 | -0.647 | 0.142 | -0.305 | 0.133 | 0.103 | 0.080 | 0.132 | 0.153 | 0.135 | 0.149 | 0.099 | 0.139 | 22.564 | ADOPT |
| E3_stage2_transition | X5_chandelier3atr | 2857 | 0.393 | 1.381 | -0.666 | 0.139 | -0.280 | 0.133 | 0.088 | 0.062 | 0.130 | 0.150 | 0.101 | 0.178 | 0.167 | 0.231 | 20.648 | REJECT |
| E1b_trigger_counter_trend | X2_target2R | 2510 | 0.425 | 1.738 | -1.051 | 0.136 | -1.012 | 0.136 | 0.081 | 0.054 | 0.070 | 0.224 | 0.152 | 0.121 | 0.128 | 0.177 | 21.086 | REJECT |
| E4_anchor_reclaim | X5_chandelier3atr | 3571 | 0.420 | 1.131 | -0.596 | 0.130 | -0.192 | 0.128 | 0.090 | 0.074 | 0.088 | 0.173 | 0.149 | 0.110 | 0.167 | 0.224 | 21.644 | REJECT |
| E5_score4 | X4_trendline_trail | 6748 | 0.338 | 1.484 | -0.570 | 0.125 | -0.284 | 0.116 | 0.089 | 0.073 | 0.107 | 0.144 | 0.129 | 0.121 | 0.084 | 0.118 | 19.856 | ADOPT |
| E4_anchor_reclaim | X4_trendline_trail | 4279 | 0.336 | 1.282 | -0.474 | 0.116 | -0.251 | 0.114 | 0.080 | 0.058 | 0.087 | 0.146 | 0.126 | 0.107 | 0.084 | 0.130 | 19.734 | REJECT |
| E5_score4 | X5_chandelier3atr | 6536 | 0.390 | 1.365 | -0.690 | 0.112 | -0.286 | 0.107 | 0.076 | 0.058 | 0.104 | 0.119 | 0.097 | 0.127 | 0.167 | 0.211 | 19.507 | REJECT |
| E3_stage2_transition | X7_stage_drop | 3121 | 0.319 | 1.439 | -0.515 | 0.109 | -0.283 | 0.104 | 0.059 | 0.027 | 0.110 | 0.107 | 0.066 | 0.152 | 0.099 | 0.156 | 18.307 | REJECT |
| E2_exhaustion_confluence | X3_target3R | 1247 | 0.319 | 2.650 | -1.093 | 0.102 | -1.035 | 0.102 | 0.003 | -0.056 | 0.051 | 0.160 | 0.139 | 0.067 | 0.190 | 0.273 | 15.605 | REJECT |
| E3_stage2_transition | X4_trendline_trail | 3126 | 0.288 | 1.281 | -0.386 | 0.093 | -0.223 | 0.088 | 0.049 | 0.025 | 0.081 | 0.107 | 0.067 | 0.119 | 0.084 | 0.133 | 13.763 | REJECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 1264 | 0.313 | 2.414 | -0.973 | 0.088 | -1.014 | 0.069 | -0.031 | -0.082 | 0.024 | 0.162 | 0.148 | 0.032 | 0.167 | 0.272 | 15.672 | REJECT |
| E4_anchor_reclaim | X6_partial1R_then_line | 4285 | 0.384 | 0.953 | -0.477 | 0.072 | -0.216 | 0.072 | 0.047 | 0.035 | 0.048 | 0.097 | 0.080 | 0.065 | 0.023 | 0.050 | 19.349 | ADOPT |
| E1_trigger_with_trend | X7_stage_drop | 554 | 0.442 | 0.485 | -0.265 | 0.067 | -0.047 | 0.064 | 0.002 | -0.029 | 0.022 | 0.117 | 0.038 | 0.096 | 0.099 | 0.223 | 3.621 | REJECT |
| E5_score4 | X6_partial1R_then_line | 6838 | 0.412 | 0.976 | -0.575 | 0.064 | -0.210 | 0.063 | 0.040 | 0.028 | 0.048 | 0.081 | 0.068 | 0.060 | 0.023 | 0.043 | 19.047 | ADOPT |
| E1_trigger_with_trend | X4_trendline_trail | 554 | 0.444 | 0.462 | -0.261 | 0.060 | -0.045 | 0.057 | -0.001 | -0.029 | 0.005 | 0.122 | 0.039 | 0.082 | 0.084 | 0.207 | 3.193 | REJECT |
| E3_stage2_transition | X1_time10 | 3006 | 0.508 | 0.718 | -0.646 | 0.047 | 0.012 | 0.047 | 0.013 | -0.007 | 0.044 | 0.049 | 0.036 | 0.057 | 0.051 | 0.090 | 9.120 | REJECT |
| E4_anchor_reclaim | X1_time10 | 3968 | 0.525 | 0.632 | -0.603 | 0.045 | 0.040 | 0.045 | 0.019 | 0.005 | 0.016 | 0.075 | 0.050 | 0.039 | 0.051 | 0.087 | 9.306 | REJECT |
| E3_stage2_transition | X6_partial1R_then_line | 3126 | 0.328 | 0.927 | -0.387 | 0.044 | -0.203 | 0.044 | 0.013 | -0.004 | 0.035 | 0.055 | 0.029 | 0.059 | 0.023 | 0.055 | 13.500 | REJECT |
| E5_score4 | X1_time10 | 7594 | 0.501 | 0.771 | -0.697 | 0.038 | 0.003 | 0.038 | 0.017 | 0.004 | 0.024 | 0.054 | 0.044 | 0.033 | 0.051 | 0.077 | 8.937 | REJECT |
| E2_exhaustion_confluence | X2_target2R | 1252 | 0.376 | 1.919 | -1.097 | 0.038 | -1.029 | 0.038 | -0.044 | -0.086 | -0.007 | 0.089 | 0.045 | 0.030 | 0.128 | 0.196 | 11.601 | REJECT |
| E1b_trigger_counter_trend | X1_time10 | 2603 | 0.482 | 0.962 | -0.823 | 0.037 | -0.052 | 0.037 | -0.007 | -0.033 | 0.007 | 0.077 | 0.038 | 0.035 | 0.051 | 0.095 | 8.352 | REJECT |
| E1_trigger_with_trend | X6_partial1R_then_line | 554 | 0.446 | 0.405 | -0.261 | 0.036 | -0.044 | 0.036 | -0.012 | -0.037 | -0.006 | 0.083 | -0.000 | 0.074 | 0.023 | 0.098 | 3.191 | REJECT |
| E1b_trigger_counter_trend | X7_stage_drop | 2789 | 0.451 | 0.352 | -0.320 | -0.017 | -0.038 | -0.017 | -0.036 | -0.046 | -0.016 | -0.018 | -0.005 | -0.028 | 0.099 | 0.155 | 2.235 | REJECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 2789 | 0.453 | 0.347 | -0.319 | -0.018 | -0.036 | -0.018 | -0.037 | -0.047 | -0.019 | -0.017 | -0.007 | -0.028 | 0.084 | 0.135 | 2.148 | REJECT |
| E1b_trigger_counter_trend | X6_partial1R_then_line | 2789 | 0.455 | 0.339 | -0.319 | -0.020 | -0.034 | -0.020 | -0.038 | -0.048 | -0.019 | -0.021 | -0.010 | -0.029 | 0.023 | 0.055 | 2.148 | REJECT |
| E2_exhaustion_confluence | X7_stage_drop | 1270 | 0.453 | 0.487 | -0.458 | -0.030 | -0.043 | -0.030 | -0.069 | -0.088 | -0.021 | -0.040 | -0.040 | -0.021 | 0.099 | 0.183 | 2.202 | REJECT |
| E2_exhaustion_confluence | X4_trendline_trail | 1270 | 0.452 | 0.474 | -0.458 | -0.037 | -0.046 | -0.037 | -0.073 | -0.091 | -0.034 | -0.040 | -0.043 | -0.031 | 0.084 | 0.161 | 2.095 | REJECT |
| E2_exhaustion_confluence | X6_partial1R_then_line | 1270 | 0.457 | 0.455 | -0.454 | -0.038 | -0.037 | -0.038 | -0.071 | -0.090 | -0.036 | -0.040 | -0.044 | -0.033 | 0.023 | 0.068 | 2.091 | REJECT |
| E2_exhaustion_confluence | X1_time10 | 1264 | 0.390 | 1.397 | -0.968 | -0.046 | -0.769 | -0.047 | -0.120 | -0.161 | -0.041 | -0.050 | -0.013 | -0.076 | 0.051 | 0.112 | 7.131 | REJECT |

### Exit rules ranked (trade-weighted across setups)

| exit | trades | mean_expectancy | random_mean | edge_over_random |
|---|---|---|---|---|
| X3_target3R | 15,242 | 0.215 | 0.190 | 0.025 |
| X2_target2R | 15,593 | 0.165 | 0.128 | 0.037 |
| X5_chandelier3atr | 17,343 | 0.129 | 0.167 | -0.038 |
| X7_stage_drop | 18,039 | 0.099 | 0.099 | 0.000 |
| X4_trendline_trail | 18,766 | 0.084 | 0.084 | -0.001 |
| X6_partial1R_then_line | 18,862 | 0.042 | 0.023 | 0.020 |
| X1_time10 | 18,961 | 0.039 | 0.051 | -0.012 |

## P1b · Sizing (fixed-fractional, max open positions = 5)

| setup | exit | risk_pct | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 0.005 | 0.021 | -0.100 | 0.214 | 175,951 |
| E1_trigger_with_trend | X3_target3R | 0.010 | 0.041 | -0.191 | 0.214 | 290,706 |
| E1_trigger_with_trend | X3_target3R | 0.020 | 0.074 | -0.349 | 0.211 | 666,586 |
| E1_trigger_with_trend | X5_chandelier3atr | 0.005 | 0.022 | -0.076 | 0.290 | 179,056 |
| E1_trigger_with_trend | X5_chandelier3atr | 0.010 | 0.042 | -0.147 | 0.287 | 301,505 |
| E1_trigger_with_trend | X5_chandelier3atr | 0.020 | 0.077 | -0.275 | 0.280 | 727,831 |
| E4_anchor_reclaim | X3_target3R | 0.005 | 0.030 | -0.106 | 0.279 | 218,512 |
| E4_anchor_reclaim | X3_target3R | 0.010 | 0.057 | -0.203 | 0.282 | 442,301 |
| E4_anchor_reclaim | X3_target3R | 0.020 | 0.106 | -0.368 | 0.287 | 1,471,514 |

## P2 · Market regime (SPY > 200-day average and Trend line rising)

| setup | exit | n_on | exp_on | n_off | exp_off | diff | diff_ci_low | verdict |
|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X4_trendline_trail | 236 | 0.052 | 318 | 0.066 | -0.014 | -0.203 | NO CLEAR EFFECT |
| E1_trigger_with_trend | X5_chandelier3atr | 225 | 0.084 | 299 | 0.452 | -0.368 | -0.814 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 744 | 0.004 | 2045 | -0.026 | 0.030 | -0.028 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 692 | 0.190 | 1899 | 0.133 | 0.057 | -0.176 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X4_trendline_trail | 313 | -0.076 | 957 | -0.024 | -0.052 | -0.159 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 310 | -0.018 | 954 | 0.122 | -0.140 | -0.504 | NO CLEAR EFFECT |
| E3_stage2_transition | X4_trendline_trail | 1868 | 0.089 | 1258 | 0.100 | -0.011 | -0.140 | NO CLEAR EFFECT |
| E3_stage2_transition | X5_chandelier3atr | 1708 | 0.158 | 1149 | 0.112 | 0.046 | -0.101 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X4_trendline_trail | 2606 | 0.126 | 1673 | 0.102 | 0.024 | -0.091 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X5_chandelier3atr | 2219 | 0.136 | 1352 | 0.119 | 0.017 | -0.096 | NO CLEAR EFFECT |
| E5_score4 | X4_trendline_trail | 4449 | 0.142 | 2299 | 0.092 | 0.051 | -0.062 | NO CLEAR EFFECT |
| E5_score4 | X5_chandelier3atr | 4409 | 0.126 | 2127 | 0.082 | 0.043 | -0.061 | NO CLEAR EFFECT |

## P3 · Earnings drift (stocks)

| test | n | mean | mean_vs_spy | hit_vs_spy | ci_low |
|---|---|---|---|---|---|
| Positive earnings gap → hold 20 bars | 753 | 0.016 | 0.010 | 0.531 |  |
| IFI setups ≤20 bars after positive gap (R, X4) | 801 | 0.167 |  |  | 0.082 |
| Same setups at other times (R, X4) | 17965 | 0.080 |  |  | 0.062 |

## P4 · Portfolio heat (E1_trigger_with_trend + X3_target3R)

| rule | cagr | max_dd | mar | final |
|---|---|---|---|---|
| No sector cap | 0.031 | -0.146 | 0.215 | 228,733 |
| Max 1 open per sector | 0.034 | -0.127 | 0.265 | 241,411 |

## P6 · Playbook portfolio (E4_anchor_reclaim + E1_trigger_with_trend, exit X3_target3R, 1 per symbol, 1 per sector, max 5 open)

| risk | trades | trades_per_year | expectancy | win_rate | longest_losing_streak | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|---|---|---|
| 0.50% | 1264 | 47.192 | 0.280 | 0.463 | 14 | 0.040 | -0.086 | 0.472 | 289,298 |
| 0.75% | 1264 | 47.192 | 0.280 | 0.463 | 14 | 0.060 | -0.126 | 0.477 | 478,116 |
| 1.00% | 1264 | 47.192 | 0.280 | 0.463 | 14 | 0.079 | -0.165 | 0.482 | 775,877 |

## E6 · Playbook E4 after a positive earnings gap (stocks)

| group | n | expectancy | ci_low | verdict |
|---|---|---|---|---|
| E4 ≤20 bars after positive gap | 197 | 0.450 |  |  |
| E4 at other times | 2967 | 0.269 |  |  |
| Difference (95% CI low) | 3164 | 0.181 | 0.009 | EARNINGS CONTEXT HELPS |

---
**How to read verdicts.** ADOPT = ≥ min trades, bootstrap CI above 0 after correcting for the number of tests, positive in both time halves and both symbol halves, and better than random entries with the same exits. PROMISING = everything except significance. UNSTABLE = fails a half. REJECT = not positive or not better than random.