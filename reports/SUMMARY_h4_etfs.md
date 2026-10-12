# IFI Lab results: h4 · etfs
_Run 2026-10-12 15:20 UTC · 16 symbols · 2023-11-10 to 2026-10-12 · split 2025-04-26 · 42 setup×exit tests (Bonferroni-adjusted)_

## P1 · Exits × setups (R per trade, after costs)

Random-entry control (same stops and exits), mean expectancy by exit: X1_time10 -0.071R, X2_target2R -0.060R, X3_target3R -0.044R, X4_trendline_trail -0.020R, X5_chandelier3atr -0.053R, X6_partial1R_then_line -0.084R, X7_stage_drop -0.013R

| setup | exit | n | win_rate | avg_win | avg_loss | expectancy | ci_low | ci_low_adj | exp_early | exp_late | exp_symA | exp_symB | random_mean | random_p95 | avg_bars | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E1b_trigger_counter_trend | X3_target3R | 150 | 0.433 | 2.351 | -1.117 | 0.386 | 0.096 | -0.040 | 0.573 | 0.188 | 0.283 | 0.471 | -0.044 | 0.195 | 22.027 | PROMISING (not significant after correction) |
| E1b_trigger_counter_trend | X5_chandelier3atr | 153 | 0.418 | 2.116 | -0.887 | 0.369 | 0.054 | -0.125 | 0.498 | 0.228 | 0.239 | 0.479 | -0.053 | 0.272 | 18.170 | PROMISING (not significant after correction) |
| E1_trigger_with_trend | X3_target3R | 41 | 0.415 | 2.190 | -1.115 | 0.255 | -0.256 | -0.529 | 0.348 | 0.174 | 0.267 | 0.242 | -0.044 | 0.421 | 23.415 | INCONCLUSIVE (too few trades) |
| E4_anchor_reclaim | X3_target3R | 178 | 0.489 | 1.501 | -0.941 | 0.253 | 0.050 | -0.082 | 0.071 | 0.411 | 0.287 | 0.224 | -0.044 | 0.177 | 42.927 | PROMISING (not significant after correction) |
| E4_anchor_reclaim | X2_target2R | 179 | 0.492 | 1.394 | -0.936 | 0.209 | 0.017 | -0.067 | 0.035 | 0.364 | 0.252 | 0.173 | -0.060 | 0.116 | 38.374 | PROMISING (not significant after correction) |
| E1_trigger_with_trend | X2_target2R | 42 | 0.476 | 1.692 | -1.157 | 0.199 | -0.250 | -0.503 | 0.383 | 0.032 | 0.205 | 0.194 | -0.060 | 0.339 | 18.286 | INCONCLUSIVE (too few trades) |
| E2_exhaustion_confluence | X1_time10 | 76 | 0.395 | 2.114 | -1.071 | 0.187 | -0.228 | -0.411 | 0.209 | 0.161 | 0.636 | -0.061 | -0.071 | 0.217 | 6.816 | REJECT |
| E1b_trigger_counter_trend | X1_time10 | 155 | 0.523 | 1.200 | -0.930 | 0.183 | -0.046 | -0.191 | 0.392 | -0.052 | 0.063 | 0.287 | -0.071 | 0.146 | 8.019 | UNSTABLE (fails a split half) |
| E1_trigger_with_trend | X1_time10 | 42 | 0.571 | 1.082 | -1.063 | 0.163 | -0.197 | -0.412 | 0.388 | -0.042 | 0.278 | 0.047 | -0.071 | 0.351 | 8.286 | INCONCLUSIVE (too few trades) |
| E1_trigger_with_trend | X5_chandelier3atr | 42 | 0.500 | 1.305 | -0.998 | 0.153 | -0.260 | -0.427 | 0.344 | -0.021 | 0.135 | 0.171 | -0.053 | 0.581 | 17.071 | INCONCLUSIVE (too few trades) |
| E3_stage2_transition | X3_target3R | 151 | 0.430 | 1.638 | -0.995 | 0.138 | -0.092 | -0.222 | 0.218 | 0.057 | 0.217 | 0.058 | -0.044 | 0.191 | 33.278 | REJECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 76 | 0.329 | 2.513 | -1.044 | 0.126 | -0.359 | -0.623 | 0.242 | -0.002 | 0.518 | -0.090 | -0.053 | 0.408 | 13.237 | REJECT |
| E1b_trigger_counter_trend | X2_target2R | 150 | 0.433 | 1.746 | -1.117 | 0.124 | -0.106 | -0.221 | 0.279 | -0.040 | 0.041 | 0.192 | -0.060 | 0.135 | 17.267 | REJECT |
| E3_stage2_transition | X7_stage_drop | 179 | 0.346 | 1.256 | -0.531 | 0.088 | -0.082 | -0.159 | 0.143 | 0.033 | 0.178 | 0.001 | -0.013 | 0.329 | 19.765 | REJECT |
| E4_anchor_reclaim | X7_stage_drop | 220 | 0.364 | 1.129 | -0.511 | 0.085 | -0.056 | -0.129 | 0.046 | 0.121 | 0.160 | 0.024 | -0.013 | 0.289 | 23.445 | REJECT |
| E1_trigger_with_trend | X6_partial1R_then_line | 45 | 0.600 | 0.391 | -0.374 | 0.085 | -0.063 | -0.168 | 0.125 | 0.047 | 0.116 | 0.053 | -0.084 | 0.202 | 3.778 | INCONCLUSIVE (too few trades) |
| E4_anchor_reclaim | X4_trendline_trail | 233 | 0.378 | 1.012 | -0.478 | 0.085 | -0.047 | -0.128 | 0.006 | 0.156 | 0.185 | 0.002 | -0.020 | 0.276 | 20.412 | REJECT |
| E4_anchor_reclaim | X6_partial1R_then_line | 233 | 0.421 | 0.857 | -0.488 | 0.078 | -0.030 | -0.093 | 0.034 | 0.117 | 0.149 | 0.020 | -0.084 | 0.071 | 20.227 | PROMISING (not significant after correction) |
| E2_exhaustion_confluence | X3_target3R | 76 | 0.329 | 2.618 | -1.172 | 0.075 | -0.343 | -0.534 | 0.025 | 0.130 | 0.165 | 0.025 | -0.044 | 0.279 | 12.539 | REJECT |
| E3_stage2_transition | X2_target2R | 154 | 0.435 | 1.449 | -0.996 | 0.068 | -0.146 | -0.303 | 0.179 | -0.044 | 0.148 | -0.015 | -0.060 | 0.129 | 29.623 | REJECT |
| E3_stage2_transition | X4_trendline_trail | 179 | 0.318 | 1.099 | -0.417 | 0.066 | -0.093 | -0.165 | 0.147 | -0.016 | 0.217 | -0.080 | -0.020 | 0.339 | 15.056 | REJECT |
| E1_trigger_with_trend | X4_trendline_trail | 45 | 0.578 | 0.398 | -0.388 | 0.066 | -0.093 | -0.178 | 0.099 | 0.034 | 0.119 | 0.011 | -0.020 | 0.467 | 3.800 | INCONCLUSIVE (too few trades) |
| E5_score4 | X2_target2R | 313 | 0.441 | 1.465 | -1.042 | 0.064 | -0.093 | -0.230 | -0.024 | 0.133 | 0.154 | -0.026 | -0.060 | 0.086 | 28.252 | REJECT |
| E4_anchor_reclaim | X5_chandelier3atr | 213 | 0.423 | 0.892 | -0.545 | 0.062 | -0.068 | -0.153 | 0.083 | 0.044 | 0.123 | 0.014 | -0.053 | 0.225 | 18.601 | REJECT |
| E1_trigger_with_trend | X7_stage_drop | 45 | 0.578 | 0.391 | -0.388 | 0.062 | -0.098 | -0.182 | 0.099 | 0.026 | 0.119 | 0.003 | -0.013 | 0.507 | 3.822 | INCONCLUSIVE (too few trades) |
| E4_anchor_reclaim | X1_time10 | 221 | 0.575 | 0.549 | -0.648 | 0.040 | -0.057 | -0.127 | -0.008 | 0.083 | 0.024 | 0.053 | -0.071 | 0.113 | 9.190 | REJECT |
| E3_stage2_transition | X6_partial1R_then_line | 179 | 0.341 | 0.889 | -0.420 | 0.026 | -0.089 | -0.148 | 0.095 | -0.044 | 0.109 | -0.055 | -0.084 | 0.096 | 14.966 | REJECT |
| E3_stage2_transition | X5_chandelier3atr | 170 | 0.394 | 1.053 | -0.684 | 0.000 | -0.159 | -0.247 | 0.083 | -0.078 | 0.080 | -0.078 | -0.053 | 0.259 | 18.076 | REJECT |
| E2_exhaustion_confluence | X4_trendline_trail | 76 | 0.434 | 0.656 | -0.513 | -0.005 | -0.193 | -0.292 | 0.012 | -0.024 | -0.081 | 0.037 | -0.020 | 0.494 | 2.500 | REJECT |
| E5_score4 | X6_partial1R_then_line | 382 | 0.424 | 0.826 | -0.628 | -0.011 | -0.099 | -0.149 | 0.019 | -0.033 | 0.055 | -0.069 | -0.084 | 0.034 | 18.513 | REJECT |
| E5_score4 | X4_trendline_trail | 376 | 0.324 | 1.214 | -0.608 | -0.017 | -0.140 | -0.192 | -0.031 | -0.006 | 0.035 | -0.062 | -0.020 | 0.210 | 19.476 | REJECT |
| E5_score4 | X3_target3R | 304 | 0.391 | 1.605 | -1.063 | -0.018 | -0.192 | -0.309 | -0.144 | 0.082 | 0.033 | -0.069 | -0.044 | 0.118 | 31.984 | REJECT |
| E5_score4 | X7_stage_drop | 365 | 0.323 | 1.318 | -0.658 | -0.019 | -0.145 | -0.229 | -0.006 | -0.029 | 0.014 | -0.048 | -0.013 | 0.225 | 21.808 | REJECT |
| E2_exhaustion_confluence | X7_stage_drop | 76 | 0.434 | 0.632 | -0.521 | -0.020 | -0.206 | -0.298 | -0.008 | -0.035 | -0.081 | 0.013 | -0.013 | 0.547 | 2.553 | REJECT |
| E3_stage2_transition | X1_time10 | 172 | 0.523 | 0.579 | -0.690 | -0.026 | -0.148 | -0.204 | 0.008 | -0.059 | 0.021 | -0.072 | -0.071 | 0.134 | 8.953 | REJECT |
| E2_exhaustion_confluence | X6_partial1R_then_line | 76 | 0.434 | 0.554 | -0.513 | -0.049 | -0.205 | -0.292 | -0.040 | -0.060 | -0.085 | -0.030 | -0.084 | 0.146 | 2.500 | REJECT |
| E5_score4 | X1_time10 | 426 | 0.523 | 0.637 | -0.805 | -0.050 | -0.139 | -0.184 | -0.048 | -0.052 | 0.022 | -0.116 | -0.071 | 0.050 | 8.716 | REJECT |
| E2_exhaustion_confluence | X2_target2R | 76 | 0.355 | 1.894 | -1.172 | -0.083 | -0.426 | -0.602 | -0.183 | 0.029 | 0.041 | -0.151 | -0.060 | 0.222 | 9.447 | REJECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 165 | 0.455 | 0.294 | -0.397 | -0.083 | -0.176 | -0.232 | -0.107 | -0.057 | -0.156 | -0.023 | -0.020 | 0.365 | 2.055 | REJECT |
| E1b_trigger_counter_trend | X7_stage_drop | 165 | 0.455 | 0.292 | -0.397 | -0.084 | -0.177 | -0.233 | -0.109 | -0.057 | -0.158 | -0.023 | -0.013 | 0.371 | 2.073 | REJECT |
| E1b_trigger_counter_trend | X6_partial1R_then_line | 165 | 0.455 | 0.283 | -0.397 | -0.088 | -0.177 | -0.238 | -0.104 | -0.070 | -0.149 | -0.037 | -0.084 | 0.118 | 2.055 | REJECT |
| E5_score4 | X5_chandelier3atr | 393 | 0.344 | 1.025 | -0.702 | -0.109 | -0.218 | -0.258 | -0.079 | -0.131 | -0.069 | -0.144 | -0.053 | 0.149 | 16.379 | REJECT |

