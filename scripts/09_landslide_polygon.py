"""
Phase 3 — Delineate the landslide polygon from dNDVI.
Steps: threshold -> fill internal holes -> remove small fragments
-> vectorize. Threshold and min-size are documented parameters
(to be validated against official perimeters in Phase 4).

Input:  data/processed/cd/dndvi.tif
Output: data/processed/aoi.gpkg, layer 'landslide_ndvi'
"""

import numpy as np
import rasterio
from rasterio.features import shapes
from scipy import ndimage
import geopandas as gpd
from shapely.geometry import shape
from pathlib import Path

CD = Path("data/processed/cd")
GPKG = Path("data/processed/aoi.gpkg")

THRESHOLD = -0.2          # era -0.3
MIN_PIXELS = 150          # era 50

def main():
    with rasterio.open(CD / "dndvi.tif") as src:
        dndvi = src.read(1)
        transform = src.transform
        crs = src.crs

    # 1. Threshold (NaN-safe: NaN < x is False, so NaNs excluded)
    mask = (dndvi < THRESHOLD)
    print(f"After threshold: {mask.sum()} pixels")

    # 2. Fill internal holes (pixels enclosed by landslide)
    mask = ndimage.binary_fill_holes(mask)
    print(f"After fill holes: {mask.sum()} pixels")

    # 2b. Morphological closing: connect nearby landslide pixels into
    #     a coherent body (dilate then erode). Bridges small gaps from
    #     residual vegetation / already-bare patches inside the slide.
    structure = ndimage.generate_binary_structure(2, 2)  # 8-connectivity
    mask = ndimage.binary_closing(mask, structure=structure, iterations=3)
    print(f"After closing: {mask.sum()} pixels")

    # 3. Remove small fragments: label connected blobs, keep big ones
    labels, n = ndimage.label(mask, structure=structure)
    sizes = ndimage.sum(mask, labels, range(1, n + 1))
    keep = np.isin(labels, np.where(sizes >= MIN_PIXELS)[0] + 1)
    mask_clean = keep
    print(f"Blobs: {n} total, {(sizes >= MIN_PIXELS).sum()} kept (>= {MIN_PIXELS} px)")
    print(f"After size filter: {mask_clean.sum()} pixels")

    # 4. Vectorize the cleaned mask
    polys = []
    for geom, val in shapes(mask_clean.astype("uint8"), mask=mask_clean, transform=transform):
        if val == 1:
            polys.append(shape(geom))

    gdf = gpd.GeoDataFrame({"id": range(len(polys))}, geometry=polys, crs=crs)
    # Optional: dissolve into a single multipolygon
    gdf["area_ha"] = gdf.geometry.area / 1e4   # area in hectares
    total_ha = gdf["area_ha"].sum()
    print(f"\nLandslide polygon(s): {len(gdf)}, total area = {total_ha:.1f} ha")

    gdf.to_file(GPKG, layer="landslide_ndvi", driver="GPKG")
    print(f"Saved 'landslide_ndvi' to {GPKG}")

if __name__ == "__main__":
    main()