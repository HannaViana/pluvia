"""
Chart 2: Temporal Patterns of Flood Events
Combines monthly and seasonal analysis with statistical information
Multi-panel figure with confidence intervals
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import os
import sys

# Add parent directory to path for config import
sys.path.insert(0, os.path.dirname(__file__))
from config import (setup_plot_style, COLORS, FONT_SIZES, FIGURE_SIZES,
                    DATA_PATHS, OUTPUT_DIR, FLOOD_TYPES, EVENT_TYPE_MAPPING,
                    GENERIC_TYPE_MAPPING, STUDY_PERIOD, STUDY_LOCATION, add_sample_size_annotation,
                    add_subfigure_label, ALPHA)

def load_and_prepare_data():
    """Load and preprocess flood event data"""
    ocorrencias = pd.read_csv(DATA_PATHS['ocorrencias'])
    pops = pd.read_csv(DATA_PATHS['pops'], index_col=0)
    
    ocorrencias['data_inicio'] = pd.to_datetime(ocorrencias['data_inicio'])
    ocorrencias['data_fim'] = pd.to_datetime(ocorrencias['data_fim'])
    ocorrencias['tipo'] = ocorrencias['id_pop'].map(pops.set_index('id')['titulo'])
    
    ocorrencias = ocorrencias[ocorrencias['tipo'].isin(FLOOD_TYPES)]
    ocorrencias['tipo'] = ocorrencias['tipo'].replace(EVENT_TYPE_MAPPING)
    ocorrencias['tipo'] = ocorrencias['tipo'].replace(GENERIC_TYPE_MAPPING)
    
    return ocorrencias

def get_season(date):
    """Assign season based on month (Southern Hemisphere)"""
    month = date.month
    if month in [12, 1, 2]:
        return 'Summer'
    elif month in [3, 4, 5]:
        return 'Autumn'
    elif month in [6, 7, 8]:
        return 'Winter'
    else:
        return 'Spring'

def calculate_monthly_stats(ocorrencias):
    """Calculate monthly statistics with confidence intervals"""
    ocorrencias['year'] = ocorrencias['data_inicio'].dt.year
    ocorrencias['month'] = ocorrencias['data_inicio'].dt.month
    
    monthly_counts = ocorrencias.groupby(['year', 'month']).size().reset_index(name='count')
    monthly_stats = monthly_counts.groupby('month')['count'].agg(['mean', 'std', 'count', 'sem']).reset_index()
    
    confidence = 0.95
    monthly_stats['ci'] = monthly_stats['sem'] * stats.t.ppf((1 + confidence) / 2, monthly_stats['count'] - 1)
    monthly_stats['ci_lower'] = (monthly_stats['mean'] - monthly_stats['ci']).clip(lower=0)
    monthly_stats['ci_upper'] = monthly_stats['mean'] + monthly_stats['ci']
    
    return monthly_stats

def calculate_seasonal_stats(ocorrencias):
    """Calculate seasonal statistics with chi-square test"""
    ocorrencias['season'] = ocorrencias['data_inicio'].apply(get_season)
    season_counts = ocorrencias['season'].value_counts()
    season_order = ['Summer', 'Autumn', 'Winter', 'Spring']
    season_counts = season_counts.reindex(season_order)
    
    expected = len(ocorrencias) / 4
    chi2, p_value = stats.chisquare(season_counts.values, f_exp=[expected] * 4)
    
    return season_counts, chi2, p_value

def create_temporal_patterns_chart(ocorrencias):
    """Create multi-panel temporal analysis chart"""
    setup_plot_style()
    
    monthly_stats = calculate_monthly_stats(ocorrencias)
    season_counts, chi2, p_value = calculate_seasonal_stats(ocorrencias)
    
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_stats['month_name'] = monthly_stats['month'].apply(lambda x: month_names[x-1])
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGURE_SIZES['double'])
    fig.suptitle(f'Temporal Patterns of Urban Flood Events\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'], fontweight='bold', y=1.02)
    
    # Panel A: Monthly distribution
    ax1.plot(monthly_stats['month_name'], monthly_stats['mean'],
            marker='o', linestyle='-', color=COLORS['primary'], linewidth=2, markersize=6, label='Mean')
    ax1.fill_between(range(len(monthly_stats)), monthly_stats['ci_lower'], monthly_stats['ci_upper'],
                     color=COLORS['primary'], alpha=0.2, label='95% CI')
    
    ax1.set_xlabel('Month', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_ylabel('Average Number of Events', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_title('Monthly Distribution', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax1.grid(True, linestyle='--', alpha=0.3)
    ax1.legend(loc='upper left', fontsize=FONT_SIZES['legend'])
    ax1.set_axisbelow(True)
    add_subfigure_label(ax1, '(a)')
    
    # Panel B: Seasonal distribution
    season_order = ['Summer', 'Autumn', 'Winter', 'Spring']
    season_colors = [COLORS['seasons'][s] for s in season_order]
    
    bars = ax2.bar(season_order, season_counts.values, color=season_colors, edgecolor='black', linewidth=0.5)
    
    for bar, count in zip(bars, season_counts.values):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height, f'{int(count):,}',
                ha='center', va='bottom', fontsize=FONT_SIZES['annotation'])
    
    ax2.set_xlabel('Season', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_ylabel('Number of Events', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_title('Seasonal Distribution', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax2.grid(axis='y', linestyle='--', alpha=0.3)
    ax2.set_axisbelow(True)
    
    add_subfigure_label(ax2, '(b)')
    add_sample_size_annotation(ax2, len(ocorrencias))
    
    plt.tight_layout()
    return fig, monthly_stats, season_counts, chi2, p_value

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias = load_and_prepare_data()
    print(f"Total flood events: {len(ocorrencias)}")
    
    print("\nCreating temporal patterns chart...")
    fig, monthly_stats, season_counts, chi2, p_value = create_temporal_patterns_chart(ocorrencias)
    
    print("\nMonthly statistics:")
    print(monthly_stats[['month_name', 'mean', 'std', 'ci_lower', 'ci_upper']])
    print("\nSeasonal distribution:")
    print(season_counts)
    print(f"\nChi-square test: χ² = {chi2:.2f}, p = {p_value:.4f}")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = f'{OUTPUT_DIR}/chart_02_temporal_patterns.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nChart saved to {output_path}")
    plt.close()

if __name__ == '__main__':
    main()
