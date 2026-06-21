# Data Inventory

Raw data are NOT tracked in Git (see .gitignore). This file records their origin to make the analysis replicable by downloading them again from the original source

## Sentinel-2 (ottico)

| Ruolo | Product ID | Data | Livello | Tile | Fonte | Scaricato |
|-------|-----------|------|---------|------|-------|-----------|
| PRE  | S2B_MSIL2A_20251227T095329_N0511_R079_T33SVB | 2025-12-27 | L2A | T33SVB | Copernicus Data Space | 2026-06-18 |
| POST | S2B_MSIL2A_20260225T095029_N0512_R079_T33SVB | 2026-02-25 | L2A | T33SVB | Copernicus Data Space | 2026-06-18 |

**Selection Criterion:** see LOG.md. PRE = acquisition closest to
16/01/2026 with cloudless hillside; 11/01 e 01/01 dismissed due to clouds/mist on the hillside. POST = first clear acquisition after the collapse of the 25/01. Range ~60 days → seasonal variety declared as limit.


## DEM
| Product | Cell | Resolution | Native CRS | Source | Downloaded |
|---------|------|-----------|-----------|--------|-----------|
| TINITALY/01 | W41095 | 10 m | EPSG:32632 | INGV TINITALY | 2026-06-19 |

Type: DTM (bare-earth). Chosen over Copernicus DEM 30 m for finer
resolution adequate to the landslide scarps. To be reprojected to
EPSG:32633 in Phase 2.

## Dati vettoriali (rischio, amministrativi)
(da aggiungere — PAI/IFFI, confini ISTAT)