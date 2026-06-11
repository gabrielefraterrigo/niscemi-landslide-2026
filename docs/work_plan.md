# Work Plan — Niscemi Landslide 2026

## 1. Background e motivazione
Il caso studio in oggetto è la frana avvenuta a Niscemi(CL) iniziata nelle prime ore del 16 gennaio 2026 e culminata il 25 gennaio quando una seconda frana di entità maggiore ha riattivato un vecchio fronte a sud del centro abitato causando devastazioni tali da richiedere l'evaquazione di 1.500 persone. L'evento è estremamente attuale e rilevante poichè a Giugno 2026 la frana non si è ancora arrestata e poichè ha causato lo stato di emergenza nazionale

## 2. Obiettivo del progetto
caratterizzare l'evento franoso e il suo contesto di suscettibilità usando dati satellitari open, DEM e dati ufficiali, producendo un'analisi riproducibile (codice Python/GEE) e cartografia professionale.

## 3. Domande di ricerca
La prima domanda è di natura descrittiva, ovvero quali sono la geometria e l'estensione dell'area della frana del 2026, osservabile tramite dati satellitari SAR e ottici?

La seconda riguarda la morfologia,quali caratteristiche morfometriche (pendenza, esposizione, curvatura) caratterizzano il versante coinvolto, e come si confronta l'area in frana con il resto del territorio comunale?

La terza interroga sui rischi, quanta parte dell'area collassata nel 2026 ricadeva già nelle perimetrazioni di pericolosità del PAI e dell'inventario IFFI? Quanti edifici ricadevano in zone classificate a rischio?

## 4. Area di studio
Poichè le domande di ricerca hanno scale diverse definisco due AOI che avranno scale diverse, scala evento e scala contesto.

## 5. Sistema di riferimento
Come CRS scelgo EPSG:32633 come CRS di progetto per minimizzare le riproiezioni dei raster, riproiettando invece i vettoriali (PAI, edifici) che sopportano la trasformazione senza perdita.

## 6. Dati previsti
(elenco preliminare: Sentinel-2, Sentinel-1, DEM TINITALY, PAI/IFFI, piogge —
con una riga ciascuno sul ruolo che avrà)

## 7. Fasi e deliverable
(tabella o elenco sintetico delle fasi 1-7 con output atteso)

## 8. Limiti dichiarati
(cosa il progetto NON fa: niente analisi delle cause geologiche, ecc.)