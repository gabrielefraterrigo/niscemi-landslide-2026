"""
Phase 2 — Reproject the TINITALY DEM from its native CRS (EPSG:32632,
UTM 32N) to the project CRS (EPSG:32633, UTM 33N), resampling with
bilinear interpolation (DEM = continuous data).

Output: data/processed/dem_32633.tif (10 m pixels)
"""

import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from pathlib import Path

DEM_IN = Path("data/raw/w41095_s10/w41095_s10.tif")          
DEM_OUT = Path("data/processed/dem_32633.tif")
DST_CRS = "EPSG:32633"
TARGET_RES = 10.0                              # force 10 m pixels

def main():
    DEM_OUT.parent.mkdir(parents=True, exist_ok=True)

    with rasterio.open(DEM_IN) as src:
        print(f"Source CRS: {src.crs}, size: {src.width}x{src.height}, res: {src.res}")

        # Compute the transform, width and height of the reprojected grid.
        # Passing resolution=TARGET_RES forces clean 10 m pixels.
        transform, width, height = calculate_default_transform(
            src.crs, DST_CRS, src.width, src.height, *src.bounds,
            resolution=TARGET_RES
        )

        # Copy source metadata, then update the geospatial fields.
        kwargs = src.meta.copy()
        kwargs.update({
            "crs": DST_CRS,
            "transform": transform,
            "width": width,
            "height": height,
        })

        with rasterio.open(DEM_OUT, "w", **kwargs) as dst:
            reproject(
                source=rasterio.band(src, 1),
                destination=rasterio.band(dst, 1),
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=DST_CRS,
                resampling=Resampling.bilinear,   # continuous data -> bilinear
            )

        print(f"Reprojected DEM written to {DEM_OUT} ({width}x{height}, {DST_CRS})")

if __name__ == "__main__":
    main()