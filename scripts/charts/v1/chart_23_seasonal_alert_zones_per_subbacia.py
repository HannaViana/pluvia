"""
Chart 23: API Alert Zones by Season — Per Sub-bacia
One figure per sub-bacia with 4 columns (seasons) × 10 rows (time-steps),
using seasonally fitted parameters and API computed with optimal K.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from config import setup_plot_style, FONT_SIZES, OUTPUT_DIR, STUDY_PERIOD, STUDY_LOCATION

SEASONAL_PATH  = 'data/processed/api_analysis_subbacia/api_threshold_parameters_seasonal.csv'
EVENTS_PATH    = 'data/processed/api_analysis_subbacia/api_analysis_events_subbacia.csv'
COMPOSITE_PATH = 'data/processed/api_analysis_subbacia/subbacia_daily_composite_reconstructed.csv'

TIME_STEP_COLS  = ['I_15min','I_30min','I_1h','I_2h','I_3h','I_6h','I_8h','I_10h','I_12h','I_24h']
TS_LABELS       = ['15 min','30 min','1 h','2 h','3 h','6 h','8 h','10 h','12 h','24 h']
MAX_ANT_DAYS    = 10

SEASON_ORDER  = ['Verao','Outono','Inverno','Primavera']
SEASON_LABELS = ['Summer (DJF)','Autumn (MAM)','Winter (JJA)','Spring (SON)']

ZONE_COLORS = {'red':'#d73027','orange':'#fc8d59','yellow':'#fee090','blue':'#91bfdb'}
EA_COLOR  = '#d6604d'
ESA_COLOR = '#333333'

MONTH_TO_SEASON = {12:'Verao',1:'Verao',2:'Verao',
                   3:'Outono',4:'Outono',5:'Outono',
                   6:'Inverno',7:'Inverno',8:'Inverno',
                   9:'Primavera',10:'Primavera',11:'Primavera'}


def compute_api_for_k(events_df, daily_df, k):
    daily_df = daily_df[['date','daily_total_mm']].copy()
    daily_df['date'] = pd.to_datetime(daily_df['date'])
    precip_map = dict(zip(daily_df['date'], daily_df['daily_total_mm'].fillna(0.0)))

    result = events_df.copy()
    dates  = pd.to_datetime(result['date']).values

    for n in range(1, MAX_ANT_DAYS + 1):
        api = np.zeros(len(dates))
        for i in range(1, n + 1):
            shifted = pd.to_datetime(dates) - pd.Timedelta(days=i)
            api += (k ** i) * np.array([precip_map.get(pd.Timestamp(d), 0.0) for d in shifted])
        result[f'_api_{n}d'] = api
    return result


def load_data():
    df        = pd.read_csv(SEASONAL_PATH)
    events    = pd.read_csv(EVENTS_PATH)
    composite = pd.read_csv(COMPOSITE_PATH)
    composite['date'] = pd.to_datetime(composite['date'])
    events['season']  = pd.to_datetime(events['date']).dt.month.map(MONTH_TO_SEASON)
    return df, events, composite


def create_chart_for_subbacia(shi_cd, shi_nm, sb_events, sb_params, sb_composite):
    setup_plot_style()

    n_rows, n_cols = len(TIME_STEP_COLS), len(SEASON_ORDER)
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, 36))

    # Pre-compute API for each unique K per season
    api_cache = {}
    for season in SEASON_ORDER:
        seas_params = sb_params[sb_params['season'] == season]
        seas_events = sb_events[sb_events['season'] == season].copy()
        for k in seas_params['best_k'].dropna().unique():
            key = (season, round(k, 2))
            if key not in api_cache and len(seas_events) > 0:
                api_cache[key] = compute_api_for_k(seas_events, sb_composite, k)

    for row_idx, ts_col in enumerate(TIME_STEP_COLS):
        for col_idx, (season, s_label) in enumerate(zip(SEASON_ORDER, SEASON_LABELS)):
            ax = axes[row_idx, col_idx]

            row = sb_params[(sb_params['season'] == season) &
                            (sb_params['time_step_col'] == ts_col)]
            seas_events = sb_events[sb_events['season'] == season]

            if row.empty or pd.isna(row.iloc[0]['upper_tol']):
                ax.text(0.5, 0.5, 'No data', transform=ax.transAxes,
                        ha='center', va='center', fontsize=8, color='gray')
                ax.set_xticks([])
                ax.set_yticks([])
                if row_idx == 0:
                    ax.set_title(s_label, fontsize=FONT_SIZES['tick_label'],
                                 fontweight='bold')
                continue

            r = row.iloc[0]
            upper_tol   = r['upper_tol']
            lower_tol   = r['lower_tol']
            a, b, c     = r['a'], r['b'], r['c']
            best_days   = int(r['best_antecedent_days']) if not np.isnan(r['best_antecedent_days']) else 0
            best_k      = r['best_k'] if not np.isnan(r['best_k']) else 0

            key = (season, round(best_k, 2))
            if best_k > 0 and key in api_cache and best_days > 0:
                ts_data  = api_cache[key]
                api_col  = f'_api_{best_days}d'
            else:
                ts_data  = seas_events.copy()
                api_col  = 'api_5d'

            valid_mask = ts_data[ts_col].notna() & ts_data[api_col].notna()
            ts_plot    = ts_data[valid_mask]

            if ts_plot.empty:
                ax.text(0.5, 0.5, 'No data', transform=ax.transAxes,
                        ha='center', va='center', fontsize=8, color='gray')
                if row_idx == 0:
                    ax.set_title(s_label, fontsize=FONT_SIZES['tick_label'],
                                 fontweight='bold')
                continue

            intensities     = ts_plot[ts_col].values
            api_values      = ts_plot[api_col].values
            classifications = ts_plot['classificacao'].values

            api_max      = min(100, np.percentile(api_values, 99) * 1.2) if len(api_values) > 0 else 100
            i_max_display = upper_tol * 1.5
            api_range    = np.linspace(0, api_max, 200)

            ax.fill_between(api_range, upper_tol, i_max_display,
                            color=ZONE_COLORS['red'], alpha=0.7, zorder=0)
            ax.fill_between(api_range, 0, lower_tol,
                            color=ZONE_COLORS['blue'], alpha=0.7, zorder=0)

            if not np.isnan(a) and best_days > 0 and best_k > 0:
                curve = np.clip(a * np.exp(b * api_range) + c, lower_tol, upper_tol)
                ax.fill_between(api_range, curve, upper_tol,
                                color=ZONE_COLORS['orange'], alpha=0.7, zorder=0)
                ax.fill_between(api_range, lower_tol, curve,
                                color=ZONE_COLORS['yellow'], alpha=0.7, zorder=0)
                ax.plot(api_range, a * np.exp(b * api_range) + c,
                        color='black', linewidth=1, zorder=4)
            else:
                ax.fill_between(api_range, lower_tol, upper_tol,
                                color=ZONE_COLORS['orange'], alpha=0.5, zorder=0)

            ax.axhline(upper_tol, color='darkred', linewidth=0.8, linestyle='--', zorder=3)
            ax.axhline(lower_tol, color='darkblue', linewidth=0.8, linestyle='--', zorder=3)

            esa_m = classifications == 'ESA'
            ea_m  = classifications == 'EA'
            if esa_m.any():
                ax.scatter(api_values[esa_m], intensities[esa_m],
                           color=ESA_COLOR, s=8, alpha=0.4, zorder=2,
                           marker='s', edgecolors='none')
            if ea_m.any():
                ax.scatter(api_values[ea_m], intensities[ea_m],
                           color=EA_COLOR, s=15, alpha=0.85, zorder=3,
                           marker='o', edgecolors='black', linewidths=0.3)

            ax.set_xlim(0, api_max)
            ax.set_ylim(0, i_max_display)
            ax.tick_params(labelsize=7)

            if row_idx == 0:
                ax.set_title(s_label, fontsize=FONT_SIZES['tick_label'],
                             fontweight='bold', pad=5)
            if col_idx == 0:
                ax.set_ylabel(f'{TS_LABELS[row_idx]}\nI (mm h⁻¹)',
                              fontsize=7, labelpad=3)
            if row_idx == n_rows - 1:
                ax.set_xlabel('API (mm)', fontsize=7)

    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    legend_elements = [
        Patch(facecolor=ZONE_COLORS['red'],    alpha=0.7, label='Red alert'),
        Patch(facecolor=ZONE_COLORS['orange'], alpha=0.7, label='Orange alert'),
        Patch(facecolor=ZONE_COLORS['yellow'], alpha=0.7, label='Yellow alert'),
        Patch(facecolor=ZONE_COLORS['blue'],   alpha=0.7, label='Blue alert'),
        Line2D([0],[0], marker='o', color='w', markerfacecolor=EA_COLOR,
               markersize=6, markeredgecolor='black', markeredgewidth=0.3, label='EA'),
        Line2D([0],[0], marker='s', color='w', markerfacecolor=ESA_COLOR,
               markersize=5, alpha=0.6, label='ESA'),
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=6,
               fontsize=FONT_SIZES['legend'], frameon=True,
               bbox_to_anchor=(0.5, -0.01))

    title_name = f'{shi_nm} (shi_cd={shi_cd})' if shi_nm else f'shi_cd={shi_cd}'
    fig.suptitle(f'API Alert Zones by Season — {title_name}\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                 fontsize=FONT_SIZES['title'], fontweight='bold', y=1.005)

    plt.tight_layout(rect=[0, 0.02, 1, 0.99])
    return fig


def main():
    print("=" * 70)
    print("CHART 23: SEASONAL API ALERT ZONES PER SUB-BACIA")
    print("=" * 70)

    df, events, composite = load_data()
    subbacia_ids = sorted(df['shi_cd'].unique())
    print(f"  Sub-bacias: {len(subbacia_ids)}")

    out_dir = f'{OUTPUT_DIR}/chart_23_seasonal_alert_zones'
    os.makedirs(out_dir, exist_ok=True)

    ok, fail = 0, 0
    for shi_cd in subbacia_ids:
        try:
            sb_events    = events[events['shi_cd'] == shi_cd].copy()
            sb_params    = df[df['shi_cd'] == shi_cd]
            sb_composite = composite[composite['shi_cd'] == shi_cd].copy()
            shi_nm = (sb_params['shi_nm'].iloc[0]
                      if 'shi_nm' in sb_params.columns and not sb_params.empty else '')

            if sb_events.empty:
                print(f"  {shi_cd:03d}: no events, skipping")
                continue

            fig  = create_chart_for_subbacia(shi_cd, shi_nm, sb_events,
                                              sb_params, sb_composite)
            path = f'{out_dir}/subbacia_{shi_cd:03d}.png'
            fig.savefig(path, dpi=150, bbox_inches='tight')
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
