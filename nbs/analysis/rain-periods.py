# %% [markdown]
# # Build Static Thiessen Polygons + Areal Rainfall Estimation
# 
# This notebook implements the Thiessen Polygon method to estimate areal average rainfall for Rio de Janeiro city using 15-minute pluviometric data. This approach uses **static Thiessen polygons**, meaning the polygons are generated once based on station locations and then applied across all timestamps.
# 
# **Methodology Outline:**
# 
# 1.  **Setup:** Import libraries and define paths.
# 2.  **Define Paths and Constants**
# 3.  **Load and Process Data:**
#     *   Simulate loading of `alertario` pluviometric data (as it's assumed to be pre-loaded).
#     *   Load station locations (latitude/longitude for each `id_estacao`).
#     *   Load the Rio de Janeiro city boundary (created in a previous step).
# 4.  **Generate Static Thiessen Polygons:**
#     *   Use `scipy.spatial.Voronoi` to generate Voronoi cells from station locations.
#     *   Convert these cells into `shapely` Polygons and create a GeoDataFrame.
#     *   Clip these polygons to the city boundary.
# 5.  **Calculate Polygon Weights:**
#     *   Calculate the area of each clipped Thiessen polygon.
#     *   Calculate the weight for each station's polygon (`Area_polygon_i / Total_City_Area`).
# 6.  **Calculate Time-Series Areal Average Rainfall:**
#     *   Merge Thiessen polygon weights with the 15-minute rainfall data.
#     *   For each timestamp, calculate the weighted average rainfall: `Areal_Rainfall = Σ (Rainfall_at_station_i * Weight_i)`.
# 7.  **Visualization & Results:**
#     *   Plot the Thiessen polygons overlaid on the city map.
#     *   Plot the time series of the calculated areal average rainfall.
# 8.  **Save Outputs:**
#     *   Save the generated Thiessen polygons (with weights) as a GeoPackage.
#     *   Save the areal average rainfall time series as a CSV file.
# 9.  **Conclusions**
# 
# 
# ---
# 
# ## 1. Setup and Imports

# %%
import os
import pandas as pd
import geopandas as gpd
import numpy as np
from scipy.spatial import Voronoi
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches # For custom legends
import seaborn as sns

# Plotting style for nicer academic-ready charts
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("viridis") # A good colormap for sequential data

# Display options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 50)

# %% [markdown]
# ## 2. Define Paths and Constants

# %%
# --- Input Data Paths ---
# Path for the ALERTA RIO rainfall data (assuming it's loaded as 'alertario')
# For this notebook, we will simulate its loading.
input_data_directory = '../../../../data/meteorologia/clean'

# Path for station locations (this file needs to be created or provided)
# Example: '../../../../../data/meteorologia/auxiliary/stations_coordenadas.csv'
STATIONS_CSV_PATH = f'{input_data_directory}/clima_pluviometro/estacoes_alertario.csv' # ADJUST AS NEEDED

# Path for the city boundary file (created in the previous notebook)
CITY_BOUNDARY_FILE_PATH = f'{input_data_directory}/limites_geograficos_rj/limite_municipio_rio_de_janeiro.gpkg' # ADJUST AS NEEDED

# --- Output Data Paths ---
OUTPUT_DATA_DIRECTORY = '../../../../../data/meteorologia/processed/thiessen_analysis'
THIESSEN_POLYGONS_FILENAME = 'thiessen_polygons_rio.gpkg'
AREAL_RAINFALL_FILENAME = 'areal_rainfall_15min_rio.csv'

# --- CRS Definitions ---
CRS_GEOGRAPHIC = "EPSG:4326"  # WGS84 for input lat/lon
CRS_PROJECTED = "EPSG:31983"  # SIRGAS 2000 / UTM zone 23S (suitable for Rio de Janeiro for area calculations)

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DATA_DIRECTORY, exist_ok=True)

# %% [markdown]
# ## 3. Load and Process Data

# %% [markdown]
# ### Load Data

# %%
input_data_directory = '../../../../data/meteorologia/clean'

alertario = pd.read_csv(f'{input_data_directory}/clima_pluviometro/taxa_precipitacao_alertario.csv')
stations = pd.read_csv(f'{input_data_directory}/clima_pluviometro/estacoes_alertario.csv')
ocorrencias = pd.read_csv(f'{input_data_directory}/adm_cor_comando/ocorrencias.csv')
pops = pd.read_csv('../../data/raw/adm_cor_comando/pops.csv', index_col=0)
city_boundary_gdf = gpd.read_file(CITY_BOUNDARY_FILE_PATH)

# %% [markdown]
# ### 3.1. Process Precipitation

# %%
# Convert datetime data type fields
alertario['horario'] = pd.to_timedelta(alertario['horario'])
alertario['data_particao'] = pd.to_datetime(alertario['data_particao'])
alertario['timestamp'] = pd.to_datetime(alertario['timestamp'])

# Map station name and coordinates
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

# Ensure rainfall data is numeric
alertario['acumulado_chuva_15_min'] = pd.to_numeric(alertario['acumulado_chuva_15_min'], errors='coerce')

# Handle missing rainfall values: fill with 0.
# This means if a station has a Thiessen polygon but no data for an interval, it contributes 0mm to the areal average.
alertario['acumulado_chuva_15_min'] = alertario['acumulado_chuva_15_min'].fillna(0)

alertario = alertario

print("\nCleaned 'alertario' (info):")
alertario.info()
display(alertario.describe())

# %% [markdown]
# ### 3.2. Process Station Locations
# These are the geographic coordinates of the pluviometric stations. This data is **essential** for Thiessen polygons.

# %%
print("\nStation Locations DataFrame (first 5 rows):")
display(stations.head())

# Convert to GeoDataFrame
stations_gdf = gpd.GeoDataFrame(
    stations,
    geometry=gpd.points_from_xy(stations.longitude, stations.latitude),
    crs=CRS_GEOGRAPHIC
)

# Drop stations with missing coordinates
stations_gdf = stations_gdf.dropna(subset=['latitude', 'longitude'])

# Stations with rainfall data
stations_with_data_ids = alertario['id_estacao'].unique()

# Filter stations_gdf to include only those with data in alertario
# OR, for static polygons, you might decide to use ALL known station locations,
# assuming they could report at any time. Let's use all known stations from stations_gdf for polygon generation.
# If a station in stations_gdf never appears in alertario, its weight will simply never be used.

# Let's ensure stations_gdf has unique id_estacao if there are duplicates from source
stations_gdf = stations_gdf.drop_duplicates(subset=['id_estacao'], keep='first')

# For robustness, it's good to check if all stations in alertario have locations
stations_in_alertario_without_loc = set(stations_with_data_ids) - set(stations_gdf['id_estacao'])
if stations_in_alertario_without_loc:
    print(f"WARNING: Stations present in alertario but MISSING locations: {stations_in_alertario_without_loc}")
    print("These stations will be excluded from Thiessen polygon analysis.")
    # Filter alertario to only include stations that have locations
    alertario = alertario[alertario['id_estacao'].isin(stations_gdf['id_estacao'])]

print(f"\nNumber of unique stations in (potentially filtered) alertario: {alertario['id_estacao'].nunique()}")
print(f"Number of stations in stations_gdf to be used for polygons: {len(stations_gdf)}")

# If no stations are left, stop.
if stations_gdf.empty or alertario['id_estacao'].nunique() == 0:
    raise ValueError("No stations available for Thiessen polygon generation after filtering. Please check your station location data and rainfall data.")

print("\nStation Locations GeoDataFrame (first 5 rows):")
display(stations_gdf.head())

# %% [markdown]
# ### 3.3. Process City Boundary
# Load the city boundary file (e.g., GeoPackage or Shapefile) that defines the study area.

# %%
print("\nCity Boundary GeoDataFrame:")
display(city_boundary_gdf.head())
print(f"CRS of city boundary: {city_boundary_gdf.crs}")

# Plot to verify (optional)
fig, ax = plt.subplots(1,1, figsize=(8,8))
city_boundary_gdf.plot(ax=ax, facecolor='lightgray', edgecolor='black')
stations_gdf.plot(ax=ax, color='red', markersize=50, label='Stations')
plt.title("City Boundary and Station Locations (Geographic CRS)")
plt.legend()
plt.show()

# %% [markdown]
# ### 3.4. Processing `ocorrencias`

# %%
# Convert datetime data type fields
ocorrencias['data_inicio'] = pd.to_datetime(ocorrencias['data_inicio'])
ocorrencias['data_fim'] = pd.to_datetime(ocorrencias['data_fim'])

# Map event type
ocorrencias['tipo'] = ocorrencias['id_pop'].map(pops.set_index('id')['titulo'])

# Filter ocorrences by type
ocorrencias = ocorrencias[ocorrencias['tipo'].isin(["Bolsão d'água em via", 'Alagamento', 'Enchente', 'Alagamentos e enchentes'])]

print("\nOcorrencias DataFrame (first 5 rows):")
display(ocorrencias.head())

# Convert to GeoDataFrame
ocorrencias_gdf = gpd.GeoDataFrame(
    ocorrencias,
    geometry=gpd.points_from_xy(ocorrencias.longitude, ocorrencias.latitude),
    crs=CRS_GEOGRAPHIC
)

# %% [markdown]
# ### Select Target Period for Precipitation Values  

# %%
min_time_ocorrencias = ocorrencias['data_inicio'].min()

alertario = alertario[alertario['timestamp'] > str(min_time_ocorrencias.year)]

print(f"Min. Time: {alertario['timestamp'].min()} | Max. Time: {alertario['timestamp'].max()}")

# %% [markdown]
# ### 3.5. CRS Transformation
# Transform `stations_gdf` and `city_boundary_gdf` to the projected CRS for accurate geometric operations (area calculation, Voronoi).

# %%
print(f"\nOriginal CRS - Stations: {stations_gdf.crs}, Boundary: {city_boundary_gdf.crs}")

if stations_gdf.crs != CRS_PROJECTED:
    stations_gdf = stations_gdf.to_crs(CRS_PROJECTED)
    print(f"Stations GeoDataFrame reprojected to {CRS_PROJECTED}")

if city_boundary_gdf.crs != CRS_PROJECTED:
    city_boundary_gdf = city_boundary_gdf.to_crs(CRS_PROJECTED)
    print(f"City Boundary GeoDataFrame reprojected to {CRS_PROJECTED}")

print(f"New CRS - Stations: {stations_gdf.crs}, Boundary: {city_boundary_gdf.crs}")

# Get the unary union of the city boundary in case it's a MultiPolygon or has multiple features
# This ensures a single, clean boundary polygon for clipping.
study_area_polygon = city_boundary_gdf.geometry.unary_union
print(f"Study area polygon type: {type(study_area_polygon)}")

# %% [markdown]
# ## 4. Generate Static Thiessen Polygons
# 
# We'll define a function to compute Voronoi polygons from points and then clip them to the study area.

# %%
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
import warnings

def create_voronoi_polygons(points_gdf: gpd.GeoDataFrame,
                            boundary_gdf: gpd.GeoDataFrame,
                            id_column: str = None) -> gpd.GeoDataFrame:
    """
    Generates Voronoi polygons for a set of input points, clipped to a specified boundary.

    The function takes a GeoDataFrame of points and a GeoDataFrame containing a single
    boundary (Multi)Polygon. It computes the Voronoi diagram for the points and
    clips the resulting polygons (including infinite ones) to this boundary.

    Args:
        points_gdf (gpd.GeoDataFrame):
            A GeoDataFrame containing the input points. Must have a valid geometry column
            with Point geometries.
        boundary_gdf (gpd.GeoDataFrame):
            A GeoDataFrame containing a single feature which is a Polygon or MultiPolygon
            defining the area to clip the Voronoi polygons. If multiple features exist,
            their unary_union will be taken, with a warning.
        id_column (str, optional):
            The name of a column in `points_gdf` to use as an identifier for the
            resulting Voronoi polygons. If None, a default ID may not be explicitly set,
            but attributes from points_gdf will be carried over.

    Returns:
        gpd.GeoDataFrame:
            A GeoDataFrame containing the Voronoi polygons. Each polygon corresponds
            to an input point, and all polygons are clipped to the provided boundary.
            Attributes from the input `points_gdf` are carried over to the
            corresponding Voronoi polygons.

    Raises:
        TypeError: If inputs are not GeoDataFrames.
        ValueError: If input GeoDataFrames are empty, points_gdf does not contain Points,
                    or boundary_gdf does not define a valid polygonal boundary.
    """

    # 1. Input Validation
    if not isinstance(points_gdf, gpd.GeoDataFrame):
        raise TypeError("points_gdf must be a GeoDataFrame.")
    if not isinstance(boundary_gdf, gpd.GeoDataFrame):
        raise TypeError("boundary_gdf must be a GeoDataFrame.")

    if points_gdf.empty:
        raise ValueError("points_gdf cannot be empty.")
    if boundary_gdf.empty:
        raise ValueError("boundary_gdf cannot be empty.")

    if not points_gdf.geometry.geom_type.isin(['Point']).all():
        raise ValueError("points_gdf geometry column must contain only Point geometries.")

    if not boundary_gdf.geometry.geom_type.isin(['Polygon', 'MultiPolygon']).all():
        raise ValueError("boundary_gdf geometry column must contain Polygon or MultiPolygon geometries.")

    # 2. Prepare the clipping boundary
    if len(boundary_gdf) > 1:
        warnings.warn(
            "boundary_gdf contains multiple features. Their unary_union will be used as the boundary.",
            UserWarning
        )
        clip_boundary = boundary_gdf.geometry.unary_union
    else:
        clip_boundary = boundary_gdf.geometry.iloc[0]

    if not isinstance(clip_boundary, (Polygon, MultiPolygon)):
        raise ValueError(
            "The resulting boundary geometry is not a Polygon or MultiPolygon. "
            "Ensure boundary_gdf defines a valid area."
        )
    if not clip_boundary.is_valid:
        warnings.warn("Boundary geometry is not valid. Attempting to buffer by 0 to fix.", UserWarning)
        clip_boundary = clip_boundary.buffer(0)
        if not clip_boundary.is_valid:
            raise ValueError("Boundary geometry could not be fixed and is invalid.")


    # 3. CRS (Coordinate Reference System) Check
    # It's crucial that both GeoDataFrames are in the same CRS for meaningful geometric operations.
    # For Voronoi diagrams, a projected CRS is often preferred for accuracy over geographic (lat/lon).
    # However, this function will proceed if they are the same, or warn if different.
    if points_gdf.crs is None:
        warnings.warn("points_gdf has no CRS defined. Assuming it matches boundary_gdf.", UserWarning)
    elif boundary_gdf.crs is None:
        warnings.warn("boundary_gdf has no CRS defined. Assuming it matches points_gdf.", UserWarning)
    elif points_gdf.crs != boundary_gdf.crs:
        warnings.warn(
            f"CRS mismatch: points_gdf CRS is '{points_gdf.crs}' and boundary_gdf CRS is '{boundary_gdf.crs}'. "
            "Results may be unexpected. Consider reprojecting to a common projected CRS.",
            UserWarning
        )
        # Example of reprojection (optional, could be enforced or done by user):
        # points_gdf = points_gdf.to_crs(boundary_gdf.crs)


    # 4. Generate Voronoi Polygons
    # The `extend_to` parameter in `voronoi_polygons` (GeoPandas >= 0.10.0)
    # handles the clipping of infinite polygons to the provided geometry.
    try:
        voronoi_series = points_gdf.geometry.voronoi_polygons(extend_to=clip_boundary)
    except AttributeError:
        raise ImportError(
            "The 'voronoi_polygons' method with 'extend_to' requires GeoPandas >= 0.10.0 and Shapely >= 1.8. "
            "Please upgrade your libraries."
        )
    except Exception as e:
        raise RuntimeError(f"Error during Voronoi generation: {e}")


    # 5. Create the output GeoDataFrame
    # We want to retain attributes from the original points_gdf.
    # Assigning the new geometries to a copy of points_gdf is a good way.
    voronoi_gdf = points_gdf.copy()
    voronoi_gdf.geometry = voronoi_series

    # If an id_column was specified and exists, ensure it's clear.
    # Otherwise, all columns from points_gdf are already present.
    if id_column:
        if id_column not in voronoi_gdf.columns:
            warnings.warn(f"Specified id_column '{id_column}' not found in points_gdf. It will not be specifically used.", UserWarning)
        # No explicit action needed here if we are just carrying over all columns.
        # If we wanted to *only* keep the id_column and geometry:
        # voronoi_gdf = gpd.GeoDataFrame(points_gdf[[id_column]], geometry=voronoi_series, crs=points_gdf.crs)

    # Filter out any empty or invalid geometries that might result from edge cases
    # (e.g., points far outside the boundary, though `extend_to` should largely prevent this)
    voronoi_gdf = voronoi_gdf[~voronoi_gdf.is_empty & voronoi_gdf.is_valid]
    
    # Ensure the resulting geometries are indeed within the boundary after clipping
    # (This step might be slightly redundant if extend_to works perfectly, but good for robustness)
    # It can also trim tiny overlaps if precision issues occur.
    # Use a small buffer on the boundary to avoid issues with floating point precision for intersections
    # This might slightly alter the boundary, so use with caution or make buffer distance configurable.
    # For now, let's assume extend_to handles it well. If not, one could add:
    voronoi_gdf.geometry = voronoi_gdf.geometry.intersection(clip_boundary)
    voronoi_gdf = voronoi_gdf[~voronoi_gdf.is_empty & voronoi_gdf.is_valid & (voronoi_gdf.geom_type != 'GeometryCollection')]


    if voronoi_gdf.empty:
        warnings.warn("Resulting Voronoi GeoDataFrame is empty. This might happen if all points are outside "
                      "the boundary or due to other geometric issues.", UserWarning)

    return voronoi_gdf

'''
# --- Example Usage ---
if __name__ == '__main__':
    from shapely.geometry import Point

    # 1. Create some sample points
    points_data = {
        'id': ['P1', 'P2', 'P3', 'P4', 'P5'],
        'value': [10, 20, 15, 25, 30],
        'geometry': [Point(0.5, 0.5), Point(1.5, 1.5), Point(0.5, 1.5), Point(1.5, 0.5), Point(1, 1)]
    }
    points_gdf = gpd.GeoDataFrame(points_data, crs="EPSG:4326") # Using a common geographic CRS

    # 2. Create a sample boundary (a square MultiPolygon)
    # For simplicity, make it a Polygon first, then wrap in MultiPolygon
    boundary_poly = Polygon([(0, 0), (0, 2), (2, 2), (2, 0), (0, 0)])
    boundary_multipoly = MultiPolygon([boundary_poly])
    boundary_gdf = gpd.GeoDataFrame({'name': ['study_area']},
                                    geometry=[boundary_multipoly],
                                    crs="EPSG:4326")

    print("Input Points GDF:")
    print(points_gdf)
    print("\nInput Boundary GDF:")
    print(boundary_gdf)

    # 3. Generate Voronoi polygons
    try:
        voronoi_result_gdf = create_voronoi_polygons(points_gdf, boundary_gdf, id_column='id')
        print("\nResulting Voronoi GDF:")
        print(voronoi_result_gdf)
        print(f"\nNumber of Voronoi polygons: {len(voronoi_result_gdf)}")

        # Optional: Plotting for visual verification (requires matplotlib)
        try:
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(1, 1, figsize=(8, 8))
            boundary_gdf.plot(ax=ax, facecolor='none', edgecolor='black', linewidth=2, label='Boundary')
            voronoi_result_gdf.plot(ax=ax, alpha=0.5, edgecolor='blue', cmap='viridis', column='value', legend=True)
            points_gdf.plot(ax=ax, color='red', markersize=50, label='Input Points')
            ax.set_title("Voronoi Polygons Clipped to Boundary")
            ax.legend()
            plt.show()
        except ImportError:
            print("\nMatplotlib not installed. Skipping plot.")

    except Exception as e:
        print(f"\nAn error occurred: {e}")

    # Example with points outside the boundary
    print("\n--- Example with some points outside the boundary ---")
    points_data_mixed = {
        'id': ['P1_in', 'P2_out', 'P3_in', 'P4_out'],
        'value': [10, 99, 15, 88],
        'geometry': [Point(0.5, 0.5), Point(3, 3), Point(1.5, 1.5), Point(-1, -1)]
    }
    points_gdf_mixed = gpd.GeoDataFrame(points_data_mixed, crs="EPSG:4326")
    
    try:
        voronoi_mixed_gdf = create_voronoi_polygons(points_gdf_mixed, boundary_gdf, id_column='id')
        print("\nResulting Voronoi GDF (mixed points):")
        print(voronoi_mixed_gdf) # Points outside should still generate polygons, clipped to boundary
                                 # Their influence region will be limited by the boundary.

        # Optional Plotting
        try:
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(1, 1, figsize=(8, 8))
            boundary_gdf.plot(ax=ax, facecolor='none', edgecolor='black', linewidth=2, label='Boundary')
            if not voronoi_mixed_gdf.empty:
                 voronoi_mixed_gdf.plot(ax=ax, alpha=0.5, edgecolor='blue', cmap='viridis', column='value', legend=True)
            points_gdf_mixed.plot(ax=ax, color='red', markersize=50, label='Input Points')
            ax.set_title("Voronoi Polygons (Mixed Points) Clipped to Boundary")
            ax.legend()
            plt.show()
        except ImportError:
            print("\nMatplotlib not installed. Skipping plot.")
            
    except Exception as e:
        print(f"\nAn error occurred with mixed points: {e}")
'''

thiessen_polygons_gdf = create_voronoi_polygons(stations_gdf, city_boundary_gdf, id_column='id_estacao')

