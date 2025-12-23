"""
Chart 9: Event Duration Distribution by Type
Based on Chart 6a - generates two charts:
1. Combined chart for Flood Type I and Flood Type II
2. Single chart for Flood Type III
Each chart shows histogram and CDF for events < 12 hours
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

def calculate_duration_stats(durations):
    """Calculate comprehensive duration statistics"""
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
    
    return stats_dict

def create_duration_distribution_chart_by_type(ocorrencias_type, event_types_list, chart_title):
    """Create histogram and CDF chart for one or more event types (< 12 hours)"""
    setup_plot_style()
    
    # Get durations for this event type(s)
    durations = ocorrencias_type['duration_hours'].dropna()
    
    # Filter durations to only show events < 12 hours
    durations_filtered = durations[durations < 12]
    total_events = len(durations)
    filtered_events = len(durations_filtered)
    
    # Calculate statistics from ALL data (for reference)
    stats_dict_all = calculate_duration_stats(durations)
    
    # Calculate statistics from FILTERED data (< 12h) for display on chart
    stats_dict = calculate_duration_stats(durations_filtered)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGURE_SIZES['double'])
    fig.suptitle(f'Duration Distribution for {chart_title} (< 12 hours)\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'], fontweight='bold', y=1.02)
    
    # Panel A: Histogram with statistics
    n, bins, patches = ax1.hist(durations_filtered, bins=24, color=COLORS['primary'],
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
    
    # Add statistics box (using ALL data for context)
    stats_text = (f"All data:\n"
                 f"Mean: {stats_dict_all['mean']:.2f}h\n"
                 f"Median: {stats_dict_all['median']:.2f}h\n"
                 f"90th pct: {stats_dict_all['q90']:.2f}h")
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
    
    return fig, stats_dict

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias = load_and_prepare_data()
    print(f"Total flood events with valid duration: {len(ocorrencias)}")
    
    # Get unique event types
    event_types = ocorrencias['tipo'].value_counts().index.tolist()
    print(f"\nEvent types found: {event_types}")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Define chart groups (using generic names)
    chart_groups = [
        {
            'types': ['Flood Type I', 'Flood Type II'],
            'title': 'Flood Type I and Flood Type II Events',
            'filename': 'bolsao_and_lamina'
        },
        {
            'types': ['Flood Type III'],
            'title': 'Flood Type III Events',
            'filename': 'alagamento'
        }
    ]
    
    # Create a chart for each group
    for group in chart_groups:
        print(f"\n{'='*70}")
        print(f"Processing: {group['title']}")
        print(f"{'='*70}")
        
        # Filter data for this group
        ocorrencias_group = ocorrencias[ocorrencias['tipo'].isin(group['types'])].copy()
        n_events = len(ocorrencias_group)
        
        print(f"Events for this group: {n_events}")
        print(f"  Event types included: {group['types']}")
        
        if n_events == 0:
            print(f"Skipping {group['title']} - no events found")
            continue
        
        # Create chart
        print(f"Creating duration distribution chart for {group['title']}...")
        fig, stats_dict = create_duration_distribution_chart_by_type(
            ocorrencias_group, group['types'], group['title']
        )
        
        print("\nDuration Statistics (< 12h filtered):")
        print(f"  Mean: {stats_dict['mean']:.2f} hours")
        print(f"  Median: {stats_dict['median']:.2f} hours")
        print(f"  Std Dev: {stats_dict['std']:.2f} hours")
        print(f"  Min: {stats_dict['min']:.2f} hours")
        print(f"  Max: {stats_dict['max']:.2f} hours")
        print(f"  90th percentile: {stats_dict['q90']:.2f} hours")
        
        # Save chart
        output_path = f'{OUTPUT_DIR}/chart_09_duration_distribution_{group["filename"]}.png'
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Chart saved to {output_path}")
        plt.close()
    
    print(f"\n{'='*70}")
    print("All charts created successfully!")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()
