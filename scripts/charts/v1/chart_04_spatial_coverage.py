"""
Chart 4: Spatial Coverage Analysis - Distance to Nearest Rain Gauge Station
Includes histogram and cumulative distribution function (CDF)
Addresses spatial bias implications for the study
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from config import (setup_plot_style, COLORS, FONT_SIZES, FIGURE_SIZES,
                    DATA_PATHS, OUTPUT_DIR, FLOOD_TYPES, EVENT_TYPE_MAPPING,
                    GENERIC_TYPE_MAPPING, STUDY_PERIOD, STUDY_LOCATION, add_sample_size_annotation,
                    add_subfigure_label, CRS_GEOGRAPHIC, CRS_PROJECTED)

def load_and_prepare_data():
    """Load and preprocess flood event and station data"""
    ocorrencias = pd.read_csv(DATA_PATHS['ocorrencias'])
    pops = pd.read_csv(DATA_PATHS['pops'], index_col=0)
    stations = pd.read_csv(os.path.expanduser(DATA_PATHS['stations']))
    
    ocorrencias['data_inicio'] = pd.to_datetime(ocorrencias['data_inicio'])
    ocorrencias['data_fim'] = pd.to_datetime(ocorrencias['data_fim'])
    ocorrencias['tipo'] = ocorrencias['id_pop'].map(pops.set_index('id')['titulo'])
    
    ocorrencias = ocorrencias[ocorrencias['tipo'].isin(FLOOD_TYPES)]
    ocorrencias['tipo'] = ocorrencias['tipo'].replace(EVENT_TYPE_MAPPING)
    ocorrencias['tipo'] = ocorrencias['tipo'].replace(GENERIC_TYPE_MAPPING)
    
    return ocorrencias, stations

def calculate_distances(ocorrencias, stations):
    """Calculate distance from each flood event to nearest rain gauge station"""
    # Convert to GeoDataFrame
    ocorrencias_gdf = gpd.GeoDataFrame(
        ocorrencias,
        geometry=gpd.points_from_xy(ocorrencias.longitude, ocorrencias.latitude),
        crs=CRS_GEOGRAPHIC
    )
    
    stations_gdf = gpd.GeoDataFrame(
        stations,
        geometry=gpd.points_from_xy(stations.longitude, stations.latitude),
        crs=CRS_GEOGRAPHIC
    )
    
    # Drop stations with missing coordinates
    stations_gdf = stations_gdf.dropna(subset=['latitude', 'longitude'])
    stations_gdf = stations_gdf.drop_duplicates(subset=['id_estacao'], keep='first')
    
    # Transform to projected CRS for accurate distance calculations
    ocorrencias_gdf = ocorrencias_gdf.to_crs(CRS_PROJECTED)
    stations_gdf = stations_gdf.to_crs(CRS_PROJECTED)
    
    # Calculate distance to nearest station for each flood event
    def calculate_nearest_distance(flood_point):
        distances = stations_gdf.geometry.distance(flood_point)
        return distances.min()
    
    ocorrencias_gdf['distance_m'] = ocorrencias_gdf.geometry.apply(calculate_nearest_distance)
    ocorrencias_gdf['distance_km'] = ocorrencias_gdf['distance_m'] / 1000
    
    return ocorrencias_gdf

def create_spatial_coverage_chart(ocorrencias_gdf):
    """Create spatial coverage analysis chart with histogram and CDF"""
    setup_plot_style()
    
    # Filter out NaN values before calculating statistics
    distances_km = ocorrencias_gdf['distance_km'].dropna().values
    
    # Calculate statistics
    mean_dist = np.nanmean(distances_km)
    median_dist = np.nanmedian(distances_km)
    p90_dist = np.nanpercentile(distances_km, 90)
    max_dist = np.nanmax(distances_km)
    
    # Create figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGURE_SIZES['double'])
    fig.suptitle(f'Spatial Coverage: Distance to Nearest Rain Gauge Station\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'], fontweight='bold', y=1.02)
    
    # Panel A: Histogram
    n, bins, patches = ax1.hist(distances_km, bins=30, color=COLORS['primary'], 
                                edgecolor='black', linewidth=0.5, alpha=0.7)
    
    # Add vertical lines for statistics
    ax1.axvline(mean_dist, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_dist:.2f} km')
    ax1.axvline(median_dist, color='orange', linestyle='--', linewidth=2, label=f'Median: {median_dist:.2f} km')
    ax1.axvline(p90_dist, color='purple', linestyle=':', linewidth=2, label=f'90th percentile: {p90_dist:.2f} km')
    
    ax1.set_xlabel('Distance to Nearest Station (km)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_ylabel('Frequency', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_title('Distribution', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax1.legend(loc='upper right', fontsize=FONT_SIZES['legend'])
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    ax1.set_axisbelow(True)
    add_subfigure_label(ax1, '(a)')
    
    # Panel B: Cumulative Distribution Function (CDF)
    sorted_distances = np.sort(distances_km)
    cumulative = np.arange(1, len(sorted_distances) + 1) / len(sorted_distances) * 100
    
    ax2.plot(sorted_distances, cumulative, color=COLORS['primary'], linewidth=2)
    ax2.fill_between(sorted_distances, 0, cumulative, color=COLORS['primary'], alpha=0.2)
    
    # Add reference lines
    ax2.axhline(50, color='orange', linestyle='--', linewidth=1, alpha=0.5)
    ax2.axhline(90, color='purple', linestyle=':', linewidth=1, alpha=0.5)
    ax2.axvline(median_dist, color='orange', linestyle='--', linewidth=1, alpha=0.5)
    ax2.axvline(p90_dist, color='purple', linestyle=':', linewidth=1, alpha=0.5)
    
    # Add annotations
    ax2.text(median_dist, 50, f' {median_dist:.2f} km', fontsize=FONT_SIZES['annotation'],
            verticalalignment='bottom', color='orange')
    ax2.text(p90_dist, 90, f' {p90_dist:.2f} km', fontsize=FONT_SIZES['annotation'],
            verticalalignment='bottom', color='purple')
    
    ax2.set_xlabel('Distance to Nearest Station (km)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_ylabel('Cumulative Percentage (%)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_title('Cumulative Distribution', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax2.grid(True, linestyle='--', alpha=0.3)
    ax2.set_axisbelow(True)
    ax2.set_ylim(0, 100)
    add_subfigure_label(ax2, '(b)')
    
    # Add sample size and coverage info
    coverage_text = f'50% within {median_dist:.2f} km\n90% within {p90_dist:.2f} km'
    ax2.text(0.98, 0.15, coverage_text, transform=ax2.transAxes, fontsize=FONT_SIZES['annotation'],
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, edgecolor='gray'))
    
    add_sample_size_annotation(ax2, len(ocorrencias_gdf))
    
    plt.tight_layout()
    return fig, mean_dist, median_dist, p90_dist, max_dist

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias, stations = load_and_prepare_data()
    print(f"Total flood events: {len(ocorrencias)}")
    print(f"Total rain gauge stations: {len(stations)}")
    
    print("\nCalculating distances to nearest station...")
    ocorrencias_gdf = calculate_distances(ocorrencias, stations)
    
    print("\nCreating spatial coverage chart...")
    fig, mean_dist, median_dist, p90_dist, max_dist = create_spatial_coverage_chart(ocorrencias_gdf)
    
    print("\nDistance Statistics (km):")
    print(f"  Mean: {mean_dist:.2f}")
    print(f"  Median: {median_dist:.2f}")
    print(f"  90th percentile: {p90_dist:.2f}")
    print(f"  Maximum: {max_dist:.2f}")
    print(f"\nCoverage: 50% of events within {median_dist:.2f} km, 90% within {p90_dist:.2f} km")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = f'{OUTPUT_DIR}/chart_04_spatial_coverage.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nChart saved to {output_path}")
    plt.close()

if __name__ == '__main__':
    main()
