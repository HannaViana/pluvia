"""
Chart 12: Intensity-Duration (I-D) Thresholds by Station
Creates individual I-D scatter plots with fitted threshold curves
Shows EA/ESA classification and the fitted threshold line I = a × D^(-b)
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
THRESHOLDS_PATH = f'{ID_ANALYSIS_DIR}/threshold_parameters.csv'

# Duration windows used in analysis (in minutes)
DURATIONS_MIN = [15, 30, 60, 120, 180, 720]

# Chart colors and styling (referencing project palette from config)
COLORS_ID = {
    'ESA': COLORS['diverging'][1],   # '#4393c3' - Blue, no flooding
    'EA': COLORS['diverging'][-2],   # '#d6604d' - Red, with flooding
    'threshold': '#252525'  # Black - high contrast threshold line
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
    'EA': 2,
    'threshold': 3
}

def load_data():
    """Load I-D analysis data and fitted thresholds"""
    print(f"Loading I-D points from {PONTOS_ID_PATH}...")
    pontos_id_df = pd.read_csv(PONTOS_ID_PATH)

    print(f"Loading thresholds from {THRESHOLDS_PATH}...")
    thresholds_df = pd.read_csv(THRESHOLDS_PATH)

    # Convert timestamps
    pontos_id_df['start_time'] = pd.to_datetime(pontos_id_df['start_time'])
    pontos_id_df['end_time'] = pd.to_datetime(pontos_id_df['end_time'])

    return pontos_id_df, thresholds_df

def create_threshold_chart_for_station(station_id, station_data, threshold_params):
    """Create I-D scatter plot with fitted threshold curve for a single station"""
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
                  label='No Flooding (ESA)',
                  edgecolor='none')

    # Plot EA (with flooding) on top - foreground layer for emphasis
    if not ea_data.empty:
        ax.scatter(ea_data['duracao_h'], ea_data['intensidade_max_mm_h'],
                  color=COLORS_ID['EA'],
                  s=MARKER_SIZES['EA'],
                  alpha=MARKER_ALPHA['EA'],
                  zorder=ZORDER['EA'],
                  label='With Flooding (EA)',
                  edgecolor='black',
                  linewidth=0.5)

    # Plot threshold curve if parameters are valid
    a = threshold_params['a']
    b = threshold_params['b']

    if not np.isnan(a) and not np.isnan(b):
        # Generate smooth curve
        D_range = np.logspace(np.log10(DURATIONS_MIN[0]/60),
                             np.log10(DURATIONS_MIN[-1]/60), 100)
        I_threshold = a * (D_range ** (-b))

        ax.plot(D_range, I_threshold,
               color=COLORS_ID['threshold'],
               linewidth=2,
               linestyle='--',
               zorder=ZORDER['threshold'],
               label='Threshold Curve')

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
    ax.set_title(f'Intensity-Duration Threshold\nStation {station_id}',
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

    # Add threshold equation and metrics annotation
    if not np.isnan(a) and not np.isnan(b):
        precision = threshold_params['precision']
        recall = threshold_params['recall']
        f1 = threshold_params['f1']

        equation_text = f'I = {a:.3f} × D$^{{{-b:.3f}}}$'
        metrics_text = f'P={precision:.2f}, R={recall:.2f}, F1={f1:.2f}'
        annotation_text = f'{equation_text}\n{metrics_text}'
    else:
        annotation_text = 'No threshold\n(insufficient data)'

    ax.text(0.02, 0.98, annotation_text,
            transform=ax.transAxes,
            fontsize=FONT_SIZES['annotation'],
            verticalalignment='top',
            horizontalalignment='left',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9,
                     edgecolor='gray', linewidth=0.5))

    # Add confusion matrix annotation
    tp = int(threshold_params['TP'])
    fp = int(threshold_params['FP'])
    fn = int(threshold_params['FN'])
    tn = int(threshold_params['TN'])

    confusion_text = f'TP={tp}, FP={fp}\nFN={fn}, TN={tn}'
    ax.text(0.98, 0.02, confusion_text,
            transform=ax.transAxes,
            fontsize=FONT_SIZES['annotation'],
            verticalalignment='bottom',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9,
                     edgecolor='gray', linewidth=0.5))

    plt.tight_layout()

    return fig

def main():
    """Main execution function"""
    print("="*70)
    print("CHART 12: INTENSITY-DURATION THRESHOLDS BY STATION")
    print("="*70)

    # Load data
    print("\nLoading data...")
    pontos_id_df, thresholds_df = load_data()

    print(f"\nTotal I-D points: {len(pontos_id_df):,}")
    print(f"Total stations with thresholds: {len(thresholds_df)}")
    print(f"Stations with valid thresholds: {thresholds_df['a'].notna().sum()}")

    # Create output directory for this chart
    chart_output_dir = f'{OUTPUT_DIR}/chart_12_id_thresholds'
    os.makedirs(chart_output_dir, exist_ok=True)
    print(f"\nOutput directory: {chart_output_dir}")

    # Sort stations by F1 score (descending) to show best performing thresholds first
    thresholds_df = thresholds_df.sort_values(by='f1', ascending=False, na_position='last')

    # Generate chart for each station
    print(f"\nGenerating charts for {len(thresholds_df)} stations...")

    successful = 0
    failed = 0

    for idx, row in thresholds_df.iterrows():
        station_id = int(row['id_estacao'])

        try:
            # Get data for this station
            station_data = pontos_id_df[pontos_id_df['id_estacao'] == station_id]

            if station_data.empty:
                print(f"  [{idx+1}/{len(thresholds_df)}] Station {station_id}: No data, skipping")
                continue

            # Create chart
            fig = create_threshold_chart_for_station(station_id, station_data, row)

            # Save with station ID in filename (zero-padded for sorting)
            output_path = f'{chart_output_dir}/station_{station_id:02d}.png'
            fig.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close(fig)

            successful += 1

            # Status message
            if not np.isnan(row['a']):
                print(f"  [{idx+1}/{len(thresholds_df)}] Station {station_id}: "
                      f"✓ Saved (a={row['a']:.3f}, b={row['b']:.3f}, F1={row['f1']:.3f})")
            else:
                print(f"  [{idx+1}/{len(thresholds_df)}] Station {station_id}: "
                      f"✓ Saved (no valid threshold)")

        except Exception as e:
            failed += 1
            print(f"  [{idx+1}/{len(thresholds_df)}] Station {station_id}: ✗ Failed - {str(e)}")

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
