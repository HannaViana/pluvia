"""
Chart 4: Tendência Média de Eventos por Semana do Ano
Source: temporal.py lines 644-688
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

# Extract week of year
ocorrencias['week_of_year'] = ocorrencias['data_inicio'].dt.isocalendar().week

# Aggregate by week
events_per_week_avg = (
    ocorrencias.groupby('week_of_year')
    .size()
    .reset_index(name='count')
    .sort_values('week_of_year')
)

# Create visualization
fig, ax = plt.subplots(figsize=(12, 6))

sns.lineplot(
    data=events_per_week_avg,
    x='week_of_year',
    y='count',
    marker='o',
    markersize=5,
    linewidth=2,
    color='steelblue',
    ax=ax
)

# Styling
ax.set_title('Average Event Trend by Week of Year', fontsize=16, weight='bold')
ax.set_xlabel('Week of Year', fontsize=12)
ax.set_ylabel('Number of Events', fontsize=12)
ax.grid(True, which='major', linestyle='--', linewidth=0.5)
ax.set_xlim(0, 53)
ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True, nbins=13))
ax.tick_params(axis='x', labelsize=10)
ax.tick_params(axis='y', labelsize=10)

# Save
plt.tight_layout()
plt.savefig(f'{output_directory}/chart_04_weekly_average_trend.png', dpi=300, bbox_inches='tight')
print(f"Chart saved to {output_directory}/chart_04_weekly_average_trend.png")
plt.close()
