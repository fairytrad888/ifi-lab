# Book construction test v1: how should the proven edge be deployed?

_Run 2026-10-16 13:03 UTC · commit `5ac20a4` · lock `a5718f5bc26ee246` · sealed snapshot cutoff 2026-10-15 (manifest `bf7473c15cb8b4c7`, created 2026-10-16T13:01:43Z) · design data: exit-test snapshot `a3609f3fec828066`_

Pre-registered in `research/construction/prereg_construction_v1.yaml`. The confirmation runs on a **sealed set** of symbols no IFI test had used. Both books trade exactly the same E4/E1 signals with the Lab's 3R exit; only the deployment differs.

## Validity

| check | result |
|---|---|
| Lock (prereg, construction code, Lab and research modules; exit lock too) | ok `a5718f5bc26ee246` |
| Synthetic null (martingale prices) | ok: C1 FAIL (P 0.442; Sharpe C1 -0.25 vs B0 -0.20; required: no PASS) |
| Synthetic power (persistent trends, independent symbols) | ok: C1 PASS (P 1.000; Sharpe C1 2.43 vs B0 1.32; required: PASS) |
| Design trades vs the Lab's trade files (informational) | 4,700 of 4,700 Lab E4/E1 trades have the same entry here (2 only here); 4,570 of those have the same R to 1e-6 (informational: the Lab files may come from a different data date) |
| Design data (working history, daily marks) | ok: P 0.951, both halves True; Sharpe C1 0.91 vs B0 0.69 |
| Sealed snapshot (opened once) | created 2026-10-16T13:01:43Z · cutoff 2026-10-15 · 91 symbols · missing: BK |

## Verdict (sealed set)

| comparison | verdict | information (P ≥ 0.95) | both halves | edge present |
|---|---|---|---|---|
| C1 vs B0 | **FAIL** | no (P = 0.873) | no | yes |

Bootstrap of Sharpe C1 − B0: 5th to 95th percentile -0.07 to +0.43. B0 Sharpe across its 30 random same-day orders: 0.15 to 0.29 (10th–90th pct); C1: 0.39 to 0.40.

## Books on the sealed set (5,503 E4/E1 trades, mean +0.132 R)

| book | rule | Sharpe | Sharpe 2000–14 | Sharpe 2015– | P(beats B0) | CAGR | max DD | MAR | worst month | trades/yr | signals taken | positions avg / max | heat avg / max |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B0 | current: 5 slots x 0.75% | 0.22 | 0.18 | 0.25 | – | 1.4% | -28.2% | 0.05 | -7.0% | 32 | 16% | 4.5 / 5 | 3.3% / 3.9% |
| C1 | every signal at 0.10%, cash-limited | 0.40 | 0.57 | 0.22 | 0.873 | 2.4% | -21.3% | 0.11 | -4.8% | 200 | 97% | 29.0 / 85 | 2.9% / 8.1% |
| C2 | every signal at 0.20%, max 2 new per day | 0.36 | 0.50 | 0.20 | 0.832 | 2.6% | -25.9% | 0.10 | -6.8% | 132 | 64% | 18.8 / 44 | 3.7% / 8.7% |
| S10 | 10 slots x 0.375% | 0.39 | 0.58 | 0.19 | 0.934 | 2.6% | -26.4% | 0.10 | -5.8% | 62 | 30% | 8.7 / 10 | 3.2% / 3.9% |
| S20 | 20 slots x 0.1875% | 0.43 | 0.56 | 0.30 | 0.959 | 2.7% | -20.3% | 0.13 | -6.8% | 110 | 53% | 15.7 / 20 | 2.9% / 3.9% |

## Same drawdown, different return (sealed set, daily marks)

| max drawdown target | book | risk per trade | CAGR | max DD | Sharpe | signals taken |
|---|---|---|---|---|---|---|
| -15% | 5 slots | 0.300% | 0.7% | -12.2% | 0.24 | 16% |
| -15% | every signal | 0.050% | 1.3% | -10.9% | 0.41 | 100% |
| -15% | every signal, max 2 new a day | 0.075% | 1.2% | -11.9% | 0.36 | 71% |
| -20% | 5 slots | 0.500% | 1.2% | -19.5% | 0.24 | 16% |
| -20% | every signal | 0.075% | 1.9% | -16.0% | 0.41 | 100% |
| -20% | every signal, max 2 new a day | 0.100% | 1.5% | -15.7% | 0.36 | 71% |

