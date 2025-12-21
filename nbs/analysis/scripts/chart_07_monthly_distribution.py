"""
Chart 7: Distribuição Mensal dos Eventos
Source: temporal.py lines 917-934
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

# Extract month
ocorrencias['month'] = ocorrencias['data_inicio'].dt.month_name()

# Month order
month_order_en = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
month_names_en = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Aggregate by month
monthly_distribution = ocorrencias['month'].value_counts()
monthly_distribution = monthly_distribution.reindex(month_order_en)

# Create visualization
plt.figure(figsize=(12, 6))

ax3 = sns.barplot(x=month_names_en, y=monthly_distribution.values, color='steelblue')
ax3.set_title('Monthly Distribution of Events', fontsize=14, weight='bold')
ax3.set_xlabel('Month', fontsize=12)
ax3.set_ylabel('Number of Events', fontsize=12)
plt.xticks(rotation=45, ha='right')
ax3.tick_params(axis='x', labelsize=10)
ax3.tick_params(axis='y', labelsize=10)

# Save
plt.tight_layout()
plt.savefig(f'{output_directory}/chart_07_monthly_distribution.png', dpi=300, bbox_inches='tight')
print(f"Chart saved to {output_directory}/chart_07_monthly_distribution.png")
plt.close()
