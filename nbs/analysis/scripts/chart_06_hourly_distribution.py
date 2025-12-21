"""
Chart 6: Distribuição Horária dos Eventos
Source: temporal.py lines 882-901
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

# Extract hour
ocorrencias['hour_start'] = ocorrencias['data_inicio'].dt.hour

# Aggregate by hour
hourly_distribution = ocorrencias['hour_start'].value_counts().sort_index()

# Create visualization
plt.figure(figsize=(10, 5))

ax1 = sns.barplot(x=hourly_distribution.index, y=hourly_distribution.values, color='steelblue')
ax1.set_title('Hourly Distribution of Events', fontsize=14, weight='bold')
ax1.set_xlabel('Hour of Day', fontsize=12)
ax1.set_ylabel('Number of Events', fontsize=12)
ax1.tick_params(axis='x', labelsize=10)
ax1.tick_params(axis='y', labelsize=10)

# Save
plt.tight_layout()
plt.savefig(f'{output_directory}/chart_06_hourly_distribution.png', dpi=300, bbox_inches='tight')
print(f"Chart saved to {output_directory}/chart_06_hourly_distribution.png")
plt.close()
