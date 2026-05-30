"""
Chart 22: I-D Thresholds by Season — Per Sub-bacia
One figure per sub-bacia with 4 panels (one per season) showing EA/ESA scatter
and seasonal lower_tol / upper_tol threshold lines.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from config import setup_plot_style, FONT_SIZES, OUTPUT_DIR, STUDY_PERIOD, STUDY_LOCATION

SEASONAL_PATH = 'data/processed/api_analysis_subbacia/api_threshold_parameters_seasonal.csv'
EVENTS_PATH   = 'data/processed/api_analysis_subbacia/api_analysis_events_subbacia.csv'

TIME_STEP_COLS  = ['I_15min','I_30min','I_1h','I_2h','I_3h','I_6h','I_8h','I_10h','I_12h','I_24h']
DURATION_HOURS  = [0.25, 0.5, 1, 2, 3, 6, 8, 10, 12, 24]
DURATION_LABELS = ['15min','30min','1h','2h','3h','6h','8h','10h','12h','24h']

SEASON_ORDER  = ['Verao','Outono','Inverno','Primavera']
SEASON_LABELS = ['Summer (DJF)','Autumn (MAM)','Winter (JJA)','Spring (SON)']
SEASON_COLORS_LINE = ['#d73027','#fc8d59','#4393c3','#74add1']

COLORS_API = {'EA': '#d6604d', 'ESA': '#333333',
              'upper': '#b2182b', 'lower': '#2166ac'}

MONTH_TO_SEASON = {12:'Verao',1:'Verao',2:'Verao',
                   3:'Outono',4:'Outono',5:'Outono',
                   6:'Inverno',7:'Inverno',8:'Inverno',
                   9:'Primavera',10:'Primavera',11:'Primavera'}


def load_data():
    df     = pd.read_csv(SEASONAL_PATH)
    events = pd.read_csv(EVENTS_PATH)
    events['season'] = pd.to_datetime(events['date']).dt.month.map(MONTH_TO_SEASON)
    return df, events


def create_chart_for_subbacia(shi_cd, shi_nm, sb_events, sb_params):
    setup_plot_style()

    fig, axes = plt.subplots(1, 4, figsize=(22, 6), sharey=True)

    for col_idx, (season, s_label, s_color) in enumerate(
            zip(SEASON_ORDER, SEASON_LABELS, SEASON_COLORS_LINE)):

        ax = axes[col_idx]
        seas_events = sb_events[sb_events['season'] == season]
        seas_params = sb_params[sb_params['season'] == season]

        esa = seas_events[seas_events['classificacao'] == 'ESA']
        ea  = seas_events[seas_events['classificacao'] == 'EA']

        for ts_col, d_h in zip(TIME_STEP_COLS, DURATION_HOURS):
            vals_esa = esa[ts_col].dropna()
            if not vals_esa.empty:
                ax.scatter(np.full(len(vals_esa), d_h * 0.96), vals_esa,
                           color=COLORS_API['ESA'], s=12, alpha=0.3,
                           zorder=1, marker='s', edgecolors='none')
            vals_ea = ea[ts_col].dropna()
            if not vals_ea.empty:
                ax.scatter(np.full(len(vals_ea), d_h * 1.04), vals_ea,
                           color=COLORS_API['EA'], s=30, alpha=0.85,
                           zorder=2, marker='o', linewidths=0.4, edgecolors='black')

        upper_vals, lower_vals, valid_d = [], [], []
        for ts_col, d_h in zip(TIME_STEP_COLS, DURATION_HOURS):
            row = seas_params[seas_params['time_step_col'] == ts_col]
            if row.empty:
                continue
            row = row.iloc[0]
            u, l = row['upper_tol'], row['lower_tol']
            if not np.isnan(u) and not np.isnan(l):
                upper_vals.append(u)
                lower_vals.append(l)
                valid_d.append(d_h)

        if upper_vals:
            ax.plot(valid_d, upper_vals, color=s_color, linewidth=2,
                    linestyle='-', label='Upper threshold', zorder=5)
            ax.plot(valid_d, lower_vals, color=s_color, linewidth=2,
                    linestyle='--', label='Lower threshold', zorder=5)

        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xticks(DURATION_HOURS)
        ax.set_xticklabels(DURATION_LABELS, fontsize=FONT_SIZES['tick_label'] - 1, rotation=45)
        ax.set_xlabel('Duration', fontsize=FONT_SIZES['axis_label'])
        ax.grid(True, which='both', linestyle='--', alpha=0.3, linewidth=0.5)
        ax.set_axisbelow(True)

        n_ea_s  = len(ea)
        n_esa_s = len(esa)
        has_thr = len(upper_vals) > 0
        suffix  = '' if has_thr else '\n(no threshold)'
        ax.set_title(f'{s_label}\nEA={n_ea_s}  ESA={n_esa_s}{suffix}',
                     fontsize=FONT_SIZES['tick_label'], fontweight='bold', pad=6)

        if col_idx == 0:
            ax.set_ylabel('Intensity (mm h$^{-1}$)', fontsize=FONT_SIZES['axis_label'])

        from matplotlib.lines import Line2D
        handles = [
            Line2D([0],[0], marker='o', color='w', markerfacecolor=COLORS_API['EA'],
                   markersize=7, markeredgecolor='black', markeredgewidth=0.4,
                   label=f'EA (n={n_ea_s})'),
            Line2D([0],[0], marker='s', color='w', markerfacecolor=COLORS_API['ESA'],
                   markersize=5, alpha=0.6, label=f'ESA (n={n_esa_s})'),
        ]
        if upper_vals:
            handles += [
                Line2D([0],[0], color=s_color, linewidth=2, linestyle='-',
                       label='Upper tol.'),
                Line2D([0],[0], color=s_color, linewidth=2, linestyle='--',
                       label='Lower tol.'),
            ]
        ax.legend(handles=handles, loc='upper right',
                  fontsize=FONT_SIZES['legend'] - 1, framealpha=0.9)

    title_name = f'{shi_nm} (shi_cd={shi_cd})' if shi_nm else f'shi_cd={shi_cd}'
    fig.suptitle(f'I-D Thresholds by Season — {title_name}\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                 fontsize=FONT_SIZES['title'], fontweight='bold', y=1.02)

    plt.tight_layout()
    return fig


def main():
    print("=" * 70)
    print("CHART 22: SEASONAL I-D THRESHOLDS PER SUB-BACIA")
    print("=" * 70)

    df, events = load_data()
    subbacia_ids = sorted(df['shi_cd'].unique())
    print(f"  Sub-bacias: {len(subbacia_ids)}")

    out_dir = f'{OUTPUT_DIR}/chart_22_seasonal_id_thresholds'
    os.makedirs(out_dir, exist_ok=True)

    ok, fail = 0, 0
    for shi_cd in subbacia_ids:
        try:
            sb_events = events[events['shi_cd'] == shi_cd]
            sb_params = df[df['shi_cd'] == shi_cd]
            shi_nm    = (sb_params['shi_nm'].iloc[0]
                         if 'shi_nm' in sb_params.columns and not sb_params.empty else '')

            if sb_events.empty:
                print(f"  {shi_cd:03d}: no events, skipping")
                continue

            fig = create_chart_for_subbacia(shi_cd, shi_nm, sb_events, sb_params)
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
