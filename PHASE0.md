# R007 Phase 0: events, features and checks (no outcomes)

_Run 2026-10-22 15:28 UTC · lock `e47a7479492e6491` · live reference `37f6f7d4126c` (2026-10-20T16:52:52Z) · snapshot `aa0949a7f26275b5`_

**Phase 0: NOT PASSED** · lock ok · look-ahead ok · fidelity ok · live parity ok · power below criterion

No outcome was computed. Phase 1 (S1 gate) needs its own deploy and an explicit go.

## 1. Universe and snapshot
- Universe 1503 (live list): S1 559, S2 552, S3 207, E 65, X 114, XD 6 (X = excluded, already used by IFI tests; XD = second share class of a company).
- Snapshot: 1533 tickers, 7 missing (ADIG, BLFS, CWEN-A, HLX, LEG, QRVO, VYLR); reused: True; tickers with a later split (price floor made point-in-time): 631.
- Build: 1487 stocks read, 9 too short, 7 without data, 0 without a group; 36 group ETFs with a state series.

## 2. Events
| set | events | symbols | weeks | per_week_median | max_in_a_week | share_top_10_weeks |
|---|---|---|---|---|---|---|
| S1 | 2260 | 464 | 559 | 2.00 | 62 | 0.17 |
| S2 | 2154 | 430 | 545 | 2.00 | 52 | 0.15 |
| S3 | 878 | 162 | 364 | 1.00 | 22 | 0.17 |
| E | 221 | 44 | 157 | 1.00 | 6 | 0.18 |

Events per year:

| year | S1 | S2 | S3 | E |
|---|---|---|---|---|
| 2008 | 193 | 203 | 75 | 14 |
| 2009 | 54 | 47 | 19 | 5 |
| 2010 | 34 | 39 | 6 | 1 |
| 2011 | 87 | 87 | 31 | 12 |
| 2012 | 64 | 54 | 23 | 7 |
| 2013 | 36 | 34 | 16 | 2 |
| 2014 | 64 | 79 | 27 | 6 |
| 2015 | 125 | 102 | 48 | 11 |
| 2016 | 84 | 74 | 31 | 6 |
| 2017 | 82 | 64 | 28 | 8 |
| 2018 | 213 | 219 | 94 | 24 |
| 2019 | 120 | 113 | 45 | 13 |
| 2020 | 95 | 88 | 32 | 3 |
| 2021 | 75 | 83 | 37 | 9 |
| 2022 | 318 | 275 | 142 | 31 |
| 2023 | 205 | 188 | 70 | 19 |
| 2024 | 119 | 121 | 39 | 11 |
| 2025 | 231 | 210 | 90 | 33 |
| 2026 | 61 | 74 | 25 | 6 |

## 3. Features (S1 + S2, no outcomes)
| feature | shares (S1+S2) |
|---|---|
| group_state | basing 15%, bearish 41%, bullish 21%, missing 3%, neutral 20% |
| n_types | 1 90%, 2 10%, 3 0% |
| stage | -1 57%, 0 1%, 1 42%, 3 0% |
| red_age | 0.0 21%, 1.0 78%, 2.0 0%, 3.0 1% |
| trig2 | 0 98%, 1 2% |
| leader | 0.0 72%, 1.0 28% |
| f_signals_trigger | present 3% |
| f_ad_divergence | present 4% |
| f_matrix_divergence | present 2% |
| f_down9 | present 22% |
| f_accumulation_exit | present 80% |

| feature | missing | p1 | p25 | median | p75 | p99 |
|---|---|---|---|---|---|---|
| flow_min | 0.00 | -5.97 | -0.78 | 0.56 | 1.51 | 2.27 |
| stop_pct | 0.00 | 0.00 | 0.03 | 0.05 | 0.09 | 0.36 |
| dist_anchor_atr | 0.02 | -11.07 | -4.68 | -3.27 | -1.46 | 7.06 |
| breadth_acc | 0.00 | 0.02 | 0.10 | 0.18 | 0.32 | 0.67 |
| breadth_stage2 | 0.00 | 0.00 | 0.08 | 0.24 | 0.44 | 0.80 |
| w_score | 0.00 | 0.35 | 1.45 | 2.66 | 4.23 | 6.21 |

Feature pairs with |r| >= 0.4:

| a | b | r |
|---|---|---|
| red_age | f_accumulation_exit | 0.90 |
| trig2 | f_signals_trigger | 0.77 |
| breadth_acc | breadth_stage2 | -0.67 |
| f_down9 | f_accumulation_exit | -0.63 |
| red_age | f_down9 | -0.55 |
| red_age | stop_pct | 0.42 |
| n_types | f_down9 | 0.42 |
| n_types | f_signals_trigger | 0.40 |

**Model W tier cut points** (terciles of S1 W scores): 1.568 / 3.417

| set | A | B | C | weeks_with_A_and_C | sum_week_weight |
|---|---|---|---|---|---|
| S1 | 753 | 750 | 757 | 162 | 213.19 |
| S2 | 741 | 680 | 733 | 174 | 215.74 |

