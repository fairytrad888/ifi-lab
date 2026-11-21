# IFI Lab results: daily · etfs
_Run 2026-11-21 18:52 UTC · 16 symbols · 2000-01-03 to 2026-11-20 · split 2015-01-01 · 42 setup×exit tests (Bonferroni-adjusted) · engine v1.3.3_

## P1 · Exits × setups (R per trade, after costs)

Random-entry control (same stops and exits), mean expectancy by exit: X1_time10 +0.019R, X2_target2R +0.117R, X3_target3R +0.143R, X4_trendline_trail +0.024R, X5_chandelier3atr +0.092R, X6_partial1R_then_line +0.001R, X7_stage_drop +0.030R

| setup | exit | n | win_rate | avg_win | avg_loss | expectancy | median | exp_w10 | ci_low | ci_low_adj | exp_early | exp_late | exp_symA | exp_symB | random_mean | random_p95 | avg_bars | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 129 | 0.426 | 2.173 | -1.030 | 0.335 | -1.014 | 0.335 | 0.038 | -0.140 | 0.290 | 0.388 | 0.506 | 0.172 | 0.143 | 0.385 | 28.411 | REJECT |
| E4_anchor_reclaim | X3_target3R | 831 | 0.504 | 1.574 | -0.948 | 0.323 | 0.027 | 0.323 | 0.224 | 0.159 | 0.230 | 0.423 | 0.232 | 0.422 | 0.143 | 0.242 | 40.824 | ADOPT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 651 | 0.392 | 1.850 | -0.756 | 0.265 | -0.374 | 0.259 | 0.138 | 0.091 | 0.139 | 0.432 | 0.248 | 0.282 | 0.092 | 0.210 | 21.977 | ADOPT |
| E4_anchor_reclaim | X2_target2R | 832 | 0.516 | 1.403 | -0.948 | 0.264 | 0.138 | 0.264 | 0.183 | 0.132 | 0.216 | 0.316 | 0.203 | 0.330 | 0.117 | 0.197 | 36.749 | ADOPT |
| E1_trigger_with_trend | X2_target2R | 129 | 0.465 | 1.739 | -1.022 | 0.262 | -1.008 | 0.262 | 0.012 | -0.172 | 0.255 | 0.270 | 0.292 | 0.234 | 0.117 | 0.321 | 22.062 | REJECT |
| E1_trigger_with_trend | X1_time10 | 130 | 0.569 | 1.103 | -0.851 | 0.261 | 0.253 | 0.261 | 0.059 | -0.086 | 0.265 | 0.258 | 0.297 | 0.227 | 0.019 | 0.222 | 8.385 | PROMISING (not significant after correction) |
| E1b_trigger_counter_trend | X3_target3R | 630 | 0.402 | 2.078 | -1.016 | 0.227 | -1.009 | 0.227 | 0.102 | 0.027 | 0.134 | 0.349 | 0.219 | 0.235 | 0.143 | 0.256 | 28.859 | REJECT |
| E5_score4 | X3_target3R | 1353 | 0.430 | 1.811 | -0.999 | 0.210 | -1.012 | 0.210 | 0.128 | 0.077 | 0.134 | 0.291 | 0.158 | 0.263 | 0.143 | 0.218 | 34.842 | REJECT |
| E1_trigger_with_trend | X5_chandelier3atr | 129 | 0.473 | 1.339 | -0.809 | 0.207 | -0.045 | 0.207 | -0.014 | -0.143 | 0.207 | 0.207 | 0.303 | 0.116 | 0.092 | 0.362 | 19.814 | REJECT |
| E5_score4 | X2_target2R | 1436 | 0.460 | 1.579 | -1.001 | 0.185 | -1.005 | 0.185 | 0.112 | 0.080 | 0.124 | 0.250 | 0.160 | 0.209 | 0.117 | 0.176 | 29.728 | ADOPT |
| E4_anchor_reclaim | X5_chandelier3atr | 960 | 0.451 | 1.069 | -0.572 | 0.168 | -0.135 | 0.168 | 0.095 | 0.048 | 0.138 | 0.200 | 0.126 | 0.214 | 0.092 | 0.186 | 23.589 | REJECT |
| E4_anchor_reclaim | X7_stage_drop | 1072 | 0.379 | 1.256 | -0.506 | 0.161 | -0.215 | 0.156 | 0.084 | 0.050 | 0.165 | 0.157 | 0.046 | 0.286 | 0.030 | 0.103 | 24.059 | ADOPT |
| E3_stage2_transition | X3_target3R | 618 | 0.421 | 1.736 | -1.004 | 0.149 | -1.011 | 0.149 | 0.025 | -0.068 | 0.105 | 0.196 | 0.125 | 0.173 | 0.143 | 0.258 | 34.586 | REJECT |
| E4_anchor_reclaim | X4_trendline_trail | 1181 | 0.369 | 1.130 | -0.433 | 0.144 | -0.189 | 0.144 | 0.082 | 0.044 | 0.149 | 0.138 | 0.078 | 0.214 | 0.024 | 0.094 | 20.060 | ADOPT |
| E1b_trigger_counter_trend | X2_target2R | 633 | 0.430 | 1.674 | -1.022 | 0.137 | -1.008 | 0.137 | 0.029 | -0.058 | 0.039 | 0.266 | 0.172 | 0.100 | 0.117 | 0.209 | 24.196 | REJECT |
| E3_stage2_transition | X2_target2R | 622 | 0.445 | 1.546 | -1.003 | 0.132 | -1.009 | 0.132 | 0.034 | -0.035 | 0.088 | 0.180 | 0.121 | 0.144 | 0.117 | 0.207 | 30.593 | REJECT |
| E4_anchor_reclaim | X6_partial1R_then_line | 1182 | 0.409 | 0.893 | -0.441 | 0.105 | -0.160 | 0.105 | 0.060 | 0.034 | 0.101 | 0.111 | 0.063 | 0.150 | 0.001 | 0.045 | 19.759 | ADOPT |
| E1b_trigger_counter_trend | X1_time10 | 652 | 0.525 | 0.876 | -0.758 | 0.099 | 0.026 | 0.099 | 0.011 | -0.045 | 0.008 | 0.221 | 0.108 | 0.089 | 0.019 | 0.105 | 8.443 | REJECT |
| E5_score4 | X5_chandelier3atr | 1687 | 0.410 | 1.164 | -0.661 | 0.086 | -0.238 | 0.086 | 0.029 | -0.015 | 0.040 | 0.135 | 0.052 | 0.122 | 0.092 | 0.160 | 20.888 | REJECT |
| E5_score4 | X7_stage_drop | 1692 | 0.357 | 1.323 | -0.632 | 0.066 | -0.307 | 0.062 | 0.005 | -0.027 | 0.034 | 0.100 | 0.023 | 0.110 | 0.030 | 0.087 | 22.892 | REJECT |
| E3_stage2_transition | X7_stage_drop | 756 | 0.337 | 1.266 | -0.546 | 0.065 | -0.298 | 0.055 | -0.026 | -0.067 | 0.045 | 0.087 | 0.094 | 0.037 | 0.030 | 0.112 | 18.939 | REJECT |
| E4_anchor_reclaim | X1_time10 | 1100 | 0.575 | 0.568 | -0.616 | 0.064 | 0.103 | 0.063 | 0.016 | -0.011 | 0.032 | 0.098 | 0.019 | 0.112 | 0.019 | 0.086 | 9.259 | REJECT |
| E5_score4 | X4_trendline_trail | 1786 | 0.356 | 1.184 | -0.574 | 0.051 | -0.283 | 0.051 | -0.002 | -0.031 | 0.025 | 0.078 | 0.024 | 0.079 | 0.024 | 0.080 | 20.015 | REJECT |
| E5_score4 | X1_time10 | 1985 | 0.537 | 0.669 | -0.688 | 0.040 | 0.071 | 0.039 | 0.001 | -0.022 | -0.003 | 0.085 | 0.032 | 0.048 | 0.019 | 0.069 | 8.921 | REJECT |
| E3_stage2_transition | X5_chandelier3atr | 699 | 0.392 | 1.189 | -0.702 | 0.039 | -0.298 | 0.030 | -0.051 | -0.097 | -0.015 | 0.097 | 0.052 | 0.026 | 0.092 | 0.204 | 21.774 | REJECT |
| E1_trigger_with_trend | X4_trendline_trail | 145 | 0.434 | 0.510 | -0.349 | 0.025 | -0.071 | 0.025 | -0.071 | -0.140 | -0.012 | 0.069 | 0.055 | -0.007 | 0.024 | 0.216 | 4.186 | REJECT |
| E1_trigger_with_trend | X7_stage_drop | 145 | 0.434 | 0.508 | -0.350 | 0.023 | -0.072 | 0.023 | -0.072 | -0.143 | -0.014 | 0.067 | 0.055 | -0.011 | 0.030 | 0.235 | 4.207 | REJECT |
| E5_score4 | X6_partial1R_then_line | 1805 | 0.417 | 0.876 | -0.590 | 0.022 | -0.231 | 0.022 | -0.020 | -0.035 | -0.001 | 0.046 | -0.001 | 0.045 | 0.001 | 0.034 | 19.311 | REJECT |
| E1b_trigger_counter_trend | X6_partial1R_then_line | 703 | 0.501 | 0.330 | -0.311 | 0.010 | 0.000 | 0.010 | -0.021 | -0.042 | -0.027 | 0.060 | -0.002 | 0.022 | 0.001 | 0.060 | 2.248 | REJECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 703 | 0.501 | 0.335 | -0.317 | 0.009 | 0.000 | 0.009 | -0.024 | -0.045 | -0.030 | 0.063 | -0.004 | 0.024 | 0.024 | 0.110 | 2.248 | REJECT |
| E1b_trigger_counter_trend | X7_stage_drop | 703 | 0.499 | 0.335 | -0.317 | 0.009 | -0.002 | 0.009 | -0.025 | -0.045 | -0.029 | 0.060 | -0.005 | 0.023 | 0.030 | 0.124 | 2.290 | REJECT |
| E1_trigger_with_trend | X6_partial1R_then_line | 145 | 0.434 | 0.459 | -0.349 | 0.002 | -0.071 | 0.002 | -0.079 | -0.141 | -0.027 | 0.037 | 0.009 | -0.004 | 0.001 | 0.135 | 4.186 | REJECT |
| E3_stage2_transition | X4_trendline_trail | 756 | 0.315 | 0.891 | -0.413 | -0.002 | -0.245 | -0.010 | -0.071 | -0.108 | -0.020 | 0.017 | 0.046 | -0.050 | 0.024 | 0.106 | 13.488 | REJECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 316 | 0.266 | 2.676 | -0.983 | -0.011 | -1.023 | -0.011 | -0.217 | -0.332 | -0.270 | 0.259 | -0.295 | 0.270 | 0.092 | 0.253 | 14.519 | REJECT |
| E3_stage2_transition | X6_partial1R_then_line | 756 | 0.336 | 0.745 | -0.408 | -0.021 | -0.227 | -0.021 | -0.071 | -0.107 | -0.043 | 0.002 | 0.011 | -0.052 | 0.001 | 0.055 | 13.392 | REJECT |
| E2_exhaustion_confluence | X7_stage_drop | 316 | 0.494 | 0.486 | -0.529 | -0.028 | -0.002 | -0.028 | -0.106 | -0.152 | -0.022 | -0.034 | -0.013 | -0.043 | 0.030 | 0.167 | 2.465 | REJECT |
| E2_exhaustion_confluence | X4_trendline_trail | 316 | 0.494 | 0.465 | -0.529 | -0.039 | -0.002 | -0.039 | -0.114 | -0.159 | -0.043 | -0.034 | -0.013 | -0.064 | 0.024 | 0.149 | 2.294 | REJECT |
| E2_exhaustion_confluence | X6_partial1R_then_line | 316 | 0.500 | 0.431 | -0.514 | -0.041 | 0.004 | -0.041 | -0.112 | -0.159 | -0.047 | -0.035 | -0.017 | -0.065 | 0.001 | 0.090 | 2.294 | REJECT |
| E3_stage2_transition | X1_time10 | 730 | 0.488 | 0.562 | -0.693 | -0.081 | -0.029 | -0.081 | -0.137 | -0.172 | -0.121 | -0.038 | -0.057 | -0.106 | 0.019 | 0.100 | 8.856 | REJECT |
| E2_exhaustion_confluence | X3_target3R | 313 | 0.268 | 2.666 | -1.090 | -0.082 | -1.030 | -0.082 | -0.261 | -0.385 | -0.245 | 0.085 | -0.278 | 0.114 | 0.143 | 0.302 | 14.438 | REJECT |
| E2_exhaustion_confluence | X2_target2R | 314 | 0.318 | 1.927 | -1.081 | -0.123 | -1.027 | -0.123 | -0.283 | -0.375 | -0.283 | 0.041 | -0.175 | -0.071 | 0.117 | 0.248 | 10.924 | REJECT |
| E2_exhaustion_confluence | X1_time10 | 316 | 0.358 | 1.339 | -1.012 | -0.171 | -1.020 | -0.171 | -0.319 | -0.387 | -0.365 | 0.031 | -0.320 | -0.024 | 0.019 | 0.151 | 6.538 | REJECT |

