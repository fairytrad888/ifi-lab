# Research diagnostics (inputs only: no forward returns, no rule tested)

_Snapshot cutoff 2026-10-14 · manifest `a5bb7be73b52cba8` · lock `5345b23c62de6500` · thresholds v2.1 base set_

## 1. TradingView parity

Matched **100%** within 1.5% (Step 1 requires 90%).

| ratio | date | field | TradingView | Python | difference |
|---|---|---|---|---|---|
| XLE | 2022-12-30 | close | 0.1144 | 0.1144 | 0.03% |
| XLE | 2022-12-30 | line | 0.1115 | 0.1115 | 0.04% |
| XLE | 2022-12-30 | anchor | 0.1065 | 0.1063 | 0.21% |
| XLE | 2022-12-30 | sma200 | 0.1013 | 0.1013 | 0.01% |
| XLK | 2022-12-30 | close | 0.1627 | 0.1627 | 0.00% |
| XLK | 2022-12-30 | line | 0.1650 | 0.1650 | 0.02% |
| XLU | 2022-12-30 | close | 0.0922 | 0.0922 | 0.03% |
| XLU | 2022-12-30 | line | 0.0905 | 0.0905 | 0.03% |
| XLE | 2022-08-17 | close | 0.0907 | 0.0907 | 0.01% |
| XLE | 2022-08-17 | line | 0.0923 | 0.0923 | 0.04% |
| XLE | 2022-08-17 | anchor | 0.0958 | 0.0947 | 1.20% |
| XLE | 2022-08-17 | sma200 | 0.0827 | 0.0827 | 0.03% |
| XLU | 2022-08-17 | close | 0.0908 | 0.0908 | 0.04% |
| XLU | 2022-08-17 | line | 0.0896 | 0.0896 | 0.06% |
| XLU | 2022-08-17 | anchor | 0.0905 | 0.0905 | 0.04% |
| XLU | 2022-08-17 | sma200 | 0.0822 | 0.0822 | 0.00% |
| XLK | 2026-10-14 | line | 0.2505 | 0.2504 | 0.06% |
| XLK | 2026-10-14 | anchor | 0.2440 | 0.2446 | 0.23% |
| XLK | 2026-10-14 | sma200 | 0.2296 | 0.2298 | 0.09% |
| XLU | 2026-10-14 | line | 0.0543 | 0.0543 | 0.01% |
| XLU | 2026-10-14 | anchor | 0.0603 | 0.0599 | 0.61% |
| XLU | 2026-10-14 | sma200 | 0.0614 | 0.0614 | 0.08% |
| XLF | 2026-10-14 | line | 0.0719 | 0.0719 | 0.01% |
| XLF | 2026-10-14 | anchor | 0.0740 | 0.0740 | 0.05% |
| XLF | 2026-10-14 | sma200 | 0.0742 | 0.0742 | 0.01% |
| XLI | 2026-10-14 | line | 0.2238 | 0.2239 | 0.02% |
| XLI | 2026-10-14 | anchor | 0.2349 | 0.2341 | 0.32% |
| XLI | 2026-10-14 | sma200 | 0.2391 | 0.2391 | 0.01% |

## 2. Definition audit

Found **72%** (Step 1 requires 80%): reclaims (Trend 2.0 E4 markers) 18/22 · rule 3 tops (eye-dated) 13/21.

