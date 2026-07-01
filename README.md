# Niscemi Landslide 2026 — Multi-sensor Geospatial Analysis

Geospatial analysis of the January 2026 Niscemi (Sicily) landslide using
Sentinel-2 optical imagery and DEM-derived terrain analysis, cross-checked
against official hazard mapping (PAI) and building footprints. SAR coherence
analysis of the urban sector is planned as a final stage.

**Status:** 🚧 Core analysis complete (Q1–Q3). Code refinement, SAR stage
(Phase 7), and final report in progress.

---

## Context

On 25 January 2026 a landslide reactivated on the western slope of Niscemi
(Caltanissetta, Sicily), following an earlier movement on 16 January. The main
collapse affected the southern front near the built-up area, leading to
evacuations. The slope is a historically known instability, already mapped in
the regional hydrogeological plan (PAI). This project characterises the event
from open geospatial data and quantifies how much of it was already recognised
as hazardous.

---

## Research questions

1. **Extent & geometry** — What is the extent and geometry of the area affected
   by the January 2026 landslide, as detectable from satellite data?
2. **Morphometry** — Which morphometric characteristics (slope) define the
   failed slope compared to the wider municipal area?
3. **Risk context** — How much of the 2026 collapsed area was already mapped as
   hazardous in the PAI inventory, and how many buildings fall within classified
   risk zones?

---

## Key results

| Question | Result |
|----------|--------|
| **Q1 — Extent** | Landslide polygon of ~24.8 ha (two main bodies), delineated by optical change detection (dNDVI) and manual refinement. Qualitatively validated against Civil Protection mapping. |
| **Q2 — Morphometry** | Failed slope mean gradient **11.9°** (median 11.1°) vs municipal mean **6.9°** (median 5.3°) — the landslide concentrates on terrain markedly steeper than the municipal average. |
| **Q3 — Risk context** | **73%** of the collapsed area fell within PAI hazard zones (**50%** in the highest class, P4). Intersecting dissesti were all classified **active**. **13** buildings intersect the landslide; **104** buildings lie within high-hazard (P3–P4) zones. |

*The 2026 failure reactivated a slope that was morphologically predisposed and
already officially recognised as hazardous — not an unforeseen event.*

---

## Data

| Dataset | Source | CRS (native) | Notes |
|---------|--------|--------------|-------|
| Sentinel-2 L2A (pre 2025-12-27, post 2026-02-25) | Copernicus / ESA | 32633 | Tile T33SVB, atmospherically corrected |
| DEM TINITALY (10 m) | INGV | 32632 | Reprojected to 32633 |
| PAI Geomorfologia (hazard, dissesti) | SITR Regione Siciliana (upd. 2026-05-12) | 25833 | Shapefile; not legally binding (ref. = official PDF) |
| Municipal boundaries | ISTAT 2024 (via ISPRA) | 32632 | |
| Building footprints | OpenStreetMap (QuickOSM) | 4326 | Coverage good but not guaranteed exhaustive |

Project CRS: **EPSG:32633** (WGS84 / UTM 33N) — native CRS of Sentinel products
over Sicily. Full details in [`docs/data_inventory.md`](docs/data_inventory.md).

---

## Repository structure

```
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
```

Data lives outside version control: raw data is downloadable from the sources
above, and processed outputs are regenerable by running the pipeline.

---

## Pipeline

Scripts are numbered in execution order. Each reads from `data/` and writes
derived outputs back to `data/processed/`.

| # | Script | Purpose |
|---|--------|---------|
| 00 | `create_aoi.py` | Define event and context areas of interest |
| 01 | `reproject_dem.py` | Reproject DEM 32632 → 32633 (bilinear) |
| 02 | `slope.py` | Slope from DEM (degrees) |
| 03 | `extract_niscemi.py` | Extract Niscemi municipality (ISTAT) |
| 04 | `zonal_slope.py` | Zonal slope statistics over the municipality |
| 05 | `extract_clip.py` | Clip Sentinel-2 bands to the event AOI |
| 06 | `ndvi_masked.py` | Cloud-masked NDVI (pre/post) via SCL |
| 07 | `dndvi.py` | NDVI change (post − pre) |
| 08 | `bsi_masked.py` | Bare Soil Index + dBSI (independent confirmation) |
| 09 | `landslide_polygon.py` | Delineate landslide (threshold + morphology) |
| 10 | `clip_slope_aoi.py` | Clip slope to the event AOI |
| 11 | `zonal_landslide.py` | Zonal slope statistics over the landslide |
| 12 | `overlay_pai.py` | Landslide × PAI hazard classes |
| 13 | `overlay_dissesti.py` | Landslide × mapped dissesti |
| 14 | `buildings.py` | Buildings in landslide & high-hazard zones |

The landslide polygon is finalised with manual cleanup in QGIS (removal of
agricultural false positives), guided by dNDVI and validated against Civil
Protection orthophotos.

---

## Setup

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

Run scripts in order from the project root, e.g.:

```bash
python scripts/06_ndvi_masked.py
```

---

## Limitations

- **Optical detection underestimates the urban sector.** NDVI/BSI respond weakly
  where dense buildings collapse (little vegetation to lose), so the polygon
  captures the vegetated slope well but under-represents the built-up area. SAR
  coherence analysis (Phase 7) is planned to recover this.
- **Pre-event DEM.** Slope morphometry describes pre-existing susceptibility, not
  post-failure morphology; the detachment scarp — steep only after the event — is
  not "seen" as steep by the pre-event DEM.
- **Threshold + manual refinement** introduce operator subjectivity in the
  polygon; mitigated by validation against official mapping.
- **~60-day image interval** (Dec–Feb) introduces seasonal vegetation change as
  background noise, handled via per-pixel change detection rather than aggregate
  statistics.

---

## Data licences & credits

- Sentinel-2: Copernicus / ESA (free & open).
- DEM TINITALY: INGV.
- PAI Geomorfologia: Regione Siciliana — CC BY-NC 3.0 IT (not legally binding;
  official reference is the notified PDF cartography).
- Building footprints: © OpenStreetMap contributors (ODbL).
- Official landslide perimeter (qualitative validation): Dipartimento della
  Protezione Civile / GEOSDI–CNR-IMAA.