## 4. Look-ahead (truncation) and fidelity to the weekly scan on real data
- 60 symbols x 5 cuts: identical; group-state failures 0.
- Fidelity on the same symbols: week records vs weekscan `week_records` at 300 weeks, arms vs weekscan `step` (578 arms): identical.
- Not covered by truncation (by design): Yahoo's split adjustment (handled by the split factor in the price floor; all other inputs are ratios) and weekscan's bad-tick filter, which removes one-bar spikes of 40%+ that fully reverse on the next bar.

## 5. Live parity (weekscan code on the R007 snapshot vs the live armed list)
- Armed: live 165, R007 replay 168, shared 165, Jaccard 0.9821; among shared: armed week 100.0%, low 100.0%, released 100.0%. Week alerts: live 1, R007 1, Jaccard 1.0.
- Only live: –
- Only R007: OI, SAH, WD
- Mismatches near the eligibility thresholds at the live run date (price within 10% of $5 or dollar volume within 25% of $20M, where intraday vs end-of-day data can flip them): 3 of 3.

## 6. Synthetic power (real event weeks, random tiers, planted A-C spread)
**S1**

| spread_R | events | weeks_with_events | power | power_holm_worst | gate_pass | mean_est | sd_est |
|---|---|---|---|---|---|---|---|
| 0.00 | 2260.00 | 559.00 | 0.05 | 0.03 | 0.04 | 0.00 | 0.09 |
| 0.10 | 2260.00 | 559.00 | 0.36 | 0.25 | 0.23 | 0.10 | 0.09 |
| 0.15 | 2260.00 | 559.00 | 0.52 | 0.40 | 0.37 | 0.15 | 0.08 |
| 0.20 | 2260.00 | 559.00 | 0.72 | 0.59 | 0.56 | 0.19 | 0.09 |
| 0.25 | 2260.00 | 559.00 | 0.87 | 0.80 | 0.75 | 0.25 | 0.09 |
| 0.30 | 2260.00 | 559.00 | 0.97 | 0.95 | 0.90 | 0.30 | 0.08 |

**S1 (W tiers)**

| spread_R | events | weeks_with_events | power | power_holm_worst | gate_pass | mean_est | sd_est |
|---|---|---|---|---|---|---|---|
| 0.00 | 2260.00 | 559.00 | 0.04 | 0.03 | 0.03 | -0.01 | 0.10 |
| 0.10 | 2260.00 | 559.00 | 0.31 | 0.19 | 0.23 | 0.11 | 0.10 |
| 0.15 | 2260.00 | 559.00 | 0.48 | 0.34 | 0.37 | 0.15 | 0.10 |
| 0.20 | 2260.00 | 559.00 | 0.67 | 0.53 | 0.57 | 0.20 | 0.09 |
| 0.25 | 2260.00 | 559.00 | 0.84 | 0.76 | 0.73 | 0.25 | 0.09 |
| 0.30 | 2260.00 | 559.00 | 0.94 | 0.89 | 0.86 | 0.30 | 0.09 |

**S2**

| spread_R | events | weeks_with_events | power | power_holm_worst | gate_pass | mean_est | sd_est |
|---|---|---|---|---|---|---|---|
| 0.00 | 2154.00 | 545.00 | 0.07 | 0.04 | 0.05 | 0.00 | 0.09 |
| 0.10 | 2154.00 | 545.00 | 0.33 | 0.24 | 0.26 | 0.10 | 0.09 |
| 0.15 | 2154.00 | 545.00 | 0.57 | 0.45 | 0.45 | 0.16 | 0.09 |
| 0.20 | 2154.00 | 545.00 | 0.73 | 0.61 | 0.61 | 0.20 | 0.09 |
| 0.25 | 2154.00 | 545.00 | 0.91 | 0.83 | 0.82 | 0.26 | 0.09 |
| 0.30 | 2154.00 | 545.00 | 0.96 | 0.92 | 0.88 | 0.30 | 0.09 |

**S2 (W tiers)**

| spread_R | events | weeks_with_events | power | power_holm_worst | gate_pass | mean_est | sd_est |
|---|---|---|---|---|---|---|---|
| 0.00 | 2154.00 | 545.00 | 0.05 | 0.02 | 0.03 | 0.00 | 0.09 |
| 0.10 | 2154.00 | 545.00 | 0.28 | 0.21 | 0.23 | 0.10 | 0.10 |
| 0.15 | 2154.00 | 545.00 | 0.47 | 0.34 | 0.37 | 0.15 | 0.09 |
| 0.20 | 2154.00 | 545.00 | 0.63 | 0.52 | 0.54 | 0.19 | 0.10 |
| 0.25 | 2154.00 | 545.00 | 0.85 | 0.75 | 0.73 | 0.25 | 0.10 |
| 0.30 | 2154.00 | 545.00 | 0.94 | 0.89 | 0.87 | 0.31 | 0.09 |

`power` = P(one-sided p < 0.05); `power_holm_worst` = P(p < 0.025); `gate_pass` = the full Phase 1 rule (p < 0.05, spread >= 0.15R, each half >= 0.075R); at a true spread of exactly 0.15R the point rule alone passes about half the time, so read `gate_pass` for the chance that Phase 1 passes at each true spread. Criterion: power >= 0.80 at 0.15R on S1 with random thirds. The `(W tiers)` tables use model W's actual tiers, which involve no outcome; they show how much power is lost when a model's tiers cluster by week (reported, not judged).
