"""
Phase 2 — Zonal statistics of slope within the municipality of Niscemi.
Produces summary stats (mean, median, min, max, std) and the
distribution of slope across morphological classes. This is the
REFERENCE distribution for Q2; the landslide-area distribution
(Phase 3) will be compared against it.

Inputs:  data/processed/slope_deg.tif      (EPSG:32633)
         data/processed/aoi.gpkg :: comune_niscemi  (EPSG:32633)
Output:  printed stats + data/processed/zonal_comune.txt
"""

import geopandas as gpd
import numpy as np
import rasterio
from rasterio.mask import mask
from pathlib import Path

SLOPE = Path("data/processed/slope_deg.tif")
GPKG = Path("data/processed/aoi.gpkg")
LAYER = "comune_niscemi"
OUT = Path("data/processed/zonal_comune.txt")

# Slope classes (degrees) — same thresholds as the map symbology
CLASS_EDGES = [0, 5, 15, 25, 35, 90]
CLASS_NAMES = ["0-5 flat", "5-15 gentle", "15-25 moderate",
               "25-35 steep", ">35 very steep"]

def main():
    # 1. Load the zone polygon (already in 32633)
    zone = gpd.read_file(GPKG, layer=LAYER)
    print(f"Zone CRS: {zone.crs}")

    # 2. Open slope raster and clip to the polygon.
    #    'crop=True' limits the read to the polygon's bounding box;
    #    pixels outside the polygon become nodata in the masked array.
    with rasterio.open(SLOPE) as src:
        geom = [zone.geometry.iloc[0].__geo_interface__]
        clipped, _ = mask(src, geom, crop=True, nodata=np.nan)
        nodata_src = src.nodata
        print(f"Raster CRS: {src.crs}, source nodata: {nodata_src}")

    # 3. Flatten to 1D and drop nodata (NaN) -> only valid slope pixels
    data = clipped[0].astype("float64")
    valid = data[~np.isnan(data)]
    print(f"Valid pixels inside municipality: {valid.size}")

    # 4. Summary statistics
    print("\n--- Slope statistics within Niscemi municipality ---")
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

    # 6. Save results to a text file (for later comparison)
    OUT.write_text(
        "Zonal slope stats — Niscemi municipality\n"
        f"mean={valid.mean():.1f} median={np.median(valid):.1f} "
        f"min={valid.min():.1f} max={valid.max():.1f} std={valid.std():.1f}\n\n"
        + "\n".join(lines) + "\n"
    )
    print(f"\nSaved to {OUT}")

if __name__ == "__main__":
    main()