### Exit rules ranked (trade-weighted across setups)

| exit | trades | mean_expectancy | random_mean | edge_over_random |
|---|---|---|---|---|
| X3_target3R | 3,874 | 0.208 | 0.143 | 0.065 |
| X2_target2R | 3,966 | 0.164 | 0.117 | 0.047 |
| X5_chandelier3atr | 4,442 | 0.119 | 0.092 | 0.027 |
| X7_stage_drop | 4,684 | 0.071 | 0.030 | 0.041 |
| X4_trendline_trail | 4,887 | 0.053 | 0.024 | 0.028 |
| X6_partial1R_then_line | 4,907 | 0.029 | 0.001 | 0.028 |
| X1_time10 | 4,913 | 0.027 | 0.019 | 0.008 |

## P1b · Sizing (fixed-fractional, max open positions = 5)

| setup | exit | risk_pct | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 0.005 | 0.009 | -0.047 | 0.182 | 124,968 |
| E1_trigger_with_trend | X3_target3R | 0.010 | 0.016 | -0.091 | 0.178 | 152,917 |
| E1_trigger_with_trend | X3_target3R | 0.020 | 0.030 | -0.176 | 0.169 | 216,216 |
| E4_anchor_reclaim | X3_target3R | 0.005 | 0.028 | -0.117 | 0.240 | 210,890 |
| E4_anchor_reclaim | X3_target3R | 0.010 | 0.054 | -0.223 | 0.243 | 411,728 |
| E4_anchor_reclaim | X3_target3R | 0.020 | 0.099 | -0.403 | 0.247 | 1,270,255 |
| E1b_trigger_counter_trend | X5_chandelier3atr | 0.005 | 0.018 | -0.165 | 0.106 | 159,714 |
| E1b_trigger_counter_trend | X5_chandelier3atr | 0.010 | 0.032 | -0.317 | 0.100 | 232,195 |
| E1b_trigger_counter_trend | X5_chandelier3atr | 0.020 | 0.052 | -0.569 | 0.091 | 386,262 |

