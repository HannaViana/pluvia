"""
Chart 7a: Event Duration by Type (< 12 hours)
Comparative analysis of flood event durations across different event types
Includes box plots and mean duration with error bars
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

def perform_statistical_tests(ocorrencias):
    """Perform statistical tests comparing durations across groups"""
    # Kruskal-Wallis test for event types (non-parametric ANOVA)
    event_types = ocorrencias['tipo'].unique()
    groups = [ocorrencias[ocorrencias['tipo'] == t]['duration_hours'].dropna() 
              for t in event_types]
    h_stat, p_value = stats.kruskal(*groups)
    
    return h_stat, p_value

def create_duration_by_type_chart(ocorrencias):
    """Create comparative duration analysis chart by event type"""
    setup_plot_style()
    
    # Filter to < 12 hours for panel a
    ocorrencias_filtered = ocorrencias[ocorrencias['duration_hours'] < 12].copy()
    total_events = len(ocorrencias)
    filtered_events = len(ocorrencias_filtered)
    
    # Perform statistical tests on filtered data
    h_stat, p_value = perform_statistical_tests(ocorrencias_filtered)
    
    # Create 1x2 subplot grid
    fig, axes = plt.subplots(1, 2, figsize=FIGURE_SIZES['double'])
    fig.suptitle(f'Flood Event Duration by Type\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'], fontweight='bold', y=1.02)
    
    # Panel A: Box plot by event type (< 12 hours)
    ax1 = axes[0]
    event_types = ocorrencias_filtered['tipo'].value_counts().index.tolist()
    event_types = [event_types[1], event_types[0], event_types[2]] + event_types[3:]
    data_by_type = [ocorrencias_filtered[ocorrencias_filtered['tipo'] == t]['duration_hours'].dropna() 
                    for t in event_types]
    
    bp1 = ax1.boxplot(data_by_type, labels=event_types, patch_artist=True,
                      showmeans=True, meanline=True,
                      boxprops=dict(facecolor=COLORS['primary'], alpha=0.7),
                      medianprops=dict(color='red', linewidth=2),
                      meanprops=dict(color='blue', linewidth=2, linestyle='--'))
    
    ax1.set_ylabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_title('Duration by Event Type (< 12h)', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax1.set_xticklabels(event_types, rotation=45, ha='right')
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    ax1.set_axisbelow(True)
    add_subfigure_label(ax1, '(a)')
    
    # Extend y-axis to accommodate text labels at the top
    y_min, y_max = ax1.get_ylim()
    ax1.set_ylim(y_min, y_max * 1.12)
    
    # Add sample sizes
    for i, event_type in enumerate(event_types):
        n = len(ocorrencias_filtered[ocorrencias_filtered['tipo'] == event_type])
        ax1.text(i+1, ax1.get_ylim()[1] * 0.88, f'n={n}',
                ha='center', fontsize=FONT_SIZES['annotation'])
    
    # Add statistical test result
    # sig_text = f"Kruskal-Wallis: H={h_stat:.2f}, p={'<0.001' if p_value < 0.001 else f'={p_value:.3f}'}"
    # ax1.text(0.02, 0.98, sig_text, transform=ax1.transAxes,
    #         fontsize=FONT_SIZES['annotation'], verticalalignment='top',
    #         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, edgecolor='gray'))
    
    # Add filter info
    filter_text = f'Filtered: {filtered_events:,} / {total_events:,}'
    # filter_text = f'N = {filtered_events:,}'
    ax1.text(0.98, 0.98, filter_text, transform=ax1.transAxes,
            fontsize=FONT_SIZES['annotation'], verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray'))
    
    # Panel B: Mean duration by event type with error bars (all data)
    ax2 = axes[1]
    type_stats = ocorrencias.groupby('tipo')['duration_hours'].agg(['mean', 'std', 'count', 'sem'])
    type_stats = type_stats.sort_values('mean', ascending=False)
    
    bars = ax2.barh(range(len(type_stats)), type_stats['mean'],
                    xerr=type_stats['sem'], capsize=5,
                    color=COLORS['categorical'][:len(type_stats)],
                    edgecolor='black', linewidth=0.5, alpha=0.7)
    
    ax2.set_yticks(range(len(type_stats)))
    ax2.set_yticklabels(type_stats.index)
    ax2.set_xlabel('Mean Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_title('Mean Duration by Event Type', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax2.grid(axis='x', linestyle='--', alpha=0.3)
    ax2.set_axisbelow(True)
    add_subfigure_label(ax2, '(b)')
    
    # Calculate max value for x-axis extension
    max_value = (type_stats['mean'] + type_stats['sem']).max()
    ax2.set_xlim(0, max_value * 1.15)  # Add 25% padding for text labels
    
    # Add value labels
    for i, (mean, sem) in enumerate(zip(type_stats['mean'], type_stats['sem'])):
        ax2.text(mean + sem + 0.1, i, f'{mean:.2f}h',
                va='center', fontsize=FONT_SIZES['annotation'])
    
    add_sample_size_annotation(ax2, len(ocorrencias))
    
    plt.tight_layout()
    
    return fig, type_stats, h_stat, p_value

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias = load_and_prepare_data()
    print(f"Total flood events with valid duration: {len(ocorrencias)}")
    
    print("\nCreating duration by type chart...")
    fig, type_stats, h_stat, p_value = create_duration_by_type_chart(ocorrencias)
    
    print("\nDuration Statistics by Event Type:")
    print(type_stats[['mean', 'std', 'count']])
    print(f"\nKruskal-Wallis Test: H = {h_stat:.2f}, p = {p_value:.6f}")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = f'{OUTPUT_DIR}/chart_07a_duration_by_type.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nChart saved to {output_path}")
    plt.close()

if __name__ == '__main__':
    main()
