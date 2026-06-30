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

## 2026-06-26 
- Confronto con perimetrazione ufficiale PC: il dNDVI cattura il corpo della frana su versante ma sottostima il settore urbano crollato (nord, SO) — conferma quantitativa del limite dell'ottico su superfici edificate. Risoluzione prevista: integrazione SAR (coerenza) in Fase 7

## 2026-06-26 — Fase 3: change detection e poligono frana

### Pipeline change detection
- Estratte e ritagliate le 12 bande Sentinel-2 (6 ×pre, 6 ×post) sull'aoi_event con
  05_extract_clip.py (glob per trovare le bande nei .SAFE, robusto ai path GRANULE).
- NDVI mascherato nuvole via SCL (codici invalidi 0,1,3,8,9,10; SCL 20m→10m nearest
  perché categorico). Mascherato pre 5,5% / post 1,9% → immagini pulite sul versante.
  Media NDVI pre 0,37 / post 0,43 (post più alto per crescita stagionale = rumore).
- dNDVI = post − pre. Media +0,06 (verde stagionale domina in superficie),
  min −1,01. Conteggi: <−0,2 = 1,41%, <−0,3 = 0,37%, <−0,4 = 0,07%.
  Visualizzato con palette divergente RdBu centrata su 0: frana = macchia rossa
  compatta sul versante ovest abitato (fronte a −0,42); campi blu = rumore stagionale.
- BSI + dBSI come conferma indipendente. dBSI e dNDVI risultano perimetri COINCIDENTI
  → la frana co-localizza perdita di vegetazione e comparsa di suolo nudo. BSI usato
  come conferma, non come recupero. Delimitazione basata su dNDVI.

### Limite ottico sul settore urbano
- Confronto con perimetrazione ufficiale Protezione Civile: il dNDVI cattura bene il
  corpo della frana su versante ma sottostima il settore urbano (transizione
  edificio→macerie = variazione spettrale modesta). Conferma quantitativa del limite
  dell'ottico su superfici edificate.
- Riesame ortofoto PC ad alta risoluzione (layer EME_FRANA_NISCEMI_2026): parte del
  presunto "urbano non rilevato" era OMBRA fotografica, non crollo. La frana reale è
  prevalentemente una striscia di suolo esposto su versante, ben rilevata dal dNDVI.
  Limite urbano ridimensionato. Recupero pieno del settore urbano rinviato a Fase 7
  (SAR/coerenza), con obiettivo documentato.

### Delimitazione del poligono (iterazioni)
- Soglia −0,3: frammentato, ~10 ha, schegge sparse.
- −0,2 + closing morfologico (8-connectivity, iter 3): corpo connesso ma rumore agricolo
  residuo (~21 ha, molti blob).
- Aggiunto vincolo di pendenza (slope_aoi ≥ 10°): rumore agricolo −82%, MA scarta la
  scarpata di distacco. SCOPERTA: il vincolo basato sul DEM PRE-evento penalizza la
  scarpata, che diventa ripida solo DOPO la frana (il DEM pre non la "vede" ripida).
  → vincolo di pendenza abbandonato per questa frana.
- Versione finale: −0,2 + closing senza vincolo slope → costone catturato bene +
  pochi falsi positivi agricoli, rimossi MANUALMENTE in QGIS (verificati su ortofoto PC).
- Risultato: 2 corpi coerenti con la frana (~13,3 + ~11,5 ha ≈ 24,8 ha),
  salvato in landslide_ndvi_final.gpkg.

### Validazione
- Qualitativa POSITIVA: il costone dNDVI coincide con la frana ufficiale PC (forma a
  fagiolo su versante ovest abitato). Dato vettoriale ufficiale non scaricabile dal sito
  → validazione quantitativa rinviata a Fase 4 (PAI/IFFI).

### Note metodologiche
- La delimitazione automatica di frane in contesto misto (agricolo+urbano) non è mai
  perfetta: rumore e frana hanno dNDVI sovrapposti. Workflow ibrido auto+manuale = prassi.
- Il vincolo morfologico va usato con cautela quando il DEM è pre-evento.

## 2026-06-29 — Q2 completata: statistiche zonali pendenza area frana

- Nuovo script 11_zonal_landslide.py (gemello del 04, applica le zonali al
  poligono frana; passa TUTTE le geometrie alla mask perché la frana ha 2 corpi).
- Risultato: frana media 11,9° / mediana 11,1° vs comune 6,9° / 5,3°.
  → pendenza media della frana ~72% più alta del comune.
- Distribuzione: frana spostata su classi medio-ripide (5-25° = 81,6%;
  15-35° = 29,5%), contro comune dove domina il piano (<5° = 47,7%).
  Classe >35° = 0% nella frana.
- Lettura: media≈mediana nella frana → versante omogeneamente inclinato
  (non outlier). Comune media>mediana → coda di poche zone ripide.
- Limiti: pendenze da DEM PRE-evento = suscettibilità antecedente, non
  morfologia post-frana. Risoluzione 10m + DEM pre spiegano l'assenza di >35°
  (la scarpata ripida è creata DALLA frana, non presente prima).
- Q2 conclusa: il versante franato è significativamente più inclinato del
  territorio comunale, confermando la predisposizione morfologica.

  L'area di frana presenta una pendenza media di 11,9° (mediana 11,1°), contro una media comunale di 6,9° (mediana 5,3°). La distribuzione è spostata verso le classi medio-ripide: il 30% dell'area di frana ricade in classi (15-35°) che nel comune occupano meno del 10% del territorio. Media e mediana quasi coincidenti indicano un versante omogeneamente inclinato. Le pendenze, valutate sul DEM pre-evento, descrivono la suscettibilità morfologica antecedente al collasso; la risoluzione di 10 m e l'uso del DEM pre-evento spiegano l'assenza delle classi più ripide (>35°), generate dalla frana stessa
  