# Calculate area for each polygon (in square meters, since CRS is projected)
thiessen_polygons_gdf['area_m2'] = thiessen_polygons_gdf.geometry.area

if thiessen_polygons_gdf.empty:
    raise ValueError("Thiessen polygon generation failed or resulted in no polygons within the study area.")

print(f"\nGenerated {len(thiessen_polygons_gdf)} Thiessen polygons.")
print(thiessen_polygons_gdf[['id_estacao', 'geometry']].head())



# %% [markdown]
# ## 5. Calculate Polygon Weights

# %%

# Calculate total area of the study region (sum of polygon areas after clipping)
# This should be very close to study_area_polygon.area
total_study_area_m2 = thiessen_polygons_gdf['area_m2'].sum()
print(f"\nTotal area of Thiessen polygons within study boundary: {total_study_area_m2 / 1e6:.2f} km^2")
print(f"Actual study area (from boundary file): {study_area_polygon.area / 1e6:.2f} km^2")

# Calculate weight for each polygon
thiessen_polygons_gdf['weight'] = thiessen_polygons_gdf['area_m2'] / total_study_area_m2

print("\nThiessen Polygons with Areas and Weights (first 5 rows):")
print(thiessen_polygons_gdf[['id_estacao', 'area_m2', 'weight']].head())
print(f"\nSum of weights: {thiessen_polygons_gdf['weight'].sum():.4f}") # Should be very close to 1.0

# %% [markdown]
# ## 6. Calculate Time-Series Areal Average Rainfall

# %%
# Merge rainfall data with Thiessen polygon weights
# We need 'id_estacao', 'timestamp', 'acumulado_chuva_15_min' from alertario
# and 'id_estacao', 'weight' from thiessen_polygons_gdf
rainfall_with_weights_df = pd.merge(
    alertario[['id_estacao', 'timestamp', 'acumulado_chuva_15_min']],
    thiessen_polygons_gdf[['id_estacao', 'weight']],
    on='id_estacao',
    how='left' # Use left merge to keep all rainfall records; stations not in thiessen_polygons_gdf will have NaN weight
)

# Handle cases where a station in alertario might not have a polygon (e.g., filtered out, outside boundary)
# These would have NaN weights and should be reported or handled.
if rainfall_with_weights_df['weight'].isnull().any():
    missing_weight_stations = rainfall_with_weights_df[rainfall_with_weights_df['weight'].isnull()]['id_estacao'].unique()
    print(f"WARNING: Stations in rainfall data missing Thiessen weights: {missing_weight_stations}. Their rainfall will not be counted.")
    rainfall_with_weights_df.dropna(subset=['weight'], inplace=True) # Remove records that can't be weighted

# Calculate weighted rainfall for each station record
rainfall_with_weights_df['weighted_rainfall'] = rainfall_with_weights_df['acumulado_chuva_15_min'] * rainfall_with_weights_df['weight']

# Group by timestamp and sum weighted rainfall to get areal average
areal_rainfall_s = rainfall_with_weights_df.groupby('timestamp')['weighted_rainfall'].sum()
areal_rainfall_ts_df = areal_rainfall_s.reset_index()
areal_rainfall_ts_df.rename(columns={'weighted_rainfall': 'areal_avg_rainfall_mm_15min'}, inplace=True)

print("\nAreal Average Rainfall Time Series (first 5 rows):")
print(areal_rainfall_ts_df.head())

# %% [markdown]
# ## 7. Save & Reload
# 
# ### 7.1 Save Outputs

# %%
# --- Save Thiessen Polygons GeoDataFrame ---
thiessen_output_path = os.path.join(OUTPUT_DATA_DIRECTORY, THIESSEN_POLYGONS_FILENAME)
try:
    # Select relevant columns for saving, ensure geometry is named 'geometry'
    cols_to_save = ['id_estacao', 'area_m2', 'weight', 'geometry']
    thiessen_polygons_to_save = thiessen_polygons_gdf[cols_to_save].copy()
    thiessen_polygons_to_save.to_file(thiessen_output_path, driver="GPKG")
    print(f"\nThiessen polygons saved to: {thiessen_output_path}")
except Exception as e:
    print(f"Error saving Thiessen polygons: {e}")

# --- Save Areal Rainfall Time Series ---
areal_rainfall_output_path = os.path.join(OUTPUT_DATA_DIRECTORY, AREAL_RAINFALL_FILENAME)
try:
    areal_rainfall_ts_df.to_csv(areal_rainfall_output_path, index=False)
    print(f"Areal rainfall time series saved to: {areal_rainfall_output_path}")
except Exception as e:
    print(f"Error saving areal rainfall time series: {e}")

# %% [markdown]
# ### 7.2 Reload Results

# %%
# Reload Thiessen polygons
thiessen_path = os.path.join(OUTPUT_DATA_DIRECTORY, THIESSEN_POLYGONS_FILENAME)
if os.path.exists(thiessen_path):
    thiessen_polygons_gdf = gpd.read_file(thiessen_path)
    print(f"✓ Thiessen polygons loaded: {len(thiessen_polygons_gdf)} polygons")
else:
    print("⚠ Thiessen polygons file not found")
    
# Reload areal rainfall time series
areal_rainfall_path = os.path.join(OUTPUT_DATA_DIRECTORY, AREAL_RAINFALL_FILENAME)
if os.path.exists(areal_rainfall_path):
    areal_rainfall_ts_df = pd.read_csv(areal_rainfall_path, parse_dates=['timestamp'])
    print(f"✓ Areal rainfall time series loaded: {len(areal_rainfall_ts_df)} records")
else:
    print("⚠ Areal rainfall time series file not found")
    

# %% [markdown]
# ## 8. Visualization & Results
# 
# ### 8.1. Map of Thiessen Polygons

# %%
fig, ax = plt.subplots(1, 1, figsize=(12, 12))

# Plot city boundary
city_boundary_gdf.plot(ax=ax, facecolor='none', edgecolor='black', linewidth=1.5, label='City Boundary', zorder=3)

# Plot Thiessen polygons
# Use a qualitative colormap for distinct station areas
num_stations = len(thiessen_polygons_gdf['id_estacao'].unique())
cmap_qualitative = plt.get_cmap('viridis', num_stations) # Or 'tab20', 'Set3'

# Create a color mapping for each station ID for consistent coloring
unique_station_ids = sorted(thiessen_polygons_gdf['id_estacao'].unique())
color_map = {station_id: cmap_qualitative(i) for i, station_id in enumerate(unique_station_ids)}

for idx, row in thiessen_polygons_gdf.iterrows():
    gpd.GeoSeries([row.geometry]).plot(
        ax=ax, 
        color=color_map[row.id_estacao], 
        edgecolor='gray', 
        alpha=0.6, 
        zorder=1
    )

# Plot station points
# Filter stations_gdf to only those that have a polygon, to avoid plotting points without areas.
stations_in_polygons = thiessen_polygons_gdf['id_estacao'].unique()
stations_to_plot_gdf = stations_gdf[stations_gdf['id_estacao'].isin(stations_in_polygons)]

stations_to_plot_gdf.plot(ax=ax, marker='o', color='red', markersize=50, edgecolor='black', label='Rain Gauges', zorder=2)
for x, y, label in zip(stations_to_plot_gdf.geometry.x, stations_to_plot_gdf.geometry.y, stations_to_plot_gdf.id_estacao):
    ax.text(x + 500, y + 500, label, fontsize=9, ha='center', va='bottom', color='black', zorder=4) # Adjust offset as needed

# # ---- Full Legend ----

# # Create custom legend patches for station areas
# legend_patches = [mpatches.Patch(color=color_map[sid], label=f'Est. {sid} - {stations_gdf.set_index("id_estacao").loc[sid, "estacao"]}') for sid in unique_station_ids]
# # Add boundary and station points to legend
# legend_patches.append(plt.Line2D([0], [0], color='black', lw=1.5, label='City Boundary'))
# legend_patches.append(plt.Line2D([0], [0], marker='o', color='red', markeredgecolor='black', markersize=7, linestyle='None', label='Rain Gauges'))

# ---- Fixed Size Legend ----

# Create custom legend
station_info_for_legend = stations_gdf.set_index('id_estacao')
legend_patches = []

# Limit legend entries if too many stations for clarity, e.g., max 15-20
max_legend_stations = 20
ids_for_legend = unique_station_ids[:max_legend_stations]
for sid in ids_for_legend:
    station_name = station_info_for_legend.loc[sid, "estacao"] if sid in station_info_for_legend.index else f"Est. {sid}"
    legend_patches.append(mpatches.Patch(color=color_map[sid], label=f'Est. {sid} - {station_name}'))
if len(unique_station_ids) > max_legend_stations:
     legend_patches.append(mpatches.Patch(color='grey', label=f'... and {len(unique_station_ids)-max_legend_stations} more stations'))

legend_patches.append(plt.Line2D([0], [0], color='black', lw=1.5, label='City Boundary'))
legend_patches.append(plt.Line2D([0], [0], marker='o', color='red', markeredgecolor='black', markersize=7, linestyle='None', label='Rain Gauges'))

# ----

ax.set_title('Static Thiessen Polygons for Rainfall Stations in Rio de Janeiro', fontsize=16)
ax.set_xlabel('Easting (m)', fontsize=12)
ax.set_ylabel('Northing (m)', fontsize=12)
ax.tick_params(axis='both', which='major', labelsize=10)
ax.grid(True, linestyle='--', alpha=0.7)
plt.legend(handles=legend_patches, title="Legend", fontsize=10, title_fontsize=12, loc='upper left', bbox_to_anchor=(1.02, 1))
plt.tight_layout(rect=[0, 0, 0.85, 1]) # Adjust layout to make space for legend
plt.show()

# %% [markdown]
# ### 8.1. Map of Thiessen Polygons
# 

# %%
import matplotlib.pyplot as plt
import geopandas as gpd
import matplotlib.patches as mpatches
import contextily as ctx

# --- Estilo e Configuração para Publicação ---
plt.style.use('seaborn-v0_8-paper')
plt.rcParams['figure.dpi'] = 300 # Alta resolução para a figura
plt.rcParams['font.family'] = 'sans-serif'

# --- Criação da Figura e Eixo ---
# O GeoPandas e Contextily cuidam da projeção.
fig, ax = plt.subplots(1, 1, figsize=(12, 12))

# --- Plotagem dos Polígonos de Thiessen ---
# Mapa de cores para distinção visual das áreas das estações
num_stations = len(thiessen_polygons_gdf['id_estacao'].unique())
cmap_qualitative = plt.get_cmap('viridis', num_stations)

# Mapeia um ID de estação para uma cor para consistência
unique_station_ids = sorted(thiessen_polygons_gdf['id_estacao'].unique())
color_map = {station_id: cmap_qualitative(i) for i, station_id in enumerate(unique_station_ids)}

# Plota cada polígono com sua cor correspondente
thiessen_polygons_gdf.plot(
    ax=ax,
    column='id_estacao',
    categorical=True, # Garante que cada ID tenha uma cor única do cmap
    cmap=cmap_qualitative,
    edgecolor='white',
    linewidth=0.7,
    alpha=0.6, # Alfa para que o mapa base seja visível
    zorder=2 # Ordem de empilhamento
)

# --- Plotagem do Limite do Município ---
city_boundary_gdf.plot(ax=ax, facecolor='none', edgecolor='black', linewidth=2.0, label='Limite do Município', zorder=4)

# --- Plotagem das Estações Pluviométricas ---
stations_in_polygons = thiessen_polygons_gdf['id_estacao'].unique()
stations_to_plot_gdf = stations_gdf[stations_gdf['id_estacao'].isin(stations_in_polygons)]

stations_to_plot_gdf.plot(ax=ax, marker='^', color='#e63946', markersize=60, edgecolor='black', label='Estações Pluviométricas', zorder=5)
# Adiciona rótulos para cada estação para fácil identificação
for x, y, label in zip(stations_to_plot_gdf.geometry.x, stations_to_plot_gdf.geometry.y, stations_to_plot_gdf.id_estacao):
    ax.text(x, y + 400, label, fontsize=8, ha='center', color='black',
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1), zorder=6)

# --- Adicionar Mapa Base (Basemap) ---
# O Contextily adiciona um mapa de fundo para dar contexto geográfico
# ctx.add_basemap(ax, crs=city_boundary_gdf.crs.to_string(), source=ctx.providers.CartoDB.Positron, zorder=1)

# --- Construção da Legenda Customizada ---
#station_info_for_legend = stations_gdf.set_index('id_estacao')
#legend_patches = []

# Limita a legenda a um número máximo de estações para clareza
max_legend_stations = 15
ids_for_legend = unique_station_ids[:max_legend_stations]

for sid in ids_for_legend:
    # Garante que o nome da estação existe, senão usa o ID
    if sid in station_info_for_legend.index:
        station_name = station_info_for_legend.loc[sid, "estacao"]
        legend_patches.append(mpatches.Patch(color=color_map[sid], label=f'Est. {sid} - {station_name}'))
    else:
        legend_patches.append(mpatches.Patch(color=color_map[sid], label=f'Estação {sid}'))

if len(unique_station_ids) > max_legend_stations:
     legend_patches.append(mpatches.Patch(color='lightgrey', label=f'... e mais {len(unique_station_ids)-max_legend_stations} estações'))

legend_patches.append(plt.Line2D([0], [0], color='black', lw=2, label='Limite do Município'))
legend_patches.append(plt.Line2D([0], [0], marker='^', color='#e63946', markeredgecolor='black', markersize=8, linestyle='None', label='Estações Pluviométricas'))

# --- Títulos, Rótulos e Finalização ---
ax.set_title('Polígonos de Thiessen para Estações Pluviométricas no Rio de Janeiro', fontsize=16, weight='bold')
ax.set_xlabel('Coordenada Leste (m)', fontsize=12)
ax.set_ylabel('Coordenada Norte (m)', fontsize=12)
ax.tick_params(axis='both', which='major', labelsize=10)
ax.grid(False) # A grade não é necessária com o mapa base
ax.set_axis_off() # Oculta os eixos para um visual de mapa mais limpo

plt.legend(handles=legend_patches, title="Legenda", fontsize=10, title_fontsize=12, loc='upper left', bbox_to_anchor=(1.02, 1))
plt.tight_layout(rect=[0, 0, 0.85, 1]) # Ajusta o layout para dar espaço à legenda
plt.show()

# %%
import matplotlib.pyplot as plt
import geopandas as gpd
import matplotlib.patches as mpatches
import contextily as ctx
import matplotlib.gridspec as gridspec # Importação necessária para o layout

# --- DADOS (Assumindo que seus GeoDataFrames 'thiessen_polygons_gdf', 
#             'city_boundary_gdf', e 'stations_gdf' já estão carregados) ---
# Exemplo de como seus dados devem estar estruturados:
# thiessen_polygons_gdf = gpd.read_file(...)
# city_boundary_gdf = gpd.read_file(...)
# stations_gdf = gpd.read_file(...)
# --------------------------------------------------------------------------


# --- Estilo e Configuração para Publicação ---
plt.style.use('seaborn-v0_8-paper')
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'

# --- Criação da Figura e Eixos com GridSpec ---
# Usamos GridSpec para ter controle total sobre o layout, 
# separando a área do mapa da área da legenda.
# A figura terá 15 polegadas de altura para acomodar a legenda abaixo.
fig = plt.figure(figsize=(12, 15))
# Cria uma grade de 2 linhas e 1 coluna. O mapa ocupará 4/5 do espaço e a legenda 1/5.
gs = gridspec.GridSpec(2, 1, height_ratios=[4, 1]) 

ax_map = fig.add_subplot(gs[0]) # Eixo para o mapa (superior)
ax_legend = fig.add_subplot(gs[1]) # Eixo para a legenda (inferior)

# --- Plotagem dos Polígonos de Thiessen ---
num_stations = len(thiessen_polygons_gdf['id_estacao'].unique())
cmap_qualitative = plt.get_cmap('viridis', num_stations)

unique_station_ids = sorted(thiessen_polygons_gdf['id_estacao'].unique())
color_map = {station_id: cmap_qualitative(i) for i, station_id in enumerate(unique_station_ids)}

thiessen_polygons_gdf.plot(
    ax=ax_map, # Plota no eixo do mapa
    column='id_estacao',
    categorical=True,
    cmap=cmap_qualitative,
    edgecolor='white',
    linewidth=0.7,
    alpha=0.6,
    zorder=2
)

# --- Plotagem do Limite do Município ---
city_boundary_gdf.plot(ax=ax_map, facecolor='none', edgecolor='black', linewidth=2.0, label='Limite do Município', zorder=4)

# --- Plotagem das Estações Pluviométricas ---
stations_in_polygons = thiessen_polygons_gdf['id_estacao'].unique()
stations_to_plot_gdf = stations_gdf[stations_gdf['id_estacao'].isin(stations_in_polygons)]

stations_to_plot_gdf.plot(ax=ax_map, marker='^', color='#e63946', markersize=60, edgecolor='black', label='Estações Pluviométricas', zorder=5)

for x, y, label in zip(stations_to_plot_gdf.geometry.x, stations_to_plot_gdf.geometry.y, stations_to_plot_gdf.id_estacao):
    ax_map.text(x, y + 400, label, fontsize=8, ha='center', color='black',
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1), zorder=6)

# --- Adicionar Mapa Base (Basemap) ---
# ctx.add_basemap(ax_map, crs=city_boundary_gdf.crs.to_string(), source=ctx.providers.CartoDB.Positron, zorder=1)

# --- Títulos e Configurações do Eixo do Mapa ---
ax_map.set_title('Polígonos de Thiessen para Estações Pluviométricas no Rio de Janeiro', fontsize=16, weight='bold')
ax_map.set_axis_off() # Oculta os eixos para um visual de mapa limpo

# Adiciona uma legenda simples para os símbolos principais diretamente no mapa
main_legend_handles = [
    plt.Line2D([0], [0], color='black', lw=2, label='Limite do Município'),
    plt.Line2D([0], [0], marker='^', color='#e63946', markeredgecolor='black', markersize=8, linestyle='None', label='Estações Pluviométricas')
]
ax_map.legend(handles=main_legend_handles, loc='upper right', fontsize=10)


###################################################################################
# --- INÍCIO DA SEÇÃO MODIFICADA: CONSTRUÇÃO DA LEGENDA TABELADA ---
###################################################################################

# 1. Desligar o eixo da área da legenda para usá-lo como um "canvas"
ax_legend.axis('off')

# 2. Preparar os itens da legenda para os polígonos
station_info_for_legend = stations_gdf.set_index('id_estacao')
legend_patches_stations = []

for sid in unique_station_ids:
    # Garante que o nome da estação existe, senão usa o ID
    if sid in station_info_for_legend.index:
        station_name = station_info_for_legend.loc[sid, "estacao"]
        # Formato: Quadrado colorido, ID da Estação - Nome da Estação
        label = f'{sid} - {station_name}'
        legend_patches_stations.append(mpatches.Patch(color=color_map[sid], label=label))
    else:
        # Caso não encontre o nome, usa apenas o ID
        legend_patches_stations.append(mpatches.Patch(color=color_map[sid], label=f'Estação {sid}'))

# 3. Criar a legenda tabelada no eixo inferior
#    - `handles`: os itens a serem exibidos (nossos quadrados coloridos)
#    - `ncol`: número de colunas. Ajuste conforme necessário para o seu número de estações.
#    - `loc`: 'center' para centralizar a tabela na área designada.
#    - `frameon`: False para remover a borda ao redor da legenda.
#    - `title`: Adiciona um título à legenda.
ax_legend.legend(
    handles=legend_patches_stations,
    ncol=3, # A legenda será organizada em 3 colunas. Altere para 4 se preferir.
    loc='center',
    fontsize=9,
    title="Legenda dos Polígonos de Thiessen (Estações Pluviométricas)",
    title_fontsize=12,
    frameon=False,
    labelspacing=1.0 # Aumenta o espaçamento vertical entre as linhas da legenda
)

###################################################################################
# --- FIM DA SEÇÃO MODIFICADA ---
###################################################################################

# --- Finalização e Exibição ---
# Ajusta o layout para evitar sobreposições e garantir que tudo caiba na figura
plt.tight_layout(pad=2.0)
plt.show()

# %%
import geopandas as gpd
import matplotlib.patches as mpatches
import contextily as ctx

# --- Estilo e Configuração para Publicação ---
plt.style.use('seaborn-v0_8-paper')
plt.rcParams['figure.dpi'] = 300 # Alta resolução para a figura
plt.rcParams['font.family'] = 'sans-serif'

# --- Criação da Figura e Eixo ---
# O GeoPandas e Contextily cuidam da projeção.
fig, ax = plt.subplots(1, 1, figsize=(12, 12))

# --- Plotagem dos Polígonos de Thiessen ---
# Mapa de cores para distinção visual das áreas das estações
num_stations = len(thiessen_polygons_gdf['id_estacao'].unique())
cmap_qualitative = plt.get_cmap('viridis', num_stations)

# Mapeia um ID de estação para uma cor para consistência
unique_station_ids = sorted(thiessen_polygons_gdf['id_estacao'].unique())
color_map = {station_id: cmap_qualitative(i) for i, station_id in enumerate(unique_station_ids)}

# Plota cada polígono com sua cor correspondente
thiessen_polygons_gdf.plot(
    ax=ax,
    column='id_estacao',
    categorical=True, # Garante que cada ID tenha uma cor única do cmap
    cmap=cmap_qualitative,
    edgecolor='white',
    linewidth=0.7,
    alpha=0.6, # Alfa para que o mapa base seja visível
    zorder=2 # Ordem de empilhamento
)

# --- Plotagem do Limite do Município ---
city_boundary_gdf.plot(ax=ax, facecolor='none', edgecolor='black', linewidth=2.0, label='Limite do Município', zorder=4)

