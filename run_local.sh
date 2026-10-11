#!/bin/bash
# Run the whole pipeline on your own computer (fallback if GitHub Actions is unavailable).
set -e
cd "$(dirname "$0")"
python3 -m venv .venv 2>/dev/null || true
source .venv/bin/activate
pip install -q -r requirements.txt
python tests/test_smoke.py
python -m ifi.update_data
if [ ! -f logs/events.csv ]; then python -m ifi.scan --backfill 250; else python -m ifi.scan; fi
python -m ifi.run_backtests --tf daily --universe etfs
python -m ifi.scan
echo "Done. Open docs/index.html and reports/."
