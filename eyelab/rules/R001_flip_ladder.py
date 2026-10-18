"""Ratio flip: confluence and the condition ladder (C1-C7). 16 pre-registered hypotheses, Holm across all; only those that pass discovery are locked and confirmed.
Definitions, outcomes and cut points: eyelab/studies/ratio_flip.py (shared by R001-R004)."""

from eyelab.studies import ratio_flip as RF

STUDY = "ratio_flip"
PRIMARY = "o1_up9"         # an up-9 completes within 20 bars before a close below the event low

SPEC = {
    "id": "R001_flip_ladder",
    "version": 1,
    "name": "Ratio flip: confluence and the condition ladder (C1-C7)",
    "eye_description": "Ratio (ETF/SPY) in a downtrend. Bullish signals cluster: of IFI Signals trigger, A&D accumulation bar, A&D green triangle and Matrix divergence, 2 or 3 appear within 10 bars. Question: which extra condition makes the up-9 count complete (a true flip) more likely. Seen on XLU/SPY: June 2026 attempt failed at 0.06 (triangle #3 + RK+5 + accumulation); late-September flip after 2 down-9 cycles, accumulation group and triangle #1.",
    "timeframe": "D",
    "direction": "long",
    "status": "draft",
    "source": "screenshot XLU/SPY daily + verbal, Oct 18, 2026",
}
HYPOTHESES = [("base", 2), ("base", 3)] + [(c, t) for c in RF.COND_TEXT for t in (2, 3)]      # first = primary
SECONDARY = []         # reported, not tested for the verdict
CARRY = "holm_pass"


def blind_mask(x):
    """Events the blind review samples (and that your examples are matched against)."""
    return x["e2"] | x["e3"]
