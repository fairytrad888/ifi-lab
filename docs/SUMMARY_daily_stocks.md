# IFI Lab results: daily · stocks
_Run 2026-11-07 17:38 UTC · 60 symbols · 2000-01-03 to 2026-11-06 · split 2015-01-01 · 42 setup×exit tests (Bonferroni-adjusted) · engine v1.3.3_

> **Survivorship bias:** this stock list was chosen in 2026 from today's large caps, so random long entries earn money too. Judge stock setups by their edge over the random-entry control, not by raw expectancy.

## P1 · Exits × setups (R per trade, after costs)

Random-entry control (same stops and exits), mean expectancy by exit: X1_time10 +0.034R, X2_target2R +0.106R, X3_target3R +0.163R, X4_trendline_trail +0.056R, X5_chandelier3atr +0.136R, X6_partial1R_then_line +0.004R, X7_stage_drop +0.074R

| setup | exit | n | win_rate | avg_win | avg_loss | expectancy | median | exp_w10 | ci_low | ci_low_adj | exp_early | exp_late | exp_symA | exp_symB | random_mean | random_p95 | avg_bars | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 511 | 0.413 | 2.276 | -1.045 | 0.326 | -1.018 | 0.326 | 0.163 | 0.080 | 0.282 | 0.376 | 0.314 | 0.340 | 0.163 | 0.292 | 26.904 | ADOPT |
| E1_trigger_with_trend | X5_chandelier3atr | 513 | 0.435 | 1.669 | -0.777 | 0.287 | -0.259 | 0.271 | 0.146 | 0.056 | 0.213 | 0.367 | 0.214 | 0.366 | 0.136 | 0.286 | 20.086 | ADOPT |
| E4_anchor_reclaim | X3_target3R | 3126 | 0.470 | 1.653 | -0.956 | 0.271 | -0.220 | 0.271 | 0.216 | 0.182 | 0.237 | 0.305 | 0.259 | 0.282 | 0.163 | 0.214 | 38.793 | ADOPT |
| E1_trigger_with_trend | X2_target2R | 512 | 0.453 | 1.803 | -1.050 | 0.243 | -1.012 | 0.243 | 0.119 | 0.049 | 0.230 | 0.256 | 0.241 | 0.245 | 0.106 | 0.215 | 21.602 | ADOPT |
| E4_anchor_reclaim | X2_target2R | 3130 | 0.488 | 1.455 | -0.959 | 0.219 | -0.088 | 0.219 | 0.174 | 0.153 | 0.196 | 0.242 | 0.203 | 0.235 | 0.106 | 0.150 | 34.416 | ADOPT |
| E1b_trigger_counter_trend | X3_target3R | 2470 | 0.390 | 2.176 | -1.049 | 0.208 | -1.016 | 0.208 | 0.140 | 0.097 | 0.141 | 0.296 | 0.184 | 0.235 | 0.163 | 0.223 | 26.101 | REJECT |
| E5_score4 | X3_target3R | 5222 | 0.416 | 1.919 | -1.022 | 0.202 | -1.015 | 0.202 | 0.158 | 0.131 | 0.181 | 0.224 | 0.210 | 0.193 | 0.163 | 0.202 | 32.359 | REJECT |
| E3_stage2_transition | X3_target3R | 2460 | 0.411 | 1.889 | -0.999 | 0.188 | -1.013 | 0.188 | 0.122 | 0.092 | 0.191 | 0.184 | 0.232 | 0.140 | 0.163 | 0.222 | 34.252 | REJECT |
| E1_trigger_with_trend | X1_time10 | 515 | 0.540 | 0.972 | -0.775 | 0.168 | 0.118 | 0.168 | 0.073 | 0.007 | 0.156 | 0.180 | 0.164 | 0.172 | 0.034 | 0.143 | 8.664 | ADOPT |
| E5_score4 | X2_target2R | 5521 | 0.450 | 1.610 | -1.020 | 0.164 | -1.008 | 0.164 | 0.126 | 0.105 | 0.143 | 0.186 | 0.172 | 0.156 | 0.106 | 0.141 | 27.774 | ADOPT |
| E3_stage2_transition | X2_target2R | 2492 | 0.445 | 1.619 | -1.003 | 0.163 | -1.008 | 0.163 | 0.107 | 0.079 | 0.168 | 0.157 | 0.195 | 0.128 | 0.106 | 0.157 | 28.871 | ADOPT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 2555 | 0.381 | 1.731 | -0.824 | 0.149 | -0.440 | 0.146 | 0.086 | 0.042 | 0.043 | 0.292 | 0.133 | 0.167 | 0.136 | 0.207 | 19.564 | REJECT |
| E4_anchor_reclaim | X7_stage_drop | 3849 | 0.365 | 1.366 | -0.552 | 0.148 | -0.256 | 0.145 | 0.107 | 0.086 | 0.125 | 0.171 | 0.135 | 0.161 | 0.074 | 0.119 | 23.522 | ADOPT |
| E5_score4 | X7_stage_drop | 6295 | 0.353 | 1.589 | -0.646 | 0.143 | -0.305 | 0.133 | 0.101 | 0.085 | 0.133 | 0.153 | 0.164 | 0.120 | 0.074 | 0.108 | 22.526 | ADOPT |
| E3_stage2_transition | X5_chandelier3atr | 2807 | 0.392 | 1.387 | -0.666 | 0.139 | -0.285 | 0.133 | 0.089 | 0.058 | 0.133 | 0.145 | 0.184 | 0.091 | 0.136 | 0.200 | 20.652 | REJECT |
| E1b_trigger_counter_trend | X2_target2R | 2476 | 0.425 | 1.735 | -1.050 | 0.134 | -1.012 | 0.134 | 0.076 | 0.045 | 0.069 | 0.220 | 0.107 | 0.165 | 0.106 | 0.158 | 21.125 | REJECT |
| E4_anchor_reclaim | X5_chandelier3atr | 3521 | 0.417 | 1.135 | -0.594 | 0.127 | -0.198 | 0.125 | 0.088 | 0.065 | 0.086 | 0.169 | 0.111 | 0.145 | 0.136 | 0.197 | 21.565 | REJECT |
| E5_score4 | X4_trendline_trail | 6639 | 0.337 | 1.489 | -0.569 | 0.125 | -0.285 | 0.116 | 0.089 | 0.066 | 0.108 | 0.144 | 0.135 | 0.114 | 0.056 | 0.089 | 19.828 | ADOPT |
| E4_anchor_reclaim | X4_trendline_trail | 4214 | 0.335 | 1.281 | -0.475 | 0.113 | -0.253 | 0.111 | 0.079 | 0.055 | 0.085 | 0.141 | 0.106 | 0.120 | 0.056 | 0.099 | 19.689 | ADOPT |
| E5_score4 | X5_chandelier3atr | 6431 | 0.389 | 1.371 | -0.689 | 0.112 | -0.287 | 0.108 | 0.078 | 0.063 | 0.107 | 0.119 | 0.136 | 0.088 | 0.136 | 0.178 | 19.477 | REJECT |
| E3_stage2_transition | X7_stage_drop | 3070 | 0.318 | 1.443 | -0.514 | 0.109 | -0.284 | 0.104 | 0.061 | 0.038 | 0.113 | 0.103 | 0.160 | 0.055 | 0.074 | 0.128 | 18.277 | REJECT |
| E2_exhaustion_confluence | X3_target3R | 1221 | 0.318 | 2.649 | -1.097 | 0.093 | -1.035 | 0.093 | -0.010 | -0.062 | 0.045 | 0.149 | 0.049 | 0.145 | 0.163 | 0.243 | 15.498 | REJECT |
| E3_stage2_transition | X4_trendline_trail | 3075 | 0.286 | 1.284 | -0.386 | 0.091 | -0.224 | 0.086 | 0.047 | 0.021 | 0.082 | 0.102 | 0.121 | 0.059 | 0.056 | 0.105 | 13.714 | REJECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 1235 | 0.311 | 2.453 | -0.975 | 0.091 | -1.014 | 0.071 | -0.028 | -0.102 | 0.023 | 0.168 | 0.040 | 0.150 | 0.136 | 0.233 | 15.650 | REJECT |
| E1_trigger_with_trend | X7_stage_drop | 541 | 0.442 | 0.501 | -0.260 | 0.076 | -0.046 | 0.073 | 0.010 | -0.020 | 0.029 | 0.128 | 0.111 | 0.038 | 0.074 | 0.199 | 3.680 | REJECT |
| E4_anchor_reclaim | X6_partial1R_then_line | 4220 | 0.382 | 0.954 | -0.478 | 0.069 | -0.220 | 0.069 | 0.043 | 0.030 | 0.045 | 0.093 | 0.066 | 0.072 | 0.004 | 0.032 | 19.302 | ADOPT |
| E1_trigger_with_trend | X4_trendline_trail | 541 | 0.444 | 0.477 | -0.256 | 0.069 | -0.044 | 0.066 | 0.007 | -0.024 | 0.011 | 0.133 | 0.095 | 0.041 | 0.056 | 0.177 | 3.242 | REJECT |
| E5_score4 | X6_partial1R_then_line | 6730 | 0.411 | 0.978 | -0.576 | 0.063 | -0.213 | 0.063 | 0.040 | 0.028 | 0.047 | 0.081 | 0.070 | 0.057 | 0.004 | 0.025 | 19.015 | ADOPT |
| E3_stage2_transition | X1_time10 | 2955 | 0.507 | 0.716 | -0.644 | 0.045 | 0.009 | 0.045 | 0.014 | -0.006 | 0.044 | 0.046 | 0.063 | 0.026 | 0.034 | 0.077 | 9.127 | REJECT |
| E1_trigger_with_trend | X6_partial1R_then_line | 541 | 0.445 | 0.416 | -0.257 | 0.043 | -0.043 | 0.043 | -0.006 | -0.027 | -0.000 | 0.090 | 0.078 | 0.005 | 0.004 | 0.083 | 3.240 | REJECT |
| E3_stage2_transition | X6_partial1R_then_line | 3075 | 0.327 | 0.926 | -0.388 | 0.042 | -0.204 | 0.042 | 0.013 | -0.010 | 0.035 | 0.050 | 0.061 | 0.023 | 0.004 | 0.036 | 13.447 | PROMISING (not significant after correction) |
| E4_anchor_reclaim | X1_time10 | 3911 | 0.521 | 0.631 | -0.601 | 0.042 | 0.035 | 0.042 | 0.016 | -0.001 | 0.012 | 0.072 | 0.038 | 0.046 | 0.034 | 0.070 | 9.290 | REJECT |
| E5_score4 | X1_time10 | 7469 | 0.499 | 0.774 | -0.696 | 0.037 | -0.001 | 0.037 | 0.015 | -0.004 | 0.024 | 0.052 | 0.045 | 0.029 | 0.034 | 0.061 | 8.930 | REJECT |
| E2_exhaustion_confluence | X2_target2R | 1225 | 0.376 | 1.919 | -1.099 | 0.034 | -1.029 | 0.034 | -0.049 | -0.091 | -0.009 | 0.083 | 0.018 | 0.054 | 0.106 | 0.176 | 11.505 | REJECT |
| E1b_trigger_counter_trend | X1_time10 | 2567 | 0.480 | 0.958 | -0.822 | 0.033 | -0.057 | 0.033 | -0.012 | -0.045 | 0.004 | 0.072 | 0.028 | 0.038 | 0.034 | 0.079 | 8.338 | REJECT |
| E1b_trigger_counter_trend | X7_stage_drop | 2747 | 0.449 | 0.346 | -0.322 | -0.022 | -0.040 | -0.022 | -0.040 | -0.054 | -0.018 | -0.027 | -0.032 | -0.011 | 0.074 | 0.129 | 2.218 | REJECT |
| E1b_trigger_counter_trend | X6_partial1R_then_line | 2747 | 0.454 | 0.336 | -0.321 | -0.023 | -0.035 | -0.023 | -0.040 | -0.055 | -0.021 | -0.024 | -0.031 | -0.013 | 0.004 | 0.038 | 2.129 | REJECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 2747 | 0.451 | 0.341 | -0.321 | -0.023 | -0.037 | -0.023 | -0.041 | -0.054 | -0.021 | -0.025 | -0.032 | -0.013 | 0.056 | 0.107 | 2.130 | REJECT |
| E2_exhaustion_confluence | X7_stage_drop | 1240 | 0.452 | 0.489 | -0.460 | -0.031 | -0.046 | -0.031 | -0.069 | -0.098 | -0.023 | -0.041 | -0.016 | -0.050 | 0.074 | 0.161 | 2.208 | REJECT |
| E2_exhaustion_confluence | X4_trendline_trail | 1240 | 0.451 | 0.475 | -0.460 | -0.038 | -0.046 | -0.038 | -0.072 | -0.101 | -0.036 | -0.041 | -0.029 | -0.049 | 0.056 | 0.134 | 2.098 | REJECT |
| E2_exhaustion_confluence | X6_partial1R_then_line | 1240 | 0.456 | 0.457 | -0.456 | -0.039 | -0.037 | -0.039 | -0.071 | -0.098 | -0.038 | -0.041 | -0.030 | -0.049 | 0.004 | 0.055 | 2.094 | REJECT |
| E2_exhaustion_confluence | X1_time10 | 1235 | 0.388 | 1.398 | -0.971 | -0.052 | -0.833 | -0.054 | -0.133 | -0.182 | -0.052 | -0.053 | -0.083 | -0.016 | 0.034 | 0.099 | 7.113 | REJECT |