# --- Plotagem das Estações Pluviométricas ---
stations_in_polygons = thiessen_polygons_gdf['id_estacao'].unique()
stations_to_plot_gdf = stations_gdf[stations_gdf['id_estacao'].isin(stations_in_polygons)]

stations_to_plot_gdf.plot(ax=ax, marker='^', color='#e63946', markersize=60, edgecolor='black', label='Estações Pluviométricas', zorder=5)
# Adiciona rótulos para cada estação para fácil identificação
for x, y, label in zip(stations_to_plot_gdf.geometry.x, stations_to_plot_gdf.geometry.y, stations_to_plot_gdf.id_estacao):
    ax.text(x, y + 400, label, fontsize=8, ha='center', color='black',
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1), zorder=6)

# --- Adicionar Mapa Base (Basemap) ---
# O Contextily adiciona um mapa de fundo para dar contexto geográfico
# ctx.add_basemap(ax, crs=city_boundary_gdf.crs.to_string(), source=ctx.providers.CartoDB.Positron, zorder=1)

# --- Construção da Legenda Customizada ---
station_info_for_legend = stations_gdf.set_index('id_estacao')
legend_patches = []

# Limita a legenda a um número máximo de estações para clareza
max_legend_stations = 15
ids_for_legend = unique_station_ids[:max_legend_stations]

for sid in ids_for_legend:
    # Garante que o nome da estação existe, senão usa o ID
    if sid in station_info_for_legend.index:
        station_name = station_info_for_legend.loc[sid, "estacao"]
        legend_patches.append(mpatches.Patch(color=color_map[sid], label=f'Est. {sid} - {station_name}'))
    else:
        legend_patches.append(mpatches.Patch(color=color_map[sid], label=f'Estação {sid}'))

if len(unique_station_ids) > max_legend_stations:
     legend_patches.append(mpatches.Patch(color='lightgrey', label=f'... e mais {len(unique_station_ids)-max_legend_stations} estações'))

legend_patches.append(plt.Line2D([0], [0], color='black', lw=2, label='Limite do Município'))
legend_patches.append(plt.Line2D([0], [0], marker='^', color='#e63946', markeredgecolor='black', markersize=8, linestyle='None', label='Estações Pluviométricas'))

# --- Títulos, Rótulos e Finalização ---
ax.set_title('Polígonos de Thiessen para Estações Pluviométricas no Rio de Janeiro', fontsize=16, weight='bold')
ax.set_xlabel('Coordenada Leste (m)', fontsize=12)
ax.set_ylabel('Coordenada Norte (m)', fontsize=12)
ax.tick_params(axis='both', which='major', labelsize=10)
ax.grid(False) # A grade não é necessária com o mapa base
ax.set_axis_off() # Oculta os eixos para um visual de mapa mais limpo

plt.legend(handles=legend_patches, title="Legenda", fontsize=10, title_fontsize=12, loc='upper left', bbox_to_anchor=(1.02, 1))
plt.tight_layout(rect=[0, 0, 0.85, 1]) # Ajusta o layout para dar espaço à legenda
plt.show()

# %% [markdown]
# ### 8.2. Time Series Plot of Areal Average Rainfall

# %%
plt.figure(figsize=(15, 6))
plt.plot(areal_rainfall_ts_df['timestamp'], areal_rainfall_ts_df['areal_avg_rainfall_mm_15min'], 
         marker='o', linestyle='-', markersize=4, color=sns.color_palette("viridis")[0], label='Areal Average Rainfall (15 min)')

