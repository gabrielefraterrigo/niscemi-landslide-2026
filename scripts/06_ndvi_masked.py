"""
Phase 3 — Cloud-masked NDVI for PRE and POST.
Uses the SCL band to mask clouds/shadows, then computes NDVI on
valid pixels only. SCL (20 m) is resampled to 10 m with NEAREST
(categorical data). NDVI is scale-invariant, so scaled DN are fine.

Output: data/processed/cd/{pre,post}_ndvi.tif
"""

import numpy as np
import rasterio
from rasterio.enums import Resampling
from pathlib import Path

CD = Path("data/processed/cd")

# SCL codes to EXCLUDE (clouds, shadows, defective, nodata)
SCL_INVALID = {0, 1, 3, 8, 9, 10}

def load_band(path):
    with rasterio.open(path) as src:
        return src.read(1).astype("float32"), src.profile

def load_scl_resampled(path, out_shape):
    """Read SCL and resample to 10 m grid (out_shape) with nearest."""
    with rasterio.open(path) as src:
        scl = src.read(
            1, out_shape=out_shape, resampling=Resampling.nearest
        )
    return scl

def compute_ndvi(tag):
    red, profile = load_band(CD / f"{tag}_B04.tif")   # 10 m
    nir, _       = load_band(CD / f"{tag}_B08.tif")   # 10 m

    # SCL resampled to the 10 m band shape (nearest = categorical)
    scl = load_scl_resampled(CD / f"{tag}_SCL.tif", red.shape)

    # Valid-pixel mask: True where NOT cloud/shadow/etc.
    valid = ~np.isin(scl, list(SCL_INVALID))

    # NDVI (scale factor cancels in the ratio)
    denom = nir + red
    ndvi = np.where(denom != 0, (nir - red) / denom, np.nan)

    # Apply cloud mask: invalid pixels -> NaN
    ndvi = np.where(valid, ndvi, np.nan)

    # Write out
    profile.update(dtype="float32", count=1, nodata=np.nan)
    out = CD / f"{tag}_ndvi.tif"
    with rasterio.open(out, "w", **profile) as dst:
        dst.write(ndvi.astype("float32"), 1)

    # Quick stats on valid pixels
    v = ndvi[~np.isnan(ndvi)]
    print(f"{tag}: NDVI mean={v.mean():.2f} min={v.min():.2f} "
          f"max={v.max():.2f}  (masked {100*(1-valid.mean()):.1f}% as cloud/shadow)")

def main():
    for tag in ("pre", "post"):
        compute_ndvi(tag)
    print("\nNDVI rasters written to", CD)

if __name__ == "__main__":
    main()