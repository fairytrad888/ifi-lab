# IFI Process: priorities, routine, decision rules

## The principle
Find out what works as fast as possible, decide by rules written in advance, and let the machine do the repetitive work.

## Priority queue (fixed order)

| # | Question | How it's answered | Why this order |
|---|---|---|---|
| **P1** | **Which exits and sizing turn IFI entries into positive expectancy?** | 6 setups × 7 exit rules on 17 ETFs (since 2000) and ~60 stocks, against random entries with the same exits | Exits and sizing set the size of wins and losses directly; the biggest lever |
| **P2** | **When should you not trade?** | Same trades split by market regime (SPY above its 200-day average and Trend line rising) | Skipping bad conditions often adds more than better entries |
| **P3** | **Do catalysts add real information?** | Positive earnings gaps alone (20-bar drift vs SPY), and IFI setups shortly after them | The only input that isn't price |
| **P4** | **How much risk at once?** | Same trades with and without a one-position-per-sector cap | Correlated positions are one bet |
| P5 | Does 4H timing add anything over Daily? | P1 repeated on 4H bars (about 2 years of data) | Short history, so secondary |

## Setups and exits under test (frozen)

**Setups (signal on the close, fill at the next open):**
- **E1:** Signals bullish trigger *with* trend (above a rising 200-bar average)
- **E1b:** the same trigger *against* trend
- **E2:** washout exit and a completed down-9 within 3 bars (exhaustion confluence)
- **E3:** move into stage 2 after 5+ bars below, with a higher low
- **E4:** anchor reclaim (close crosses above an anchor that was resistance)
- **E5:** checklist score reaches 4

**Stop:** lowest low of the last 5 bars − 0.5 ATR. **1R** = entry − stop.

**Exits:**
- **X1:** time, 10 bars
- **X2:** 2R target
- **X3:** 3R target
- **X4:** trail with the Trend line
- **X5:** chandelier, 3 ATR
- **X6:** half off at 1R, rest trailed by the Trend line
- **X7:** stage-drop exit

**Costs:** 0.05% per side for ETFs, 0.10% for stocks.

## Decision rules (pre-registered)

| Verdict | Meaning | Action |
|---|---|---|
| **ADOPT** | At least 100 trades; bootstrap 95% CI above 0 after correcting for the 42 tests; positive in both time halves (before/after 2015) and both symbol halves; better than random entries with the same exits | Trade it at full risk (1%) |
| **PROMISING** | Everything except significance | Trade at half risk; review after 20 live trades |
| **UNSTABLE** | Fails a split half | Paper only |
| **REJECT** | Not positive, or no better than random | Drop it |

**Live kill switch:** after 20 live trades in a setup, if journal expectancy is below 0 **and** below the backtest's CI lower bound, stop trading it and investigate.

## Routine

**The loop (automatic, v1.3):** signal → paper trade (exact backtest rules) → scoreboard vs backtest → status → alert on change. Saturday backtests feed the drift check. Your journal is matched to the signals.

**Each evening (5 minutes, after the board updates around 6:30 pm ET):**
1. Check the regime line at the top of the board for context only. Round 1 (P2) found no reliable benefit from skipping or shrinking trades in "caution" regimes, so size stays constant.
2. Look at alerts and the Sector Board for stage 2–3 names with fresh events.
3. Only act on setups with an ADOPT or PROMISING verdict. Confirm on the TradingView 4H chart.
4. Enter with the logged stop and share size. Add the trade to the journal sheet.

**Saturday (20 minutes):**
1. Backtests rerun automatically. Check the **Scoreboard** and any **drift banner** first. Then read `SUMMARY_*.md`, or ask Claude to review the repo.
   - **ON TRACK:** keep trading.
   - **WATCH:** halve risk on that setup.
   - **STOP or drift:** pause that setup and bring it to Claude.
2. Check the rotation map and update the watchlist in `config.yaml` (leading and improving sectors, plus their power names).
3. Compare the event statistics and journal against the backtest verdicts.

**Monthly:** a CPI or Fed review using the pre-event baseline and post-event comparison (the October template in the IFI project).

## Round 1 decisions (engine v1.1 rerun, Oct 12, 2026)
**Adoption rule added:** a setup/exit pair joins the playbook only if it is ADOPT on **both** ETFs and stocks (two-universe replication).

| Pair | ETFs (edge over random) | Stocks (edge over random) | Status |
|---|---|---|---|
| **E4 anchor reclaim + 3R** | +0.324R (+0.18), n=885 | +0.281R (+0.14), n=3157 | **Playbook: primary** |
| **E1 with-trend trigger + 3R** | +0.410R (+0.26), n=135 | +0.324R (+0.18), n=522 | **Playbook: secondary (rare)** |
| E4 + 2R / stage-drop / trail | ADOPT both, smaller edges | ADOPT both | Allowed alternatives, not used (one exit keeps it simple) |
| E5 score ≥4 + 2R | +0.08 edge | +0.06 edge | Dropped: small edge, overlaps E4 |
| E1b counter-trend + chandelier | ADOPT | REJECT | Not replicated |
| E2 exhaustion, E3 stage-2 | REJECT / stock-only | — | Context only |

- **Exit:** one rule. Stop = 5-bar low − 0.5 ATR; target = 3R; skip if the next open is below the 5-bar low.
- **Risk:** 0.75% per trade. Over half of 3R trades lose (median ≈ −1R), and losing streaks of 8–14 are normal.
- **Limits:** one open position per symbol and per sector, max 5 open. **No regime filter** (P2 found no effect).
- **4H:** counter-trend triggers + 3R or chandelier look promising (+0.38R, n≈150) but there are only 3 years of data. Watch only; rerun quarterly.

## Roadmap

| Week | Milestone | Done when |
|---|---|---|
| 1 | Infrastructure live; P1 + P2 on ETFs and stocks | First SUMMARY reports exist; dashboard online |
| 2 | P3 earnings drift; first adopted setup/exit pair traded at defined risk | Verdict table reviewed with Claude |
| 3 | P4 portfolio heat + P5 4H | Sizing and heat rules fixed |
| 4+ | Live log vs backtest; IFI 2.0 Pine scripts for chart reading | Live results within the backtest's CI |

## What to change, and what not to

- **Change freely:** the watchlist, the account size, alert choices.
- **Change only with a new pre-registered test:** setups, exits, stop rule, costs, split date. Add new ideas as new setups (E6, E7…) rather than editing existing ones, so earlier results stay comparable.
