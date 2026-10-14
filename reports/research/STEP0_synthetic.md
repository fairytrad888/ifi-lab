# Step 0 pipeline check on random walks (should show NO information)

_18 ratios · 2000-01-03 to 2026-09-11 · 125,370 ratio-days · 3-month block bootstrap, Bonferroni k=7_

## Gate

- Trend-state information (P1-P4): NO
- Accumulation-bounce information (P5): NO
- Pullback-in-uptrend information (P6): NO
- Cross-sectional ranking (P7 IC): NO (IC -0.019, t -1.44, needs > 2.69)

**Decision:** STOP: Daily ratio states carry no measurable information at 5-20 days. Ratio rules are not built; ratios remain context. Effort moves to E4 on prices, exits/allocation, and the forecast ledger..

## Primary results (h = 20 bars, ratio, % difference in forward return)

| test | comparison | diff % | 95% CI | adj. CI low | n (A / B) | 2000-14 | 2015- | sectors | others | pass |
|---|---|---|---|---|---|---|---|---|---|---|
| P1 | stage 3 vs stage -1 | -0.09 | -0.27 … +0.09 | -0.34 | 49,998 / 37,055 | -0.04 | -0.15 | -0.11 | -0.05 | – |
| P2 | Trend line rising vs falling | -0.06 | -0.19 … +0.07 | -0.23 | 63,288 / 62,082 | -0.03 | -0.10 | -0.05 | -0.07 | – |
| P3 | HH+HL vs LH+LL | -0.04 | -0.22 … +0.15 | -0.30 | 41,410 / 39,247 | -0.06 | -0.02 | -0.11 | +0.06 | – |
| P4 | above vs below anchor | -0.10 | -0.25 … +0.06 | -0.29 | 63,563 / 61,807 | -0.09 | -0.11 | -0.12 | -0.07 | – |
| P5 | <=10 bars after washout exit vs no washout | -0.07 | -0.24 … +0.10 | -0.31 | 28,889 / 88,680 | +0.00 | -0.17 | -0.06 | -0.09 | – |
| P6 | pullback to line in HH+HL uptrend vs all days | +0.04 | -0.18 … +0.27 | -0.26 | 5,792 / 125,370 | -0.15 | +0.30 | -0.06 | +0.21 | – |

P7 rank IC (stage vs 20-bar forward return): all -0.019 (t -1.44, 340 dates) · 2000-14 +0.003 · 2015- -0.027 · no pass

## All horizons and the tradeable version (numerator ETF price, same dates)

| test | h | measure | diff % | 95% CI | pass |
|---|---|---|---|---|---|
| P1 | 5 | ratio | -0.01 | -0.06 … +0.05 | – |
| P1 | 5 | numerator price | -0.04 | -0.11 … +0.02 | – |
| P1 | 10 | ratio | -0.03 | -0.12 … +0.07 | – |
| P1 | 10 | numerator price | -0.08 | -0.19 … +0.02 | – |
| P1 | 20 | ratio | -0.09 | -0.27 … +0.09 | – |
| P1 | 20 | numerator price | -0.20 | -0.40 … +0.01 | – |
| P2 | 5 | ratio | -0.02 | -0.06 … +0.02 | – |
| P2 | 5 | numerator price | -0.05 | -0.09 … -0.00 | – |
| P2 | 10 | ratio | -0.03 | -0.10 … +0.04 | – |
| P2 | 10 | numerator price | -0.07 | -0.15 … +0.01 | – |
| P2 | 20 | ratio | -0.06 | -0.19 … +0.07 | – |
| P2 | 20 | numerator price | -0.13 | -0.28 … +0.03 | – |
| P3 | 5 | ratio | +0.02 | -0.04 … +0.08 | – |
| P3 | 5 | numerator price | +0.00 | -0.06 … +0.07 | – |
| P3 | 10 | ratio | -0.01 | -0.11 … +0.10 | – |
| P3 | 10 | numerator price | -0.05 | -0.17 … +0.08 | – |
| P3 | 20 | ratio | -0.04 | -0.22 … +0.15 | – |
| P3 | 20 | numerator price | -0.14 | -0.35 … +0.08 | – |
| P4 | 5 | ratio | -0.02 | -0.06 … +0.02 | – |
| P4 | 5 | numerator price | -0.04 | -0.09 … +0.01 | – |
| P4 | 10 | ratio | -0.03 | -0.11 … +0.05 | – |
| P4 | 10 | numerator price | -0.07 | -0.16 … +0.02 | – |
| P4 | 20 | ratio | -0.10 | -0.25 … +0.06 | – |
| P4 | 20 | numerator price | -0.17 | -0.34 … +0.02 | – |
| P5 | 5 | ratio | -0.08 | -0.14 … -0.02 | – |
| P5 | 5 | numerator price | -0.06 | -0.13 … +0.01 | – |
| P5 | 10 | ratio | -0.12 | -0.23 … -0.01 | – |
| P5 | 10 | numerator price | -0.10 | -0.22 … +0.02 | – |
| P5 | 20 | ratio | -0.07 | -0.24 … +0.10 | – |
| P5 | 20 | numerator price | -0.01 | -0.19 … +0.18 | – |
| P6 | 5 | ratio | +0.04 | -0.08 … +0.14 | – |
| P6 | 5 | numerator price | +0.02 | -0.11 … +0.13 | – |
| P6 | 10 | ratio | +0.06 | -0.11 … +0.24 | – |
| P6 | 10 | numerator price | +0.05 | -0.14 … +0.23 | – |
| P6 | 20 | ratio | +0.04 | -0.18 … +0.27 | – |
| P6 | 20 | numerator price | +0.02 | -0.22 … +0.26 | – |

## Current ratio states (last completed bar)

| ratio | group | date | stage | line | structure | anchor | phase | pullback in uptrend |
|---|---|---|---|---|---|---|---|---|
| XLU/SPY | S | 2026-10-09 | 1 | ▼ | up | below | none |  |
| QQQ/SPY | O | 2026-10-09 | 3 | ▲ | mixed | above | none |  |
| XLB/SPY | S | 2026-10-09 | 3 | ▲ | mixed | above | none |  |
| XLC/SPY | S | 2026-10-09 | 3 | ▲ | up | above | none |  |
| XLE/SPY | S | 2026-10-09 | 3 | ▲ | up | above | none |  |
| XLF/SPY | S | 2026-10-09 | 3 | ▲ | up | above | none |  |
| XLI/SPY | S | 2026-10-09 | 0 | ▲ | down | below | none |  |
| XLK/SPY | S | 2026-10-09 | 3 | ▲ | mixed | above | none |  |
| GLD/SPY | O | 2026-10-09 | 0 | ▲ | down | above | post_exit |  |
| XLP/SPY | S | 2026-10-09 | 0 | ▲ | up | above | none | yes |
| XLV/SPY | S | 2026-10-09 | 3 | ▲ | up | above | none |  |
| XLY/SPY | S | 2026-10-09 | -1 | ▼ | down | below | none |  |
| SMH/SPY | O | 2026-10-09 | 3 | ▲ | down | above | none |  |
| XBI/SPY | O | 2026-10-09 | 3 | ▲ | up | above | none |  |
| IWM/SPY | O | 2026-10-09 | 3 | ▲ | up | above | none |  |
| RSP/SPY | O | 2026-10-09 | 3 | ▲ | up | above | none |  |
| XLRE/SPY | S | 2026-10-09 | 0 | ▼ | mixed | above | none |  |
| TLT/SPY | O | 2026-10-09 | 3 | ▲ | up | above | none |  |
