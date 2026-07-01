"""
Phase 7 — Quantify SAR coherence by zone to confirm, with numbers, the
visual pattern: low coherence over the landslide (structural change /
collapse), high coherence over intact built-up area, low over farmland
(natural temporal decorrelation).

Coherence: HyP3 InSAR GAMMA (S1 14/01 → 01/02/2026), values 0–1.

Inputs:  data/raw/sar_coherence/.../*_corr.tif
         data/processed/landslide_ndvi_final.gpkg :: landslide_ndvi_final
         data/raw/osm_buildings.gpkg :: buildings
         data/processed/aoi.gpkg :: aoi_event
Output:  printed coherence means per zone
"""

import geopandas as gpd
import numpy as np
import rasterio
from rasterio.mask import mask
from rasterio.warp import calculate_default_transform, reproject, Resampling
from pathlib import Path
import glob

CORR = glob.glob("data/raw/sar_coherence/**/*_corr.tif", recursive=True)[0]
LANDSLIDE = ("data/processed/landslide_ndvi_final.gpkg", "landslide_ndvi_final")
BUILDINGS = ("data/raw/osm_buildings.gpkg", "buildings")
AOI = ("data/processed/aoi.gpkg", "aoi_event")
PROJECT_CRS = "EPSG:32633"

def reproject_to_32633(src_path):
    """Reproject the coherence raster to project CRS, return array + transform + meta."""
    with rasterio.open(src_path) as src:
        transform, width, height = calculate_default_transform(
            src.crs, PROJECT_CRS, src.width, src.height, *src.bounds)
        dst = np.empty((height, width), dtype="float32")
        reproject(
            source=rasterio.band(src, 1),
            destination=dst,
            src_transform=src.transform, src_crs=src.crs,
            dst_transform=transform, dst_crs=PROJECT_CRS,
            resampling=Resampling.bilinear)
        meta = src.meta.copy()
        meta.update(crs=PROJECT_CRS, transform=transform,
                    width=width, height=height, dtype="float32")
    return dst, transform, meta

def mean_coh_in(geoms, corr_path):
    """Mean coherence within given geometries (raster already reprojected on disk)."""
    with rasterio.open(corr_path) as src:
        clipped, _ = mask(src, geoms, crop=True, nodata=np.nan)
    v = clipped[0]
    v = v[(~np.isnan(v)) & (v > 0)]   # drop nodata / zero-fill
    return v.mean(), v.size

def main():
    print(f"Coherence file: {Path(CORR).name}")

    # 1. Reproject coherence to 32633, write a temp file to disk for masking
    dst, transform, meta = reproject_to_32633(CORR)
    tmp = Path("data/processed/corr_32633.tif")
    with rasterio.open(tmp, "w", **meta) as out:
        out.write(dst, 1)
    print(f"Reprojected coherence -> {tmp}")

    # 2. Load zones
    frana = gpd.read_file(LANDSLIDE[0], layer=LANDSLIDE[1]).to_crs(PROJECT_CRS)
    blds = gpd.read_file(BUILDINGS[0], layer=BUILDINGS[1]).to_crs(PROJECT_CRS)
    aoi = gpd.read_file(AOI[0], layer=AOI[1]).to_crs(PROJECT_CRS)

    # Urban proxy: dissolved buildings + small buffer (fill gaps between them)
    urban = blds.buffer(30).union_all()
    frana_geom = frana.union_all()
    # Farmland proxy: AOI minus urban minus landslide
    farmland = aoi.union_all().difference(urban).difference(frana_geom)

    # 3. Mean coherence per zone
    print("\n--- Mean SAR coherence by zone ---")
    for name, geom in [("Landslide", frana_geom),
                       ("Urban (buildings)", urban),
                       ("Farmland (control)", farmland)]:
        m, n = mean_coh_in([geom.__geo_interface__], tmp)
        print(f"  {name:20s}: coherence = {m:.3f}  (n={n} px)")

    print("\nExpected: landslide LOW (structural change), urban HIGH "
          "(intact buildings), farmland LOW (vegetation decorrelation).")

if __name__ == "__main__":
    main()