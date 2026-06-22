"""
Phase 3 — Extract and clip Sentinel-2 bands to the event AOI.
Finds each band inside the .SAFE via glob (robust to the long
GRANULE path), clips it to aoi_event, and saves to data/processed/cd/.

Bands: B02 (blue), B04 (red), B08 (NIR) @10m; B11, B12 (SWIR), SCL @20m.
Output naming: <pre|post>_<band>.tif  (e.g. pre_B04.tif)
"""

import geopandas as gpd
import rasterio
from rasterio.mask import mask
from pathlib import Path

# --- Two SAFE products (adjust folder names if needed) ---
SAFE = {
    "pre":  next(Path("data/raw").glob("S2B_MSIL2A_20251227*.SAFE")),
    "post": next(Path("data/raw").glob("S2B_MSIL2A_20260225*.SAFE")),
}

# Bands to extract, with their resolution subfolder
BANDS_10M = ["B02", "B04", "B08"]
BANDS_20M = ["B11", "B12", "SCL"]

GPKG = Path("data/processed/aoi.gpkg")
AOI_LAYER = "aoi_event"
OUT_DIR = Path("data/processed/cd")

def find_band(safe: Path, band: str, res: str) -> Path:
    """Locate a band .jp2 inside a .SAFE via glob pattern."""
    pattern = f"**/R{res}/*_{band}_{res}.jp2"
    matches = list(safe.glob(pattern))
    if len(matches) != 1:
        raise FileNotFoundError(f"{band}@{res}: found {len(matches)} matches in {safe.name}")
    return matches[0]

def clip_band(src_path: Path, aoi, out_path: Path):
    """Clip a raster to the AOI polygon and save."""
    with rasterio.open(src_path) as src:
        # AOI must be in the raster's CRS
        aoi_proj = aoi.to_crs(src.crs)
        geom = [aoi_proj.geometry.iloc[0].__geo_interface__]
        clipped, transform = mask(src, geom, crop=True)
        meta = src.meta.copy()
        meta.update({
            "driver": "GTiff",
            "height": clipped.shape[1],
            "width": clipped.shape[2],
            "transform": transform,
        })
    with rasterio.open(out_path, "w", **meta) as dst:
        dst.write(clipped)

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    aoi = gpd.read_file(GPKG, layer=AOI_LAYER)

    for tag, safe in SAFE.items():
        print(f"\n=== {tag.upper()} : {safe.name} ===")
        for band in BANDS_10M:
            src = find_band(safe, band, "10m")
            out = OUT_DIR / f"{tag}_{band}.tif"
            clip_band(src, aoi, out)
            print(f"  {band} -> {out.name}")
        for band in BANDS_20M:
            src = find_band(safe, band, "20m")
            out = OUT_DIR / f"{tag}_{band}.tif"
            clip_band(src, aoi, out)
            print(f"  {band} -> {out.name}")

    print("\nDone. Clipped bands in", OUT_DIR)

if __name__ == "__main__":
    main()