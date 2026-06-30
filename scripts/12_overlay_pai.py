"""
Phase 4 — Q3: overlay the landslide polygon with PAI landslide-hazard
zones (PERICOLOSITA) to quantify how much of the 2026 failure fell
within areas already classified as hazardous, and in which class.

PAI 'PERICOLO' field: 1=P1 moderate, 2=P2 medium, 3=P3 high, 4=P4 very high.
PAI CRS is EPSG:25833 (ETRS89/UTM33N) → reprojected to project CRS 32633.

Inputs:  data/processed/landslide_ndvi_final.gpkg :: landslide_ndvi_final
         data/raw/PAI_GEOMORFOLOGIA/PERICOLOSITA.shp  (EPSG:25833)
Output:  printed table + data/processed/overlay_pai.txt
         data/processed/landslide_pai.gpkg (intersection, for mapping)
"""

import geopandas as gpd
from pathlib import Path

LANDSLIDE = Path("data/processed/landslide_ndvi_final.gpkg")
LANDSLIDE_LAYER = "landslide_ndvi_final"
PAI = Path("data/raw/PAI_GEOMORFOLOGIA/PERICOLOSITA.shp")
PROJECT_CRS = "EPSG:32633"
OUT_TXT = Path("data/processed/overlay_pai.txt")
OUT_GPKG = Path("data/processed/landslide_pai.gpkg")

CLASS_NAMES = {1: "P1 moderate", 2: "P2 medium", 3: "P3 high", 4: "P4 very high"}

def main():
    # 1. Load landslide polygon (already 32633)
    frana = gpd.read_file(LANDSLIDE, layer=LANDSLIDE_LAYER)
    print(f"Landslide: {len(frana)} polygon(s), CRS {frana.crs}")
    total_ha = frana.geometry.area.sum() / 1e4
    print(f"Total landslide area: {total_ha:.2f} ha")

    # 2. Load PAI hazard and reproject to project CRS.
    #    Read only what we need; PAI covers all Sicily, so we clip to the
    #    landslide bounding box first (bbox filter = fast, avoids loading 75 MB).
    bbox = tuple(frana.to_crs("EPSG:25833").total_bounds)  # bbox in PAI's CRS
    pai = gpd.read_file(PAI, bbox=bbox)
    print(f"PAI features near landslide: {len(pai)} (before reproject)")
    pai = pai.to_crs(PROJECT_CRS)

    # 3. Intersect landslide x PAI hazard (geometric overlay)
    inter = gpd.overlay(frana, pai, how="intersection")
    inter["area_ha"] = inter.geometry.area / 1e4

    # 4. Aggregate area by hazard class
    print("\n--- Landslide area by PAI hazard class ---")
    by_class = inter.groupby("PERICOLO")["area_ha"].sum()
    covered = 0.0
    for cls, ha in by_class.items():
        name = CLASS_NAMES.get(cls, f"class {cls}")
        pct = 100 * ha / total_ha
        print(f"  {name:14s}: {ha:6.2f} ha  ({pct:4.1f}% of landslide)")
        covered += ha

    # 5. Part of the landslide NOT covered by any PAI hazard zone
    uncovered = total_ha - covered
    print(f"\n  Covered by PAI hazard : {covered:6.2f} ha  ({100*covered/total_ha:4.1f}%)")
    print(f"  NOT in any PAI zone   : {uncovered:6.2f} ha  ({100*uncovered/total_ha:4.1f}%)")

    # 6. Save intersection for mapping + a text summary
    inter.to_file(OUT_GPKG, layer="landslide_pai", driver="GPKG")
    lines = [f"Landslide vs PAI hazard — total {total_ha:.2f} ha\n"]
    for cls, ha in by_class.items():
        lines.append(f"{CLASS_NAMES.get(cls, cls)}: {ha:.2f} ha ({100*ha/total_ha:.1f}%)")
    lines.append(f"Covered: {covered:.2f} ha ({100*covered/total_ha:.1f}%)")
    lines.append(f"Not in any PAI zone: {uncovered:.2f} ha ({100*uncovered/total_ha:.1f}%)")
    OUT_TXT.write_text("\n".join(lines) + "\n")
    print(f"\nSaved intersection to {OUT_GPKG} and summary to {OUT_TXT}")

if __name__ == "__main__":
    main()