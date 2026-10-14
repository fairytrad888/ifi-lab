# Step 0: does the Daily ratio state carry information?

_18 ratios · 2000-01-03 to 2026-09-16 · 105,793 ratio-days · 3-month block bootstrap, Bonferroni k=7_

## Gate

- Trend-state information (P1-P4): NO
- Accumulation-bounce information (P5): NO
- Pullback-in-uptrend information (P6): NO
- Cross-sectional ranking (P7 IC): NO (IC -0.010, t -0.48, needs > 2.69)

**Decision:** STOP: Daily ratio states carry no measurable information at 5-20 days. Ratio rules are not built; ratios remain context. Effort moves to E4 on prices, exits/allocation, and the forecast ledger..

## Primary results (h = 20 bars, ratio, % difference in forward return)

| test | comparison | diff % | 95% CI | adj. CI low | n (A / B) | 2000-14 | 2015- | sectors | others | pass |
|---|---|---|---|---|---|---|---|---|---|---|
| P1 | stage 3 vs stage -1 | -0.01 | -0.28 … +0.24 | -0.38 | 40,028 / 32,003 | +0.00 | -0.03 | -0.08 | +0.09 | – |
| P2 | Trend line rising vs falling | -0.03 | -0.22 … +0.17 | -0.30 | 52,056 / 53,737 | +0.01 | -0.07 | -0.04 | -0.00 | – |
| P3 | HH+HL vs LH+LL | -0.12 | -0.36 … +0.09 | -0.44 | 32,819 / 34,125 | +0.01 | -0.26 | -0.16 | -0.06 | – |
| P4 | above vs below anchor | +0.09 | -0.14 … +0.33 | -0.20 | 52,401 / 53,392 | +0.12 | +0.06 | +0.02 | +0.20 | – |
| P5 | <=10 bars after washout exit vs no washout | -0.07 | -0.28 … +0.13 | -0.34 | 22,856 / 76,925 | -0.10 | -0.05 | -0.09 | -0.04 | – |
| P6 | pullback to line in HH+HL uptrend vs all days | +0.00 | -0.21 … +0.21 | -0.29 | 5,789 / 105,793 | +0.15 | -0.19 | +0.04 | -0.05 | – |

P7 rank IC (stage vs 20-bar forward return): all -0.010 (t -0.48, 336 dates) · 2000-14 -0.009 · 2015- -0.043 · no pass

## All horizons and the tradeable version (numerator ETF price, same dates)

| test | h | measure | diff % | 95% CI | pass |
|---|---|---|---|---|---|
| P1 | 5 | ratio | -0.03 | -0.12 … +0.06 | – |
| P1 | 5 | numerator price | -0.08 | -0.17 … +0.01 | – |
| P1 | 10 | ratio | -0.02 | -0.18 … +0.13 | – |
| P1 | 10 | numerator price | -0.13 | -0.30 … +0.04 | – |
| P1 | 20 | ratio | -0.01 | -0.28 … +0.24 | – |
| P1 | 20 | numerator price | -0.20 | -0.53 … +0.10 | – |
| P2 | 5 | ratio | -0.03 | -0.10 … +0.04 | – |
| P2 | 5 | numerator price | -0.06 | -0.13 … +0.02 | – |
| P2 | 10 | ratio | -0.01 | -0.12 … +0.11 | – |
| P2 | 10 | numerator price | -0.06 | -0.19 … +0.06 | – |
| P2 | 20 | ratio | -0.03 | -0.22 … +0.17 | – |
| P2 | 20 | numerator price | -0.14 | -0.36 … +0.10 | – |
| P3 | 5 | ratio | -0.06 | -0.15 … +0.02 | – |
| P3 | 5 | numerator price | -0.09 | -0.19 … +0.01 | – |
| P3 | 10 | ratio | -0.10 | -0.24 … +0.05 | – |
| P3 | 10 | numerator price | -0.17 | -0.36 … +0.01 | – |
| P3 | 20 | ratio | -0.12 | -0.36 … +0.09 | – |
| P3 | 20 | numerator price | -0.22 | -0.54 … +0.09 | – |
| P4 | 5 | ratio | +0.02 | -0.06 … +0.09 | – |
| P4 | 5 | numerator price | +0.01 | -0.08 … +0.08 | – |
| P4 | 10 | ratio | +0.05 | -0.08 … +0.19 | – |
| P4 | 10 | numerator price | +0.02 | -0.12 … +0.17 | – |
| P4 | 20 | ratio | +0.09 | -0.14 … +0.33 | – |
| P4 | 20 | numerator price | +0.02 | -0.27 … +0.30 | – |
| P5 | 5 | ratio | -0.05 | -0.13 … +0.03 | – |
| P5 | 5 | numerator price | -0.00 | -0.09 … +0.09 | – |
| P5 | 10 | ratio | -0.07 | -0.20 … +0.06 | – |
| P5 | 10 | numerator price | +0.03 | -0.13 … +0.19 | – |
| P5 | 20 | ratio | -0.07 | -0.28 … +0.13 | – |
| P5 | 20 | numerator price | +0.19 | -0.08 … +0.46 | – |
| P6 | 5 | ratio | -0.05 | -0.13 … +0.04 | – |
| P6 | 5 | numerator price | -0.08 | -0.22 … +0.06 | – |
| P6 | 10 | ratio | -0.00 | -0.14 … +0.13 | – |
| P6 | 10 | numerator price | -0.01 | -0.22 … +0.21 | – |
| P6 | 20 | ratio | +0.00 | -0.21 … +0.21 | – |
| P6 | 20 | numerator price | -0.07 | -0.35 … +0.22 | – |

## Current ratio states (last completed bar)

| ratio | group | date | stage | line | structure | anchor | phase | pullback in uptrend |
|---|---|---|---|---|---|---|---|---|
| IWM/SPY | O | 2026-10-14 | 1 | ▼ | mixed | below | washout |  |
| XLY/SPY | S | 2026-10-14 | -1 | ▼ | down | below | post_exit |  |
| XLF/SPY | S | 2026-10-14 | -1 | ▼ | down | below | post_exit |  |
| GLD/SPY | O | 2026-10-14 | -1 | ▼ | down | below | post_exit |  |
| XLI/SPY | S | 2026-10-14 | -1 | ▼ | down | below | none |  |
| XLE/SPY | S | 2026-10-14 | 3 | ▲ | mixed | above | none |  |
| QQQ/SPY | O | 2026-10-14 | 0 | ▼ | up | above | none |  |
| XLK/SPY | S | 2026-10-14 | 0 | ▼ | up | above | none |  |
| XLB/SPY | S | 2026-10-14 | -1 | ▼ | down | below | post_exit |  |
| RSP/SPY | O | 2026-10-14 | -1 | ▼ | down | below | post_exit |  |
| XLRE/SPY | S | 2026-10-14 | -1 | ▼ | down | below | post_exit |  |
| XLU/SPY | S | 2026-10-14 | 1 | ▲ | mixed | below | none |  |
| XLC/SPY | S | 2026-10-14 | -1 | ▼ | mixed | below | post_exit |  |
| XBI/SPY | O | 2026-10-14 | -1 | ▼ | down | below | none |  |
| XLV/SPY | S | 2026-10-14 | 3 | ▲ | mixed | above | post_exit |  |
| SMH/SPY | O | 2026-10-14 | 0 | ▼ | up | below | none |  |
| XLP/SPY | S | 2026-10-14 | 3 | ▲ | down | above | post_exit |  |
| TLT/SPY | O | 2026-10-14 | -1 | ▼ | mixed | below | post_exit |  |
