"""
Phase 3 — dNDVI (NDVI change): post - pre.
Strong negative dNDVI = vegetation/cover loss = candidate landslide.
Positive dNDVI = vegetation gain (seasonal growth, the 'noise').

Output: data/processed/cd/dndvi.tif
"""

import numpy as np
import rasterio
from pathlib import Path

CD = Path("data/processed/cd")

def main():
    with rasterio.open(CD / "pre_ndvi.tif") as src:
        pre = src.read(1)
        profile = src.profile
    with rasterio.open(CD / "post_ndvi.tif") as src:
        post = src.read(1)

    # Difference: NaN propagates where either date was masked
    dndvi = post - pre

    # Write out
    profile.update(dtype="float32", count=1, nodata=np.nan)
    out = CD / "dndvi.tif"
    with rasterio.open(out, "w", **profile) as dst:
        dst.write(dndvi.astype("float32"), 1)

    # Stats on valid pixels
    v = dndvi[~np.isnan(dndvi)]
    print(f"dNDVI: mean={v.mean():.3f}  min={v.min():.3f}  max={v.max():.3f}  std={v.std():.3f}")
    # How many pixels show a strong drop? (preview of thresholding)
    for thr in (-0.2, -0.3, -0.4):
        n = (v < thr).sum()
        print(f"  pixels with dNDVI < {thr}: {n}  ({100*n/v.size:.2f}% of valid)")

    print(f"\nWritten to {out}")

if __name__ == "__main__":
    main()