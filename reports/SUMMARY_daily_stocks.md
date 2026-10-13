# IFI Lab results: daily · stocks
_Run 2026-10-13 17:05 UTC · 61 symbols · 2000-01-03 to 2026-10-13 · split 2015-01-01 · 42 setup×exit tests (Bonferroni-adjusted) · engine v1.3.3_

> **Survivorship bias:** this stock list was chosen in 2026 from today's large caps, so random long entries earn money too. Judge stock setups by their edge over the random-entry control, not by raw expectancy.

## P1 · Exits × setups (R per trade, after costs)

Random-entry control (same stops and exits), mean expectancy by exit: X1_time10 +0.033R, X2_target2R +0.102R, X3_target3R +0.158R, X4_trendline_trail +0.057R, X5_chandelier3atr +0.145R, X6_partial1R_then_line +0.004R, X7_stage_drop +0.075R

| setup | exit | n | win_rate | avg_win | avg_loss | expectancy | median | exp_w10 | ci_low | ci_low_adj | exp_early | exp_late | exp_symA | exp_symB | random_mean | random_p95 | avg_bars | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 522 | 0.412 | 2.274 | -1.039 | 0.326 | -1.018 | 0.326 | 0.182 | 0.114 | 0.278 | 0.379 | 0.354 | 0.297 | 0.158 | 0.282 | 26.822 | ADOPT |
| E1_trigger_with_trend | X5_chandelier3atr | 524 | 0.435 | 1.670 | -0.779 | 0.287 | -0.261 | 0.272 | 0.141 | 0.053 | 0.210 | 0.372 | 0.382 | 0.190 | 0.145 | 0.301 | 20.015 | REJECT |
| E4_anchor_reclaim | X3_target3R | 3158 | 0.474 | 1.656 | -0.959 | 0.281 | -0.192 | 0.281 | 0.229 | 0.206 | 0.244 | 0.320 | 0.314 | 0.248 | 0.158 | 0.209 | 38.999 | ADOPT |
| E1_trigger_with_trend | X2_target2R | 523 | 0.453 | 1.797 | -1.044 | 0.243 | -1.012 | 0.243 | 0.118 | 0.037 | 0.236 | 0.252 | 0.239 | 0.248 | 0.102 | 0.202 | 21.545 | ADOPT |
| E4_anchor_reclaim | X2_target2R | 3162 | 0.491 | 1.454 | -0.962 | 0.226 | -0.048 | 0.226 | 0.181 | 0.143 | 0.201 | 0.251 | 0.249 | 0.202 | 0.102 | 0.144 | 34.598 | ADOPT |
| E1b_trigger_counter_trend | X3_target3R | 2502 | 0.390 | 2.164 | -1.050 | 0.204 | -1.016 | 0.204 | 0.138 | 0.085 | 0.141 | 0.288 | 0.206 | 0.202 | 0.158 | 0.221 | 26.060 | REJECT |
| E5_score4 | X3_target3R | 5292 | 0.418 | 1.913 | -1.026 | 0.203 | -1.015 | 0.203 | 0.159 | 0.143 | 0.184 | 0.224 | 0.211 | 0.196 | 0.158 | 0.200 | 32.443 | ADOPT |
| E3_stage2_transition | X3_target3R | 2504 | 0.413 | 1.891 | -1.001 | 0.195 | -1.013 | 0.195 | 0.133 | 0.109 | 0.198 | 0.191 | 0.165 | 0.224 | 0.158 | 0.218 | 34.204 | REJECT |
| E3_stage2_transition | X2_target2R | 2536 | 0.446 | 1.619 | -1.004 | 0.166 | -1.008 | 0.166 | 0.108 | 0.084 | 0.171 | 0.161 | 0.145 | 0.186 | 0.102 | 0.148 | 28.853 | ADOPT |
| E5_score4 | X2_target2R | 5594 | 0.452 | 1.606 | -1.023 | 0.165 | -1.008 | 0.165 | 0.130 | 0.100 | 0.146 | 0.187 | 0.173 | 0.157 | 0.102 | 0.133 | 27.850 | ADOPT |
| E1_trigger_with_trend | X1_time10 | 526 | 0.540 | 0.960 | -0.774 | 0.162 | 0.129 | 0.162 | 0.072 | 0.024 | 0.150 | 0.176 | 0.170 | 0.155 | 0.033 | 0.123 | 8.644 | ADOPT |
| E4_anchor_reclaim | X7_stage_drop | 3899 | 0.367 | 1.369 | -0.552 | 0.152 | -0.254 | 0.150 | 0.109 | 0.085 | 0.128 | 0.178 | 0.168 | 0.137 | 0.075 | 0.122 | 23.622 | ADOPT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 2589 | 0.382 | 1.714 | -0.825 | 0.144 | -0.441 | 0.140 | 0.076 | 0.039 | 0.046 | 0.277 | 0.158 | 0.130 | 0.145 | 0.217 | 19.524 | REJECT |
| E5_score4 | X7_stage_drop | 6389 | 0.353 | 1.586 | -0.647 | 0.142 | -0.305 | 0.132 | 0.103 | 0.082 | 0.132 | 0.153 | 0.135 | 0.149 | 0.075 | 0.112 | 22.579 | ADOPT |
| E3_stage2_transition | X5_chandelier3atr | 2855 | 0.394 | 1.379 | -0.666 | 0.139 | -0.280 | 0.134 | 0.090 | 0.057 | 0.130 | 0.150 | 0.102 | 0.177 | 0.145 | 0.211 | 20.645 | REJECT |
| E1b_trigger_counter_trend | X2_target2R | 2508 | 0.426 | 1.729 | -1.051 | 0.133 | -1.012 | 0.133 | 0.076 | 0.041 | 0.070 | 0.217 | 0.149 | 0.118 | 0.102 | 0.149 | 21.081 | REJECT |
| E4_anchor_reclaim | X5_chandelier3atr | 3565 | 0.420 | 1.133 | -0.596 | 0.130 | -0.193 | 0.128 | 0.091 | 0.066 | 0.088 | 0.173 | 0.150 | 0.111 | 0.145 | 0.207 | 21.662 | REJECT |
| E5_score4 | X4_trendline_trail | 6737 | 0.338 | 1.484 | -0.570 | 0.125 | -0.285 | 0.116 | 0.090 | 0.067 | 0.107 | 0.143 | 0.128 | 0.121 | 0.057 | 0.091 | 19.867 | ADOPT |
| E4_anchor_reclaim | X4_trendline_trail | 4273 | 0.336 | 1.284 | -0.474 | 0.116 | -0.251 | 0.114 | 0.081 | 0.061 | 0.087 | 0.146 | 0.125 | 0.107 | 0.057 | 0.099 | 19.742 | ADOPT |
| E5_score4 | X5_chandelier3atr | 6525 | 0.390 | 1.365 | -0.690 | 0.111 | -0.287 | 0.107 | 0.075 | 0.062 | 0.104 | 0.119 | 0.097 | 0.126 | 0.145 | 0.188 | 19.520 | REJECT |
| E3_stage2_transition | X7_stage_drop | 3119 | 0.319 | 1.438 | -0.515 | 0.108 | -0.283 | 0.104 | 0.059 | 0.033 | 0.110 | 0.107 | 0.067 | 0.151 | 0.075 | 0.129 | 18.301 | REJECT |
| E2_exhaustion_confluence | X3_target3R | 1247 | 0.320 | 2.627 | -1.092 | 0.098 | -1.035 | 0.098 | -0.001 | -0.058 | 0.051 | 0.151 | 0.137 | 0.061 | 0.158 | 0.245 | 15.584 | REJECT |
| E3_stage2_transition | X4_trendline_trail | 3124 | 0.288 | 1.279 | -0.387 | 0.093 | -0.223 | 0.088 | 0.050 | 0.031 | 0.081 | 0.107 | 0.068 | 0.118 | 0.057 | 0.106 | 13.758 | REJECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 1264 | 0.314 | 2.375 | -0.973 | 0.079 | -1.014 | 0.060 | -0.038 | -0.095 | 0.024 | 0.142 | 0.140 | 0.022 | 0.145 | 0.247 | 15.636 | REJECT |
| E4_anchor_reclaim | X6_partial1R_then_line | 4279 | 0.384 | 0.954 | -0.477 | 0.072 | -0.216 | 0.072 | 0.046 | 0.031 | 0.048 | 0.098 | 0.080 | 0.065 | 0.004 | 0.030 | 19.357 | ADOPT |
| E1_trigger_with_trend | X7_stage_drop | 554 | 0.442 | 0.479 | -0.265 | 0.064 | -0.047 | 0.061 | 0.001 | -0.035 | 0.022 | 0.112 | 0.038 | 0.091 | 0.075 | 0.204 | 3.606 | REJECT |
| E5_score4 | X6_partial1R_then_line | 6826 | 0.412 | 0.976 | -0.575 | 0.063 | -0.211 | 0.063 | 0.040 | 0.027 | 0.048 | 0.081 | 0.068 | 0.059 | 0.004 | 0.026 | 19.060 | ADOPT |
| E1_trigger_with_trend | X4_trendline_trail | 554 | 0.444 | 0.456 | -0.261 | 0.057 | -0.045 | 0.055 | -0.002 | -0.033 | 0.005 | 0.117 | 0.039 | 0.077 | 0.057 | 0.183 | 3.179 | REJECT |
| E3_stage2_transition | X1_time10 | 3004 | 0.508 | 0.716 | -0.646 | 0.046 | 0.012 | 0.046 | 0.013 | -0.006 | 0.044 | 0.048 | 0.037 | 0.056 | 0.033 | 0.075 | 9.117 | REJECT |
| E4_anchor_reclaim | X1_time10 | 3962 | 0.524 | 0.632 | -0.603 | 0.045 | 0.040 | 0.045 | 0.019 | 0.006 | 0.016 | 0.074 | 0.049 | 0.040 | 0.033 | 0.069 | 9.305 | REJECT |
| E3_stage2_transition | X6_partial1R_then_line | 3124 | 0.328 | 0.926 | -0.387 | 0.044 | -0.203 | 0.044 | 0.014 | 0.000 | 0.035 | 0.054 | 0.029 | 0.059 | 0.004 | 0.037 | 13.495 | ADOPT |
| E5_score4 | X1_time10 | 7582 | 0.501 | 0.770 | -0.697 | 0.038 | 0.002 | 0.038 | 0.016 | 0.003 | 0.024 | 0.053 | 0.043 | 0.032 | 0.033 | 0.060 | 8.936 | REJECT |
| E1b_trigger_counter_trend | X1_time10 | 2601 | 0.483 | 0.960 | -0.823 | 0.038 | -0.046 | 0.038 | -0.006 | -0.037 | 0.007 | 0.079 | 0.040 | 0.035 | 0.033 | 0.079 | 8.343 | REJECT |
| E2_exhaustion_confluence | X2_target2R | 1252 | 0.377 | 1.909 | -1.096 | 0.037 | -1.029 | 0.037 | -0.046 | -0.087 | -0.007 | 0.088 | 0.044 | 0.030 | 0.102 | 0.166 | 11.589 | REJECT |
| E1_trigger_with_trend | X6_partial1R_then_line | 554 | 0.446 | 0.402 | -0.261 | 0.035 | -0.044 | 0.035 | -0.012 | -0.039 | -0.006 | 0.080 | -0.000 | 0.071 | 0.004 | 0.077 | 3.177 | REJECT |
| E1b_trigger_counter_trend | X7_stage_drop | 2787 | 0.451 | 0.352 | -0.320 | -0.017 | -0.037 | -0.017 | -0.036 | -0.051 | -0.016 | -0.018 | -0.005 | -0.028 | 0.075 | 0.129 | 2.235 | REJECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 2787 | 0.453 | 0.347 | -0.320 | -0.018 | -0.035 | -0.018 | -0.036 | -0.051 | -0.019 | -0.017 | -0.006 | -0.028 | 0.057 | 0.107 | 2.148 | REJECT |
| E1b_trigger_counter_trend | X6_partial1R_then_line | 2787 | 0.456 | 0.339 | -0.320 | -0.020 | -0.034 | -0.020 | -0.037 | -0.051 | -0.019 | -0.020 | -0.010 | -0.029 | 0.004 | 0.037 | 2.148 | REJECT |
| E2_exhaustion_confluence | X7_stage_drop | 1270 | 0.453 | 0.487 | -0.458 | -0.030 | -0.043 | -0.030 | -0.069 | -0.088 | -0.021 | -0.040 | -0.040 | -0.021 | 0.075 | 0.160 | 2.202 | REJECT |
| E2_exhaustion_confluence | X4_trendline_trail | 1270 | 0.452 | 0.474 | -0.458 | -0.037 | -0.046 | -0.037 | -0.073 | -0.091 | -0.034 | -0.040 | -0.043 | -0.031 | 0.057 | 0.134 | 2.095 | REJECT |
| E2_exhaustion_confluence | X6_partial1R_then_line | 1270 | 0.457 | 0.455 | -0.454 | -0.038 | -0.037 | -0.038 | -0.071 | -0.090 | -0.036 | -0.040 | -0.044 | -0.033 | 0.004 | 0.054 | 2.091 | REJECT |
| E2_exhaustion_confluence | X1_time10 | 1264 | 0.391 | 1.386 | -0.967 | -0.048 | -0.747 | -0.049 | -0.122 | -0.165 | -0.041 | -0.055 | -0.017 | -0.076 | 0.033 | 0.094 | 7.116 | REJECT |

