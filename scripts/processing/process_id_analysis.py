#!/usr/bin/env python3
"""
Intensity-Duration (I-D) Analysis Processing Script

This script processes rainfall and flood data to generate I-D analysis datasets.
It reproduces the processing pipeline from nbs/analysis/id-thresholds.py and saves
intermediate and final outputs to disk for reuse in chart generation.

Outputs:
    - pontos_id_df.csv: All I-D points with classifications
    - classification_summary.csv: Summary of EA/ESA events by station
    - eventos_unicos.csv: Unique rain events with metadata
    - floods_with_station.csv: Floods associated with stations
"""

import os
import sys
import pandas as pd
import geopandas as gpd
import numpy as np
from tqdm.auto import tqdm

# ==============================================================================
# CONFIGURATION - Edit these parameters as needed
# ==============================================================================

# Analysis Parameters
MIN_DRY_PERIOD_HOURS = 1        # Hours of no rain to separate events
MIN_RAIN_THRESHOLD_MM = 1       # Minimum rain (mm) to consider as rainy period
DURATIONS_TO_ANALYZE_MIN = [15, 30, 60, 120, 180, 720]  # Duration windows in minutes
MIN_FLOOD_RECORDS = 2           # Minimum flood records to classify event as EA

# Flood event types to consider
FLOOD_EVENT_TYPES = [
    "Bolsão d'água em via",
    'Alagamento',
    'Enchente',
    'Alagamentos e enchentes'
]

# CRS Definitions
CRS_GEOGRAPHIC = "EPSG:4326"    # WGS84
CRS_PROJECTED = "EPSG:31983"    # SIRGAS 2000 / UTM zone 23S

# Input Data Paths
# Note: Data is stored outside project directory structure
# Using absolute paths for reliability
import pathlib
_project_root = pathlib.Path(__file__).parent.parent.parent
INPUT_DATA_DIR = '/home/luisresende/work/data/meteorologia/clean'
ALERTARIO_CSV = f'{INPUT_DATA_DIR}/clima_pluviometro/taxa_precipitacao_alertario.csv'
STATIONS_CSV = f'{INPUT_DATA_DIR}/clima_pluviometro/estacoes_alertario.csv'
OCORRENCIAS_CSV = f'{INPUT_DATA_DIR}/adm_cor_comando/ocorrencias.csv'
POPS_CSV = str(_project_root / 'data' / 'raw' / 'adm_cor_comando' / 'pops.csv')
THIESSEN_GPKG = '/home/luisresende/work/data/meteorologia/processed/thiessen_analysis/thiessen_polygons_rio.gpkg'

# Output Data Paths (relative to project root)
OUTPUT_DIR = str(_project_root / 'data' / 'processed' / 'id_analysis')
PONTOS_ID_OUTPUT = f'{OUTPUT_DIR}/pontos_id_df.csv'
CLASSIFICATION_SUMMARY_OUTPUT = f'{OUTPUT_DIR}/classification_summary.csv'
EVENTOS_UNICOS_OUTPUT = f'{OUTPUT_DIR}/eventos_unicos.csv'
FLOODS_WITH_STATION_OUTPUT = f'{OUTPUT_DIR}/floods_with_station.csv'

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def calcular_pontos_id_evento(event_slice: pd.Series, durations_min: list) -> list:
    """
    Calcula os pontos (D, I) para um único evento de chuva usando o método de janelas deslizantes.

    Args:
        event_slice (pd.Series): Série temporal com a chuva acumulada a cada 15 min para um evento.
        durations_min (list): Lista de durações em minutos a serem analisadas (ex: [15, 30, 60]).

    Returns:
        list: Lista de dicionários, cada um contendo um par 'duracao_h' e 'intensidade_mm_h'.
    """
    id_points = []

    for duration in durations_min:
        # Calcula o tamanho da janela em número de intervalos de 15 min
        window_size = int(duration / 15)

        if window_size < 1 or window_size > len(event_slice):
            continue  # Pula durações menores que a resolução ou maiores que o próprio evento

        # Calcula a soma deslizante da precipitação
        rolling_sum = event_slice.rolling(window=window_size).sum()

        # Encontra a precipitação máxima acumulada para essa duração
        max_precip_for_duration = rolling_sum.max()

        # Converte a precipitação acumulada em intensidade média (mm/h)
        # Intensidade = (Chuva Total na Janela) / (Duração da Janela em horas)
        duration_h = duration / 60.0
        max_intensity = max_precip_for_duration / duration_h

        id_points.append({
            'duracao_h': duration_h,
            'intensidade_mm_h': max_intensity
        })

    return id_points


