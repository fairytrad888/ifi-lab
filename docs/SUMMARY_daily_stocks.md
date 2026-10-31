# IFI Lab results: daily · stocks
_Run 2026-10-31 17:01 UTC · 61 symbols · 2000-01-03 to 2026-10-30 · split 2015-01-01 · 42 setup×exit tests (Bonferroni-adjusted) · engine v1.3.3_

> **Survivorship bias:** this stock list was chosen in 2026 from today's large caps, so random long entries earn money too. Judge stock setups by their edge over the random-entry control, not by raw expectancy.

## P1 · Exits × setups (R per trade, after costs)

Random-entry control (same stops and exits), mean expectancy by exit: X1_time10 +0.053R, X2_target2R +0.117R, X3_target3R +0.174R, X4_trendline_trail +0.080R, X5_chandelier3atr +0.180R, X6_partial1R_then_line +0.024R, X7_stage_drop +0.095R

| setup | exit | n | win_rate | avg_win | avg_loss | expectancy | median | exp_w10 | ci_low | ci_low_adj | exp_early | exp_late | exp_symA | exp_symB | random_mean | random_p95 | avg_bars | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 522 | 0.412 | 2.292 | -1.042 | 0.331 | -1.018 | 0.331 | 0.185 | 0.116 | 0.278 | 0.391 | 0.366 | 0.296 | 0.174 | 0.301 | 26.874 | ADOPT |
| E1_trigger_with_trend | X5_chandelier3atr | 524 | 0.435 | 1.681 | -0.779 | 0.291 | -0.261 | 0.276 | 0.147 | 0.061 | 0.210 | 0.382 | 0.390 | 0.191 | 0.180 | 0.349 | 20.084 | REJECT |
| E4_anchor_reclaim | X3_target3R | 3167 | 0.474 | 1.654 | -0.959 | 0.279 | -0.196 | 0.279 | 0.228 | 0.206 | 0.244 | 0.316 | 0.311 | 0.247 | 0.174 | 0.228 | 38.967 | ADOPT |
| E1_trigger_with_trend | X2_target2R | 523 | 0.453 | 1.805 | -1.047 | 0.245 | -1.012 | 0.245 | 0.118 | 0.037 | 0.236 | 0.256 | 0.247 | 0.244 | 0.117 | 0.225 | 21.589 | ADOPT |
| E4_anchor_reclaim | X2_target2R | 3171 | 0.491 | 1.454 | -0.962 | 0.225 | -0.050 | 0.225 | 0.179 | 0.149 | 0.201 | 0.250 | 0.249 | 0.201 | 0.117 | 0.164 | 34.568 | ADOPT |
| E1b_trigger_counter_trend | X3_target3R | 2508 | 0.390 | 2.180 | -1.049 | 0.209 | -1.016 | 0.209 | 0.139 | 0.097 | 0.141 | 0.299 | 0.215 | 0.203 | 0.174 | 0.232 | 26.052 | REJECT |
| E5_score4 | X3_target3R | 5304 | 0.418 | 1.915 | -1.024 | 0.204 | -1.015 | 0.204 | 0.159 | 0.133 | 0.184 | 0.225 | 0.210 | 0.197 | 0.174 | 0.213 | 32.435 | REJECT |
| E3_stage2_transition | X3_target3R | 2506 | 0.413 | 1.893 | -1.002 | 0.194 | -1.013 | 0.194 | 0.132 | 0.097 | 0.198 | 0.190 | 0.160 | 0.227 | 0.174 | 0.233 | 34.221 | REJECT |
| E5_score4 | X2_target2R | 5607 | 0.452 | 1.610 | -1.022 | 0.167 | -1.008 | 0.167 | 0.130 | 0.114 | 0.146 | 0.189 | 0.174 | 0.159 | 0.117 | 0.152 | 27.839 | ADOPT |
| E3_stage2_transition | X2_target2R | 2538 | 0.446 | 1.620 | -1.005 | 0.166 | -1.008 | 0.166 | 0.109 | 0.087 | 0.171 | 0.161 | 0.143 | 0.189 | 0.117 | 0.167 | 28.860 | REJECT |
| E1_trigger_with_trend | X1_time10 | 526 | 0.540 | 0.965 | -0.774 | 0.165 | 0.119 | 0.165 | 0.073 | 0.026 | 0.150 | 0.181 | 0.169 | 0.160 | 0.053 | 0.164 | 8.663 | ADOPT |
| E4_anchor_reclaim | X7_stage_drop | 3908 | 0.367 | 1.366 | -0.552 | 0.152 | -0.254 | 0.150 | 0.111 | 0.088 | 0.128 | 0.177 | 0.167 | 0.136 | 0.095 | 0.144 | 23.604 | ADOPT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 2595 | 0.381 | 1.731 | -0.825 | 0.149 | -0.442 | 0.146 | 0.082 | 0.056 | 0.046 | 0.289 | 0.165 | 0.134 | 0.180 | 0.250 | 19.546 | REJECT |
| E5_score4 | X7_stage_drop | 6406 | 0.353 | 1.586 | -0.647 | 0.142 | -0.305 | 0.133 | 0.103 | 0.085 | 0.132 | 0.154 | 0.135 | 0.150 | 0.095 | 0.133 | 22.560 | ADOPT |
| E3_stage2_transition | X5_chandelier3atr | 2857 | 0.393 | 1.383 | -0.666 | 0.140 | -0.281 | 0.134 | 0.089 | 0.062 | 0.130 | 0.151 | 0.100 | 0.180 | 0.180 | 0.248 | 20.656 | REJECT |
| E1b_trigger_counter_trend | X2_target2R | 2514 | 0.426 | 1.735 | -1.051 | 0.135 | -1.012 | 0.135 | 0.081 | 0.051 | 0.070 | 0.222 | 0.152 | 0.119 | 0.117 | 0.166 | 21.065 | REJECT |
| E4_anchor_reclaim | X5_chandelier3atr | 3574 | 0.421 | 1.131 | -0.596 | 0.130 | -0.192 | 0.128 | 0.090 | 0.065 | 0.088 | 0.173 | 0.149 | 0.111 | 0.180 | 0.243 | 21.639 | REJECT |
| E5_score4 | X4_trendline_trail | 6754 | 0.338 | 1.484 | -0.570 | 0.125 | -0.284 | 0.117 | 0.089 | 0.071 | 0.107 | 0.145 | 0.128 | 0.122 | 0.080 | 0.114 | 19.854 | ADOPT |
| E4_anchor_reclaim | X4_trendline_trail | 4282 | 0.337 | 1.281 | -0.474 | 0.116 | -0.250 | 0.114 | 0.079 | 0.058 | 0.087 | 0.146 | 0.125 | 0.107 | 0.080 | 0.127 | 19.733 | REJECT |
| E5_score4 | X5_chandelier3atr | 6542 | 0.390 | 1.366 | -0.689 | 0.112 | -0.286 | 0.108 | 0.078 | 0.060 | 0.104 | 0.120 | 0.097 | 0.128 | 0.180 | 0.228 | 19.504 | REJECT |
| E3_stage2_transition | X7_stage_drop | 3121 | 0.319 | 1.440 | -0.515 | 0.109 | -0.283 | 0.105 | 0.059 | 0.027 | 0.110 | 0.109 | 0.066 | 0.154 | 0.095 | 0.151 | 18.315 | REJECT |
| E2_exhaustion_confluence | X3_target3R | 1248 | 0.319 | 2.650 | -1.096 | 0.099 | -1.035 | 0.099 | 0.003 | -0.059 | 0.051 | 0.154 | 0.133 | 0.067 | 0.174 | 0.260 | 15.594 | REJECT |
| E3_stage2_transition | X4_trendline_trail | 3126 | 0.288 | 1.284 | -0.386 | 0.094 | -0.223 | 0.089 | 0.049 | 0.026 | 0.081 | 0.109 | 0.067 | 0.121 | 0.080 | 0.131 | 13.769 | REJECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 1265 | 0.313 | 2.417 | -0.976 | 0.086 | -1.014 | 0.067 | -0.024 | -0.077 | 0.024 | 0.158 | 0.142 | 0.035 | 0.180 | 0.284 | 15.679 | REJECT |
| E4_anchor_reclaim | X6_partial1R_then_line | 4288 | 0.384 | 0.953 | -0.477 | 0.073 | -0.216 | 0.073 | 0.047 | 0.028 | 0.048 | 0.098 | 0.080 | 0.065 | 0.024 | 0.051 | 19.347 | ADOPT |
| E1_trigger_with_trend | X7_stage_drop | 554 | 0.442 | 0.488 | -0.265 | 0.068 | -0.047 | 0.065 | 0.003 | -0.028 | 0.022 | 0.120 | 0.038 | 0.099 | 0.095 | 0.232 | 3.630 | REJECT |
| E5_score4 | X6_partial1R_then_line | 6844 | 0.412 | 0.976 | -0.575 | 0.064 | -0.210 | 0.064 | 0.041 | 0.030 | 0.048 | 0.082 | 0.067 | 0.061 | 0.024 | 0.046 | 19.045 | ADOPT |
| E1_trigger_with_trend | X4_trendline_trail | 554 | 0.444 | 0.465 | -0.261 | 0.061 | -0.045 | 0.059 | -0.001 | -0.027 | 0.005 | 0.125 | 0.039 | 0.085 | 0.080 | 0.201 | 3.202 | REJECT |
| E3_stage2_transition | X1_time10 | 3006 | 0.508 | 0.718 | -0.646 | 0.047 | 0.012 | 0.047 | 0.013 | -0.007 | 0.044 | 0.050 | 0.036 | 0.058 | 0.053 | 0.098 | 9.124 | REJECT |
| E4_anchor_reclaim | X1_time10 | 3971 | 0.525 | 0.632 | -0.602 | 0.045 | 0.040 | 0.045 | 0.018 | 0.005 | 0.016 | 0.075 | 0.050 | 0.040 | 0.053 | 0.090 | 9.307 | REJECT |
| E3_stage2_transition | X6_partial1R_then_line | 3126 | 0.329 | 0.928 | -0.387 | 0.045 | -0.203 | 0.045 | 0.014 | -0.003 | 0.035 | 0.056 | 0.029 | 0.061 | 0.024 | 0.058 | 13.505 | REJECT |
| E5_score4 | X1_time10 | 7600 | 0.501 | 0.771 | -0.696 | 0.038 | 0.002 | 0.038 | 0.017 | 0.002 | 0.024 | 0.054 | 0.043 | 0.033 | 0.053 | 0.081 | 8.938 | REJECT |
| E1_trigger_with_trend | X6_partial1R_then_line | 554 | 0.446 | 0.407 | -0.261 | 0.037 | -0.044 | 0.037 | -0.011 | -0.037 | -0.006 | 0.085 | -0.000 | 0.075 | 0.024 | 0.101 | 3.200 | REJECT |
| E1b_trigger_counter_trend | X1_time10 | 2607 | 0.482 | 0.960 | -0.823 | 0.036 | -0.052 | 0.036 | -0.006 | -0.036 | 0.007 | 0.076 | 0.038 | 0.034 | 0.053 | 0.100 | 8.346 | REJECT |
| E2_exhaustion_confluence | X2_target2R | 1253 | 0.376 | 1.919 | -1.100 | 0.035 | -1.029 | 0.035 | -0.049 | -0.088 | -0.007 | 0.084 | 0.040 | 0.030 | 0.117 | 0.186 | 11.594 | REJECT |
| E1b_trigger_counter_trend | X7_stage_drop | 2793 | 0.451 | 0.352 | -0.319 | -0.017 | -0.038 | -0.017 | -0.035 | -0.047 | -0.016 | -0.018 | -0.005 | -0.028 | 0.095 | 0.152 | 2.235 | REJECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 2793 | 0.453 | 0.347 | -0.319 | -0.018 | -0.036 | -0.018 | -0.036 | -0.049 | -0.019 | -0.017 | -0.006 | -0.029 | 0.080 | 0.133 | 2.148 | REJECT |
| E1b_trigger_counter_trend | X6_partial1R_then_line | 2793 | 0.455 | 0.339 | -0.319 | -0.020 | -0.034 | -0.020 | -0.037 | -0.048 | -0.019 | -0.020 | -0.010 | -0.029 | 0.024 | 0.063 | 2.148 | REJECT |
| E2_exhaustion_confluence | X7_stage_drop | 1271 | 0.452 | 0.487 | -0.462 | -0.033 | -0.046 | -0.033 | -0.072 | -0.092 | -0.021 | -0.046 | -0.045 | -0.021 | 0.095 | 0.190 | 2.202 | REJECT |
| E2_exhaustion_confluence | X4_trendline_trail | 1271 | 0.452 | 0.474 | -0.462 | -0.039 | -0.046 | -0.039 | -0.076 | -0.100 | -0.034 | -0.045 | -0.048 | -0.031 | 0.080 | 0.163 | 2.095 | REJECT |
| E2_exhaustion_confluence | X6_partial1R_then_line | 1271 | 0.457 | 0.455 | -0.458 | -0.041 | -0.038 | -0.041 | -0.074 | -0.095 | -0.036 | -0.046 | -0.049 | -0.033 | 0.024 | 0.075 | 2.090 | REJECT |
| E2_exhaustion_confluence | X1_time10 | 1265 | 0.390 | 1.397 | -0.971 | -0.048 | -0.783 | -0.050 | -0.125 | -0.172 | -0.041 | -0.056 | -0.019 | -0.076 | 0.053 | 0.120 | 7.126 | REJECT |

