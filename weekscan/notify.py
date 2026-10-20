"""Phone push through ntfy (https://ntfy.sh). The topic is a repository secret (NTFY_TOPIC); without it, nothing is sent."""
from __future__ import annotations

import os


def message(week: str, alerts: list[dict], n_total: int, groups_ok: int, groups_all: int) -> tuple[str, str]:
    title = f"IFI weekly {week}: {n_total} alert{'s' if n_total != 1 else ''} · {groups_ok}/{groups_all} groups bullish or basing"
    if not alerts:
        return title, "No weekly accumulation released this week."
    lines = []
    for k, a in enumerate(alerts, 1):
        from .scan import PAIR_LABEL
        tags = " red+" + "+".join(PAIR_LABEL.get(k, k) for k in a.get("signals", [])) + \
            (" ⚠earnings" if a.get("earnings_soon") else "")
        lines.append(f"{k}. {a['symbol']} ({a['group']} {a['group_state']}) close {a['close']:.2f} "
                     f"stop<{a['acc_low']:.2f} ({a['stop_pct']:.0%}){tags}")
    if n_total > len(alerts):
        lines.append(f"+{n_total - len(alerts)} more in the weekly file")
    return title, "\n".join(lines)


def push(title: str, body: str, click: str | None = None) -> str:
    topic = os.environ.get("NTFY_TOPIC", "").strip()
    if not topic:
        return "push skipped: NTFY_TOPIC not set"
    import requests

    payload = {"topic": topic, "title": title, "message": body[:3900], "tags": ["chart_with_upwards_trend"]}
    if click:
        payload["click"] = click
    r = requests.post("https://ntfy.sh/", json=payload, timeout=30)      # JSON publish: UTF-8 title and body
    return f"push sent: HTTP {r.status_code}"
