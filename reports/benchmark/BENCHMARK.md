# Benchmark test v1: does the IFI book beat simply holding the market?

_Run 2026-10-17 21:02 UTC · commit `4fb42fa` · lock `f7dbae2e2aa467dc` · sealed manifest `bf7473c15cb8b4c7` · design manifest `a3609f3fec828066` · returns price only, idle cash 0%_

Pre-registered in `research/benchmark/prereg_benchmark_v1.yaml`. A measurement: the construction-v1 books (same trades, same seeds) against SPY buy-and-hold and a SPY 200-day trend rule. It selects no rule.

## Validity

| check | result |
|---|---|
| Lock (prereg, benchmark and construction code, data modules; construction and exit locks too) | ok `f7dbae2e2aa467dc` |
| Synthetic null (zero alpha) | ok: alpha +0.85% a year (95% -1.06 to +2.81), beta 0.60; required: gate A does not pass |
| Synthetic power (planted alpha 4%/yr) | ok: alpha +4.85% a year (95% +2.94 to +6.81), beta 0.60; required: gate A passes |
| Pinned snapshots (nothing downloaded) | design `a3609f3fec828066` · sealed `bf7473c15cb8b4c7` |

## Verdict (sealed set, the real rule B0)

| verdict | A: alpha beyond SPY and trend (95% low > 0) | B: beats the trend rule (P ≥ 0.95) | C: beats buy-and-hold (P ≥ 0.95) |
|---|---|---|---|
| **NO_EDGE_BEYOND_BENCHMARKS** | no (-1.22%, 95% -3.74% to +1.30%) | no (P 0.076) | no (P 0.044) |

On data it was not built on, the book adds nothing a passive or one-line rule doesn't. The live forward test continues as the final word, with the trend rule as the hurdle; no new entry or construction tests until live evidence shows alpha.

## Sealed set (out of sample)

_5,503 E4/E1 trades (mean +0.132 R) · 2000-01-10 to 2026-10-15 · monthly returns_

| book | Sharpe book | Sharpe SPY | Sharpe trend rule | P(book > trend) | P(book > SPY) | alpha vs SPY (a year) | beta | alpha vs SPY + trend | 95% interval | residual vol |
|---|---|---|---|---|---|---|---|---|---|---|
| B0 current: 5 slots x 0.75% | 0.22 | 0.50 | 0.49 | 0.076 | 0.044 | -0.89% | 0.37 | -1.22% | -3.74% to +1.30% | +6.6% |
| C1 every signal at 0.10%, cash-limited | 0.40 | 0.50 | 0.49 | 0.263 | 0.258 | +0.27% | 0.31 | -0.03% | -1.77% to +1.60% | +4.3% |
| S20 20 slots x 0.1875% | 0.43 | 0.50 | 0.49 | 0.325 | 0.313 | +0.35% | 0.33 | +0.05% | -1.62% to +1.62% | +4.2% |

Same risk: each benchmark scaled to the book's daily volatility.

| book | book CAGR / max DD | SPY at the same volatility | trend rule at the same volatility |
|---|---|---|---|
| B0 | +1.4% / -28.2% | +3.4% / -30.3% (×0.46) | +3.6% / -21.6% (×0.80) |
| C1 | +2.4% / -21.3% | +2.8% / -25.1% (×0.38) | +3.0% / -17.8% (×0.65) |
| S20 | +2.7% / -20.3% | +2.7% / -24.0% (×0.36) | +2.9% / -17.0% (×0.62) |

Total-return SPY (dividends included; the books' R is price only, so this is harsher on the books): alpha vs SPY B0 -1.55% (beta 0.37), C1 -0.28% (beta 0.31), S20 -0.25% (beta 0.33).

## Design data (working history; the book was built here)

_4,702 E4/E1 trades (mean +0.297 R) · 2000-01-10 to 2026-10-14 · monthly returns_

| book | Sharpe book | Sharpe SPY | Sharpe trend rule | P(book > trend) | P(book > SPY) | alpha vs SPY (a year) | beta | alpha vs SPY + trend | 95% interval | residual vol |
|---|---|---|---|---|---|---|---|---|---|---|
| B0 current: 5 slots x 0.75% | 0.69 | 0.50 | 0.49 | 0.855 | 0.889 | +3.40% | 0.36 | +3.06% | +0.92% to +5.20% | +6.8% |
| C1 every signal at 0.10%, cash-limited | 0.91 | 0.50 | 0.49 | 0.995 | 1.000 | +3.06% | 0.28 | +2.76% | +1.57% to +3.88% | +3.6% |
| S20 20 slots x 0.1875% | 0.81 | 0.50 | 0.49 | 0.972 | 0.993 | +2.81% | 0.32 | +2.45% | +1.22% to +3.67% | +4.0% |

Same risk: each benchmark scaled to the book's daily volatility.

| book | book CAGR / max DD | SPY at the same volatility | trend rule at the same volatility |
|---|---|---|---|
| B0 | +5.9% / -19.0% | +3.3% / -29.6% (×0.45) | +3.5% / -21.2% (×0.78) |
| C1 | +5.1% / -12.9% | +2.3% / -21.0% (×0.31) | +2.5% / -14.8% (×0.54) |
| S20 | +5.1% / -15.9% | +2.5% / -22.8% (×0.34) | +2.7% / -16.1% (×0.58) |

Total-return SPY (dividends included; the books' R is price only, so this is harsher on the books): alpha vs SPY B0 +2.72% (beta 0.37), C1 +2.55% (beta 0.28), S20 +2.22% (beta 0.33).

_Alpha: annualized intercept of monthly book returns regressed on SPY (and, beyond, on the trend rule). A book that only holds the market part of the time shows a low beta and an alpha near zero._
