"""
Chart 3: Tendência Média Mensal de Eventos com Variância
Source: temporal.py lines 564-600
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

# Extract year and month
ocorrencias['year'] = ocorrencias['data_inicio'].dt.year
ocorrencias['month'] = ocorrencias['data_inicio'].dt.month

# Group by year and month
monthly_counts = ocorrencias.groupby(['year', 'month']).size().reset_index(name='count')

# Compute mean and std per month (across years)
monthly_stats = monthly_counts.groupby('month')['count'].agg(['mean', 'std']).reset_index()

# Add bounds for variance band
monthly_stats['upper'] = monthly_stats['mean'] + monthly_stats['std']
monthly_stats['lower'] = monthly_stats['mean'] - monthly_stats['std']

# Month names in English
month_names_en = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthly_stats['month_name'] = monthly_stats['month'].apply(lambda x: month_names_en[x-1])

# Create visualization
fig, ax = plt.subplots(figsize=(11, 6))

# Mean line
ax.plot(monthly_stats['month_name'], monthly_stats['mean'],
        marker='o', linestyle='-', color='steelblue', label='Average Events per Month')

# Variance band (±1 standard deviation)
ax.fill_between(monthly_stats['month_name'], monthly_stats['lower'], monthly_stats['upper'],
                color='steelblue', alpha=0.15, label='Variance (±1 std dev)')

# Styling
ax.set_title('Monthly Average Event Trend with Variance', fontsize=16, weight='bold')
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Number of Events', fontsize=12)
ax.grid(True, which='major', linestyle='--', linewidth=0.5)
ax.legend(loc='upper right', fontsize=12)
ax.tick_params(axis='x', labelsize=10)
ax.tick_params(axis='y', labelsize=10)
plt.xticks(monthly_stats['month_name'])

# Save
plt.tight_layout()
plt.savefig(f'{output_directory}/chart_03_monthly_average_variance.png', dpi=300, bbox_inches='tight')
print(f"Chart saved to {output_directory}/chart_03_monthly_average_variance.png")
plt.close()
