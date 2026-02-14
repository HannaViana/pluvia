#!/usr/bin/env python3
"""
Fit I-D Threshold Parameters for Flood Prediction

This script fits Intensity-Duration threshold curves for each rain gauge station
using Support Vector Machine (SVM) with linear kernel on all I-D points in log-log space.
The approach uses classification (EA vs ESA) to find the optimal decision boundary.
The thresholds follow the power law:
    I = a × D^(-b)

Method:
    - Uses all data points (both EA and ESA)
    - Fits linear SVM classifier in (log(D), log(I)) space
    - Robust to outliers through regularization (C parameter)
    - Handles class imbalance with balanced class weights
    - Extracts decision boundary as threshold curve

The decision boundary is a straight line in log-log space:
    w0 + w1*log(D) + w2*log(I) = 0
Which is projected onto the log(I) axis to obtain the power law: I = a × D^(-b)
Stations where the boundary is near-vertical (cannot be expressed as a valid
power law) are rejected.

For each station, it calculates:
- Threshold parameters (a, b)
- Classification metrics (Precision, Recall, F1)
- Confusion matrix components (TP, FP, FN, TN)
- Sample sizes (n_EA, n_ESA)

Outputs:
    - threshold_parameters.csv: Per-station threshold parameters and metrics
"""

import pandas as pd
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
import os
import warnings

# Suppress sklearn warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# CONFIGURATION
# ==============================================================================

# Input paths
INPUT_DIR = 'data/processed/id_analysis'
PONTOS_ID_PATH = f'{INPUT_DIR}/pontos_id_df.csv'

# Output paths
OUTPUT_PATH = f'{INPUT_DIR}/threshold_parameters.csv'

# Regularization parameter for SVM (higher C = less regularization)
REGULARIZATION_C = 1.0  # Default is 1.0, can increase for more robustness

# Class weights: higher weight on EA (1) penalizes missing flood events more,
# pushing the boundary to classify all EA correctly (high recall) at the cost
# of more ESA false positives.
CLASS_WEIGHTS = {0: 1, 1: 10}

# Minimum ratio |w2|/|w1| to accept the boundary as a valid I-D curve.
# Below this, the boundary is near-vertical in log-log space (separating mostly
# by duration, not intensity) and cannot be expressed as a power law I = a*D^(-b).
MIN_W2_W1_RATIO = 0.05

# ==============================================================================
# FUNCTIONS
# ==============================================================================

def fit_threshold_for_station(station_data):
    """
    Fit I-D threshold curve for a single station using SVM with linear kernel.

    Fits a linear classifier in (log(D), log(I)) space to separate EA from ESA.
    The decision boundary is a straight line in log-log space, which corresponds
    to a power-law threshold curve I = a × D^(-b).

    Returns:
        dict: Dictionary with parameters (a, b) and metrics
    """
    from sklearn.svm import SVC

    # Prepare data
    X = station_data['duracao_h'].values
    y_intensity = station_data['intensidade_max_mm_h'].values
    y_label = (station_data['classificacao'] == 'EA').astype(int).values

    n_EA = y_label.sum()
    n_ESA = len(y_label) - n_EA

    if n_EA == 0 or n_ESA == 0:
        # Need both classes to fit classifier
        return {
            'a': np.nan,
            'b': np.nan,
            'precision': np.nan,
            'recall': np.nan,
            'f1': np.nan,
            'n_EA': int(n_EA),
            'n_ESA': int(n_ESA),
            'TP': 0,
            'FP': 0,
            'FN': 0,
            'TN': 0,
            'success': False,
            'error': 'Need both EA and ESA events'
        }

    try:
        # Transform to log space
        log_D = np.log(X)
        log_I = np.log(y_intensity)

        # Stack features: [log(D), log(I)]
        X_features = np.column_stack([log_D, log_I])

        # Fit linear SVM classifier
        # C controls regularization: lower C = more regularization = more robust to outliers
        # CLASS_WEIGHTS biases toward high EA recall (fewer missed flood events)
        CLASS_WEIGHTS[1] = len(y_label) / len(y_label[y_label == 1])
        svm = SVC(
            kernel='linear',
            C=REGULARIZATION_C,
            class_weight=CLASS_WEIGHTS,
            random_state=42
        )
        svm.fit(X_features, y_label)

        # Extract decision boundary
        # SVM decision boundary: w0 + w1*log(D) + w2*log(I) = 0
        # where w = svm.coef_[0], w0 = svm.intercept_[0]
        w = svm.coef_[0]
        w0 = svm.intercept_[0]

        w1 = w[0]  # coefficient for log(D)
        w2 = w[1]  # coefficient for log(I)

        # Reject near-vertical boundaries that can't be projected onto log(I).
        # When |w2| << |w1|, the boundary separates mostly by duration and
        # division by w2 produces extreme, meaningless a/b values.
        w_norm = np.sqrt(w1**2 + w2**2)
        if w_norm == 0 or abs(w2) / w_norm < MIN_W2_W1_RATIO:
            raise ValueError(
                f"Decision boundary is near-vertical in log-log space "
                f"(|w2|/norm={abs(w2)/w_norm:.4f}), cannot express as I=a*D^(-b)"
            )

        # Project boundary onto log(I) axis:
        # w0 + w1*log(D) + w2*log(I) = 0
        # log(I) = -w0/w2 - (w1/w2)*log(D)
        # This is in form: log(I) = intercept + slope*log(D)
        intercept = -w0 / w2
        slope = -w1 / w2

        # Convert to power law: I = a × D^(-b)
        # log(I) = log(a) - b*log(D)
        # Comparing: intercept = log(a), slope = -b
        b = -slope
        a = np.exp(intercept)

        # Use SVM's own predictions to respect the learned boundary orientation
        y_pred = svm.predict(X_features)

        # Calculate metrics
        n_EA = (y_label == 1).sum()
        n_ESA = (y_label == 0).sum()

        # Confusion matrix
        tn, fp, fn, tp = confusion_matrix(y_label, y_pred).ravel()

        # Classification metrics (handle edge cases)
        if tp + fp > 0:
            precision = precision_score(y_label, y_pred, zero_division=0)
        else:
            precision = 0.0

        if tp + fn > 0:
            recall = recall_score(y_label, y_pred, zero_division=0)
        else:
            recall = 0.0

        if precision + recall > 0:
            f1 = f1_score(y_label, y_pred, zero_division=0)
        else:
            f1 = 0.0

        return {
            'a': a,
            'b': b,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'n_EA': int(n_EA),
            'n_ESA': int(n_ESA),
            'TP': int(tp),
            'FP': int(fp),
            'FN': int(fn),
            'TN': int(tn),
            'success': True,
            'error': None
        }

    except Exception as e:
        return {
            'a': np.nan,
            'b': np.nan,
            'precision': np.nan,
            'recall': np.nan,
            'f1': np.nan,
            'n_EA': int((y_label == 1).sum()),
            'n_ESA': int((y_label == 0).sum()),
            'TP': 0,
            'FP': 0,
            'FN': 0,
            'TN': 0,
            'success': False,
            'error': str(e)
        }


