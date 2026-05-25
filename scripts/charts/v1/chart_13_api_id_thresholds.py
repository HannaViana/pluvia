"""
Chart 13: Rainfall Peak Intensity vs Duration with API Thresholds
Creates scatter plots showing occurrences/non-occurrences with upper and lower
thresholds, both with and without tolerance levels applied.
Reproduces Geraldo Moura (2021) Figure 8 methodology.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from config import (setup_plot_style, COLORS, FONT_SIZES, FIGURE_SIZES,
                    OUTPUT_DIR, STUDY_PERIOD, STUDY_LOCATION)

# Data paths
API_ANALYSIS_DIR = 'data/processed/api_analysis'
EVENTS_PATH = f'{API_ANALYSIS_DIR}/api_analysis_events.csv'
THRESHOLDS_PATH = f'{API_ANALYSIS_DIR}/api_threshold_parameters.csv'

# Time-steps
TIME_STEP_COLS = ['I_15min', 'I_30min', 'I_1h', 'I_2h', 'I_3h',
                  'I_6h', 'I_8h', 'I_10h', 'I_12h', 'I_24h']
DURATION_HOURS = [0.25, 0.5, 1, 2, 3, 6, 8, 10, 12, 24]
DURATION_LABELS = ['15min', '30min', '1h', '2h', '3h', '6h', '8h', '10h', '12h', '24h']

# Colors
COLORS_API = {
    'EA': '#d6604d',
    'ESA': '#333333',
    'upper': '#b2182b',
    'lower': '#2166ac',
    'upper_tol': '#b2182b',
    'lower_tol': '#2166ac',
}


def load_data():
    """Load events and threshold parameters"""
    print(f"Loading events from {EVENTS_PATH}...")
    events_df = pd.read_csv(EVENTS_PATH)

    print(f"Loading thresholds from {THRESHOLDS_PATH}...")
    thresholds_df = pd.read_csv(THRESHOLDS_PATH)

    return events_df, thresholds_df


def create_id_threshold_panels(events_df, thresholds_df):
    """Create 2-panel figure: (a) without tolerance, (b) with tolerance"""
    setup_plot_style()

    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

    for panel_idx, (ax, use_tolerance) in enumerate(zip(axes, [False, True])):
        # Plot scatter: each event contributes one point per duration
        # Sample events to reduce clutter
        esa_events = events_df[events_df['classificacao'] == 'ESA'] # .sample(
        #     n=min(1000, len(events_df[events_df['classificacao'] == 'ESA'])),
        #     random_state=42
        # )
        ea_events = events_df[events_df['classificacao'] == 'EA'] # .sample(
        #     n=min(500, len(events_df[events_df['classificacao'] == 'EA'])),
        #     random_state=42
        # )

        # Plot ESA first (background) — shifted slightly left in log-space
        for d_idx, (ts_col, d_h) in enumerate(zip(TIME_STEP_COLS, DURATION_HOURS)):
            intensities = esa_events[ts_col].dropna()
            durations = np.full(len(intensities), d_h * 0.96)
            ax.scatter(durations, intensities,
                       color=COLORS_API['ESA'], s=20, alpha=0.4,
                       zorder=1, marker='s', edgecolors='none')

        # Plot EA on top (foreground) — shifted slightly right in log-space
        for d_idx, (ts_col, d_h) in enumerate(zip(TIME_STEP_COLS, DURATION_HOURS)):
            intensities = ea_events[ts_col].dropna()
            durations = np.full(len(intensities), d_h * 1.04)
            ax.scatter(durations, intensities,
                       color=COLORS_API['EA'], s=45, alpha=0.85,
                       zorder=2, marker='o',
                       linewidths=0.4, edgecolors='black')

        # Plot threshold lines
        upper_key = 'upper_tol' if use_tolerance else 'upper_raw'
        lower_key = 'lower_tol' if use_tolerance else 'lower_raw'
        line_style = '--' if use_tolerance else '-'

        upper_values = []
        lower_values = []
        for _, row in thresholds_df.iterrows():
            upper_values.append(row[upper_key])
            lower_values.append(row[lower_key])

        ax.plot(DURATION_HOURS, upper_values,
                color=COLORS_API['upper'], linewidth=2, linestyle=line_style,
                label=f'Upper threshold{"$_{99th}$" if use_tolerance else ""}',
                zorder=5)
        ax.plot(DURATION_HOURS, lower_values,
                color=COLORS_API['lower'], linewidth=2, linestyle=line_style,
                label=f'Lower threshold{"$_{5\\%}$" if use_tolerance else ""}',
                zorder=5)

        # Axes configuration
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xticks(DURATION_HOURS)
        ax.set_xticklabels(DURATION_LABELS, fontsize=FONT_SIZES['tick_label'], rotation=45)
        ax.set_xlabel('Duration', fontsize=FONT_SIZES['axis_label'])
        ax.grid(True, which='both', linestyle='--', alpha=0.3, linewidth=0.5)
        ax.set_axisbelow(True)

        title_suffix = 'with tolerance levels' if use_tolerance else 'without tolerance levels'
        panel_letter = chr(ord('a') + panel_idx)
        ax.set_title(f'({panel_letter}) {title_suffix.capitalize()}',
                     fontsize=FONT_SIZES['subtitle'], fontweight='bold', pad=10)

        # Legend
        from matplotlib.lines import Line2D
        handles = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor=COLORS_API['EA'],
                   markersize=8, markeredgecolor='black', markeredgewidth=0.5,
                   label='Occurrence (EA)'),
            Line2D([0], [0], marker='s', color='w', markerfacecolor=COLORS_API['ESA'],
                   markersize=6, alpha=0.6, label='Non-occurrence (ESA)'),
            Line2D([0], [0], color=COLORS_API['upper'], linewidth=2, linestyle=line_style,
                   label='Upper threshold'),
            Line2D([0], [0], color=COLORS_API['lower'], linewidth=2, linestyle=line_style,
                   label='Lower threshold'),
        ]
        ax.legend(handles=handles, loc='upper right', fontsize=FONT_SIZES['legend'],
                  frameon=True, framealpha=0.9)

    axes[0].set_ylabel('Maximum rainfall intensity (mm h$^{-1}$)',
                       fontsize=FONT_SIZES['axis_label'])

    fig.suptitle(f'Rainfall Peak Intensity vs Duration Thresholds\n'
                 f'{STUDY_LOCATION}, {STUDY_PERIOD}',
                 fontsize=FONT_SIZES['title'], fontweight='bold', y=1.02)

    plt.tight_layout()
    return fig


def main():
    print("=" * 70)
    print("CHART 13: API-BASED I-D THRESHOLDS")
    print("=" * 70)

    events_df, thresholds_df = load_data()
    print(f"  Events: {len(events_df):,}")
    print(f"  Time-steps with thresholds: {len(thresholds_df)}")

    chart_output_dir = f'{OUTPUT_DIR}/chart_13_api_id_thresholds'
    os.makedirs(chart_output_dir, exist_ok=True)

    fig = create_id_threshold_panels(events_df, thresholds_df)

    output_path = f'{chart_output_dir}/id_thresholds_with_tolerance.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"\n  Saved: {output_path}")
    print("=" * 70)


if __name__ == '__main__':
    main()