### Exit rules ranked (trade-weighted across setups)

| exit | trades | mean_expectancy | random_mean | edge_over_random |
|---|---|---|---|---|
| X3_target3R | 15,225 | 0.214 | 0.158 | 0.056 |
| X2_target2R | 15,575 | 0.165 | 0.102 | 0.063 |
| X5_chandelier3atr | 17,322 | 0.128 | 0.145 | -0.017 |
| X7_stage_drop | 18,018 | 0.099 | 0.075 | 0.024 |
| X4_trendline_trail | 18,745 | 0.083 | 0.057 | 0.026 |
| X6_partial1R_then_line | 18,840 | 0.042 | 0.004 | 0.038 |
| X1_time10 | 18,939 | 0.038 | 0.033 | 0.005 |

## P1b · Sizing (fixed-fractional, max open positions = 5)

| setup | exit | risk_pct | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 0.005 | 0.021 | -0.100 | 0.210 | 173,997 |
| E1_trigger_with_trend | X3_target3R | 0.010 | 0.040 | -0.191 | 0.210 | 284,434 |
| E1_trigger_with_trend | X3_target3R | 0.020 | 0.072 | -0.349 | 0.206 | 639,406 |
| E1_trigger_with_trend | X5_chandelier3atr | 0.005 | 0.021 | -0.076 | 0.281 | 175,797 |
| E1_trigger_with_trend | X5_chandelier3atr | 0.010 | 0.041 | -0.147 | 0.277 | 290,848 |
| E1_trigger_with_trend | X5_chandelier3atr | 0.020 | 0.074 | -0.275 | 0.270 | 679,201 |
| E4_anchor_reclaim | X3_target3R | 0.005 | 0.029 | -0.095 | 0.308 | 216,802 |
| E4_anchor_reclaim | X3_target3R | 0.010 | 0.057 | -0.186 | 0.305 | 437,456 |
| E4_anchor_reclaim | X3_target3R | 0.020 | 0.105 | -0.350 | 0.301 | 1,462,890 |

