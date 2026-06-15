#!/usr/bin/env python3
"""
Fit API-based Rainfall Thresholds per Sub-bacia — Seasonal Split, Fixed K

Same methodology as fit_api_thresholds_per_subbacia.py (remote main) but adds
seasonal separation:
    - Verão   (Summer): DJF — December, January, February
    - Outono  (Autumn): MAM — March, April, May
    - Inverno (Winter): JJA — June, July, August
    - Primavera (Spring): SON — September, October, November

API values (api_1d … api_10d) are read directly from the events CSV —
already pre-computed with fixed K, identical to the annual analysis.
No K grid search; only antecedent days (1–10) are searched.

Outputs:
    api_threshold_parameters_seasonal_fixed_k.csv — fitted parameters per
        sub-bacia × season × time-step
    api_threshold_metrics_seasonal_fixed_k.csv    — detailed evaluation metrics
"""

import pathlib
import pandas as pd
import numpy as np
from tqdm.auto import tqdm

# ==============================================================================
# CONFIGURATION
# ==============================================================================

_project_root = pathlib.Path(__file__).parent.parent.parent

INPUT_DIR  = str(_project_root / 'data' / 'processed' / 'api_analysis_subbacia')
OUTPUT_DIR = INPUT_DIR

EVENTS_PATH = f'{INPUT_DIR}/api_analysis_events_subbacia.csv'

