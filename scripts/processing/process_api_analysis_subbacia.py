#!/usr/bin/env python3
"""
Antecedent Precipitation Index (API) Analysis — Sub-bacia Level

Same methodology as process_api_analysis.py but aggregates rainfall to
sub-bacia level using area-weighted averages based on Thiessen polygon
intersections, then computes API on the composite sub-bacia rainfall series.

Strategy:
    1. Compute Thiessen x sub-bacia intersection area weights
    2. Spatially join flood occurrences to sub-bacias
    3. For each sub-bacia x day: weighted average daily rainfall total
    4. Compute API on the sub-bacia composite rainfall series
    5. Compute weighted average peak intensities per time-step
    6. Classify EA/ESA based on flood occurrences per sub-bacia

Outputs:
    - subbacia_weights.csv: area weights per (shi_cd, id_estacao)
    - daily_peak_intensities_subbacia.csv: weighted peak intensities per sub-bacia x day
    - daily_api_values_subbacia.csv: API values per sub-bacia x day x antecedent_days
    - api_analysis_events_subbacia.csv: classified events with intensities and API
"""

import os
import pathlib
import pandas as pd
import geopandas as gpd
import numpy as np
from tqdm.auto import tqdm

# ==============================================================================
# CONFIGURATION
# ==============================================================================

TIME_STEPS_MIN = [15, 30, 60, 120, 180, 360, 480, 600, 720, 1440]
TIME_STEP_COLS = [f'I_{d}min' if d < 60 else f'I_{d//60}h' for d in TIME_STEPS_MIN]

DECAY_RATE_K = 0.85
MAX_ANTECEDENT_DAYS = 10

MIN_DAILY_RAINFALL_MM = 10.0
MIN_FLOOD_RECORDS = 1

# Sub-bacia filter: list of shi_cd to include, or None to use all valid sub-bacias.
# Default excludes: 1 (water body), 103/110/152 (unnamed oceanic islands).
SUBBACIA_IDS_FILTER = None
SUBBACIA_IDS_EXCLUDE = [1, 103, 110, 152]

FLOOD_EVENT_TYPES = [
    "Bolsão d'água em via",
    'Alagamento',
    'Enchente',
    'Alagamentos e enchentes'
]

CRS_GEOGRAPHIC = "EPSG:4326"
CRS_PROJECTED = "EPSG:31983"

_project_root = pathlib.Path(__file__).parent.parent.parent

INPUT_DATA_DIR = '/home/luisresende/work/data/meteorologia/clean'
ALERTARIO_CSV = f'{INPUT_DATA_DIR}/clima_pluviometro/taxa_precipitacao_alertario.csv'
STATIONS_CSV = f'{INPUT_DATA_DIR}/clima_pluviometro/estacoes_alertario.csv'
OCORRENCIAS_CSV = f'{INPUT_DATA_DIR}/adm_cor_comando/ocorrencias.csv'
POPS_CSV = str(_project_root / 'data' / 'raw' / 'adm_cor_comando' / 'pops.csv')
THIESSEN_GPKG = '/home/luisresende/work/data/meteorologia/processed/thiessen_analysis/thiessen_polygons_rio.gpkg'
SUBBACIAS_GEOJSON = '/home/luisresende/work/data/meteorologia/raw/hidrologia/Sub_Bacias_Hidrográficas.geojson'

OUTPUT_DIR = str(_project_root / 'data' / 'processed' / 'api_analysis_subbacia')


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def compute_daily_peak_intensities(day_data, time_steps_min):
    """Compute peak rainfall intensity for a single station-day using sliding windows."""
    results = {}
    values = day_data.values

    for i, duration in enumerate(time_steps_min):
        window_size = duration // 15
        col = TIME_STEP_COLS[i]

        if window_size < 1 or window_size > len(values):
            results[col] = np.nan
            continue

        rolling_sum = pd.Series(values).rolling(window=window_size).sum()
        max_precip = rolling_sum.max()
        duration_h = duration / 60.0
        results[col] = max_precip / duration_h

    return results


