#!/usr/bin/env python3
"""
Fit API-based Rainfall Thresholds for Flood Prediction

Implements the improved threshold methodology from Geraldo Moura Ramos Filho (2021):
1. Upper/lower I-D thresholds (peak intensity vs duration)
2. Tolerance levels (99th percentile upper, 5% lower)
3. Intermediate threshold using exponential curve: I = a * exp(b * API) + c

For each time-step, fits thresholds and selects the best antecedent days
for the API-based intermediate curve.

Outputs:
    - api_threshold_parameters.csv: fitted parameters per time-step
    - api_threshold_metrics.csv: detailed evaluation metrics
"""

import os
import pathlib
import pandas as pd
import numpy as np
from tqdm.auto import tqdm

# ==============================================================================
# CONFIGURATION
# ==============================================================================

_project_root = pathlib.Path(__file__).parent.parent.parent

INPUT_DIR = str(_project_root / 'data' / 'processed' / 'api_analysis')
OUTPUT_DIR = INPUT_DIR

EVENTS_PATH = f'{INPUT_DIR}/api_analysis_events.csv'

TIME_STEP_COLS = ['I_15min', 'I_30min', 'I_1h', 'I_2h', 'I_3h',
                  'I_6h', 'I_8h', 'I_10h', 'I_12h', 'I_24h']
TIME_STEP_LABELS = ['1/6', '1/2', '1', '2', '3', '6', '8', '10', '12', '24']
MAX_ANTECEDENT_DAYS = 10

# Tolerance level parameters
TOLERANCE_UPPER_PERCENTILE = 99
TOLERANCE_LOWER_PERCENTILE = 5

# Grid search parameters for exponential curve
GRID_A_SIZE = 50
GRID_B_SIZE = 20
GRID_C_SIZE = 50
B_MIN = -1.0
B_MAX = -0.01


# ==============================================================================
# FUNCTIONS
# ==============================================================================

def compute_metrics(y_true, y_pred):
    """
    Compute POD, FAR, PPV as defined in Geraldo Moura's thesis.

    POD = TP / (TP + FN)  -- probability of detection
    FAR = FP / (FP + TN)  -- false alarm ratio (thesis definition)
    PPV = TP / (TP + FP)  -- positive predictive value
    """
    tp = int(((y_true == 1) & (y_pred == 1)).sum())
    fp = int(((y_true == 0) & (y_pred == 1)).sum())
    fn = int(((y_true == 1) & (y_pred == 0)).sum())
    tn = int(((y_true == 0) & (y_pred == 0)).sum())

    pod = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    far = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    ppv = tp / (tp + fp) if (tp + fp) > 0 else 0.0

    return {'POD': pod, 'FAR': far, 'PPV': ppv, 'TP': tp, 'FP': fp, 'FN': fn, 'TN': tn}


def find_thresholds_raw(intensities_ea, intensities_esa):
    """
    Find raw upper and lower thresholds without tolerance levels.

    Upper: minimum intensity above which only EA events exist (0% FAR above it)
    Lower: maximum intensity below which only ESA events exist (100% POD above it)
    """
    if len(intensities_ea) == 0 or len(intensities_esa) == 0:
        return np.nan, np.nan

    # Upper threshold: smallest intensity above which no ESA exists
    # = max of all ESA values (anything above this is purely EA)
    upper = intensities_esa.max()

    # Lower threshold: largest intensity below which no EA exists
    # = min of all EA values (anything below this is purely ESA)
    lower = intensities_ea.min()

    return upper, lower


def apply_tolerance_levels(intensities_ea, intensities_esa, upper_raw, lower_raw):
    """
    Apply tolerance levels to reduce the uncertainty zone.

    Upper tolerance (99th percentile): new upper = 99th percentile of ESA values
        (allows 1% of non-occurrences above the new upper threshold)
    Lower tolerance (5%): new lower = 5th percentile of EA values
        (leaves 5% of occurrences below the new lower threshold)
    """
    # Upper with tolerance: 99th percentile of non-occurrences
    upper_tol = np.percentile(intensities_esa, TOLERANCE_UPPER_PERCENTILE)

    # Lower with tolerance: 5th percentile of occurrences
    lower_tol = np.percentile(intensities_ea, TOLERANCE_LOWER_PERCENTILE)

    # Ensure upper > lower
    if upper_tol <= lower_tol:
        upper_tol = upper_raw
        lower_tol = lower_raw

    return upper_tol, lower_tol


