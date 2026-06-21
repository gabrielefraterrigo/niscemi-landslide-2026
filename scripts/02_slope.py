"""
Phase 2 — Slope computation.

NOTE: slope was computed in QGIS (Raster > Analysis > Slope), not in
Python, because the 'osgeo'/GDAL Python bindings are not available in
this venv environment (a known GDAL-on-Windows installation issue).
QGIS uses the same GDAL engine, so the result is identical.

Equivalent GDAL command (logged for reproducibility):

    gdaldem slope C:/Users/frate/niscemi-landslide-2026/data/processed/dem_32633.tif C:/Users/frate/niscemi-landslide-2026/data/processed/slope_deg.tif -of GTiff -b 1 -s 1.0 -compute_edges

Parameters:
  - Input:  data/processed/dem_32633.tif  (EPSG:32633, 10 m)
  - Output: data/processed/slope_deg.tif  (slope in DEGREES)
  - Method: Horn (default), edges computed, units = degrees

To reproduce in pure Python, GDAL bindings would be needed
(recommended: rebuild env with conda).
"""