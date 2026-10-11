# IFI Lab results: daily · etfs
_Run 2026-10-11 20:55 UTC · 17 symbols · 2000-01-03 to 2026-10-09 · split 2015-01-01 · 42 setup×exit tests (Bonferroni-adjusted)_

## P1 · Exits × setups (R per trade, after costs)

Random-entry control (same stops and exits), mean expectancy by exit: X1_time10 -0.004R, X2_target2R +0.076R, X3_target3R +0.108R, X4_trendline_trail -0.033R, X5_chandelier3atr +0.056R, X6_partial1R_then_line -0.054R, X7_stage_drop -0.039R

| setup | exit | n | win_rate | avg_win | avg_loss | expectancy | ci_low | ci_low_adj | exp_early | exp_late | exp_symA | exp_symB | random_mean | random_p95 | avg_bars | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 135 | 0.452 | 2.131 | -1.007 | 0.411 | 0.130 | 0.028 | 0.330 | 0.515 | 0.455 | 0.360 | 0.108 | 0.364 | 28.770 | ADOPT |
| E4_anchor_reclaim | X3_target3R | 885 | 0.508 | 1.559 | -0.954 | 0.324 | 0.228 | 0.169 | 0.213 | 0.446 | 0.295 | 0.364 | 0.108 | 0.216 | 40.838 | ADOPT |
| E1_trigger_with_trend | X2_target2R | 135 | 0.489 | 1.690 | -0.997 | 0.316 | 0.074 | -0.043 | 0.272 | 0.373 | 0.326 | 0.305 | 0.076 | 0.292 | 22.778 | PROMISING (not significant after correction) |
| E1_trigger_with_trend | X1_time10 | 136 | 0.588 | 1.099 | -0.838 | 0.302 | 0.095 | -0.042 | 0.285 | 0.324 | 0.343 | 0.252 | -0.004 | 0.248 | 8.331 | PROMISING (not significant after correction) |
| E4_anchor_reclaim | X2_target2R | 886 | 0.518 | 1.388 | -0.953 | 0.260 | 0.176 | 0.115 | 0.200 | 0.325 | 0.245 | 0.280 | 0.076 | 0.165 | 36.746 | ADOPT |
| E1_trigger_with_trend | X5_chandelier3atr | 135 | 0.481 | 1.292 | -0.780 | 0.218 | 0.016 | -0.106 | 0.190 | 0.254 | 0.247 | 0.184 | 0.056 | 0.378 | 19.793 | REJECT |
| E5_score4 | X3_target3R | 1448 | 0.434 | 1.805 | -0.999 | 0.217 | 0.140 | 0.094 | 0.139 | 0.302 | 0.131 | 0.333 | 0.108 | 0.194 | 34.722 | ADOPT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 702 | 0.383 | 1.785 | -0.766 | 0.211 | 0.088 | 0.017 | 0.095 | 0.374 | 0.285 | 0.120 | 0.056 | 0.207 | 21.548 | ADOPT |
| E5_score4 | X2_target2R | 1537 | 0.464 | 1.572 | -1.002 | 0.192 | 0.123 | 0.082 | 0.129 | 0.261 | 0.157 | 0.239 | 0.076 | 0.141 | 29.602 | ADOPT |
| E4_anchor_reclaim | X7_stage_drop | 1144 | 0.384 | 1.300 | -0.510 | 0.185 | 0.109 | 0.065 | 0.186 | 0.184 | 0.194 | 0.172 | -0.039 | 0.056 | 24.077 | ADOPT |
| E1b_trigger_counter_trend | X3_target3R | 678 | 0.395 | 2.021 | -1.022 | 0.181 | 0.057 | -0.003 | 0.089 | 0.307 | 0.271 | 0.068 | 0.108 | 0.220 | 28.512 | REJECT |
| E4_anchor_reclaim | X5_chandelier3atr | 1021 | 0.450 | 1.087 | -0.577 | 0.171 | 0.102 | 0.060 | 0.129 | 0.217 | 0.170 | 0.173 | 0.056 | 0.192 | 23.752 | REJECT |
| E4_anchor_reclaim | X4_trendline_trail | 1259 | 0.369 | 1.182 | -0.436 | 0.162 | 0.092 | 0.046 | 0.166 | 0.157 | 0.153 | 0.175 | -0.033 | 0.053 | 20.052 | ADOPT |
| E3_stage2_transition | X3_target3R | 656 | 0.424 | 1.724 | -0.997 | 0.156 | 0.040 | -0.036 | 0.129 | 0.185 | 0.098 | 0.231 | 0.108 | 0.229 | 34.599 | REJECT |
| E3_stage2_transition | X2_target2R | 661 | 0.445 | 1.534 | -0.994 | 0.131 | 0.031 | -0.028 | 0.102 | 0.162 | 0.092 | 0.180 | 0.076 | 0.172 | 30.548 | REJECT |
| E4_anchor_reclaim | X6_partial1R_then_line | 1260 | 0.410 | 0.917 | -0.442 | 0.114 | 0.066 | 0.036 | 0.111 | 0.118 | 0.113 | 0.116 | -0.054 | 0.012 | 19.751 | ADOPT |
| E1b_trigger_counter_trend | X2_target2R | 681 | 0.421 | 1.645 | -1.027 | 0.099 | -0.004 | -0.064 | -0.003 | 0.240 | 0.133 | 0.056 | 0.076 | 0.170 | 24.073 | REJECT |
| E5_score4 | X5_chandelier3atr | 1792 | 0.410 | 1.168 | -0.672 | 0.083 | 0.024 | -0.007 | 0.039 | 0.129 | 0.052 | 0.125 | 0.056 | 0.150 | 21.017 | REJECT |
| E1b_trigger_counter_trend | X1_time10 | 705 | 0.506 | 0.867 | -0.756 | 0.066 | -0.014 | -0.057 | -0.029 | 0.200 | 0.136 | -0.020 | -0.004 | 0.114 | 8.329 | REJECT |
| E5_score4 | X7_stage_drop | 1800 | 0.359 | 1.321 | -0.642 | 0.064 | 0.003 | -0.029 | 0.034 | 0.097 | 0.021 | 0.125 | -0.039 | 0.040 | 22.965 | PROMISING (not significant after correction) |
| E4_anchor_reclaim | X1_time10 | 1175 | 0.569 | 0.572 | -0.617 | 0.060 | 0.015 | -0.016 | 0.029 | 0.094 | 0.071 | 0.044 | -0.004 | 0.088 | 9.258 | REJECT |
| E3_stage2_transition | X7_stage_drop | 799 | 0.335 | 1.237 | -0.545 | 0.053 | -0.034 | -0.074 | 0.040 | 0.067 | 0.026 | 0.088 | -0.039 | 0.077 | 18.830 | REJECT |
| E5_score4 | X4_trendline_trail | 1904 | 0.358 | 1.182 | -0.583 | 0.048 | -0.004 | -0.033 | 0.025 | 0.073 | 0.002 | 0.114 | -0.033 | 0.039 | 20.049 | PROMISING (not significant after correction) |
| E5_score4 | X1_time10 | 2125 | 0.533 | 0.677 | -0.697 | 0.035 | -0.005 | -0.025 | -0.010 | 0.083 | 0.001 | 0.082 | -0.004 | 0.064 | 8.904 | REJECT |
| E1_trigger_with_trend | X7_stage_drop | 150 | 0.433 | 0.514 | -0.335 | 0.033 | -0.064 | -0.103 | -0.013 | 0.094 | 0.032 | 0.034 | -0.039 | 0.186 | 4.387 | REJECT |
| E1_trigger_with_trend | X4_trendline_trail | 150 | 0.433 | 0.506 | -0.334 | 0.030 | -0.066 | -0.107 | -0.019 | 0.095 | 0.035 | 0.023 | -0.033 | 0.184 | 4.120 | REJECT |
| E3_stage2_transition | X5_chandelier3atr | 738 | 0.392 | 1.169 | -0.703 | 0.030 | -0.056 | -0.107 | -0.014 | 0.076 | 0.001 | 0.068 | 0.056 | 0.209 | 21.793 | REJECT |
| E5_score4 | X6_partial1R_then_line | 1925 | 0.420 | 0.875 | -0.596 | 0.022 | -0.018 | -0.040 | 0.003 | 0.042 | -0.023 | 0.086 | -0.054 | 0.001 | 19.344 | UNSTABLE (fails a split half) |
| E1_trigger_with_trend | X6_partial1R_then_line | 150 | 0.433 | 0.457 | -0.334 | 0.009 | -0.073 | -0.115 | -0.032 | 0.063 | 0.008 | 0.009 | -0.054 | 0.116 | 4.120 | REJECT |
| E2_exhaustion_confluence | X7_stage_drop | 355 | 0.482 | 0.637 | -0.593 | -0.000 | -0.105 | -0.159 | 0.039 | -0.043 | 0.017 | -0.029 | -0.039 | 0.120 | 2.406 | REJECT |
| E1b_trigger_counter_trend | X6_partial1R_then_line | 759 | 0.497 | 0.329 | -0.327 | -0.001 | -0.033 | -0.051 | -0.033 | 0.045 | -0.012 | 0.013 | -0.054 | 0.022 | 2.289 | REJECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 759 | 0.495 | 0.335 | -0.335 | -0.003 | -0.037 | -0.056 | -0.039 | 0.048 | -0.013 | 0.009 | -0.033 | 0.069 | 2.289 | REJECT |
| E1b_trigger_counter_trend | X7_stage_drop | 759 | 0.494 | 0.335 | -0.336 | -0.004 | -0.038 | -0.057 | -0.039 | 0.045 | -0.015 | 0.008 | -0.039 | 0.073 | 2.331 | REJECT |
| E2_exhaustion_confluence | X4_trendline_trail | 355 | 0.485 | 0.616 | -0.596 | -0.008 | -0.112 | -0.163 | 0.024 | -0.043 | 0.002 | -0.026 | -0.033 | 0.113 | 2.245 | REJECT |
| E3_stage2_transition | X4_trendline_trail | 799 | 0.315 | 0.867 | -0.413 | -0.009 | -0.076 | -0.119 | -0.022 | 0.004 | -0.019 | 0.003 | -0.033 | 0.064 | 13.451 | REJECT |
| E3_stage2_transition | X6_partial1R_then_line | 799 | 0.337 | 0.733 | -0.410 | -0.025 | -0.077 | -0.108 | -0.042 | -0.007 | -0.035 | -0.013 | -0.054 | 0.025 | 13.357 | REJECT |
| E2_exhaustion_confluence | X6_partial1R_then_line | 355 | 0.490 | 0.524 | -0.583 | -0.040 | -0.128 | -0.165 | -0.028 | -0.054 | -0.043 | -0.036 | -0.054 | 0.054 | 2.245 | REJECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 355 | 0.251 | 2.754 | -1.006 | -0.064 | -0.273 | -0.384 | -0.252 | 0.141 | -0.072 | -0.050 | 0.056 | 0.246 | 13.792 | REJECT |
| E3_stage2_transition | X1_time10 | 771 | 0.484 | 0.559 | -0.689 | -0.085 | -0.136 | -0.177 | -0.114 | -0.054 | -0.102 | -0.062 | -0.004 | 0.106 | 8.868 | REJECT |
| E2_exhaustion_confluence | X3_target3R | 351 | 0.268 | 2.646 | -1.111 | -0.105 | -0.291 | -0.416 | -0.264 | 0.064 | -0.136 | -0.055 | 0.108 | 0.275 | 14.026 | REJECT |
| E2_exhaustion_confluence | X2_target2R | 352 | 0.318 | 1.924 | -1.106 | -0.141 | -0.296 | -0.408 | -0.288 | 0.016 | -0.147 | -0.132 | 0.076 | 0.200 | 10.634 | REJECT |
| E2_exhaustion_confluence | X1_time10 | 355 | 0.344 | 1.545 | -1.042 | -0.153 | -0.339 | -0.402 | -0.247 | -0.052 | -0.094 | -0.251 | -0.004 | 0.156 | 6.380 | REJECT |

