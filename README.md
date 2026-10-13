# IFI Lab

The IFI indicator set, rebuilt in Python, running itself every night for free on GitHub.

| Runs automatically | When | Output |
|---|---|---|
| Data refresh (Yahoo Finance) | Weeknights 22:15 UTC | Daily + 4H bars, earnings dates |
| Scan of your watchlist (Daily + 4H) | Weeknights | New events added to `logs/events.csv` with stop and share size |
| Outcome tracking | Weeknights | Each logged event gets its 5- and 10-bar result vs SPY, in R |
| **Forward test** | Weeknights | Every Daily playbook signal is paper-traded with the exact backtest rules (`logs/paper_trades.csv`) |
| **Scoreboard** | Weeknights | Live results per setup vs the backtest: ON TRACK / WATCH / STOP (`logs/scoreboard.json`) |
| **Drift check** | After each backtest run | Flags and alerts if a playbook setup loses ADOPT on either universe (`state/drift.json`) |
| **Execution check** | Weeknights | Journal trades matched to signals: signals taken, entry slippage and result gap in R |
| Dashboard | Weeknights | `docs/index.html`: Sector Board, rotation map, events, statistics, journal |
| Phone alerts (optional) | Weeknights | Push via ntfy.sh for the events you choose |
| Backtest queue | Saturdays, or on demand | `reports/SUMMARY_*.md` with ADOPT / PROMISING / REJECT verdicts |

Everything is free: GitHub (public repo), GitHub Actions, GitHub Pages, Yahoo Finance via `yfinance`, ntfy.sh, and Google Sheets for the journal.

---

## Setup (about 10 minutes, once)

1. **Create the repository.** On github.com: **New repository** → name `ifi-lab` → **Public** → Create.
   *Public gives unlimited free Actions minutes and a free dashboard page, and it lets Claude read the results. It contains tickers and statistics only, no personal data.*
2. **Upload the files.** Unzip `ifi-lab.zip`. On a Mac, press **Cmd + Shift + .** in Finder so the hidden `.github` folder shows.
   In the repo: **Add file → Upload files** → drag in **everything inside** the folder → **Commit changes**.
3. **Let the robot write results.** **Settings → Actions → General → Workflow permissions → Read and write** → Save.
4. **Turn on the dashboard.** **Settings → Pages → Build and deployment → Deploy from a branch → `main` / `/docs`** → Save.
   Your board will be at `https://<your-username>.github.io/ifi-lab/`.
5. **First run.** **Actions → Nightly scan → Run workflow.** The first run downloads data and **backfills the log with the last 250 bars of events**, so statistics exist from day one.
6. **First backtests.** **Actions → Backtests → Run workflow** three times: `etfs/daily`, `stocks/daily`, `etfs/h4`.
   (After that they run automatically every Saturday.)
7. **Tell Claude the repo URL.** Claude clones it, reads the reports, and proposes the next round.

### Optional
- **Phone alerts:** install the free **ntfy** app → subscribe to a long random topic name (e.g. `ifi-7f3k9q2x`).
  In GitHub: **Settings → Secrets and variables → Actions → New repository secret** → name `NTFY_TOPIC`, value = that topic.
- **Trade journal:** copy `journal_template.csv` into a Google Sheet → **File → Share → Publish to web → (that sheet) → CSV** → copy the link into `config.yaml` → `journal.trades_csv_url`.
  Every night your real expectancy (R), win rate and per-setup results appear on the board.
- **Give Claude write access:** connect this repository to your Claude session (GitHub access) so changes are pushed directly instead of uploaded by hand.

### Run on your Mac instead (fallback)
```bash
cd ifi-lab && ./run_local.sh            # installs, downloads data, scans, runs the ETF backtests
open docs/index.html
```

---

## What's inside

| File | Purpose |
|---|---|
| `ifi/pine.py` | Pine Script functions (ema, rma, rsi, stoch, linreg, pivots, anchored VWAP) reproduced exactly |
| `ifi/indicators.py` | IFI A&D, Signals, Matrix, Trend, Chips range line; 2.0 fixes behind flags |
| `ifi/states.py` | The 0–5 checklist, stage ladder, volume by session slot, relative strength, rotation quadrant |
| `ifi/backtest.py` | Setups (entries), exit rules, trade simulator, metrics, portfolio sizing, verdict rule |
| `ifi/run_backtests.py` | The pre-registered experiment queue (P1–P4) and report writer |
| `ifi/scan.py` | Nightly scan, event log, outcomes, journal stats, alerts |
| `ifi/dashboard.py` | The static dashboard |
| `config.yaml` | Universe, watchlist, costs, risk, alert and journal settings |
| `PROCESS.md` | The operating routine, priorities and decision rules |
| `ifi/forward.py` | Paper trades, scoreboard, drift check, journal matching, change alerts |
| `tests/test_smoke.py` | Parity with TradingView (golden values), indicator sanity, random-walk look-ahead check. Runs before every backtest. |
