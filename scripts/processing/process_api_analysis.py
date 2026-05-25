#!/usr/bin/env python3
"""
Antecedent Precipitation Index (API) Analysis Processing Script

Computes daily peak rainfall intensities for multiple time-steps, calculates
the Antecedent Precipitation Index (API), links flood occurrences to stations,
and classifies each day-station pair as EA (with flooding) or ESA (without).

Methodology follows Geraldo Moura Ramos Filho (2021) PhD thesis:
"Performance of rainfall threshold for flood identification from ground-
and satellite-based (sub)daily data" - UFPB.

Outputs:
    - daily_peak_intensities.csv: daily peak intensity per station per time-step
    - daily_api_values.csv: API values per day-station-antecedent_days
    - api_analysis_events.csv: classified events with intensities and API
"""

import os
import sys
import pathlib
import pandas as pd
import geopandas as gpd
import numpy as np
from tqdm.auto import tqdm

# ==============================================================================
# CONFIGURATION
# ==============================================================================

# Time-steps for peak intensity calculation (minutes)
TIME_STEPS_MIN = [15, 30, 60, 120, 180, 360, 480, 600, 720, 1440]
TIME_STEP_COLS = [f'I_{d}min' if d < 60 else f'I_{d//60}h' for d in TIME_STEPS_MIN]

# API parameters
DECAY_RATE_K = 0.85
MAX_ANTECEDENT_DAYS = 10

# Event filtering
MIN_DAILY_RAINFALL_MM = 10.0
MIN_FLOOD_RECORDS = 4

# Station filter: list of station IDs to include, or None to use all stations
STATION_IDS_FILTER = [4, 7, 9, 12, 21, 22, 24, 25, 27, 28, 31, 32, 33]

# Flood event types
FLOOD_EVENT_TYPES = [
    "Bolsão d'água em via",
    'Alagamento',
    'Enchente',
    'Alagamentos e enchentes'
]

# CRS Definitions
CRS_GEOGRAPHIC = "EPSG:4326"
CRS_PROJECTED = "EPSG:31983"

# Input Data Paths
_project_root = pathlib.Path(__file__).parent.parent.parent
INPUT_DATA_DIR = '/home/luisresende/work/data/meteorologia/clean'
ALERTARIO_CSV = f'{INPUT_DATA_DIR}/clima_pluviometro/taxa_precipitacao_alertario.csv'
STATIONS_CSV = f'{INPUT_DATA_DIR}/clima_pluviometro/estacoes_alertario.csv'
OCORRENCIAS_CSV = f'{INPUT_DATA_DIR}/adm_cor_comando/ocorrencias.csv'
POPS_CSV = str(_project_root / 'data' / 'raw' / 'adm_cor_comando' / 'pops.csv')
THIESSEN_GPKG = '/home/luisresende/work/data/meteorologia/processed/thiessen_analysis/thiessen_polygons_rio.gpkg'

# Output paths
OUTPUT_DIR = str(_project_root / 'data' / 'processed' / 'api_analysis')

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def compute_daily_peak_intensities(day_data, time_steps_min):
    """
    Compute peak rainfall intensity for a single station-day using sliding windows.

    Args:
        day_data: Series of 15-min rainfall values for one day (up to 96 values)
        time_steps_min: list of duration windows in minutes

    Returns:
        dict mapping time-step column name to max intensity (mm/h)
    """
    results = {}
    values = day_data.values

    for i, duration in enumerate(time_steps_min):
        window_size = duration // 15

        if window_size < 1 or window_size > len(values):
            col = TIME_STEP_COLS[i]
            results[col] = np.nan
            continue

        rolling_sum = pd.Series(values).rolling(window=window_size).sum()
        max_precip = rolling_sum.max()
        duration_h = duration / 60.0
        max_intensity = max_precip / duration_h

        col = TIME_STEP_COLS[i]
        results[col] = max_intensity

    return results


