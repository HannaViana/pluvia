"""
Chart 7b: Event Duration by Season (< 12 hours)
Comparative analysis of flood event durations across different seasons
Includes box plots and violin plots
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from config import (setup_plot_style, COLORS, FONT_SIZES, FIGURE_SIZES,
                    DATA_PATHS, OUTPUT_DIR, FLOOD_TYPES, EVENT_TYPE_MAPPING,
                    GENERIC_TYPE_MAPPING, STUDY_PERIOD, STUDY_LOCATION, add_sample_size_annotation,
                    add_subfigure_label, ALPHA)

def load_and_prepare_data():
    """Load and preprocess flood event data with duration calculation"""
    ocorrencias = pd.read_csv(DATA_PATHS['ocorrencias'])
    pops = pd.read_csv(DATA_PATHS['pops'], index_col=0)
    
    ocorrencias['data_inicio'] = pd.to_datetime(ocorrencias['data_inicio'])
    ocorrencias['data_fim'] = pd.to_datetime(ocorrencias['data_fim'])
    ocorrencias['tipo'] = ocorrencias['id_pop'].map(pops.set_index('id')['titulo'])
    
    ocorrencias = ocorrencias[ocorrencias['tipo'].isin(FLOOD_TYPES)]
    ocorrencias['tipo'] = ocorrencias['tipo'].replace(EVENT_TYPE_MAPPING)
    ocorrencias['tipo'] = ocorrencias['tipo'].replace(GENERIC_TYPE_MAPPING)
    
    # Calculate duration in hours
    ocorrencias['duration_hours'] = (ocorrencias['data_fim'] - ocorrencias['data_inicio']).dt.total_seconds() / 3600
    
    # Filter out invalid durations
    ocorrencias = ocorrencias[
        (ocorrencias['duration_hours'] >= 0) & 
        (ocorrencias['duration_hours'] <= 72)
    ].copy()
    
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

def create_duration_by_season_chart(ocorrencias):
    """Create comparative duration analysis chart by season"""
    setup_plot_style()
    
    # Add season information
    ocorrencias['season'] = ocorrencias['data_inicio'].apply(get_season)
    
    # Filter to < 12 hours for both panels
    ocorrencias_filtered = ocorrencias[ocorrencias['duration_hours'] < 12].copy()
    total_events = len(ocorrencias)
    filtered_events = len(ocorrencias_filtered)
    
    # Create 1x2 subplot grid
    fig, axes = plt.subplots(1, 2, figsize=FIGURE_SIZES['double'])
    fig.suptitle(f'Flood Event Duration by Season (< 12 hours)\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'], fontweight='bold', y=1.02)
    
    season_order = ['Summer', 'Autumn', 'Winter', 'Spring']
    season_colors = [COLORS['seasons'][s] for s in season_order]
    
    # Panel A: Box plot by season (< 12 hours)
    ax1 = axes[0]
    data_by_season = [ocorrencias_filtered[ocorrencias_filtered['season'] == s]['duration_hours'].dropna() 
                      for s in season_order]
    
    bp1 = ax1.boxplot(data_by_season, labels=season_order, patch_artist=True,
                      showmeans=True, meanline=True,
                      medianprops=dict(color='red', linewidth=2),
                      meanprops=dict(color='blue', linewidth=2, linestyle='--'))
    
    for patch, color in zip(bp1['boxes'], season_colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax1.set_ylabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_title('Duration by Season', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    ax1.set_axisbelow(True)
    add_subfigure_label(ax1, '(a)')
    
    # Extend y-axis to accommodate text labels at the top
    y_min, y_max = ax1.get_ylim()
    ax1.set_ylim(y_min, y_max * 1.07)

    # Add sample sizes
    for i, season in enumerate(season_order):
        n = len(ocorrencias_filtered[ocorrencias_filtered['season'] == season])
        ax1.text(i+1, ax1.get_ylim()[1] * 0.91, f'n={n}', 
                ha='center', fontsize=FONT_SIZES['annotation'])
    
    # Add filter info
    filter_text = f'Filtered: {filtered_events:,} / {total_events:,}'
    ax1.text(0.98, 0.98, filter_text, transform=ax1.transAxes,
            fontsize=FONT_SIZES['annotation'], verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray'))
    
    # Panel B: Duration distribution by season (violin plot, < 12 hours)
    ax2 = axes[1]
    
    # Prepare data for violin plot
    season_data = []
    season_positions = []
    for i, season in enumerate(season_order):
        data = ocorrencias_filtered[ocorrencias_filtered['season'] == season]['duration_hours'].dropna()
        if len(data) > 0:
            season_data.append(data)
            season_positions.append(i + 1)
    
    parts = ax2.violinplot(season_data, positions=season_positions, 
                           showmeans=True, showmedians=True, widths=0.7)
    
    # Color the violin plots
    for i, pc in enumerate(parts['bodies']):
        pc.set_facecolor(season_colors[i])
        pc.set_alpha(0.7)
    
    ax2.set_xticks(range(1, len(season_order) + 1))
    ax2.set_xticklabels(season_order)
    ax2.set_ylabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_title('Duration Distribution by Season', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax2.grid(axis='y', linestyle='--', alpha=0.3)
    ax2.set_axisbelow(True)
    add_subfigure_label(ax2, '(b)')
    
    # Extend y-axis to accommodate text labels at the top
    y_min, y_max = ax2.get_ylim()
    ax2.set_ylim(y_min, y_max * 1.07)

    add_sample_size_annotation(ax2, filtered_events)
    
    plt.tight_layout()
    
    # Calculate season statistics for reporting
    season_stats = ocorrencias_filtered.groupby('season')['duration_hours'].agg(['mean', 'std', 'count'])
    
    return fig, season_stats

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias = load_and_prepare_data()
    print(f"Total flood events with valid duration: {len(ocorrencias)}")
    
    print("\nCreating duration by season chart...")
    fig, season_stats = create_duration_by_season_chart(ocorrencias)
    
    print("\nDuration Statistics by Season (< 12 hours):")
    print(season_stats)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = f'{OUTPUT_DIR}/chart_07b_duration_by_season.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nChart saved to {output_path}")
    plt.close()

if __name__ == '__main__':
    main()
