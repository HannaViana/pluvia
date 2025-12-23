"""
Chart 6: Event Duration Distribution Analysis
Split into two images:
- Image 1: Histogram and CDF (panels a and b)
- Image 2: Duration by hour of day (panel c)
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
    
    # Filter out invalid durations (negative or extremely long)
    ocorrencias = ocorrencias[
        (ocorrencias['duration_hours'] >= 0) & 
        (ocorrencias['duration_hours'] <= 72)  # Max 72 hours (3 days)
    ].copy()
    
    return ocorrencias

def calculate_duration_stats(ocorrencias):
    """Calculate comprehensive duration statistics"""
    durations = ocorrencias['duration_hours'].dropna()
    
    stats_dict = {
        'mean': durations.mean(),
        'median': durations.median(),
        'std': durations.std(),
        'min': durations.min(),
        'max': durations.max(),
        'q25': durations.quantile(0.25),
        'q75': durations.quantile(0.75),
        'q90': durations.quantile(0.90),
        'count': len(durations)
    }
    
    return stats_dict, durations

def create_duration_distribution_chart_part1(ocorrencias, stats_dict, durations):
    """Create first chart: Histogram and CDF (panels a and b) - filtered to <12h"""
    setup_plot_style()
    
    # Filter durations to only show events < 12 hours for panels a and b
    durations_filtered = durations[durations < 12]
    total_events = len(durations)
    filtered_events = len(durations_filtered)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGURE_SIZES['double'])
    fig.suptitle(f'Urban Flood Event Duration Distribution (< 12 hours)\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'], fontweight='bold', y=1.02)
    
    # Panel A: Histogram with statistics
    n, bins, patches = ax1.hist(durations_filtered, bins=50, color=COLORS['primary'],
                                edgecolor='black', linewidth=0.5, alpha=0.7)
    
    # Add vertical lines for statistics
    ax1.axvline(stats_dict['mean'], color=COLORS['secondary'], linestyle='--', 
               linewidth=2, label=f"Mean: {stats_dict['mean']:.2f}h")
    ax1.axvline(stats_dict['median'], color=COLORS['tertiary'], linestyle='--', 
               linewidth=2, label=f"Median: {stats_dict['median']:.2f}h")
    ax1.axvline(stats_dict['q90'], color=COLORS['quaternary'], linestyle=':', 
               linewidth=2, label=f"90th percentile: {stats_dict['q90']:.2f}h")
    
    ax1.set_xlabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_ylabel('Frequency', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_title('Duration Distribution', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax1.legend(loc='upper right', fontsize=FONT_SIZES['legend'])
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    ax1.set_axisbelow(True)
    add_subfigure_label(ax1, '(a)')
    
    # Panel B: Cumulative Distribution Function (CDF)
    sorted_durations = np.sort(durations_filtered)
    cumulative = np.arange(1, len(sorted_durations) + 1) / len(sorted_durations) * 100
    
    ax2.plot(sorted_durations, cumulative, color=COLORS['primary'], linewidth=2)
    ax2.fill_between(sorted_durations, 0, cumulative, color=COLORS['primary'], alpha=0.2)
    
    # Add reference lines
    ax2.axhline(50, color=COLORS['tertiary'], linestyle='--', linewidth=1, alpha=0.5)
    ax2.axhline(90, color=COLORS['quaternary'], linestyle=':', linewidth=1, alpha=0.5)
    ax2.axvline(stats_dict['median'], color=COLORS['tertiary'], linestyle='--', linewidth=1, alpha=0.5)
    ax2.axvline(stats_dict['q90'], color=COLORS['quaternary'], linestyle=':', linewidth=1, alpha=0.5)
    
    # Add annotations
    ax2.text(stats_dict['median'], 50, f" {stats_dict['median']:.2f}h", 
            fontsize=FONT_SIZES['annotation'], verticalalignment='bottom', 
            color=COLORS['tertiary'])
    ax2.text(stats_dict['q90'], 90, f" {stats_dict['q90']:.2f}h", 
            fontsize=FONT_SIZES['annotation'], verticalalignment='bottom',
            color=COLORS['quaternary'])
    
    ax2.set_xlabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_ylabel('Cumulative Percentage (%)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_title('Cumulative Distribution', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax2.grid(True, linestyle='--', alpha=0.3)
    ax2.set_axisbelow(True)
    ax2.set_ylim(0, 100)
    add_subfigure_label(ax2, '(b)')
    
    # Add statistics box
    stats_text = (f"Mean: {stats_dict['mean']:.2f}h\n"
                 f"Median: {stats_dict['median']:.2f}h\n"
                 f"Std Dev: {stats_dict['std']:.2f}h\n"
                 f"Range: {stats_dict['min']:.2f}h - {stats_dict['max']:.2f}h")
    ax2.text(0.98, 0.25, stats_text, transform=ax2.transAxes, 
            fontsize=FONT_SIZES['annotation'],
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, edgecolor='gray'))
    
    # Add sample size annotation showing filtered vs total
    sample_text = f'N = {filtered_events:,} (< 12h)\nTotal: {total_events:,}'
    ax2.text(0.98, 0.98, sample_text,
            transform=ax2.transAxes,
            fontsize=FONT_SIZES['annotation'],
            verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray'))
    
    plt.tight_layout()
    
    return fig

def create_duration_distribution_chart_part2(ocorrencias, stats_dict):
    """Create second chart: Duration by Hour of Day"""
    setup_plot_style()
    
    # Calculate hourly duration statistics
    ocorrencias['hour'] = ocorrencias['data_inicio'].dt.hour
    hourly_duration = ocorrencias.groupby('hour')['duration_hours'].agg(['mean', 'std', 'count'])
    hourly_duration['sem'] = hourly_duration['std'] / np.sqrt(hourly_duration['count'])
    
    fig, ax = plt.subplots(figsize=FIGURE_SIZES['wide'])
    
    ax.bar(hourly_duration.index, hourly_duration['mean'], 
           color=COLORS['primary'], edgecolor='black', linewidth=0.5, alpha=0.7,
           yerr=hourly_duration['sem'], capsize=3, error_kw={'linewidth': 1, 'alpha': 0.5})
    
    # Add mean line
    overall_mean = stats_dict['mean']
    ax.axhline(overall_mean, color=COLORS['secondary'], linestyle='--', 
               linewidth=1.5, label=f'Overall Mean: {overall_mean:.2f}h', alpha=0.7)
    
    ax.set_xlabel('Hour of Day', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax.set_ylabel('Average Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax.set_title(f'Average Event Duration by Hour of Day\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'], fontweight='bold', pad=15)
    ax.set_xticks(range(0, 24, 2))
    ax.set_xticklabels([f'{h:02d}:00' for h in range(0, 24, 2)])
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)
    ax.legend(loc='upper right', fontsize=FONT_SIZES['legend'])
    
    add_sample_size_annotation(ax, len(ocorrencias))
    
    plt.tight_layout()
    
    return fig

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias = load_and_prepare_data()
    print(f"Total flood events with valid duration: {len(ocorrencias)}")
    
    print("\nCalculating duration statistics...")
    stats_dict, durations = calculate_duration_stats(ocorrencias)
    
    print("\nDuration Statistics:")
    print(f"  Mean: {stats_dict['mean']:.2f} hours")
    print(f"  Median: {stats_dict['median']:.2f} hours")
    print(f"  Std Dev: {stats_dict['std']:.2f} hours")
    print(f"  Min: {stats_dict['min']:.2f} hours")
    print(f"  Max: {stats_dict['max']:.2f} hours")
    print(f"  25th percentile: {stats_dict['q25']:.2f} hours")
    print(f"  75th percentile: {stats_dict['q75']:.2f} hours")
    print(f"  90th percentile: {stats_dict['q90']:.2f} hours")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Create and save first chart (histogram and CDF)
    print("\nCreating duration distribution chart (Part 1: Histogram & CDF)...")
    fig1 = create_duration_distribution_chart_part1(ocorrencias, stats_dict, durations)
    output_path1 = f'{OUTPUT_DIR}/chart_06a_duration_distribution.png'
    fig1.savefig(output_path1, dpi=300, bbox_inches='tight')
    print(f"Chart saved to {output_path1}")
    plt.close()
    
    # Create and save second chart (hourly duration)
    print("\nCreating duration distribution chart (Part 2: Hourly Duration)...")
    fig2 = create_duration_distribution_chart_part2(ocorrencias, stats_dict)
    output_path2 = f'{OUTPUT_DIR}/chart_06b_duration_by_hour.png'
    fig2.savefig(output_path2, dpi=300, bbox_inches='tight')
    print(f"Chart saved to {output_path2}")
    plt.close()
    
    print("\nBoth charts created successfully!")

if __name__ == '__main__':
    main()