### Exit rules ranked (trade-weighted across setups)

| exit | trades | mean_expectancy | random_mean | edge_over_random |
|---|---|---|---|---|
| X3_target3R | 900 | 0.149 | -0.044 | 0.193 |
| X2_target2R | 914 | 0.097 | -0.060 | 0.156 |
| X5_chandelier3atr | 1,047 | 0.041 | -0.053 | 0.094 |
| X1_time10 | 1,092 | 0.030 | -0.071 | 0.100 |
| X7_stage_drop | 1,050 | 0.014 | -0.013 | 0.027 |
| X4_trendline_trail | 1,074 | 0.013 | -0.020 | 0.033 |
| X6_partial1R_then_line | 1,080 | 0.004 | -0.084 | 0.088 |

## P1b · Sizing (fixed-fractional, max open positions = 5)

| setup | exit | risk_pct | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|
| E1b_trigger_counter_trend | X3_target3R | 0.005 | 0.067 | -0.119 | 0.562 | 119,249 |
| E1b_trigger_counter_trend | X3_target3R | 0.010 | 0.127 | -0.226 | 0.561 | 138,460 |
| E1b_trigger_counter_trend | X3_target3R | 0.020 | 0.223 | -0.410 | 0.544 | 173,214 |
| E1b_trigger_counter_trend | X5_chandelier3atr | 0.005 | 0.070 | -0.103 | 0.677 | 120,232 |
| E1b_trigger_counter_trend | X5_chandelier3atr | 0.010 | 0.134 | -0.198 | 0.679 | 140,971 |
| E1b_trigger_counter_trend | X5_chandelier3atr | 0.020 | 0.243 | -0.362 | 0.672 | 181,080 |
| E4_anchor_reclaim | X3_target3R | 0.005 | 0.049 | -0.065 | 0.753 | 113,723 |
| E4_anchor_reclaim | X3_target3R | 0.010 | 0.096 | -0.126 | 0.761 | 128,098 |
| E4_anchor_reclaim | X3_target3R | 0.020 | 0.185 | -0.239 | 0.774 | 158,283 |

