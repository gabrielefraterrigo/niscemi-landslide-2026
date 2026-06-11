"""
Phase 0 — Creates the two Areas of Interest (AOI) for the project.

AOI-1: event scale  — provisional bounding box around the landslide
       front (S/SW of Niscemi urban area). To be refined in Phase 1
       against Civil Protection maps and post-event Sentinel-2.
AOI-2: context scale — wider box covering the Niscemi territory,
       used as statistical reference for terrain analysis (Q2).

Output: data/processed/aoi.gpkg (EPSG:32633), layers 'aoi_event'
        and 'aoi_context', plus an interactive HTML check map.
"""

import geopandas as gpd
from shapely.geometry import box
from pathlib import Path

# ----------------------------------------------------------------------
# 1. Define corners in geographic coordinates (EPSG:4326), lon/lat order.
#    PROVISIONAL values — refine in Phase 1.
# ----------------------------------------------------------------------
# Niscemi town centre is roughly at lon 14.387, lat 37.146.
# The landslide front (~4 km) opened along the S / SW edge of town.
AOI_EVENT_BOUNDS = (14.320, 37.090, 14.430, 37.165)   # (min_lon, min_lat, max_lon, max_lat)
AOI_CONTEXT_BOUNDS = (14.280, 37.040, 14.500, 37.210)

PROJECT_CRS = "EPSG:32633"

def make_aoi(bounds: tuple, name: str) -> gpd.GeoDataFrame:
    """Build a single-polygon GeoDataFrame in the project CRS."""
    geom = box(*bounds)                       # shapely rectangle from bounds
    gdf = gpd.GeoDataFrame(
        {"name": [name]}, geometry=[geom], crs="EPSG:4326"
    )
    return gdf.to_crs(PROJECT_CRS)            # reproject vectors, not rasters

def main():
    out_dir = Path("data/processed")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "aoi.gpkg"

    aoi_event = make_aoi(AOI_EVENT_BOUNDS, "aoi_event")
    aoi_context = make_aoi(AOI_CONTEXT_BOUNDS, "aoi_context")

    # GeoPackage supports multiple layers in one file (unlike shapefile)
    aoi_event.to_file(out_file, layer="aoi_event", driver="GPKG")
    aoi_context.to_file(out_file, layer="aoi_context", driver="GPKG")

    # Sanity check: area in km² (correct because CRS is metric)
    for gdf in (aoi_event, aoi_context):
        area_km2 = gdf.geometry.area.iloc[0] / 1e6
        print(f"{gdf['name'].iloc[0]}: {area_km2:.1f} km²")

    # Visual check: interactive map (folium uses 4326 internally)
    m = aoi_context.to_crs("EPSG:4326").explore(
        color="orange", style_kwds={"fill": False}, tiles="OpenStreetMap"
    )
    aoi_event.to_crs("EPSG:4326").explore(m=m, color="red",
                                          style_kwds={"fill": False})
    m.save("maps/aoi_check.html")
    print("Check map saved to maps/aoi_check.html")

if __name__ == "__main__":
    main()