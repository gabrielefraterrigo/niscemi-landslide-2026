"""
Phase 4 — Q3: count buildings involved by the landslide and buildings
within high-hazard PAI zones (P3+P4).

Criterion: a building counts as 'involved' if it INTERSECTS the area
(any overlap), the standard choice for landslide impact assessment.

Buildings: OpenStreetMap (via QuickOSM), polygon footprints.
NOTE: OSM coverage is good but not guaranteed exhaustive — to be
declared as a limitation in the report.

Inputs:  data/raw/osm_buildings.gpkg :: osm_buildings        (buildings)
         data/processed/landslide_ndvi_final.gpkg :: landslide_ndvi_final
         data/raw/PAI_GEOMORFOLOGIA/PERICOLOSITA.shp          (hazard)
Output:  printed counts + data/processed/buildings_in_landslide.gpkg
"""

import geopandas as gpd
from pathlib import Path

BUILDINGS = Path("data/raw/osm_buildings.gpkg")
BUILDINGS_LAYER = "buildings"
LANDSLIDE = Path("data/processed/landslide_ndvi_final.gpkg")
LANDSLIDE_LAYER = "landslide_ndvi_final"
PAI = Path("data/raw/PAI_GEOMORFOLOGIA/PERICOLOSITA.shp")
PROJECT_CRS = "EPSG:32633"
OUT = Path("data/processed/buildings_in_landslide.gpkg")

def main():
    # 1. Load buildings, ensure project CRS
    blds = gpd.read_file(BUILDINGS, layer=BUILDINGS_LAYER).to_crs(PROJECT_CRS)
    print(f"Buildings loaded: {len(blds)} (CRS {blds.crs})")

    # 2. Buildings intersecting the LANDSLIDE polygon
    frana = gpd.read_file(LANDSLIDE, layer=LANDSLIDE_LAYER).to_crs(PROJECT_CRS)
    in_frana = gpd.sjoin(blds, frana, how="inner", predicate="intersects")
    in_frana = in_frana[~in_frana.index.duplicated(keep="first")]  # dedupe
    print(f"\nBuildings intersecting the landslide area: {len(in_frana)}")

    # 3. Buildings within high-hazard PAI zones (P3 + P4)
    bbox = tuple(blds.to_crs("EPSG:25833").total_bounds)
    pai = gpd.read_file(PAI, bbox=bbox).to_crs(PROJECT_CRS)
    pai_high = pai[pai["PERICOLO"].isin(["3", "4"])]
    print(f"PAI P3+P4 polygons near area: {len(pai_high)}")
    in_hazard = gpd.sjoin(blds, pai_high, how="inner", predicate="intersects")
    in_hazard = in_hazard[~in_hazard.index.duplicated(keep="first")]
    print(f"Buildings within PAI high-hazard zones (P3+P4): {len(in_hazard)}")

    # 4. Save buildings in the landslide (for mapping)
    if len(in_frana) > 0:
        in_frana.to_file(OUT, layer="buildings_in_landslide", driver="GPKG")
        print(f"\nSaved buildings-in-landslide to {OUT}")
    else:
        print("\nNo buildings intersect the landslide polygon.")

if __name__ == "__main__":
    main()