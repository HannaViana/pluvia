"""
Chart 2: Tendência de Eventos por Estação do Ano
Source: temporal.py lines 438-518
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuration
plt.style.use('seaborn-v0_8-paper')
plt.rcParams['figure.dpi'] = 300

# Data paths
input_data_file = 'nbs/exploration/ocorrencias/ocorrencias_filtradas.csv'
output_directory = 'nbs/analysis/charts'
os.makedirs(output_directory, exist_ok=True)

# Load data
ocorrencias = pd.read_csv(input_data_file)
pops = pd.read_csv('data/raw/adm_cor_comando/pops.csv', index_col=0)

# Preprocessing
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

# Define season function
def get_season(date):
    month = date.month
    if month in [12, 1, 2]:
        return 'Summer'
    elif month in [3, 4, 5]:
        return 'Autumn'
    elif month in [6, 7, 8]:
        return 'Winter'
    else:
        return 'Spring'

# Create season and year-season label
ocorrencias['season'] = ocorrencias['data_inicio'].apply(get_season)
ocorrencias['year'] = ocorrencias['data_inicio'].dt.year

# Adjust year for December (belongs to next year's Summer)
ocorrencias.loc[ocorrencias['data_inicio'].dt.month == 12, 'year'] += 1

# Combine into a single label for plotting
ocorrencias['season_label'] = ocorrencias['year'].astype(str) + '-' + ocorrencias['season']

# Group and count events per season-year
events_per_season = (
    ocorrencias.groupby('season_label')
    .size()
    .reset_index(name='count')
)

# Ensure chronological order
events_per_season['season_order'] = pd.to_datetime(
    events_per_season['season_label'].str.extract(r'(\d{4})')[0] +
    '-' +
    events_per_season['season_label'].str.extract(r'-(\w+)$')[0].map({
        'Summer': '01',
        'Autumn': '04',
        'Winter': '07',
        'Spring': '10'
    })
)
events_per_season = events_per_season.sort_values('season_order')

# Create visualization
fig, ax = plt.subplots(figsize=(10, 6))

sns.lineplot(
    data=events_per_season,
    x='season_order',
    y='count',
    marker='o',
    markersize=6,
    linewidth=2,
    color='steelblue',
    ax=ax
)

# Styling
ax.set_title('Event Trend by Season', fontsize=16, weight='bold')
ax.set_xlabel('Season', fontsize=12)
ax.set_ylabel('Number of Events', fontsize=12)
ax.grid(True, which='major', linestyle='--', linewidth=0.5)
ax.tick_params(axis='x', labelsize=10)
ax.tick_params(axis='y', labelsize=10)

# Format X axis
ax.set_xticks(events_per_season['season_order'])
ax.set_xticklabels(events_per_season['season_label'], rotation=45, ha='right')

# Save
plt.tight_layout()
plt.savefig(f'{output_directory}/chart_02_seasonal_trend.png', dpi=300, bbox_inches='tight')
print(f"Chart saved to {output_directory}/chart_02_seasonal_trend.png")
plt.close()