| kind | ratio | logged window | found | engine dates in window | if missed: nearest engine event (±40 bars) | note |
|---|---|---|---|---|---|---|
| reclaim | XLK | 2026-04-06 … 2026-04-24 | yes | 2026-04-13 (B) |  | mid-Apr E4, leg to 0.262 |
| reclaim | XLK | 2026-09-08 … 2026-09-25 | yes | 2026-09-08 (none), 2026-09-11 (none), 2026-09-17 (none) |  | mid-Sep E4 |
| reclaim | SMH | 2026-09-08 … 2026-09-25 | yes | 2026-09-22 (A) |  | mid-Sep E4 |
| reclaim | XLE | 2026-01-08 … 2026-01-23 | yes | 2026-01-14 (A) |  | mid-Jan E4 (+2.98R) |
| reclaim | XLE | 2026-07-20 … 2026-08-21 | yes | 2026-07-23 (B), 2026-07-29 (none), 2026-08-14 (none) |  | late-Jul / mid-Aug E4s |
| reclaim | XLV | 2026-03-18 … 2026-04-03 | yes | 2026-03-30 (B) |  | late-Mar E4 without a floor (-1.1R) |
| reclaim | XLV | 2026-06-08 … 2026-06-24 | **no** |  | 2026-06-25 (1 bars after) tier none | mid-Jun E4 |
| reclaim | XLRE | 2026-01-29 … 2026-02-13 | yes | 2026-02-10 (none) |  | early-Feb E4 |
| reclaim | XLRE | 2026-07-20 … 2026-08-03 | yes | 2026-07-24 (none) |  | late-Jul E4 (-1.03R) |
| reclaim | RSP | 2025-12-01 … 2025-12-31 | yes | 2025-12-16 (A) |  | Dec E4 without a visible floor |
| reclaim | RSP | 2026-06-08 … 2026-06-24 | yes | 2026-06-24 (B) |  | mid-Jun E4 |
| reclaim | XLF | 2025-12-15 … 2026-01-02 | **no** |  | 2025-12-12 (1 bars before) tier B | late-Dec E4 without a floor |
| reclaim | XLF | 2026-06-08 … 2026-06-30 | **no** |  | 2026-07-02 (2 bars after) tier A | June E4 after the June floor |
| reclaim | XLI | 2025-12-29 … 2026-01-16 | yes | 2026-01-05 (A) |  | early-Jan E4 (+2.96R) |
| reclaim | XLI | 2026-06-18 … 2026-07-02 | yes | 2026-06-22 (none), 2026-06-24 (none) |  | late-Jun E4 (-1.03R) |
| reclaim | XLU | 2026-01-20 … 2026-02-06 | **no** |  | 2026-02-12 (4 bars after) tier none | late-Jan E4 |
| reclaim | XLE | 2021-12-27 … 2022-01-14 | yes | 2022-01-04 (A) |  | Dec 2021 reclaim, leg to Jun 2022 |
| reclaim | XLE | 2022-08-22 … 2022-09-09 | yes | 2022-08-22 (none) |  | Aug 2022 reclaim of 0.0958 |
| reclaim | XLU | 2021-11-29 … 2021-12-17 | yes | 2021-12-06 (none), 2021-12-13 (none) |  | early-Dec 2021 reclaim |
| reclaim | XLU | 2022-08-08 … 2022-08-26 | yes | 2022-08-09 (none), 2022-08-17 (none) |  | mid-Aug 2022 reclaim |
| reclaim | XLU | 2022-11-28 … 2022-12-16 | yes | 2022-11-28 (none), 2022-12-06 (none) |  | early-Dec 2022 reclaim |
| reclaim | XLK | 2022-07-18 … 2022-08-05 | yes | 2022-07-20 (A) |  | late-Jul 2022 reclaim |
| r3 | XLK | 2026-06-15 … 2026-07-10 | **no** |  | 2026-07-16 (4 bars after) | June top |
| r3 | SMH | 2026-06-15 … 2026-07-17 | yes | 2026-07-16 |  | June top (-22%) |
| r3 | XLE | 2026-04-01 … 2026-04-24 | **no** |  | 2026-05-08 (10 bars after) | April collapse |
| r3 | XLV | 2026-03-25 … 2026-04-17 | yes | 2026-04-09 |  | March top |
| r3 | XLRE | 2026-03-25 … 2026-04-30 | **no** |  | 2026-03-20 (3 bars before) | Mar lower high, Apr lower low |
| r3 | XLRE | 2026-07-27 … 2026-08-14 | **no** |  | 2026-09-04 (15 bars after) | after the late-Jul spike |
| r3 | RSP | 2026-03-20 … 2026-04-17 | yes | 2026-04-09 |  | March top |
| r3 | RSP | 2026-08-31 … 2026-09-18 | yes | 2026-09-08 |  | second top |
| r3 | XLF | 2026-01-15 … 2026-02-10 | yes | 2026-01-23 |  | January top |
| r3 | XLF | 2026-09-04 … 2026-09-25 | yes | 2026-09-08 |  | September top |
| r3 | XLI | 2026-03-30 … 2026-04-17 | yes | 2026-04-15 |  | March top |
| r3 | XLI | 2026-07-27 … 2026-08-14 | yes | 2026-08-07 |  | July top |
| r3 | XLU | 2026-04-01 … 2026-04-24 | **no** |  | 2026-05-06 (8 bars after) | Mar-Apr top |
| r3 | XLU | 2026-08-03 … 2026-08-28 | **no** |  | none within 40 bars | August top |
| r3 | XLE | 2021-11-08 … 2021-12-03 | **no** |  | 2021-10-29 (6 bars before) | Oct-Nov 2021 top |
| r3 | XLE | 2022-06-20 … 2022-07-15 | yes | 2022-07-05 |  | June 2022 top |
| r3 | XLE | 2022-12-01 … 2022-12-23 | yes | 2022-12-05 |  | Nov-Dec 2022 top |
| r3 | XLK | 2021-12-27 … 2022-01-21 | yes | 2022-01-05 |  | Dec 2021 top |
| r3 | XLK | 2022-08-22 … 2022-09-16 | yes | 2022-08-22 |  | Aug 2022 top |
| r3 | XLU | 2022-07-11 … 2022-07-29 | yes | 2022-07-19 |  | July 2022 whipsaw |
| r3 | XLU | 2022-10-03 … 2022-11-04 | **no** |  | 2022-11-11 (5 bars after) | Sep-Oct 2022 top |

