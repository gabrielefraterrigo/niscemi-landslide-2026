# Project log

## 2026-06-11 — Phase 0 (2h)
- Repo setup, venv, AOI script

## 2026-06-18 - Phase 1 Selezione coppia Sentinel-2 (PRE/POST)
- 11 gen scartata: nuvola opaca sul versante franato
- 01 gen scartata: nuvoletta sottile residua sul versante (rischio cirri)
- 27 dic SCELTA come PRE: versante libero, verificato vs mappa Protezione Civile
- 25 feb SCELTA come POST: versante sgombro
- Intervallo ~60 gg → variabilità stagionale da dichiarare nel report
- Entrambe S2B (sensore omogeneo)


## Percorsi GRANULE (per script Fase 3)
- PRE (27/12/2025): data\raw\S2B_MSIL2A_20251227T095329_N0511_R079_T33SVB_20251227T122351.SAFE\GRANULE\L2A_T33SVB_A046008_20251227T095934\IMG_DATA\R10m
- POST (25/02/2026): data\raw\S2B_MSIL2A_20260225T095029_N0512_R079_T33SVB_20260225T141422.SAFE\GRANULE\L2A_T33SVB_A046866_20260225T095231\IMG_DATA\R10m

## 2026-06-21 - Phase 2 riproiezione CRS e calcolo DEM PRE
- riproiezione CRS DEM da EPSG:32632 a 32633
- slope calcolato (QGIS/gdaldem, gradi, Horn), min 0 / max 56°, letture puntuali 27° versante vs 0,5° piana, classi 5/15/25/35, e la nota sul DEM pre-evento


## 2026-06-22 
- morfologia: slope (con zonali), hillshade, aspect (esposizione NW estratta), curvature    calcolate ma interpretazione rimandata a sviluppo futuro per rumorosità del dato a 10 m

## 2026-06-22 Phase 3 Change detection
- NDVI mascherati prodotti, % mascherata bassa, nota sul rumore stagionale che alza la media POST