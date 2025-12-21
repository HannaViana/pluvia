"""
Chart 7: Event Duration by Type and Season
Comparative analysis of flood event durations across different event types and seasons
Includes box plots and statistical comparisons
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
                    STUDY_PERIOD, STUDY_LOCATION, add_sample_size_annotation,
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

def perform_statistical_tests(ocorrencias):
    """Perform statistical tests comparing durations across groups"""
    # Kruskal-Wallis test for event types (non-parametric ANOVA)
    event_types = ocorrencias['tipo'].unique()
    groups = [ocorrencias[ocorrencias['tipo'] == t]['duration_hours'].dropna() 
              for t in event_types]
    h_stat, p_value = stats.kruskal(*groups)
    
    return h_stat, p_value

def create_duration_by_type_chart(ocorrencias):
    """Create comparative duration analysis chart"""
    setup_plot_style()
    
    # Add season information
    ocorrencias['season'] = ocorrencias['data_inicio'].apply(get_season)
    
    # Perform statistical tests
    h_stat, p_value = perform_statistical_tests(ocorrencias)
    
    # Create 2x2 subplot grid
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'Flood Event Duration by Type and Season\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'] + 2, fontweight='bold', y=0.995)
    
    # Panel A: Box plot by event type
    ax1 = axes[0, 0]
    event_types = ocorrencias['tipo'].value_counts().index.tolist()
    data_by_type = [ocorrencias[ocorrencias['tipo'] == t]['duration_hours'].dropna() 
                    for t in event_types]
    
    bp1 = ax1.boxplot(data_by_type, labels=event_types, patch_artist=True,
                      showmeans=True, meanline=True,
                      boxprops=dict(facecolor=COLORS['primary'], alpha=0.7),
                      medianprops=dict(color='red', linewidth=2),
                      meanprops=dict(color='blue', linewidth=2, linestyle='--'))
    
    ax1.set_ylabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_title('Duration by Event Type', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax1.set_xticklabels(event_types, rotation=45, ha='right')
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    ax1.set_axisbelow(True)
    add_subfigure_label(ax1, '(a)', x=-0.15, y=1.08)
    
    # Add sample sizes
    for i, event_type in enumerate(event_types):
        n = len(ocorrencias[ocorrencias['tipo'] == event_type])
        ax1.text(i+1, ax1.get_ylim()[1] * 0.95, f'n={n}', 
                ha='center', fontsize=FONT_SIZES['annotation'])
    
    # Add statistical test result
    sig_text = f"Kruskal-Wallis: H={h_stat:.2f}, p={'<0.001' if p_value < 0.001 else f'={p_value:.3f}'}"
    ax1.text(0.02, 0.98, sig_text, transform=ax1.transAxes,
            fontsize=FONT_SIZES['annotation'], verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, edgecolor='gray'))
    
    # Panel B: Box plot by season
    ax2 = axes[0, 1]
    season_order = ['Summer', 'Autumn', 'Winter', 'Spring']
    data_by_season = [ocorrencias[ocorrencias['season'] == s]['duration_hours'].dropna() 
                      for s in season_order]
    season_colors = [COLORS['seasons'][s] for s in season_order]
    
    bp2 = ax2.boxplot(data_by_season, labels=season_order, patch_artist=True,
                      showmeans=True, meanline=True,
                      medianprops=dict(color='red', linewidth=2),
                      meanprops=dict(color='blue', linewidth=2, linestyle='--'))
    
    for patch, color in zip(bp2['boxes'], season_colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax2.set_ylabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_title('Duration by Season', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax2.grid(axis='y', linestyle='--', alpha=0.3)
    ax2.set_axisbelow(True)
    add_subfigure_label(ax2, '(b)', x=-0.15, y=1.08)
    
    # Add sample sizes
    for i, season in enumerate(season_order):
        n = len(ocorrencias[ocorrencias['season'] == season])
        ax2.text(i+1, ax2.get_ylim()[1] * 0.95, f'n={n}', 
                ha='center', fontsize=FONT_SIZES['annotation'])
    
    # Panel C: Mean duration by event type with error bars
    ax3 = axes[1, 0]
    type_stats = ocorrencias.groupby('tipo')['duration_hours'].agg(['mean', 'std', 'count', 'sem'])
    type_stats = type_stats.sort_values('mean', ascending=False)
    
    bars = ax3.barh(range(len(type_stats)), type_stats['mean'],
                    xerr=type_stats['sem'], capsize=5,
                    color=COLORS['categorical'][:len(type_stats)],
                    edgecolor='black', linewidth=0.5, alpha=0.7)
    
    ax3.set_yticks(range(len(type_stats)))
    ax3.set_yticklabels(type_stats.index)
    ax3.set_xlabel('Mean Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax3.set_title('Mean Duration by Event Type', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax3.grid(axis='x', linestyle='--', alpha=0.3)
    ax3.set_axisbelow(True)
    add_subfigure_label(ax3, '(c)', x=-0.15, y=1.08)
    
    # Add value labels
    for i, (mean, sem) in enumerate(zip(type_stats['mean'], type_stats['sem'])):
        ax3.text(mean + sem + 0.1, i, f'{mean:.2f}h', 
                va='center', fontsize=FONT_SIZES['annotation'])
    
    # Panel D: Duration distribution by season (violin plot)
    ax4 = axes[1, 1]
    
    # Prepare data for violin plot
    season_data = []
    season_positions = []
    for i, season in enumerate(season_order):
        data = ocorrencias[ocorrencias['season'] == season]['duration_hours'].dropna()
        if len(data) > 0:
            season_data.append(data)
            season_positions.append(i + 1)
    
    parts = ax4.violinplot(season_data, positions=season_positions, 
                           showmeans=True, showmedians=True, widths=0.7)
    
    # Color the violin plots
    for i, pc in enumerate(parts['bodies']):
        pc.set_facecolor(season_colors[i])
        pc.set_alpha(0.7)
    
    ax4.set_xticks(range(1, len(season_order) + 1))
    ax4.set_xticklabels(season_order)
    ax4.set_ylabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax4.set_title('Duration Distribution by Season', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax4.grid(axis='y', linestyle='--', alpha=0.3)
    ax4.set_axisbelow(True)
    add_subfigure_label(ax4, '(d)', x=-0.15, y=1.08)
    
    add_sample_size_annotation(ax4, len(ocorrencias))
    
    plt.tight_layout(rect=[0, 0, 1, 0.99])
    
    return fig, type_stats, h_stat, p_value

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias = load_and_prepare_data()
    print(f"Total flood events with valid duration: {len(ocorrencias)}")
    
    print("\nCreating duration by type and season chart...")
    fig, type_stats, h_stat, p_value = create_duration_by_type_chart(ocorrencias)
    
    print("\nDuration Statistics by Event Type:")
    print(type_stats[['mean', 'std', 'count']])
    print(f"\nKruskal-Wallis Test: H = {h_stat:.2f}, p = {p_value:.6f}")
    
    # Season statistics
    ocorrencias['season'] = ocorrencias['data_inicio'].apply(get_season)
    season_stats = ocorrencias.groupby('season')['duration_hours'].agg(['mean', 'std', 'count'])
    print("\nDuration Statistics by Season:")
    print(season_stats)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = f'{OUTPUT_DIR}/chart_07_duration_by_type.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nChart saved to {output_path}")
    plt.close()

if __name__ == '__main__':
    main()
