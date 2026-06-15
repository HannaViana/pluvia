"""
Chart 25: Rainfall Peak Intensity vs Duration with Seasonal Thresholds — Per Sub-bacia (Fixed K=0.85)
One figure per sub-bacia with 2 panels (without / with tolerance).
Draws four seasonal threshold lines (upper and lower) per panel.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from config import setup_plot_style, FONT_SIZES, OUTPUT_DIR, STUDY_PERIOD, STUDY_LOCATION

API_ANALYSIS_DIR = 'data/processed/api_analysis_subbacia'
EVENTS_PATH     = f'{API_ANALYSIS_DIR}/api_analysis_events_subbacia.csv'
THRESHOLDS_PATH = f'{API_ANALYSIS_DIR}/api_threshold_parameters_seasonal_fixed_k.csv'

TIME_STEP_COLS  = ['I_15min','I_30min','I_1h','I_2h','I_3h',
                   'I_6h','I_8h','I_10h','I_12h','I_24h']
DURATION_HOURS  = [0.25, 0.5, 1, 2, 3, 6, 8, 10, 12, 24]
DURATION_LABELS = ['15min','30min','1h','2h','3h','6h','8h','10h','12h','24h']

SEASON_ORDER  = ['Verao','Outono','Inverno','Primavera']
SEASON_LABELS = ['Summer (DJF)','Autumn (MAM)','Winter (JJA)','Spring (SON)']
SEASON_COLORS = ['#d73027','#fc8d59','#4393c3','#74add1']

COLORS_API = {'EA': '#d6604d', 'ESA': '#333333'}


def load_data():
    events     = pd.read_csv(EVENTS_PATH)
    thresholds = pd.read_csv(THRESHOLDS_PATH)
    return events, thresholds


def create_chart_for_subbacia(shi_cd, shi_nm, sb_events, sb_params):
    setup_plot_style()

    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

    esa_events = sb_events[sb_events['classificacao'] == 'ESA']
    ea_events  = sb_events[sb_events['classificacao'] == 'EA']

    for panel_idx, (ax, use_tolerance) in enumerate(zip(axes, [False, True])):
        upper_key = 'upper_tol' if use_tolerance else 'upper_raw'
        lower_key = 'lower_tol' if use_tolerance else 'lower_raw'
        line_style = '--' if use_tolerance else '-'

        # ESA scatter
        for ts_col, d_h in zip(TIME_STEP_COLS, DURATION_HOURS):
            vals = esa_events[ts_col].dropna()
            if not vals.empty:
                ax.scatter(np.full(len(vals), d_h * 0.96), vals,
                           color=COLORS_API['ESA'], s=20, alpha=0.4,
                           zorder=1, marker='s', edgecolors='none')

        # EA scatter
        for ts_col, d_h in zip(TIME_STEP_COLS, DURATION_HOURS):
            vals = ea_events[ts_col].dropna()
            if not vals.empty:
                ax.scatter(np.full(len(vals), d_h * 1.04), vals,
                           color=COLORS_API['EA'], s=45, alpha=0.85,
                           zorder=2, marker='o', linewidths=0.4, edgecolors='black')

        # Seasonal threshold lines
        for season, s_color, s_label in zip(SEASON_ORDER, SEASON_COLORS, SEASON_LABELS):
            upper_vals, lower_vals, valid_d = [], [], []
            seas_params = sb_params[sb_params['season'] == season]

            for ts_col, d_h in zip(TIME_STEP_COLS, DURATION_HOURS):
                row = seas_params[seas_params['time_step_col'] == ts_col]
                if row.empty:
                    continue
                row = row.iloc[0]
                u = row[upper_key]
                l = row[lower_key]
                if not np.isnan(u) and not np.isnan(l):
                    upper_vals.append(u)
                    lower_vals.append(l)
                    valid_d.append(d_h)

            if upper_vals:
                ax.plot(valid_d, upper_vals, color=s_color, linewidth=1.8,
                        linestyle=line_style, alpha=0.85, zorder=5,
                        label=f'{s_label} upper')
                ax.plot(valid_d, lower_vals, color=s_color, linewidth=1.8,
                        linestyle=line_style, alpha=0.85, zorder=5,
                        label=f'{s_label} lower')

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
            Line2D([0],[0], marker='o', color='w', markerfacecolor=COLORS_API['EA'],
                   markersize=8, markeredgecolor='black', markeredgewidth=0.5,
                   label=f'Occurrence (EA, n={len(ea_events)})'),
            Line2D([0],[0], marker='s', color='w', markerfacecolor=COLORS_API['ESA'],
                   markersize=6, alpha=0.6,
                   label=f'Non-occurrence (ESA, n={len(esa_events)})'),
        ]
        for s_color, s_label in zip(SEASON_COLORS, SEASON_LABELS):
            handles.append(
                Line2D([0],[0], color=s_color, linewidth=1.8, linestyle=line_style,
                       label=s_label)
            )
        ax.legend(handles=handles, loc='upper right',
                  fontsize=FONT_SIZES['legend'] - 1, frameon=True, framealpha=0.9)

    axes[0].set_ylabel('Maximum rainfall intensity (mm h$^{-1}$)',
                       fontsize=FONT_SIZES['axis_label'])

    title_name = f'{shi_nm} (shi_cd={shi_cd})' if shi_nm else f'shi_cd={shi_cd}'
    fig.suptitle(f'Rainfall Peak Intensity vs Duration — Seasonal Thresholds (Fixed K=0.85)\n'
                 f'{title_name}  |  {STUDY_LOCATION}, {STUDY_PERIOD}',
                 fontsize=FONT_SIZES['title'], fontweight='bold', y=1.02)
    plt.tight_layout()
    return fig


def main():
    print("=" * 70)
    print("CHART 25: SEASONAL I-D THRESHOLDS PER SUB-BACIA (FIXED K=0.85)")
    print("=" * 70)

    events, thresholds = load_data()
    print(f"  Events: {len(events):,}")
    print(f"  Sub-bacias: {thresholds['shi_cd'].nunique()}")

    out_dir = f'{OUTPUT_DIR}/chart_25_api_id_thresholds_per_subbacia_fixed_k'
    os.makedirs(out_dir, exist_ok=True)

    subbacia_ids = sorted(thresholds['shi_cd'].unique())
    ok, fail = 0, 0

    for shi_cd in subbacia_ids:
        try:
            sb_events  = events[events['shi_cd'] == shi_cd]
            sb_params  = thresholds[thresholds['shi_cd'] == shi_cd]
            shi_nm = (sb_params['shi_nm'].iloc[0]
                      if 'shi_nm' in sb_params.columns and not sb_params.empty else '')

            if sb_events.empty:
                print(f"  {shi_cd:03d}: no events, skipping")
                continue

            fig  = create_chart_for_subbacia(shi_cd, shi_nm, sb_events, sb_params)
            path = f'{out_dir}/subbacia_{shi_cd:03d}.png'
            fig.savefig(path, dpi=300, bbox_inches='tight')
            plt.close(fig)
            ok += 1
            print(f"  {shi_cd:03d} '{shi_nm}': saved")
        except Exception as e:
            fail += 1
            print(f"  {shi_cd:03d}: failed - {e}")

    print(f"\n{'='*70}")
    print(f"  Saved: {ok}  Failed: {fail}")
    print(f"  Output: {out_dir}")
    print("=" * 70)


if __name__ == '__main__':
    main()