_The largest risk on the ladder whose median max drawdown is no deeper than the target. The full ladder is below._

### Risk ladder (sealed set): medians over 5 random orders

| risk per trade | 5 slots: CAGR / max DD / Sharpe | every signal: CAGR / max DD / Sharpe | every signal, max 2 new a day: CAGR / max DD / Sharpe |
|---|---|---|---|
| 0.050% | 0.1% / -2.1% / 0.24 | 1.3% / -10.9% / 0.41 | 0.8% / -8.1% / 0.36 |
| 0.075% | 0.2% / -3.2% / 0.24 | 1.9% / -16.0% / 0.41 | 1.2% / -11.9% / 0.36 |
| 0.100% | 0.3% / -4.2% / 0.24 | 2.4% / -20.9% / 0.40 | 1.5% / -15.7% / 0.36 |
| 0.150% | 0.4% / -6.2% / 0.24 | 3.2% / -26.3% / 0.41 | 2.1% / -22.3% / 0.34 |
| 0.200% | 0.5% / -8.3% / 0.24 | 3.6% / -32.7% / 0.41 | 2.6% / -27.0% / 0.36 |
| 0.300% | 0.7% / -12.2% / 0.24 | 3.8% / -38.4% / 0.39 | 3.5% / -32.5% / 0.39 |
| 0.400% | 1.0% / -15.9% / 0.24 | 3.8% / -43.5% / 0.37 | 3.6% / -39.1% / 0.37 |
| 0.500% | 1.2% / -19.5% / 0.24 | 3.8% / -47.8% / 0.36 | 3.7% / -42.3% / 0.36 |
| 0.750% | 1.4% / -27.4% / 0.22 | 3.2% / -48.0% / 0.31 | 3.3% / -46.9% / 0.31 |
| 1.000% | 2.7% / -35.7% / 0.31 | 2.9% / -47.2% / 0.28 | 3.3% / -48.5% / 0.31 |
| 1.250% | 1.6% / -44.4% / 0.20 | 2.0% / -54.3% / 0.21 | 2.3% / -53.0% / 0.23 |
| 1.500% | 3.0% / -46.1% / 0.29 | 2.6% / -57.8% / 0.26 | 3.0% / -53.7% / 0.28 |

## Whole shares (C1 at 0.10% risk, sealed set)

| account | signals taken | Sharpe | CAGR | max DD |
|---|---|---|---|---|
| $25,000 | 97% | 0.41 | 2.3% | -19.1% |
| $100,000 | 97% | 0.41 | 2.4% | -20.3% |

_A position smaller than one share is skipped. Fractional shares (if your broker offers them) remove this limit._

## Bad-market months (sealed set; reported, not gating)

| months | count | B0 mean monthly return | C1 mean monthly return |
|---|---|---|---|
| bad-market months | 69 | -0.27% | -0.07% |
| other months | 252 | 0.27% | 0.29% |

