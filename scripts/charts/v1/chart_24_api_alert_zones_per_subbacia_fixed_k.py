"""
Chart 24: Peak Rainfall Intensity vs API Alert Zones — Per Sub-bacia (Fixed K=0.85)
Annual overview using seasonal_fixed_k threshold parameters.
One figure per sub-bacia (2×5 grid); each panel shows all events vs api_5d
with the four seasonal threshold levels drawn as horizontal lines.
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
DURATION_LABELS = ['15 min','30 min','1 hour','2 hours','3 hours',
                   '6 hours','8 hours','10 hours','12 hours','24 hours']

SEASON_ORDER  = ['Verao','Outono','Inverno','Primavera']
SEASON_LABELS = ['Summer (DJF)','Autumn (MAM)','Winter (JJA)','Spring (SON)']
SEASON_COLORS = ['#d73027','#fc8d59','#4393c3','#74add1']

EA_COLOR  = '#d6604d'
ESA_COLOR = '#333333'

REF_API_COL = 'api_5d'   # fixed reference x-axis (5-day antecedent, K=0.85)


def load_data():
    events     = pd.read_csv(EVENTS_PATH)
    thresholds = pd.read_csv(THRESHOLDS_PATH)
    return events, thresholds


def create_chart_for_subbacia(shi_cd, shi_nm, sb_events, sb_params):
    setup_plot_style()

    n_cols, n_rows = 5, 2
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, 8))
    axes = axes.flatten()

    for idx, ts_col in enumerate(TIME_STEP_COLS):
        ax = axes[idx]
        ts_label = DURATION_LABELS[idx]

        valid = sb_events[sb_events[ts_col].notna() & sb_events[REF_API_COL].notna()]
        if valid.empty:
            ax.text(0.5, 0.5, 'No data', transform=ax.transAxes,
                    ha='center', va='center', fontsize=8, color='gray')
            ax.set_title(ts_label, fontsize=FONT_SIZES['tick_label'], fontweight='bold')
            continue

        intensities     = valid[ts_col].values
        api_values      = valid[REF_API_COL].values
        classifications = valid['classificacao'].values

        api_min = 0
        api_max = min(100, np.percentile(api_values, 99) * 1.2) if len(api_values) > 0 else 100
        i_max_display = np.percentile(intensities, 99) * 1.5 if len(intensities) > 0 else 10

        # ESA scatter
        esa_m = classifications == 'ESA'
        ea_m  = classifications == 'EA'
        if esa_m.any():
            ax.scatter(api_values[esa_m], intensities[esa_m],
                       color=ESA_COLOR, s=8, alpha=0.3, zorder=1,
                       marker='s', edgecolors='none')
        if ea_m.any():
            ax.scatter(api_values[ea_m], intensities[ea_m],
                       color=EA_COLOR, s=18, alpha=0.85, zorder=3,
                       marker='o', edgecolors='black', linewidths=0.3)

        # Seasonal threshold lines (upper_tol solid, lower_tol dashed)
        for season, s_color in zip(SEASON_ORDER, SEASON_COLORS):
            row = sb_params[(sb_params['season'] == season) &
                            (sb_params['time_step_col'] == ts_col)]
            if row.empty:
                continue
            row = row.iloc[0]
            u = row['upper_tol']
            l = row['lower_tol']
            if not np.isnan(u):
                ax.axhline(u, color=s_color, linewidth=1.2, linestyle='-',
                           alpha=0.85, zorder=4)
            if not np.isnan(l):
                ax.axhline(l, color=s_color, linewidth=1.2, linestyle='--',
                           alpha=0.85, zorder=4)

        ax.set_xlim(api_min, api_max)
        ax.set_ylim(0, i_max_display)
        ax.set_title(ts_label, fontsize=FONT_SIZES['tick_label'],
                     fontweight='bold', pad=5)
        if idx >= n_cols * (n_rows - 1):
            ax.set_xlabel(f'API {REF_API_COL} (mm)', fontsize=FONT_SIZES['tick_label'])
        if idx % n_cols == 0:
            ax.set_ylabel('Intensity (mm h$^{-1}$)', fontsize=FONT_SIZES['tick_label'])
        ax.tick_params(labelsize=8)

    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0],[0], marker='o', color='w', markerfacecolor=EA_COLOR,
               markersize=7, markeredgecolor='black', markeredgewidth=0.4, label='EA'),
        Line2D([0],[0], marker='s', color='w', markerfacecolor=ESA_COLOR,
               markersize=6, alpha=0.6, label='ESA'),
    ]
    for s_label, s_color in zip(SEASON_LABELS, SEASON_COLORS):
        legend_elements.append(
            Line2D([0],[0], color=s_color, linewidth=1.2, linestyle='-',
                   label=f'{s_label} upper')
        )
        legend_elements.append(
            Line2D([0],[0], color=s_color, linewidth=1.2, linestyle='--',
                   label=f'{s_label} lower')
        )
    fig.legend(handles=legend_elements, loc='lower center', ncol=5,
               fontsize=FONT_SIZES['legend'] - 1, frameon=True,
               bbox_to_anchor=(0.5, -0.03))

    title_name = f'{shi_nm} (shi_cd={shi_cd})' if shi_nm else f'shi_cd={shi_cd}'
    fig.suptitle(f'Rainfall Intensity vs API — {title_name} [Fixed K=0.85, Seasonal Thresholds]\n'
                 f'{STUDY_LOCATION}, {STUDY_PERIOD}',
                 fontsize=FONT_SIZES['title'], fontweight='bold', y=1.01)
    plt.tight_layout(rect=[0, 0.05, 1, 0.98])
    return fig


def main():
    print("=" * 70)
    print("CHART 24: API ALERT ZONES PER SUB-BACIA (FIXED K=0.85)")
    print("=" * 70)

    events, thresholds = load_data()
    print(f"  Events: {len(events):,}")
    print(f"  Sub-bacias: {thresholds['shi_cd'].nunique()}")

    out_dir = f'{OUTPUT_DIR}/chart_24_api_alert_zones_per_subbacia_fixed_k'
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