## 2026-06-30 — Q3 (parte 1): overlay frana × PAI pericolosità

- Script 12_overlay_pai.py: intersezione poligono frana × PAI PERICOLOSITA
  (riproiettato 25833→32633, letto con bbox filter per efficienza).
- Risultato: frana 24,82 ha → P4 (molto elevata) 12,49 ha (50,3%),
  P2 (media) 5,67 ha (22,9%). Totale in zona PAI pericolosa: 73,2%.
  Non perimetrato: 6,66 ha (26,8%).
- Verifica visiva: intersezione coerente, contenuta nel poligono frana.
  Solo classi P2 e P4 presenti (genuino, non artefatto). Il 26,8% non coperto
  è prevalentemente marginale → la frana 2026 si è estesa oltre i limiti PAI
  (con incertezza ai bordi del poligono ottico).
- Nota: dati PAI shapefile aggiornati 12/05/2026, senza valore legale
  (riferimento ufficiale = PDF). Da dichiarare nel report.


## 2026-06-30 — Q3 (parte 2): overlay frana × PAI DISSESTI

- Script 13_overlay_dissesti.py: intersezione frana × dissesti già mappati.
- 72,8% della frana (18,06 ha) interseca dissesti inventariati — coerente
  col 73% del PAI pericolosità (conferma indipendente).
- Tipi (COD_TIP): 5 (colamento/scorrimento) 12,27 ha = corpo principale;
  11 (franosità diffusa) 5,67 ha; 1 (crollo) 0,12 ha.
  [NB: codici da confermare con legenda ufficiale PAI prima del report]
- Stato di attività (COD_ATT): TUTTI = 1 (ATTIVO), 18,06 ha. Dato chiave:
  i dissesti pre-esistenti colpiti erano tutti classificati attivi.
- DATA_EVENT vuoto (NaT) → data censimento non disponibile da questo campo.
- Conclusione: la frana 2026 ha riattivato dissesti noti e attivi, non un
  evento imprevisto.

  L'area collassata nel 2026 era, per circa il 73%, già nota e classificata ufficialmente come instabile: ricadeva in zone a pericolosità da frana PAI (50% in classe massima P4), coincideva con dissesti già inventariati, e — dato più rilevante — tutti questi dissesti pre-esistenti erano classificati come ATTIVI. Il corpo principale (~12 ha) corrisponde a un dissesto di tipo colamento/scorrimento già cartografato a sud del centro abitato. La frana ha dunque riattivato un fenomeno di instabilità noto e in evoluzione, non un evento imprevisto.

  ## 2026-06-30 — Q3 (parte 2): overlay frana × PAI DISSESTI

- Script 13_overlay_dissesti.py: intersezione frana × dissesti già mappati.
- 72,8% della frana (18,06 ha) interseca dissesti inventariati — coerente
  col 73% del PAI pericolosità (conferma indipendente).
- Stato di attività (COD_ATT): TUTTI = 1 (ATTIVO), 18,06 ha. Dato chiave,
  confermato da fonti normative: i dissesti attivi determinano la classe P4
  del PAI → coerente con il 50% di P4 trovato nell'overlay pericolosità.
- Tipi (COD_TIP): 5 = 12,27 ha (corpo principale), 11 = 5,67 ha, 1 = 0,12 ha.
  ATTENZIONE: legenda numerica COD_TIP da confermare con le Norme Tecniche di
  Attuazione del PAI (allegato "Tipologie di dissesti") in fase di report.
  Ipotesi IFFI standard (5≈colamento, 1≈crollo) NON ancora verificata.
- DATA_EVENT vuoto (NaT); eventuali date in DATA_DPR/DATA_DSG (decreti).
- Conclusione: la frana 2026 ha riattivato dissesti già


## 2026-06-30 — Q3 (parte 3): edifici coinvolti e in zona a rischio

- Script 14_buildings.py: edifici OSM (4220, da QuickOSM) vs frana e zone PAI.
- Criterio: intersezione (edificio coinvolto se tocca l'area).
- Edifici intersecanti l'area franata: 13 (impatto diretto rilevato da ottico;
  sottostima del danno urbano reale per i limiti dell'ottico sul costruito).
- Edifici in zone PAI P3+P4 (pericolosità elevata/molto elevata): 104.
- BUG risolto: campo PERICOLO di PERICOLOSITA.shp è TESTO ('4', non 4) →
  il filtro isin([3,4]) numerico dava 0; corretto in isin(["3","4"]).
  Lezione: verificare sempre dtype/valori di un campo prima di filtrarlo;
  uno zero incoerente con dati noti è segnale di bug, non risultato.
- Limite: copertura edifici OSM buona ma non garantita esaustiva (da dichiarare).
- Q3 COMPLETA.

Q3 — Contesto di rischio. L'area collassata nel 2026 era in larga parte già nota come pericolosa: il 73% ricadeva in zone classificate dal PAI (50% in classe massima P4), e una quota equivalente coincideva con dissesti già inventariati, tutti in stato "attivo". Il fenomeno ha quindi riattivato un'instabilità nota e cartografata, non un evento imprevisto. Sul costruito: l'area franata rilevata da satellite interseca 13 edifici (sottostima del danno urbano, per i limiti dell'ottico sul tessuto edificato), mentre 104 edifici sorgono complessivamente nelle zone PAI a pericolosità elevata/molto elevata (P3-P4) dell'area — una misura dell'esposizione al rischio già mappato.