plt.title('Estimated Areal Average Rainfall for Rio de Janeiro', fontsize=16)
plt.xlabel('Timestamp', fontsize=12)
plt.ylabel('Average Rainfall (mm / 15 min)', fontsize=12)
plt.xticks(rotation=45)
plt.legend(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

print("\nDescriptive statistics for calculated areal average rainfall:")
print(areal_rainfall_ts_df['areal_avg_rainfall_mm_15min'].describe())

# %% [markdown]
# ## 9. Conclusion
# 
# This notebook demonstrated the complete workflow for calculating areal average rainfall using static Thiessen polygons:
# 1.  Loaded and pre-processed rainfall data, station locations, and the city boundary.
# 2.  Transformed data to a projected CRS (SIRGAS 2000 / UTM Zone 23S) for accurate area calculations.
# 3.  Generated Thiessen polygons based on station locations and clipped them to the city boundary.
# 4.  Calculated the area and weight for each polygon.
# 5.  Merged these weights with 15-minute rainfall data to compute a time series of areal average rainfall.
# 6.  Visualized the Thiessen polygons on a map and plotted the resulting rainfall time series.
# 7.  Saved the key outputs (Thiessen polygons GeoDataFrame and areal rainfall CSV) for further use.
# 
# This method provides a standard approach for estimating spatially averaged rainfall. The accuracy depends on station density, distribution, and the representativeness of the "missing data means zero rain" assumption. For more complex scenarios, dynamic Thiessen polygons or geostatistical methods like kriging might be considered.

# %% [markdown]
# ---

# %% [markdown]
# # Analysis of Main Rain Periods

# %% [markdown]
# The following notebook section continues the analysis of the previously computed areal average rainfall data. It focuses on identifying and characterizing rainfall events using three different approaches: daily aggregation, continuous rain period definition, and a Peak Over Threshold (POT) methodology.
# 
# **Methodology Addendum:**
# 
# The areal average rainfall calculated in the previous sections represents the average rainfall over the portion of Rio de Janeiro covered by the generated Thiessen polygons (~790.75 km²), not the entire administrative area of the city (~1204.15 km²). This is due to the station distribution and the clipping process. Consequently, "city-wide" rainfall in this analysis refers to this specific covered area.
# 
# A preliminary step will be to regularize the areal average rainfall time series to a fixed 15-minute interval. The original `areal_rainfall_ts_df` timestamps could be irregular due to variations in data logging times across stations. Regularization ensures that event definition algorithms, which rely on consistent time steps, function correctly.
# 
# 10. **Advanced Rainfall Event Analysis**
#     *   10.1. Data Regularization and Preparation
#     *   10.2. Analysis 1: Daily Rainfall Aggregation
#         *   Identify rainy days.
#         *   Determine days with the most significant rainfall.
#         *   Visualize daily rainfall patterns.
#     *   10.3. Analysis 2: Continuous Rainfall Period Identification (Rain Events)
#         *   Define a "rain event" as a continuous period of rainfall, allowing for short dry interruptions.
#         *   Calculate properties for each event (start, end, duration, total rainfall, peak intensity).
#         *   Identify the most significant rain events.
#     *   10.4. Analysis 3: Peak Over Threshold (POT) Event Analysis
#         *   Define a high rainfall intensity threshold.
#         *   Identify periods where 15-minute rainfall exceeds this threshold.
#         *   Characterize these "extreme" rainfall events.
#     *   10.5. Comparative Discussion of Methods
#     *   10.6. Further Conclusions from Event Analysis
# 
# ---

# %%
# Continue from the previous notebook state.
# Ensure areal_rainfall_ts_df is loaded and available.
# If not, load it:
# areal_rainfall_ts_df = pd.read_csv(os.path.join(OUTPUT_DATA_DIRECTORY, AREAL_RAINFALL_FILENAME))

# Convert timestamp to datetime if loaded from CSV
if 'timestamp' in areal_rainfall_ts_df.columns and not pd.api.types.is_datetime64_any_dtype(areal_rainfall_ts_df['timestamp']):
    areal_rainfall_ts_df['timestamp'] = pd.to_datetime(areal_rainfall_ts_df['timestamp'])

# For plotting calendar heatmaps
# !pip install calmap
try:
    import calmap
except ImportError:
    print("calmap library not found. Calendar heatmap will be skipped. Install with: pip install calmap")
    calmap = None

import matplotlib.dates as mdates

# %% [markdown]
# ## 10. Advanced Rainfall Event Analysis
# 
# This section delves deeper into the `areal_rainfall_ts_df` to identify and characterize periods of significant rainfall. We will employ three distinct methodologies to understand rainfall patterns on daily and event-based scales.
# 
# **A Note on Areal Coverage:**
# It is important to reiterate that the "areal average rainfall" pertains to the sub-region of Rio de Janeiro covered by the Thiessen polygons generated (approximately 790.75 km² out of the city's total ~1204.15 km²). Conclusions about "city-wide" rain should be interpreted within this context.
# 
# ### 10.1. Data Regularization and Preparation
# 
# The `areal_rainfall_ts_df` may have timestamps at irregular intervals. For robust event analysis, especially methods relying on `shift()` or identifying consecutive periods, we need to regularize the time series to a constant frequency (15 minutes).

# %%
# Set timestamp as index for resampling
if not isinstance(areal_rainfall_ts_df.index, pd.DatetimeIndex):
    areal_rainfall_ts_df = areal_rainfall_ts_df.set_index('timestamp')

# Regularize to 15-minute frequency.
# Values in 'areal_avg_rainfall_mm_15min' are accumulations for 15-min periods ending at 'timestamp'.
# Resampling and summing is appropriate. Fill NaNs (intervals with no original data) with 0.
areal_rainfall_15T_df = areal_rainfall_ts_df['areal_avg_rainfall_mm_15min'].resample('15T').sum().fillna(0).reset_index()
areal_rainfall_15T_df.rename(columns={'areal_avg_rainfall_mm_15min': 'rainfall_mm_15min'}, inplace=True)

print("Regularized Areal Rainfall Time Series (first 5 rows):")
display(areal_rainfall_15T_df.head())
print(f"\nNumber of 15-minute intervals in regularized data: {len(areal_rainfall_15T_df)}")
print(f"Time range: {areal_rainfall_15T_df['timestamp'].min()} to {areal_rainfall_15T_df['timestamp'].max()}")

# Basic statistics of the regularized series
print("\nDescriptive statistics for regularized 15-min areal rainfall:")
display(areal_rainfall_15T_df['rainfall_mm_15min'].describe())

# %% [markdown]
# ### 10.2. Analysis 1: Daily Rainfall Aggregation
# 
# This analysis focuses on identifying days with rainfall and quantifying the total rainfall for those days.

# %%
# Aggregate 15-minute data to daily totals
daily_rainfall_df = areal_rainfall_15T_df.set_index('timestamp')['rainfall_mm_15min'].resample('D').sum().reset_index()
daily_rainfall_df.rename(columns={'rainfall_mm_15min': 'total_daily_rainfall_mm'}, inplace=True)

# Identify rainy days (days with total rainfall > 0)
# A very small threshold can be used to avoid floating point issues if necessary, e.g., 0.001 mm
min_rain_for_rainy_day = 0.01 # mm
rainy_days_df = daily_rainfall_df[daily_rainfall_df['total_daily_rainfall_mm'] > min_rain_for_rainy_day].copy()

print(f"Total number of days in the dataset: {len(daily_rainfall_df)}")
print(f"Number of days with rainfall (> {min_rain_for_rainy_day} mm): {len(rainy_days_df)}")
if len(daily_rainfall_df) > 0:
    print(f"Percentage of rainy days: {(len(rainy_days_df) / len(daily_rainfall_df) * 100):.2f}%")

# Days with the most rain
top_n_days = 10
most_rainy_days = rainy_days_df.sort_values(by='total_daily_rainfall_mm', ascending=False).head(top_n_days)

print(f"\nTop {top_n_days} days with the most areal rainfall:")
display(most_rainy_days)

# %% [markdown]
# #### Visualizations for Daily Rainfall

# %%
# Plot 1: Time Series of Daily Rainfall (Sample)
# To avoid plotting too many points if the series is long, plot a sample or a specific year.
sample_period_daily_plot = daily_rainfall_df.set_index('timestamp')
if len(sample_period_daily_plot) > 365 * 2: # If more than 2 years of data, plot last 2 years
    sample_period_daily_plot = sample_period_daily_plot.last('730D')

plt.figure(figsize=(15, 6))
plt.bar(sample_period_daily_plot.index, sample_period_daily_plot['total_daily_rainfall_mm'], 
        color=sns.color_palette("viridis")[2], width=0.9)
plt.title(f'Daily Areal Rainfall (Sample: Last {len(sample_period_daily_plot)//30 if len(sample_period_daily_plot) > 0 else 0}-Month Period)', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Total Daily Rainfall (mm)', fontsize=12)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Plot 2: Bar Chart of Top N Rainy Days
plt.figure(figsize=(12, 7))
sns.barplot(x='total_daily_rainfall_mm', y=most_rainy_days['timestamp'].dt.strftime('%Y-%m-%d'), 
            data=most_rainy_days, palette='viridis_r', orient='h')
plt.title(f'Top {top_n_days} Days with Highest Areal Rainfall', fontsize=16)
plt.xlabel('Total Daily Rainfall (mm)', fontsize=12)
plt.ylabel('Date', fontsize=12)
plt.yticks(fontsize=10)
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Plot 3: Calendar Heatmap of Daily Rainfall (if calmap is available and data is sufficient)
if calmap and not daily_rainfall_df.empty and len(daily_rainfall_df) > 30 : # Ensure there's enough data for a meaningful calendar
    plt.figure(figsize=(16, 10))
    # Calmap expects a Series with DatetimeIndex
    daily_rainfall_series_for_calmap = daily_rainfall_df.set_index('timestamp')['total_daily_rainfall_mm']
    
    # Determine years to plot: if many years, pick the most recent ones or ones with significant rain
    unique_years = daily_rainfall_series_for_calmap.index.year.unique()
    if len(unique_years) > 3: # Limit to last 3 years or years of top events for clarity
        # Consider years of top rainy days
        years_of_top_days = most_rainy_days['timestamp'].dt.year.unique()
        # Or simply the last few years
        years_to_plot = sorted(unique_years, reverse=True)[:min(3, len(unique_years))]
        daily_rainfall_series_for_calmap = daily_rainfall_series_for_calmap[daily_rainfall_series_for_calmap.index.year.isin(years_to_plot)]

    if not daily_rainfall_series_for_calmap.empty:
        try:
            calmap.yearplot(daily_rainfall_series_for_calmap, year=years_to_plot[0] if len(years_to_plot)==1 else None, cmap='viridis', linewidth=1, fillcolor='lightgrey')
            plt.suptitle('Calendar Heatmap of Daily Areal Rainfall', fontsize=18, y=1.02 if len(years_to_plot)>1 else 0.95) # Adjust y for multi-year plots
            plt.tight_layout() # May need adjustment depending on number of years
            plt.show()
        except Exception as e:
            print(f"Could not generate calendar heatmap: {e}")
    else:
        print("Not enough data in the selected years for calendar heatmap after filtering.")

else:
    if not calmap:
        print("Skipping calendar heatmap as 'calmap' library is not installed.")
    else:
        print("Skipping calendar heatmap due to insufficient data length.")

# %% [markdown]
# ### 10.3. Analysis 2: Continuous Rainfall Period Identification (Rain Events)
# 
# This analysis aims to identify continuous "rain events." An event starts when rain begins after a dry period and ends when rain ceases for a specified minimum duration.

# %%
def identify_rain_events(rainfall_series, rain_threshold, min_dry_spell_duration_for_separation):
    """
    Identifies continuous rain events from a rainfall time series.

    Args:
        rainfall_series (pd.Series): Time series of rainfall data, indexed by timestamp.
                                     Assumes regular time intervals.
        rain_threshold (float): Minimum rainfall intensity to be considered "raining".
        min_dry_spell_duration_for_separation (pd.Timedelta): Minimum duration of no rain
                                                               to separate two events.

    Returns:
        pd.DataFrame: DataFrame with columns ['event_id', 'start_time', 'end_time',
                                            'duration', 'total_rainfall_mm',
                                            'peak_15min_intensity_mm', 'avg_intensity_mm_hr'].
    """
    df = rainfall_series.to_frame()
    col_name = rainfall_series.name if rainfall_series.name else 'rainfall'
    df.rename(columns={col_name:'rainfall'}, inplace=True)

    df['is_raining'] = df['rainfall'] > rain_threshold
    
    # Identify blocks of continuous rain/no_rain
    df['block_change'] = df['is_raining'].diff().fillna(False)
    df['block_id'] = df['block_change'].cumsum()

    events = []
    current_event_id_counter = 0
    
    # Iterate through blocks, focusing on rainy ones
    for block_id, group in df.groupby('block_id'):
        if not group['is_raining'].any(): # Skip dry blocks
            continue

        # This is a continuous block of rain.
        # Now, check if this block should be merged with the previous recorded event.
        start_time = group.index.min()
        end_time = group.index.max()
        
        if not events: # First rainy block starts the first event
            current_event_id_counter += 1
            current_event = {
                'event_id': current_event_id_counter,
                'start_time': start_time,
                'end_time': end_time, # Will be updated if merged
                'rain_periods': [(start_time, end_time)] # Store individual rainy periods
            }
            events.append(current_event)
        else:
            last_event = events[-1]
            # Time difference between end of last rain period in last_event and start of current block
            # The last_event's 'end_time' is the end of its last known rainy segment.
            time_since_last_rain = start_time - last_event['rain_periods'][-1][1]
            
            # Infer interval length from the index for accurate dry spell calculation
            # The diff gives time to the *start* of the current interval. We need interval_length for precise end.
            if len(df.index) > 1:
                 inferred_interval = df.index[1] - df.index[0]
            else: # fallback for very short series
                 inferred_interval = pd.Timedelta(minutes=15)


            # If the dry spell between the previous event's last rain and this block's start
            # is short enough, merge them. Note: `time_since_last_rain` includes one interval from the previous block's end.
            # A dry spell means `is_raining` was false.
            # `min_dry_spell_duration_for_separation` refers to the actual duration of the dry period.
            # If `start_time` is the beginning of a 15-min interval, and `last_event['rain_periods'][-1][1]`
            # is the beginning of the last 15-min interval of rain in the previous event,
            # then `time_since_last_rain - inferred_interval` represents the duration of the dry spell between them.
            
            actual_dry_spell_duration = time_since_last_rain - inferred_interval # Assuming end_time is start of last interval
            
            if actual_dry_spell_duration <= min_dry_spell_duration_for_separation:
                # Merge with the last event
                last_event['end_time'] = end_time # Update overall event end time
                last_event['rain_periods'].append((start_time, end_time))
            else:
                # Start a new event
                current_event_id_counter += 1
                current_event = {
                    'event_id': current_event_id_counter,
                    'start_time': start_time,
                    'end_time': end_time,
                    'rain_periods': [(start_time, end_time)]
                }
                events.append(current_event)

    if not events:
        return pd.DataFrame(columns=['event_id', 'start_time', 'end_time', 'duration', 
                                     'total_rainfall_mm', 'peak_15min_intensity_mm', 'avg_intensity_mm_hr'])

    # Process event list to create final DataFrame
    event_summary_list = []
    for event_data in events:
        # Consolidate start_time for the event (min of all start_times in rain_periods)
        # Overall start_time is already the start of the first rain period.
        # Overall end_time needs to be the end of the last 15-min interval of the last rain_period.
        
        # This is slightly tricky because event_data['end_time'] is the *start* of the last 15-min interval.
        # We need to add the interval length to get the true end.
        true_event_end_time = event_data['end_time'] + inferred_interval
        duration = true_event_end_time - event_data['start_time']
        
        # Extract all rainfall data for this event period
        event_rainfall_series = rainfall_series.loc[event_data['start_time']:event_data['end_time']]
        total_rainfall = event_rainfall_series.sum()
        peak_intensity = event_rainfall_series.max()
        
        duration_hours = duration.total_seconds() / 3600
        avg_intensity_mm_hr = total_rainfall / duration_hours if duration_hours > 0 else 0
        
        event_summary_list.append({
            'event_id': event_data['event_id'],
            'start_time': event_data['start_time'],
            'end_time': true_event_end_time, # Use the true end time
            'duration': duration,
            'total_rainfall_mm': total_rainfall,
            'peak_15min_intensity_mm': peak_intensity,
            'avg_intensity_mm_hr': avg_intensity_mm_hr
        })
        
    events_df = pd.DataFrame(event_summary_list)
    return events_df

# Parameters for rain event definition
RAIN_THRESHOLD_FOR_EVENT = 0.01  # mm in a 15-min interval to be considered "raining"
MIN_DRY_SPELL_HOURS = 1       # e.g., 1 hour of no rain separates events
MIN_DRY_SPELL_DURATION = pd.Timedelta(hours=MIN_DRY_SPELL_HOURS)

# Prepare series for event identification
rainfall_series_for_events = areal_rainfall_15T_df.set_index('timestamp')['rainfall_mm_15min']

# Identify events
rain_events_df = identify_rain_events(rainfall_series_for_events, 
                                      RAIN_THRESHOLD_FOR_EVENT, 
                                      MIN_DRY_SPELL_DURATION)

print(f"\nIdentified {len(rain_events_df)} rain events with a separation of {MIN_DRY_SPELL_HOURS} dry hours.")
if not rain_events_df.empty:
    print("Summary of identified rain events:")
    display(rain_events_df.describe(percentiles=[.5, .75, .9, .95, .99]))

    # Top N events by total rainfall
    top_n_events = 10
    most_intense_events = rain_events_df.sort_values(by='total_rainfall_mm', ascending=False).head(top_n_events)
    print(f"\nTop {top_n_events} rain events by total rainfall:")
    display(most_intense_events[['event_id', 'start_time', 'end_time', 'duration', 'total_rainfall_mm', 'peak_15min_intensity_mm', 'avg_intensity_mm_hr']])
else:
    print("No rain events identified with the current parameters.")

# %% [markdown]
# #### Visualizations for Rain Events

# %%
if not rain_events_df.empty and not most_intense_events.empty:
    # Plot 1: Gantt-like chart of Top N Rain Events
    plt.figure(figsize=(15, 8))
    for i, event_row in most_intense_events.iterrows():
        plt.plot([event_row['start_time'], event_row['end_time']], [i, i], 
                 linewidth=5, solid_capstyle='butt', 
                 label=f"Event {event_row['event_id']} ({event_row['total_rainfall_mm']:.1f}mm)")
    
    # Use actual event IDs or rank for y-ticks if preferred
    plt.yticks(most_intense_events.index, [f"Event {eid}" for eid in most_intense_events['event_id']]) 
    plt.gca().invert_yaxis() # Show event with largest rainfall at top

    plt.title(f'Top {top_n_events} Rain Events by Total Rainfall', fontsize=16)
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Event Rank (by total rainfall)', fontsize=12)
    plt.xticks(rotation=45)
    plt.legend(title="Event (Total Rainfall)", bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.5, axis='x')
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    plt.show()

    # Plot 2: Rainfall Pattern for one of the Top Events
    # Select the event with the absolute highest total rainfall
    top_event_details = most_intense_events.iloc[0]
    
    plt.figure(figsize=(15, 6))
    event_period_data = areal_rainfall_15T_df[
        (areal_rainfall_15T_df['timestamp'] >= top_event_details['start_time']) &
        (areal_rainfall_15T_df['timestamp'] < top_event_details['end_time']) # Use < end_time because end_time is start of next interval
    ]
    plt.bar(event_period_data['timestamp'], event_period_data['rainfall_mm_15min'], 
            width=0.01, # Approx 15min width on date axis
            color=sns.color_palette("viridis")[3])
    
    plt.title(f"Rainfall Pattern for Top Event ID {top_event_details['event_id']} (Started: {top_event_details['start_time'].strftime('%Y-%m-%d %H:%M')})", fontsize=16)
    plt.xlabel('Timestamp (15-minute intervals)', fontsize=12)
    plt.ylabel('Rainfall (mm/15min)', fontsize=12)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
else:
    print("Skipping event visualizations as no significant events were identified or data is insufficient.")

# %% [markdown]
# ### 10.4. Analysis 3: Peak Over Threshold (POT) Event Analysis
# 
# This method focuses on identifying "extreme" rainfall periods by selecting rainfall intensities that exceed a defined threshold. These exceedances are then clustered into POT events.

# %%
def identify_pot_events(rainfall_series, pot_threshold, min_exceedance_intervals, max_time_between_exceedances_for_clustering):
    """
    Identifies Peak Over Threshold (POT) events.

    Args:
        rainfall_series (pd.Series): Time series of rainfall data, indexed by timestamp (regular intervals).
        pot_threshold (float): Rainfall intensity threshold for an interval to be considered an exceedance.
        min_exceedance_intervals (int): Minimum number of consecutive 15-min intervals an exceedance must last.
        max_time_between_exceedances_for_clustering (pd.Timedelta): Max time between end of one
                                                                    exceedance block and start of next
                                                                    to cluster them into one POT event.
    Returns:
        pd.DataFrame: DataFrame of POT events.
    """
    df = rainfall_series.to_frame()
    col_name = rainfall_series.name if rainfall_series.name else 'rainfall'
    df.rename(columns={col_name:'rainfall'}, inplace=True)

    df['is_exceedance'] = df['rainfall'] > pot_threshold
    
    # Filter out short exceedances
    df['exceedance_block_id'] = (df['is_exceedance'] != df['is_exceedance'].shift()).cumsum()
    block_counts = df.groupby('exceedance_block_id')['is_exceedance'].count()
    
    # Keep only blocks that are actual exceedances AND meet min_duration
    valid_exceedance_blocks = df[df['is_exceedance']]['exceedance_block_id'].unique()
    
    filtered_exceedance_ids = []
    for block_id in valid_exceedance_blocks:
        if block_counts[block_id] >= min_exceedance_intervals:
            filtered_exceedance_ids.append(block_id)
            
    df['is_valid_exceedance_period'] = df['exceedance_block_id'].isin(filtered_exceedance_ids) & df['is_exceedance']

    # Now, cluster these valid_exceedance_periods if they are close enough
    # This is similar to the rain event identification logic.
    df['pot_event_change'] = df['is_valid_exceedance_period'].diff().fillna(False)
    df['pot_block_id'] = df['pot_event_change'].cumsum() # New blocks of valid exceedances or non-exceedances

    pot_events = []
    current_pot_event_id_counter = 0
    inferred_interval = pd.Timedelta(minutes=15) # Assuming 15-min data as per regularization
    if len(df.index) > 1:
         inferred_interval = df.index[1] - df.index[0]


    for block_id, group in df.groupby('pot_block_id'):
        if not group['is_valid_exceedance_period'].any(): # Skip non-exceedance blocks
            continue

        start_time = group.index.min()
        end_time = group.index.max() # This is the start of the last 15-min interval in this block
        
        if not pot_events:
            current_pot_event_id_counter += 1
            current_pot_event = {
                'pot_event_id': current_pot_event_id_counter,
                'start_time': start_time, # Start of first exceedance
                'end_time': end_time,     # Start of last exceedance interval in this block
                'exceedance_periods': [(start_time, end_time)]
            }
            pot_events.append(current_pot_event)
        else:
            last_pot_event = pot_events[-1]
            # Time diff between end of last exceedance period in last_pot_event and start of current block
            # last_pot_event['exceedance_periods'][-1][1] is the timestamp of the last interval of exceedance.
            time_since_last_exceedance_block = start_time - last_pot_event['exceedance_periods'][-1][1]
            
            # The actual gap (dry or below threshold) between end of one exceedance and start of next
            actual_gap_duration = time_since_last_exceedance_block - inferred_interval
            
            if actual_gap_duration <= max_time_between_exceedances_for_clustering:
                last_pot_event['end_time'] = end_time # Update overall event end time (of exceedance period)
                last_pot_event['exceedance_periods'].append((start_time, end_time))
            else:
                current_pot_event_id_counter += 1
                current_pot_event = {
                    'pot_event_id': current_pot_event_id_counter,
                    'start_time': start_time,
                    'end_time': end_time,
                    'exceedance_periods': [(start_time, end_time)]
                }
                pot_events.append(current_pot_event)
    
    if not pot_events:
         return pd.DataFrame()

    # Final processing for POT events
    pot_event_summary_list = []
    for pot_event_data in pot_events:
        # The event boundary for POT analysis often includes the "shoulders" -
        # i.e., the full rain event encompassing the exceedances.
        # Here, we define POT event start/end strictly by the clustered exceedance periods.
        true_pot_event_start_time = pot_event_data['start_time']
        # End time needs to be the end of the last 15-min interval of the last exceedance period
        true_pot_event_end_time = pot_event_data['end_time'] + inferred_interval
        
        duration_of_exceedance_phase = true_pot_event_end_time - true_pot_event_start_time
        
        # Rainfall characteristics *during the period of exceedance*
        exceedance_phase_rainfall_series = rainfall_series.loc[true_pot_event_start_time : pot_event_data['end_time']] # Slicing includes end
        
        total_rainfall_during_exceedance = exceedance_phase_rainfall_series.sum()
        peak_15min_intensity_during_exceedance = exceedance_phase_rainfall_series.max()
        
        # Sum of (rainfall - threshold) for intervals that are part of the valid exceedance
        magnitude_over_threshold = exceedance_phase_rainfall_series[exceedance_phase_rainfall_series > pot_threshold].apply(lambda x: x - pot_threshold).sum()
        
        # Number of 15-min intervals where threshold was exceeded within this event
        num_exceeding_intervals = len(exceedance_phase_rainfall_series[exceedance_phase_rainfall_series > pot_threshold])

        pot_event_summary_list.append({
            'pot_event_id': pot_event_data['pot_event_id'],
            'start_time': true_pot_event_start_time,
            'end_time': true_pot_event_end_time,
            'duration_exceedance_phase': duration_of_exceedance_phase,
            'num_exceeding_intervals': num_exceeding_intervals,
            'total_rainfall_during_exceedance_phase': total_rainfall_during_exceedance,
            'peak_15min_intensity_during_exceedance_phase': peak_15min_intensity_during_exceedance,
            'magnitude_over_threshold_mm': magnitude_over_threshold
        })
        
    pot_events_df = pd.DataFrame(pot_event_summary_list)
    return pot_events_df


# Parameters for POT analysis
# Define POT threshold: e.g., 95th percentile of non-zero 15-min rainfall, or a fixed value.
non_zero_rainfall = rainfall_series_for_events[rainfall_series_for_events > RAIN_THRESHOLD_FOR_EVENT]
if not non_zero_rainfall.empty:
    POT_INTENSITY_THRESHOLD = non_zero_rainfall.quantile(0.95) # e.g., 95th percentile
else:
    POT_INTENSITY_THRESHOLD = 1.0 # fallback if no/little rain (mm/15min)
print(f"POT Intensity Threshold (e.g., 95th percentile of rainy intervals): {POT_INTENSITY_THRESHOLD:.2f} mm/15min")

MIN_EXCEEDANCE_INTERVALS = 2  # e.g., must exceed threshold for at least 2*15 = 30 minutes
MAX_TIME_BETWEEN_EXCEEDANCES_HOURS = 3 # e.g., 3 hours
MAX_TIME_BETWEEN_EXCEEDANCES = pd.Timedelta(hours=MAX_TIME_BETWEEN_EXCEEDANCES_HOURS)

pot_events_df = identify_pot_events(rainfall_series_for_events,
                                    POT_INTENSITY_THRESHOLD,
                                    MIN_EXCEEDANCE_INTERVALS,
                                    MAX_TIME_BETWEEN_EXCEEDANCES)

print(f"\nIdentified {len(pot_events_df)} POT events.")
if not pot_events_df.empty:
    print("Summary of identified POT events:")
    display(pot_events_df.describe(percentiles=[.5, .75, .9, .95, .99]))

    top_n_pot_events = 10
    # Sort by magnitude over threshold or total rainfall during exceedance
    most_significant_pot_events = pot_events_df.sort_values(by='magnitude_over_threshold_mm', ascending=False).head(top_n_pot_events)
    
    print(f"\nTop {top_n_pot_events} POT events by magnitude over threshold:")
    display(most_significant_pot_events)
else:
    print("No POT events identified with the current parameters (threshold might be too high for this dataset).")

# %% [markdown]
# #### Visualizations for POT Events

# %%
if not pot_events_df.empty and not most_significant_pot_events.empty:
    # Plot 1: Overall time series with POT threshold and highlighted POT events (sample period)
    plt.figure(figsize=(18, 7))
    
    # Select a sample period for clarity, e.g., a period containing some of the top POT events
    if not most_significant_pot_events.empty:
        sample_start = most_significant_pot_events['start_time'].min() - pd.Timedelta(days=1)
        sample_end = most_significant_pot_events['end_time'].max() + pd.Timedelta(days=1)
        
        # Ensure sample isn't excessively long if events are very spread out
        if (sample_end - sample_start) > pd.Timedelta(days=90): # Limit to ~3 months window for this plot
             sample_start_ref = most_significant_pot_events.iloc[0]['start_time']
             # sample_start = sample_start_ref - pd.Timedelta(days=15)
             # sample_end = sample_start_ref + pd.Timedelta(days=15)
             sample_start = sample_start_ref - pd.Timedelta(days=365 * 5)
             sample_end = sample_start_ref + pd.Timedelta(days=365 * 5)
        
        plot_data_pot = areal_rainfall_15T_df[
            (areal_rainfall_15T_df['timestamp'] >= sample_start) & 
            (areal_rainfall_15T_df['timestamp'] <= sample_end)
        ]
    else: # Fallback to last N days if no specific events to center on
        plot_data_pot = areal_rainfall_15T_df.last('30D')


    plt.plot(plot_data_pot['timestamp'], plot_data_pot['rainfall_mm_15min'], 
             label='Areal Rainfall (15 min)', color='lightblue', zorder=1)
    plt.axhline(POT_INTENSITY_THRESHOLD, color='red', linestyle='--', 
                label=f'POT Threshold ({POT_INTENSITY_THRESHOLD:.2f} mm/15min)', zorder=2)

    for idx, event_row in most_significant_pot_events.iterrows():
        # Check if event falls within the plot_data_pot range
        if event_row['start_time'] <= plot_data_pot['timestamp'].max() and \
           event_row['end_time'] >= plot_data_pot['timestamp'].min():
            
            plt.fill_between(
                x=[event_row['start_time'], event_row['end_time']],
                y1=POT_INTENSITY_THRESHOLD, # Start highlighting from threshold
                y2=plot_data_pot['rainfall_mm_15min'].loc[
                    (plot_data_pot['timestamp'] >= event_row['start_time']) & 
                    (plot_data_pot['timestamp'] < event_row['end_time'])
                    ].max() if not plot_data_pot.empty else POT_INTENSITY_THRESHOLD + 1, # Highlight up to peak in event
                color=sns.color_palette("autumn")[1], alpha=0.5, 
                label=f"POT Event {event_row['pot_event_id']}" if idx == most_significant_pot_events.index[0] else None, # Label first one
                zorder=3
            )
            # Also shade the full height of the rainfall during the event duration
            event_specific_data = plot_data_pot[
                (plot_data_pot['timestamp'] >= event_row['start_time']) &
                (plot_data_pot['timestamp'] < event_row['end_time']) # end_time is exclusive for intervals
            ]
            if not event_specific_data.empty:
                 plt.bar(event_specific_data['timestamp'], event_specific_data['rainfall_mm_15min'],
                        width= (event_specific_data['timestamp'].iloc[1]-event_specific_data['timestamp'].iloc[0]) if len(event_specific_data)>1 else 0.01, # Approx 15min width
                        color=sns.color_palette("autumn")[3], alpha=0.7, zorder=4)


    plt.title(f'Areal Rainfall with Highlighted POT Events (Sample Period)', fontsize=16)
    plt.xlabel('Timestamp', fontsize=12)
    plt.ylabel('Rainfall (mm/15min)', fontsize=12)
    plt.legend(loc='upper right')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.xticks(rotation=30)
    plt.ylim(bottom=0) # Ensure y-axis starts at 0
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()
else:
    print("Skipping POT event visualizations as no significant POT events were identified or data is insufficient.")

# %% [markdown]
# ## 10.5. Comparative Discussion of Methods
# 
# The three analyses provide different perspectives on rainy periods in Rio de Janeiro (for the covered area):
# 
# 1.  **Daily Rainfall Aggregation:**
#     *   **Pros:** Simple to calculate and understand. Useful for general climate summaries, agricultural impact, or daily operational planning. Aligns well with common reporting standards.
#     *   **Cons:** Masks intra-day rainfall variability (e.g., a short, intense storm vs. prolonged light rain might yield similar daily totals). Does not directly identify individual storm events if they span across midnight.
#     *   **Best for:** Identifying overall wettest days, long-term trends in daily rainfall. The results showed `X` rainy days, with the top day receiving `Y` mm.
# 
# 2.  **Continuous Rainfall Period Identification (Rain Events):**
#     *   **Pros:** Defines hydrologically meaningful events based on continuous rainfall, allowing for brief interruptions. Captures event duration, total volume, and peak/average intensities within an event. More aligned with how actual storm systems behave.
#     *   **Cons:** Definition is sensitive to parameters like `rain_threshold` and `min_dry_spell_duration`. The algorithm for merging rain blocks can be complex.
#     *   **Best for:** Flood risk assessment, studying storm characteristics (duration, intensity), understanding water resource inputs from individual systems. We identified `N` such events, with the largest event lasting `D` hours and delivering `R` mm.
# 
# 3.  **Peak Over Threshold (POT) Event Analysis:**
#     *   **Pros:** Focuses specifically on periods of high-intensity rainfall, which are often linked to flash floods, erosion, or infrastructure strain. Based on established extreme value theory principles.
#     *   **Cons:** Results are highly dependent on the chosen `pot_threshold`. May not capture prolonged, moderate rainfall events if they don't exceed the intensity threshold, even if their total volume is significant. Definition of event start/end (e.g., shoulders vs. just exceedance period) can vary.
#     *   **Best for:** Analyzing extreme rainfall characteristics, designing infrastructure for peak loads, issuing warnings for high-impact weather. The analysis highlighted `M` periods of extreme intensity, with the most severe having a peak of `P` mm/15min.
# 
# **Synergies:**
# These methods are complementary. Daily totals can provide context. Rain event analysis can describe typical storm structures. POT analysis can pinpoint the most hazardous short-duration rainfalls. For instance, a "top rainy day" might consist of one large "rain event" which also qualifies as a "POT event", or it could be due to multiple smaller events.
# 
# The choice of method depends on the specific research question or application. For comprehensive hydrological risk assessment, elements from both event-based approaches (Analysis 2 and 3) are often valuable.
# 
# ## 10.6. Further Conclusions from Event Analysis
# 
# *(This section would be populated after observing the actual numerical and visual outputs from a more complete dataset. Given the sample data's sparseness, definitive conclusions about Rio's rainfall climatology are illustrative here.)*
# 
# From the analyses performed on the available dataset:
# 
# *   **Rainfall Occurrence:** The daily analysis indicated that rainfall (above a minor threshold) occurred on approximately `[Insert percentage from 10.2]`% of days. This provides a baseline understanding of rain frequency.
# *   **Significant Daily Rainfall:** The top rainy days (e.g., `[Insert value from most_rainy_days.total_daily_rainfall_mm.max()]` mm on `[Insert date]`) represent substantial water input over the monitored area. These days would likely correlate with significant impacts.
# *   **Rain Event Characteristics:** The event analysis (Method 2) revealed `[Insert len(rain_events_df)]` distinct rain events. The distribution of event durations and total rainfalls (e.g., median duration `[Insert median from rain_events_df.duration.describe()]`, median total `[Insert median from rain_events_df.total_rainfall_mm.describe()]`) helps characterize typical storm systems. The most significant event identified delivered `[Insert max total_rainfall_mm from rain_events_df]` mm over `[Insert corresponding duration]`.
# *   **Extreme Intensities:** The POT analysis, using a threshold of `[Insert POT_INTENSITY_THRESHOLD]` mm/15min, pinpointed `[Insert len(pot_events_df)]` periods of particularly high rainfall rates. The peak 15-minute intensity observed in these events was `[Insert max peak_15min_intensity_during_exceedance_phase from pot_events_df]`. Such intensities are critical for understanding flash flood potential.
# 
# The limited nature of the initial `alertario` sample data (100,000 rows) means these findings are illustrative of the methodology rather than definitive climatological statements for Rio de Janeiro. A more extensive dataset would yield more robust statistics and potentially reveal clearer patterns in event occurrence, seasonality, and intensity.
# 
# Future work could involve:
# *   Analyzing seasonality of these event types.
# *   Correlating significant rain events with reported incidents (e.g., `ocorrencias_gdf`).
# *   Applying these methods to individual station data to understand spatial variability in event characteristics.
# *   Refining event definition parameters based on local hydrological knowledge or sensitivity analyses.
# 
# This concludes the advanced rainfall event analysis. The generated dataframes (`daily_rainfall_df`, `rain_events_df`, `pot_events_df`) can be saved and used for further specialized studies.

# %%
# --- Save Outputs from Advanced Analysis (Optional) ---
# Define output paths for the new DFs

DAILY_RAINFALL_FILENAME = 'daily_areal_rainfall_rio.csv'
RAIN_EVENTS_FILENAME = 'rain_events_rio.csv'
POT_EVENTS_FILENAME = 'pot_events_rio.csv'

# Save daily rainfall data
daily_rainfall_output_path = os.path.join(OUTPUT_DATA_DIRECTORY, DAILY_RAINFALL_FILENAME)
try:
    daily_rainfall_df.to_csv(daily_rainfall_output_path, index=False)
    print(f"\nDaily areal rainfall data saved to: {daily_rainfall_output_path}")
except Exception as e:
    print(f"Error saving daily rainfall data: {e}")

# Save rain events data
if not rain_events_df.empty:
    rain_events_output_path = os.path.join(OUTPUT_DATA_DIRECTORY, RAIN_EVENTS_FILENAME)
    try:
        rain_events_df.to_csv(rain_events_output_path, index=False)
        print(f"Rain events data saved to: {rain_events_output_path}")
    except Exception as e:
        print(f"Error saving rain events data: {e}")
else:
    print("Rain events DataFrame is empty, not saving.")

# Save POT events data
if not pot_events_df.empty:
    pot_events_output_path = os.path.join(OUTPUT_DATA_DIRECTORY, POT_EVENTS_FILENAME)
    try:
        pot_events_df.to_csv(pot_events_output_path, index=False)
        print(f"POT events data saved to: {pot_events_output_path}")
    except Exception as e:
        print(f"Error saving POT events data: {e}")
else:
    print("POT events DataFrame is empty, not saving.")

# %% [markdown]
# ---

# %% [markdown]
# # Evaluate and Compare Methods to Find Rain Periods

# %%
# Ensure all necessary imports from the previous part of the notebook are available
import os
import pandas as pd
import geopandas as gpd
import numpy as np
from scipy.spatial import Voronoi
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches # For custom legends
import seaborn as sns
import matplotlib.dates as mdates

try:
    import calmap
except ImportError:
    print("calmap library not found. Calendar heatmap will be skipped. Install with: pip install calmap")
    calmap = None

# Plotting style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("viridis")
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 50)

# Assuming the following DataFrames are loaded and processed from the previous notebook sections:
# areal_rainfall_ts_df: Original areal rainfall time series
# areal_rainfall_15T_df: Regularized 15-minute areal rainfall
# daily_rainfall_df: Daily aggregated rainfall
# most_rainy_days: Top N daily rainfall events
# rain_events_df: Identified continuous rain events
# most_intense_events: Top N continuous rain events
# pot_events_df: Identified POT events
# most_significant_pot_events: Top N POT events

# Also, constants like OUTPUT_DATA_DIRECTORY, CRS_*, etc. are assumed to be defined.
# For this continuation, let's ensure the key dataframes are explicitly available or reloaded if necessary.
# (In a real continuous notebook, they would be in memory. For robustness in a new cell block, we might reload)

# --- Define Paths (if not already defined, or for standalone execution of this part) ---
OUTPUT_DATA_DIRECTORY = '../../../../../data/meteorologia/processed/thiessen_analysis' # Adjust if necessary
AREAL_RAINFALL_FILENAME = 'areal_rainfall_15min_rio.csv'
DAILY_RAINFALL_FILENAME = 'daily_areal_rainfall_rio.csv'
RAIN_EVENTS_FILENAME = 'rain_events_rio.csv'
POT_EVENTS_FILENAME = 'pot_events_rio.csv'

# Load data if not in memory (example)
try:
    if 'areal_rainfall_15T_df' not in locals():
        areal_rainfall_ts_df_loaded = pd.read_csv(os.path.join(OUTPUT_DATA_DIRECTORY, AREAL_RAINFALL_FILENAME), parse_dates=['timestamp'])
        areal_rainfall_ts_df_loaded = areal_rainfall_ts_df_loaded.set_index('timestamp')
        areal_rainfall_15T_df = areal_rainfall_ts_df_loaded['areal_avg_rainfall_mm_15min'].resample('15T').sum().fillna(0).reset_index()
        areal_rainfall_15T_df.rename(columns={'areal_avg_rainfall_mm_15min': 'rainfall_mm_15min'}, inplace=True)

    if 'daily_rainfall_df' not in locals():
        daily_rainfall_df = pd.read_csv(os.path.join(OUTPUT_DATA_DIRECTORY, DAILY_RAINFALL_FILENAME), parse_dates=['timestamp'])
    
    if 'rain_events_df' not in locals() or rain_events_df.empty: # check for empty too
        rain_events_df = pd.read_csv(os.path.join(OUTPUT_DATA_DIRECTORY, RAIN_EVENTS_FILENAME), parse_dates=['start_time', 'end_time'])
        rain_events_df['duration'] = pd.to_timedelta(rain_events_df['duration'])


    if 'pot_events_df' not in locals() or pot_events_df.empty: # check for empty too
        pot_events_df = pd.read_csv(os.path.join(OUTPUT_DATA_DIRECTORY, POT_EVENTS_FILENAME), parse_dates=['start_time', 'end_time'])
        pot_events_df['duration_exceedance_phase'] = pd.to_timedelta(pot_events_df['duration_exceedance_phase'])

    # Re-generate top N lists if needed
    min_rain_for_rainy_day = 0.01
    rainy_days_df = daily_rainfall_df[daily_rainfall_df['total_daily_rainfall_mm'] > min_rain_for_rainy_day].copy()
    most_rainy_days = rainy_days_df.sort_values(by='total_daily_rainfall_mm', ascending=False).head(10)

    if not rain_events_df.empty:
        most_intense_events = rain_events_df.sort_values(by='total_rainfall_mm', ascending=False).head(10)
    else:
        most_intense_events = pd.DataFrame() # Empty if no rain_events_df

    if not pot_events_df.empty:
        most_significant_pot_events = pot_events_df.sort_values(by='magnitude_over_threshold_mm', ascending=False).head(10)
    else:
        most_significant_pot_events = pd.DataFrame() # Empty if no pot_events_df
        
except FileNotFoundError:
    print("Error: One or more pre-computed data files not found. Please run the previous notebook sections first.")
    # Potentially raise an error or exit if these files are critical for this section
    raise

# Constants from previous analysis (ensure they are defined for context if needed)
RAIN_THRESHOLD_FOR_EVENT = 0.01
MIN_DRY_SPELL_HOURS = 1
if not areal_rainfall_15T_df.empty and not areal_rainfall_15T_df[areal_rainfall_15T_df['rainfall_mm_15min'] > RAIN_THRESHOLD_FOR_EVENT].empty:
    POT_INTENSITY_THRESHOLD = areal_rainfall_15T_df[areal_rainfall_15T_df['rainfall_mm_15min'] > RAIN_THRESHOLD_FOR_EVENT]['rainfall_mm_15min'].quantile(0.95)
else: # Fallback
    POT_INTENSITY_THRESHOLD = 1.0 
    print(f"Warning: Could not calculate POT_INTENSITY_THRESHOLD dynamically, using fallback: {POT_INTENSITY_THRESHOLD} mm/15min")

# %% [markdown]
# ## 11. Comprehensive Evaluation of Rainfall Event Identification Methods
# 
# This section provides an in-depth evaluation of the three methodologies used for identifying significant rainfall periods: Daily Rainfall Aggregation, Continuous Rainfall Period Identification (Rain Events), and Peak Over Threshold (POT) Event Analysis. We will examine the characteristics of events captured by each method and discuss their inherent strengths and limitations based on the generated results.
# 
# ### 11.1. Recap of Identified Events
# 
# Before diving into individual evaluations, let's summarize the number and overall characteristics of events identified by each method.

# %%
print("--- Summary of Identified Events ---")

print(f"\n1. Daily Rainfall Aggregation:")
print(f"   Total days in dataset: {len(daily_rainfall_df)}")
print(f"   Number of rainy days (> {min_rain_for_rainy_day} mm): {len(rainy_days_df)}")
if not daily_rainfall_df.empty:
    print(f"   Percentage of rainy days: {(len(rainy_days_df) / len(daily_rainfall_df) * 100):.2f}%")
    print(f"   Mean daily rainfall on rainy days: {rainy_days_df['total_daily_rainfall_mm'].mean():.2f} mm")
    print(f"   Max daily rainfall recorded: {daily_rainfall_df['total_daily_rainfall_mm'].max():.2f} mm")
display(most_rainy_days.head(3))

print(f"\n2. Continuous Rainfall Period Identification (Rain Events):")
if not rain_events_df.empty:
    print(f"   Total continuous rain events identified: {len(rain_events_df)}")
    print(f"   Mean event duration: {rain_events_df['duration'].mean()}")
    print(f"   Mean total rainfall per event: {rain_events_df['total_rainfall_mm'].mean():.2f} mm")
    print(f"   Mean peak 15-min intensity per event: {rain_events_df['peak_15min_intensity_mm'].mean():.2f} mm/15min")
    print(f"   Max total rainfall in an event: {rain_events_df['total_rainfall_mm'].max():.2f} mm")
    display(most_intense_events[['start_time', 'duration', 'total_rainfall_mm', 'peak_15min_intensity_mm']].head(3))
else:
    print("   No continuous rain events were identified or loaded.")


print(f"\n3. Peak Over Threshold (POT) Event Analysis:")
if not pot_events_df.empty:
    print(f"   POT Intensity Threshold used: {POT_INTENSITY_THRESHOLD:.2f} mm/15min")
    print(f"   Total POT events identified: {len(pot_events_df)}")
    print(f"   Mean duration of exceedance phase: {pot_events_df['duration_exceedance_phase'].mean()}")
    print(f"   Mean total rainfall during exceedance phase: {pot_events_df['total_rainfall_during_exceedance_phase'].mean():.2f} mm")
    print(f"   Mean magnitude over threshold: {pot_events_df['magnitude_over_threshold_mm'].mean():.2f} mm")
    print(f"   Max peak 15-min intensity during POT event: {pot_events_df['peak_15min_intensity_during_exceedance_phase'].max():.2f} mm/15min")
    display(most_significant_pot_events[['start_time', 'duration_exceedance_phase', 'total_rainfall_during_exceedance_phase', 'magnitude_over_threshold_mm', 'peak_15min_intensity_during_exceedance_phase']].head(3))
else:
    print("   No POT events were identified or loaded.")

# %% [markdown]
# ### 11.2. Evaluation of Daily Rainfall Aggregation
# 
# This method provides a straightforward, calendar-based view of rainfall.
# 
# **Characteristics of Top Daily Events:**
# The `most_rainy_days` DataFrame (displayed above and in previous plots) highlights days with exceptionally high cumulative rainfall. For example, the wettest day, `[Date of most_rainy_days.iloc[0]['timestamp']]`, recorded `[Value of most_rainy_days.iloc[0]['total_daily_rainfall_mm']]` mm. Such days are critical for water balance studies and often correlate with widespread impacts.
# 
# **Distribution of Daily Rainfall:**

# %%
plt.figure(figsize=(12, 6))
sns.histplot(data=rainy_days_df, x='total_daily_rainfall_mm', bins=50, kde=True, color=sns.color_palette("viridis")[0])
plt.title('Distribution of Total Daily Rainfall on Rainy Days', fontsize=16)
plt.xlabel('Total Daily Rainfall (mm)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.yscale('log') # Use log scale for better visibility of tail
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()

print(rainy_days_df['total_daily_rainfall_mm'].describe(percentiles=[.5, .75, .90, .95, .99]))

# %% [markdown]
# **Evaluation:**
# *   **Strengths:**
#     *   **Simplicity and Intuitiveness:** Easy to compute and understand. Aligns with common meteorological reporting.
#     *   **Climatological Standard:** Useful for long-term climate analysis, tracking annual/seasonal rainfall, and identifying general wet/dry periods.
#     *   **Broad Impact Indication:** High daily totals often signify days with notable weather conditions, though not necessarily the specific nature of the rainfall (e.g., intensity).
# *   **Weaknesses:**
#     *   **Loss of Temporal Detail:** Aggregating to a daily scale masks crucial intra-day variability. A day with 50mm could be from a short, intense 1-hour storm or 24 hours of light, continuous rain. This has vastly different hydrological consequences.
#     *   **Arbitrary Cutoff:** The midnight cutoff can split a single meteorological rain event into two separate days, potentially underrepresenting the true magnitude of the event.
#     *   **Limited for Process Understanding:** Less effective for detailed hydrological modeling, flash flood prediction, or understanding storm dynamics, which require sub-daily data.
# 
# The distribution plot typically shows a right-skewed distribution, with many days of light rain and a few days of very heavy rain, which is characteristic of many climates.
# 
# ### 11.3. Evaluation of Continuous Rainfall Period Identification (Rain Events)
# 
# This method groups consecutive rainy intervals into distinct events, offering a more hydrologically relevant perspective.
# 
# **Characteristics of Top Continuous Events:**
# The `most_intense_events` DataFrame showcases events with the largest total accumulated rainfall. These events are characterized by their `start_time`, `end_time`, `duration`, `total_rainfall_mm`, and `peak_15min_intensity_mm`. For instance, the event ID `[most_intense_events.iloc[0]['event_id']]` delivered `[most_intense_events.iloc[0]['total_rainfall_mm']]` mm over `[most_intense_events.iloc[0]['duration']]`.
# 
# **Distributions of Rain Event Properties:**

# %%
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

if not rain_events_df.empty:
    # Sample a subset if data is too large
    MAX_POINTS = 100_000
    if len(rain_events_df) > MAX_POINTS:
        rain_events_sample = rain_events_df.sample(n=MAX_POINTS, random_state=42)
    else:
        rain_events_sample = rain_events_df

    # Convert duration to hours early (more efficient than per-tick conversion)
    duration_hours = rain_events_sample['duration'].dt.total_seconds() / 3600

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Duration plot
    sns.histplot(duration_hours, ax=axes[0], bins=30, color=sns.color_palette("viridis")[1])
    axes[0].set_title('Distribution of Event Durations')
    axes[0].set_xlabel('Duration (Hours)')
    axes[0].tick_params(axis='x', rotation=30)

    # Total rainfall
    sns.histplot(rain_events_sample['total_rainfall_mm'], ax=axes[1], bins=30, color=sns.color_palette("viridis")[2])
    axes[1].set_title('Distribution of Event Total Rainfall')
    axes[1].set_xlabel('Total Rainfall (mm)')
    axes[1].set_yscale('log')

    # Peak 15-min intensity
    sns.histplot(rain_events_sample['peak_15min_intensity_mm'], ax=axes[2], bins=30, color=sns.color_palette("viridis")[3])
    axes[2].set_title('Distribution of Event Peak 15-min Intensity')
    axes[2].set_xlabel('Peak Intensity (mm/15min)')
    axes[2].set_yscale('log')

    plt.tight_layout()
    plt.show()

    print("\nDescriptive Statistics for Continuous Rain Event Properties:")
    display(rain_events_sample[['duration', 'total_rainfall_mm', 'peak_15min_intensity_mm', 'avg_intensity_mm_hr']].describe(percentiles=[.5, .75, .90, .95, .99]))
else:
    print("Rain events data is empty, skipping distribution plots.")


# %% [markdown]
# **Evaluation:**
# *   **Strengths:**
#     *   **Hydrologically Relevant:** Defines events based on continuous precipitation, better reflecting individual storm systems or rain periods.
#     *   **Captures Key Event Metrics:** Provides duration, total volume, and intensities (peak and average), which are crucial for impact assessment (e.g., runoff volume, flood potential).
#     *   **Parameter Control:** Allows tuning of `rain_threshold` and `min_dry_spell_duration` to define events according to specific regional characteristics or study objectives.
# *   **Weaknesses:**
#     *   **Parameter Sensitivity:** The number and characteristics of identified events can be sensitive to the chosen parameters. A different `min_dry_spell_duration` can merge or split events significantly.
#     *   **Complexity:** The algorithm for identifying and merging rain blocks is more complex than simple daily aggregation.
#     *   **May Obscure Short Bursts:** While peak intensity within the event is captured, the overall event definition might group periods of varying intensity. A very long event with moderate rain might overshadow short, extreme bursts if not examined carefully using POT.
# 
# The distributions often show that most events are short and produce little rain, while a few are long-duration and/or high-volume, contributing significantly to the total rainfall.
# 
# ### 11.4. Evaluation of Peak Over Threshold (POT) Event Analysis
# 
# This method specifically targets periods of high-intensity rainfall, which are often associated with acute impacts like flash floods.
# 
# **Characteristics of Top POT Events:**
# The `most_significant_pot_events` DataFrame highlights periods where rainfall intensity significantly exceeded the defined threshold (`[POT_INTENSITY_THRESHOLD]` mm/15min). Key metrics include the `duration_exceedance_phase`, `total_rainfall_during_exceedance_phase`, `peak_15min_intensity_during_exceedance_phase`, and `magnitude_over_threshold_mm`. The POT event with ID `[most_significant_pot_events.iloc[0]['pot_event_id']]` had a peak intensity of `[most_significant_pot_events.iloc[0]['peak_15min_intensity_during_exceedance_phase']]` mm/15min.
# 
# **Distributions of POT Event Properties:**

# %%
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

if not pot_events_df.empty:
    # Downsample if needed
    MAX_POINTS = 100_000
    if len(pot_events_df) > MAX_POINTS:
        pot_sample = pot_events_df.sample(n=MAX_POINTS, random_state=42)
    else:
        pot_sample = pot_events_df

    # Convert duration to hours in advance
    duration_hours = pot_sample['duration_exceedance_phase'].dt.total_seconds() / 3600

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Duration plot
    sns.histplot(duration_hours, ax=axes[0], bins=20, color=sns.color_palette("viridis")[4])
    axes[0].set_title('Distribution of POT Event Durations (Exceedance Phase)')
    axes[0].set_xlabel('Duration (Hours)')
    axes[0].tick_params(axis='x', rotation=30)

    # Magnitude over threshold
    sns.histplot(pot_sample['magnitude_over_threshold_mm'], ax=axes[1], bins=20, color=sns.color_palette("viridis")[5])
    axes[1].set_title('Distribution of POT Event Magnitude Over Threshold')
    axes[1].set_xlabel('Magnitude Over Threshold (mm)')
    axes[1].set_yscale('log')

    # Peak 15-min intensity
    sns.histplot(pot_sample['peak_15min_intensity_during_exceedance_phase'], ax=axes[2], bins=20, color=sns.color_palette("viridis_r")[2])
    axes[2].set_title('Distribution of POT Event Peak 15-min Intensity')
    axes[2].set_xlabel('Peak Intensity (mm/15min)')
    axes[2].set_yscale('log')

    plt.tight_layout()
    plt.show()

    print("\nDescriptive Statistics for POT Event Properties:")
    display(pot_sample[['duration_exceedance_phase', 'total_rainfall_during_exceedance_phase', 
                        'peak_15min_intensity_during_exceedance_phase', 'magnitude_over_threshold_mm']].describe(percentiles=[.5, .75, .90, .95, .99]))
else:
    print("POT events data is empty, skipping distribution plots.")


# %% [markdown]
# **Evaluation:**
# *   **Strengths:**
#     *   **Focus on Extremes:** Directly identifies periods of high rainfall rates critical for flash flood warnings, erosion studies, and infrastructure design for peak loads.
#     *   **Statistically Grounded:** The POT approach is rooted in Extreme Value Theory, providing a robust framework for analyzing exceedances.
#     *   **Detailed Intensity Information:** Provides clear metrics on the severity of high-intensity periods (e.g., magnitude over threshold, duration of exceedance).
# *   **Weaknesses:**
#     *   **Threshold Dependency:** The selection of `pot_threshold` is crucial and can significantly alter results. A threshold too high might miss relevant events; too low might include too many minor ones. The choice often involves statistical considerations (e.g., percentiles) or domain knowledge.
#     *   **Ignores Lower Intensity Rain:** By definition, it doesn't characterize prolonged, moderate rainfall events unless they breach the threshold, even if their cumulative volume is large.
#     *   **Event Definition Nuances:** Parameters like `min_exceedance_intervals` and `max_time_between_exceedances_for_clustering` influence how exceedances are grouped into distinct POT events.
# 
# The distributions for POT events usually show fewer events overall compared to continuous rain events, but these are characterized by higher intensities.
# 
# ## 12. Comparative Analysis of Rainfall Event Identification Methods
# 
# This section compares the three event identification methods to understand their relationships, overlaps, and unique contributions to characterizing Rio de Janeiro's rainfall.
# 
# ### 12.1. Overlap Analysis: Top Daily Events vs. Continuous Rain Events
# 
# We investigate how the top N daily rainfall amounts relate to the continuous rain events defined.

# %%
if not most_rainy_days.empty and not rain_events_df.empty:
    print(f"\n--- Overlap: Top {len(most_rainy_days)} Daily Rain Events vs. Continuous Rain Events ---")
    
    # Ensure rain_events_df times are timezone-naive if daily_rainfall_df is, or vice-versa, for comparison
    # Assuming both are already timezone-naive from preprocessing
    
    comparison_data = []
    for idx, daily_event in most_rainy_days.iterrows():
        day_start = daily_event['timestamp'] # This is already a date (start of day)
        day_end = day_start + pd.Timedelta(days=1) - pd.Timedelta(seconds=1) # End of the day
        
        # Find continuous rain events that overlap with this day
        overlapping_continuous_events = rain_events_df[
            (rain_events_df['start_time'] <= day_end) & 
            (rain_events_df['end_time'] >= day_start)
        ].copy() # Use .copy() to avoid SettingWithCopyWarning

        num_cont_events = len(overlapping_continuous_events)
        total_rain_from_cont_events_on_day = 0
        
        if num_cont_events > 0:
            # Calculate rainfall from continuous events specifically within the daily event's timeframe
            for _, cont_event in overlapping_continuous_events.iterrows():
                # Determine the intersection of the continuous event and the day
                overlap_start = max(day_start, cont_event['start_time'])
                overlap_end = min(day_end, cont_event['end_time']) # cont_event['end_time'] is exclusive for sum
                
                if overlap_start < overlap_end:
                    # Sum rainfall from areal_rainfall_15T_df for this specific overlap period
                    rain_in_overlap = areal_rainfall_15T_df[
                        (areal_rainfall_15T_df['timestamp'] >= overlap_start) &
                        (areal_rainfall_15T_df['timestamp'] < overlap_end) # Use < as end_time is exclusive
                    ]['rainfall_mm_15min'].sum()
                    total_rain_from_cont_events_on_day += rain_in_overlap
            
            largest_cont_event_rain = overlapping_continuous_events['total_rainfall_mm'].max()
            largest_cont_event_id = overlapping_continuous_events.loc[overlapping_continuous_events['total_rainfall_mm'].idxmax()]['event_id']
        else:
            largest_cont_event_rain = 0
            largest_cont_event_id = None
            
        comparison_data.append({
            'Rainy Day Date': day_start.strftime('%Y-%m-%d'),
            'Daily Total (mm)': daily_event['total_daily_rainfall_mm'],
            'Num Overlapping Cont. Events': num_cont_events,
            'Total Rain from Cont. Events on Day (mm)': total_rain_from_cont_events_on_day,
            'Largest Cont. Event ID on Day': largest_cont_event_id,
            'Largest Cont. Event Total Rain (mm)': largest_cont_event_rain
        })

    daily_vs_continuous_df = pd.DataFrame(comparison_data)
    display(daily_vs_continuous_df)

    # Discussion:
    # - Often, a top rainy day is dominated by one or two major continuous rain events.
    # - The 'Total Rain from Cont. Events on Day (mm)' should be very close to 'Daily Total (mm)' if event definitions are consistent.
    # - Discrepancies might arise from how thresholds or dry spell durations are handled, or if parts of continuous events fall outside the specific day.
else:
    print("Skipping Daily vs Continuous comparison due to empty dataframes.")

# %% [markdown]
# ### 12.2. Overlap Analysis: Continuous Rain Events vs. POT Events
# 
# Here, we examine if the most intense continuous rain events also trigger POT conditions.

# %%
if not most_intense_events.empty and not pot_events_df.empty:
    print(f"\n--- Overlap: Top {len(most_intense_events)} Continuous Rain Events vs. POT Events ---")
    
    comparison_data_cont_pot = []
    for idx, cont_event in most_intense_events.iterrows():
        event_start = cont_event['start_time']
        event_end = cont_event['end_time']
        
        overlapping_pot_events = pot_events_df[
            (pot_events_df['start_time'] <= event_end) & 
            (pot_events_df['end_time'] >= event_start)
        ]
        
        num_pot_events = len(overlapping_pot_events)
        total_pot_magnitude = 0
        max_pot_peak_intensity = 0
        
        if num_pot_events > 0:
            total_pot_magnitude = overlapping_pot_events['magnitude_over_threshold_mm'].sum()
            max_pot_peak_intensity = overlapping_pot_events['peak_15min_intensity_during_exceedance_phase'].max()
            
        comparison_data_cont_pot.append({
            'Cont. Event ID': cont_event['event_id'],
            'Cont. Event Start': cont_event['start_time'].strftime('%Y-%m-%d %H:%M'),
            'Cont. Event Total (mm)': cont_event['total_rainfall_mm'],
            'Cont. Event Peak (mm/15m)': cont_event['peak_15min_intensity_mm'],
            'Num Overlapping POT Events': num_pot_events,
            'Total POT Magnitude in Cont. Event (mm)': total_pot_magnitude,
            'Max POT Peak Intensity in Cont. Event (mm/15m)': max_pot_peak_intensity
        })
        
    continuous_vs_pot_df = pd.DataFrame(comparison_data_cont_pot)
    display(continuous_vs_pot_df)

    # Plotting an example: Top continuous event with its POT events
    if not continuous_vs_pot_df.empty and continuous_vs_pot_df.iloc[0]['Num Overlapping POT Events'] > 0:
        top_cont_event_detail = most_intense_events.iloc[0]
        
        fig, ax = plt.subplots(figsize=(15, 7))
        
        # Plot 15-min rainfall for the duration of the top continuous event
        event_rain_data = areal_rainfall_15T_df[
            (areal_rainfall_15T_df['timestamp'] >= top_cont_event_detail['start_time']) &
            (areal_rainfall_15T_df['timestamp'] < top_cont_event_detail['end_time'])
        ]
        ax.bar(event_rain_data['timestamp'], event_rain_data['rainfall_mm_15min'], 
               width=0.01, color='lightblue', label='15-min Rainfall')
        
        # Highlight POT threshold
        ax.axhline(POT_INTENSITY_THRESHOLD, color='red', linestyle='--', label=f'POT Threshold ({POT_INTENSITY_THRESHOLD:.2f} mm/15min)')
        
        # Highlight POT event periods within this continuous event
        overlapping_pots_for_plot = pot_events_df[
            (pot_events_df['start_time'] <= top_cont_event_detail['end_time']) & 
            (pot_events_df['end_time'] >= top_cont_event_detail['start_time'])
        ]
        for _, pot_event_row in overlapping_pots_for_plot.iterrows():
            ax.axvspan(pot_event_row['start_time'], pot_event_row['end_time'], 
                       color=sns.color_palette("autumn")[2], alpha=0.4, 
                       label=f"POT Event {pot_event_row['pot_event_id']}" if _ == overlapping_pots_for_plot.index[0] else None)

        ax.set_title(f"Top Continuous Rain Event (ID {top_cont_event_detail['event_id']}) with Overlapping POT Events", fontsize=16)
        ax.set_xlabel('Timestamp', fontsize=12)
        ax.set_ylabel('Rainfall (mm/15min)', fontsize=12)
        ax.legend()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    # Discussion:
    # - High-total-rainfall continuous events often, but not always, contain periods exceeding the POT threshold.
    # - A long, moderate continuous event might have a high total but no POT segments.
    # - A shorter, very intense continuous event is likely to be dominated by POT segments.
else:
    print("Skipping Continuous vs POT comparison due to empty dataframes.")

# %% [markdown]
# ### 12.3. Overlap Analysis: Top Daily Events vs. POT Events
# 
# Finally, we check if the days with the highest total rainfall also experienced POT-level intensities.

# %%
if not most_rainy_days.empty and not pot_events_df.empty:
    print(f"\n--- Overlap: Top {len(most_rainy_days)} Daily Rain Events vs. POT Events ---")
    
    comparison_data_daily_pot = []
    for idx, daily_event in most_rainy_days.iterrows():
        day_start = daily_event['timestamp']
        day_end = day_start + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
        
        overlapping_pot_events_daily = pot_events_df[
            (pot_events_df['start_time'] <= day_end) & 
            (pot_events_df['end_time'] >= day_start)
        ]
        
        num_pot_events_on_day = len(overlapping_pot_events_daily)
        total_pot_magnitude_on_day = 0
        max_pot_peak_on_day = 0
        
        if num_pot_events_on_day > 0:
            total_pot_magnitude_on_day = overlapping_pot_events_daily['magnitude_over_threshold_mm'].sum()
            max_pot_peak_on_day = overlapping_pot_events_daily['peak_15min_intensity_during_exceedance_phase'].max()

        comparison_data_daily_pot.append({
            'Rainy Day Date': day_start.strftime('%Y-%m-%d'),
            'Daily Total (mm)': daily_event['total_daily_rainfall_mm'],
            'Num POT Events on Day': num_pot_events_on_day,
            'Total POT Magnitude on Day (mm)': total_pot_magnitude_on_day,
            'Max POT Peak on Day (mm/15m)': max_pot_peak_on_day
        })
        
    daily_vs_pot_df = pd.DataFrame(comparison_data_daily_pot)
    display(daily_vs_pot_df)

    # Discussion:
    # - Top rainy days are highly likely to contain POT events, as high daily totals often result from at least some periods of intense rain.
    # - However, it's possible for a day to accumulate a high total from prolonged, moderate rain that never breaches the POT intensity threshold.
else:
    print("Skipping Daily vs POT comparison due to empty dataframes.")

# %% [markdown]
# ### 12.4. Temporal Coincidence of Top Events
# 
# A timeline plot can visualize if the "top" events identified by each method tend to occur at similar times.

# %%
if not most_rainy_days.empty and not most_intense_events.empty and not most_significant_pot_events.empty:
    plt.figure(figsize=(18, 8))

    # Prepare data for eventplot
    # For daily events, plot a single point at the date.
    daily_event_dates = [mdates.date2num(d.to_pydatetime()) for d in most_rainy_days['timestamp']]
    
    # For continuous and POT events, plot their duration ranges.
    # Convert to (start_num, duration_num) for eventplot or use a different plotting approach if ranges are preferred.
    # Here, we'll plot them as lines for simplicity with y-offsets.

    y_positions = [1, 2, 3] 
    event_types = ['Top Daily Events', 'Top Continuous Rain Events', 'Top POT Events']
    colors = [sns.color_palette("Set1")[0], sns.color_palette("Set1")[1], sns.color_palette("Set1")[2]]

    # Plot Top Daily Events (as points or very short lines)
    for date_val in most_rainy_days['timestamp']:
        plt.plot([date_val, date_val + pd.Timedelta(hours=1)], [y_positions[0], y_positions[0]], 
                 color=colors[0], linewidth=3, alpha=0.7)
    # Dummy plot for legend
    plt.plot([],[], color=colors[0], linewidth=3, label=event_types[0])


    # Plot Top Continuous Rain Events
    for idx, row in most_intense_events.iterrows():
        plt.plot([row['start_time'], row['end_time']], [y_positions[1], y_positions[1]], 
                 color=colors[1], linewidth=3, alpha=0.7)
    plt.plot([],[], color=colors[1], linewidth=3, label=event_types[1])


    # Plot Top POT Events
    for idx, row in most_significant_pot_events.iterrows():
        plt.plot([row['start_time'], row['end_time']], [y_positions[2], y_positions[2]], 
                 color=colors[2], linewidth=3, alpha=0.7)
    plt.plot([],[], color=colors[2], linewidth=3, label=event_types[2])


    plt.yticks(y_positions, event_types)
    plt.title('Temporal Coincidence of Top Ranked Events from Different Methods', fontsize=16)
    plt.xlabel('Time', fontsize=12)
    plt.ylim(0.5, 3.5)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    plt.legend(loc='upper right')
    plt.grid(True, axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()
else:
    print("Skipping temporal coincidence plot due to empty dataframes for one or more event types.")

# %% [markdown]
# **Interpretation of Temporal Coincidence Plot:**
# This plot helps visualize whether the "most significant" periods identified by different criteria tend to align.
# - Strong alignment suggests that extreme daily totals, large continuous events, and high-intensity POT events often co-occur, pointing to particularly impactful meteorological situations.
# - Divergence might indicate different types of impactful rain: e.g., a top POT event might be very short and not make it into top daily totals if the rest of the day was dry. A top continuous event might be very long with moderate rain, accumulating a high total but not triggering POT conditions.
# 
# ### 12.5. Discussion on Method Selection for Different Applications
# 
# The choice of method critically depends on the analytical goal:
# 
# *   **Daily Rainfall Aggregation:**
#     *   **Suitable for:** General climatological summaries, long-term trend analysis of wet/dry days, agricultural impact assessments where daily water input is key, simple public communication.
#     *   **Example Application:** "How many rainy days were there last year?" "Which were the 10 wettest days in the last decade?"
# 
# *   **Continuous Rainfall Period Identification (Rain Events):**
#     *   **Suitable for:** Hydrological modeling (e.g., runoff estimation, reservoir inflow), flood forecasting based on event volume and duration, detailed storm system analysis, understanding typical rainfall event structures (duration-intensity-frequency).
#     *   **Example Application:** "What was the duration and total rainfall of the storm system that caused flooding on [date]?" "Characterize typical storm events for this region."
# 
# *   **Peak Over Threshold (POT) Event Analysis:**
#     *   **Suitable for:** Flash flood risk assessment, urban drainage design, soil erosion studies, analysis of extreme short-duration rainfall intensities, issuing warnings for immediate high-impact weather.
#     *   **Example Application:** "Identify all periods in the last 5 years where rainfall intensity exceeded critical thresholds for urban drainage capacity." "What is the typical peak intensity during extreme rainfall bursts?"
# 
# **Synergies and Complementarity:**
# Often, a combination of methods provides the most comprehensive understanding.
# - A top daily total might be investigated using continuous event analysis to see if it was one long event or multiple shorter ones.
# - A major continuous event can be analyzed for POT segments to understand if it contained periods of particularly hazardous intensity.
# - POT events can be contextualized by looking at the total rainfall of the continuous event they belong to, or the daily total on which they occurred.
# 
# The analyses show that while there is significant overlap (e.g., very wet days often contain large continuous events with POT segments), each method also highlights unique aspects of the rainfall regime.
# 
# ## 13. Enhanced Conclusions and Future Directions
# 
# This comprehensive evaluation and comparison of three rainfall event identification methods has provided deeper insights into the rainfall characteristics of the studied area in Rio de Janeiro.
# 
# **Key Findings from Comparative Analysis:**
# 
# 1.  **Interrelation of Extreme Events:** The top daily rainfall events are generally well-explained by one or more significant continuous rain events occurring on those days. The total rainfall calculated by summing parts of continuous events within a day closely matches the daily aggregated total, confirming consistency.
# 2.  **Intensity within Volume:** Many (but not all) of the continuous rain events with the highest total rainfall also featured periods of intensity exceeding the POT threshold. This indicates that high volume events often include, or are driven by, intense rainfall bursts. However, some long-duration, moderate-intensity continuous events can accumulate large totals without triggering POT conditions. Conversely, some very high-intensity POT events can be relatively short and may not always rank among the top continuous events by total volume.
# 3.  **Daily Extremes and POT:** Days with the highest total rainfall almost invariably include POT events, highlighting that extreme daily accumulations are typically driven by periods of very high rainfall rates.
# 4.  **Methodological Complementarity:** No single method captures all aspects of "significant rain." Daily aggregation offers a broad overview, continuous event analysis details individual storm structures, and POT analysis pinpoints the most intense, potentially hazardous, periods. Their combined use offers a richer understanding.
# 
# **Refined Conclusions on Rainfall in Rio de Janeiro (based on this analysis):**
# 
# *   The rainfall regime in the analyzed portion of Rio de Janeiro is characterized by a mix of frequent, lower-volume/intensity events and less frequent, but highly significant, high-volume and/or high-intensity events.
# *   The most impactful rainfall periods, whether defined by daily totals, event volumes, or peak intensities, often see these metrics align, indicating complex and severe storm systems.
# *   The POT analysis, with a threshold derived from the 95th percentile of rainy intervals, successfully isolated periods of exceptionally high rainfall rates that are critical for understanding acute hazards like flash floods.
# 
# **Future Directions and Potential Enhancements:**
# 
# 1.  **Parameter Sensitivity Analysis:** Systematically vary parameters like `min_dry_spell_duration` for continuous events and `pot_threshold` or `min_exceedance_intervals` for POT events to understand their impact on event statistics and select optimal values based on specific criteria or validation data.
# 2.  **Correlation with Impacts:** Spatially and temporally correlate the identified significant rain events (from all three methods) with actual impact data from `ocorrencias_gdf` (e.g., flooding reports, landslides). This would help validate which event definitions best predict adverse outcomes.
# 3.  **Spatial Variability:** Extend this event analysis framework to individual rain gauge stations (before areal averaging) to understand the spatial variability of event characteristics across Rio de Janeiro.
# 4.  **Seasonality and Trend Analysis:** Analyze the seasonality of different event types (daily, continuous, POT) and investigate long-term trends in their frequency, intensity, or duration using the full historical dataset.
# 5.  **Multivariate Event Definition:** Explore more advanced event definitions that consider multiple attributes simultaneously (e.g., events with both high total rainfall AND high peak intensity).
# 6.  **Application of Other Academic Methods:**
#     *   **Intensity-Duration-Frequency (IDF) Curves:** While not an event identification method per se, IDF curves are a standard outcome of analyzing extreme rainfall data (often derived from POT or annual maxima series) and are fundamental for engineering design.
#     *   **Storm Typing/Classification:** Develop methods to classify the identified continuous rain events based on their temporal rainfall patterns (e.g., using hierarchical clustering on normalized event profiles) to identify typical storm "shapes" (e.g., front-loaded, back-loaded, uniform).
#     *   **Independent Storms (Inter-Event Time Definition - IETD):** Further refine the `min_dry_spell_duration` using statistical methods to define IETD, ensuring identified rain events are truly independent. Common approaches involve analyzing the autocorrelation of rainfall time series or the distribution of dry spell durations.
# 
# This detailed analysis framework provides a solid foundation for more advanced hydro-meteorological studies in Rio de Janeiro. The generated event datasets are valuable resources for risk assessment, climate studies, and operational forecasting improvements.

# %%
# Final check to ensure all outputs are saved (already done at the end of section 10, but good to confirm)
print("\n--- Output File Check ---")
files_to_check = [
    os.path.join(OUTPUT_DATA_DIRECTORY, DAILY_RAINFALL_FILENAME),
    os.path.join(OUTPUT_DATA_DIRECTORY, RAIN_EVENTS_FILENAME),
    os.path.join(OUTPUT_DATA_DIRECTORY, POT_EVENTS_FILENAME)
]
for f_path in files_to_check:
    if os.path.exists(f_path):
        print(f"File found: {f_path}")
    else:
        print(f"File NOT found: {f_path} - Ensure previous sections were run and saved correctly.")

print("\nEnd of comprehensive evaluation and comparison.")

# %% [markdown]
# ---

# %% [markdown]
# # Grid of Hourly Maps for Top Events 

# %%
# Ensure the CRS_PROJECTED is defined (it should be from the previous notebook parts)
if 'CRS_PROJECTED' not in locals():
    CRS_PROJECTED = "EPSG:31983" # Fallback, but should be inherited

# Ensure ocorrencias_gdf is available and projected
if 'ocorrencias_gdf' not in locals():
    # This is a simplified version of ocorrencias_gdf loading for this specific task.
    # In a full notebook, it would be loaded and preprocessed earlier.
    print("Warning: 'ocorrencias_gdf' not found in local scope. Attempting to load and process.")
    try:
        ocorrencias_csv_path = '../../../../data/meteorologia/clean/adm_cor_comando/ocorrencias.csv' # Adjust as per your structure
        ocorrencias = pd.read_csv(ocorrencias_csv_path)
        ocorrencias['data_inicio'] = pd.to_datetime(ocorrencias['data_inicio'], errors='coerce')
        ocorrencias['data_fim'] = pd.to_datetime(ocorrencias['data_fim'], errors='coerce')
        ocorrencias = ocorrencias.dropna(subset=['latitude', 'longitude', 'data_inicio', 'data_fim'])
        ocorrencias_gdf = gpd.GeoDataFrame(
            ocorrencias,
            geometry=gpd.points_from_xy(ocorrencias.longitude, ocorrencias.latitude),
            crs="EPSG:4326" # Assuming original is geographic
        )
    except FileNotFoundError:
        print(f"Error: Ocorrencias CSV file not found at {ocorrencias_csv_path}. Flood occurrences cannot be plotted.")
        ocorrencias_gdf = gpd.GeoDataFrame() # Empty GeoDataFrame
else:
    # Ensure 'data_inicio' and 'data_fim' are datetime objects if loaded from CSV earlier
    if not pd.api.types.is_datetime64_any_dtype(ocorrencias_gdf['data_inicio']):
        ocorrencias_gdf['data_inicio'] = pd.to_datetime(ocorrencias_gdf['data_inicio'], errors='coerce')
    if not pd.api.types.is_datetime64_any_dtype(ocorrencias_gdf['data_fim']):
        ocorrencias_gdf['data_fim'] = pd.to_datetime(ocorrencias_gdf['data_fim'], errors='coerce')
    ocorrencias_gdf = ocorrencias_gdf.dropna(subset=['data_inicio', 'data_fim', 'geometry'])


# Project ocorrencias_gdf if it's not already and not empty
if not ocorrencias_gdf.empty and ocorrencias_gdf.crs != CRS_PROJECTED:
    print(f"Reprojecting 'ocorrencias_gdf' from {ocorrencias_gdf.crs} to {CRS_PROJECTED}")
    ocorrencias_gdf = ocorrencias_gdf.to_crs(CRS_PROJECTED)

# The 'alertario' dataframe with 15-min rainfall data per station should be available.
# If not, it needs to be loaded. Assuming it's in scope from previous cells.
# Example: alertario = pd.read_csv(f'{input_data_directory}/clima_pluviometro/taxa_precipitacao_alertario_manual.csv')
# And 'timestamp' column is datetime
if 'alertario' in locals() and not pd.api.types.is_datetime64_any_dtype(alertario['timestamp']):
    alertario['timestamp'] = pd.to_datetime(alertario['timestamp'])

# %% [markdown]
# ## 14. Focused Visualization of Top Rain Events with Hourly Maps
# 
# This section focuses on visualizing the spatio-temporal evolution of rainfall and associated flood occurrences for the top 10 most significant rain events.
# 
# ### 14.1. Selection of the "Best" Method for Defining Top Rain Events
# 
# Among the three methods analyzed (Daily Aggregation, Continuous Rain Periods, Peak Over Threshold), the **Continuous Rainfall Period Identification** method (resulting in `rain_events_df`) is deemed the most suitable for selecting comprehensive rain events for this visualization task. This is because:
# 
# 1.  **Hydrological Coherence:** It defines events based on continuous rainfall activity, allowing for realistic dry spell interruptions, thereby better capturing individual storm systems or prolonged rain periods.
# 2.  **Complete Event Profile:** It provides a full profile of each event, including start time, end time, total duration, accumulated volume, and peak intensity, which are essential for understanding an event's overall impact.
# 3.  **Contextual Breadth:** Unlike POT which focuses solely on high-intensity peaks, or daily aggregation which loses sub-daily detail and can split events, the continuous event definition captures the entire lifecycle of a rain period that could contribute to saturation and flooding.
# 
# Therefore, we will use the `most_intense_events` DataFrame (the top 10 events from `rain_events_df` sorted by total rainfall) as the basis for this detailed hourly visualization.
# 
# ### 14.2. Generating Hourly Rainfall Maps for Top 10 Rain Events
# 
# For each of the top 10 continuous rain events:
# *   If the event duration is longer than 10 hours, we will identify the 10 consecutive hours with the highest cumulative areal rainfall within that event.
# *   For each selected hour (up to 10 hours), a map will be generated showing:
#     *   Thiessen polygons colored by the 1-hour accumulated rainfall at their respective associated stations.
#     *   Flood occurrences reported during that specific hour.
#     *   The city boundary for spatial context.

# %%
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.patheffects as PathEffects
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ocorrencias_gdf_time_cut = ocorrencias_gdf.copy()
# ocorrencias_gdf_time_cut['data_fim'] = ocorrencias_gdf_time_cut['data_inicio'] + pd.Timedelta(1, 'h')

# --- ArcGIS Tiler Setup ---
class ArcGISWorldLightGray(cimgt.GoogleTiles):
    def _image_url(self, tile):
        x, y, z = tile
        return f"https://server.arcgisonline.com/arcgis/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}"

tiler = ArcGISWorldLightGray(cache=True)
map_projection_crs = tiler.crs
data_geographic_crs = ccrs.PlateCarree()

# --- Rainfall Colors and Binning ---
rainfall_bins = [0, 0.1, 2.5, 10, 25, 50, np.inf]
rainfall_labels = [
    "Trace (<0.1 mm)", "Light (0.1-2.5 mm)", "Moderate (2.5-10 mm)",
    "Heavy (10-25 mm)", "Very Heavy (25-50 mm)", "Extreme (>50 mm)"
]
rainfall_colors = ['#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', '#6baed6', '#3182bd', '#08519c']
actual_plot_colors = rainfall_colors[:len(rainfall_bins)-1]
custom_cmap = ListedColormap(actual_plot_colors)
norm = BoundaryNorm(rainfall_bins, custom_cmap.N)

city_boundary_map_proj = city_boundary_gdf.to_crs(map_projection_crs)
xmin_map, ymin_map, xmax_map, ymax_map = city_boundary_map_proj.total_bounds
padding_map = 7000
map_extent_viz = [xmin_map - padding_map, xmax_map + padding_map,
                  ymin_map - padding_map, ymax_map + padding_map]

TARGET_TILE_RESOLUTION_VIZ = 11

if thiessen_polygons_gdf.crs != CRS_PROJECTED:
    thiessen_polygons_gdf = thiessen_polygons_gdf.to_crs(CRS_PROJECTED)
if city_boundary_gdf.crs != CRS_PROJECTED:
    city_boundary_gdf = city_boundary_gdf.to_crs(CRS_PROJECTED)
if not ocorrencias_gdf_time_cut.empty and ocorrencias_gdf_time_cut.crs != CRS_PROJECTED:
    ocorrencias_gdf_time_cut = ocorrencias_gdf_time_cut.to_crs(CRS_PROJECTED)

for index, event_row in most_intense_events.iterrows():
    event_id = event_row['event_id']
    event_start_time = event_row['start_time']
    event_end_time = event_row['end_time']
    event_duration = event_row['duration']

    print(f"\nGenerating Enhanced Maps for Event ID: {event_id}")
    print(f"   Start: {event_start_time}, End: {event_end_time}, Duration: {event_duration}")

    # --- Define 3-hour intervals for 24 hours ---
    def generate_3h_timestamps(start, end):
        if start.date() != end.date():
            base = pd.Timestamp(start.date()) + pd.Timedelta(hours=12)
        else:
            base = pd.Timestamp(start.date())
        return [base + pd.Timedelta(hours=3*i) for i in range(8)]

    list_of_hourly_timestamps = generate_3h_timestamps(event_start_time, event_end_time)
    vis_window_start = min(list_of_hourly_timestamps)
    vis_window_end = max(list_of_hourly_timestamps) + pd.Timedelta(hours=3)

    # --- Resample Hourly Rainfall ---
    hourly_station_rain_event = pd.DataFrame()
    if not alertario.empty:
        alertario_in_vis_window = alertario[
            (alertario['timestamp'] >= vis_window_start) & (alertario['timestamp'] < vis_window_end)
        ]
        resampled_list = []
        for station_id, group in alertario_in_vis_window.groupby('id_estacao'):
            resampled = group.set_index('timestamp')['acumulado_chuva_15_min'].resample('3h').sum()
            if not resampled.empty:
                df = resampled.reset_index()
                df['id_estacao'] = station_id
                resampled_list.append(df)
        if resampled_list:
            hourly_station_rain_event = pd.concat(resampled_list)
            hourly_station_rain_event.rename(columns={'acumulado_chuva_15_min': 'hourly_rain_mm'}, inplace=True)

    # --- Plotting: 2x4 Grid (3-hour intervals down columns) ---
    fig = plt.figure(figsize=(12, 16))
    gs_main = gridspec.GridSpec(4, 2, figure=fig, hspace=0.25) # wspace=0.1, bottom=0.18, top=0.90, left=0.05, right=0.95

    for i, map_hour_start in enumerate(list_of_hourly_timestamps):
        col, row = divmod(i, 4)
        ax = fig.add_subplot(gs_main[row, col], projection=map_projection_crs)
        map_hour_end = map_hour_start + pd.Timedelta(hours=3)

        ax.set_extent(map_extent_viz, crs=map_projection_crs)
        ax.add_image(tiler, TARGET_TILE_RESOLUTION_VIZ, interpolation='bilinear')

        current_hour_data = pd.DataFrame()
        if not hourly_station_rain_event.empty:
            current_hour_data = hourly_station_rain_event[hourly_station_rain_event['timestamp'] == map_hour_start]

        thiessen_viz_gdf = thiessen_polygons_gdf.merge(
            current_hour_data[['id_estacao', 'hourly_rain_mm']],
            on='id_estacao', how='left'
        ).fillna({'hourly_rain_mm': 0})

        thiessen_viz_gdf_map_proj = thiessen_viz_gdf.to_crs(map_projection_crs)

        for _, poly_row_viz in thiessen_viz_gdf_map_proj.iterrows():
            rain_val = poly_row_viz['hourly_rain_mm']
            color_idx = norm(rain_val)
            color = custom_cmap(color_idx)
            ax.add_geometries([poly_row_viz.geometry], crs=map_projection_crs,
                              facecolor=color, edgecolor='slategray',
                              linewidth=0.4, alpha=0.65, zorder=2)

        city_boundary_map_proj_plot = city_boundary_gdf.to_crs(map_projection_crs)
        ax.add_geometries(city_boundary_map_proj_plot.geometry, crs=map_projection_crs,
                          facecolor='none', edgecolor='gray', linewidth=1.2, zorder=4,
                          path_effects=[PathEffects.withStroke(linewidth=2.5, foreground='white', alpha=0.7)])

        active_ocorrencias_map = pd.DataFrame()
        if not ocorrencias_gdf_time_cut.empty:
            active_ocorrencias_map = ocorrencias_gdf_time_cut[
                (ocorrencias_gdf_time_cut['data_inicio'] < str(map_hour_end)) &
                (ocorrencias_gdf_time_cut['data_inicio'] >= str(map_hour_start))
            ]
        if not active_ocorrencias_map.empty:
            ocorr_proj = active_ocorrencias_map.to_crs(map_projection_crs)
            ax.scatter(ocorr_proj.geometry.x, ocorr_proj.geometry.y,
                       transform=map_projection_crs, marker='^', color='red', s=60, alpha=0.9,
                       edgecolor='black', linewidth=0.7, zorder=5,
                       path_effects=[PathEffects.withStroke(linewidth=2, foreground='white', alpha=0.7)])

        ax.set_title(f"{map_hour_start.strftime('%H:%M')}–{map_hour_end.strftime('%H:%M')}", fontsize=11)

        gl = ax.gridlines(crs=data_geographic_crs, draw_labels=True, linewidth=0.6,
                          color='gray', alpha=0.4, linestyle=':')
        gl.top_labels = False
        gl.right_labels = False
        gl.left_labels = (col == 0)
        gl.bottom_labels = (row == 3)
        gl.xlabel_style = {'size': 9, 'color': 'black'}
        gl.ylabel_style = {'size': 9, 'color': 'black'}

    # --- Custom Legend ---
    legend_handles = [
        mpatches.Patch(facecolor=actual_plot_colors[i], edgecolor='dimgray', label=label)
        for i, label in enumerate(rainfall_labels)
    ]
    legend_handles.append(plt.Line2D([0], [0], marker='^', color='none', label='Flood Occurrence',
                                     markerfacecolor='red', markeredgecolor='black', markersize=10))
    legend_handles.append(plt.Line2D([0], [0], color='gray', lw=1.5, label='City Boundary'))

    fig.legend(handles=legend_handles, loc='lower center', ncol=4,
               bbox_to_anchor=(0.5, 0.03), fontsize=10, title="Legend",
               title_fontsize=13, frameon=True, facecolor='whitesmoke',
               framealpha=0.85, borderpad=0.8)

    fig.text(0.98, 0.02, f"Tiles: {tiler.__class__.__name__}, ESRI",
             ha='right', va='bottom', fontsize=7, color='dimgray',
             bbox=dict(facecolor='white', alpha=0.5, edgecolor='none', pad=1))

    fig.suptitle(f"3-Hourly Rainfall & Floods: Event {event_id}\n{event_start_time.strftime('%Y-%m-%d %H:%M')} to {event_end_time.strftime('%Y-%m-%d %H:%M')}",
                 fontsize=18, fontweight='bold', y=0.98)

    plt.show()


# %% [markdown]
# ---

# %% [markdown]
# # 14. Análise de Limiar de Intensidade-Duração por Estação
# 
# Esta seção implementa a etapa final da análise: a definição de limiares de chuva críticos para o acionamento de alagamentos. A nova abordagem, no entanto, não definirá uma única linha, mas **duas curvas de limiar** para criar três zonas distintas:
# 
# 1.  **Zona Segura:** Abaixo do limiar inferior, onde a ocorrência de alagamentos é muito improvável.
# 2.  **Zona Crítica:** Acima do limiar superior, onde a ocorrência de alagamentos é muito provável.
# 3.  **Zona Mista (ou de Incerteza):** Entre os dois limiares, representando uma região de transição onde fatores secundários podem determinar a ocorrência de um alagamento.
# 
# Para encontrar essas duas linhas, implementaremos e compararemos duas metodologias distintas, conforme solicitado.
# 
# **Avaliação da Estratégia de Segmentação de Eventos:**
# 
# Conforme a avaliação anterior, a segmentação de eventos de chuva para a cidade inteira **não é suficiente**. O artigo exige uma análise local. Portanto, mantemos a decisão de segmentar os eventos de chuva para cada uma das 33 estações pluviométricas de forma independente, utilizando o método de **Identificação de Período Contínuo de Chuva (Opção 3)**, que é o mais adequado para capturar a Duração e a Intensidade de sistemas de chuva individuais.
# 
# **Plano de Implementação:**
# 
# 1.  **Segmentação de Eventos de Chuva por Estação:** Identificar eventos de chuva discretos e calcular seus atributos (Duração e Intensidade Máxima) para cada estação.
# 2.  **Associação Espaço-Temporal e Classificação:** Vincular cada registro de alagamento a uma estação de influência e classificar os eventos de chuva como "Com Alagamento" (EA) ou "Sem Alagamento" (ESA).
# 3.  **Modelagem e Otimização dos Limiares:** Para cada estação, encontrar as duas curvas de limiar (`I = a * D^-b`) usando duas abordagens diferentes:
#     *   **Abordagem A:** Grid Search com Métrica de Otimização.
#     *   **Abordagem B:** Máquinas de Vetores de Suporte (SVM).
# 4.  **Visualização e Análise dos Resultados:** Gerar gráficos comparativos e consolidar os parâmetros de limiar (`a_inf`, `b_inf`, `a_sup`, `b_sup`) para análise.
# 
# ---
# 
# ## 15. Etapa 1: Segmentação de Eventos de Chuva por Estação
# 
# Nesta etapa, processaremos a série temporal de chuvas de 15 minutos para cada estação, a fim de identificar eventos discretos e calcular suas características principais.

# %%
# Importando bibliotecas necessárias para esta etapa
from tqdm.auto import tqdm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display

# Configurações de estilo para gráficos acadêmicos
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("viridis")
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 300

# %% [markdown]
# ### 15.1. Cálculo dos Pontos I-D por Evento

# %%
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
            continue # Pula durações menores que a resolução ou maiores que o próprio evento

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

# %% [markdown]
# ### 15.2. Função de Segmentação Atualizada

# %%
def segmenta_e_calcula_id(
    df_estacao: pd.DataFrame,
    id_estacao: int,
    min_rain: float = 0.1,
    min_dry_period_hours: int = 6,
    durations_to_analyze_min = [15, 30, 60, 120, 180, 720, 1440]
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
            point['id_evento_chuva'] = f"{id_estacao}_{int(start_time.timestamp())}" # ID único para o evento original
            point['start_time'] = start_time
            point['end_time'] = end_time + pd.Timedelta(minutes=15)
            all_event_points.append(point)

    return pd.DataFrame(all_event_points)

# %% [markdown]
# ### 15.3. Execução da Nova Segmentação em Lote

# %%
# Main Parameters
min_dry_period_hours = 1 # hour
min_rain = 1 # mm
# Durações de análise (em minutos), conforme o paper.
# Adaptamos 10 min para 15 min (0.25h) para se alinhar à resolução dos dados.
durations_to_analyze_min = [15, 30, 60, 120, 180, 720, 1440]

# ---

# Garante que o timestamp é do tipo datetime e define como índice para eficiência
if not pd.api.types.is_datetime64_any_dtype(alertario['timestamp']):
    alertario['timestamp'] = pd.to_datetime(alertario['timestamp'])
alertario_indexed = alertario.set_index('timestamp')

# Obtém a lista de estações únicas com dados de chuva
station_ids = alertario['id_estacao'].unique()

# Lista para armazenar os DataFrames de pontos I-D de cada estação
lista_pontos_id = []

print(f"Iniciando a nova análise I-D para {len(station_ids)} estações...")
for station_id in tqdm(station_ids, desc="Processando Estações"):
    df_station_data = alertario_indexed[alertario_indexed['id_estacao'] == station_id]
    
    # Chama a nova função de segmentação e cálculo I-D
    station_id_points = segmenta_e_calcula_id(
        df_station_data,
        station_id,
        min_rain,
        min_dry_period_hours,
        durations_to_analyze_min
    )
    
    if not station_id_points.empty:
        lista_pontos_id.append(station_id_points)

# Concatena todos os resultados em um único DataFrame
# O novo DataFrame contém múltiplos pontos (D,I) para cada evento de chuva original
pontos_id_df = pd.concat(lista_pontos_id, ignore_index=True)

# Renomeia a coluna de intensidade para manter compatibilidade com o código subsequente
pontos_id_df = pontos_id_df.rename(columns={'intensidade_mm_h': 'intensidade_max_mm_h'})

print("\nAnálise I-D concluída.")
print(f"Total de pontos (D, I) gerados: {len(pontos_id_df)}")
print(f"Total de eventos de chuva originais identificados: {pontos_id_df['id_evento_chuva'].nunique()}")

# %% [markdown]
# ### 15.4. Visualização do Cálculo I-D

# %%
# Exibe as primeiras linhas do DataFrame resultante com formatação
print("\nAmostra dos Pontos I-D Gerados:")
display(pontos_id_df.head())

# Exibe estatísticas descritivas formatadas
print("\nEstatísticas Descritivas dos Pontos I-D:")
display(pontos_id_df[['duracao_h', 'intensidade_max_mm_h']].describe().style.format("{:.2f}"))

# Visualização inicial para verificar a estrutura dos dados
print("\nVisualização Rápida dos Pontos I-D Gerados (Estação 21):")
df_plot = pontos_id_df[pontos_id_df['id_estacao'] == 21]
if not df_plot.empty:
    plt.figure(figsize=(10, 7))
    sns.scatterplot(data=df_plot, x='duracao_h', y='intensidade_max_mm_h', hue='id_estacao', palette='viridis', s=100)
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Gráfico de Intensidade-Duração (Estrutura Correta)')
    plt.xlabel('Duração da Análise (h)')
    plt.ylabel('Intensidade Máxima Calculada (mm/h)')
    plt.grid(True, which="both", ls="--")
    # plt.legend(title='ID do Evento Original', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()
else:
    print("Não há dados para plotar para a estação 21.")

# %% [markdown]
# ### 15.4. Visualização das Características dos Eventos
# 
# Para entender melhor a natureza dos eventos de chuva identificados, visualizamos a distribuição de suas durações e intensidades máximas.

# %%
if not pontos_id_df.empty:
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Distribuição das Características dos Eventos de Chuva por Estação', fontsize=16, y=1.02)

    # Gráfico 1: Distribuição da Duração dos Eventos
    sns.histplot(data=pontos_id_df, x='duracao_h', bins=50, ax=axes[0], color=sns.color_palette("viridis")[2])
    axes[0].set_title('Distribuição da Duração (D)', fontsize=12)
    axes[0].set_xlabel('Duração do Evento (horas)', fontsize=11)
    axes[0].set_ylabel('Frequência', fontsize=11)
    axes[0].set_yscale('log') # Escala log para melhor visualização da cauda longa

    # Gráfico 2: Distribuição da Intensidade Máxima dos Eventos
    sns.histplot(data=pontos_id_df, x='intensidade_max_mm_h', bins=50, ax=axes[1], color=sns.color_palette("viridis")[4])
    axes[1].set_title('Distribuição da Intensidade Máxima (I)', fontsize=12)
    axes[1].set_xlabel('Intensidade Máxima em 1h (mm/h)', fontsize=11)
    axes[1].set_ylabel('Frequência', fontsize=11)
    axes[1].set_yscale('log')

    plt.tight_layout()
    plt.show()
else:
    print("Nenhum evento de chuva foi identificado para gerar os gráficos de distribuição.")


# %% [markdown]
# ## 16. Etapa 2: Associação Espaço-Temporal e Classificação dos Eventos
# 
# Com os eventos de chuva por estação definidos na etapa anterior, o próximo passo é associá-los aos registros de alagamento para classificá-los. Este processo é fundamental para determinar quais eventos de chuva estão correlacionados com impactos observados no solo.

# %% [markdown]
# ### 16.1. Associação Espacial dos Alagamentos
# 
# Primeiro, atribuímos cada ocorrência de alagamento à sua estação pluviométrica de influência, utilizando os Polígonos de Thiessen gerados anteriormente.

# %%
import geopandas as gpd
import pandas as pd
from IPython.display import display

# Garante que os GeoDataFrames estão no mesmo sistema de coordenadas projetado para o join espacial
if 'CRS_PROJECTED' not in locals():
    CRS_PROJECTED = "EPSG:31983" # SIRGAS 2000 / UTM zone 23S

if ocorrencias_gdf.crs != CRS_PROJECTED:
    ocorrencias_gdf = ocorrencias_gdf.to_crs(CRS_PROJECTED)
if thiessen_polygons_gdf.crs != CRS_PROJECTED:
    thiessen_polygons_gdf = thiessen_polygons_gdf.to_crs(CRS_PROJECTED)

# Realiza o join espacial para associar cada alagamento ao seu polígono e, consequentemente, à sua estação
# Usamos 'inner' para manter apenas os alagamentos que caem dentro de uma área de influência
floods_with_station_gdf = gpd.sjoin(
    ocorrencias_gdf,
    thiessen_polygons_gdf[['id_estacao', 'geometry']],
    how='inner',
    predicate='within'
)

# Seleciona e renomeia colunas para clareza
floods_with_station_gdf = floods_with_station_gdf[['id_evento', 'data_inicio', 'id_estacao', 'geometry']].reset_index(drop=True)

print(f"Total de {len(floods_with_station_gdf)} ocorrências de alagamento associadas a uma estação pluviométrica.")
print("\nAmostra de Alagamentos com Estação de Influência Atribuída:")
display(floods_with_station_gdf.head())

# %% [markdown]
# ### 16.2. Classificação dos Eventos de Chuva (EA vs. ESA)
# 
# Agora, usamos a associação temporal para classificar cada evento de chuva em `pontos_id_df` como "Com Alagamento" (EA) ou "Sem Alagamento" (ESA). Um evento de chuva é classificado como EA se o seu período de ocorrência coincidiu com pelo menos um registro de alagamento em sua área de influência.

# %%
print("Iniciando a classificação dos eventos de chuva...")

# 1. Criar DataFrame de eventos de chuva únicos para a classificação
# Isso evita processamento redundante, já que a classificação se aplica ao evento inteiro.
eventos_unicos_df = pontos_id_df.drop_duplicates(subset=['id_evento_chuva']).copy()
eventos_unicos_df = eventos_unicos_df[['id_evento_chuva', 'id_estacao', 'start_time', 'end_time']]

# 2. Preparar os dados e classificar os eventos únicos
floods_to_check = floods_with_station_gdf[['data_inicio', 'id_estacao']]

# Garantir tipos de dados consistentes para o merge (uma causa comum de falhas)
eventos_unicos_df['id_estacao'] = eventos_unicos_df['id_estacao'].astype(str)
floods_to_check['id_estacao'] = floods_to_check['id_estacao'].astype(str)

# Garantir que todos os datetimes são timezone-aware (UTC) para evitar erros de comparação
# Esta é uma boa prática mantida do código original.
for df in [eventos_unicos_df, floods_to_check]:
    for col in ['start_time', 'end_time', 'data_inicio']:
        if col in df.columns:
            # Se a coluna for timezone-naive, localiza para UTC.
            if df[col].dt.tz is None:
                df[col] = df[col].dt.tz_localize('UTC')
            # Se já tiver timezone, apenas converte para UTC.
            else:
                df[col] = df[col].dt.tz_convert('UTC')

# Merge para criar pares de evento de chuva e alagamento que ocorreram na mesma área de estação
merged_pairs = pd.merge(eventos_unicos_df, floods_to_check, on='id_estacao')

# Filtra para encontrar os pares onde há sobreposição temporal
temporal_overlap_condition = (
    (merged_pairs['data_inicio'] >= merged_pairs['start_time']) &
    (merged_pairs['data_inicio'] < merged_pairs['end_time'])
)
eventos_com_alagamento = merged_pairs[temporal_overlap_condition]

# Obtém a lista de IDs únicos dos eventos de chuva que causaram alagamento
ids_eventos_ea = eventos_com_alagamento['id_evento_chuva'].unique()

# 3. Propagar a classificação para o DataFrame principal de pontos I-D
# Primeiro, inicializa todos os pontos como 'ESA' (Evento Sem Alagamento)
pontos_id_df['classificacao'] = 'ESA'

# Em seguida, atualiza para 'EA' (Evento Com Alagamento) aqueles cujos IDs de evento correspondem
pontos_id_df.loc[pontos_id_df['id_evento_chuva'].isin(ids_eventos_ea), 'classificacao'] = 'EA'


# --- SAÍDAS E VERIFICAÇÕES (Mantendo o Padrão do Código Original) ---

print("Classificação dos eventos de chuva concluída.")

# Resumo global da classificação dos pontos I-D
classification_counts = pontos_id_df['classificacao'].value_counts()
print("\nResumo da Classificação Global dos Pontos I-D:")
print(f"Pontos Sem Alagamento (ESA): {classification_counts.get('ESA', 0)}")
print(f"Pontos Com Alagamento (EA):  {classification_counts.get('EA', 0)}")

# Amostra do DataFrame final com a nova coluna 'classificacao'
print("\nAmostra do DataFrame 'pontos_id_df' com a classificação:")
display(pontos_id_df.sample(5))

# Resumo da classificação por estação, contando *eventos únicos*
# É crucial usar drop_duplicates aqui para contar eventos, não pontos I-D.
eventos_classificados_df = pontos_id_df.drop_duplicates(subset=['id_evento_chuva'])
classification_summary = eventos_classificados_df.groupby('id_estacao')['classificacao'].value_counts().unstack(fill_value=0)
classification_summary['Total'] = classification_summary.sum(axis=1)
# classification_summary = classification_summary.sort_values(by='EA', ascending=False)

print("\nResumo da Classificação de EVENTOS por Estação:")
display(classification_summary.style.format("{:d}")) #.background_gradient(cmap='viridis', subset=['EA', 'ESA'], axis=0)

# A visualização do gráfico de barras (código 16.3) pode agora ser executada
# usando o `classification_summary` que acabamos de criar, e funcionará como esperado.

# %% [markdown]
# ### 16.3. Visualização da Classificação
# 
# Um gráfico de barras empilhadas é uma forma eficaz de visualizar a proporção de eventos com e sem alagamento para cada estação, permitindo uma rápida comparação da criticidade entre as diferentes áreas de influência.

# %%
# Prepara os dados para o gráfico de barras empilhadas
summary_for_plot = classification_summary[['EA', 'ESA']].copy()
summary_for_plot['EA_perc'] = (summary_for_plot['EA'] / (summary_for_plot['EA'] + summary_for_plot['ESA'])) * 100
summary_for_plot = summary_for_plot.sort_values(by='EA_perc', ascending=False)

# Criação do gráfico
fig, ax = plt.subplots(figsize=(12, 8))

# Cores para as barras
colors = {'EA': '#d95f02', 'ESA': '#7570b3'}

# Plot das barras empilhadas
summary_for_plot[['ESA', 'EA']].plot(
    kind='bar',
    stacked=True,
    ax=ax,
    color=[colors['ESA'], colors['EA']],
    width=0.8
)

# Configuração de títulos e rótulos
ax.set_title('Contagem de Eventos de Chuva por Classificação e Estação', fontsize=16, pad=20)
ax.set_xlabel('ID da Estação Pluviométrica', fontsize=12)
ax.set_ylabel('Número de Eventos de Chuva Identificados', fontsize=12)
ax.tick_params(axis='x', rotation=90, labelsize=10)
ax.tick_params(axis='y', labelsize=10)

# Legenda
handles, labels = ax.get_legend_handles_labels()
ax.legend(
    handles,
    ['Eventos Sem Alagamento (ESA)', 'Eventos Com Alagamento (EA)'],
    title='Classificação',
    fontsize=11,
    title_fontsize=12,
    bbox_to_anchor=(1.02, 1),
    loc='upper left'
)

# Adiciona uma grade horizontal para melhor leitura
ax.grid(axis='y', linestyle='--', alpha=0.7)
ax.set_axisbelow(True)

plt.tight_layout()
plt.show()


# %% [markdown]
# ## 17. Etapa 3: Modelagem e Definição das Zonas de Limiar
# 
# Nesta etapa, determinaremos as duas curvas de limiar (`I = a * D⁻ᵇ`) que definem as zonas segura, mista e crítica para cada estação pluviométrica. Implementaremos e compararemos duas abordagens distintas para encontrar os parâmetros `(a, b)` para as curvas de limiar inferior e superior.

# %%
# Importando bibliotecas para modelagem
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import warnings

# Suprimir avisos de convergência do SVM que podem poluir o output
from sklearn.exceptions import ConvergenceWarning
warnings.filterwarnings("ignore", category=ConvergenceWarning)
warnings.filterwarnings("ignore", category=UserWarning, module='sklearn')

# %% [markdown]
# ### 17.1. Abordagem A: Grid Search com Métrica de Otimização
# 
# Esta abordagem testa sistematicamente uma grade de parâmetros `(a, b)` para encontrar as curvas que melhor satisfazem critérios pré-definidos para os limiares inferior e superior.
# 
# -   **Limiar Inferior:** Busca a curva mais alta possível que mantém a taxa de falsos positivos (eventos sem alagamento classificados incorretamente como críticos) abaixo de um percentual baixo (ex: 5%).
# -   **Limiar Superior:** Busca a curva mais baixa possível que mantém a taxa de verdadeiros positivos (eventos com alagamento classificados corretamente) acima de um percentual alto (ex: 80%).

# %%
def encontrar_limiares_grid_search(df_eventos_estacao: pd.DataFrame,
                                    fpr_threshold: float = 0.05,
                                    tpr_threshold: float = 0.80,
                                    a_vals = np.linspace(5, 50, 100),
                                    b_vals = np.linspace(0.1, 1.5, 100)) -> dict:
    """
    Encontra os limiares inferior e superior usando uma busca em grade (grid search).

    Args:
        df_eventos_estacao (pd.DataFrame): Eventos de chuva para uma estação.
        fpr_threshold (float): Limiar máximo da Taxa de Falsos Positivos para a curva inferior.
        tpr_threshold (float): Limiar mínimo da Taxa de Verdadeiros Positivos para a curva superior.

    Returns:
        dict: Dicionário com os parâmetros 'a_inf_grid', 'b_inf_grid', 'a_sup_grid', 'b_sup_grid'.
    """
    eventos_ea = df_eventos_estacao[df_eventos_estacao['classificacao'] == 'EA']
    eventos_esa = df_eventos_estacao[df_eventos_estacao['classificacao'] == 'ESA']

    if eventos_ea.empty or eventos_esa.empty:
        return {'a_inf_grid': np.nan, 'b_inf_grid': np.nan, 'a_sup_grid': np.nan, 'b_sup_grid': np.nan}

    # Define a grade de busca para os parâmetros

    best_lower = {'a': np.nan, 'b': np.nan, 'score': -np.inf}
    best_upper = {'a': np.nan, 'b': np.nan, 'score': -np.inf}

    for a in a_vals:
        for b in b_vals:
            # Calcula o limiar para todos os eventos com o par (a, b) atual
            i_limiar_ea = a * (eventos_ea['duracao_h'] ** -b)
            i_limiar_esa = a * (eventos_esa['duracao_h'] ** -b)

            # Calcula métricas
            tp = (eventos_ea['intensidade_max_mm_h'] >= i_limiar_ea).sum()
            fp = (eventos_esa['intensidade_max_mm_h'] >= i_limiar_esa).sum()
            
            tpr = tp / len(eventos_ea)
            fpr = fp / len(eventos_esa)

            # Otimização para o limiar inferior (maximizar 'a' mantendo FPR baixo)
            if fpr <= fpr_threshold:
                if a > best_lower['score']:
                    best_lower = {'a': a, 'b': b, 'score': a}

            # Otimização para o limiar superior (minimizar 'a' mantendo TPR alto)
            if tpr >= tpr_threshold:
                # Usamos -a para que o score maior (-a menor) seja melhor
                if -a > best_upper['score']:
                    best_upper = {'a': a, 'b': b, 'score': -a}

    return {
        'a_inf_grid': best_lower['a'], 'b_inf_grid': best_lower['b'],
        'a_sup_grid': best_upper['a'], 'b_sup_grid': best_upper['b']
    }

# %% [markdown]
# ### 17.2. Abordagem B: Máquinas de Vetores de Suporte (SVM)
# 
# Esta abordagem utiliza um classificador SVM linear no espaço logarítmico dos dados. As margens do hiperplano de separação encontrado pelo SVM são usadas para definir as curvas de limiar inferior e superior, oferecendo uma fronteira de decisão matematicamente robusta.

# %%
def encontrar_limiares_svm(df_eventos_estacao: pd.DataFrame) -> dict:
    """
    Encontra os limiares inferior e superior usando um classificador SVM.

    Args:
        df_eventos_estacao (pd.DataFrame): Eventos de chuva para uma estação.

    Returns:
        dict: Dicionário com os parâmetros 'a_inf_svm', 'b_inf_svm', 'a_sup_svm', 'b_sup_svm'.
    """
    # Filtra dados para evitar log(0) e garante que há ambas as classes
    df_filtered = df_eventos_estacao[
        (df_eventos_estacao['duracao_h'] > 0) & (df_eventos_estacao['intensidade_max_mm_h'] > 0)
    ]
    if df_filtered['classificacao'].nunique() < 2:
        return {'a_inf_svm': np.nan, 'b_inf_svm': np.nan, 'a_sup_svm': np.nan, 'b_sup_svm': np.nan}

    # Transforma os dados para o espaço logarítmico
    X = np.log(df_filtered[['duracao_h', 'intensidade_max_mm_h']].values)
    y = (df_filtered['classificacao'] == 'EA').astype(int).values

    # Cria e treina o pipeline SVM com normalização e pesos de classe balanceados
    svm_pipeline = make_pipeline(StandardScaler(), SVC(kernel='linear', class_weight='balanced'))
    svm_pipeline.fit(X, y)
    
    # Extrai o modelo treinado do pipeline
    svc_model = svm_pipeline.named_steps['svc']
    scaler = svm_pipeline.named_steps['standardscaler']
    
    # Coeficientes e intercepto do hiperplano no espaço escalado
    w = svc_model.coef_[0]
    intercept = svc_model.intercept_[0]
    
    # Desfaz a escala para obter os coeficientes no espaço logarítmico original
    w_original = w / scaler.scale_
    intercept_original = intercept - np.sum(w * scaler.mean_ / scaler.scale_)

    # Extrai os coeficientes para log(D) e log(I)
    w_d, w_i = w_original[0], w_original[1]

    if abs(w_i) < 1e-9: # Evita divisão por zero
        return {'a_inf_svm': np.nan, 'b_inf_svm': np.nan, 'a_sup_svm': np.nan, 'b_sup_svm': np.nan}

    # Calcula os parâmetros 'a' e 'b' para as três linhas (margens e decisão)
    # A equação é: log(I) = - (w_d/w_i) * log(D) - (intercept/w_i)
    # Comparando com log(I) = log(a) - b*log(D), temos:
    # b = w_d / w_i
    # a = exp(-intercept / w_i)
    
    b_svm = w_d / w_i
    
    # Interceptos para as margens inferior, de decisão e superior
    intercept_inf = (intercept_original - 1) / w_i
    intercept_sup = (intercept_original + 1) / w_i
    
    a_inf = np.exp(-intercept_sup)
    a_sup = np.exp(-intercept_inf)
    
    # Garante que a_sup > a_inf
    if a_inf > a_sup:
        a_inf, a_sup = a_sup, a_inf

    return {
        'a_inf_svm': a_inf, 'b_inf_svm': b_svm,
        'a_sup_svm': a_sup, 'b_sup_svm': b_svm
    }

# %% [markdown]
# ### 17.3. Execução em Lote
# 
# Agora, aplicamos ambas as funções de modelagem a todas as estações que possuem um número mínimo de eventos com e sem alagamento, consolidando os resultados em uma única tabela para análise comparativa.

# %%
fpr_threshold = 0.05
tpr_threshold = 0.80
a_vals = np.linspace(5, 50, 100)
b_vals = np.linspace(0.1, 1.5, 100)

# Lista para armazenar os resultados de cada estação
resultados_lista = []
station_ids_com_dados = pontos_id_df['id_estacao'].unique()

print(f"Iniciando modelagem de limiares para {len(station_ids_com_dados)} estações...")
for station_id in tqdm(station_ids_com_dados, desc="Modelando Limiares"):
    df_station = pontos_id_df[pontos_id_df['id_estacao'] == station_id]
    
    # Verifica se há dados suficientes para a modelagem
    counts = df_station['classificacao'].value_counts()
    if 'EA' not in counts or 'ESA' not in counts or counts['EA'] < 5 or counts['ESA'] < 5:
        continue

    # Executa a Abordagem A: Grid Search
    params_grid = encontrar_limiares_grid_search(
        df_station,
        fpr_threshold,
        tpr_threshold,
        a_vals, b_vals
    )
    
    # Executa a Abordagem B: SVM
    params_svm = encontrar_limiares_svm(df_station)
    
    # Consolida os resultados
    resultado_final = {'id_estacao': station_id}
    resultado_final.update(params_grid)
    resultado_final.update(params_svm)
    resultados_lista.append(resultado_final)

# Cria o DataFrame final com os resultados consolidados
resultados_limiar_consolidado = pd.DataFrame(resultados_lista).set_index('id_estacao')

print("\nModelagem concluída.")
print("Tabela de Parâmetros de Limiar Consolidados (Grid Search vs. SVM):")

# Estiliza a tabela para publicação
styled_table = resultados_limiar_consolidado.style.format("{:.2f}", na_rep="-").set_table_styles(
    [{'selector': 'th', 'props': [('text-align', 'center')]},
     {'selector': 'td', 'props': [('text-align', 'center')]}]
).set_caption("Parâmetros 'a' e 'b' para as curvas de limiar inferior (inf) e superior (sup) por método de modelagem.")

display(styled_table)


# %% [markdown]
# ## 18. Etapa 4: Visualização e Análise dos Resultados
# 
# A etapa final consiste em visualizar os limiares encontrados por ambos os métodos para interpretar e comparar os resultados. Criaremos gráficos de Intensidade-Duração para estações individuais e mapas para analisar a distribuição espacial dos parâmetros de limiar.

# %% [markdown]
# ### 18.1. Criação da Função de Plotagem Comparativa
# 
# Desenvolvemos uma função robusta para gerar o gráfico de Intensidade-Duração para uma única estação. Esta função plotará os eventos de chuva, coloridos por sua classificação, e sobreporá as duas curvas de limiar (inferior e superior) encontradas por ambos os métodos (Grid Search e SVM).

# %%
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plotar_grafico_limiar_comparativo(id_estacao: int, df_eventos: pd.DataFrame, df_resultados: pd.DataFrame, sample=1.0, random_state=None):
    """
    Gera um gráfico de Intensidade-Duração comparando os limiares dos métodos Grid Search e SVM.

    Args:
        id_estacao (int): O ID da estação a ser plotada.
        df_eventos (pd.DataFrame): DataFrame com todos os eventos de chuva de todas as estações.
        df_resultados (pd.DataFrame): DataFrame com os parâmetros de limiar consolidados.
    """
    # Filtra os dados para a estação específica
    df_station_events = df_eventos[df_eventos['id_estacao'] == id_estacao]
    if df_station_events.empty:
        print(f"Não há dados de eventos para a estação {id_estacao}.")
        return

    if sample and sample > 1:
        df_station_events = df_station_events.sample(sample, replace=False, random_state=random_state)
    elif sample and sample > 0:
        size = int(samples * len(df_station_events))
        df_station_events = df_station_events.sample(size, replace=False, random_state=random_state)
    
    params = df_resultados.loc[id_estacao]

    # Separa eventos com e sem alagamento
    eventos_ea = df_station_events[df_station_events['classificacao'] == 'EA']
    eventos_esa = df_station_events[df_station_events['classificacao'] == 'ESA']

    # Configuração do gráfico
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Cores e marcadores
    colors = {'EA': '#d95f02', 'ESA': '#7570b3'}
    
    # Plot dos pontos de evento
    ax.scatter(eventos_esa['duracao_h'], eventos_esa['intensidade_max_mm_h'],
               color=colors['ESA'], alpha=0.5, label='Evento Sem Alagamento (ESA)', s=50, edgecolor='k', linewidth=0.5)
    ax.scatter(eventos_ea['duracao_h'], eventos_ea['intensidade_max_mm_h'],
               color=colors['EA'], alpha=0.8, label='Evento Com Alagamento (EA)', s=80, marker='^', edgecolor='k', linewidth=0.5)

    # Gera pontos para as curvas de limiar
    d_range = np.logspace(np.log10(max(0.1, df_station_events['duracao_h'].min())),
                          np.log10(df_station_events['duracao_h'].max()), 100)

    # Plot das curvas do Grid Search
    if pd.notna(params['a_inf_grid']):
        i_inf_grid = params['a_inf_grid'] * (d_range ** -params['b_inf_grid'])
        ax.plot(d_range, i_inf_grid, color='blue', linestyle='--', linewidth=2, label='Grid Search - Limiar Inferior')
    if pd.notna(params['a_sup_grid']):
        i_sup_grid = params['a_sup_grid'] * (d_range ** -params['b_sup_grid'])
        ax.plot(d_range, i_sup_grid, color='blue', linestyle='-', linewidth=2.5, label='Grid Search - Limiar Superior')

    # Plot das curvas do SVM
    if pd.notna(params['a_inf_svm']):
        i_inf_svm = params['a_inf_svm'] * (d_range ** -params['b_inf_svm'])
        ax.plot(d_range, i_inf_svm, color='red', linestyle='--', linewidth=2, label='SVM - Limiar Inferior')
    if pd.notna(params['a_sup_svm']):
        i_sup_svm = params['a_sup_svm'] * (d_range ** -params['b_sup_svm'])
        ax.plot(d_range, i_sup_svm, color='red', linestyle='-', linewidth=2.5, label='SVM - Limiar Superior')

    # Configuração dos eixos e título
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_title(f'Limiares de Intensidade-Duração para a Estação {id_estacao}', fontsize=16, pad=20)
    ax.set_xlabel('Duração do Evento (D) [horas]', fontsize=12)
    ax.set_ylabel('Intensidade Máxima em 1h (I) [mm/h]', fontsize=12)
    ax.grid(True, which="both", linestyle='--', linewidth=0.5)
    
    # Limites dos eixos para melhor visualização
#     ax.set_xlim(left=0.1)
#     ax.set_ylim(bottom=1)

    # Legenda
    ax.legend(title='Legenda', fontsize=10, title_fontsize=11)
    
    plt.tight_layout()
    plt.show()

# %% [markdown]
# ### 18.2. Geração e Análise dos Gráficos
# 
# Geramos os gráficos para algumas estações representativas para uma inspeção visual detalhada dos resultados. A seleção inclui estações com um número significativo de eventos com alagamento para garantir uma análise robusta.

# %%
# Seleciona as 3 estações com mais eventos de alagamento para visualização

TOP_N = 33
top_stations_to_plot = classification_summary.sort_values(by='EA', ascending=False).head(TOP_N).index

print("Gerando gráficos de limiar para as 3 estações com mais eventos de alagamento registrados...")
for station_id in top_stations_to_plot:
    if station_id in resultados_limiar_consolidado.index:
        plotar_grafico_limiar_comparativo(
            station_id,
            pontos_id_df,
            resultados_limiar_consolidado,
            sample=500,
            random_state=None
        )
    else:
        print(f"Estação {station_id} não possui resultados de limiar para plotar (provavelmente por falta de dados).")

# %% [markdown]
# ### 18.3. Análise Espacial dos Parâmetros de Limiar
# 
# Para entender como os limiares de chuva variam geograficamente pela cidade, criamos mapas coropléticos (choropleth maps). Estes mapas colorem a área de influência de cada estação (Polígono de Thiessen) de acordo com os valores dos parâmetros `a` e `b` encontrados. Analisaremos os resultados do método **Grid Search**, que é mais diretamente interpretável em termos de taxas de detecção.
# 
# -   **Parâmetro `a`:** Relaciona-se com a magnitude da chuva. Valores mais altos de `a` indicam que a estação suporta chuvas de maior intensidade para uma mesma duração antes de gerar alagamentos.
# -   **Parâmetro `b`:** Relaciona-se com a sensibilidade à duração. Valores mais altos de `b` indicam que a intensidade crítica diminui mais rapidamente com o aumento da duração do evento.

# %%
# Junta os resultados dos limiares ao GeoDataFrame dos polígonos de Thiessen
thiessen_com_limiares_gdf = thiessen_polygons_gdf.merge(
    resultados_limiar_consolidado,
    left_on='id_estacao',
    right_index=True,
    how='left'
)

# Função para criar mapas coropléticos
def plotar_mapa_parametros(gdf, column, title, cmap='viridis'):
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    
    # Plota os polígonos com base no valor da coluna
    gdf.plot(column=column, ax=ax, legend=True,
             legend_kwds={'label': "Valor do Parâmetro", 'orientation': "horizontal"},
             cmap=cmap, missing_kwds={"color": "lightgrey", "label": "Sem Dados"},
             edgecolor='black', linewidth=0.5)
    
    # Adiciona o contorno da cidade
    city_boundary_gdf.plot(ax=ax, facecolor='none', edgecolor='black', linewidth=1.5)
    
    # Adiciona rótulos com o ID da estação
    for idx, row in gdf.dropna(subset=[column]).iterrows():
        centroid = row.geometry.centroid
        ax.text(centroid.x, centroid.y, str(row['id_estacao']),
                fontsize=8, ha='center', color='white',
                path_effects=[plt.matplotlib.patheffects.withStroke(linewidth=2, foreground='black')])

    ax.set_title(title, fontsize=16, pad=20)
    ax.set_xlabel("Coordenada Leste (m)", fontsize=12)
    ax.set_ylabel("Coordenada Norte (m)", fontsize=12)
    ax.tick_params(axis='both', which='major', labelsize=10)
    ax.grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.show()

# Gera os mapas para os parâmetros do limiar superior do método Grid Search
if not thiessen_com_limiares_gdf.empty:
    plotar_mapa_parametros(thiessen_com_limiares_gdf, 'a_sup_grid', 'Distribuição Espacial do Parâmetro "a" (Limiar Superior - Grid Search)', cmap='plasma')
    plotar_mapa_parametros(thiessen_com_limiares_gdf, 'b_sup_grid', 'Distribuição Espacial do Parâmetro "b" (Limiar Superior - Grid Search)', cmap='cividis')
else:
    print("Não foi possível gerar os mapas pois não há dados de limiares para associar aos polígonos.")