_Bad-market month: starts with SPY below a falling 200-day average (state at the previous month's last close)._

## E4 and E1 on new symbols (first out-of-sample check of the setups; reported, not gating)

| universe | setup | trades | mean R | win rate | random-entry mean R (same exit) | setup minus random |
|---|---|---|---|---|---|---|
| etf | E1 | 237 | +0.152 | 41% | 0.064 | 0.088 |
| etf | E4 | 1,962 | +0.155 | 45% | 0.064 | 0.091 |
| stock | E1 | 415 | +0.238 | 40% | 0.069 | 0.169 |
| stock | E4 | 2,889 | +0.100 | 44% | 0.069 | 0.031 |

## Design data (working history, daily marks): the finding the sealed set was asked to confirm

Gate check: information P = 0.951, both halves yes, edge present yes (4,702 trades, mean +0.297 R).

| book | rule | Sharpe | Sharpe 2000–14 | Sharpe 2015– | P(beats B0) | CAGR | max DD | MAR | worst month | trades/yr | signals taken | positions avg / max | heat avg / max |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B0 | current: 5 slots x 0.75% | 0.69 | 0.58 | 0.82 | – | 5.9% | -19.0% | 0.31 | -7.0% | 33 | 19% | 4.5 / 5 | 3.3% / 3.9% |
| C1 | every signal at 0.10%, cash-limited | 0.91 | 0.76 | 1.08 | 0.951 | 5.1% | -12.9% | 0.40 | -4.5% | 175 | 100% | 25.6 / 74 | 2.5% / 7.1% |
| C2 | every signal at 0.20%, max 2 new per day | 0.88 | 0.82 | 0.94 | 0.943 | 6.9% | -15.5% | 0.45 | -5.5% | 127 | 73% | 18.1 / 41 | 3.6% / 7.9% |
| S10 | 10 slots x 0.375% | 0.72 | 0.41 | 1.06 | 0.619 | 5.3% | -20.0% | 0.26 | -5.6% | 63 | 36% | 8.6 / 10 | 3.2% / 3.9% |
| S20 | 20 slots x 0.1875% | 0.81 | 0.61 | 1.02 | 0.869 | 5.1% | -15.9% | 0.32 | -4.8% | 110 | 63% | 15.4 / 20 | 2.9% / 3.8% |

| max drawdown target | book | risk per trade | CAGR | max DD | Sharpe | signals taken |
|---|---|---|---|---|---|---|
| -15% | 5 slots | 0.500% | 4.1% | -14.7% | 0.71 | 19% |
| -15% | every signal | 0.100% | 5.1% | -12.9% | 0.91 | 100% |
| -15% | every signal, max 2 new a day | 0.150% | 5.5% | -12.1% | 0.91 | 75% |
| -20% | 5 slots | 0.500% | 4.1% | -14.7% | 0.71 | 19% |
| -20% | every signal | 0.150% | 6.9% | -18.4% | 0.88 | 94% |
| -20% | every signal, max 2 new a day | 0.200% | 6.9% | -15.5% | 0.89 | 73% |

### Risk ladder (design data)

| risk per trade | 5 slots: CAGR / max DD / Sharpe | every signal: CAGR / max DD / Sharpe | every signal, max 2 new a day: CAGR / max DD / Sharpe |
|---|---|---|---|
| 0.050% | 0.4% / -1.6% / 0.70 | 2.6% / -6.7% / 0.91 | 1.9% / -4.2% / 0.92 |
| 0.075% | 0.6% / -2.3% / 0.70 | 3.9% / -9.8% / 0.91 | 2.8% / -6.2% / 0.92 |
| 0.100% | 0.8% / -3.1% / 0.70 | 5.1% / -12.9% / 0.91 | 3.7% / -8.2% / 0.92 |
| 0.150% | 1.2% / -4.6% / 0.70 | 6.9% / -18.4% / 0.88 | 5.5% / -12.1% / 0.91 |
| 0.200% | 1.6% / -6.1% / 0.70 | 7.4% / -23.5% / 0.82 | 6.9% / -15.5% / 0.89 |
| 0.300% | 2.4% / -9.1% / 0.70 | 7.8% / -28.6% / 0.75 | 8.0% / -20.8% / 0.82 |
| 0.400% | 3.2% / -11.9% / 0.70 | 8.1% / -30.2% / 0.73 | 8.7% / -27.6% / 0.79 |
| 0.500% | 4.1% / -14.7% / 0.71 | 8.6% / -34.5% / 0.71 | 8.9% / -31.4% / 0.75 |
| 0.750% | 5.7% / -21.5% / 0.67 | 9.8% / -39.0% / 0.73 | 10.3% / -37.8% / 0.76 |
| 1.000% | 6.5% / -27.1% / 0.62 | 10.4% / -41.7% / 0.72 | 11.0% / -43.4% / 0.77 |
| 1.250% | 8.6% / -30.0% / 0.71 | 11.7% / -43.8% / 0.77 | 11.7% / -38.2% / 0.78 |
| 1.500% | 7.8% / -37.1% / 0.58 | 12.0% / -42.6% / 0.77 | 11.8% / -42.8% / 0.76 |

## Decision

The 5-slot book stays. The construction question is closed for this cycle; the sealed set has been used once and is logged.
