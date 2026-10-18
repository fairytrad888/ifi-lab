"""Demo rule for the self-test only (status 'demo': it can never be graded, locked or confirmed)."""

SPEC = {
    "id": "R000_demo",
    "version": 1,
    "name": "Demo: close crosses above a rising Trend line",
    "eye_description": "Not a hypothesis. Exercises the pipeline end to end.",
    "timeframe": "D",
    "direction": "long",
    "status": "demo",
}


def signal(x):
    above = x["close"] > x["tr_line"]
    return above & ~above.shift(1, fill_value=True) & x["tr_line_rising"]