def compute_api(daily_totals, target_date, k, n_days):
    """
    Compute Antecedent Precipitation Index for a given date.
    API = sum_{t=1}^{n_days} P_{target_date - t} * k^t
    """
    api = 0.0
    for t in range(1, n_days + 1):
        antecedent_date = (pd.Timestamp(target_date) - pd.Timedelta(days=t)).date()
        if antecedent_date in daily_totals.index:
            api += daily_totals[antecedent_date] * (k ** t)
        else:
            return np.nan
    return api


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print("=" * 80)
    print("API ANALYSIS — SUB-BACIA LEVEL PROCESSING PIPELINE")
    print("=" * 80)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"\nOutput directory: {OUTPUT_DIR}")

    # -------------------------------------------------------------------------
    # STEP 1: Load Input Data
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("STEP 1: Loading Input Data")
    print("=" * 80)

    print(f"\nLoading alertario data...")
    alertario = pd.read_csv(ALERTARIO_CSV)
    print(f"  Loaded {len(alertario):,} records")

    print(f"Loading stations data...")
    stations = pd.read_csv(STATIONS_CSV)
    print(f"  Loaded {len(stations)} stations")

    print(f"Loading ocorrencias data...")
    ocorrencias = pd.read_csv(OCORRENCIAS_CSV)
    print(f"  Loaded {len(ocorrencias):,} occurrences")

    print(f"Loading POPs data...")
    pops = pd.read_csv(POPS_CSV, index_col=0)
    print(f"  Loaded {len(pops)} POP types")

    print(f"Loading Thiessen polygons...")
    thiessen = gpd.read_file(THIESSEN_GPKG)
    print(f"  Loaded {len(thiessen)} polygons (CRS: {thiessen.crs})")

    print(f"Loading sub-bacias...")
    subbacias = gpd.read_file(SUBBACIAS_GEOJSON)
    print(f"  Loaded {len(subbacias)} sub-bacias (CRS: {subbacias.crs})")

    # -------------------------------------------------------------------------
    # STEP 2: Compute Thiessen x Sub-bacia Area Weights
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("STEP 2: Computing Thiessen x Sub-bacia Area Weights")
    print("=" * 80)

    # Reproject sub-bacias to match Thiessen CRS
    subbacias = subbacias.to_crs(thiessen.crs)

    # Apply sub-bacia filter
    if SUBBACIA_IDS_FILTER is not None:
        subbacias = subbacias[subbacias['shi_cd'].isin(SUBBACIA_IDS_FILTER)]
        print(f"  Filter applied: {len(subbacias)} sub-bacias retained")
    else:
        subbacias = subbacias[~subbacias['shi_cd'].isin(SUBBACIA_IDS_EXCLUDE)]
        print(f"  Excluded shi_cd {SUBBACIA_IDS_EXCLUDE}: {len(subbacias)} sub-bacias retained")

    # Intersect Thiessen polygons with sub-bacias
    intersection = gpd.overlay(
        subbacias[['shi_cd', 'shi_nm', 'geometry']],
        thiessen[['id_estacao', 'geometry']],
        how='intersection'
    )
    intersection['area'] = intersection.geometry.area
    intersection['total_area'] = intersection.groupby('shi_cd')['area'].transform('sum')
    intersection['weight'] = intersection['area'] / intersection['total_area']

    weights_df = intersection[['shi_cd', 'shi_nm', 'id_estacao', 'weight']].copy()
    weights_df = weights_df.sort_values(['shi_cd', 'weight'], ascending=[True, False]).reset_index(drop=True)

    weights_path = f'{OUTPUT_DIR}/subbacia_weights.csv'
    weights_df.to_csv(weights_path, index=False, float_format='%.6f')
    print(f"  {len(weights_df)} station-subbacia pairs across {weights_df['shi_cd'].nunique()} sub-bacias")
    print(f"  Saved {weights_path}")

    subbacia_ids = sorted(weights_df['shi_cd'].unique())

    # -------------------------------------------------------------------------
    # STEP 3: Process Precipitation Data
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("STEP 3: Processing Precipitation Data")
    print("=" * 80)

    alertario['horario'] = pd.to_timedelta(alertario['horario'])
    alertario['data_particao'] = pd.to_datetime(alertario['data_particao'])
    alertario['timestamp'] = pd.to_datetime(alertario['timestamp'])
    alertario['acumulado_chuva_15_min'] = pd.to_numeric(
        alertario['acumulado_chuva_15_min'], errors='coerce'
    ).fillna(0)
    alertario['date'] = alertario['timestamp'].dt.date

    station_name_map = stations.set_index('id_estacao')['estacao']
    alertario['estacao'] = alertario['id_estacao'].map(station_name_map)

    print(f"  Rain date range: {alertario['timestamp'].min()} -> {alertario['timestamp'].max()}")

    # -------------------------------------------------------------------------
    # STEP 4: Process Flood Occurrences & Spatial Join to Sub-bacias
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("STEP 4: Processing Flood Occurrences")
    print("=" * 80)

    ocorrencias['data_inicio'] = pd.to_datetime(ocorrencias['data_inicio'])
    ocorrencias['data_fim'] = pd.to_datetime(ocorrencias['data_fim'])
    ocorrencias['tipo'] = ocorrencias['id_pop'].map(pops.set_index('id')['titulo'])
    ocorrencias = ocorrencias[ocorrencias['tipo'].isin(FLOOD_EVENT_TYPES)]
    print(f"  Filtered to {len(ocorrencias):,} flood events")

    ocorrencias_gdf = gpd.GeoDataFrame(
        ocorrencias,
        geometry=gpd.points_from_xy(ocorrencias.longitude, ocorrencias.latitude),
        crs=CRS_GEOGRAPHIC
    ).to_crs(thiessen.crs)

    # Filter alertario to period covered by occurrences
    min_time_ocorrencias = ocorrencias['data_inicio'].min()
    alertario = alertario[alertario['timestamp'] > str(min_time_ocorrencias.year)]
    print(f"  Alertario filtered: {alertario['timestamp'].min()} -> {alertario['timestamp'].max()}")

    # Spatial join: floods -> sub-bacias
    subbacias_proj = subbacias[['shi_cd', 'shi_nm', 'geometry']]
    floods_with_subbacia = gpd.sjoin(
        ocorrencias_gdf,
        subbacias_proj,
        how='inner',
        predicate='within'
    )
    floods_with_subbacia = floods_with_subbacia[['id_evento', 'data_inicio', 'shi_cd', 'shi_nm']].reset_index(drop=True)
    floods_with_subbacia['flood_date'] = floods_with_subbacia['data_inicio'].dt.date
    print(f"  Associated {len(floods_with_subbacia):,} flood occurrences with sub-bacias")

    # -------------------------------------------------------------------------
    # STEP 5: Compute Station-level Daily Peak Intensities and Daily Totals
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("STEP 5: Computing Station-level Daily Peak Intensities")
    print("=" * 80)

    # Only process stations that appear in at least one sub-bacia
    station_ids_needed = set(weights_df['id_estacao'].unique())
    station_ids_available = set(alertario['id_estacao'].unique())
    station_ids = sorted(station_ids_needed & station_ids_available)
    print(f"  Stations needed: {len(station_ids_needed)}, available: {len(station_ids_available)}, processing: {len(station_ids)}")

    station_daily_peaks = []   # list of dicts: {id_estacao, date, I_*, daily_total_mm}
    station_daily_totals = {}  # {id_estacao: Series indexed by date}

    for station_id in tqdm(station_ids, desc="Station daily peaks"):
        station_data = alertario[alertario['id_estacao'] == station_id]
        grouped = station_data.groupby('date')

        daily_total_map = {}
        for day, day_group in grouped:
            day_sorted = day_group.sort_values('timestamp')
            rain_series = day_sorted['acumulado_chuva_15_min']
            daily_total = rain_series.sum()
            daily_total_map[day] = daily_total

            if len(rain_series) < 4:
                continue

            peaks = compute_daily_peak_intensities(rain_series, TIME_STEPS_MIN)
            peaks['id_estacao'] = station_id
            peaks['date'] = day
            peaks['daily_total_mm'] = daily_total
            station_daily_peaks.append(peaks)

        station_daily_totals[station_id] = pd.Series(daily_total_map)

    station_peaks_df = pd.DataFrame(station_daily_peaks)
    print(f"  Station-day records: {len(station_peaks_df):,}")

    # -------------------------------------------------------------------------
    # STEP 6: Aggregate to Sub-bacia Level (Weighted Average)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("STEP 6: Aggregating to Sub-bacia Level")
    print("=" * 80)

    # Merge station peaks with weights
    peaks_weighted = station_peaks_df.merge(
        weights_df[['shi_cd', 'shi_nm', 'id_estacao', 'weight']],
        on='id_estacao',
        how='inner'
    )

    # Filter by minimum daily rainfall at station level before aggregating
    peaks_weighted = peaks_weighted[peaks_weighted['daily_total_mm'] >= MIN_DAILY_RAINFALL_MM]

    # For each sub-bacia x day, compute weighted sum of intensities.
    # Re-normalize weights to account for stations that may be missing on a given day.
    intensity_cols = TIME_STEP_COLS + ['daily_total_mm']

    subbacia_daily_records = []

    for (shi_cd, day), group in tqdm(
        peaks_weighted.groupby(['shi_cd', 'date']),
        desc="Sub-bacia daily aggregation"
    ):
        total_weight = group['weight'].sum()
        if total_weight == 0:
            continue

        record = {'shi_cd': shi_cd, 'date': day}
        shi_nm = group['shi_nm'].iloc[0]
        record['shi_nm'] = shi_nm

        for col in intensity_cols:
            valid = group[col].notna()
            if not valid.any():
                record[col] = np.nan
            else:
                w = group.loc[valid, 'weight']
                w_norm = w / w.sum()
                record[col] = (group.loc[valid, col] * w_norm).sum()

        subbacia_daily_records.append(record)

    subbacia_peaks_df = pd.DataFrame(subbacia_daily_records)
    subbacia_peaks_df = subbacia_peaks_df[subbacia_peaks_df['daily_total_mm'] >= MIN_DAILY_RAINFALL_MM]
    print(f"  Sub-bacia day records (>= {MIN_DAILY_RAINFALL_MM} mm): {len(subbacia_peaks_df):,}")

    out_peaks = f'{OUTPUT_DIR}/daily_peak_intensities_subbacia.csv'
    subbacia_peaks_df.to_csv(out_peaks, index=False)
    print(f"  Saved {out_peaks}")

    # -------------------------------------------------------------------------
    # STEP 7: Compute Sub-bacia Composite Daily Rainfall Totals
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("STEP 7: Computing Sub-bacia Composite Daily Rainfall Series")
    print("=" * 80)

    # For each sub-bacia, build a composite daily total series (area-weighted)
    # covering ALL days (not just rainy ones) so API has full antecedent history.
    all_dates = set()
    for s in station_daily_totals.values():
        all_dates.update(s.index)

    subbacia_daily_composite = {}

    for shi_cd in tqdm(subbacia_ids, desc="Sub-bacia composite series"):
        sb_weights = weights_df[weights_df['shi_cd'] == shi_cd][['id_estacao', 'weight']]

        composite = {}
        for day in all_dates:
            total_w = 0.0
            weighted_sum = 0.0
            for _, wrow in sb_weights.iterrows():
                sid = wrow['id_estacao']
                w = wrow['weight']
                if sid in station_daily_totals and day in station_daily_totals[sid].index:
                    weighted_sum += station_daily_totals[sid][day] * w
                    total_w += w
            if total_w > 0:
                composite[day] = weighted_sum / total_w
            # If no station data for this day, leave it absent (API returns NaN)

        subbacia_daily_composite[shi_cd] = pd.Series(composite)

    print(f"  Built composite series for {len(subbacia_daily_composite)} sub-bacias")

    # -------------------------------------------------------------------------
    # STEP 8: Compute API per Sub-bacia
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("STEP 8: Computing API per Sub-bacia")
    print("=" * 80)
    print(f"  Decay rate k = {DECAY_RATE_K}, max antecedent days = {MAX_ANTECEDENT_DAYS}")

    qualifying = subbacia_peaks_df[['shi_cd', 'date']].drop_duplicates()

    api_records = []
    for shi_cd in tqdm(subbacia_ids, desc="Sub-bacia API"):
        composite_series = subbacia_daily_composite.get(shi_cd, pd.Series(dtype=float))
        if composite_series.empty:
            continue

        sb_qualifying = qualifying[qualifying['shi_cd'] == shi_cd]['date'].values
        for day in sb_qualifying:
            record = {'shi_cd': shi_cd, 'date': day}
            for n_days in range(1, MAX_ANTECEDENT_DAYS + 1):
                record[f'api_{n_days}d'] = compute_api(
                    composite_series, pd.Timestamp(day), DECAY_RATE_K, n_days
                )
            api_records.append(record)

    api_df = pd.DataFrame(api_records)
    print(f"  Computed API for {len(api_df):,} sub-bacia x day pairs")

    out_api = f'{OUTPUT_DIR}/daily_api_values_subbacia.csv'
    api_df.to_csv(out_api, index=False)
    print(f"  Saved {out_api}")

    # -------------------------------------------------------------------------
    # STEP 9: Classify Events (EA vs ESA)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("STEP 9: Classifying Events (EA vs ESA)")
    print("=" * 80)

    flood_counts = floods_with_subbacia.groupby(['flood_date', 'shi_cd']).size()
    ea_pairs = set(flood_counts[flood_counts >= MIN_FLOOD_RECORDS].index)
    print(f"  Unique flood day-subbacia pairs: {len(flood_counts):,}")
    print(f"  Pairs with >= {MIN_FLOOD_RECORDS} flood records (EA): {len(ea_pairs):,}")

    # Merge peaks with API
    subbacia_peaks_df['date'] = pd.to_datetime(subbacia_peaks_df['date']).dt.date
    api_df['date'] = pd.to_datetime(api_df['date']).dt.date

    events_df = subbacia_peaks_df.merge(api_df, on=['shi_cd', 'date'], how='inner')

    events_df['classificacao'] = events_df.apply(
        lambda row: 'EA' if (row['date'], row['shi_cd']) in ea_pairs else 'ESA',
        axis=1
    )

    n_ea = (events_df['classificacao'] == 'EA').sum()
    n_esa = (events_df['classificacao'] == 'ESA').sum()
    print(f"  Total classified events: {len(events_df):,}")
    print(f"  EA (>= {MIN_FLOOD_RECORDS} flood records): {n_ea:,}")
    print(f"  ESA (without flooding): {n_esa:,}")

    # -------------------------------------------------------------------------
    # STEP 10: Save Final Output
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("STEP 10: Saving Outputs")
    print("=" * 80)

    out_events = f'{OUTPUT_DIR}/api_analysis_events_subbacia.csv'
    events_df.to_csv(out_events, index=False)
    print(f"  Saved {out_events} ({len(events_df):,} records)")

    print("\n" + "=" * 80)
    print("PROCESSING COMPLETE")
    print("=" * 80)
    print(f"\n  Sub-bacias processed: {len(subbacia_ids)}")
    print(f"  Qualifying sub-bacia x day pairs: {len(events_df):,}")
    print(f"  EA events: {n_ea:,}")
    print(f"  ESA events: {n_esa:,}")
    print(f"  Output directory: {OUTPUT_DIR}")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
