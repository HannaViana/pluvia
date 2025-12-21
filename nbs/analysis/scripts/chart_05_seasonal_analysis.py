"""
Chart 5: Análise Sazonal das Ocorrências de Inundação
Source: temporal.py lines 763-834
"""

import pandas as pd
import matplotlib.pyplot as plt
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

# Assign season
ocorrencias['season'] = ocorrencias['data_inicio'].apply(get_season)

# Count events per season
events_per_season = (
    ocorrencias['season']
    .value_counts()
    .reindex(['Summer', 'Autumn', 'Winter', 'Spring'])
    .reset_index()
)
events_per_season.columns = ['season', 'count']

# Create visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
fig.suptitle('Seasonal Analysis of Flood Occurrences', fontsize=16, weight='bold')

# Colors (colorblind-friendly palette)
colors = ['#E69F00', '#009E73', '#0072B2', '#D55E00']
season_order = ['Summer', 'Autumn', 'Winter', 'Spring']
events_per_season_sorted = events_per_season.set_index('season').loc[season_order]

# Bar chart (ax1)
ax1.bar(events_per_season_sorted.index, events_per_season_sorted['count'], color=colors)
ax1.set_title('Event Count by Season', fontsize=14)
ax1.set_ylabel('Number of Events', fontsize=12)
ax1.tick_params(axis='x', rotation=15, labelsize=12)
ax1.tick_params(axis='y', labelsize=10)
ax1.grid(axis='y', linestyle='--', alpha=0.7)

# Pie chart (ax2)
ax2.pie(events_per_season_sorted['count'], labels=events_per_season_sorted.index,
        autopct='%1.1f%%', pctdistance=0.8, startangle=90, colors=colors,
        wedgeprops=dict(width=0.4, edgecolor='w'))
ax2.set_title('Percentage Distribution by Season', fontsize=14)
ax2.axis('equal')

# Increase pie chart label size
for text in ax2.texts:
    text.set_fontsize(12)

# Save
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(f'{output_directory}/chart_05_seasonal_analysis.png', dpi=300, bbox_inches='tight')
print(f"Chart saved to {output_directory}/chart_05_seasonal_analysis.png")
plt.close()
