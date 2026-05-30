"""
Chart 19: Peak Rainfall Intensity vs API Alert Zones — Per Sub-bacia (Optimized K)
Like chart_17 but uses the per-sub-bacia optimized K decay coefficient to compute
API values from the reconstructed daily composite precipitation series.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from config import (setup_plot_style, FONT_SIZES,
                    OUTPUT_DIR, STUDY_PERIOD, STUDY_LOCATION)

API_ANALYSIS_DIR = 'data/processed/api_analysis_subbacia'
EVENTS_PATH = f'{API_ANALYSIS_DIR}/api_analysis_events_subbacia.csv'
THRESHOLDS_PATH = f'{API_ANALYSIS_DIR}/api_threshold_parameters_per_subbacia.csv'
COMPOSITE_PATH = f'{API_ANALYSIS_DIR}/subbacia_daily_composite_reconstructed.csv'

TIME_STEP_COLS = ['I_15min', 'I_30min', 'I_1h', 'I_2h', 'I_3h',
                  'I_6h', 'I_8h', 'I_10h', 'I_12h', 'I_24h']
DURATION_LABELS = ['15 min', '30 min', '1 hour', '2 hours', '3 hours',
                   '6 hours', '8 hours', '10 hours', '12 hours', '24 hours']
MAX_ANTECEDENT_DAYS = 10

ZONE_COLORS = {
    'red': '#d73027',
    'orange': '#fc8d59',
    'yellow': '#fee090',
    'blue': '#91bfdb',
}
EA_COLOR = '#d6604d'
ESA_COLOR = '#333333'


def compute_api_for_k(events_df, daily_df, k):
    """Compute API columns for a given K using reconstructed daily composite."""
    daily_df = daily_df[['date', 'daily_total_mm']].copy()
    daily_df['date'] = pd.to_datetime(daily_df['date'])
    precip_map = dict(zip(daily_df['date'], daily_df['daily_total_mm'].fillna(0.0)))

    result = events_df.copy()
    dates = pd.to_datetime(result['date']).values

    for n_days in range(1, MAX_ANTECEDENT_DAYS + 1):
        api_values = np.zeros(len(dates))
        for i in range(1, n_days + 1):
            shifted = pd.to_datetime(dates) - pd.Timedelta(days=i)
            api_values += (k ** i) * np.array(
                [precip_map.get(pd.Timestamp(d), 0.0) for d in shifted]
            )
        result[f'_api_{n_days}d'] = api_values

    return result


def load_data():
    events_df = pd.read_csv(EVENTS_PATH)
    thresholds_df = pd.read_csv(THRESHOLDS_PATH)
    composite_df = pd.read_csv(COMPOSITE_PATH)
    composite_df['date'] = pd.to_datetime(composite_df['date'])
    return events_df, thresholds_df, composite_df


def create_alert_zone_chart_for_subbacia(shi_cd, shi_nm, subbacia_events,
                                          subbacia_params, subbacia_composite):
    """Create 2x5 grid of I vs API panels using optimized K per time step."""
    setup_plot_style()

    n_cols = 5
    n_rows = 2
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, 8))
    axes = axes.flatten()

    # Pre-compute API for each unique K used in this sub-basin
    unique_ks = subbacia_params['best_k'].dropna().unique()
    api_cache = {}
    for k in unique_ks:
        if not np.isnan(k) and k > 0:
            api_cache[k] = compute_api_for_k(subbacia_events, subbacia_composite, k)

    for idx, ts_col in enumerate(TIME_STEP_COLS):
        ax = axes[idx]
        ts_label = DURATION_LABELS[idx]

        row = subbacia_params[subbacia_params['time_step_col'] == ts_col]
        if row.empty:
            ax.text(0.5, 0.5, 'No data', transform=ax.transAxes,
                    ha='center', va='center')
            ax.set_title(ts_label, fontsize=FONT_SIZES['tick_label'], fontweight='bold')
            continue

        row = row.iloc[0]
        upper_tol = row['upper_tol']
        lower_tol = row['lower_tol']
        a = row['a']
        b = row['b']
        c = row['c']
        best_days = int(row['best_antecedent_days']) if not np.isnan(row['best_antecedent_days']) else 0
        best_k = row['best_k'] if not np.isnan(row['best_k']) else 0

        if np.isnan(upper_tol) or np.isnan(lower_tol):
            ax.text(0.5, 0.5, 'Insufficient data', transform=ax.transAxes,
                    ha='center', va='center', fontsize=8)
            ax.set_title(ts_label, fontsize=FONT_SIZES['tick_label'], fontweight='bold')
            continue

        # Get events with API computed at the optimal K
        if best_k > 0 and best_k in api_cache and best_days > 0:
            ts_data = api_cache[best_k]
            api_col = f'_api_{best_days}d'
        else:
            ts_data = subbacia_events.copy()
            api_col = 'api_5d'  # fallback to stored K=0.85 value

        valid_mask = ts_data[ts_col].notna() & ts_data[api_col].notna()
        ts_plot = ts_data[valid_mask].copy()

        intensities = ts_plot[ts_col].values
        api_values = ts_plot[api_col].values
        classifications = ts_plot['classificacao'].values

        api_min = 0
        api_max = min(100, np.percentile(api_values, 99) * 1.2) if len(api_values) > 0 else 100
        i_min = 0
        i_max_display = upper_tol * 1.5

        api_range = np.linspace(api_min, api_max, 200)

        # Fill alert zones
        ax.fill_between(api_range, upper_tol, i_max_display,
                        color=ZONE_COLORS['red'], alpha=0.7, zorder=0)
        ax.fill_between(api_range, i_min, lower_tol,
                        color=ZONE_COLORS['blue'], alpha=0.7, zorder=0)

        if not np.isnan(a) and best_days > 0 and best_k > 0:
            i_curve = a * np.exp(b * api_range) + c
            i_curve = np.clip(i_curve, lower_tol, upper_tol)

            ax.fill_between(api_range, i_curve, upper_tol,
                            color=ZONE_COLORS['orange'], alpha=0.7, zorder=0)
            ax.fill_between(api_range, lower_tol, i_curve,
                            color=ZONE_COLORS['yellow'], alpha=0.7, zorder=0)
            ax.plot(api_range, a * np.exp(b * api_range) + c,
                    color='black', linewidth=1.5, zorder=4)

            eq_text = f'I = {a:.1f}e$^{{{b:.2f}\\cdot API}}$ + {c:.1f}\nK={best_k:.2f}'
            ax.text(0.95, 0.08, eq_text, transform=ax.transAxes,
                    fontsize=7, ha='right', va='bottom',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
        else:
            ax.fill_between(api_range, lower_tol, upper_tol,
                            color=ZONE_COLORS['orange'], alpha=0.5, zorder=0)

        ax.axhline(upper_tol, color='darkred', linewidth=1, linestyle='--', zorder=3)
        ax.axhline(lower_tol, color='darkblue', linewidth=1, linestyle='--', zorder=3)

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

        k_label = f' (K={best_k:.2f})' if best_k > 0 else ''
        title = (f'{ts_label} × {best_days}d{k_label}'
                 if best_days > 0 else ts_label)
        ax.set_title(title, fontsize=FONT_SIZES['tick_label'], fontweight='bold', pad=5)

        if idx >= n_cols * (n_rows - 1):
            ax.set_xlabel('API (mm)', fontsize=FONT_SIZES['tick_label'])
        if idx % n_cols == 0:
            ax.set_ylabel('Intensity (mm h$^{-1}$)', fontsize=FONT_SIZES['tick_label'])

        ax.tick_params(labelsize=8)

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

    title_name = f'{shi_nm} (shi_cd={shi_cd})' if shi_nm else f'shi_cd={shi_cd}'
    fig.suptitle(f'Peak Rainfall Intensity vs API — {title_name} [Optimized K]\n'
                 f'{STUDY_LOCATION}, {STUDY_PERIOD}',
                 fontsize=FONT_SIZES['title'], fontweight='bold', y=1.01)

    plt.tight_layout(rect=[0, 0.04, 1, 0.98])
    return fig


def main():
    print("=" * 70)
    print("CHART 19: API ALERT ZONES PER SUB-BACIA (OPTIMIZED K)")
    print("=" * 70)

    events_df, thresholds_df, composite_df = load_data()
    print(f"  Events: {len(events_df):,}")
    print(f"  Sub-bacias: {thresholds_df['shi_cd'].nunique()}")
    print(f"  Composite rows: {len(composite_df):,}")

    chart_output_dir = f'{OUTPUT_DIR}/chart_19_api_alert_zones_per_subbacia_v2'
    os.makedirs(chart_output_dir, exist_ok=True)

    subbacia_ids = sorted(thresholds_df['shi_cd'].unique())
    successful = 0
    failed = 0

    for shi_cd in subbacia_ids:
        try:
            subbacia_events = events_df[events_df['shi_cd'] == shi_cd].copy()
            subbacia_params = thresholds_df[thresholds_df['shi_cd'] == shi_cd]
            subbacia_composite = composite_df[composite_df['shi_cd'] == shi_cd].copy()
            shi_nm = (subbacia_params['shi_nm'].iloc[0]
                      if 'shi_nm' in subbacia_params.columns and not subbacia_params.empty else '')

            if subbacia_events.empty:
                print(f"  Sub-bacia {shi_cd:03d}: no events, skipping")
                continue

            fig = create_alert_zone_chart_for_subbacia(
                shi_cd, shi_nm, subbacia_events, subbacia_params, subbacia_composite
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