### Exit rules ranked (trade-weighted across setups)

| exit | trades | mean_expectancy | random_mean | edge_over_random |
|---|---|---|---|---|
| X3_target3R | 15,010 | 0.210 | 0.163 | 0.047 |
| X2_target2R | 15,356 | 0.162 | 0.106 | 0.056 |
| X5_chandelier3atr | 17,062 | 0.129 | 0.136 | -0.007 |
| X7_stage_drop | 17,742 | 0.098 | 0.074 | 0.025 |
| X4_trendline_trail | 18,456 | 0.082 | 0.056 | 0.026 |
| X6_partial1R_then_line | 18,553 | 0.041 | 0.004 | 0.037 |
| X1_time10 | 18,652 | 0.037 | 0.034 | 0.003 |

## P1b · Sizing (fixed-fractional, max open positions = 5)

| setup | exit | risk_pct | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 0.005 | 0.021 | -0.100 | 0.208 | 173,191 |
| E1_trigger_with_trend | X3_target3R | 0.010 | 0.040 | -0.191 | 0.207 | 282,155 |
| E1_trigger_with_trend | X3_target3R | 0.020 | 0.071 | -0.349 | 0.204 | 631,618 |
| E1_trigger_with_trend | X5_chandelier3atr | 0.005 | 0.020 | -0.076 | 0.261 | 169,252 |
| E1_trigger_with_trend | X5_chandelier3atr | 0.010 | 0.038 | -0.147 | 0.257 | 270,375 |
| E1_trigger_with_trend | X5_chandelier3atr | 0.020 | 0.069 | -0.275 | 0.250 | 592,968 |
| E4_anchor_reclaim | X3_target3R | 0.005 | 0.033 | -0.099 | 0.331 | 238,003 |
| E4_anchor_reclaim | X3_target3R | 0.010 | 0.064 | -0.190 | 0.336 | 526,001 |
| E4_anchor_reclaim | X3_target3R | 0.020 | 0.120 | -0.348 | 0.346 | 2,101,569 |

