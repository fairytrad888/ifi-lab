# IFI Lab results: daily · stocks
_Run 2026-10-17 15:15 UTC · 61 symbols · 2000-01-03 to 2026-10-16 · split 2015-01-01 · 42 setup×exit tests (Bonferroni-adjusted) · engine v1.3.3_

> **Survivorship bias:** this stock list was chosen in 2026 from today's large caps, so random long entries earn money too. Judge stock setups by their edge over the random-entry control, not by raw expectancy.

## P1 · Exits × setups (R per trade, after costs)

Random-entry control (same stops and exits), mean expectancy by exit: X1_time10 +0.036R, X2_target2R +0.108R, X3_target3R +0.168R, X4_trendline_trail +0.069R, X5_chandelier3atr +0.151R, X6_partial1R_then_line +0.009R, X7_stage_drop +0.083R

| setup | exit | n | win_rate | avg_win | avg_loss | expectancy | median | exp_w10 | ci_low | ci_low_adj | exp_early | exp_late | exp_symA | exp_symB | random_mean | random_p95 | avg_bars | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 522 | 0.412 | 2.287 | -1.040 | 0.330 | -1.018 | 0.330 | 0.185 | 0.116 | 0.278 | 0.389 | 0.362 | 0.299 | 0.168 | 0.293 | 26.841 | ADOPT |
| E1_trigger_with_trend | X5_chandelier3atr | 524 | 0.435 | 1.688 | -0.779 | 0.294 | -0.261 | 0.280 | 0.150 | 0.066 | 0.210 | 0.389 | 0.390 | 0.198 | 0.151 | 0.316 | 20.032 | REJECT |
| E4_anchor_reclaim | X3_target3R | 3161 | 0.474 | 1.657 | -0.959 | 0.280 | -0.198 | 0.280 | 0.228 | 0.183 | 0.244 | 0.318 | 0.312 | 0.247 | 0.168 | 0.221 | 38.980 | ADOPT |
| E1_trigger_with_trend | X2_target2R | 523 | 0.453 | 1.807 | -1.045 | 0.247 | -1.012 | 0.247 | 0.120 | 0.040 | 0.236 | 0.260 | 0.248 | 0.247 | 0.108 | 0.222 | 21.560 | ADOPT |
| E4_anchor_reclaim | X2_target2R | 3165 | 0.491 | 1.455 | -0.961 | 0.225 | -0.052 | 0.225 | 0.181 | 0.156 | 0.201 | 0.250 | 0.249 | 0.201 | 0.108 | 0.148 | 34.581 | ADOPT |
| E1b_trigger_counter_trend | X3_target3R | 2503 | 0.390 | 2.172 | -1.050 | 0.208 | -1.016 | 0.208 | 0.139 | 0.087 | 0.141 | 0.297 | 0.211 | 0.205 | 0.168 | 0.228 | 26.068 | REJECT |
| E5_score4 | X3_target3R | 5294 | 0.418 | 1.916 | -1.025 | 0.203 | -1.015 | 0.203 | 0.158 | 0.126 | 0.184 | 0.224 | 0.211 | 0.195 | 0.168 | 0.210 | 32.446 | REJECT |
| E3_stage2_transition | X3_target3R | 2504 | 0.413 | 1.893 | -1.002 | 0.194 | -1.013 | 0.194 | 0.132 | 0.109 | 0.198 | 0.189 | 0.162 | 0.225 | 0.168 | 0.230 | 34.217 | REJECT |
| E1_trigger_with_trend | X1_time10 | 526 | 0.540 | 0.969 | -0.774 | 0.167 | 0.129 | 0.167 | 0.075 | 0.028 | 0.150 | 0.186 | 0.172 | 0.163 | 0.036 | 0.134 | 8.656 | ADOPT |
| E3_stage2_transition | X2_target2R | 2536 | 0.446 | 1.621 | -1.005 | 0.166 | -1.008 | 0.166 | 0.109 | 0.085 | 0.171 | 0.160 | 0.144 | 0.188 | 0.108 | 0.156 | 28.864 | ADOPT |
| E5_score4 | X2_target2R | 5597 | 0.451 | 1.608 | -1.023 | 0.165 | -1.008 | 0.165 | 0.131 | 0.105 | 0.146 | 0.186 | 0.173 | 0.157 | 0.108 | 0.140 | 27.847 | ADOPT |
| E4_anchor_reclaim | X7_stage_drop | 3902 | 0.366 | 1.369 | -0.552 | 0.151 | -0.255 | 0.149 | 0.109 | 0.084 | 0.128 | 0.176 | 0.166 | 0.136 | 0.083 | 0.133 | 23.612 | ADOPT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 2590 | 0.382 | 1.718 | -0.825 | 0.146 | -0.441 | 0.142 | 0.078 | 0.033 | 0.046 | 0.282 | 0.160 | 0.133 | 0.151 | 0.220 | 19.533 | REJECT |
| E5_score4 | X7_stage_drop | 6393 | 0.353 | 1.586 | -0.647 | 0.141 | -0.305 | 0.132 | 0.104 | 0.072 | 0.132 | 0.152 | 0.134 | 0.149 | 0.083 | 0.123 | 22.574 | ADOPT |
| E3_stage2_transition | X5_chandelier3atr | 2855 | 0.393 | 1.381 | -0.666 | 0.139 | -0.281 | 0.133 | 0.090 | 0.057 | 0.130 | 0.149 | 0.100 | 0.178 | 0.151 | 0.222 | 20.653 | REJECT |
| E1b_trigger_counter_trend | X2_target2R | 2509 | 0.426 | 1.736 | -1.051 | 0.136 | -1.012 | 0.136 | 0.079 | 0.043 | 0.070 | 0.225 | 0.153 | 0.121 | 0.108 | 0.155 | 21.084 | REJECT |
| E4_anchor_reclaim | X5_chandelier3atr | 3568 | 0.420 | 1.132 | -0.596 | 0.130 | -0.193 | 0.128 | 0.092 | 0.069 | 0.088 | 0.172 | 0.149 | 0.110 | 0.151 | 0.207 | 21.651 | REJECT |
| E5_score4 | X4_trendline_trail | 6741 | 0.338 | 1.484 | -0.570 | 0.124 | -0.285 | 0.116 | 0.088 | 0.065 | 0.107 | 0.143 | 0.128 | 0.121 | 0.069 | 0.104 | 19.863 | ADOPT |
| E4_anchor_reclaim | X4_trendline_trail | 4276 | 0.336 | 1.282 | -0.474 | 0.116 | -0.251 | 0.114 | 0.081 | 0.060 | 0.087 | 0.145 | 0.125 | 0.107 | 0.069 | 0.116 | 19.735 | ADOPT |
| E5_score4 | X5_chandelier3atr | 6529 | 0.390 | 1.365 | -0.690 | 0.111 | -0.287 | 0.107 | 0.076 | 0.060 | 0.104 | 0.119 | 0.097 | 0.127 | 0.151 | 0.196 | 19.515 | REJECT |
| E3_stage2_transition | X7_stage_drop | 3119 | 0.319 | 1.440 | -0.515 | 0.108 | -0.284 | 0.103 | 0.059 | 0.033 | 0.110 | 0.106 | 0.065 | 0.151 | 0.083 | 0.137 | 18.308 | REJECT |
| E2_exhaustion_confluence | X3_target3R | 1247 | 0.320 | 2.637 | -1.093 | 0.100 | -1.035 | 0.100 | 0.002 | -0.057 | 0.051 | 0.157 | 0.139 | 0.065 | 0.168 | 0.252 | 15.594 | REJECT |
| E3_stage2_transition | X4_trendline_trail | 3124 | 0.287 | 1.281 | -0.387 | 0.093 | -0.223 | 0.088 | 0.049 | 0.031 | 0.081 | 0.107 | 0.067 | 0.119 | 0.069 | 0.124 | 13.764 | REJECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 1264 | 0.314 | 2.394 | -0.973 | 0.084 | -1.014 | 0.065 | -0.033 | -0.088 | 0.024 | 0.154 | 0.144 | 0.029 | 0.151 | 0.249 | 15.651 | REJECT |
| E4_anchor_reclaim | X6_partial1R_then_line | 4282 | 0.384 | 0.954 | -0.477 | 0.072 | -0.216 | 0.072 | 0.047 | 0.032 | 0.048 | 0.097 | 0.079 | 0.065 | 0.009 | 0.038 | 19.350 | ADOPT |
| E1_trigger_with_trend | X7_stage_drop | 554 | 0.442 | 0.488 | -0.265 | 0.068 | -0.047 | 0.065 | 0.003 | -0.029 | 0.022 | 0.120 | 0.038 | 0.099 | 0.083 | 0.229 | 3.612 | REJECT |
| E5_score4 | X6_partial1R_then_line | 6831 | 0.412 | 0.976 | -0.575 | 0.063 | -0.212 | 0.063 | 0.040 | 0.027 | 0.048 | 0.081 | 0.067 | 0.059 | 0.009 | 0.031 | 19.053 | ADOPT |
| E1_trigger_with_trend | X4_trendline_trail | 554 | 0.444 | 0.465 | -0.261 | 0.061 | -0.045 | 0.058 | -0.001 | -0.028 | 0.005 | 0.125 | 0.039 | 0.084 | 0.069 | 0.204 | 3.184 | REJECT |
| E3_stage2_transition | X1_time10 | 3004 | 0.508 | 0.718 | -0.646 | 0.046 | 0.012 | 0.046 | 0.013 | -0.007 | 0.044 | 0.048 | 0.036 | 0.057 | 0.036 | 0.078 | 9.122 | REJECT |
| E4_anchor_reclaim | X1_time10 | 3965 | 0.524 | 0.632 | -0.603 | 0.044 | 0.040 | 0.044 | 0.019 | 0.001 | 0.016 | 0.074 | 0.049 | 0.039 | 0.036 | 0.072 | 9.303 | REJECT |
| E3_stage2_transition | X6_partial1R_then_line | 3124 | 0.328 | 0.927 | -0.387 | 0.044 | -0.203 | 0.044 | 0.014 | 0.000 | 0.035 | 0.054 | 0.028 | 0.059 | 0.009 | 0.042 | 13.501 | ADOPT |
| E2_exhaustion_confluence | X2_target2R | 1252 | 0.377 | 1.915 | -1.097 | 0.038 | -1.029 | 0.038 | -0.042 | -0.086 | -0.007 | 0.091 | 0.045 | 0.032 | 0.108 | 0.172 | 11.597 | REJECT |
| E5_score4 | X1_time10 | 7587 | 0.501 | 0.770 | -0.697 | 0.038 | 0.002 | 0.038 | 0.016 | 0.003 | 0.024 | 0.053 | 0.043 | 0.033 | 0.036 | 0.062 | 8.936 | REJECT |
| E1b_trigger_counter_trend | X1_time10 | 2602 | 0.482 | 0.961 | -0.824 | 0.037 | -0.049 | 0.037 | -0.008 | -0.032 | 0.007 | 0.078 | 0.038 | 0.036 | 0.036 | 0.080 | 8.349 | REJECT |
| E1_trigger_with_trend | X6_partial1R_then_line | 554 | 0.446 | 0.407 | -0.261 | 0.037 | -0.044 | 0.037 | -0.011 | -0.037 | -0.006 | 0.085 | -0.000 | 0.075 | 0.009 | 0.084 | 3.182 | REJECT |
| E1b_trigger_counter_trend | X7_stage_drop | 2788 | 0.451 | 0.352 | -0.320 | -0.017 | -0.037 | -0.017 | -0.036 | -0.048 | -0.016 | -0.018 | -0.005 | -0.028 | 0.083 | 0.145 | 2.235 | REJECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 2788 | 0.453 | 0.347 | -0.320 | -0.018 | -0.036 | -0.018 | -0.036 | -0.048 | -0.019 | -0.017 | -0.006 | -0.028 | 0.069 | 0.128 | 2.148 | REJECT |
| E1b_trigger_counter_trend | X6_partial1R_then_line | 2788 | 0.456 | 0.339 | -0.319 | -0.020 | -0.034 | -0.020 | -0.038 | -0.048 | -0.019 | -0.020 | -0.010 | -0.029 | 0.009 | 0.044 | 2.148 | REJECT |
| E2_exhaustion_confluence | X7_stage_drop | 1270 | 0.453 | 0.487 | -0.458 | -0.030 | -0.043 | -0.030 | -0.069 | -0.088 | -0.021 | -0.040 | -0.040 | -0.021 | 0.083 | 0.170 | 2.202 | REJECT |
| E2_exhaustion_confluence | X4_trendline_trail | 1270 | 0.452 | 0.474 | -0.458 | -0.037 | -0.046 | -0.037 | -0.073 | -0.091 | -0.034 | -0.040 | -0.043 | -0.031 | 0.069 | 0.160 | 2.095 | REJECT |
| E2_exhaustion_confluence | X6_partial1R_then_line | 1270 | 0.457 | 0.455 | -0.454 | -0.038 | -0.037 | -0.038 | -0.071 | -0.090 | -0.036 | -0.040 | -0.044 | -0.033 | 0.009 | 0.058 | 2.091 | REJECT |
| E2_exhaustion_confluence | X1_time10 | 1264 | 0.391 | 1.395 | -0.968 | -0.044 | -0.754 | -0.046 | -0.118 | -0.161 | -0.041 | -0.048 | -0.013 | -0.073 | 0.036 | 0.099 | 7.126 | REJECT |

