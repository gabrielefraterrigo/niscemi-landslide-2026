Niscemi Landslide 2026 — Multi-sensor Geospatial Analysis

Geospatial analysis of the January 2026 Niscemi (Sicily) landslide using
Sentinel-2 optical imagery and DEM-derived terrain analysis, cross-checked
against official hazard mapping (PAI) and building footprints. SAR coherence
analysis of the urban sector is planned as a final stage.

Status: 🚧 Core analysis complete (Q1–Q3). Code refinement, SAR stage
(Phase 7), and final report in progress.


Context

On 25 January 2026 a landslide reactivated on the western slope of Niscemi
(Caltanissetta, Sicily), following an earlier movement on 16 January. The main
collapse affected the southern front near the built-up area, leading to
evacuations. The slope is a historically known instability, already mapped in
the regional hydrogeological plan (PAI). This project characterises the event
from open geospatial data and quantifies how much of it was already recognised
as hazardous.


Research questions


Extent & geometry — What is the extent and geometry of the area affected
by the January 2026 landslide, as detectable from satellite data?
Morphometry — Which morphometric characteristics (slope) define the
failed slope compared to the wider municipal area?
Risk context — How much of the 2026 collapsed area was already mapped as
hazardous in the PAI inventory, and how many buildings fall within classified
risk zones?



Key results

QuestionResultQ1 — ExtentLandslide polygon of ~24.8 ha (two main bodies), delineated by optical change detection (dNDVI) and manual refinement. Qualitatively validated against Civil Protection mapping.Q2 — MorphometryFailed slope mean gradient 11.9° (median 11.1°) vs municipal mean 6.9° (median 5.3°) — the landslide concentrates on terrain markedly steeper than the municipal average.Q3 — Risk context73% of the collapsed area fell within PAI hazard zones (50% in the highest class, P4). Intersecting dissesti were all classified active. 13 buildings intersect the landslide; 104 buildings lie within high-hazard (P3–P4) zones.

The 2026 failure reactivated a slope that was morphologically predisposed and
already officially recognised as hazardous — not an unforeseen event.


Data

DatasetSourceCRS (native)NotesSentinel-2 L2A (pre 2025-12-27, post 2026-02-25)Copernicus / ESA32633Tile T33SVB, atmospherically correctedDEM TINITALY (10 m)INGV32632Reprojected to 32633PAI Geomorfologia (hazard, dissesti)SITR Regione Siciliana (upd. 2026-05-12)25833Shapefile; not legally binding (ref. = official PDF)Municipal boundariesISTAT 2024 (via ISPRA)32632Building footprintsOpenStreetMap (QuickOSM)4326Coverage good but not guaranteed exhaustive

Project CRS: EPSG:32633 (WGS84 / UTM 33N) — native CRS of Sentinel products
over Sicily. Full details in docs/data_inventory.md.


Repository structure

niscemi-landslide-2026/
├── scripts/      # Numbered analysis pipeline (00 → 14)
├── data/         # Not versioned (raw + processed); see data_inventory.md
│   ├── raw/      # Source data (Sentinel, DEM, PAI, ISTAT, OSM)
│   └── processed/# Derived outputs (regenerable from scripts)
├── docs/         # data_inventory.md, work_plan.md, styles
├── maps/         # Exported maps (Phase 6)
├── LOG.md        # Working diary (Italian)
├── requirements.txt
└── README.md

Data lives outside version control: raw data is downloadable from the sources
above, and processed outputs are regenerable by running the pipeline.


Pipeline

Scripts are numbered in execution order. Each reads from data/ and writes
derived outputs back to data/processed/.

#ScriptPurpose00create_aoi.pyDefine event and context areas of interest01reproject_dem.pyReproject DEM 32632 → 32633 (bilinear)02slope.pySlope from DEM (degrees)03extract_niscemi.pyExtract Niscemi municipality (ISTAT)04zonal_slope.pyZonal slope statistics over the municipality05extract_clip.pyClip Sentinel-2 bands to the event AOI06ndvi_masked.pyCloud-masked NDVI (pre/post) via SCL07dndvi.pyNDVI change (post − pre)08bsi_masked.pyBare Soil Index + dBSI (independent confirmation)09landslide_polygon.pyDelineate landslide (threshold + morphology)10clip_slope_aoi.pyClip slope to the event AOI11zonal_landslide.pyZonal slope statistics over the landslide12overlay_pai.pyLandslide × PAI hazard classes13overlay_dissesti.pyLandslide × mapped dissesti14buildings.pyBuildings in landslide & high-hazard zones

The landslide polygon is finalised with manual cleanup in QGIS (removal of
agricultural false positives), guided by dNDVI and validated against Civil
Protection orthophotos.


Setup

bashpython -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt

Run scripts in order from the project root, e.g.:

bashpython scripts/06_ndvi_masked.py


Limitations


Optical detection underestimates the urban sector. NDVI/BSI respond weakly
where dense buildings collapse (little vegetation to lose), so the polygon
captures the vegetated slope well but under-represents the built-up area. SAR
coherence analysis (Phase 7) is planned to recover this.
Pre-event DEM. Slope morphometry describes pre-existing susceptibility, not
post-failure morphology; the detachment scarp — steep only after the event — is
not "seen" as steep by the pre-event DEM.
Threshold + manual refinement introduce operator subjectivity in the
polygon; mitigated by validation against official mapping.
~60-day image interval (Dec–Feb) introduces seasonal vegetation change as
background noise, handled via per-pixel change detection rather than aggregate
statistics.



Data licences & credits


Sentinel-2: Copernicus / ESA (free & open).
DEM TINITALY: INGV.
PAI Geomorfologia: Regione Siciliana — CC BY-NC 3.0 IT (not legally binding;
official reference is the notified PDF cartography).
Building footprints: © OpenStreetMap contributors (ODbL).
Official landslide perimeter (qualitative validation): Dipartimento della
Protezione Civile / GEOSDI–CNR-IMAA.