## P2 · Market regime (SPY > 200-day average and Trend line rising)

| setup | exit | n_on | exp_on | n_off | exp_off | diff | diff_ci_low | verdict |
|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X4_trendline_trail | 231 | 0.064 | 310 | 0.072 | -0.008 | -0.199 | NO CLEAR EFFECT |
| E1_trigger_with_trend | X5_chandelier3atr | 221 | 0.072 | 292 | 0.449 | -0.376 | -0.821 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 735 | -0.011 | 2012 | -0.027 | 0.016 | -0.037 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 683 | 0.193 | 1872 | 0.133 | 0.060 | -0.167 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X4_trendline_trail | 307 | -0.091 | 933 | -0.021 | -0.071 | -0.185 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 305 | -0.015 | 930 | 0.125 | -0.140 | -0.543 | NO CLEAR EFFECT |
| E3_stage2_transition | X4_trendline_trail | 1837 | 0.087 | 1238 | 0.097 | -0.010 | -0.144 | NO CLEAR EFFECT |
| E3_stage2_transition | X5_chandelier3atr | 1678 | 0.158 | 1129 | 0.110 | 0.048 | -0.096 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X4_trendline_trail | 2557 | 0.124 | 1657 | 0.096 | 0.028 | -0.077 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X5_chandelier3atr | 2181 | 0.137 | 1340 | 0.112 | 0.025 | -0.090 | NO CLEAR EFFECT |
| E5_score4 | X4_trendline_trail | 4373 | 0.142 | 2266 | 0.092 | 0.049 | -0.060 | NO CLEAR EFFECT |
| E5_score4 | X5_chandelier3atr | 4332 | 0.126 | 2099 | 0.085 | 0.041 | -0.065 | NO CLEAR EFFECT |