### Exit rules ranked (trade-weighted across setups)

| exit | trades | mean_expectancy | random_mean | edge_over_random |
|---|---|---|---|---|
| X3_target3R | 4,153 | 0.203 | 0.108 | 0.095 |
| X2_target2R | 4,252 | 0.158 | 0.076 | 0.082 |
| X5_chandelier3atr | 4,743 | 0.105 | 0.056 | 0.050 |
| X7_stage_drop | 5,007 | 0.074 | -0.039 | 0.113 |
| X4_trendline_trail | 5,226 | 0.055 | -0.033 | 0.088 |
| X6_partial1R_then_line | 5,248 | 0.029 | -0.054 | 0.083 |
| X1_time10 | 5,267 | 0.021 | -0.004 | 0.026 |

## P1b · Sizing (fixed-fractional, max open positions = 5)

| setup | exit | risk_pct | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 0.005 | 0.010 | -0.047 | 0.224 | 131,269 |
| E1_trigger_with_trend | X3_target3R | 0.010 | 0.020 | -0.091 | 0.220 | 168,612 |
| E1_trigger_with_trend | X3_target3R | 0.020 | 0.037 | -0.176 | 0.213 | 262,199 |
| E4_anchor_reclaim | X3_target3R | 0.005 | 0.027 | -0.128 | 0.209 | 203,102 |
| E4_anchor_reclaim | X3_target3R | 0.010 | 0.052 | -0.242 | 0.213 | 383,103 |
| E4_anchor_reclaim | X3_target3R | 0.020 | 0.094 | -0.457 | 0.206 | 1,112,997 |
| E1_trigger_with_trend | X2_target2R | 0.005 | 0.008 | -0.033 | 0.230 | 122,026 |
| E1_trigger_with_trend | X2_target2R | 0.010 | 0.015 | -0.066 | 0.225 | 146,761 |
| E1_trigger_with_trend | X2_target2R | 0.020 | 0.028 | -0.128 | 0.214 | 203,779 |

