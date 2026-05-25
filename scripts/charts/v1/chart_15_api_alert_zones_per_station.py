"""
Chart 15: Peak Rainfall Intensity vs API Alert Zones — Per Station
One figure per station, 2x5 grid of time-step panels showing the exponential
intermediate threshold I = a * exp(b * API) + c and four alert zones.
Mirrors chart 14 but uses per-station fitted parameters.
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
THRESHOLDS_PATH = f'{API_ANALYSIS_DIR}/api_threshold_parameters_per_station.csv'

# Time-step configuration
TIME_STEP_COLS = ['I_15min', 'I_30min', 'I_1h', 'I_2h', 'I_3h',
                  'I_6h', 'I_8h', 'I_10h', 'I_12h', 'I_24h']
DURATION_LABELS = ['15 min', '30 min', '1 hour', '2 hours', '3 hours',
                   '6 hours', '8 hours', '10 hours', '12 hours', '24 hours']

ZONE_COLORS = {
    'red': '#d73027',
    'orange': '#fc8d59',
    'yellow': '#fee090',
    'blue': '#91bfdb',
}

EA_COLOR = '#d6604d'
ESA_COLOR = '#333333'


def load_data():
    events_df = pd.read_csv(EVENTS_PATH)
    thresholds_df = pd.read_csv(THRESHOLDS_PATH)
    return events_df, thresholds_df


def create_alert_zone_chart_for_station(station_id, station_events, station_params):
    """Create 2x5 grid of I vs API panels for a single station."""
    setup_plot_style()

    n_cols = 5
    n_rows = 2
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, 8))
    axes = axes.flatten()

    for idx, ts_col in enumerate(TIME_STEP_COLS):
        ax = axes[idx]
        ts_label = DURATION_LABELS[idx]

        row = station_params[station_params['time_step_col'] == ts_col]
        if row.empty:
            ax.text(0.5, 0.5, 'No data', transform=ax.transAxes, ha='center', va='center')
            ax.set_title(ts_label, fontsize=FONT_SIZES['tick_label'], fontweight='bold')
            continue

        row = row.iloc[0]
        upper_tol = row['upper_tol']
        lower_tol = row['lower_tol']
        a = row['a']
        b = row['b']
        c = row['c']
        best_days = int(row['best_antecedent_days']) if not np.isnan(row['best_antecedent_days']) else 0
        api_col = f'api_{best_days}d' if best_days > 0 else 'api_5d'

        if np.isnan(upper_tol) or np.isnan(lower_tol):
            ax.text(0.5, 0.5, 'Insufficient data', transform=ax.transAxes,
                    ha='center', va='center', fontsize=8)
            ax.set_title(ts_label, fontsize=FONT_SIZES['tick_label'], fontweight='bold')
            continue

        valid_mask = station_events[ts_col].notna() & station_events[api_col].notna()
        ts_data = station_events[valid_mask].copy()

        intensities = ts_data[ts_col].values
        api_values = ts_data[api_col].values
        classifications = ts_data['classificacao'].values

        api_min = 0
        api_max = min(100, np.percentile(api_values, 99) * 1.2) if len(api_values) > 0 else 100
        i_min = 0
        i_max_display = upper_tol * 1.5

        api_range = np.linspace(api_min, api_max, 200)

        # Fill zones
        ax.fill_between(api_range, upper_tol, i_max_display,
                        color=ZONE_COLORS['red'], alpha=0.7, zorder=0)
        ax.fill_between(api_range, i_min, lower_tol,
                        color=ZONE_COLORS['blue'], alpha=0.7, zorder=0)

        if not np.isnan(a) and best_days > 0:
            i_curve = a * np.exp(b * api_range) + c
            i_curve = np.clip(i_curve, lower_tol, upper_tol)

            ax.fill_between(api_range, i_curve, upper_tol,
                            color=ZONE_COLORS['orange'], alpha=0.7, zorder=0)
            ax.fill_between(api_range, lower_tol, i_curve,
                            color=ZONE_COLORS['yellow'], alpha=0.7, zorder=0)
            ax.plot(api_range, a * np.exp(b * api_range) + c,
                    color='black', linewidth=1.5, zorder=4)

            eq_text = f'I = {a:.1f}e$^{{{b:.2f}\\cdot API}}$ + {c:.1f}'
            ax.text(0.95, 0.08, eq_text, transform=ax.transAxes,
                    fontsize=7, ha='right', va='bottom',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
        else:
            ax.fill_between(api_range, lower_tol, upper_tol,
                            color=ZONE_COLORS['orange'], alpha=0.5, zorder=0)

        ax.axhline(upper_tol, color='darkred', linewidth=1, linestyle='--', zorder=3)
        ax.axhline(lower_tol, color='darkblue', linewidth=1, linestyle='--', zorder=3)

        # Scatter points
        esa_mask = classifications == 'ESA'
        ea_mask = classifications == 'EA'
        if esa_mask.any():
            ax.scatter(api_values[esa_mask], intensities[esa_mask],
                       color=ESA_COLOR, s=10, alpha=0.4, zorder=2,
                       marker='s', edgecolors='none')
        if ea_mask.any():
            ax.scatter(api_values[ea_mask], intensities[ea_mask],
                       color=EA_COLOR, s=20, alpha=0.85, zorder=3,
                       marker='o', edgecolors='black', linewidths=0.3)

        ax.set_xlim(api_min, api_max)
        ax.set_ylim(i_min, i_max_display)

        title = (f'{ts_label} × {best_days} day{"s" if best_days != 1 else ""}'
                 if best_days > 0 else ts_label)
        ax.set_title(title, fontsize=FONT_SIZES['tick_label'], fontweight='bold', pad=5)

        if idx >= n_cols * (n_rows - 1):
            ax.set_xlabel('API (mm)', fontsize=FONT_SIZES['tick_label'])
        if idx % n_cols == 0:
            ax.set_ylabel('Intensity (mm h$^{-1}$)', fontsize=FONT_SIZES['tick_label'])

        ax.tick_params(labelsize=8)

    # Legend
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    legend_elements = [
        Patch(facecolor=ZONE_COLORS['red'], alpha=0.7, label='Red alert'),
        Patch(facecolor=ZONE_COLORS['orange'], alpha=0.7, label='Orange alert'),
        Patch(facecolor=ZONE_COLORS['yellow'], alpha=0.7, label='Yellow alert'),
        Patch(facecolor=ZONE_COLORS['blue'], alpha=0.7, label='Blue alert'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=EA_COLOR,
               markersize=7, markeredgecolor='black', markeredgewidth=0.4, label='EA'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor=ESA_COLOR,
               markersize=6, alpha=0.6, label='ESA'),
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=6,
               fontsize=FONT_SIZES['legend'], frameon=True,
               bbox_to_anchor=(0.5, -0.02))

    fig.suptitle(f'Peak Rainfall Intensity vs API — Station {station_id}\n'
                 f'{STUDY_LOCATION}, {STUDY_PERIOD}',
                 fontsize=FONT_SIZES['title'], fontweight='bold', y=1.01)

    plt.tight_layout(rect=[0, 0.04, 1, 0.98])
    return fig


def main():
    print("=" * 70)
    print("CHART 15: API ALERT ZONES PER STATION")
    print("=" * 70)

    events_df, thresholds_df = load_data()
    print(f"  Events: {len(events_df):,}")
    print(f"  Stations: {thresholds_df['id_estacao'].nunique()}")

    chart_output_dir = f'{OUTPUT_DIR}/chart_15_api_alert_zones_per_station'
    os.makedirs(chart_output_dir, exist_ok=True)

    station_ids = sorted(thresholds_df['id_estacao'].unique())
    successful = 0
    failed = 0

    for station_id in station_ids:
        try:
            station_events = events_df[events_df['id_estacao'] == station_id]
            station_params = thresholds_df[thresholds_df['id_estacao'] == station_id]

            fig = create_alert_zone_chart_for_station(station_id, station_events, station_params)

            output_path = f'{chart_output_dir}/station_{station_id:02d}.png'
            fig.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close(fig)
            successful += 1
            print(f"  Station {station_id:02d}: saved")

        except Exception as e:
            failed += 1
            print(f"  Station {station_id:02d}: failed — {e}")

    print(f"\n{'='*70}")
    print(f"  Saved: {successful}  Failed: {failed}")
    print(f"  Output: {chart_output_dir}")
    print("=" * 70)


if __name__ == '__main__':
    main()
