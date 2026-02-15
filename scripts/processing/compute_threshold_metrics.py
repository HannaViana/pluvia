#!/usr/bin/env python3
"""
Compute classification metrics for manually defined I-D thresholds.

Reads manual_thresholds.csv (id_estacao, a, b) and pontos_id_df.csv,
classifies each I-D point against the threshold I = a * D^(-b),
computes metrics, and outputs the full threshold_parameters.csv
compatible with chart_12_id_thresholds.py.
"""

import pandas as pd
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
import os

# Paths
ID_ANALYSIS_DIR = 'data/processed/id_analysis'
PONTOS_ID_PATH = f'{ID_ANALYSIS_DIR}/pontos_id_df.csv'
MANUAL_THRESHOLDS_PATH = f'{ID_ANALYSIS_DIR}/manual_thresholds.csv'
OUTPUT_PATH = f'{ID_ANALYSIS_DIR}/threshold_parameters.csv'


def compute_metrics_for_station(station_data, a, b):
    """Compute classification metrics given threshold parameters a, b."""
    D = station_data['duracao_h'].values
    I = station_data['intensidade_max_mm_h'].values
    y_true = (station_data['classificacao'] == 'EA').astype(int).values

    # Predicted EA if I >= a * D^(-b)
    I_threshold = a * (D ** (-b))
    y_pred = (I >= I_threshold).astype(int)

    n_EA = int(y_true.sum())
    n_ESA = int(len(y_true) - n_EA)

    if len(np.unique(y_true)) < 2 or len(np.unique(y_pred)) < 2:
        tn = int(((y_true == 0) & (y_pred == 0)).sum())
        fp = int(((y_true == 0) & (y_pred == 1)).sum())
        fn = int(((y_true == 1) & (y_pred == 0)).sum())
        tp = int(((y_true == 1) & (y_pred == 1)).sum())
    else:
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        tn, fp, fn, tp = int(tn), int(fp), int(fn), int(tp)

    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    return {
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'n_EA': n_EA,
        'n_ESA': n_ESA,
        'TP': tp,
        'FP': fp,
        'FN': fn,
        'TN': tn,
    }


def main():
    print("=" * 70)
    print("COMPUTE THRESHOLD METRICS")
    print("=" * 70)

    if not os.path.exists(MANUAL_THRESHOLDS_PATH):
        print(f"ERROR: {MANUAL_THRESHOLDS_PATH} not found. Save thresholds first.")
        return

    print(f"\nLoading data...")
    pontos_df = pd.read_csv(PONTOS_ID_PATH)
    manual_df = pd.read_csv(MANUAL_THRESHOLDS_PATH)
    print(f"  {len(pontos_df):,} I-D points loaded")
    print(f"  {len(manual_df)} stations with manual thresholds")

    results = []

    for _, row in manual_df.iterrows():
        station_id = int(row['id_estacao'])
        a = row['a']
        b = row['b']

        station_data = pontos_df[pontos_df['id_estacao'] == station_id]

        if station_data.empty or np.isnan(a) or np.isnan(b):
            results.append({
                'id_estacao': station_id,
                'a': a, 'b': b,
                'precision': np.nan, 'recall': np.nan, 'f1': np.nan,
                'n_EA': 0, 'n_ESA': 0,
                'TP': 0, 'FP': 0, 'FN': 0, 'TN': 0,
            })
            print(f"  Station {station_id}: skipped (no data or invalid params)")
            continue

        metrics = compute_metrics_for_station(station_data, a, b)
        result = {'id_estacao': station_id, 'a': a, 'b': b, **metrics}
        results.append(result)
        print(f"  Station {station_id}: P={metrics['precision']:.3f}, "
              f"R={metrics['recall']:.3f}, F1={metrics['f1']:.3f}")

    results_df = pd.DataFrame(results)
    columns_order = ['id_estacao', 'a', 'b', 'precision', 'recall', 'f1',
                     'n_EA', 'n_ESA', 'TP', 'FP', 'FN', 'TN']
    results_df = results_df[columns_order]

    results_df.to_csv(OUTPUT_PATH, index=False, float_format='%.6f')
    print(f"\n✓ Saved to {OUTPUT_PATH}")
    print(f"  {len(results_df)} stations")
    print(f"  Mean F1: {results_df['f1'].mean():.3f}")


if __name__ == '__main__':
    main()