## P2 · Market regime (SPY > 200-day average and Trend line rising)

| setup | exit | n_on | exp_on | n_off | exp_off | diff | diff_ci_low | verdict |
|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X4_trendline_trail | 43 | 0.069 | 107 | 0.014 | 0.054 | -0.234 | NO CLEAR EFFECT |
| E1_trigger_with_trend | X5_chandelier3atr | 38 | -0.063 | 97 | 0.328 | -0.391 | -1.057 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 70 | 0.021 | 689 | -0.006 | 0.027 | -0.114 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 62 | -0.048 | 640 | 0.236 | -0.285 | -0.729 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X4_trendline_trail | 32 | -0.354 | 323 | 0.026 | -0.380 | -0.989 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 32 | -0.479 | 323 | -0.023 | -0.456 | -1.421 | NO CLEAR EFFECT |
| E3_stage2_transition | X4_trendline_trail | 476 | 0.061 | 323 | -0.112 | 0.173 | 0.002 | FILTER HELPS |
| E3_stage2_transition | X5_chandelier3atr | 447 | 0.081 | 291 | -0.048 | 0.129 | -0.118 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X4_trendline_trail | 845 | 0.184 | 414 | 0.116 | 0.068 | -0.130 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X5_chandelier3atr | 692 | 0.206 | 329 | 0.098 | 0.108 | -0.088 | NO CLEAR EFFECT |
| E5_score4 | X4_trendline_trail | 1370 | 0.057 | 534 | 0.025 | 0.032 | -0.135 | NO CLEAR EFFECT |
| E5_score4 | X5_chandelier3atr | 1318 | 0.085 | 474 | 0.077 | 0.008 | -0.169 | NO CLEAR EFFECT |

## P4 · Portfolio heat (E1_trigger_with_trend + X3_target3R)

| rule | cagr | max_dd | mar | final |
|---|---|---|---|---|
| No sector cap | 0.020 | -0.091 | 0.220 | 168,607 |
| Max 1 open per sector | 0.020 | -0.091 | 0.220 | 168,607 |

---
**How to read verdicts.** ADOPT = ≥ min trades, bootstrap CI above 0 after correcting for the number of tests, positive in both time halves and both symbol halves, and better than random entries with the same exits. PROMISING = everything except significance. UNSTABLE = fails a half. REJECT = not positive or not better than random.