def main():
    """Main execution function"""
    print("="*80)
    print("I-D THRESHOLD FITTING")
    print("="*80)

    # Load data
    print(f"\nLoading data from {PONTOS_ID_PATH}...")
    pontos_id_df = pd.read_csv(PONTOS_ID_PATH)
    print(f"  ✓ Loaded {len(pontos_id_df):,} I-D points")

    # Get unique stations
    station_ids = sorted(pontos_id_df['id_estacao'].unique())
    print(f"\nProcessing {len(station_ids)} stations...")

    # Fit thresholds for each station
    results = []

    for idx, station_id in enumerate(station_ids, 1):
        station_data = pontos_id_df[pontos_id_df['id_estacao'] == station_id]

        if station_data.empty:
            print(f"  [{idx}/{len(station_ids)}] Station {station_id}: No data, skipping")
            continue

        # Fit threshold
        result = fit_threshold_for_station(station_data)
        result['id_estacao'] = station_id
        results.append(result)

        if result['success']:
            print(f"  [{idx}/{len(station_ids)}] Station {station_id}: "
                  f"✓ a={result['a']:.2f}, b={result['b']:.3f}, "
                  f"F1={result['f1']:.3f}, P={result['precision']:.3f}, R={result['recall']:.3f}")
        else:
            print(f"  [{idx}/{len(station_ids)}] Station {station_id}: ✗ Failed - {result['error']}")

    # Convert to DataFrame
    results_df = pd.DataFrame(results)

    # Reorder columns
    columns_order = [
        'id_estacao', 'a', 'b',
        'precision', 'recall', 'f1',
        'n_EA', 'n_ESA',
        'TP', 'FP', 'FN', 'TN'
    ]
    results_df = results_df[columns_order]

    # Save results
    print(f"\nSaving results to {OUTPUT_PATH}...")
    results_df.to_csv(OUTPUT_PATH, index=False, float_format='%.6f')
    print(f"  ✓ Saved threshold parameters for {len(results_df)} stations")

    # Summary statistics
    print("\n" + "="*80)
    print("SUMMARY STATISTICS")
    print("="*80)

    successful = results_df['a'].notna().sum()
    failed = results_df['a'].isna().sum()

    print(f"\nSuccessfully fitted: {successful} stations")
    print(f"Failed: {failed} stations")

    if successful > 0:
        valid_results = results_df[results_df['a'].notna()]

        print(f"\nThreshold Parameters:")
        print(f"  a: mean={valid_results['a'].mean():.2f}, "
              f"median={valid_results['a'].median():.2f}, "
              f"range=[{valid_results['a'].min():.2f}, {valid_results['a'].max():.2f}]")
        print(f"  b: mean={valid_results['b'].mean():.3f}, "
              f"median={valid_results['b'].median():.3f}, "
              f"range=[{valid_results['b'].min():.3f}, {valid_results['b'].max():.3f}]")

        print(f"\nClassification Metrics (mean):")
        print(f"  Precision: {valid_results['precision'].mean():.3f}")
        print(f"  Recall: {valid_results['recall'].mean():.3f}")
        print(f"  F1-score: {valid_results['f1'].mean():.3f}")

        print(f"\nSample Sizes:")
        print(f"  Total EA events: {valid_results['n_EA'].sum():,}")
        print(f"  Total ESA events: {valid_results['n_ESA'].sum():,}")
        print(f"  EA per station (mean): {valid_results['n_EA'].mean():.1f}")
        print(f"  ESA per station (mean): {valid_results['n_ESA'].mean():.1f}")

    print("\n" + "="*80)
    print(f"✓ Threshold fitting completed!")
    print(f"Output: {OUTPUT_PATH}")
    print("="*80 + "\n")


if __name__ == '__main__':
    main()