## P2 · Market regime (SPY > 200-day average and Trend line rising)

| setup | exit | n_on | exp_on | n_off | exp_off | diff | diff_ci_low | verdict |
|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X4_trendline_trail | 43 | 0.028 | 102 | 0.023 | 0.004 | -0.300 | NO CLEAR EFFECT |
| E1_trigger_with_trend | X5_chandelier3atr | 37 | -0.077 | 92 | 0.321 | -0.399 | -1.045 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 70 | 0.017 | 633 | 0.009 | 0.009 | -0.139 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 62 | 0.103 | 589 | 0.282 | -0.179 | -0.696 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X4_trendline_trail | 28 | -0.131 | 288 | -0.030 | -0.101 | -0.391 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 28 | -0.188 | 288 | 0.006 | -0.194 | -1.120 | NO CLEAR EFFECT |
| E3_stage2_transition | X4_trendline_trail | 450 | 0.070 | 306 | -0.107 | 0.177 | -0.021 | NO CLEAR EFFECT |
| E3_stage2_transition | X5_chandelier3atr | 423 | 0.090 | 276 | -0.039 | 0.129 | -0.121 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X4_trendline_trail | 795 | 0.154 | 386 | 0.123 | 0.031 | -0.189 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X5_chandelier3atr | 650 | 0.200 | 310 | 0.100 | 0.100 | -0.102 | NO CLEAR EFFECT |
| E5_score4 | X4_trendline_trail | 1290 | 0.053 | 496 | 0.047 | 0.006 | -0.168 | NO CLEAR EFFECT |
| E5_score4 | X5_chandelier3atr | 1242 | 0.082 | 445 | 0.097 | -0.014 | -0.199 | NO CLEAR EFFECT |

