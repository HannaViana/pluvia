#!/usr/bin/env python3
"""
Fit API-based Rainfall Thresholds per Station for Flood Prediction

Same methodology as fit_api_thresholds.py but fits a separate set of threshold
parameters for each station instead of pooling all stations together.

For each station x time-step, fits:
1. Upper/lower I-D thresholds (with tolerance levels)
2. Intermediate exponential curve: I = a * exp(b * API) + c

Outputs:
    - api_threshold_parameters_per_station.csv: fitted parameters per station x time-step
    - api_threshold_metrics_per_station.csv: detailed evaluation metrics
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

TOLERANCE_UPPER_PERCENTILE = 99
TOLERANCE_LOWER_PERCENTILE = 5

GRID_A_SIZE = 50
GRID_B_SIZE = 20
GRID_C_SIZE = 50
B_MIN = -1.0
B_MAX = -0.01


# ==============================================================================
# FUNCTIONS (identical to fit_api_thresholds.py)
# ==============================================================================

def compute_metrics(y_true, y_pred):
    tp = int(((y_true == 1) & (y_pred == 1)).sum())
    fp = int(((y_true == 0) & (y_pred == 1)).sum())
    fn = int(((y_true == 1) & (y_pred == 0)).sum())
    tn = int(((y_true == 0) & (y_pred == 0)).sum())

    pod = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    far = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    ppv = tp / (tp + fp) if (tp + fp) > 0 else 0.0

    return {'POD': pod, 'FAR': far, 'PPV': ppv, 'TP': tp, 'FP': fp, 'FN': fn, 'TN': tn}


def find_thresholds_raw(intensities_ea, intensities_esa):
    if len(intensities_ea) == 0 or len(intensities_esa) == 0:
        return np.nan, np.nan
    upper = intensities_esa.max()
    lower = intensities_ea.min()
    return upper, lower


def apply_tolerance_levels(intensities_ea, intensities_esa, upper_raw, lower_raw):
    upper_tol = np.percentile(intensities_esa, TOLERANCE_UPPER_PERCENTILE)
    lower_tol = np.percentile(intensities_ea, TOLERANCE_LOWER_PERCENTILE)
    if upper_tol <= lower_tol:
        upper_tol = upper_raw
        lower_tol = lower_raw
    return upper_tol, lower_tol


def fit_exponential_curve(intensities, api_values, y_true):
    if len(intensities) < 5 or y_true.sum() < 2 or (y_true == 0).sum() < 2:
        return {'a': np.nan, 'b': np.nan, 'c': np.nan,
                'POD': np.nan, 'FAR': np.nan, 'PPV': np.nan, 'score': np.nan}

    i_ea = intensities[y_true == 1]

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

    for a in a_vals:
        for b in b_vals:
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
    intensities = events_df[intensity_col].values
    api_values = events_df[api_col].values
    y_true = (events_df['classificacao'] == 'EA').astype(int).values

    y_pred = np.zeros(len(intensities), dtype=int)

    above_upper = intensities >= upper_tol
    y_pred[above_upper] = 1

    middle = (~above_upper) & (intensities >= lower_tol)
    if middle.any() and not np.isnan(a):
        i_threshold = a * np.exp(b * api_values[middle]) + c
        y_pred[middle] = (intensities[middle] >= i_threshold).astype(int)

    return compute_metrics(y_true, y_pred)


def fit_station_timestep(station_events, ts_col, ts_label):
    """Fit all thresholds for one station x time-step combination."""
    valid_mask = station_events[ts_col].notna()
    ts_events = station_events[valid_mask].copy()

    empty = {
        'upper_raw': np.nan, 'lower_raw': np.nan,
        'upper_tol': np.nan, 'lower_tol': np.nan,
        'POD_upper_raw': np.nan, 'FAR_upper_raw': np.nan, 'PPV_upper_raw': np.nan,
        'POD_lower_raw': np.nan, 'FAR_lower_raw': np.nan, 'PPV_lower_raw': np.nan,
        'POD_upper_tol': np.nan, 'FAR_upper_tol': np.nan, 'PPV_upper_tol': np.nan,
        'POD_lower_tol': np.nan, 'FAR_lower_tol': np.nan, 'PPV_lower_tol': np.nan,
        'best_antecedent_days': 0,
        'a': np.nan, 'b': np.nan, 'c': np.nan,
        'POD_api': np.nan, 'FAR_api': np.nan, 'PPV_api': np.nan,
    }

    if len(ts_events) < 10:
        return empty, []

    y_true = (ts_events['classificacao'] == 'EA').astype(int)
    i_ea = ts_events.loc[y_true == 1, ts_col]
    i_esa = ts_events.loc[y_true == 0, ts_col]

    if len(i_ea) < 2 or len(i_esa) < 2:
        return empty, []

    upper_raw, lower_raw = find_thresholds_raw(i_ea, i_esa)

    y_pred_upper = (ts_events[ts_col] >= upper_raw).astype(int)
    metrics_upper_raw = compute_metrics(y_true, y_pred_upper)

    y_pred_lower = (ts_events[ts_col] >= lower_raw).astype(int)
    metrics_lower_raw = compute_metrics(y_true, y_pred_lower)

    upper_tol, lower_tol = apply_tolerance_levels(i_ea, i_esa, upper_raw, lower_raw)

    y_pred_upper_tol = (ts_events[ts_col] >= upper_tol).astype(int)
    metrics_upper_tol = compute_metrics(y_true, y_pred_upper_tol)

    y_pred_lower_tol = (ts_events[ts_col] >= lower_tol).astype(int)
    metrics_lower_tol = compute_metrics(y_true, y_pred_lower_tol)

    # Fit intermediate curve
    best_api_result = None
    best_api_days = 0
    best_api_score = -np.inf
    detailed = []

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

            result = fit_exponential_curve(me[ts_col], me[api_col], y_middle)

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

            detailed.append({
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
                           'full_POD': np.nan, 'full_FAR': np.nan, 'full_PPV': np.nan}

    params = {
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
    }

    return params, detailed


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print("=" * 80)
    print("API THRESHOLD FITTING — PER STATION")
    print("=" * 80)

    print(f"\nLoading events from {EVENTS_PATH}...")
    events_df = pd.read_csv(EVENTS_PATH)
    print(f"  Loaded {len(events_df):,} events")
    print(f"  EA: {(events_df['classificacao'] == 'EA').sum():,}")
    print(f"  ESA: {(events_df['classificacao'] == 'ESA').sum():,}")

    station_ids = sorted(events_df['id_estacao'].unique())
    print(f"  Stations: {len(station_ids)}")

    all_results = []
    detailed_metrics = []

    for station_id in tqdm(station_ids, desc="Stations"):
        station_events = events_df[events_df['id_estacao'] == station_id]
        n_ea = (station_events['classificacao'] == 'EA').sum()
        n_esa = (station_events['classificacao'] == 'ESA').sum()

        print(f"\n{'─'*60}")
        print(f"  Station {station_id}  (EA={n_ea}, ESA={n_esa}, total={len(station_events)})")

        for ts_idx, ts_col in enumerate(TIME_STEP_COLS):
            ts_label = TIME_STEP_LABELS[ts_idx]

            params, detailed = fit_station_timestep(station_events, ts_col, ts_label)

            for d in detailed:
                d['id_estacao'] = station_id
            detailed_metrics.extend(detailed)

            fitted = not np.isnan(params['a'])
            status = (f"a={params['a']:.2f}, b={params['b']:.4f}, c={params['c']:.2f}, "
                      f"days={params['best_antecedent_days']}, "
                      f"POD={params['POD_api']:.2%}, FAR={params['FAR_api']:.2%}"
                      if fitted else "no curve fitted")
            print(f"    {ts_label}h: {status}")

            all_results.append({
                'id_estacao': station_id,
                'time_step': ts_label,
                'time_step_col': ts_col,
                **params,
            })

    # Save
    print(f"\n{'='*80}")
    print("SAVING RESULTS")
    print(f"{'='*80}")

    params_df = pd.DataFrame(all_results)
    params_path = f'{OUTPUT_DIR}/api_threshold_parameters_per_station.csv'
    params_df.to_csv(params_path, index=False, float_format='%.6f')
    print(f"  Saved {params_path} ({len(params_df)} rows)")

    if detailed_metrics:
        metrics_df = pd.DataFrame(detailed_metrics)
        metrics_path = f'{OUTPUT_DIR}/api_threshold_metrics_per_station.csv'
        metrics_df.to_csv(metrics_path, index=False, float_format='%.6f')
        print(f"  Saved {metrics_path} ({len(metrics_df)} rows)")

    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    fitted = params_df['a'].notna().sum()
    total = len(params_df)
    print(f"  Fitted curves: {fitted}/{total} station x time-step combinations")
    print(f"  Stations: {len(station_ids)}")
    print(f"  Time-steps: {len(TIME_STEP_COLS)}")
    print(f"\n{'='*80}\n")


if __name__ == '__main__':
    main()
