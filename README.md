# Niscemi Landslide 2026 — Multi-sensor Geospatial Analysis

Analysis of the January 2026 Niscemi (Sicily) landslide using
Sentinel-2 optical imagery, Sentinel-1 SAR, and DEM-derived
terrain analysis, with validation against official hazard maps (PAI/IFFI).

**Status:** 🚧 work in progress — Phase 0 (project scoping)

## Research questions
1. What is the extent and geometry of the area affected by the
   January 2026 landslide, as detectable from optical and SAR data?
2. Which morphometric characteristics (slope, aspect, curvature)
   define the failed slope compared to the wider municipal area?
3. How much of the 2026 collapsed area was already mapped as
   hazardous in the PAI / IFFI inventories, and how many buildings
   fell within classified risk zones?

## Stack
QGIS · Python (geopandas, rasterio) · Google Earth Engine · Sentinel-1/2 · TINITALY DEM

## Project CRS
EPSG:32633 (WGS84 / UTM 33N) — native CRS of Sentinel products over Sicily.