## P4 · Portfolio heat (E1_trigger_with_trend + X3_target3R)

| rule | cagr | max_dd | mar | final |
|---|---|---|---|---|
| No sector cap | 0.012 | -0.069 | 0.180 | 138,588 |
| Max 1 open per sector | 0.012 | -0.069 | 0.180 | 138,588 |

## P6 · Playbook portfolio (E4_anchor_reclaim + E1_trigger_with_trend, exit X3_target3R, 1 per symbol, 1 per sector, max 5 open)

| risk | trades | trades_per_year | expectancy | win_rate | longest_losing_streak | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|---|---|---|
| 0.50% | 885 | 32.947 | 0.350 | 0.499 | 26 | 0.031 | -0.129 | 0.244 | 229,613 |
| 0.75% | 885 | 32.947 | 0.350 | 0.499 | 26 | 0.046 | -0.187 | 0.247 | 337,043 |
| 1.00% | 885 | 32.947 | 0.350 | 0.499 | 26 | 0.061 | -0.243 | 0.250 | 484,879 |

---
**How to read verdicts.** ADOPT = ≥ min trades, bootstrap CI above 0 after correcting for the number of tests, positive in both time halves and both symbol halves, and better than random entries with the same exits. PROMISING = everything except significance. UNSTABLE = fails a half. REJECT = not positive or not better than random.