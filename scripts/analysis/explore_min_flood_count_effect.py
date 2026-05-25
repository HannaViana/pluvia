#!/usr/bin/env python3
"""
Exploratory script: effect of MIN_FLOOD_RECORDS threshold on EA/ESA separability.

Loads pre-processed I-D data and reclassifies events for multiple flood count
thresholds without rerunning the full pipeline. Produces:
  - intensity_distributions.png : KDE grid (one col per duration, one row per threshold)
  - ea_esa_counts.png           : EA/ESA event counts vs threshold
"""

import pathlib
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from scipy.stats import gaussian_kde

# ==============================================================================
# PATHS
# ==============================================================================

_project_root = pathlib.Path(__file__).parent.parent.parent
DATA_DIR = _project_root / 'data' / 'processed' / 'id_analysis'
OUTPUT_DIR = _project_root / 'results' / 'charts' / 'v1' / 'explore_min_flood_count'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ==============================================================================
# PARAMETERS
# ==============================================================================

THRESHOLDS = [1, 2, 3, 5, 10]
DURATIONS_H = [0.25, 0.5, 1.0, 2.0, 3.0, 12.0]
DURATION_LABELS = ['15min', '30min', '1h', '2h', '3h', '12h']

COLORS = {'EA': '#e74c3c', 'ESA': '#3498db'}

# ==============================================================================
# LOAD DATA
# ==============================================================================

print("Loading data...")
pontos = pd.read_csv(DATA_DIR / 'pontos_id_df.csv')
eventos = pd.read_csv(DATA_DIR / 'eventos_unicos.csv')
floods  = pd.read_csv(DATA_DIR / 'floods_with_station.csv')

floods['data_inicio'] = pd.to_datetime(floods['data_inicio'], utc=True)
eventos['start_time'] = pd.to_datetime(eventos['start_time'], utc=True)
eventos['end_time']   = pd.to_datetime(eventos['end_time'],   utc=True)
eventos['id_estacao'] = eventos['id_estacao'].astype(str)
floods['id_estacao']  = floods['id_estacao'].astype(str)

# Pre-compute flood count per rain event (station-filtered temporal overlap)
print("Computing flood counts per rain event...")
merged = pd.merge(eventos[['id_evento_chuva', 'id_estacao', 'start_time', 'end_time']],
                  floods[['data_inicio', 'id_estacao']],
                  on='id_estacao')

overlap = merged[
    (merged['data_inicio'] >= merged['start_time']) &
    (merged['data_inicio'] <  merged['end_time'])
]
flood_counts = overlap.groupby('id_evento_chuva').size().rename('flood_count')

# Attach flood count to unique events (0 if no floods)
eventos = eventos.set_index('id_evento_chuva')
eventos['flood_count'] = flood_counts
eventos['flood_count'] = eventos['flood_count'].fillna(0).astype(int)
eventos = eventos.reset_index()

print(f"  Events with flood_count > 0: {(eventos['flood_count'] > 0).sum()}")
print(f"  flood_count distribution:\n{eventos['flood_count'].value_counts().sort_index().head(10)}")

# ==============================================================================
# RECLASSIFY FOR EACH THRESHOLD
# ==============================================================================

def reclassify(min_flood_records):
    ea_ids = eventos.loc[eventos['flood_count'] >= min_flood_records, 'id_evento_chuva']
    result = pontos.copy()
    result['classificacao'] = 'ESA'
    result.loc[result['id_evento_chuva'].isin(ea_ids), 'classificacao'] = 'EA'
    return result


# ==============================================================================
# PLOT 1: KDE intensity distributions (grid: rows=thresholds, cols=durations)
# ==============================================================================

print("\nPlotting intensity distributions...")

n_rows = len(THRESHOLDS)
n_cols = len(DURATIONS_H)

fig, axes = plt.subplots(n_rows, n_cols, figsize=(4 * n_cols, 3 * n_rows),
                          sharex=False, sharey=False)