## P2 · Market regime (SPY > 200-day average and Trend line rising)

| setup | exit | n_on | exp_on | n_off | exp_off | diff | diff_ci_low | verdict |
|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X4_trendline_trail | 236 | 0.045 | 318 | 0.066 | -0.021 | -0.208 | NO CLEAR EFFECT |
| E1_trigger_with_trend | X5_chandelier3atr | 225 | 0.067 | 299 | 0.452 | -0.385 | -0.830 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 743 | 0.004 | 2044 | -0.026 | 0.030 | -0.028 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 691 | 0.175 | 1898 | 0.132 | 0.043 | -0.183 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X4_trendline_trail | 313 | -0.076 | 957 | -0.024 | -0.052 | -0.159 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 310 | -0.048 | 954 | 0.120 | -0.168 | -0.533 | NO CLEAR EFFECT |
| E3_stage2_transition | X4_trendline_trail | 1868 | 0.088 | 1256 | 0.100 | -0.011 | -0.145 | NO CLEAR EFFECT |
| E3_stage2_transition | X5_chandelier3atr | 1708 | 0.158 | 1147 | 0.111 | 0.047 | -0.097 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X4_trendline_trail | 2603 | 0.126 | 1670 | 0.102 | 0.024 | -0.083 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X5_chandelier3atr | 2216 | 0.137 | 1349 | 0.119 | 0.018 | -0.101 | NO CLEAR EFFECT |
| E5_score4 | X4_trendline_trail | 4445 | 0.142 | 2292 | 0.091 | 0.050 | -0.057 | NO CLEAR EFFECT |
| E5_score4 | X5_chandelier3atr | 4405 | 0.125 | 2120 | 0.082 | 0.043 | -0.061 | NO CLEAR EFFECT |

