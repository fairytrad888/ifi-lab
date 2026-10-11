"""Synthetic OHLCV for pipeline smoke tests only (no market conclusions)."""
import numpy as np, pandas as pd, sys
from pathlib import Path
def make(seed, n=6500, start="2000-01-03"):
    rng = np.random.default_rng(seed)
    regime = np.repeat(rng.choice([-0.0006, 0.0002, 0.0008], size=n // 120 + 1), 120)[:n]
    r = regime + rng.normal(0, 0.012, n)
    c = 100 * np.exp(np.cumsum(r))
    o = c * np.exp(rng.normal(0, 0.004, n))
    h = np.maximum(o, c) * np.exp(np.abs(rng.normal(0, 0.006, n)))
    l = np.minimum(o, c) * np.exp(-np.abs(rng.normal(0, 0.006, n)))
    v = rng.integers(1_000_000, 5_000_000, n)
    idx = pd.bdate_range(start, periods=n)
    return pd.DataFrame(dict(open=o, high=h, low=l, close=c, volume=v), index=pd.Index(idx, name="date"))
if __name__ == "__main__":
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    for i, s in enumerate(["SPY","RSP","IWM","QQQ","SMH","XBI","XLB","XLC","XLE","XLF","XLI","XLK","XLP","XLRE","XLU","XLV","XLY"]):
        make(i).to_csv(out / f"{s}.csv")
