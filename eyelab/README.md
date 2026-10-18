# IFI Eye Lab v1

Turns eye-level chart signals into testable rules and measures their **process advantage**: does the rule's entry
beat matched random entries taken the same day, or on the same symbol, with the same risk geometry?

The prior system (IFI Lab v1.x: nightly scan, paper trades, ladder, research tests) is **frozen and keeps running
untouched**. Nothing here imports it, writes to it, or shares its schedule.

## Isolation

| Guarantee | How |
|---|---|
| No shared code | The IFI 2.0 indicator code is vendored byte-identical into `eyelab/core/` (pinned by `VENDOR.sha256`). The tests fail if any Eye Lab file imports `ifi` or `research`. |
| No shared data | The Eye Lab downloads and pins its own snapshots. It never reads `data/`, `logs/`, `state/` or `reports/`. |
| No shared writes | Output goes to `EYELAB_OUT` outside the checkout. The workflow pushes it to the branch `eyelab-results`, never to the default branch, so it can't race the nightly's push. |
| No shared schedule | Manual runs only, with their own concurrency group. Runs are refused inside the nightly, catch-up and Saturday backtest windows. |
| Proof | `FREEZE.sha256` hashes every prior file except the folders the prior system rewrites itself. Each run verifies it, and fails if the checkout changed in any way. |

## The pipeline (each step gates the next)

1. **Eye.** You show a signal as an annotated screenshot, a symbol + date list, or in words.
2. **Rule.** Claude writes `rules/R<NNN>_<name>.py` in your words (`SPEC.eye_description`), using only bars up to the signal bar.
3. **Fidelity (outcome-blind, dev pool).** Does the code see what your eye sees?
   - Measured as recall and specificity against your labelled examples, plus your verdict on blind charts of its hits. Blind charts hide the ticker, dates and prices.
   - A look-ahead test is also required.
   - No outcome is computed: the engine refuses in blind mode.
   - The charts you learned from (dev pool) are never graded.
4. **Discovery (pool A: 269 symbols, outcomes measured).**
   - First-passage and forward metrics against cross and time nulls, with month-clustered bootstrap.
   - Splits by time half, SPY regime and ETF vs stock.
   - Every version is a counted variant in the ledger.
5. **Lock.** Fingerprints the rule file, the Eye Lab code + config + pools, and pool B's manifest, together with the pre-registered pass rule.
6. **Confirmation (pool B: 194 sealed symbols, opened once per rule version).** The opening is recorded before any read.
   - Pass rule (`config.yaml` → `primary`): the 95% lower bound of fp1 advantage vs the cross null > 0, the time-null advantage > 0, and positive in both halves.
7. **Book.** Only a confirmed rule goes on to a book test against SPY and the SPY 200-day trend rule.

**Why first passage.** P(+1u before −1u) is a yes/no outcome with about a tenth of the variance of trade R, so the same number of signals measures it far more precisely. Matched nulls remove market drift, which was most of the prior system's apparent edge.

## Pools

| Pool | Symbols | Role |
|---|---|---|
| dev | the 78 core symbols you chart | fidelity only, never graded |
| A | 92 extended (sealed set 1) + 177 new (269) | discovery |
| B | 194 new | confirmation, sealed |
| ex | symbols from your examples outside the pools | fidelity only |

- New stocks and the first 20 new ETFs were split into A or B by `sha256(ticker)` (even or odd first byte). The 67 equity ETFs added for ratio studies were sorted by `sha256(ticker)` within each class (industry, country) and dealt alternately to B and A, so both pools get half of each class. Nobody chose a symbol's pool.
- `pools/etf_classes.csv` tags each ETF as sector, industry, country, broad, bond or commodity.
- An example symbol that sits in A or B is excluded from grading that rule, because your eye has seen it.

## Event studies (ratio flips: R001–R004)

A rule can be a **study** (`STUDY = "ratio_flip"`): events on ETF/SPY ratios, with structural outcomes and pre-registered condition lifts. The shared definitions live in `studies/ratio_flip.py`.

- **Events:** 2 or 3 of the 4 bullish signal types within 10 bars, on a downtrending ratio.
- **Outcomes:** the primary is an up-9 completing before the event low breaks. Also measured: a close above the last lower high, and +k ATR ladders on the ratio and the ETF itself.
- **Nulls:** a context null (random days of the same ratio in the same downtrend) and a cross null.
- **Lifts:** each with and without a condition, with Holm across the test's hypotheses.
- **Jitter check:** a ±0.01% price jitter shows whether a tiny data difference changes an event or a condition.

R001 tests the ladder (C1–C7). R002–R004 are three separate pre-registered combo tests (K1, K2, K3), each with its own lock and its own opening of pool B.

## Commands

```
python -m eyelab.run selftest
python -m eyelab.run build-data --pools bench,dev,A,B --tf D
python -m eyelab.run fidelity  --rule R001_x
python -m eyelab.run discovery --rule R001_x
python -m eyelab.run lock      --rule R001_x
python -m eyelab.run confirm   --rule R001_x
python eyelab/tests/test_eyelab.py
```

In GitHub, use **Actions → Eye Lab → Run workflow** (stage, rule). Results go to the `eyelab-results` branch: `LEDGER.csv`, `fidelity/`, `discovery/`, `locks/`, `confirm/` and `data/`.

**Working rule for Claude:**
- Fidelity iterations may run locally, from the pinned dev snapshot on `eyelab-results`, because they compute no outcomes.
- Anything that computes outcomes runs only through the workflow, so the ledger sees it.
