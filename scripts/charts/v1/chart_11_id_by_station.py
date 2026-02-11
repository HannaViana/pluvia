"""
Chart 11: Intensity-Duration (I-D) Analysis by Station
Creates individual I-D scatter plots for each rain gauge station
Shows EA (with flooding) vs ESA (without flooding) classification
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

# Add parent directory to path for config import
sys.path.insert(0, os.path.dirname(__file__))
from config import (setup_plot_style, COLORS, FONT_SIZES, FIGURE_SIZES,
                    OUTPUT_DIR, STUDY_PERIOD, STUDY_LOCATION)

# Data paths
ID_ANALYSIS_DIR = 'data/processed/id_analysis'
PONTOS_ID_PATH = f'{ID_ANALYSIS_DIR}/pontos_id_df.csv'
CLASSIFICATION_SUMMARY_PATH = f'{ID_ANALYSIS_DIR}/classification_summary.csv'

# Duration windows used in analysis (in minutes)
DURATIONS_MIN = [15, 30, 60, 120, 180, 720]

# Chart colors and styling
COLORS_ID = {
    'ESA': '#4393c3',  # Blue - no flooding
    'EA': '#d6604d'     # Red - with flooding
}

MARKER_SIZES = {
    'ESA': 20,
    'EA': 50
}

MARKER_ALPHA = {
    'ESA': 0.5,
    'EA': 0.9
}

ZORDER = {
    'ESA': 1,
    'EA': 2
}

def load_data():
    """Load I-D analysis data"""
    print(f"Loading I-D points from {PONTOS_ID_PATH}...")
    pontos_id_df = pd.read_csv(PONTOS_ID_PATH)

    print(f"Loading classification summary from {CLASSIFICATION_SUMMARY_PATH}...")
    classification_summary = pd.read_csv(CLASSIFICATION_SUMMARY_PATH, index_col=0)

    # Convert timestamps
    pontos_id_df['start_time'] = pd.to_datetime(pontos_id_df['start_time'])
    pontos_id_df['end_time'] = pd.to_datetime(pontos_id_df['end_time'])

    return pontos_id_df, classification_summary

def create_id_chart_for_station(station_id, station_data, ea_count, esa_count):
    """Create I-D scatter plot for a single station"""
    setup_plot_style()

    fig, ax = plt.subplots(figsize=FIGURE_SIZES['single'])

    # Filter data by classification
    esa_data = station_data[station_data['classificacao'] == 'ESA']
    ea_data = station_data[station_data['classificacao'] == 'EA']

    # Plot ESA (no flooding) first - background layer
    if not esa_data.empty:
        ax.scatter(esa_data['duracao_h'], esa_data['intensidade_max_mm_h'],
                  color=COLORS_ID['ESA'],
                  s=MARKER_SIZES['ESA'],
                  alpha=MARKER_ALPHA['ESA'],
                  zorder=ZORDER['ESA'],
                  label=f'No Flooding (ESA, n={len(esa_data)})',
                  edgecolor='none')

    # Plot EA (with flooding) on top - foreground layer for emphasis
    if not ea_data.empty:
        ax.scatter(ea_data['duracao_h'], ea_data['intensidade_max_mm_h'],
                  color=COLORS_ID['EA'],
                  s=MARKER_SIZES['EA'],
                  alpha=MARKER_ALPHA['EA'],
                  zorder=ZORDER['EA'],
                  label=f'With Flooding (EA, n={len(ea_data)})',
                  edgecolor='black',
                  linewidth=0.5)

    # Set log scales
    ax.set_xscale('log')
    ax.set_yscale('log')

    # Configure x-axis ticks with custom labels
    x_tick_positions = [d/60 for d in DURATIONS_MIN]
    x_tick_labels = []
    for d in DURATIONS_MIN:
        if d < 60:
            x_tick_labels.append(f'{d}min')
        else:
            hours = d // 60
            x_tick_labels.append(f'{hours}h')

    ax.set_xticks(x_tick_positions)
    ax.set_xticklabels(x_tick_labels, fontsize=FONT_SIZES['tick_label'])

    # Labels and title
    ax.set_xlabel('Duration', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax.set_ylabel('Maximum Intensity (mm/h)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax.set_title(f'Intensity-Duration Classification\nStation {station_id}',
                fontsize=FONT_SIZES['title'], fontweight='bold', pad=15)

    # Grid
    ax.grid(True, which="both", linestyle='--', alpha=0.4, linewidth=0.5)
    ax.set_axisbelow(True)

    # Legend
    legend = ax.legend(loc='upper right', fontsize=FONT_SIZES['legend'],
                      frameon=True, fancybox=True, shadow=False)
    legend.get_frame().set_alpha(0.9)
    legend.get_frame().set_edgecolor('gray')
    legend.get_frame().set_linewidth(0.5)

    # Add station statistics annotation
    stats_text = f'EA Events: {ea_count}\nESA Events: {esa_count}\nTotal: {ea_count + esa_count}'
    ax.text(0.02, 0.02, stats_text,
            transform=ax.transAxes,
            fontsize=FONT_SIZES['annotation'],
            verticalalignment='bottom',
            horizontalalignment='left',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9,
                     edgecolor='gray', linewidth=0.5))

    plt.tight_layout()

    return fig

def main():
    """Main execution function"""
    print("="*70)
    print("CHART 11: INTENSITY-DURATION ANALYSIS BY STATION")
    print("="*70)

    # Load data
    print("\nLoading data...")
    pontos_id_df, classification_summary = load_data()

    print(f"\nTotal I-D points: {len(pontos_id_df):,}")
    print(f"Total stations: {len(classification_summary)}")
    print(f"Stations with EA events: {(classification_summary['EA'] > 0).sum()}")

    # Sort stations by number of EA events (descending)
    station_ids_to_plot = classification_summary.sort_values(by='EA', ascending=False).index.astype(int)

    # Create output directory for this chart
    chart_output_dir = f'{OUTPUT_DIR}/chart_11_id_by_station'
    os.makedirs(chart_output_dir, exist_ok=True)
    print(f"\nOutput directory: {chart_output_dir}")

    # Generate chart for each station
    print(f"\nGenerating charts for {len(station_ids_to_plot)} stations...")

    successful = 0
    failed = 0

    for idx, station_id in enumerate(station_ids_to_plot, 1):
        try:
            # Get data for this station
            station_data = pontos_id_df[pontos_id_df['id_estacao'] == station_id]

            if station_data.empty:
                print(f"  [{idx}/{len(station_ids_to_plot)}] Station {station_id}: No data, skipping")
                continue

            # Get event counts from classification summary
            ea_count = int(classification_summary.loc[station_id, 'EA'])
            esa_count = int(classification_summary.loc[station_id, 'ESA'])

            # Create chart
            fig = create_id_chart_for_station(station_id, station_data, ea_count, esa_count)

            # Save with station ID in filename (zero-padded for sorting)
            output_path = f'{chart_output_dir}/station_{station_id:02d}.png'
            fig.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close(fig)

            successful += 1
            print(f"  [{idx}/{len(station_ids_to_plot)}] Station {station_id}: ✓ Saved (EA={ea_count}, ESA={esa_count})")

        except Exception as e:
            failed += 1
            print(f"  [{idx}/{len(station_ids_to_plot)}] Station {station_id}: ✗ Failed - {str(e)}")

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Successfully generated: {successful} charts")
    print(f"Failed: {failed} charts")
    print(f"Output directory: {chart_output_dir}")
    print("="*70)

    if failed == 0:
        print("\n✓ All station charts generated successfully!")
    else:
        print(f"\n⚠ {failed} chart(s) failed to generate")

if __name__ == '__main__':
    main()
