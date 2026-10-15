# E4 profile: the proven edge, measured (descriptive only)

_Run 2026-10-15 20:01 UTC · snapshot cutoff 2026-10-14 (manifest `a3609f3fec828066`) · E4 entry + X3 exit (3R target, 60 bars) · Lab sequencing (one open trade per symbol) · R includes dividends unless marked price-only_

**Nothing here is a test.** Every split below is a description of the past. A pattern worth acting on becomes a pre-registered hypothesis, ideally confirmed on the live paper log first. With dozens of slices, some will look different by chance alone.

## 1. Headline

| universe | trades | trades/yr | mean R | mean R (price only) | win % | avg win | avg loss | median R | profit factor | random-entry mean R (same exit) | E4 minus random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ETF | 872 | 32.6 | +0.403 | +0.336 | 52 | +1.63 | -0.95 | +0.13 | 1.90 | +0.166 | +0.236 |
| stock | 3,112 | 116.3 | +0.332 | +0.282 | 48 | +1.69 | -0.94 | -0.14 | 1.68 | +0.224 | +0.108 |

_Random entries (5 seeds per symbol, ~1 per 40 bars) with the same stop, exit and one-trade-per-symbol sequencing show how much of the mean R any long entry would earn from drift; the difference is the part that comes from the E4 entry itself._

## 2. Over time (ETFs)

| year | trades | mean R | win share | median R |
|---|---|---|---|---|
| 2000 | 34 | -0.487 | 23.5% | -1.010 |
| 2001 | 26 | -0.478 | 30.8% | -0.960 |
| 2002 | 22 | -0.580 | 18.2% | -0.926 |
| 2003 | 21 | +1.485 | 81.0% | +1.867 |
| 2004 | 31 | +0.132 | 38.7% | -0.914 |
| 2005 | 40 | +0.407 | 60.0% | +0.570 |
| 2006 | 25 | +1.019 | 68.0% | +1.684 |
| 2007 | 43 | -0.029 | 39.5% | -0.950 |
| 2008 | 24 | -0.630 | 16.7% | -0.977 |
| 2009 | 29 | +0.795 | 65.5% | +0.793 |
| 2010 | 36 | +0.608 | 50.0% | +0.005 |
| 2011 | 41 | -0.221 | 31.7% | -1.014 |
| 2012 | 33 | +1.090 | 69.7% | +1.227 |
| 2013 | 19 | +0.883 | 73.7% | +1.324 |
| 2014 | 34 | +0.710 | 70.6% | +0.899 |
| 2015 | 30 | -0.246 | 43.3% | -0.923 |
| 2016 | 35 | +1.138 | 91.4% | +1.259 |
| 2017 | 18 | +1.609 | 77.8% | +2.215 |
| 2018 | 44 | -0.394 | 27.3% | -0.990 |
| 2019 | 44 | +1.049 | 68.2% | +0.418 |
| 2020 | 34 | +1.058 | 73.5% | +0.975 |
| 2021 | 27 | +0.503 | 63.0% | +0.689 |
| 2022 | 53 | -0.404 | 30.2% | -1.012 |
| 2023 | 37 | +0.773 | 62.2% | +0.722 |
| 2024 | 31 | +0.882 | 61.3% | +0.891 |
| 2025 | 43 | +0.477 | 46.5% | -0.078 |
| 2026 | 18 | +1.363 | 77.8% | +1.796 |

Linear trend of the yearly mean: +0.0322 R per year (descriptive; yearly means are noisy).
- 2000-2014: 458 trades, mean +0.288 R, win 48%
- 2015-: 414 trades, mean +0.530 R, win 57%

## 3. Shape of the results (ETFs)

- R percentiles 5/25/50/75/95: -1.04 / -1.01 / +0.13 / +1.48 / +3.07
- Exit reasons: time 391 (45%), stop 334 (38%), target 97 (11%), stop_gap 50 (6%)
- Mean R by exit reason: stop -0.99, stop_gap -1.10, target +3.10, time +1.11
- Losers that were at least +1R at some point: 20% of losers
- Winners that were at -0.5R or worse at some point: 38% of winners
- Average holding: 41 bars (winners 55, losers 25)

_Best and worst points during a trade (MFE/MAE) use daily highs and lows, price only (no dividends)._

## 4. Streaks and portfolio (ETFs)

- Longest losing streak in the full history: 19 trades
- Longest losing streak to expect within any 100 trades (bootstrap): 95th percentile 9, 99th 11