### Exit rules ranked (trade-weighted across setups)

| exit | trades | mean_expectancy | random_mean | edge_over_random |
|---|---|---|---|---|
| X3_target3R | 15,255 | 0.214 | 0.174 | 0.040 |
| X2_target2R | 15,606 | 0.165 | 0.117 | 0.048 |
| X5_chandelier3atr | 17,357 | 0.129 | 0.180 | -0.050 |
| X7_stage_drop | 18,053 | 0.099 | 0.095 | 0.005 |
| X4_trendline_trail | 18,780 | 0.084 | 0.080 | 0.004 |
| X6_partial1R_then_line | 18,876 | 0.043 | 0.024 | 0.019 |
| X1_time10 | 18,975 | 0.039 | 0.053 | -0.015 |

## P1b · Sizing (fixed-fractional, max open positions = 5)

| setup | exit | risk_pct | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 0.005 | 0.021 | -0.100 | 0.215 | 176,422 |
| E1_trigger_with_trend | X3_target3R | 0.010 | 0.041 | -0.191 | 0.215 | 292,226 |
| E1_trigger_with_trend | X3_target3R | 0.020 | 0.074 | -0.349 | 0.212 | 673,265 |
| E1_trigger_with_trend | X5_chandelier3atr | 0.005 | 0.022 | -0.076 | 0.286 | 177,943 |
| E1_trigger_with_trend | X5_chandelier3atr | 0.010 | 0.042 | -0.147 | 0.283 | 297,864 |
| E1_trigger_with_trend | X5_chandelier3atr | 0.020 | 0.076 | -0.275 | 0.277 | 711,215 |
| E4_anchor_reclaim | X3_target3R | 0.005 | 0.034 | -0.099 | 0.345 | 246,800 |
| E4_anchor_reclaim | X3_target3R | 0.010 | 0.067 | -0.191 | 0.349 | 562,806 |
| E4_anchor_reclaim | X3_target3R | 0.020 | 0.125 | -0.352 | 0.355 | 2,360,677 |

