"""
Chart 20: Rainfall Peak Intensity vs Duration with API Thresholds — Per Sub-bacia (Optimized K)
Like chart_18 but uses the threshold parameters fitted with optimized K per sub-bacia.
Reads the updated api_threshold_parameters_per_subbacia.csv which contains best_k column.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from config import (setup_plot_style, COLORS, FONT_SIZES, FIGURE_SIZES,
                    OUTPUT_DIR, STUDY_PERIOD, STUDY_LOCATION)

API_ANALYSIS_DIR = 'data/processed/api_analysis_subbacia'
EVENTS_PATH = f'{API_ANALYSIS_DIR}/api_analysis_events_subbacia.csv'
THRESHOLDS_PATH = f'{API_ANALYSIS_DIR}/api_threshold_parameters_per_subbacia.csv'

TIME_STEP_COLS = ['I_15min', 'I_30min', 'I_1h', 'I_2h', 'I_3h',
                  'I_6h', 'I_8h', 'I_10h', 'I_12h', 'I_24h']
DURATION_HOURS = [0.25, 0.5, 1, 2, 3, 6, 8, 10, 12, 24]
DURATION_LABELS = ['15min', '30min', '1h', '2h', '3h', '6h', '8h', '10h', '12h', '24h']

COLORS_API = {
    'EA': '#d6604d',
    'ESA': '#333333',
    'upper': '#b2182b',
    'lower': '#2166ac',
}


def load_data():
    events_df = pd.read_csv(EVENTS_PATH)
    thresholds_df = pd.read_csv(THRESHOLDS_PATH)
    return events_df, thresholds_df


def create_id_threshold_chart_for_subbacia(shi_cd, shi_nm, subbacia_events, subbacia_params):
    """Create 2-panel I-D figure (without / with tolerance) for a single sub-bacia."""
    setup_plot_style()

    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

    for panel_idx, (ax, use_tolerance) in enumerate(zip(axes, [False, True])):
        upper_key = 'upper_tol' if use_tolerance else 'upper_raw'
        lower_key = 'lower_tol' if use_tolerance else 'lower_raw'
        line_style = '--' if use_tolerance else '-'

        esa_events = subbacia_events[subbacia_events['classificacao'] == 'ESA']
        ea_events = subbacia_events[subbacia_events['classificacao'] == 'EA']

        # ESA scatter (background)
        for ts_col, d_h in zip(TIME_STEP_COLS, DURATION_HOURS):
            intensities = esa_events[ts_col].dropna()
            if intensities.empty:
                continue
            durations = np.full(len(intensities), d_h * 0.96)
            ax.scatter(durations, intensities,
                       color=COLORS_API['ESA'], s=20, alpha=0.4,
                       zorder=1, marker='s', edgecolors='none')

        # EA scatter (foreground)
        for ts_col, d_h in zip(TIME_STEP_COLS, DURATION_HOURS):
            intensities = ea_events[ts_col].dropna()
            if intensities.empty:
                continue
            durations = np.full(len(intensities), d_h * 1.04)
            ax.scatter(durations, intensities,
                       color=COLORS_API['EA'], s=45, alpha=0.85,
                       zorder=2, marker='o',
                       linewidths=0.4, edgecolors='black')

        # Threshold lines
        upper_values = []
        lower_values = []
        valid_durations = []

        for ts_col, d_h in zip(TIME_STEP_COLS, DURATION_HOURS):
            row = subbacia_params[subbacia_params['time_step_col'] == ts_col]
            if row.empty:
                continue
            row = row.iloc[0]
            u = row[upper_key]
            l = row[lower_key]
            if not np.isnan(u) and not np.isnan(l):
                upper_values.append(u)
                lower_values.append(l)
                valid_durations.append(d_h)

        if upper_values:
            upper_label = 'Upper threshold$_{99th}$' if use_tolerance else 'Upper threshold'
            lower_label = 'Lower threshold$_{5\\%}$' if use_tolerance else 'Lower threshold'
            ax.plot(valid_durations, upper_values,
                    color=COLORS_API['upper'], linewidth=2, linestyle=line_style,
                    label=upper_label, zorder=5)
            ax.plot(valid_durations, lower_values,
                    color=COLORS_API['lower'], linewidth=2, linestyle=line_style,
                    label=lower_label, zorder=5)

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

        from matplotlib.lines import Line2D
        handles = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor=COLORS_API['EA'],
                   markersize=8, markeredgecolor='black', markeredgewidth=0.5,
                   label=f'Occurrence (EA, n={len(ea_events)})'),
            Line2D([0], [0], marker='s', color='w', markerfacecolor=COLORS_API['ESA'],
                   markersize=6, alpha=0.6,
                   label=f'Non-occurrence (ESA, n={len(esa_events)})'),
            Line2D([0], [0], color=COLORS_API['upper'], linewidth=2, linestyle=line_style,
                   label='Upper threshold'),
            Line2D([0], [0], color=COLORS_API['lower'], linewidth=2, linestyle=line_style,
                   label='Lower threshold'),
        ]
        ax.legend(handles=handles, loc='upper right', fontsize=FONT_SIZES['legend'],
                  frameon=True, framealpha=0.9)

    axes[0].set_ylabel('Maximum rainfall intensity (mm h$^{-1}$)',
                       fontsize=FONT_SIZES['axis_label'])

    # Show best_k range in title if available
    if 'best_k' in subbacia_params.columns:
        k_vals = subbacia_params['best_k'].dropna().unique()
        k_str = ', '.join([f'{k:.2f}' for k in sorted(k_vals)]) if len(k_vals) > 0 else ''
        k_note = f' [K={k_str}]' if k_str else ''
    else:
        k_note = ''

    title_name = f'{shi_nm} (shi_cd={shi_cd})' if shi_nm else f'shi_cd={shi_cd}'
    fig.suptitle(f'Rainfall Peak Intensity vs Duration Thresholds — {title_name}{k_note}\n'
                 f'{STUDY_LOCATION}, {STUDY_PERIOD}',
                 fontsize=FONT_SIZES['title'], fontweight='bold', y=1.02)

    plt.tight_layout()
    return fig


def main():
    print("=" * 70)
    print("CHART 20: API-BASED I-D THRESHOLDS PER SUB-BACIA (OPTIMIZED K)")
    print("=" * 70)

    events_df, thresholds_df = load_data()
    print(f"  Events: {len(events_df):,}")
    print(f"  Sub-bacias: {thresholds_df['shi_cd'].nunique()}")

    chart_output_dir = f'{OUTPUT_DIR}/chart_20_api_id_thresholds_per_subbacia_v2'
    os.makedirs(chart_output_dir, exist_ok=True)

    subbacia_ids = sorted(thresholds_df['shi_cd'].unique())
    successful = 0
    failed = 0

    for shi_cd in subbacia_ids:
        try:
            subbacia_events = events_df[events_df['shi_cd'] == shi_cd]
            subbacia_params = thresholds_df[thresholds_df['shi_cd'] == shi_cd]
            shi_nm = (subbacia_params['shi_nm'].iloc[0]
                      if 'shi_nm' in subbacia_params.columns and not subbacia_params.empty else '')

            if subbacia_events.empty:
                print(f"  Sub-bacia {shi_cd:03d}: no events, skipping")
                continue

            fig = create_id_threshold_chart_for_subbacia(
                shi_cd, shi_nm, subbacia_events, subbacia_params
            )

            output_path = f'{chart_output_dir}/subbacia_{shi_cd:03d}.png'
            fig.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close(fig)
            successful += 1
            print(f"  Sub-bacia {shi_cd:03d} '{shi_nm}': saved")

        except Exception as e:
            failed += 1
            print(f"  Sub-bacia {shi_cd:03d}: failed - {e}")

    print(f"\n{'='*70}")
    print(f"  Saved: {successful}  Failed: {failed}")
    print(f"  Output: {chart_output_dir}")
    print("=" * 70)


if __name__ == '__main__':
    main()
