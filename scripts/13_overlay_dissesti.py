"""
Phase 4 — Q3: overlay the landslide polygon with PAI DISSESTI (already
mapped instability phenomena) to check whether the 2026 failure coincides
with previously inventoried landslides/instability — an independent
confirmation, complementary to the hazard-class overlay (script 12).

PAI CRS is EPSG:25833 → reprojected to 32633.

Inputs:  data/processed/landslide_ndvi_final.gpkg :: landslide_ndvi_final
         data/raw/PAI_GEOMORFOLOGIA/DISSESTI.shp  (EPSG:25833)
Output:  printed summary + data/processed/landslide_dissesti.gpkg
"""

import geopandas as gpd
from pathlib import Path

LANDSLIDE = Path("data/processed/landslide_ndvi_final.gpkg")
LANDSLIDE_LAYER = "landslide_ndvi_final"
DISSESTI = Path("data/raw/PAI_GEOMORFOLOGIA/DISSESTI.shp")
PROJECT_CRS = "EPSG:32633"
OUT_GPKG = Path("data/processed/landslide_dissesti.gpkg")

def main():
    frana = gpd.read_file(LANDSLIDE, layer=LANDSLIDE_LAYER)
    total_ha = frana.geometry.area.sum() / 1e4
    print(f"Landslide total area: {total_ha:.2f} ha")

    # Load DISSESTI near the landslide (bbox in DISSESTI's CRS), reproject
    bbox = tuple(frana.to_crs("EPSG:25833").total_bounds)
    diss = gpd.read_file(DISSESTI, bbox=bbox)
    print(f"DISSESTI features near landslide: {len(diss)}")
    print(f"DISSESTI columns: {list(diss.columns)}")   # inspect available fields
    diss = diss.to_crs(PROJECT_CRS)

    # Intersect
    inter = gpd.overlay(frana, diss, how="intersection")
    if len(inter) == 0:
        print("\nNo overlap: the landslide does NOT intersect any mapped dissesto.")
        return
    inter["area_ha"] = inter.geometry.area / 1e4
    covered = inter["area_ha"].sum()
    print(f"\nLandslide area intersecting mapped dissesti: {covered:.2f} ha "
          f"({100*covered/total_ha:.1f}% of landslide)")

# Show only the meaningful descriptive fields, readable
    cols = ["area_ha", "COD_TIP", "COD_ATT", "PERICOLO", "DATA_EVENT", "LOCALITA"]
    cols = [c for c in cols if c in inter.columns]
    print("\n--- Mapped dissesti intersecting the landslide ---")
    print(inter[cols].to_string(index=False))

    # Area by dissesto type and by activity state
    if "COD_TIP" in inter.columns:
        print("\nArea by dissesto type (COD_TIP):")
        print((inter.groupby("COD_TIP")["area_ha"].sum()).to_string())
    if "COD_ATT" in inter.columns:
        print("\nArea by activity state (COD_ATT):")
        print((inter.groupby("COD_ATT")["area_ha"].sum()).to_string())
if __name__ == "__main__":
    main()