**Rule 3 misses: pivot highs before each window end** (a top arms only on a higher high while the line is rising, then needs a lower high and a close below the last pivot low)

- XLK 2026-06-15…2026-07-10: 03-25 0.2102 HH; 04-30 0.2245 HH; 05-14 0.2407 HH; 06-08 0.2619 HH; 06-25 0.2590 LH; 07-06 0.2553 LH
- XLE 2026-04-01…2026-04-24: 01-08 0.0687 HH (line not rising); 02-24 0.0814 HH; 03-05 0.0851 HH; 04-02 0.0991 HH
- XLRE 2026-03-25…2026-04-30: 01-05 0.0593 LH (line not rising); 01-23 0.0615 HH (line not rising); 02-20 0.0643 HH; 03-06 0.0642 LH; 03-25 0.0639 LH (line not rising); 04-06 0.0637 LH (line not rising); 04-10 0.0635 LH (line not rising); 04-23 0.0630 LH (line not rising)
- XLRE 2026-07-27…2026-08-14: 04-23 0.0630 LH (line not rising); 05-26 0.0599 LH (line not rising); 06-15 0.0620 HH (line not rising); 07-01 0.0625 HH (line not rising); 07-13 0.0604 LH (line not rising); 07-22 0.0616 HH (line not rising); 08-03 0.0630 HH
- XLU 2026-04-01…2026-04-24: 01-07 0.0632 LH (line not rising); 01-26 0.0637 HH (line not rising); 02-03 0.0629 LH (line not rising); 02-20 0.0688 HH; 03-05 0.0699 HH; 03-25 0.0711 HH; 04-02 0.0727 HH
- XLU 2026-08-03…2026-08-28: 05-28 0.0608 LH (line not rising); 06-16 0.0608 LH (line not rising); 07-01 0.0640 HH (line not rising); 07-10 0.0617 LH (line not rising); 07-22 0.0619 HH (line not rising); 07-29 0.0628 HH (line not rising); 08-21 0.0580 LH (line not rising)
- XLE 2021-11-08…2021-12-03: 08-16 0.0565 LH (line not rising); 09-01 0.0551 LH (line not rising); 09-22 0.0564 HH (line not rising); 10-14 0.0657 HH; 10-21 0.0652 LH; 10-29 0.0649 LH; 11-11 0.0632 LH (line not rising); 11-30 0.0620 LH (line not rising)
- XLU 2022-10-03…2022-11-04: 07-18 0.0924 LH; 07-29 0.0905 LH (line not rising); 08-05 0.0909 HH (line not rising); 08-12 0.0914 HH (line not rising); 08-25 0.0928 HH; 09-13 0.0973 HH; 09-19 0.0973 HH; 09-29 0.0977 HH

## 3. Data and state summary (after the 250-bar warm-up)