## P3 · Earnings drift (stocks)

| test | n | mean | mean_vs_spy | hit_vs_spy | ci_low |
|---|---|---|---|---|---|
| Positive earnings gap → hold 20 bars | 749 | 0.017 | 0.010 | 0.531 |  |
| IFI setups ≤20 bars after positive gap (R, X4) | 796 | 0.175 |  |  | 0.088 |
| Same setups at other times (R, X4) | 17949 | 0.079 |  |  | 0.062 |

## P4 · Portfolio heat (E1_trigger_with_trend + X3_target3R)

| rule | cagr | max_dd | mar | final |
|---|---|---|---|---|
| No sector cap | 0.031 | -0.146 | 0.211 | 224,978 |
| Max 1 open per sector | 0.033 | -0.127 | 0.260 | 237,447 |

## P6 · Playbook portfolio (E4_anchor_reclaim + E1_trigger_with_trend, exit X3_target3R, 1 per symbol, 1 per sector, max 5 open)

| risk | trades | trades_per_year | expectancy | win_rate | longest_losing_streak | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|---|---|---|
| 0.50% | 1265 | 47.277 | 0.276 | 0.462 | 14 | 0.041 | -0.082 | 0.499 | 291,510 |
| 0.75% | 1265 | 47.277 | 0.276 | 0.462 | 14 | 0.061 | -0.121 | 0.500 | 484,040 |
| 1.00% | 1265 | 47.277 | 0.276 | 0.462 | 14 | 0.080 | -0.161 | 0.499 | 789,638 |

## E6 · Playbook E4 after a positive earnings gap (stocks)

| group | n | expectancy | ci_low | verdict |
|---|---|---|---|---|
| E4 ≤20 bars after positive gap | 197 | 0.446 |  |  |
| E4 at other times | 2961 | 0.270 |  |  |
| Difference (95% CI low) | 3158 | 0.176 | -0.010 | NO CLEAR EFFECT |

---
**How to read verdicts.** ADOPT = ≥ min trades, bootstrap CI above 0 after correcting for the number of tests, positive in both time halves and both symbol halves, and better than random entries with the same exits. PROMISING = everything except significance. UNSTABLE = fails a half. REJECT = not positive or not better than random.