fig.suptitle('EA vs ESA Intensity Distributions by MIN_FLOOD_RECORDS threshold',
             fontsize=14, y=1.01)

for r, thresh in enumerate(THRESHOLDS):
    df = reclassify(thresh)
    n_ea  = (df['id_evento_chuva'].isin(
        eventos.loc[eventos['flood_count'] >= thresh, 'id_evento_chuva'])).sum() // n_cols
    # unique event counts
    ev_classified = df.drop_duplicates('id_evento_chuva')
    n_ea_ev  = (ev_classified['classificacao'] == 'EA').sum()
    n_esa_ev = (ev_classified['classificacao'] == 'ESA').sum()

    for c, (dur, dur_label) in enumerate(zip(DURATIONS_H, DURATION_LABELS)):
        ax = axes[r][c]
        subset = df[df['duracao_h'] == dur]

        ea_vals  = subset.loc[subset['classificacao'] == 'EA',  'intensidade_max_mm_h'].dropna()
        esa_vals = subset.loc[subset['classificacao'] == 'ESA', 'intensidade_max_mm_h'].dropna()

        x_max = subset['intensidade_max_mm_h'].quantile(0.99)
        x = np.linspace(0, x_max, 300)

        for vals, label in [(esa_vals, 'ESA'), (ea_vals, 'EA')]:
            if len(vals) >= 5:
                kde = gaussian_kde(vals, bw_method='scott')
                ax.fill_between(x, kde(x), alpha=0.35, color=COLORS[label])
                ax.plot(x, kde(x), color=COLORS[label], linewidth=1.5, label=label)

        ax.set_xlim(0, x_max)
        ax.set_xlabel('Intensity (mm/h)', fontsize=8)
        ax.set_ylabel('Density', fontsize=8)
        ax.tick_params(labelsize=7)

        if r == 0:
            ax.set_title(dur_label, fontsize=10, fontweight='bold')
        if c == 0:
            ax.set_ylabel(f'min_floods≥{thresh}\n(EA={n_ea_ev}, ESA={n_esa_ev})\nDensity', fontsize=8)

        if r == 0 and c == n_cols - 1:
            ax.legend(fontsize=7)

plt.tight_layout()
out_path = OUTPUT_DIR / 'intensity_distributions.png'
plt.savefig(out_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"  Saved: {out_path}")


# ==============================================================================
# PLOT 2: EA/ESA event counts vs threshold
# ==============================================================================

print("Plotting event counts vs threshold...")

counts = []
for thresh in THRESHOLDS:
    df = reclassify(thresh)
    ev = df.drop_duplicates('id_evento_chuva')
    counts.append({
        'threshold': thresh,
        'EA':  (ev['classificacao'] == 'EA').sum(),
        'ESA': (ev['classificacao'] == 'ESA').sum(),
    })
counts_df = pd.DataFrame(counts)

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(counts_df['threshold'], counts_df['EA'],  marker='o', color=COLORS['EA'],  label='EA')
ax.plot(counts_df['threshold'], counts_df['ESA'], marker='o', color=COLORS['ESA'], label='ESA')

for _, row in counts_df.iterrows():
    ax.annotate(str(row['EA']),  (row['threshold'], row['EA']),
                textcoords='offset points', xytext=(0, 6), fontsize=8, color=COLORS['EA'])
    ax.annotate(str(row['ESA']), (row['threshold'], row['ESA']),
                textcoords='offset points', xytext=(0, 6), fontsize=8, color=COLORS['ESA'])

ax.set_xlabel('MIN_FLOOD_RECORDS threshold', fontsize=11)
ax.set_ylabel('Number of unique rain events', fontsize=11)
ax.set_title('EA and ESA event counts vs MIN_FLOOD_RECORDS', fontsize=12)
ax.set_xticks(THRESHOLDS)
ax.legend(fontsize=10)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
out_path = OUTPUT_DIR / 'ea_esa_counts.png'
plt.savefig(out_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"  Saved: {out_path}")

print("\nDone.")
