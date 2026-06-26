"""
Phase 3 — Clip the full-cell slope raster to the event AOI so it
aligns with the dNDVI grid (needed for the slope constraint in
the landslide delineation).

Input:  data/processed/slope_deg.tif  (full TINITALY cell)
Output: data/processed/cd/slope_aoi.tif  (clipped to aoi_event)
"""

import geopandas as gpd
import rasterio
from rasterio.mask import mask
from pathlib import Path

SLOPE = Path("data/processed/slope_deg.tif")
GPKG = Path("data/processed/aoi.gpkg")
AOI_LAYER = "aoi_event"
OUT = Path("data/processed/cd/slope_aoi.tif")

def main():
    aoi = gpd.read_file(GPKG, layer=AOI_LAYER)
    with rasterio.open(SLOPE) as src:
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
    with rasterio.open(OUT, "w", **meta) as dst:
        dst.write(clipped)
    print(f"Slope clipped to AOI -> {OUT} ({clipped.shape[2]}x{clipped.shape[1]})")

if __name__ == "__main__":
    main()