def fit_exponential_curve(intensities, api_values, y_true):
    """
    Fit intermediate threshold: I = a * exp(b * API) + c via grid search.

    The curve separates EA from ESA in the middle zone.
    Events above the curve are predicted as EA.

    Returns:
        dict with best (a, b, c) parameters and associated metrics
    """
    if len(intensities) < 5 or y_true.sum() < 2 or (y_true == 0).sum() < 2:
        return {'a': np.nan, 'b': np.nan, 'c': np.nan,
                'POD': np.nan, 'FAR': np.nan, 'PPV': np.nan, 'score': np.nan}

    i_ea = intensities[y_true == 1]

    # Define grid ranges
    a_min = max(0.1, i_ea.min() * 0.1)
    a_max = i_ea.max() * 3.0
    c_min = 0.0
    c_max = i_ea.mean()

    a_vals = np.linspace(a_min, a_max, GRID_A_SIZE)
    b_vals = np.linspace(B_MIN, B_MAX, GRID_B_SIZE)
    c_vals = np.linspace(c_min, c_max, GRID_C_SIZE)

    best_score = -np.inf
    best_params = {'a': np.nan, 'b': np.nan, 'c': np.nan}
    best_metrics = {'POD': 0, 'FAR': 1, 'PPV': 0}

    intensities_arr = intensities.values
    api_arr = api_values.values
    y_true_arr = y_true.values

    n_ea = y_true_arr.sum()
    n_esa = len(y_true_arr) - n_ea

    for a in a_vals:
        for b in b_vals:
            # Vectorized: compute threshold for all API values at once
            i_threshold = a * np.exp(b * api_arr) + c_vals[0]

            for c in c_vals:
                i_threshold = a * np.exp(b * api_arr) + c
                y_pred = (intensities_arr >= i_threshold).astype(int)

                tp = ((y_true_arr == 1) & (y_pred == 1)).sum()
                fp = ((y_true_arr == 0) & (y_pred == 1)).sum()
                fn = ((y_true_arr == 1) & (y_pred == 0)).sum()
                tn = ((y_true_arr == 0) & (y_pred == 0)).sum()

                pod = tp / (tp + fn) if (tp + fn) > 0 else 0.0
                far = fp / (fp + tn) if (fp + tn) > 0 else 0.0
                ppv = tp / (tp + fp) if (tp + fp) > 0 else 0.0

                score = pod * ppv * (1 - far)

                if score > best_score:
                    best_score = score
                    best_params = {'a': a, 'b': b, 'c': c}
                    best_metrics = {'POD': pod, 'FAR': far, 'PPV': ppv}

    return {**best_params, **best_metrics, 'score': best_score}