def compute_api(daily_totals, target_date, k, n_days):
    """
    Compute Antecedent Precipitation Index for a given date.

    API = sum_{t=1}^{n_days} P_{target_date - t} * k^t

    Args:
        daily_totals: Series indexed by date with daily rainfall totals
        target_date: the date for which to compute API
        k: decay rate (0.80-0.98)
        n_days: number of antecedent days

    Returns:
        float: API value in mm, or NaN if insufficient data
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
# MAIN PROCESSING PIPELINE
# ==============================================================================

def main():
    print("=" * 80)
    print("API ANALYSIS PROCESSING PIPELINE")
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
    thiessen_polygons_gdf = gpd.read_file(THIESSEN_GPKG)
    print(f"  Loaded {len(thiessen_polygons_gdf)} polygons")

    # -------------------------------------------------------------------------
    # STEP 2: Process Precipitation Data
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("STEP 2: Processing Precipitation Data")
    print("=" * 80)

    alertario['horario'] = pd.to_timedelta(alertario['horario'])
    alertario['data_particao'] = pd.to_datetime(alertario['data_particao'])
    alertario['timestamp'] = pd.to_datetime(alertario['timestamp'])
    alertario['acumulado_chuva_15_min'] = pd.to_numeric(
        alertario['acumulado_chuva_15_min'], errors='coerce'
    ).fillna(0)

    station_name_map = stations.set_index('id_estacao')['estacao']
    alertario['estacao'] = alertario['id_estacao'].map(station_name_map)

    alertario['date'] = alertario['timestamp'].dt.date

    print(f"  Rain Date Range: {alertario['timestamp'].min()} -> {alertario['timestamp'].max()}")

    # -------------------------------------------------------------------------
    # STEP 3: Process Flood Occurrences & Spatial Join
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("STEP 3: Processing Flood Occurrences")
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
    )

    # Filter alertario to period covered by occurrences
    min_time_ocorrencias = ocorrencias['data_inicio'].min()
    alertario = alertario[alertario['timestamp'] > str(min_time_ocorrencias.year)]
    print(f"  Alertario filtered: {alertario['timestamp'].min()} -> {alertario['timestamp'].max()}")

    # Spatial join: floods -> stations via Thiessen polygons
    if ocorrencias_gdf.crs != CRS_PROJECTED:
        ocorrencias_gdf = ocorrencias_gdf.to_crs(CRS_PROJECTED)
    if thiessen_polygons_gdf.crs != CRS_PROJECTED:
        thiessen_polygons_gdf = thiessen_polygons_gdf.to_crs(CRS_PROJECTED)

    floods_with_station = gpd.sjoin(
        ocorrencias_gdf,
        thiessen_polygons_gdf[['id_estacao', 'geometry']],
        how='inner',
        predicate='within'
    )
    floods_with_station = floods_with_station[['id_evento', 'data_inicio', 'id_estacao']].reset_index(drop=True)
    floods_with_station['flood_date'] = floods_with_station['data_inicio'].dt.date
    print(f"  Associated {len(floods_with_station):,} flood occurrences with stations")

    # -------------------------------------------------------------------------
    # STEP 4: Compute Daily Peak Intensities
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("STEP 4: Computing Daily Peak Intensities")
    print("=" * 80)
    print(f"  Time-steps: {TIME_STEPS_MIN} min")

    station_ids = alertario['id_estacao'].unique()
    if STATION_IDS_FILTER is not None:
        station_ids = [s for s in station_ids if s in STATION_IDS_FILTER]
        print(f"  Station filter applied: {len(station_ids)} stations")
    all_daily_records = []

    for station_id in tqdm(station_ids, desc="Computing daily peaks"):
        station_data = alertario[alertario['id_estacao'] == station_id]
        grouped_by_day = station_data.groupby('date')

        for day, day_group in grouped_by_day:
            day_sorted = day_group.sort_values('timestamp')
            rain_series = day_sorted['acumulado_chuva_15_min']

            if len(rain_series) < 4:
                continue

            daily_total = rain_series.sum()

            peaks = compute_daily_peak_intensities(rain_series, TIME_STEPS_MIN)
            peaks['date'] = day
            peaks['id_estacao'] = station_id
            peaks['daily_total_mm'] = daily_total
            all_daily_records.append(peaks)

    daily_peaks_df = pd.DataFrame(all_daily_records)
    print(f"  Total day-station records: {len(daily_peaks_df):,}")

    # Filter by minimum daily rainfall
    daily_peaks_df = daily_peaks_df[daily_peaks_df['daily_total_mm'] >= MIN_DAILY_RAINFALL_MM]
    print(f"  After filtering (>= {MIN_DAILY_RAINFALL_MM} mm): {len(daily_peaks_df):,} records")

    # -------------------------------------------------------------------------
    # STEP 5: Compute API Values
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("STEP 5: Computing API Values")
    print("=" * 80)
    print(f"  Decay rate k = {DECAY_RATE_K}")
    print(f"  Max antecedent days = {MAX_ANTECEDENT_DAYS}")

    # Build daily totals per station (including days below threshold, needed for API)
    all_station_daily_totals = alertario.groupby(['id_estacao', 'date'])['acumulado_chuva_15_min'].sum()

    api_records = []
    qualifying_dates = daily_peaks_df[['date', 'id_estacao']].drop_duplicates()

    for station_id in tqdm(station_ids, desc="Computing API"):
        station_daily = all_station_daily_totals.loc[station_id] if station_id in all_station_daily_totals.index.get_level_values(0) else pd.Series(dtype=float)
        if station_daily.empty:
            continue

        station_qualifying = qualifying_dates[qualifying_dates['id_estacao'] == station_id]['date'].values

        for day in station_qualifying:
            record = {'date': day, 'id_estacao': station_id}
            for n_days in range(1, MAX_ANTECEDENT_DAYS + 1):
                api_val = compute_api(station_daily, pd.Timestamp(day), DECAY_RATE_K, n_days)
                record[f'api_{n_days}d'] = api_val
            api_records.append(record)

    api_df = pd.DataFrame(api_records)
    print(f"  Computed API for {len(api_df):,} day-station pairs")

    # -------------------------------------------------------------------------
    # STEP 6: Classify Events (EA vs ESA)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("STEP 6: Classifying Events (EA vs ESA)")
    print("=" * 80)

    # Create set of (date, station) pairs with at least MIN_FLOOD_RECORDS flood occurrences
    flood_counts = floods_with_station.groupby(['flood_date', 'id_estacao']).size()
    ea_pairs = set(flood_counts[flood_counts >= MIN_FLOOD_RECORDS].index)
    print(f"  Unique flood day-station pairs: {len(flood_counts):,}")
    print(f"  Pairs with >= {MIN_FLOOD_RECORDS} flood records (EA): {len(ea_pairs):,}")

    # Merge peak intensities with API values
    daily_peaks_df['date'] = pd.to_datetime(daily_peaks_df['date']).dt.date
    api_df['date'] = pd.to_datetime(api_df['date']).dt.date

    events_df = daily_peaks_df.merge(api_df, on=['date', 'id_estacao'], how='inner')

    # Classify
    events_df['classificacao'] = events_df.apply(
        lambda row: 'EA' if (row['date'], row['id_estacao']) in ea_pairs else 'ESA',
        axis=1
    )

    n_ea = (events_df['classificacao'] == 'EA').sum()
    n_esa = (events_df['classificacao'] == 'ESA').sum()
    print(f"  Total classified events: {len(events_df):,}")
    print(f"  EA (>= {MIN_FLOOD_RECORDS} flood records): {n_ea:,}")
    print(f"  ESA (without flooding): {n_esa:,}")

    # -------------------------------------------------------------------------
    # STEP 7: Save Outputs
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("STEP 7: Saving Outputs")
    print("=" * 80)

    out_peaks = f'{OUTPUT_DIR}/daily_peak_intensities.csv'
    daily_peaks_df.to_csv(out_peaks, index=False)
    print(f"  Saved {out_peaks} ({len(daily_peaks_df):,} records)")

    out_api = f'{OUTPUT_DIR}/daily_api_values.csv'
    api_df.to_csv(out_api, index=False)
    print(f"  Saved {out_api} ({len(api_df):,} records)")

    out_events = f'{OUTPUT_DIR}/api_analysis_events.csv'
    events_df.to_csv(out_events, index=False)
    print(f"  Saved {out_events} ({len(events_df):,} records)")

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("PROCESSING COMPLETE")
    print("=" * 80)
    print(f"\n  Stations processed: {len(station_ids)}")
    print(f"  Qualifying day-station pairs: {len(events_df):,}")
    print(f"  EA events: {n_ea:,}")
    print(f"  ESA events: {n_esa:,}")
    print(f"  Output directory: {OUTPUT_DIR}")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
