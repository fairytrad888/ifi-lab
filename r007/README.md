# R007: confluence ladder for sizing

Pre-registered study (Oct 22, 2026): among weekly accumulation events (a red A&D bar paired with another bullish
signal, as the live weekly scan), do IFI tags sort events into tiers whose outcomes differ enough to size by?
The comparison is between events of the same week. Design: project doc `IFI_R007_Confluence_Ladder_Design.md`;
definitions and thresholds: `prereg_r007.yaml` (locked by `PREREG.lock`).

**This deploy is Phase 0 only.** No outcome can be computed: `guard.OPEN_PHASES` is empty and `outcomes.trade`
refuses real data. Phases 1, 2, 3 and E each need their own deploy and an explicit go.

## Isolation
- Own folder (`r007/`), own workflow (`.github/workflows/r007.yml`, manual only), own results branch `r007-results`.
- Reads `weekscan-results` (never writes it) and imports `weekscan` read-only. Never imports the prior Lab
  (`ifi`, `research`) or the Eye Lab; `python -m eyelab.freeze verify` must stay OK before and after a run.
- Writes only under `R007_OUT` (outside the checkout in Actions). The workflow fails if the checkout changes.
- Refuses to start when a run could reach a prior-system or weekly-scan window (`config.yaml guard_windows_utc`).
- The lock covers the pre-registration, the R007 method code and the weekscan files R007 reuses. If weekscan
  changes later, R007 stops until the change is handled as a recorded deviation.

## Phase 0 (`Actions → R007 confluence ladder → Run workflow → phase0`)
1. Live reference: the first `weekscan-results` commit with state v2 for the week ending 2026-10-16. Its
   `universe.csv` is the R007 universe; its `state.json` is the parity target.
2. Symbol sets S1 40% / S2 40% / S3 15% / E 5% by a fixed hash deal within each GICS sector. Excluded: the 61 Lab
   stocks and the 54 sealed-set-1 stocks (X), and second share classes (XD).
3. Snapshot: Yahoo daily bars 2003-01-01 to 2026-10-21, downloaded once, committed with a sha256 manifest in its
   own commit, never refreshed. SPY and every group ETF are required.
4. Events and features for 2008-01-04 to 2026-03-27 (no outcomes): `events/<set>.csv.gz`.
5. Checks: look-ahead truncation, fidelity to weekscan code on real data, live parity, synthetic power.
6. Report: `PHASE0.md`, `PHASE0.json`, `LEDGER.md` on `r007-results`.

## Files
`prereg_r007.yaml` definitions · `config.yaml` paths and guards · `guard.py` isolation, lock, outcome guard ·
`data.py` snapshot · `sets.py` symbol sets · `events.py` events and features · `outcomes.py` trade outcomes (locked,
closed) · `metric.py` within-week spread, bootstrap, Holm · `power.py` synthetic power · `lookahead.py` truncation and
fidelity · `parity.py` live reference and parity · `phase0.py` orchestration and report · `run.py` CLI ·
`tests/test_r007.py` synthetic tests.
