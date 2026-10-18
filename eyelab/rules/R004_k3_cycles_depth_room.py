"""Ratio flip K3: >=2 down-9 cycles + deep WT1 + room to the key level. Separate pre-registered test. Primary: K3 lift on tier-2 events (one hypothesis, no correction).
Definitions, outcomes and cut points: eyelab/studies/ratio_flip.py (shared by R001-R004)."""

from eyelab.studies import ratio_flip as RF

STUDY = "ratio_flip"
PRIMARY = "o1_up9"         # an up-9 completes within 20 bars before a close below the event low

SPEC = {
    "id": "R004_k3_cycles_depth_room",
    "version": 1,
    "name": "Ratio flip K3: >=2 down-9 cycles + deep WT1 + room to the key level",
    "eye_description": "Ratio (ETF/SPY) in a downtrend. Bullish signals cluster: of IFI Signals trigger, A&D accumulation bar, A&D green triangle and Matrix divergence, 2 or 3 appear within 10 bars. Question: which extra condition makes the up-9 count complete (a true flip) more likely. Seen on XLU/SPY: June 2026 attempt failed at 0.06 (triangle #3 + RK+5 + accumulation); late-September flip after 2 down-9 cycles, accumulation group and triangle #1.",
    "timeframe": "D",
    "direction": "long",
    "status": "draft",
    "source": "screenshot XLU/SPY daily + verbal, Oct 18, 2026",
}
HYPOTHESES = [("K3", 2)]      # first = primary
SECONDARY = [("K3", 3), ("base", 2)]         # reported, not tested for the verdict
CARRY = "primary"


def blind_mask(x):
    """Events the blind review samples (and that your examples are matched against)."""
    return (x["e2"] | x["e3"]) & x["K3"]
