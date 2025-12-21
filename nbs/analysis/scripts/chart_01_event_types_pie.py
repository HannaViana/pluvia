"""
Chart 1: Pie Chart - Percentage Share of Event Types
Source: preliminary.py lines 332-360
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

# Calculate event type counts
event_type_counts = ocorrencias['tipo'].value_counts().to_frame()

# Create visualization
labels = event_type_counts.index
sizes = event_type_counts['count'].values
colors = plt.cm.viridis([0.2, 0.6, 0.9])

fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(
    sizes, 
    autopct='%1.1f%%', 
    pctdistance=0.8, 
    startangle=90, 
    colors=colors,
    wedgeprops=dict(width=0.4, edgecolor='w')
)

# Legend and title
ax.legend(
    wedges, 
    labels,
    title="Event Type",
    loc="center left",
    fontsize=12,
    bbox_to_anchor=(1, 0, 0.5, 1)
)

plt.setp(autotexts, size=10, weight="bold", color="white")
ax.set_title("Percentage Distribution of Event Types", fontsize=14, weight='bold')
ax.axis('equal')

# Save
plt.tight_layout()
plt.savefig(f'{output_directory}/chart_01_event_types_pie.png', dpi=300, bbox_inches='tight')
print(f"Chart saved to {output_directory}/chart_01_event_types_pie.png")
plt.close()
