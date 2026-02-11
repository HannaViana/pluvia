# Processing Scripts

This directory contains scripts for processing raw data into analysis-ready datasets.

## Scripts

### `process_id_analysis.py`

Processes rainfall and flood data to generate Intensity-Duration (I-D) analysis datasets.

**Purpose:** This script reproduces the data processing pipeline from `nbs/analysis/id-thresholds.py` and saves intermediate and final outputs to disk, eliminating the need to reprocess data each time a chart is generated.

**Outputs:**
- `data/processed/id_analysis/pontos_id_df.csv` - All I-D points with EA/ESA classifications
- `data/processed/id_analysis/classification_summary.csv` - Summary of events by station
- `data/processed/id_analysis/eventos_unicos.csv` - Unique rain events with metadata
- `data/processed/id_analysis/floods_with_station.csv` - Floods associated with stations

**Usage:**
```bash
# From project root
python scripts/processing/process_id_analysis.py

# Or make it executable and run directly
chmod +x scripts/processing/process_id_analysis.py
./scripts/processing/process_id_analysis.py
```

**Key Parameters** (edit at top of script):
- `MIN_DRY_PERIOD_HOURS = 1` - Hours of no rain to separate events
- `MIN_RAIN_THRESHOLD_MM = 1` - Minimum rain to consider as rainy period
- `DURATIONS_TO_ANALYZE_MIN = [15, 30, 60, 120, 180, 720]` - Duration windows in minutes
- `MIN_FLOOD_RECORDS = 2` - Minimum flood records to classify event as EA (with flooding)

**Requirements:**
- pandas
- geopandas
- numpy
- tqdm

**Input Data:**
- `data/meteorologia/clean/clima_pluviometro/taxa_precipitacao_alertario.csv`
- `data/meteorologia/clean/clima_pluviometro/estacoes_alertario.csv`
- `data/meteorologia/clean/adm_cor_comando/ocorrencias.csv`
- `data/raw/adm_cor_comando/pops.csv`
- `data/meteorologia/processed/thiessen_analysis/thiessen_polygons_rio.gpkg`

**Processing Steps:**
1. Load input data (rainfall, stations, flood occurrences, Thiessen polygons)
2. Process precipitation data (datetime conversions, station mapping)
3. Process flood occurrences (type filtering, GeoDataFrame creation)
4. Segment rain events and calculate I-D points using sliding windows
5. Associate floods with stations via spatial join (Thiessen polygons)
6. Classify rain events as EA (with flooding) or ESA (without flooding)
7. Save all outputs to disk

**Implementation Notes:**
- Faithfully reproduces the logic from `nbs/analysis/id-thresholds.py`
- Uses CSV format for all outputs (human-readable, no dependencies)
- All parameters are configurable at the top of the script
