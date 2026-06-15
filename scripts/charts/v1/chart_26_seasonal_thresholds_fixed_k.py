"""
Chart 26: Seasonal API Threshold Analysis — Summary (Fixed K=0.85)
Three panels:
  (a) POD / FAR / Score by season (bar chart, with annual reference)
  (b) Distribution of lower_tol by season and time-step (box plot)
  (c) Best antecedent days distribution by season (replaces K distribution)
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from config import setup_plot_style, FONT_SIZES, OUTPUT_DIR, STUDY_PERIOD, STUDY_LOCATION

SEASONAL_FK_PATH = 'data/processed/api_analysis_subbacia/api_threshold_parameters_seasonal_fixed_k.csv'
ANNUAL_PATH      = 'data/processed/api_analysis_subbacia/api_threshold_parameters_per_subbacia.csv'

SEASON_ORDER  = ['Verao','Outono','Inverno','Primavera']
SEASON_LABELS = ['Summer\n(DJF)','Autumn\n(MAM)','Winter\n(JJA)','Spring\n(SON)']
SEASON_COLORS = ['#d73027','#fc8d59','#4393c3','#74add1']

TS_ORDER  = ['I_15min','I_30min','I_1h','I_2h','I_3h','I_6h','I_8h','I_10h','I_12h','I_24h']
TS_LABELS = ['15min','30min','1h','2h','3h','6h','8h','10h','12h','24h']

DAYS_VALUES = list(range(1, 11))
DAYS_COLORS = ['#f7fcf5','#e5f5e0','#c7e9c0','#a1d99b','#74c476',
               '#41ab5d','#238b45','#006d2c','#00441b','#002b00']


def load_data():
    df     = pd.read_csv(SEASONAL_FK_PATH)
    annual = pd.read_csv(ANNUAL_PATH)
    valid  = df[df['upper_tol'].notna() & df['POD_lower_tol'].notna()]
    av     = annual[annual['upper_tol'].notna() & annual['POD_lower_tol'].notna()]
    return valid, av


def panel_a_metrics(ax, valid, annual_valid):
    metrics = valid.groupby('season').agg(
        POD=('POD_lower_tol','mean'),
        FAR=('FAR_lower_tol','mean'),
        PPV=('PPV_lower_tol','mean'),
    ).reindex(SEASON_ORDER)
    metrics['Score'] = metrics['POD'] * metrics['PPV'] * (1 - metrics['FAR'])

    ann_pod   = annual_valid['POD_lower_tol'].mean()
    ann_far   = annual_valid['FAR_lower_tol'].mean()
    ann_ppv   = annual_valid['PPV_lower_tol'].mean()
    ann_score = ann_pod * ann_ppv * (1 - ann_far)

    x = np.arange(len(SEASON_ORDER))
    w = 0.22

    ax.bar(x - w, metrics['POD'],   w, label='POD',   color='#2166ac', alpha=0.85)
    bars_far = ax.bar(x,     metrics['FAR'],   w, label='FAR',   color='#d6604d', alpha=0.85)
    ax.bar(x + w, metrics['Score'], w, label='Score', color='#35978f', alpha=0.85)

    ax.axhline(ann_pod,   color='#2166ac', linewidth=1.2, linestyle='--', alpha=0.6)
    ax.axhline(ann_far,   color='#d6604d', linewidth=1.2, linestyle='--', alpha=0.6)
    ax.axhline(ann_score, color='#35978f', linewidth=1.2, linestyle='--', alpha=0.6)

    ax.set_xticks(x)
    ax.set_xticklabels(SEASON_LABELS, fontsize=FONT_SIZES['tick_label'])
    ax.set_ylabel('Value', fontsize=FONT_SIZES['axis_label'])
    ax.set_ylim(0, 1.05)
    ax.legend(fontsize=FONT_SIZES['legend'], framealpha=0.9,
              title='Dashed = annual ref.', title_fontsize=8)
    ax.set_title('(a) Performance metrics by season',
                 fontsize=FONT_SIZES['subtitle'], fontweight='bold')
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)

    for bar in bars_far:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.01,
                f'{h:.2f}', ha='center', va='bottom', fontsize=7)


def panel_b_thresholds(ax, valid, annual_valid):
    ann_means = annual_valid.groupby('time_step_col')['lower_tol'].mean().reindex(TS_ORDER)

    positions_base = np.arange(len(TS_ORDER)) * (len(SEASON_ORDER) + 1.5)
    width = 0.8

    for s_idx, (season, color) in enumerate(zip(SEASON_ORDER, SEASON_COLORS)):
        sv = valid[valid['season'] == season]
        data_by_ts = [sv[sv['time_step_col'] == ts]['lower_tol'].dropna().values
                      for ts in TS_ORDER]
        positions = positions_base + s_idx * width

        ax.boxplot(data_by_ts, positions=positions, widths=width * 0.7,
                   patch_artist=True, showfliers=False,
                   medianprops=dict(color='black', linewidth=1.5),
                   whiskerprops=dict(linewidth=0.8),
                   capprops=dict(linewidth=0.8),
                   boxprops=dict(facecolor=color, alpha=0.7, linewidth=0.8))

    for i, ts in enumerate(TS_ORDER):
        x_center = positions_base[i] + (len(SEASON_ORDER) - 1) * width / 2
        ax.plot([x_center - 1.5, x_center + 1.5],
                [ann_means[ts], ann_means[ts]],
                color='black', linewidth=1.5, linestyle='--', zorder=5)

    tick_positions = positions_base + (len(SEASON_ORDER) - 1) * width / 2
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(TS_LABELS, fontsize=FONT_SIZES['tick_label'], rotation=45)
    ax.set_ylabel('Lower threshold (mm h⁻¹)', fontsize=FONT_SIZES['axis_label'])
    ax.set_yscale('log')
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)

    legend_patches = [mpatches.Patch(facecolor=c, alpha=0.7, label=l)
                      for c, l in zip(SEASON_COLORS, SEASON_LABELS)]
    legend_patches.append(plt.Line2D([0],[0], color='black', linestyle='--',
                                     linewidth=1.5, label='Annual mean'))
    ax.legend(handles=legend_patches, fontsize=FONT_SIZES['legend'],
              ncol=3, framealpha=0.9, loc='upper right')
    ax.set_title('(b) Lower threshold by season and duration',
                 fontsize=FONT_SIZES['subtitle'], fontweight='bold')


def panel_c_antecedent_days(ax, valid):
    """Stacked bar: best_antecedent_days distribution by season."""
    x = np.arange(len(SEASON_ORDER))
    w = 0.55
    bottoms = np.zeros(len(SEASON_ORDER))

    for d_val, d_color in zip(DAYS_VALUES, DAYS_COLORS):
        counts = []
        for s in SEASON_ORDER:
            sv = valid[valid['season'] == s]['best_antecedent_days'].dropna()
            sv = sv[sv > 0]
            pct = (sv == d_val).mean() * 100 if len(sv) > 0 else 0
            counts.append(pct)
        ax.bar(x, counts, w, bottom=bottoms, color=d_color,
               label=f'{d_val}d', alpha=0.9)
        bottoms += np.array(counts)

    ax.set_xticks(x)
    ax.set_xticklabels(SEASON_LABELS, fontsize=FONT_SIZES['tick_label'])
    ax.set_ylabel('% of time-steps', fontsize=FONT_SIZES['axis_label'])
    ax.set_ylim(0, 105)
    ax.legend(fontsize=FONT_SIZES['legend'] - 1, ncol=5, loc='upper right',
              framealpha=0.9, title='Antecedent days')
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)
    ax.set_title('(c) Best antecedent days by season (K=0.85 fixed)',
                 fontsize=FONT_SIZES['subtitle'], fontweight='bold')

    for s_idx, s in enumerate(SEASON_ORDER):
        sv = valid[valid['season'] == s]['best_antecedent_days']
        sv = sv[sv > 0]
        mean_d = sv.mean()
        ax.text(s_idx, 102, f'mean={mean_d:.1f}d', ha='center', va='bottom',
                fontsize=8, fontweight='bold')


def main():
    print("=" * 70)
    print("CHART 26: SEASONAL THRESHOLD SUMMARY (FIXED K=0.85)")
    print("=" * 70)

    setup_plot_style()
    valid, annual_valid = load_data()

    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    panel_a_metrics(axes[0], valid, annual_valid)
    panel_b_thresholds(axes[1], valid, annual_valid)
    panel_c_antecedent_days(axes[2], valid)

    fig.suptitle(f'Seasonal API Rainfall Thresholds (Fixed K=0.85) — {STUDY_LOCATION}, {STUDY_PERIOD}',
                 fontsize=FONT_SIZES['title'], fontweight='bold', y=1.01)
    plt.tight_layout()

    out_dir = f'{OUTPUT_DIR}/chart_26_seasonal_thresholds_fixed_k'
    os.makedirs(out_dir, exist_ok=True)
    out_path = f'{out_dir}/seasonal_summary_fixed_k.png'
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"  Saved: {out_path}")
    print("=" * 70)


if __name__ == '__main__':
    main()
