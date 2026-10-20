# IFI weekly accumulation alerts

Every Saturday the scan reads the S&P 1500 on weekly bars. It reports stocks with a **red IFI A&D accumulation bar
(washout) paired with at least one other bullish signal within 4 weeks**, while their sector or industry is **bullish or
basing**. It is a selection aid; the edge is not yet tested.

**Pairing signals:** Signals △, A&D ▲, Matrix ◆, a completed down-9, or the green accumulation bar.

**Change in v1.1 (Oct 19):** v1.0 waited for the green bar (washout exit), which usually prints after the low.

## Rules (`config.yaml`)
- **Group state:** each sector ETF (XLK, XLV, …) and industry ETF (SMH, IGV, XBI, KRE, XOP, ITB, XRT, …) is rated on its ratio to SPY, using the weekly IFI stage.
  - 2–3 = bullish; 1 = basing; 0 = neutral; −1 = bearish.
  - A stock uses its industry ETF when its GICS sub-industry has one, otherwise its sector ETF.
- **Arm and release:**
  - The paired signal arms the stock for 8 weeks, as long as weekly closes hold above the window's lowest low.
  - While armed and not yet released, the stop follows new lows inside the washout and more signals are added.
  - One alert is released when the group is bullish or basing: in the same week, or later when the group turns.
  - A weekly close below the low disarms the stock.
  - The same stock gets no second alert within 8 weeks.
- **Liquidity:** price ≥ $5 and ≥ $20M traded per day (20-day average).
- **Rank:** group state, sector breadth (share of members with accumulation in 8 weeks, share at stage ≥ 2), the stock's ratio to its ETF, the number of distinct pairing signals (confluence), and stop width. The top 10 are pushed.
- **Weeks:** a week counts from the Saturday after its Friday. There are never partial bars.

## Output (branch `weekscan-results`)
- **`LATEST.md`:** this week's ranked alerts, every group's state with changes and breadth, and stocks armed and waiting for their group.
- **`weeks/<friday>/`:**
  - `ALERTS.md`;
  - `alerts.csv`;
  - `groups.csv`;
  - `charts/<symbol>.png` (weekly IFI chart for each pushed alert).
- **`state.json`:** arm and release memory.
- **`alerts_log.csv` and `events.csv`:** every alert, arm, disarm and suppression, kept for a later Eye Lab test.

## Phone push
1. Install the free **ntfy** app and subscribe to a private topic name (a long random name; anyone who knows it can read it).
2. Add that name as a repository secret called `NTFY_TOPIC`.

Without the secret the scan still runs and writes its files; it just sends no push.

## Isolation
- It has its own copy of the IFI 2.0 indicator code (`core/`, sha-pinned) and no imports of `ifi`, `research` or `eyelab`.
- It has its own data downloads and its own Saturday 15:20 UTC schedule, outside the prior system's windows.
- It writes only to `weekscan-results`, never to the default branch. The workflow fails if the checkout changed.

## Commands
```
python -m weekscan.run --no-push           # local, writes to weekscan/_out
python weekscan/tests/test_weekscan.py
```