| ratio | group | first | last | bars | gaps >5d | max gap (d) | stage 3 % | stage 2 % | stage −1 % | line rising % | flat % | reclaims | tier A | tier B | rule 3 | washout exits | bull divs | warnings |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| XLB/SPY | S | 1998-12-22 | 2026-10-14 | 6995 | 1 | 7 | 35 | 8 | 29 | 32 | 33 | 86 | 15 | 18 | 66 | 183 | 135 | 258 |
| XLC/SPY | S | 2018-06-19 | 2026-10-14 | 2092 | 0 | 4 | 40 | 5 | 27 | 32 | 34 | 35 | 7 | 4 | 21 | 40 | 38 | 75 |
| XLE/SPY | S | 1998-12-22 | 2026-10-14 | 6995 | 1 | 7 | 34 | 8 | 33 | 33 | 28 | 82 | 24 | 10 | 70 | 174 | 168 | 279 |
| XLF/SPY | S | 1998-12-22 | 2026-10-14 | 6995 | 1 | 7 | 36 | 7 | 31 | 32 | 32 | 98 | 22 | 11 | 77 | 170 | 158 | 208 |
| XLI/SPY | S | 1998-12-22 | 2026-10-14 | 6995 | 1 | 7 | 41 | 6 | 27 | 35 | 34 | 114 | 24 | 11 | 69 | 149 | 135 | 281 |
| XLK/SPY | S | 1998-12-22 | 2026-10-14 | 6995 | 1 | 7 | 44 | 8 | 25 | 39 | 34 | 118 | 15 | 17 | 72 | 140 | 127 | 319 |
| XLP/SPY | S | 1998-12-22 | 2026-10-14 | 6995 | 1 | 7 | 31 | 7 | 35 | 29 | 26 | 91 | 26 | 18 | 74 | 262 | 191 | 220 |
| XLRE/SPY | S | 2015-10-08 | 2026-10-14 | 2770 | 0 | 4 | 25 | 6 | 41 | 22 | 30 | 33 | 9 | 7 | 25 | 92 | 86 | 69 |
| XLU/SPY | S | 1998-12-22 | 2026-10-14 | 6995 | 1 | 7 | 34 | 7 | 33 | 31 | 30 | 93 | 25 | 22 | 79 | 212 | 156 | 219 |
| XLV/SPY | S | 1998-12-22 | 2026-10-14 | 6995 | 1 | 7 | 39 | 6 | 32 | 35 | 30 | 92 | 19 | 22 | 71 | 202 | 153 | 258 |
| XLY/SPY | S | 1998-12-22 | 2026-10-14 | 6995 | 1 | 7 | 43 | 6 | 28 | 38 | 32 | 93 | 20 | 13 | 75 | 160 | 136 | 324 |
| SMH/SPY | O | 2000-06-05 | 2026-10-14 | 6630 | 1 | 7 | 45 | 7 | 25 | 39 | 34 | 93 | 17 | 10 | 71 | 136 | 115 | 315 |
| XBI/SPY | O | 2006-02-06 | 2026-10-14 | 5205 | 0 | 5 | 41 | 7 | 25 | 38 | 29 | 68 | 18 | 9 | 53 | 113 | 100 | 199 |
| IWM/SPY | O | 2000-05-26 | 2026-10-14 | 6635 | 1 | 7 | 37 | 9 | 27 | 34 | 34 | 90 | 25 | 17 | 75 | 166 | 128 | 253 |
| RSP/SPY | O | 2003-05-01 | 2026-10-14 | 5902 | 0 | 5 | 39 | 6 | 30 | 35 | 31 | 70 | 13 | 16 | 57 | 149 | 116 | 263 |
| QQQ/SPY | O | 1999-03-10 | 2026-10-14 | 6943 | 1 | 7 | 48 | 6 | 25 | 44 | 30 | 72 | 16 | 10 | 76 | 123 | 127 | 367 |
| GLD/SPY | O | 2004-11-18 | 2026-10-14 | 5510 | 0 | 5 | 35 | 6 | 35 | 32 | 25 | 69 | 18 | 12 | 58 | 191 | 136 | 186 |
| TLT/SPY | O | 2002-07-30 | 2026-10-14 | 6092 | 0 | 5 | 23 | 6 | 43 | 22 | 25 | 77 | 20 | 13 | 66 | 264 | 210 | 141 |

## 4. Charts of every logged event (compare with TradingView)

Yellow band = the window logged by eye; purple circle = engine reclaim; red x = engine rule 3; orange dash = pivot high at its pivot bar.