### Exit rules ranked (trade-weighted across setups)

| exit | trades | mean_expectancy | random_mean | edge_over_random |
|---|---|---|---|---|
| X3_target3R | 15,231 | 0.214 | 0.168 | 0.047 |
| X2_target2R | 15,582 | 0.165 | 0.108 | 0.057 |
| X5_chandelier3atr | 17,330 | 0.128 | 0.151 | -0.022 |
| X7_stage_drop | 18,026 | 0.099 | 0.083 | 0.016 |
| X4_trendline_trail | 18,753 | 0.083 | 0.069 | 0.014 |
| X6_partial1R_then_line | 18,849 | 0.042 | 0.009 | 0.033 |
| X1_time10 | 18,948 | 0.039 | 0.036 | 0.003 |

## P1b · Sizing (fixed-fractional, max open positions = 5)

| setup | exit | risk_pct | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X3_target3R | 0.005 | 0.021 | -0.100 | 0.215 | 176,114 |
| E1_trigger_with_trend | X3_target3R | 0.010 | 0.041 | -0.191 | 0.214 | 291,261 |
| E1_trigger_with_trend | X3_target3R | 0.020 | 0.074 | -0.349 | 0.211 | 669,290 |
| E1_trigger_with_trend | X5_chandelier3atr | 0.005 | 0.022 | -0.076 | 0.291 | 179,377 |
| E1_trigger_with_trend | X5_chandelier3atr | 0.010 | 0.042 | -0.147 | 0.288 | 302,556 |
| E1_trigger_with_trend | X5_chandelier3atr | 0.020 | 0.077 | -0.275 | 0.281 | 732,623 |
| E4_anchor_reclaim | X3_target3R | 0.005 | 0.034 | -0.108 | 0.317 | 245,526 |
| E4_anchor_reclaim | X3_target3R | 0.010 | 0.066 | -0.206 | 0.321 | 556,285 |
| E4_anchor_reclaim | X3_target3R | 0.020 | 0.124 | -0.376 | 0.330 | 2,292,811 |

