"""
Phase 3 — Cloud-masked BSI (Bare Soil Index) for PRE and POST, and dBSI.
BSI = [(B11+B04) - (B08+B02)] / [(B11+B04) + (B08+B02)]
High BSI = bare soil. Landslide -> BSI increases -> dBSI positive.
Complements dNDVI (which may miss already-bare areas).

B11 (20m) is resampled to 10m (bilinear, continuous).
Output: data/processed/cd/{pre,post}_bsi.tif, dbsi.tif
"""

import numpy as np
import rasterio
from rasterio.enums import Resampling
from pathlib import Path

CD = Path("data/processed/cd")
SCL_INVALID = {0, 1, 3, 8, 9, 10}

def read10(path):
    with rasterio.open(path) as src:
        return src.read(1).astype("float32"), src.profile

def read_resampled(path, out_shape, method):
    with rasterio.open(path) as src:
        return src.read(1, out_shape=out_shape, resampling=method).astype("float32")

def compute_bsi(tag):
    blue, profile = read10(CD / f"{tag}_B02.tif")
    red,  _       = read10(CD / f"{tag}_B04.tif")
    nir,  _       = read10(CD / f"{tag}_B08.tif")
    # B11 (SWIR, 20m) -> resample to 10m grid, bilinear (continuous)
    swir = read_resampled(CD / f"{tag}_B11.tif", blue.shape, Resampling.bilinear)
    # SCL (20m) -> 10m, nearest (categorical)
    scl  = read_resampled(CD / f"{tag}_SCL.tif", blue.shape, Resampling.nearest)
    valid = ~np.isin(scl.astype("int16"), list(SCL_INVALID))

    num = (swir + red) - (nir + blue)
    den = (swir + red) + (nir + blue)
    bsi = np.where(den != 0, num / den, np.nan)
    bsi = np.where(valid, bsi, np.nan)

    profile.update(dtype="float32", count=1, nodata=np.nan)
    with rasterio.open(CD / f"{tag}_bsi.tif", "w", **profile) as dst:
        dst.write(bsi.astype("float32"), 1)
    v = bsi[~np.isnan(bsi)]
    print(f"{tag} BSI: mean={v.mean():.3f} min={v.min():.3f} max={v.max():.3f}")
    return bsi, profile

def main():
    pre, profile = compute_bsi("pre")
    post, _ = compute_bsi("post")

    dbsi = post - pre
    with rasterio.open(CD / "dbsi.tif", "w", **profile) as dst:
        dst.write(dbsi.astype("float32"), 1)
    v = dbsi[~np.isnan(dbsi)]
    print(f"\ndBSI: mean={v.mean():.3f} min={v.min():.3f} max={v.max():.3f} std={v.std():.3f}")
    for thr in (0.2, 0.3, 0.4):
        n = (v > thr).sum()
        print(f"  pixels with dBSI > {thr}: {n} ({100*n/v.size:.2f}%)")

if __name__ == "__main__":
    main()