TIME_STEP_COLS   = ['I_15min', 'I_30min', 'I_1h', 'I_2h', 'I_3h',
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

MIN_EA    = 3
MIN_ESA   = 3
MIN_TOTAL = 10

SEASONS = {
    'Verao':     [12, 1, 2],
    'Outono':    [3, 4, 5],
    'Inverno':   [6, 7, 8],
    'Primavera': [9, 10, 11],
}


# ==============================================================================
# HELPER FUNCTIONS  (identical to remote main)
# ==============================================================================

def assign_season(df):
    month_to_season = {}
    for season, months in SEASONS.items():
        for m in months:
            month_to_season[m] = season
    df = df.copy()
    df['month'] = pd.to_datetime(df['date']).dt.month
    df['season'] = df['month'].map(month_to_season)
    return df


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
    return intensities_esa.max(), intensities_ea.min()


def apply_tolerance_levels(intensities_ea, intensities_esa, upper_raw, lower_raw):
    upper_tol = np.percentile(intensities_esa, TOLERANCE_UPPER_PERCENTILE)
    lower_tol = np.percentile(intensities_ea,  TOLERANCE_LOWER_PERCENTILE)
    if upper_tol <= lower_tol:
        upper_tol = upper_raw
        lower_tol = lower_raw
    return upper_tol, lower_tol


def fit_exponential_curve(intensities, api_values, y_true):
    if len(intensities) < 5 or y_true.sum() < 2 or (y_true == 0).sum() < 2:
        return {'a': np.nan, 'b': np.nan, 'c': np.nan,
                'POD': np.nan, 'FAR': np.nan, 'PPV': np.nan, 'score': np.nan}

    i_ea  = intensities[y_true == 1]
    a_min = max(0.1, i_ea.min() * 0.1)
    a_max = i_ea.max() * 3.0
    c_min = 0.0
    c_max = i_ea.mean()

    a_vals = np.linspace(a_min, a_max, GRID_A_SIZE)
    b_vals = np.linspace(B_MIN, B_MAX, GRID_B_SIZE)
    c_vals = np.linspace(c_min, c_max, GRID_C_SIZE)

    best_score  = -np.inf
    best_params = {'a': np.nan, 'b': np.nan, 'c': np.nan}
    best_met    = {'POD': 0, 'FAR': 1, 'PPV': 0}

    i_arr   = intensities.values
    api_arr = api_values.values
    y_arr   = y_true.values

    for a in a_vals:
        for b in b_vals:
            for c in c_vals:
                i_thr  = a * np.exp(b * api_arr) + c
                y_pred = (i_arr >= i_thr).astype(int)

                tp = ((y_arr == 1) & (y_pred == 1)).sum()
                fp = ((y_arr == 0) & (y_pred == 1)).sum()
                fn = ((y_arr == 1) & (y_pred == 0)).sum()
                tn = ((y_arr == 0) & (y_pred == 0)).sum()

                pod   = tp / (tp + fn) if (tp + fn) > 0 else 0.0
                far   = fp / (fp + tn) if (fp + tn) > 0 else 0.0
                ppv   = tp / (tp + fp) if (tp + fp) > 0 else 0.0
                score = pod * ppv * (1 - far)

                if score > best_score:
                    best_score  = score
                    best_params = {'a': a, 'b': b, 'c': c}
                    best_met    = {'POD': pod, 'FAR': far, 'PPV': ppv}

    return {**best_params, **best_met, 'score': best_score}


def evaluate_full_system(events_df, intensity_col, upper_tol, lower_tol,
                         api_col, a, b, c):
    i_arr   = events_df[intensity_col].values
    api_arr = events_df[api_col].values
    y_true  = (events_df['classificacao'] == 'EA').astype(int).values
    y_pred  = np.zeros(len(i_arr), dtype=int)

    above  = i_arr >= upper_tol
    y_pred[above] = 1

    middle = (~above) & (i_arr >= lower_tol)
    if middle.any() and not np.isnan(a):
        i_thr = a * np.exp(b * api_arr[middle]) + c
        y_pred[middle] = (i_arr[middle] >= i_thr).astype(int)

    return compute_metrics(y_true, y_pred)


# ==============================================================================
# CORE FITTING FUNCTION  (seasonal-aware, reads api_{n}d from CSV)
# ==============================================================================

EMPTY_PARAMS = {
    'upper_raw': np.nan, 'lower_raw': np.nan,
    'upper_tol': np.nan, 'lower_tol': np.nan,
    'POD_upper_raw': np.nan, 'FAR_upper_raw': np.nan, 'PPV_upper_raw': np.nan,
    'POD_lower_raw': np.nan, 'FAR_lower_raw': np.nan, 'PPV_lower_raw': np.nan,
    'POD_upper_tol': np.nan, 'FAR_upper_tol': np.nan, 'PPV_upper_tol': np.nan,
    'POD_lower_tol': np.nan, 'FAR_lower_tol': np.nan, 'PPV_lower_tol': np.nan,
    'best_antecedent_days': 0,
    'a': np.nan, 'b': np.nan, 'c': np.nan,
    'POD_api': np.nan, 'FAR_api': np.nan, 'PPV_api': np.nan,
    'n_ea': 0, 'n_esa': 0,
}


def fit_season_timestep(season_events, ts_col, ts_label):
    """Fit thresholds for one sub-bacia × season × time-step.

    Reads api_{n}d columns already present in season_events — identical
    source as the annual analysis on the remote main branch.
    """
    valid = season_events[season_events[ts_col].notna()].copy()

    if len(valid) < MIN_TOTAL:
        return EMPTY_PARAMS.copy(), []

    y_true = (valid['classificacao'] == 'EA').astype(int)
    i_ea   = valid.loc[y_true == 1, ts_col]
    i_esa  = valid.loc[y_true == 0, ts_col]
    n_ea, n_esa = len(i_ea), len(i_esa)

    if n_ea < MIN_EA or n_esa < MIN_ESA:
        return {**EMPTY_PARAMS.copy(), 'n_ea': n_ea, 'n_esa': n_esa}, []

    upper_raw, lower_raw = find_thresholds_raw(i_ea, i_esa)
    upper_tol, lower_tol = apply_tolerance_levels(i_ea, i_esa, upper_raw, lower_raw)

    met_ur = compute_metrics(y_true, (valid[ts_col] >= upper_raw).astype(int))
    met_lr = compute_metrics(y_true, (valid[ts_col] >= lower_raw).astype(int))
    met_ut = compute_metrics(y_true, (valid[ts_col] >= upper_tol).astype(int))
    met_lt = compute_metrics(y_true, (valid[ts_col] >= lower_tol).astype(int))

    best_api_result = None
    best_api_days   = 0
    best_api_score  = -np.inf
    detailed        = []

    middle_mask   = (valid[ts_col] >= lower_tol) & (valid[ts_col] < upper_tol)
    middle_events = valid[middle_mask]

    if len(middle_events) >= MIN_TOTAL:
        for n_days in range(1, MAX_ANTECEDENT_DAYS + 1):
            api_col = f'api_{n_days}d'
            if api_col not in middle_events.columns:
                continue

            ok = middle_events[api_col].notna()
            me = middle_events[ok]
            if len(me) < 5:
                continue

            y_mid = (me['classificacao'] == 'EA').astype(int)
            if y_mid.sum() < 2 or (y_mid == 0).sum() < 2:
                continue

            result = fit_exponential_curve(me[ts_col], me[api_col], y_mid)

            if not np.isnan(result['a']):
                fv   = valid[valid[api_col].notna()]
                fmet = evaluate_full_system(fv, ts_col, upper_tol, lower_tol,
                                            api_col, result['a'], result['b'], result['c'])
                result['full_POD'] = fmet['POD']
                result['full_FAR'] = fmet['FAR']
                result['full_PPV'] = fmet['PPV']
            else:
                result['full_POD'] = result['full_FAR'] = result['full_PPV'] = np.nan

            detailed.append({
                'time_step': ts_label, 'time_step_col': ts_col,
                'antecedent_days': n_days,
                **result
            })

            if result['score'] > best_api_score:
                best_api_score  = result['score']
                best_api_result = result
                best_api_days   = n_days

    if best_api_result is None:
        best_api_result = {'a': np.nan, 'b': np.nan, 'c': np.nan,
                           'full_POD': np.nan, 'full_FAR': np.nan, 'full_PPV': np.nan}

    params = {
        'upper_raw': upper_raw, 'lower_raw': lower_raw,
        'upper_tol': upper_tol, 'lower_tol': lower_tol,
        'POD_upper_raw': met_ur['POD'], 'FAR_upper_raw': met_ur['FAR'], 'PPV_upper_raw': met_ur['PPV'],
        'POD_lower_raw': met_lr['POD'], 'FAR_lower_raw': met_lr['FAR'], 'PPV_lower_raw': met_lr['PPV'],
        'POD_upper_tol': met_ut['POD'], 'FAR_upper_tol': met_ut['FAR'], 'PPV_upper_tol': met_ut['PPV'],
        'POD_lower_tol': met_lt['POD'], 'FAR_lower_tol': met_lt['FAR'], 'PPV_lower_tol': met_lt['PPV'],
        'best_antecedent_days': best_api_days,
        'a': best_api_result['a'],
        'b': best_api_result['b'],
        'c': best_api_result['c'],
        'POD_api': best_api_result.get('full_POD', np.nan),
        'FAR_api': best_api_result.get('full_FAR', np.nan),
        'PPV_api': best_api_result.get('full_PPV', np.nan),
        'n_ea':  n_ea,
        'n_esa': n_esa,
    }

    return params, detailed


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print("=" * 80)
    print("API THRESHOLD FITTING — PER SUB-BACIA, SEASONAL (FIXED K via pre-computed API)")
    print("=" * 80)

    params_path  = f'{OUTPUT_DIR}/api_threshold_parameters_seasonal_fixed_k.csv'
    metrics_path = f'{OUTPUT_DIR}/api_threshold_metrics_seasonal_fixed_k.csv'
    for path in (params_path, metrics_path):
        if pathlib.Path(path).exists():
            raise FileExistsError(
                f"Output file already exists — aborting to avoid overwrite:\n  {path}"
            )

    print(f"\nLoading events: {EVENTS_PATH}")
    events_df = pd.read_csv(EVENTS_PATH)
    events_df = assign_season(events_df)
    print(f"  {len(events_df):,} events  "
          f"(EA={(events_df.classificacao=='EA').sum():,}  "
          f"ESA={(events_df.classificacao=='ESA').sum():,})")
    print("  Season distribution:")
    print(events_df.groupby('season')['classificacao'].value_counts().unstack(fill_value=0).to_string())

    subbacia_ids = sorted(events_df['shi_cd'].unique())
    season_order = ['Verao', 'Outono', 'Inverno', 'Primavera']

    all_results  = []
    detailed_all = []

    for shi_cd in tqdm(subbacia_ids, desc="Sub-bacias"):
        sb_events = events_df[events_df['shi_cd'] == shi_cd]
        shi_nm    = sb_events['shi_nm'].iloc[0] if 'shi_nm' in sb_events.columns else ''

        n_ea  = (sb_events['classificacao'] == 'EA').sum()
        n_esa = (sb_events['classificacao'] == 'ESA').sum()
        print(f"\n{'-'*60}")
        print(f"  {shi_cd} '{shi_nm}'  (EA={n_ea}, ESA={n_esa})")

        for season in season_order:
            seas_events = sb_events[sb_events['season'] == season]
            n_s_ea  = (seas_events['classificacao'] == 'EA').sum()
            n_s_esa = (seas_events['classificacao'] == 'ESA').sum()
            print(f"    [{season}] EA={n_s_ea}  ESA={n_s_esa}")

            for ts_idx, ts_col in enumerate(TIME_STEP_COLS):
                ts_label = TIME_STEP_LABELS[ts_idx]

                params, detailed = fit_season_timestep(seas_events, ts_col, ts_label)

                for d in detailed:
                    d.update({'shi_cd': shi_cd, 'shi_nm': shi_nm, 'season': season})
                detailed_all.extend(detailed)

                all_results.append({
                    'shi_cd': shi_cd, 'shi_nm': shi_nm,
                    'season': season,
                    'time_step': ts_label, 'time_step_col': ts_col,
                    **params,
                })

    print(f"\n{'='*80}")
    print("SAVING RESULTS")
    print(f"{'='*80}")

    params_df = pd.DataFrame(all_results)
    params_df.to_csv(params_path, index=False, float_format='%.6f')
    print(f"  {params_path}  ({len(params_df)} rows)")

    if detailed_all:
        metrics_df = pd.DataFrame(detailed_all)
        metrics_df.to_csv(metrics_path, index=False, float_format='%.6f')
        print(f"  {metrics_path}  ({len(metrics_df)} rows)")

    print(f"\n{'='*80}")
    print("SUMMARY PER SEASON")
    print(f"{'='*80}")

    fitted = params_df[params_df['upper_tol'].notna()]
    print(f"  Total rows  : {len(params_df)}")
    print(f"  Fitted rows : {len(fitted)}")
    print()

    print("  Fitted rows per season:")
    print(fitted.groupby('season').size().reindex(season_order).to_string())
    print()

    print("  Mean POD / FAR / Score (API) by season:")
    api_fitted = fitted[fitted['POD_api'].notna()].copy()
    api_fitted['score_api'] = api_fitted['POD_api'] * api_fitted['PPV_api'] * (1 - api_fitted['FAR_api'])
    summary = (api_fitted.groupby('season')[['POD_api', 'FAR_api', 'score_api']]
               .mean().reindex(season_order).round(3))
    print(summary.to_string())
    print()

    print("  Mean POD / FAR by season (lower_tol — intensity-only baseline):")
    baseline = (fitted.groupby('season')[['POD_lower_tol', 'FAR_lower_tol']]
                .mean().reindex(season_order).round(3))
    print(baseline.to_string())
    print(f"\n{'='*80}\n")


if __name__ == '__main__':
    main()
