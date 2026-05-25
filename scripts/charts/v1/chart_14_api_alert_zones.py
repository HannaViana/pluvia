"""
Chart 14: Peak Rainfall Intensity vs API with Alert Zones
Creates multi-panel charts showing the exponential intermediate threshold
I = a * exp(b * API) + c that defines four alert zones per time-step.
Reproduces Geraldo Moura (2021) Figures 9/10 methodology.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from config import (setup_plot_style, FONT_SIZES, FIGURE_SIZES,
                    OUTPUT_DIR, STUDY_PERIOD, STUDY_LOCATION)

# Data paths
API_ANALYSIS_DIR = 'data/processed/api_analysis'
EVENTS_PATH = f'{API_ANALYSIS_DIR}/api_analysis_events.csv'
THRESHOLDS_PATH = f'{API_ANALYSIS_DIR}/api_threshold_parameters.csv'

# Time-step configuration
TIME_STEP_COLS = ['I_15min', 'I_30min', 'I_1h', 'I_2h', 'I_3h',
                  'I_6h', 'I_8h', 'I_10h', 'I_12h', 'I_24h']
DURATION_LABELS = ['15 min', '30 min', '1 hour', '2 hours', '3 hours',
                   '6 hours', '8 hours', '10 hours', '12 hours', '24 hours']

# Alert zone colors (following CEMADEN / civil defense convention)
ZONE_COLORS = {
    'red': '#d73027',
    'orange': '#fc8d59',
    'yellow': '#fee090',
    'blue': '#91bfdb',
}


def load_data():
    """Load events and threshold parameters"""
    events_df = pd.read_csv(EVENTS_PATH)
    thresholds_df = pd.read_csv(THRESHOLDS_PATH)
    return events_df, thresholds_df


def create_alert_zone_chart(events_df, thresholds_df):
    """Create 2x5 grid of I vs API charts with colored alert zones"""
    setup_plot_style()

    n_panels = len(thresholds_df)
    n_cols = 5
    n_rows = int(np.ceil(n_panels / n_cols))

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, 4 * n_rows))
    axes = axes.flatten()

    for idx, (_, params) in enumerate(thresholds_df.iterrows()):
        ax = axes[idx]
        ts_col = params['time_step_col']
        ts_label = DURATION_LABELS[idx] if idx < len(DURATION_LABELS) else params['time_step']

        upper_tol = params['upper_tol']
        lower_tol = params['lower_tol']
        a = params['a']
        b = params['b']
        c = params['c']
        best_days = int(params['best_antecedent_days']) if not np.isnan(params['best_antecedent_days']) else 0
        api_col = f'api_{best_days}d' if best_days > 0 else 'api_5d'

        # Get valid data for this time-step
        valid_mask = events_df[ts_col].notna() & events_df[api_col].notna()
        ts_data = events_df[valid_mask].copy()

        if ts_data.empty:
            ax.text(0.5, 0.5, 'No data', transform=ax.transAxes, ha='center')
            ax.set_title(f'{ts_label}', fontsize=FONT_SIZES['tick_label'], fontweight='bold')
            continue

        intensities = ts_data[ts_col].values
        api_values = ts_data[api_col].values
        classifications = ts_data['classificacao'].values

        # Define axis ranges (match Geraldo Moura's ~1-100mm API range)
        api_min = 0
        api_max = min(100, np.percentile(api_values, 99) * 1.2)
        i_min = 0

        api_range = np.linspace(api_min, api_max, 200)

        # Fill zones
        i_max_display = upper_tol * 1.5
        # Red zone: above upper_tol
        ax.fill_between(api_range, upper_tol, i_max_display,
                        color=ZONE_COLORS['red'], alpha=0.7, zorder=0)

        # Blue zone: below lower_tol
        ax.fill_between(api_range, i_min, lower_tol,
                        color=ZONE_COLORS['blue'], alpha=0.7, zorder=0)

        # Middle zone: split by exponential curve if fitted
        if not np.isnan(a) and best_days > 0:
            i_curve = a * np.exp(b * api_range) + c
            i_curve = np.clip(i_curve, lower_tol, upper_tol)

            # Orange: above curve (high probability)
            ax.fill_between(api_range, i_curve, upper_tol,
                            color=ZONE_COLORS['orange'], alpha=0.7, zorder=0)

            # Yellow: below curve (moderate probability)
            ax.fill_between(api_range, lower_tol, i_curve,
                            color=ZONE_COLORS['yellow'], alpha=0.7, zorder=0)

            # Plot curve line
            ax.plot(api_range, a * np.exp(b * api_range) + c,
                    color='black', linewidth=1.5, linestyle='-', zorder=4)

            # Annotate equation
            eq_text = f'I = {a:.1f}e$^{{{b:.2f}\\cdot API}}$ + {c:.1f}'
            ax.text(0.95, 0.08, eq_text, transform=ax.transAxes,
                    fontsize=7, ha='right', va='bottom',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
        else:
            # No curve fitted: fill middle entirely as orange
            ax.fill_between(api_range, lower_tol, upper_tol,
                            color=ZONE_COLORS['orange'], alpha=0.5, zorder=0)

        # Threshold lines
        ax.axhline(upper_tol, color='darkred', linewidth=1, linestyle='--', zorder=3)
        ax.axhline(lower_tol, color='darkblue', linewidth=1, linestyle='--', zorder=3)

        # Set axis limits
        ax.set_xlim(api_min, api_max)
        ax.set_ylim(i_min, i_max_display)

        # Title
        title = f'{ts_label} x {best_days} day{"s" if best_days != 1 else ""}' if best_days > 0 else ts_label
        ax.set_title(title, fontsize=FONT_SIZES['tick_label'], fontweight='bold', pad=5)

        # Axis labels (only for edge panels)
        if idx >= n_cols * (n_rows - 1):
            ax.set_xlabel('API (mm)', fontsize=FONT_SIZES['tick_label'])
        if idx % n_cols == 0:
            ax.set_ylabel('Intensity (mm h$^{-1}$)', fontsize=FONT_SIZES['tick_label'])

        ax.tick_params(labelsize=8)

    # Turn off unused axes
    for idx in range(n_panels, len(axes)):
        axes[idx].axis('off')

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=ZONE_COLORS['red'], alpha=0.7, label='Red alert'),
        Patch(facecolor=ZONE_COLORS['orange'], alpha=0.7, label='Orange alert'),
        Patch(facecolor=ZONE_COLORS['yellow'], alpha=0.7, label='Yellow alert'),
        Patch(facecolor=ZONE_COLORS['blue'], alpha=0.7, label='Blue alert'),
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=4,
               fontsize=FONT_SIZES['legend'], frameon=True,
               bbox_to_anchor=(0.5, -0.02))

    fig.suptitle(f'Peak Rainfall Intensity vs Antecedent Precipitation Index (API)\n'
                 f'Warning Level Systems — {STUDY_LOCATION}, {STUDY_PERIOD}',
                 fontsize=FONT_SIZES['title'], fontweight='bold', y=1.02)

    plt.tight_layout(rect=[0, 0.03, 1, 0.98])
    return fig


def main():
    print("=" * 70)
    print("CHART 14: API ALERT ZONES")
    print("=" * 70)

    events_df, thresholds_df = load_data()
    print(f"  Events: {len(events_df):,}")
    print(f"  Time-steps: {len(thresholds_df)}")

    chart_output_dir = f'{OUTPUT_DIR}/chart_14_api_alert_zones'
    os.makedirs(chart_output_dir, exist_ok=True)

    fig = create_alert_zone_chart(events_df, thresholds_df)

    output_path = f'{chart_output_dir}/api_alert_zones.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"\n  Saved: {output_path}")
    print("=" * 70)


if __name__ == '__main__':
    main()