def segmenta_e_calcula_id(
    df_estacao: pd.DataFrame,
    id_estacao: int,
    min_rain: float,
    min_dry_period_hours: int,
    durations_to_analyze_min: list
) -> pd.DataFrame:
    """
    Identifica eventos de chuva e, para cada um, calcula os múltiplos pontos I-D.
    Mantém a lógica original de segmentação de eventos, que estava correta.
    """
    if df_estacao.empty or 'acumulado_chuva_15_min' not in df_estacao.columns:
        return pd.DataFrame()

    df = df_estacao.sort_index()
    df['is_raining'] = df['acumulado_chuva_15_min'] >= min_rain
    rainy_periods = df[df['is_raining']]

    if rainy_periods.empty:
        return pd.DataFrame()

    time_diffs = rainy_periods.index.to_series().diff()
    min_dry_period = pd.Timedelta(hours=min_dry_period_hours)
    is_new_event_series = time_diffs > min_dry_period
    event_ids = is_new_event_series.cumsum()
    rainy_periods_with_id = rainy_periods.assign(event_id=event_ids)

    all_event_points = []

    for event_id, event_group in rainy_periods_with_id.groupby('event_id'):
        start_time = event_group.index.min()
        end_time = event_group.index.max()

        # Pega a série temporal completa do evento (incluindo zeros internos)
        event_slice = df.loc[start_time:end_time, 'acumulado_chuva_15_min']

        # Calcula os pontos I-D para este evento
        id_points = calcular_pontos_id_evento(event_slice, durations_to_analyze_min)

        # Adiciona informações do evento a cada ponto I-D gerado
        for point in id_points:
            point['id_estacao'] = id_estacao
            point['id_evento_chuva'] = f"{id_estacao}_{int(start_time.timestamp())}"  # ID único para o evento original
            point['start_time'] = start_time
            point['end_time'] = end_time + pd.Timedelta(minutes=15)
            all_event_points.append(point)

    return pd.DataFrame(all_event_points)


# ==============================================================================
# MAIN PROCESSING PIPELINE
# ==============================================================================

