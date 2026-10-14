# Research gates (Step 0 and Step 1)

Pre-registered tests of the IFI ratio rules v2.1, run on a **Daily ratio of each ETF to SPY**. Every rule, threshold and pass rule was fixed in `prereg_v21.yaml` before any result existed. The file's SHA-256 is stored in `PREREG.lock`, and the runner refuses to start if they differ.

## How to run
Use **Actions → Research → Run workflow**:

| Input | Meaning |
|---|---|
| `step` | `all` (default): Step 0, then Step 1 gated by Step 0. Or `step0`, or `step1` (needs an earlier Step 0 result) |
| `refresh_data` | Off: reuse the committed frozen snapshot. On: download a new one. The first run creates it automatically |

All results are written to `reports/research/`:
- `STEP0.md` and `STEP1.md` (the reports);
- CSV tables;
- `STEP0_gate.json` and `STEP1_meta.json`;
- `audit/*.png` (event audit sheets).

## Order of operations (`research/run.py`)
Every check aborts the run before the real result it protects is produced.

1. **Lock:** `prereg_v21.yaml`, `fixtures_scan.yaml`, every research module and the indicator modules they use (`ifi/pine.py`, `indicators.py`, `states.py`, `data.py`) must match `PREREG.lock`.
2. **Look-ahead check:** every event is recomputed on data cut at three points. Each event dated before the cut must be identical to the full-history run.
3. **Frozen data snapshot:** `research/snapshot/` holds gzip CSVs plus a sha256 manifest, from Yahoo via yfinance, split-adjusted like TradingView, trimmed to the last completed session. Only a Yahoo-sourced snapshot is accepted.
4. **Step 0:** first on random walks, where it must find nothing. Then on real data: does the Daily ratio state carry information at all? Writes `STEP0_gate.json`, stamped with the snapshot and lock.
5. **Step 1 gate:** Step 0 must come from the same snapshot and lock. If Step 0 found nothing (STOP), Step 1 does not run.
6. **Step 1 synthetic checks:**
   - On random walks, 0 PASS across all 7 comparisons.
   - On planted trend persistence, T1 and T3 must detect it. T2, T5 and T6 have no planted effect and should not pass.
7. **Step 1 on real data:** only the tests whose Step 0 prerequisite passed.

## Step 1 tests (7 primary comparisons, Bonferroni k = 7)

| Test | Question | Compared | Measure |
|---|---|---|---|
| T1 | Does a tier A floor + anchor reclaim start a relative leg? | Tier A entries vs all ratio-days | 40-bar peer-relative return |
| T2 | Does the bullish divergence add? | Tier A vs tier B entries | Same |
| T3 | Does rule 3 confirmation predict further relative decline? | Confirmations vs all ratio-days | 20-bar, expected negative |
| T4a | Does the structural exit beat 3R? | X-A vs X-3R on the same trades | Paired R |
| T4b | Does the fast exit beat 3R? | X-B vs X-3R on the same trades | Paired R |
| T5 | Is the line support in a rising trend more than in a flat range? | First touches, rising vs flat line | 20-bar peer-relative return |
| T6 | Do entries do better when macro favours the sector? | M > 0 vs M ≤ 0 (cross-fitted halves) | 40-bar peer-relative return |

**Pass rules:**
- Enough events.
- A Bonferroni-adjusted bootstrap CI (3-calendar-month blocks) that excludes 0 in the expected direction.
- The same sign in both time halves (2000–14 / 2015–) and both groups (sectors / others).
- The same sign at every neighbouring threshold.
- For T4: no loss of R per 100 bars held.

**Verdicts:**
- **TRADEABLE:** the numerator ETF's own price confirms the result. Otherwise **CONTEXT**.
- **FRAGILE:** a neighbouring threshold flips the sign.
- **OPPOSITE:** significant in the wrong direction.
- **INSUFFICIENT:** too few events.

**Validity:** each run also checks:
- that the engine finds the scan's eye-logged events (`fixtures_scan.yaml`, at least 80%);
- TradingView parity against screenshot values (at least 90% within 1.5%).

If either falls short, the run is marked **PROVISIONAL** and must be reviewed before acting.

## Files
| File | Role |
|---|---|
| `prereg_v21.yaml`, `PREREG.lock` | Locked definitions, thresholds, pass rules and decisions |
| `engine.py` | Event engine: floors, reclaims, rule 3, warnings, 9-count context, touches, trade simulation |
| `step1.py` | Tests, sensitivity, verdicts, report, audit sheets |
| `step0.py` | Step 0 gate (P1–P7) |
| `common.py` | Lock, snapshot, ratio bars, calendar-block bootstrap |
| `checks.py`, `synthetic.py` | Look-ahead check and synthetic markets |
| `fixtures_scan.yaml` | Definition audit and parity fixtures |
| `run.py` | The runner |
| `../tests/test_research.py` | Unit tests |

**Changing a definition after results are seen** needs a new version: a new `prereg_v22.yaml` and a new lock (`python -m research.common --write-lock`), visible in git history. Never edit v2.1 in place.

**Python versions:** the workflow pins pandas 3.0.6, numpy 2.5.4, scipy 1.18.1, matplotlib 3.11.2 and yfinance 1.7.0, the versions the code was validated with. The report header records them.
