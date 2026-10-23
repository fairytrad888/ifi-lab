# R007 Phase 1: information gate on S1+S2

_Run 2026-10-23 16:28 UTC · lock `30cf81d70b9ce176` · snapshot `aa0949a7f26275b5` · events identical to Phase 0: {'snapshot': 'same as Phase 0', 'S1': 'identical', 'S2': 'identical'}_

**Phase 1 FAILED for both models: per the pre-registration, size flat; the weekly-scan score orders alerts for reading only; S3 and E stay unused; R007 closes; no R008.**

Judge events 4414: traded 3686, skipped 728 ({'risk < 0.5 ATR': 512, 'entry open <= stop': 216}). Null trades 20054; events without a null 47.

All traded events: mean R 0.220, +2R-first rate 40.4%; same-week null mean R 0.207.

## 1. Gate (each model: Holm one-sided p < 0.05 across W and L, spread >= 0.10R, each half >= 0.05R)

| model | A-C spread (R) | 90% CI low | 90% CI high | p (one-sided) | weeks | 2008-16 | 2017-26 | Holm p ok | spread ok | halves ok | PASS |
|---|---|---|---|---|---|---|---|---|---|---|---|
| W | 0.020 | -0.102 | 0.136 | 0.372 | 234 | 0.162 | -0.043 | no | no | no | no |
| L | -0.028 | -0.192 | 0.130 | 0.613 | 174 | -0.274 | 0.054 | no | no | no | no |

Model W tier cut points (terciles of all S1+S2 W scores): 1.560 / 3.433

## 2a. Tiers, model W

| tier | traded | skipped | mean_R | hit_2R_first | tail_le_-1.25R | mean_null_R | R_minus_null |
|---|---|---|---|---|---|---|---|
| A | 1257 | 214 | 0.263 | 0.426 | 0.041 | 0.226 | 0.037 |
| B | 1212 | 258 | 0.182 | 0.389 | 0.032 | 0.198 | -0.016 |
| C | 1217 | 256 | 0.213 | 0.396 | 0.035 | 0.195 | 0.016 |

## 2b. Tiers, model L

| tier | traded | skipped | mean_R | hit_2R_first | tail_le_-1.25R | mean_null_R | R_minus_null |
|---|---|---|---|---|---|---|---|
| A | 1336 | 402 | 0.294 | 0.433 | 0.037 | 0.249 | 0.041 |
| B | 1226 | 190 | 0.146 | 0.383 | 0.034 | 0.207 | -0.060 |
| C | 1124 | 136 | 0.213 | 0.392 | 0.036 | 0.156 | 0.058 |

## 3. Model L details (descriptive)

- Chosen C per block (2008-11, 2012-15, 2016-18, 2019-21, 2022-26): {'0': 0.03, '1': 0.03, '2': 0.03, '3': 0.03, '4': 0.03}
- Out-of-fold log-loss 0.6810 vs constant training base rate 0.6764 (gain -0.0046; positive = the tags carry information).
- Leave-one-out (out-of-fold log-loss increase when the input is dropped; positive = the input helps):

| input | logloss change |
|---|---|
| breadth_acc | 0.000 |
| log_stop | 0.000 |
| f_signals_trigger | 0.000 |
| red_age | 0.000 |
| f_accumulation_exit | 0.000 |
| n_types | -0.000 |
| leader | -0.000 |
| f_ad_divergence | -0.000 |
| f_down9 | -0.000 |
| flow_min | -0.000 |
| trig2 | -0.000 |
| f_matrix_divergence | -0.000 |
| stage | -0.000 |
| breadth_stage2 | -0.001 |
| group_state | -0.002 |
| dist_anchor_atr | -0.002 |

Calibration by decile of the out-of-fold probability:

| decile | n | predicted | observed |
|---|---|---|---|
| 0 | 369 | 0.305 | 0.407 |
| 1 | 369 | 0.347 | 0.423 |
| 2 | 368 | 0.369 | 0.380 |
| 3 | 369 | 0.387 | 0.347 |
| 4 | 368 | 0.405 | 0.413 |
| 5 | 369 | 0.421 | 0.409 |
| 6 | 368 | 0.438 | 0.391 |
| 7 | 369 | 0.458 | 0.425 |
| 8 | 368 | 0.482 | 0.394 |
| 9 | 369 | 0.530 | 0.450 |

Reading notes: the gate compares tiers within the same week, so market timing cancels. `R_minus_null` is each event's R minus the mean R of 5 random same-week, same-rule trades on S1+S2 stocks without an event (reported, not judged). Survivorship (today's constituents) flatters levels; the halves rule guards the ranking. Model L's time blocks have no gap, so 26-week outcomes of late-December training events overlap the next block's first weeks; the within-week comparison largely cancels this.