def evaluate_full_system(events_df, intensity_col, upper_tol, lower_tol,
                         api_col, a, b, c):
    """
    Evaluate the complete 3-threshold system:
    - Above upper_tol: predict EA
    - Below lower_tol: predict ESA
    - Middle zone: use exponential curve I = a*exp(b*API) + c
    """
    intensities = events_df[intensity_col].values
    api_values = events_df[api_col].values
    y_true = (events_df['classificacao'] == 'EA').astype(int).values

    y_pred = np.zeros(len(intensities), dtype=int)

    # Above upper -> predict EA
    above_upper = intensities >= upper_tol
    y_pred[above_upper] = 1

    # Below lower -> predict ESA (already 0)

    # Middle zone -> use exponential curve
    middle = (~above_upper) & (intensities >= lower_tol)
    if middle.any() and not np.isnan(a):
        i_threshold = a * np.exp(b * api_values[middle]) + c
        y_pred[middle] = (intensities[middle] >= i_threshold).astype(int)

    return compute_metrics(y_true, y_pred)


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print("=" * 80)
    print("API THRESHOLD FITTING")
    print("=" * 80)

    # Load data
    print(f"\nLoading events from {EVENTS_PATH}...")
    events_df = pd.read_csv(EVENTS_PATH)
    print(f"  Loaded {len(events_df):,} events")
    print(f"  EA: {(events_df['classificacao'] == 'EA').sum():,}")
    print(f"  ESA: {(events_df['classificacao'] == 'ESA').sum():,}")

    # Results storage
    all_results = []
    detailed_metrics = []

    # Process each time-step
    print(f"\nFitting thresholds for {len(TIME_STEP_COLS)} time-steps...")
    for ts_idx, ts_col in enumerate(TIME_STEP_COLS):
        ts_label = TIME_STEP_LABELS[ts_idx]
        print(f"\n{'─'*60}")
        print(f"  Time-step: {ts_label} h ({ts_col})")

        intensities = events_df[ts_col].dropna()
        valid_mask = events_df[ts_col].notna()
        ts_events = events_df[valid_mask].copy()

        if len(ts_events) < 10:
            print(f"    Skipping: insufficient data")
            continue

        y_true = (ts_events['classificacao'] == 'EA').astype(int)
        i_ea = ts_events.loc[y_true == 1, ts_col]
        i_esa = ts_events.loc[y_true == 0, ts_col]

        if len(i_ea) < 2 or len(i_esa) < 2:
            print(f"    Skipping: need both EA and ESA events")
            continue

        # Raw thresholds
        upper_raw, lower_raw = find_thresholds_raw(i_ea, i_esa)
        print(f"    Raw thresholds: upper={upper_raw:.2f}, lower={lower_raw:.2f}")

        # Metrics without tolerance
        y_pred_upper = (ts_events[ts_col] >= upper_raw).astype(int)
        metrics_upper_raw = compute_metrics(y_true, y_pred_upper)

        y_pred_lower = (ts_events[ts_col] >= lower_raw).astype(int)
        metrics_lower_raw = compute_metrics(y_true, y_pred_lower)

        # Tolerance levels
        upper_tol, lower_tol = apply_tolerance_levels(i_ea, i_esa, upper_raw, lower_raw)
        print(f"    Tolerance thresholds: upper={upper_tol:.2f}, lower={lower_tol:.2f}")

        # Metrics with tolerance (upper)
        y_pred_upper_tol = (ts_events[ts_col] >= upper_tol).astype(int)
        metrics_upper_tol = compute_metrics(y_true, y_pred_upper_tol)

        # Metrics with tolerance (lower)
        y_pred_lower_tol = (ts_events[ts_col] >= lower_tol).astype(int)
        metrics_lower_tol = compute_metrics(y_true, y_pred_lower_tol)

        # Fit intermediate curve for each antecedent_days
        best_api_result = None
        best_api_days = 0
        best_api_score = -np.inf

        # Middle zone events
        middle_mask = (ts_events[ts_col] >= lower_tol) & (ts_events[ts_col] < upper_tol)
        middle_events = ts_events[middle_mask]

        if len(middle_events) >= 10:
            for n_days in range(1, MAX_ANTECEDENT_DAYS + 1):
                api_col = f'api_{n_days}d'
                if api_col not in middle_events.columns:
                    continue

                valid_api = middle_events[api_col].notna()
                me = middle_events[valid_api]

                if len(me) < 5:
                    continue

                y_middle = (me['classificacao'] == 'EA').astype(int)
                if y_middle.sum() < 2 or (y_middle == 0).sum() < 2:
                    continue

                result = fit_exponential_curve(
                    me[ts_col], me[api_col], y_middle
                )

                # Evaluate full system with this API
                if not np.isnan(result['a']):
                    full_valid = ts_events[ts_events[api_col].notna()]
                    full_metrics = evaluate_full_system(
                        full_valid, ts_col, upper_tol, lower_tol,
                        api_col, result['a'], result['b'], result['c']
                    )
                    result['full_POD'] = full_metrics['POD']
                    result['full_FAR'] = full_metrics['FAR']
                    result['full_PPV'] = full_metrics['PPV']
                else:
                    result['full_POD'] = np.nan
                    result['full_FAR'] = np.nan
                    result['full_PPV'] = np.nan

                detailed_metrics.append({
                    'time_step': ts_label,
                    'time_step_col': ts_col,
                    'antecedent_days': n_days,
                    **result
                })

                if result['score'] > best_api_score:
                    best_api_score = result['score']
                    best_api_result = result
                    best_api_days = n_days

        if best_api_result is None:
            best_api_result = {'a': np.nan, 'b': np.nan, 'c': np.nan,
                               'POD': np.nan, 'FAR': np.nan, 'PPV': np.nan,
                               'full_POD': np.nan, 'full_FAR': np.nan, 'full_PPV': np.nan}

        print(f"    Best API: {best_api_days} days "
              f"(a={best_api_result['a']:.2f}, b={best_api_result['b']:.4f}, "
              f"c={best_api_result['c']:.2f})" if not np.isnan(best_api_result.get('a', np.nan)) else
              f"    Best API: none fitted")
        print(f"    Full system POD={best_api_result.get('full_POD', 0):.2%}, "
              f"FAR={best_api_result.get('full_FAR', 0):.2%}, "
              f"PPV={best_api_result.get('full_PPV', 0):.2%}")

        all_results.append({
            'time_step': ts_label,
            'time_step_col': ts_col,
            'upper_raw': upper_raw,
            'lower_raw': lower_raw,
            'upper_tol': upper_tol,
            'lower_tol': lower_tol,
            'POD_upper_raw': metrics_upper_raw['POD'],
            'FAR_upper_raw': metrics_upper_raw['FAR'],
            'PPV_upper_raw': metrics_upper_raw['PPV'],
            'POD_lower_raw': metrics_lower_raw['POD'],
            'FAR_lower_raw': metrics_lower_raw['FAR'],
            'PPV_lower_raw': metrics_lower_raw['PPV'],
            'POD_upper_tol': metrics_upper_tol['POD'],
            'FAR_upper_tol': metrics_upper_tol['FAR'],
            'PPV_upper_tol': metrics_upper_tol['PPV'],
            'POD_lower_tol': metrics_lower_tol['POD'],
            'FAR_lower_tol': metrics_lower_tol['FAR'],
            'PPV_lower_tol': metrics_lower_tol['PPV'],
            'best_antecedent_days': best_api_days,
            'a': best_api_result['a'],
            'b': best_api_result['b'],
            'c': best_api_result['c'],
            'POD_api': best_api_result.get('full_POD', np.nan),
            'FAR_api': best_api_result.get('full_FAR', np.nan),
            'PPV_api': best_api_result.get('full_PPV', np.nan),
        })

    # Save results
    print(f"\n{'='*80}")
    print("SAVING RESULTS")
    print(f"{'='*80}")

    params_df = pd.DataFrame(all_results)
    params_path = f'{OUTPUT_DIR}/api_threshold_parameters.csv'
    params_df.to_csv(params_path, index=False, float_format='%.6f')
    print(f"  Saved {params_path} ({len(params_df)} time-steps)")

    if detailed_metrics:
        metrics_df = pd.DataFrame(detailed_metrics)
        metrics_path = f'{OUTPUT_DIR}/api_threshold_metrics.csv'
        metrics_df.to_csv(metrics_path, index=False, float_format='%.6f')
        print(f"  Saved {metrics_path} ({len(metrics_df)} rows)")

    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    if not params_df.empty:
        valid = params_df[params_df['a'].notna()]
        print(f"  Successfully fitted: {len(valid)}/{len(params_df)} time-steps")
        if not valid.empty:
            best_row = valid.loc[valid['POD_api'].idxmax()] if valid['POD_api'].notna().any() else valid.iloc[0]
            print(f"\n  Best overall: {best_row['time_step']}h x {int(best_row['best_antecedent_days'])} days")
            print(f"    I = {best_row['a']:.2f} * exp({best_row['b']:.4f} * API) + {best_row['c']:.2f}")
            print(f"    POD={best_row['POD_api']:.2%}, FAR={best_row['FAR_api']:.2%}, PPV={best_row['PPV_api']:.2%}")
    print(f"\n{'='*80}\n")


if __name__ == '__main__':
    main()