def main():
    print("="*80)
    print("I-D ANALYSIS PROCESSING PIPELINE")
    print("="*80)

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"\n✓ Output directory: {OUTPUT_DIR}")

    # -------------------------------------------------------------------------
    # STEP 1: Load Input Data
    # -------------------------------------------------------------------------
    print("\n" + "="*80)
    print("STEP 1: Loading Input Data")
    print("="*80)

    print(f"\nLoading alertario data from {ALERTARIO_CSV}...")
    alertario = pd.read_csv(ALERTARIO_CSV)
    print(f"  ✓ Loaded {len(alertario):,} records")

    print(f"\nLoading stations data from {STATIONS_CSV}...")
    stations = pd.read_csv(STATIONS_CSV)
    print(f"  ✓ Loaded {len(stations)} stations")

    print(f"\nLoading ocorrencias data from {OCORRENCIAS_CSV}...")
    ocorrencias = pd.read_csv(OCORRENCIAS_CSV)
    print(f"  ✓ Loaded {len(ocorrencias):,} occurrences")

    print(f"\nLoading POPs data from {POPS_CSV}...")
    pops = pd.read_csv(POPS_CSV, index_col=0)
    print(f"  ✓ Loaded {len(pops)} POP types")

    print(f"\nLoading Thiessen polygons from {THIESSEN_GPKG}...")
    thiessen_polygons_gdf = gpd.read_file(THIESSEN_GPKG)
    print(f"  ✓ Loaded {len(thiessen_polygons_gdf)} polygons")

    # -------------------------------------------------------------------------
    # STEP 2: Process Precipitation Data
    # -------------------------------------------------------------------------
    print("\n" + "="*80)
    print("STEP 2: Processing Precipitation Data")
    print("="*80)

    # Convert datetime fields
    alertario['horario'] = pd.to_timedelta(alertario['horario'])
    alertario['data_particao'] = pd.to_datetime(alertario['data_particao'])
    alertario['timestamp'] = pd.to_datetime(alertario['timestamp'])

    # Map station information
    station_name_map = stations.set_index('id_estacao')['estacao']
    station_latitude_map = stations.set_index('id_estacao')['latitude']
    station_longitude_map = stations.set_index('id_estacao')['longitude']

    alertario['estacao'] = alertario['id_estacao'].map(station_name_map)
    alertario['latitude'] = alertario['id_estacao'].map(station_latitude_map)
    alertario['longitude'] = alertario['id_estacao'].map(station_longitude_map)

    # Reorder columns
    alertario = alertario[[
        'primary_key',
        'id_estacao',
        'estacao',
        'latitude',
        'longitude',
        'horario',
        'data_particao',
        'timestamp',
        'acumulado_chuva_15_min',
        'acumulado_chuva_1_h',
        'acumulado_chuva_4_h',
        'acumulado_chuva_24_h',
        'acumulado_chuva_96_h'
    ]]

    print(f"  ✓ Processed alertario data")
    print(f"  Rain Date Range: {alertario['timestamp'].min()} -> {alertario['timestamp'].max()}")

    # -------------------------------------------------------------------------
    # STEP 3: Process Flood Occurrences
    # -------------------------------------------------------------------------
    print("\n" + "="*80)
    print("STEP 3: Processing Flood Occurrences")
    print("="*80)

    # Convert datetime fields
    ocorrencias['data_inicio'] = pd.to_datetime(ocorrencias['data_inicio'])
    ocorrencias['data_fim'] = pd.to_datetime(ocorrencias['data_fim'])

    # Map event type
    ocorrencias['tipo'] = ocorrencias['id_pop'].map(pops.set_index('id')['titulo'])

    # Filter occurrences by type
    ocorrencias = ocorrencias[ocorrencias['tipo'].isin(FLOOD_EVENT_TYPES)]
    print(f"  ✓ Filtered to {len(ocorrencias):,} flood events")

    # Convert to GeoDataFrame
    ocorrencias_gdf = gpd.GeoDataFrame(
        ocorrencias,
        geometry=gpd.points_from_xy(ocorrencias.longitude, ocorrencias.latitude),
        crs=CRS_GEOGRAPHIC
    )

    # Filter alertario by time period
    min_time_ocorrencias = ocorrencias['data_inicio'].min()
    alertario = alertario[alertario['timestamp'] > str(min_time_ocorrencias.year)]
    print(f"  ✓ Filtered alertario to period: {alertario['timestamp'].min()} -> {alertario['timestamp'].max()}")

    # -------------------------------------------------------------------------
    # STEP 4: Segment Rain Events and Calculate I-D Points
    # -------------------------------------------------------------------------
    print("\n" + "="*80)
    print("STEP 4: Segmenting Rain Events and Calculating I-D Points")
    print("="*80)
    print(f"\nParameters:")
    print(f"  - Min dry period: {MIN_DRY_PERIOD_HOURS} hour(s)")
    print(f"  - Min rain threshold: {MIN_RAIN_THRESHOLD_MM} mm")
    print(f"  - Duration windows: {DURATIONS_TO_ANALYZE_MIN} min")

    # Prepare alertario data
    if not pd.api.types.is_datetime64_any_dtype(alertario['timestamp']):
        alertario['timestamp'] = pd.to_datetime(alertario['timestamp'])
    alertario_indexed = alertario.set_index('timestamp')

    # Get unique stations
    station_ids = alertario['id_estacao'].unique()

    # Process each station
    lista_pontos_id = []
    print(f"\nProcessing {len(station_ids)} stations...")
    for station_id in tqdm(station_ids, desc="Processing Stations"):
        df_station_data = alertario_indexed[alertario_indexed['id_estacao'] == station_id]

        station_id_points = segmenta_e_calcula_id(
            df_station_data,
            station_id,
            MIN_RAIN_THRESHOLD_MM,
            MIN_DRY_PERIOD_HOURS,
            DURATIONS_TO_ANALYZE_MIN
        )

        if not station_id_points.empty:
            lista_pontos_id.append(station_id_points)

    # Concatenate results
    pontos_id_df = pd.concat(lista_pontos_id, ignore_index=True)

    # Rename intensity column for compatibility
    pontos_id_df = pontos_id_df.rename(columns={'intensidade_mm_h': 'intensidade_max_mm_h'})

    print(f"\n  ✓ I-D Analysis completed")
    print(f"  Total I-D points generated: {len(pontos_id_df):,}")
    print(f"  Total unique rain events: {pontos_id_df['id_evento_chuva'].nunique():,}")

    # -------------------------------------------------------------------------
    # STEP 5: Associate Floods with Stations (Spatial Join)
    # -------------------------------------------------------------------------
    print("\n" + "="*80)
    print("STEP 5: Associating Floods with Stations (Spatial Join)")
    print("="*80)

    # Ensure same CRS
    if ocorrencias_gdf.crs != CRS_PROJECTED:
        ocorrencias_gdf = ocorrencias_gdf.to_crs(CRS_PROJECTED)
    if thiessen_polygons_gdf.crs != CRS_PROJECTED:
        thiessen_polygons_gdf = thiessen_polygons_gdf.to_crs(CRS_PROJECTED)

    # Spatial join
    floods_with_station_gdf = gpd.sjoin(
        ocorrencias_gdf,
        thiessen_polygons_gdf[['id_estacao', 'geometry']],
        how='inner',
        predicate='within'
    )

    # Select and rename columns
    floods_with_station_gdf = floods_with_station_gdf[['id_evento', 'data_inicio', 'id_estacao', 'geometry']].reset_index(drop=True)

    print(f"  ✓ Associated {len(floods_with_station_gdf):,} flood occurrences with stations")

    # -------------------------------------------------------------------------
    # STEP 6: Classify Rain Events (EA vs ESA)
    # -------------------------------------------------------------------------
    print("\n" + "="*80)
    print("STEP 6: Classifying Rain Events (EA vs ESA)")
    print("="*80)
    print(f"\nMinimum flood records for EA classification: {MIN_FLOOD_RECORDS}")

    # Create DataFrame of unique rain events
    eventos_unicos_df = pontos_id_df.drop_duplicates(subset=['id_evento_chuva']).copy()
    eventos_unicos_df = eventos_unicos_df[['id_evento_chuva', 'id_estacao', 'start_time', 'end_time']]

    # Prepare data for temporal matching
    floods_to_check = floods_with_station_gdf[['data_inicio', 'id_estacao']]

    eventos_unicos_df['id_estacao'] = eventos_unicos_df['id_estacao'].astype(str)
    floods_to_check['id_estacao'] = floods_to_check['id_estacao'].astype(str)

    # Handle timezones
    for df in [eventos_unicos_df, floods_to_check]:
        for col in ['start_time', 'end_time', 'data_inicio']:
            if col in df.columns:
                if df[col].dt.tz is None:
                    df[col] = df[col].dt.tz_localize('UTC')
                else:
                    df[col] = df[col].dt.tz_convert('UTC')

    # Merge to create pairs of rain events and floods in the same station area
    merged_pairs = pd.merge(eventos_unicos_df, floods_to_check, on='id_estacao')

    # Filter for temporal overlap
    temporal_overlap_condition = (
        (merged_pairs['data_inicio'] >= merged_pairs['start_time']) &
        (merged_pairs['data_inicio'] < merged_pairs['end_time'])
    )
    eventos_com_alagamento = merged_pairs[temporal_overlap_condition]

    # Count flood records per rain event
    flood_counts = eventos_com_alagamento.groupby('id_evento_chuva').size()

    # Get IDs of rain events with at least MIN_FLOOD_RECORDS
    ids_eventos_ea = flood_counts[flood_counts >= MIN_FLOOD_RECORDS].index.unique()

    # Propagate classification to main I-D points DataFrame
    pontos_id_df['classificacao'] = 'ESA'
    pontos_id_df.loc[pontos_id_df['id_evento_chuva'].isin(ids_eventos_ea), 'classificacao'] = 'EA'

    # Print summary
    classification_counts = pontos_id_df['classificacao'].value_counts()
    print(f"\n  ✓ Classification completed")
    print(f"  I-D Points without flooding (ESA): {classification_counts.get('ESA', 0):,}")
    print(f"  I-D Points with flooding (EA): {classification_counts.get('EA', 0):,}")

    # Create classification summary by station
    eventos_classificados_df = pontos_id_df.drop_duplicates(subset=['id_evento_chuva'])
    classification_summary = eventos_classificados_df.groupby('id_estacao')['classificacao'].value_counts().unstack(fill_value=0)
    classification_summary['Total'] = classification_summary.sum(axis=1)

    print(f"\n  Classification by station:")
    print(f"  Stations with EA events: {(classification_summary['EA'] > 0).sum()}")
    print(f"  Stations with ESA events: {(classification_summary['ESA'] > 0).sum()}")

    # -------------------------------------------------------------------------
    # STEP 7: Save Outputs
    # -------------------------------------------------------------------------
    print("\n" + "="*80)
    print("STEP 7: Saving Outputs")
    print("="*80)

    print(f"\nSaving pontos_id_df to {PONTOS_ID_OUTPUT}...")
    pontos_id_df.to_csv(PONTOS_ID_OUTPUT, index=False)
    print(f"  ✓ Saved {len(pontos_id_df):,} records")

    print(f"\nSaving classification_summary to {CLASSIFICATION_SUMMARY_OUTPUT}...")
    classification_summary.to_csv(CLASSIFICATION_SUMMARY_OUTPUT)
    print(f"  ✓ Saved summary for {len(classification_summary)} stations")

    print(f"\nSaving eventos_unicos to {EVENTOS_UNICOS_OUTPUT}...")
    # Add classification to unique events before saving
    eventos_unicos_with_class = eventos_classificados_df[['id_evento_chuva', 'id_estacao', 'start_time', 'end_time', 'classificacao']]
    eventos_unicos_with_class.to_csv(EVENTOS_UNICOS_OUTPUT, index=False)
    print(f"  ✓ Saved {len(eventos_unicos_with_class):,} unique events")

    print(f"\nSaving floods_with_station to {FLOODS_WITH_STATION_OUTPUT}...")
    # Drop geometry column and save as CSV for simplicity
    floods_with_station_df = floods_with_station_gdf.drop(columns=['geometry'])
    floods_with_station_df.to_csv(FLOODS_WITH_STATION_OUTPUT, index=False)
    print(f"  ✓ Saved {len(floods_with_station_df):,} flood-station associations")

    # -------------------------------------------------------------------------
    # FINAL SUMMARY
    # -------------------------------------------------------------------------
    print("\n" + "="*80)
    print("PROCESSING COMPLETE")
    print("="*80)
    print(f"\nOutputs saved to: {OUTPUT_DIR}")
    print(f"\nKey Statistics:")
    print(f"  - Stations processed: {len(station_ids)}")
    print(f"  - Unique rain events: {pontos_id_df['id_evento_chuva'].nunique():,}")
    print(f"  - Total I-D points: {len(pontos_id_df):,}")
    print(f"  - EA events: {(eventos_classificados_df['classificacao'] == 'EA').sum():,}")
    print(f"  - ESA events: {(eventos_classificados_df['classificacao'] == 'ESA').sum():,}")
    print(f"  - Flood occurrences linked: {len(floods_with_station_gdf):,}")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
