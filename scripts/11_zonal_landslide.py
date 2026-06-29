"""
Phase 3 — Zonal statistics of slope within the landslide polygon.
Mirrors scripts/04_zonal_slope.py (which does the same for the
municipality) so the two distributions can be compared directly
to answer Q2: is the failed slope steeper than the municipal reference?

Note: the landslide layer has multiple polygons (two main bodies),
so all geometries are passed to the mask, not just the first.
Slope comes from the PRE-event DEM → describes pre-existing
susceptibility, not post-failure morphology.

Inputs:  data/processed/slope_deg.tif                        (EPSG:32633)
         data/processed/landslide_ndvi_final.gpkg :: landslide_ndvi_final
Output:  printed stats + data/processed/zonal_landslide.txt
"""

import geopandas as gpd
import numpy as np
import rasterio
from rasterio.mask import mask
from pathlib import Path

SLOPE = Path("data/processed/slope_deg.tif")
GPKG = Path("data/processed/landslide_ndvi_final.gpkg")
LAYER = "landslide_ndvi_final"
OUT = Path("data/processed/zonal_landslide.txt")

# Slope classes (degrees) — same thresholds as the municipality stats
CLASS_EDGES = [0, 5, 15, 25, 35, 90]
CLASS_NAMES = ["0-5 flat", "5-15 gentle", "15-25 moderate",
               "25-35 steep", ">35 very steep"]

def main():
    # 1. Load the landslide polygon(s) — multiple bodies expected
    zone = gpd.read_file(GPKG, layer=LAYER)
    print(f"Landslide layer: {len(zone)} polygon(s), CRS: {zone.crs}")
    geoms = [g.__geo_interface__ for g in zone.geometry]  # ALL bodies

    # 2. Clip slope to the polygon(s)
    with rasterio.open(SLOPE) as src:
        clipped, _ = mask(src, geoms, crop=True, nodata=np.nan)
        print(f"Raster CRS: {src.crs}, source nodata: {src.nodata}")

    # 3. Keep only valid slope pixels (drop nodata / outside polygon)
    data = clipped[0].astype("float64")
    valid = data[~np.isnan(data)]
    print(f"Valid pixels inside landslide: {valid.size}")
    if valid.size == 0:
        raise ValueError("No valid pixels — check CRS alignment / layer name.")

    # 4. Summary statistics
    print("\n--- Slope statistics within the landslide area ---")
    print(f"mean   = {valid.mean():.1f}°")
    print(f"median = {np.median(valid):.1f}°")
    print(f"min    = {valid.min():.1f}°")
    print(f"max    = {valid.max():.1f}°")
    print(f"std    = {valid.std():.1f}°")

    # 5. Distribution across morphological classes (% of area)
    print("\n--- Slope class distribution ---")
    counts, _ = np.histogram(valid, bins=CLASS_EDGES)
    total = counts.sum()
    lines = []
    for name, c in zip(CLASS_NAMES, counts):
        pct = 100 * c / total
        line = f"{name:18s}: {pct:5.1f}%  ({c} px)"
        print(line)
        lines.append(line)

    # 6. Save results for the report / comparison
    OUT.write_text(
        "Zonal slope stats — Niscemi landslide area\n"
        f"mean={valid.mean():.1f} median={np.median(valid):.1f} "
        f"min={valid.min():.1f} max={valid.max():.1f} std={valid.std():.1f}\n\n"
        + "\n".join(lines) + "\n"
    )
    print(f"\nSaved to {OUT}")

if __name__ == "__main__":
    main()