## P3 · Earnings drift (stocks)

| test | n | mean | mean_vs_spy | hit_vs_spy | ci_low |
|---|---|---|---|---|---|
| Positive earnings gap → hold 20 bars | 729 | 0.016 | 0.010 | 0.528 |  |
| IFI setups ≤20 bars after positive gap (R, X4) | 782 | 0.161 |  |  | 0.071 |
| Same setups at other times (R, X4) | 17674 | 0.079 |  |  | 0.060 |

## P4 · Portfolio heat (E1_trigger_with_trend + X3_target3R)

| rule | cagr | max_dd | mar | final |
|---|---|---|---|---|
| No sector cap | 0.032 | -0.146 | 0.216 | 229,967 |
| Max 1 open per sector | 0.033 | -0.127 | 0.264 | 240,717 |

## P6 · Playbook portfolio (E4_anchor_reclaim + E1_trigger_with_trend, exit X3_target3R, 1 per symbol, 1 per sector, max 5 open)

| risk | trades | trades_per_year | expectancy | win_rate | longest_losing_streak | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|---|---|---|
| 0.50% | 1275 | 47.534 | 0.264 | 0.456 | 14 | 0.042 | -0.080 | 0.529 | 302,435 |
| 0.75% | 1275 | 47.534 | 0.264 | 0.456 | 14 | 0.063 | -0.118 | 0.530 | 510,212 |
| 1.00% | 1275 | 47.534 | 0.264 | 0.456 | 14 | 0.083 | -0.157 | 0.527 | 844,319 |

## E6 · Playbook E4 after a positive earnings gap (stocks)

| group | n | expectancy | ci_low | verdict |
|---|---|---|---|---|
| E4 ≤20 bars after positive gap | 194 | 0.390 |  |  |
| E4 at other times | 2932 | 0.263 |  |  |
| Difference (95% CI low) | 3126 | 0.128 | -0.053 | NO CLEAR EFFECT |

---
**How to read verdicts.** ADOPT = ≥ min trades, bootstrap CI above 0 after correcting for the number of tests, positive in both time halves and both symbol halves, and better than random entries with the same exits. PROMISING = everything except significance. UNSTABLE = fails a half. REJECT = not positive or not better than random.