## P2 · Market regime (SPY > 200-day average and Trend line rising)

| setup | exit | n_on | exp_on | n_off | exp_off | diff | diff_ci_low | verdict |
|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X4_trendline_trail | 19 | 0.106 | 26 | 0.037 | 0.069 | -0.458 | NO CLEAR EFFECT |
| E1_trigger_with_trend | X5_chandelier3atr | 16 | 0.239 | 26 | 0.101 | 0.138 | -1.062 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 40 | -0.197 | 125 | -0.047 | -0.150 | -0.552 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 34 | 0.313 | 119 | 0.385 | -0.072 | -1.093 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X4_trendline_trail | 27 | -0.245 | 49 | 0.127 | -0.371 | -0.902 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 27 | -0.136 | 49 | 0.270 | -0.406 | -1.776 | NO CLEAR EFFECT |
| E3_stage2_transition | X4_trendline_trail | 117 | -0.026 | 62 | 0.239 | -0.265 | -0.994 | NO CLEAR EFFECT |
| E3_stage2_transition | X5_chandelier3atr | 111 | -0.066 | 59 | 0.126 | -0.192 | -0.775 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X4_trendline_trail | 170 | -0.029 | 63 | 0.391 | -0.420 | -0.989 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X5_chandelier3atr | 154 | -0.047 | 59 | 0.347 | -0.395 | -0.879 | NO CLEAR EFFECT |
| E5_score4 | X4_trendline_trail | 283 | -0.146 | 93 | 0.376 | -0.522 | -1.070 | NO CLEAR EFFECT |
| E5_score4 | X5_chandelier3atr | 298 | -0.178 | 95 | 0.107 | -0.285 | -0.707 | NO CLEAR EFFECT |

## P4 · Portfolio heat (E1b_trigger_counter_trend + X3_target3R)

| rule | cagr | max_dd | mar | final |
|---|---|---|---|---|
| No sector cap | 0.108 | -0.226 | 0.479 | 132,347 |
| Max 1 open per sector | 0.108 | -0.226 | 0.479 | 132,347 |

---
**How to read verdicts.** ADOPT = ≥ min trades, bootstrap CI above 0 after correcting for the number of tests, positive in both time halves and both symbol halves, and better than random entries with the same exits. PROMISING = everything except significance. UNSTABLE = fails a half. REJECT = not positive or not better than random.