| risk per trade | trades taken (max 5 open) | CAGR | max drawdown | MAR |
|---|---|---|---|---|
| 0.50% | 493 | 3.5% | -12.6% | 0.28 |
| 0.75% | 493 | 5.2% | -18.4% | 0.28 |
| 1.00% | 493 | 6.8% | -23.8% | 0.29 |

_Daily mark-to-market equity, dividends included. The drawdown scales roughly with risk; MAR barely changes, because risk size doesn't change the edge._

## 5. Stops, gaps and stop width (ETFs)

- Stops filled through a gap: 50 (5.7% of trades), mean -1.10 R (worst -2.47 R)

| stop width quintile | median stop width (% of price) | trades | mean R | win share |
|---|---|---|---|---|
| 1 narrowest | 2.9% | 175 | +0.731 | 48.0% |
| 2 | 4.1% | 174 | +0.495 | 53.4% |
| 3 | 5.1% | 174 | +0.254 | 52.3% |
| 4 | 6.4% | 174 | +0.293 | 51.7% |
| 5 widest | 9.1% | 175 | +0.239 | 56.6% |

## 6. By symbol (ETFs)

| ETF | trades | mean R | win share |
|---|---|---|---|
| XLC | 12 | +0.977 | 58.3% |
| XLI | 57 | +0.653 | 59.6% |
| QQQ | 51 | +0.652 | 64.7% |
| XLU | 59 | +0.643 | 50.8% |
| XBI | 42 | +0.629 | 57.1% |
| IWM | 49 | +0.548 | 57.1% |
| RSP | 51 | +0.503 | 56.9% |
| XLK | 54 | +0.466 | 57.4% |
| XLP | 62 | +0.393 | 51.6% |
| XLV | 68 | +0.355 | 47.1% |
| SMH | 48 | +0.328 | 50.0% |
| XLE | 58 | +0.290 | 50.0% |
| XLY | 57 | +0.270 | 50.9% |
| XLF | 61 | +0.264 | 49.2% |
| XLRE | 25 | +0.135 | 44.0% |
| XLB | 59 | +0.119 | 47.5% |
| SPY | 59 | +0.067 | 44.1% |

_Per-symbol samples are small (about 30-60 trades); differences between symbols are mostly noise._

## 7. Clustering (ETFs)

| entry clustering | trades | mean R | win share |
|---|---|---|---|
| 2 entries within 3 days | 162 | +0.312 | 50.6% |
| 3+ entries within 3 days | 494 | +0.433 | 54.7% |
| alone | 216 | +0.400 | 48.6% |

_Clustered entries usually share one market move: their results are correlated, so 5 open positions entered in the same week are closer to one bet than five._

## 8. Context at the signal bar (ETFs; hypothesis-generating only)

**price above a rising 200-day average**

| group | trades | mean R | win share |
|---|---|---|---|
| False | 375 | +0.449 | 54.7% |
| True | 497 | +0.368 | 50.7% |

**SPY above a rising 200-day average**

| group | trades | mean R | win share |
|---|---|---|---|
| False | 311 | +0.286 | 51.4% |
| True | 561 | +0.467 | 52.9% |

**IFI stage**

| group | trades | mean R | win share |
|---|---|---|---|
| -1 | 2 | -0.279 | 50.0% |
| 0 | 56 | -0.044 | 41.1% |
| 1 | 2 | +0.313 | 100.0% |
| 3 | 812 | +0.435 | 53.1% |

**ATR percentile (250 bars)**

| group | trades | mean R | win share |
|---|---|---|---|
| low | 169 | +0.480 | 47.3% |
| mid | 303 | +0.508 | 54.5% |
| high | 400 | +0.290 | 53.0% |

**distance above the anchor (ATR)**

| group | trades | mean R | win share |
|---|---|---|---|
| < 0.5 | 569 | +0.477 | 53.1% |
| 0.5-1.5 | 172 | +0.365 | 55.8% |
| > 1.5 | 131 | +0.128 | 45.0% |

**bars since the last washout exit**

| group | trades | mean R | win share |
|---|---|---|---|
| <= 20 | 224 | +0.335 | 51.3% |
| 21-60 | 334 | +0.410 | 52.7% |
| > 60 | 314 | +0.443 | 52.9% |

_17 groups shown. At this many, a difference of about ±0.2 R between groups of ~200 trades can appear by chance._
