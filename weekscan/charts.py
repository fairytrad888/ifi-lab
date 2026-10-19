"""Charts for the eye: the IFI reading drawn the way it looks on TradingView, with no future bars.

blind=True hides the ticker, the dates and the price scale, so memory of what happened next cannot steer the
review. The chart key (id -> symbol, date) is written separately.
Panels: price (candles, Trend line, anchor, stage strip, washout exits, completed 9s, signal arrow) | Signals WT1/WT2
(△n triggers, ◆ Matrix divergence) | A&D flow (green bars = accumulation / washout exit, ▲ = bullish divergence).
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

STAGE_COLORS = {3: "#1a9850", 2: "#91cf60", 1: "#d9ef8b", 0: "#e0e0e0", -1: "#d73027"}


def render(x: pd.DataFrame, i_signal: int, path: Path, bars: int = 120, blind: bool = True, title: str = "",
           marks: list[int] | None = None, after: int = 0) -> Path:
    """Draw bars [i_signal-bars+1, i_signal+after]. `after` > 0 only for non-blind example checks."""
    lo = max(0, i_signal - bars + 1)
    v = x.iloc[lo:i_signal + 1 + after]
    n = len(v)
    xs = np.arange(n)
    fig, (a1, a2, a3) = plt.subplots(3, 1, figsize=(9, 6.2), sharex=True,
                                     gridspec_kw={"height_ratios": [3.2, 1, 1]})
    o, h, l, c = (v[k].to_numpy() for k in ("open", "high", "low", "close"))
    up = c >= o
    a1.vlines(xs, l, h, color=np.where(up, "#26a69a", "#ef5350"), linewidth=0.8)
    a1.bar(xs, np.abs(c - o) + 1e-12, bottom=np.minimum(o, c), color=np.where(up, "#26a69a", "#ef5350"), width=0.7)
    if "tr_line" in v:
        a1.plot(xs, v["tr_line"].to_numpy(), color="#2962ff", linewidth=1.3, label="Trend line")
    if "tr_anchor" in v:
        sup = v["tr_anchor_is_support"].to_numpy(bool) if "tr_anchor_is_support" in v else np.ones(n, bool)
        an = v["tr_anchor"].to_numpy()
        a1.plot(xs, np.where(sup, an, np.nan), color="#00897b", linewidth=1.1, linestyle="--", label="Anchor (support)")
        a1.plot(xs, np.where(~sup, an, np.nan), color="#c62828", linewidth=1.1, linestyle="--", label="Anchor (resistance)")
    ymin, ymax = np.nanmin(l), np.nanmax(h)
    pad = (ymax - ymin) * 0.06
    if "stage" in v:
        st = v["stage"].to_numpy()
        for k in range(n):
            a1.add_patch(plt.Rectangle((k - 0.5, ymin - pad), 1, pad * 0.6, color=STAGE_COLORS.get(int(st[k]), "#e0e0e0"),
                                       linewidth=0))
    if "ad_washout_exit" in v:
        we = np.flatnonzero(v["ad_washout_exit"].to_numpy(bool))
        a1.scatter(we, l[we] - pad * 0.15, marker="^", s=18, color="#7b1fa2", zorder=5, label="Washout exit")
    if "tr_nine" in v:
        nine = v["tr_nine"].to_numpy()
        for k in np.flatnonzero(nine == -1):
            a1.annotate("9", (k, l[k] - pad * 0.45), fontsize=7, color="#d32f2f", ha="center", weight="bold")
        for k in np.flatnonzero(nine == 1):
            a1.annotate("9", (k, h[k] + pad * 0.15), fontsize=7, color="#2e7d32", ha="center", weight="bold")
    sig_k = i_signal - lo
    a1.annotate("", xy=(sig_k, l[sig_k] - pad * 0.3), xytext=(sig_k, l[sig_k] - pad * 1.6),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=1.6))
    for m in marks or []:
        if lo <= m <= lo + n - 1:
            a1.axvline(m - lo, color="#ff9800", linewidth=0.8, alpha=0.7)
    if after:
        a1.axvspan(sig_k + 0.5, n - 0.5, color="#fff3e0", alpha=0.6, zorder=0)
    a1.set_ylim(ymin - pad * 1.8, ymax + pad)
    a1.legend(loc="upper left", fontsize=7, frameon=False, ncol=4)
    if "sig_wt1" in v:
        a2.plot(xs, v["sig_wt1"].to_numpy(), color="#26a69a", linewidth=1)
        a2.plot(xs, v["sig_wt2"].to_numpy(), color="#ef5350", linewidth=1)
        for y in (60, -50, 0):
            a2.axhline(y, color="#9e9e9e", linewidth=0.6, linestyle=":")
        tb = np.flatnonzero(v["sig_trig_bull"].to_numpy(bool))
        a2.scatter(tb, v["sig_wt1"].to_numpy()[tb], s=14, color="#26a69a", zorder=5)
        if "sig_bull_streak" in v:
            for k in tb:
                a2.annotate(f"△{int(v['sig_bull_streak'].iloc[k])}", (k, v["sig_wt1"].iloc[k] - 14), fontsize=6,
                            color="#26a69a", ha="center")
        if "mx_strong_bull" in v:
            md = np.flatnonzero(v["mx_strong_bull"].to_numpy(bool))
            a2.scatter(md, np.full(len(md), -92.0), marker="D", s=14, color="#26a69a", zorder=5, label="Matrix ◆")
        a2.set_ylabel("Signals", fontsize=7)
    if "ad_flow" in v:
        a3.plot(xs, v["ad_flow"].to_numpy(), color="#5e35b1", linewidth=1)
        for y in (2.3, 50):
            a3.axhline(y, color="#9e9e9e", linewidth=0.6, linestyle=":")
        if "ad_washout_exit" in v:
            we = np.flatnonzero(v["ad_washout_exit"].to_numpy(bool))
            a3.vlines(we, 0, 100, color="#26a69a", linewidth=2.2, alpha=0.8)
        if "ad_bull_div" in v:
            bd = np.flatnonzero(v["ad_bull_div"].to_numpy(bool))
            a3.scatter(bd, np.full(len(bd), -2.0), marker="^", s=22, color="#26a69a", zorder=5)
        a3.set_ylim(-5, 105)
        a3.set_ylabel("A&D flow", fontsize=7)
    if blind:
        a1.set_yticklabels([])
        a3.set_xticks([0, n - 1 - after])
        a3.set_xticklabels([f"-{n - 1 - after}", "signal"])
    else:
        ticks = np.linspace(0, n - 1, 6).astype(int)
        a3.set_xticks(ticks)
        a3.set_xticklabels([str(v.index[t])[:10] for t in ticks], fontsize=7)
    a1.set_title(title, fontsize=9, loc="left")
    for a in (a1, a2, a3):
        a.tick_params(labelsize=7)
        a.grid(alpha=0.15)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=90)
    plt.close(fig)
    return path


def sheet(paths: list[Path], out: Path, cols: int = 3) -> Path:
    """Tile chart PNGs into one contact sheet (9 per sheet reads well on a phone)."""
    from PIL import Image

    ims = [Image.open(p) for p in paths]
    if not ims:
        return out
    w, h = ims[0].size
    rows = (len(ims) + cols - 1) // cols
    canvas = Image.new("RGB", (w * cols, h * rows), "white")
    for k, im in enumerate(ims):
        canvas.paste(im, ((k % cols) * w, (k // cols) * h))
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, optimize=True)
    return out
