# Ranking test v1: which E4 signals should take the 5 slots?

_Run 2026-10-15 21:31 UTC · commit `7c62df1` · lock `d52fee814461fe5a` · snapshot cutoff 2026-10-14 (manifest `a3609f3fec828066`) · 61 stocks (primary) + 17 ETFs (consistency) · risk 0.75%, max 5 open, notional cap 20% per position_

Pre-registered in `research/ranking/prereg_ranking_v1.yaml`. The hypotheses came from the ETF profile, so ETFs only have to agree in sign; the stock universe, whose context slices were never inspected, is the evidence.

## Validity

| check | result |
|---|---|
| Lock (prereg, ranking code, exit simulator, engine, ifi modules; exit lock too) | ok `d52fee814461fe5a` |
| Engine look-ahead (truncation) | ok: identical events at 3 cut points on 2 synthetic markets (1093 events in the last full run) |
| Synthetic nulls (nothing planted) | ok: martingale prices: F1 FAIL, persistent trends: F1 FAIL (required: no PASS) |
| Synthetic power (persistent trends, -0.5 R planted on the trades F1 skips) | ok: F1 PASS, percentile in random-drop controls 100.0% (required: PASS) |
| Frozen snapshot (pre-registered manifest) | cutoff 2026-10-14 · manifest `a3609f3fec828066` |
| Baseline parity (uncapped first-come = research/exits/run.py portfolio()) | ok: stocks: 797 trades, CAGR 5.759%, max DD -16.379% in both |

## Verdict

| arm | rule | verdict | information | both halves | sizing (uncapped) | consistency (ETFs) | stock trades changed |
|---|---|---|---|---|---|---|---|
| F1 | skip signals more than 1.5 ATR above the anchor or at stage < 1 | **FAIL** | no | yes | yes | yes | 651 |

Design note: same-day ranking arms were dropped before this run because the synthetic power check showed they cannot move portfolio MAR (see design_history in the pre-registration).

## Stocks, capped (the primary book)

| book | trades | CAGR | max drawdown | MAR | avg exposure | MAR 2000-14 | MAR 2015- | random-control median MAR | control quantile to beat | arm percentile in controls |
|---|---|---|---|---|---|---|---|---|---|---|
| baseline (first-come) | 797 | 5.4% | -15.9% | 0.340 | 44.8% | 0.188 | 0.819 | – | – | – |
| F1 | 732 | 6.0% | -14.3% | 0.416 | 44.1% | 0.277 | 0.892 | 0.328 | 0.476 | 85.7% |

Paired calendar-block bootstrap of daily returns (6-month blocks; reported, not gating): 95% interval of arm MAR − baseline MAR:
- F1: -0.149 to +0.326

F1 skips 24.6% of stock E4 signals; its control skips the same share at random (300 draws).

## Sign checks: uncapped stocks, capped ETFs, and one combined book (78 symbols)

| book | baseline MAR | F1 |
|---|---|---|
| stocks, uncapped | 0.352 | 0.429 |
| ETFs, capped | 0.244 | 0.301 |
| combined, capped (report only) | 0.308 | 0.378 |
| combined, capped: CAGR / max DD | 5.4% / -17.6% | 6.2% / -16.4% |

## Supporting per-trade checks (stocks, one open trade per symbol; unadjusted 95% intervals; not gating)

| check | measure | estimate | 95% interval | parts |
|---|---|---|---|---|
| C5 | mean R (dist > 1.5) − mean R (dist ≤ 1.5) | -0.078 | -0.232 to +0.081 | +0.273 (n 762) vs +0.351 (n 2350) |
| C6 | mean R (stage < 1) − mean R (stage ≥ 1) | -0.063 | -0.311 to +0.181 | +0.273 (n 170) vs +0.336 (n 2942) |
| C3b | (E4 narrow − wide) − (random narrow − wide) | +0.023 | -0.159 to +0.225 | E4 +0.355 / +0.330; random +0.219 / +0.217; narrow ≤ 4.7%, wide ≥ 12.1% of price |

## Decision

First-come with no filter stays. The slot question is closed for this cycle (these definitions are not re-tested on this data). Supporting checks update the candidate registry only.