## P2 · Market regime (SPY > 200-day average and Trend line rising)

| setup | exit | n_on | exp_on | n_off | exp_off | diff | diff_ci_low | verdict |
|---|---|---|---|---|---|---|---|---|
| E1_trigger_with_trend | X4_trendline_trail | 236 | 0.054 | 318 | 0.066 | -0.012 | -0.202 | NO CLEAR EFFECT |
| E1_trigger_with_trend | X5_chandelier3atr | 225 | 0.085 | 299 | 0.452 | -0.366 | -0.810 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X4_trendline_trail | 744 | 0.004 | 2044 | -0.026 | 0.030 | -0.031 | NO CLEAR EFFECT |
| E1b_trigger_counter_trend | X5_chandelier3atr | 692 | 0.183 | 1898 | 0.132 | 0.050 | -0.162 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X4_trendline_trail | 313 | -0.076 | 957 | -0.024 | -0.052 | -0.159 | NO CLEAR EFFECT |
| E2_exhaustion_confluence | X5_chandelier3atr | 310 | -0.028 | 954 | 0.121 | -0.149 | -0.514 | NO CLEAR EFFECT |
| E3_stage2_transition | X4_trendline_trail | 1868 | 0.088 | 1256 | 0.099 | -0.011 | -0.143 | NO CLEAR EFFECT |
| E3_stage2_transition | X5_chandelier3atr | 1708 | 0.158 | 1147 | 0.111 | 0.046 | -0.099 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X4_trendline_trail | 2606 | 0.125 | 1670 | 0.102 | 0.023 | -0.082 | NO CLEAR EFFECT |
| E4_anchor_reclaim | X5_chandelier3atr | 2219 | 0.136 | 1349 | 0.119 | 0.018 | -0.090 | NO CLEAR EFFECT |
| E5_score4 | X4_trendline_trail | 4449 | 0.142 | 2292 | 0.091 | 0.051 | -0.056 | NO CLEAR EFFECT |
| E5_score4 | X5_chandelier3atr | 4409 | 0.125 | 2120 | 0.082 | 0.043 | -0.062 | NO CLEAR EFFECT |

