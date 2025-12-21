"""
Chart 8: Distribuição da Distância à Estação Pluviométrica Mais Próxima
Source: Derived from id-thresholds.py spatial join logic
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Configuration
plt.style.use('seaborn-v0_8-paper')
plt.rcParams['figure.dpi'] = 300

# Data paths
input_data_directory = os.path.expanduser('~/work/data/meteorologia/clean')
input_data_file = 'nbs/exploration/ocorrencias/ocorrencias_filtradas.csv'
stations_file = f'{input_data_directory}/clima_pluviometro/estacoes_alertario.csv'
output_directory = 'nbs/analysis/charts'
os.makedirs(output_directory, exist_ok=True)

# CRS Definitions
CRS_GEOGRAPHIC = "EPSG:4326"  # WGS84 for input lat/lon
CRS_PROJECTED = "EPSG:31983"  # SIRGAS 2000 / UTM zone 23S (for distance calculations)

print("Loading data...")

# Load data
ocorrencias = pd.read_csv(input_data_file)
pops = pd.read_csv('data/raw/adm_cor_comando/pops.csv', index_col=0)
stations = pd.read_csv(stations_file)

# Preprocessing ocorrencias
ocorrencias['data_inicio'] = pd.to_datetime(ocorrencias['data_inicio'])
ocorrencias['data_fim'] = pd.to_datetime(ocorrencias['data_fim'])
ocorrencias['tipo'] = ocorrencias['id_pop'].map(pops.set_index('id')['titulo'])

# Filter flood events
flood_types = [
    "Bolsão d'água em via",
    'Alagamento',
    'Alagamentos e enchentes',
    'Enchente',
    "Lâmina d'água"
]
ocorrencias = ocorrencias[ocorrencias['tipo'].isin(flood_types)]
ocorrencias['tipo'] = ocorrencias['tipo'].replace('Alagamentos e enchentes', 'Alagamento').replace('Enchente', 'Alagamento')

print(f"Total flood events: {len(ocorrencias)}")

# Convert to GeoDataFrame
ocorrencias_gdf = gpd.GeoDataFrame(
    ocorrencias,
    geometry=gpd.points_from_xy(ocorrencias.longitude, ocorrencias.latitude),
    crs=CRS_GEOGRAPHIC
)

# Convert stations to GeoDataFrame
stations_gdf = gpd.GeoDataFrame(
    stations,
    geometry=gpd.points_from_xy(stations.longitude, stations.latitude),
    crs=CRS_GEOGRAPHIC
)

# Drop stations with missing coordinates
stations_gdf = stations_gdf.dropna(subset=['latitude', 'longitude'])
stations_gdf = stations_gdf.drop_duplicates(subset=['id_estacao'], keep='first')

print(f"Total rain gauge stations: {len(stations_gdf)}")

# Transform to projected CRS for accurate distance calculations
ocorrencias_gdf = ocorrencias_gdf.to_crs(CRS_PROJECTED)
stations_gdf = stations_gdf.to_crs(CRS_PROJECTED)

print("Calculating distances to nearest station...")

# Calculate distance to nearest station for each flood event
def calculate_nearest_station_distance(flood_point, stations_gdf):
    """Calculate distance from flood point to nearest rain gauge station"""
    distances = stations_gdf.geometry.distance(flood_point)
    return distances.min()

# Apply distance calculation
ocorrencias_gdf['distance_to_nearest_station_m'] = ocorrencias_gdf.geometry.apply(
    lambda x: calculate_nearest_station_distance(x, stations_gdf)
)

# Convert to kilometers for better readability
ocorrencias_gdf['distance_to_nearest_station_km'] = ocorrencias_gdf['distance_to_nearest_station_m'] / 1000

print("\nDistance Statistics (km):")
print(ocorrencias_gdf['distance_to_nearest_station_km'].describe())

# Create visualization
fig, ax = plt.subplots(figsize=(10, 6))

# Create histogram
distances_km = ocorrencias_gdf['distance_to_nearest_station_km']

# Add statistics to the plot
mean_dist = distances_km.mean()
median_dist = distances_km.median()
max_dist = distances_km.max()

# Plot histogram with KDE (without legend)
sns.histplot(
    data=distances_km,
    bins=30,
    kde=True,
    color='steelblue',
    edgecolor='black',
    linewidth=0.5,
    ax=ax,
    legend=False
)

# Add vertical lines for mean and median
ax.axvline(mean_dist, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_dist:.2f} km')
ax.axvline(median_dist, color='orange', linestyle='--', linewidth=2, label=f'Median: {median_dist:.2f} km')

# Add statistics as text in the legend
# stats_label = f'N={len(distances_km)}, SD={distances_km.std():.2f} km, Max={max_dist:.2f} km'
# ax.plot([], [], ' ', label=stats_label)  # Empty plot for stats in legend

# Labels and title
ax.set_title('Distribution of Distance to Nearest Rain Gauge Station',
             fontsize=14, weight='bold', pad=15)
ax.set_xlabel('Distance to Nearest Station (km)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.tick_params(axis='both', labelsize=10)
ax.legend(fontsize=10, loc='upper right', framealpha=0.9)
ax.grid(True, alpha=0.3, linestyle='--')

# Save
plt.tight_layout()
output_path = f'{output_directory}/chart_08_distance_to_nearest_station.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"\nChart saved to {output_path}")
plt.close()

# Additional analysis: Distribution by event type
print("\n" + "="*60)
print("Distance statistics by event type:")
print("="*60)
for event_type in ocorrencias_gdf['tipo'].unique():
    subset = ocorrencias_gdf[ocorrencias_gdf['tipo'] == event_type]
    print(f"\n{event_type}:")
    print(f"  Count: {len(subset)}")
    print(f"  Mean distance: {subset['distance_to_nearest_station_km'].mean():.2f} km")
    print(f"  Median distance: {subset['distance_to_nearest_station_km'].median():.2f} km")
    print(f"  Max distance: {subset['distance_to_nearest_station_km'].max():.2f} km")