- [reclaim_XLK_2026-04-06.png](diagnose/reclaim_XLK_2026-04-06.png)
- [reclaim_XLK_2026-09-08.png](diagnose/reclaim_XLK_2026-09-08.png)
- [reclaim_SMH_2026-09-08.png](diagnose/reclaim_SMH_2026-09-08.png)
- [reclaim_XLE_2026-01-08.png](diagnose/reclaim_XLE_2026-01-08.png)
- [reclaim_XLE_2026-07-20.png](diagnose/reclaim_XLE_2026-07-20.png)
- [reclaim_XLV_2026-03-18.png](diagnose/reclaim_XLV_2026-03-18.png)
- [reclaim_XLV_2026-06-08.png](diagnose/reclaim_XLV_2026-06-08.png)
- [reclaim_XLRE_2026-01-29.png](diagnose/reclaim_XLRE_2026-01-29.png)
- [reclaim_XLRE_2026-07-20.png](diagnose/reclaim_XLRE_2026-07-20.png)
- [reclaim_RSP_2025-12-01.png](diagnose/reclaim_RSP_2025-12-01.png)
- [reclaim_RSP_2026-06-08.png](diagnose/reclaim_RSP_2026-06-08.png)
- [reclaim_XLF_2025-12-15.png](diagnose/reclaim_XLF_2025-12-15.png)
- [reclaim_XLF_2026-06-08.png](diagnose/reclaim_XLF_2026-06-08.png)
- [reclaim_XLI_2025-12-29.png](diagnose/reclaim_XLI_2025-12-29.png)
- [reclaim_XLI_2026-06-18.png](diagnose/reclaim_XLI_2026-06-18.png)
- [reclaim_XLU_2026-01-20.png](diagnose/reclaim_XLU_2026-01-20.png)
- [reclaim_XLE_2021-12-27.png](diagnose/reclaim_XLE_2021-12-27.png)
- [reclaim_XLE_2022-08-22.png](diagnose/reclaim_XLE_2022-08-22.png)
- [reclaim_XLU_2021-11-29.png](diagnose/reclaim_XLU_2021-11-29.png)
- [reclaim_XLU_2022-08-08.png](diagnose/reclaim_XLU_2022-08-08.png)
- [reclaim_XLU_2022-11-28.png](diagnose/reclaim_XLU_2022-11-28.png)
- [reclaim_XLK_2022-07-18.png](diagnose/reclaim_XLK_2022-07-18.png)
- [r3_XLK_2026-06-15.png](diagnose/r3_XLK_2026-06-15.png)
- [r3_SMH_2026-06-15.png](diagnose/r3_SMH_2026-06-15.png)
- [r3_XLE_2026-04-01.png](diagnose/r3_XLE_2026-04-01.png)
- [r3_XLV_2026-03-25.png](diagnose/r3_XLV_2026-03-25.png)
- [r3_XLRE_2026-03-25.png](diagnose/r3_XLRE_2026-03-25.png)
- [r3_XLRE_2026-07-27.png](diagnose/r3_XLRE_2026-07-27.png)
- [r3_RSP_2026-03-20.png](diagnose/r3_RSP_2026-03-20.png)
- [r3_RSP_2026-08-31.png](diagnose/r3_RSP_2026-08-31.png)
- [r3_XLF_2026-01-15.png](diagnose/r3_XLF_2026-01-15.png)
- [r3_XLF_2026-09-04.png](diagnose/r3_XLF_2026-09-04.png)
- [r3_XLI_2026-03-30.png](diagnose/r3_XLI_2026-03-30.png)
- [r3_XLI_2026-07-27.png](diagnose/r3_XLI_2026-07-27.png)
- [r3_XLU_2026-04-01.png](diagnose/r3_XLU_2026-04-01.png)
- [r3_XLU_2026-08-03.png](diagnose/r3_XLU_2026-08-03.png)
- [r3_XLE_2021-11-08.png](diagnose/r3_XLE_2021-11-08.png)
- [r3_XLE_2022-06-20.png](diagnose/r3_XLE_2022-06-20.png)
- [r3_XLE_2022-12-01.png](diagnose/r3_XLE_2022-12-01.png)
- [r3_XLK_2021-12-27.png](diagnose/r3_XLK_2021-12-27.png)
- [r3_XLK_2022-08-22.png](diagnose/r3_XLK_2022-08-22.png)
- [r3_XLU_2022-07-11.png](diagnose/r3_XLU_2022-07-11.png)
- [r3_XLU_2022-10-03.png](diagnose/r3_XLU_2022-10-03.png)