## P3 · Earnings drift (stocks)

| test | n | mean | mean_vs_spy | hit_vs_spy | ci_low |
|---|---|---|---|---|---|
| Positive earnings gap → hold 20 bars | 752 | 0.017 | 0.010 | 0.532 |  |
| IFI setups ≤20 bars after positive gap (R, X4) | 798 | 0.172 |  |  | 0.088 |
| Same setups at other times (R, X4) | 17955 | 0.079 |  |  | 0.062 |

## P4 · Portfolio heat (E1_trigger_with_trend + X3_target3R)

| rule | cagr | max_dd | mar | final |
|---|---|---|---|---|
| No sector cap | 0.032 | -0.146 | 0.216 | 229,055 |
| Max 1 open per sector | 0.034 | -0.127 | 0.266 | 241,750 |

## P6 · Playbook portfolio (E4_anchor_reclaim + E1_trigger_with_trend, exit X3_target3R, 1 per symbol, 1 per sector, max 5 open)

| risk | trades | trades_per_year | expectancy | win_rate | longest_losing_streak | cagr | max_dd | mar | final |
|---|---|---|---|---|---|---|---|---|---|
| 0.50% | 1267 | 47.338 | 0.269 | 0.456 | 15 | 0.040 | -0.078 | 0.509 | 283,877 |
| 0.75% | 1267 | 47.338 | 0.269 | 0.456 | 15 | 0.059 | -0.115 | 0.514 | 464,402 |
| 1.00% | 1267 | 47.338 | 0.269 | 0.456 | 15 | 0.078 | -0.150 | 0.518 | 745,653 |

## E6 · Playbook E4 after a positive earnings gap (stocks)

| group | n | expectancy | ci_low | verdict |
|---|---|---|---|---|
| E4 ≤20 bars after positive gap | 197 | 0.450 |  |  |
| E4 at other times | 2964 | 0.269 |  |  |
| Difference (95% CI low) | 3161 | 0.181 | -0.006 | NO CLEAR EFFECT |

---
**How to read verdicts.** ADOPT = ≥ min trades, bootstrap CI above 0 after correcting for the number of tests, positive in both time halves and both symbol halves, and better than random entries with the same exits. PROMISING = everything except significance. UNSTABLE = fails a half. REJECT = not positive or not better than random.