## P2 · Market regime (SPY > 200-day average and Trend line rising)

| setup | exit | n_on | exp_on | n_off | exp_off | diff | diff_ci_low | verdict |
|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X4_trendline_trail | 236 | 0.055 | 318 | 0.066 | -0.011 | -0.201 | NO CLEAR EFFECT |
| E1_trigger_with_trend | X5_chandelier3atr | 225 | 0.078 | 299 | 0.452 | -0.374 | -0.813 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 747 | 0.004 | 2046 | -0.026 | 0.030 | -0.028 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 695 | 0.196 | 1900 | 0.132 | 0.063 | -0.137 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X4_trendline_trail | 314 | -0.086 | 957 | -0.024 | -0.062 | -0.174 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 311 | -0.023 | 954 | 0.122 | -0.144 | -0.530 | NO CLEAR EFFECT |
| E3_stage2_transition | X4_trendline_trail | 1868 | 0.090 | 1258 | 0.100 | -0.010 | -0.140 | NO CLEAR EFFECT |
| E3_stage2_transition | X5_chandelier3atr | 1708 | 0.159 | 1149 | 0.112 | 0.047 | -0.100 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X4_trendline_trail | 2607 | 0.126 | 1675 | 0.102 | 0.023 | -0.087 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X5_chandelier3atr | 2220 | 0.137 | 1354 | 0.120 | 0.017 | -0.095 | NO CLEAR EFFECT |
| E5_score4 | X4_trendline_trail | 4452 | 0.143 | 2302 | 0.092 | 0.050 | -0.051 | NO CLEAR EFFECT |
| E5_score4 | X5_chandelier3atr | 4412 | 0.126 | 2130 | 0.083 | 0.043 | -0.062 | NO CLEAR EFFECT |

