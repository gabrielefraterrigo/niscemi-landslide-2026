"""
Phase 2 — Extract the municipality of Niscemi from the national ISTAT
boundaries shapefile, reproject to the project CRS (EPSG:32633), and
save it into the project GeoPackage as the reference unit for zonal
statistics (Q2).

Input:  data/raw/<istat_folder>/Com01012024_WGS84.shp  (EPSG:32632)
Output: data/processed/aoi.gpkg, layer 'comune_niscemi' (EPSG:32633)
"""

import geopandas as gpd
from pathlib import Path

COMUNI_SHP = Path("data/raw/Com01012024/Com01012024_WGS84.shp")
GPKG_OUT = Path("data/processed/aoi.gpkg")
PROJECT_CRS = "EPSG:32633"
MUNICIPALITY = "Niscemi"

def main():
    # 1. Load the national municipalities layer
    comuni = gpd.read_file(COMUNI_SHP)
    print(f"Loaded {len(comuni)} municipalities, CRS: {comuni.crs}")

    # 2. Filter the single municipality by name (field 'COMUNE')
    niscemi = comuni[comuni["COMUNE"] == MUNICIPALITY]
    if len(niscemi) == 0:
        raise ValueError(f"'{MUNICIPALITY}' not found in field COMUNE")
    if len(niscemi) > 1:
        print(f"WARNING: {len(niscemi)} rows matched — check for namesakes")
    print(f"Matched {len(niscemi)} feature(s) for {MUNICIPALITY}")

    # 3. Reproject vectors (formula on vertices, no resampling, lossless)
    niscemi = niscemi.to_crs(PROJECT_CRS)

    # 4. Sanity check: area in km² (legit because CRS is metric)
    area_km2 = niscemi.geometry.area.iloc[0] / 1e6
    print(f"Niscemi area: {area_km2:.1f} km²  (expected ~97 km²)")

    # 5. Save into the project GeoPackage
    niscemi.to_file(GPKG_OUT, layer="comune_niscemi", driver="GPKG")
    print(f"Saved 'comune_niscemi' to {GPKG_OUT}")

if __name__ == "__main__":
    main()