## P3 · Earnings drift (stocks)

| test | n | mean | mean_vs_spy | hit_vs_spy | ci_low |
|---|---|---|---|---|---|
| Positive earnings gap → hold 20 bars | 753 | 0.016 | 0.010 | 0.531 |  |
| IFI setups ≤20 bars after positive gap (R, X4) | 801 | 0.167 |  |  | 0.082 |
| Same setups at other times (R, X4) | 17979 | 0.080 |  |  | 0.062 |

## P4 · Portfolio heat (E1_trigger_with_trend + X3_target3R)

| rule | cagr | max_dd | mar | final |
|---|---|---|---|---|
| No sector cap | 0.032 | -0.146 | 0.216 | 229,640 |
| Max 1 open per sector | 0.034 | -0.127 | 0.266 | 242,368 |

## P6 · Playbook portfolio (E4_anchor_reclaim + E1_trigger_with_trend, exit X3_target3R, 1 per symbol, 1 per sector, max 5 open)

| risk | trades | trades_per_year | expectancy | win_rate | longest_losing_streak | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|---|---|---|
| 0.50% | 1267 | 47.270 | 0.273 | 0.462 | 14 | 0.041 | -0.096 | 0.430 | 294,672 |
| 0.75% | 1267 | 47.270 | 0.273 | 0.462 | 14 | 0.061 | -0.142 | 0.431 | 491,796 |
| 1.00% | 1267 | 47.270 | 0.273 | 0.462 | 14 | 0.081 | -0.187 | 0.432 | 806,252 |

## E6 · Playbook E4 after a positive earnings gap (stocks)

| group | n | expectancy | ci_low | verdict |
|---|---|---|---|---|
| E4 ≤20 bars after positive gap | 197 | 0.450 |  |  |
| E4 at other times | 2970 | 0.268 |  |  |
| Difference (95% CI low) | 3167 | 0.182 | 0.004 | EARNINGS CONTEXT HELPS |

---
**How to read verdicts.** ADOPT = ≥ min trades, bootstrap CI above 0 after correcting for the number of tests, positive in both time halves and both symbol halves, and better than random entries with the same exits. PROMISING = everything except significance. UNSTABLE = fails a half. REJECT = not positive or not better than random.