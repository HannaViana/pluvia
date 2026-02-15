#!/usr/bin/env python3
"""
Manual I-D Threshold Editor

Streamlit app to manually draw intensity-duration threshold lines per station.
Streamlit sliders control the line position; the chart renders as a static
Plotly HTML embed (fast, no Python figure object overhead).

Run from project root:
    streamlit run apps/id_threshold_editor.py
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import subprocess
import os
import json

# ---------------------------------------------------------------------------
# Paths (relative to project root)
# ---------------------------------------------------------------------------
ID_ANALYSIS_DIR = 'data/processed/id_analysis'
PONTOS_ID_PATH = f'{ID_ANALYSIS_DIR}/pontos_id_df.csv'
MANUAL_THRESHOLDS_PATH = f'{ID_ANALYSIS_DIR}/manual_thresholds.csv'
METRICS_SCRIPT = 'scripts/processing/compute_threshold_metrics.py'

# ---------------------------------------------------------------------------
# Data loading (cached)
# ---------------------------------------------------------------------------

@st.cache_data
def load_pontos():
    return pd.read_csv(PONTOS_ID_PATH)


def load_manual_thresholds():
    if os.path.exists(MANUAL_THRESHOLDS_PATH):
        return pd.read_csv(MANUAL_THRESHOLDS_PATH)
    return pd.DataFrame(columns=['id_estacao', 'a', 'b'])


def save_threshold(station_id, a, b):
    df = load_manual_thresholds()
    mask = df['id_estacao'] == station_id
    if mask.any():
        df.loc[mask, 'a'] = a
        df.loc[mask, 'b'] = b
    else:
        new_row = pd.DataFrame([{'id_estacao': station_id, 'a': a, 'b': b}])
        df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(MANUAL_THRESHOLDS_PATH, index=False, float_format='%.6f')


def points_to_ab(d1, i1, d2, i2):
    if d1 == d2:
        return np.nan, np.nan
    b = -(np.log(i2) - np.log(i1)) / (np.log(d2) - np.log(d1))
    a = i1 * (d1 ** b)
    return a, b


def compute_metrics(station_data, a, b):
    D = station_data['duracao_h'].values
    I = station_data['intensidade_max_mm_h'].values
    y_true = (station_data['classificacao'] == 'EA').astype(int).values
    y_pred = (I >= a * (D ** (-b))).astype(int)

    tp = int(((y_true == 1) & (y_pred == 1)).sum())
    fp = int(((y_true == 0) & (y_pred == 1)).sum())
    fn = int(((y_true == 1) & (y_pred == 0)).sum())
    tn = int(((y_true == 0) & (y_pred == 0)).sum())

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return dict(precision=precision, recall=recall, f1=f1,
                tp=tp, fp=fp, fn=fn, tn=tn)


# ---------------------------------------------------------------------------
# Chart builder (static HTML string — very fast)
# ---------------------------------------------------------------------------

@st.cache_data
def get_station_chart_data(station_id, _pontos_df):
    """Pre-compute and cache the static scatter data for a station."""
    station_data = _pontos_df[_pontos_df['id_estacao'] == station_id]
    esa = station_data[station_data['classificacao'] == 'ESA']
    ea = station_data[station_data['classificacao'] == 'EA']
    return (
        esa['duracao_h'].tolist(), esa['intensidade_max_mm_h'].tolist(),
        ea['duracao_h'].tolist(), ea['intensidade_max_mm_h'].tolist(),
    )


def build_chart_html(esa_d, esa_i, ea_d, ea_i, line_d, line_i,
                     x_min, x_max):
    """Build minimal Plotly HTML with pre-computed data."""
    html = f"""
<!DOCTYPE html>
<html><head>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>* {{ margin:0; padding:0; }} body {{ background:white; }}</style>
</head><body>
<div id="c" style="width:100%;height:500px;"></div>
<script>
Plotly.newPlot('c', [
  {{ x:{json.dumps(esa_d)}, y:{json.dumps(esa_i)}, mode:'markers',
     name:'No Flooding (ESA)',
     marker:{{ color:'#4393c3', size:5, opacity:0.5 }} }},
  {{ x:{json.dumps(ea_d)}, y:{json.dumps(ea_i)}, mode:'markers',
     name:'With Flooding (EA)',
     marker:{{ color:'#d6604d', size:8, opacity:0.9,
              line:{{ color:'black', width:0.5 }} }} }},
  {{ x:{json.dumps(line_d)}, y:{json.dumps(line_i)}, mode:'lines',
     name:'Threshold',
     line:{{ color:'#252525', width:2, dash:'dash' }} }}
], {{
  xaxis:{{ type:'log', title:'Duration (h)',
           range:[{np.log10(x_min)},{np.log10(x_max)}],
           showgrid:true, gridcolor:'#e8e8e8' }},
  yaxis:{{ type:'log', title:'Max Intensity (mm/h)',
           showgrid:true, gridcolor:'#e8e8e8' }},
  legend:{{ x:0.01, y:0.99, bgcolor:'rgba(255,255,255,0.85)',
            bordercolor:'gray', borderwidth:1 }},
  margin:{{ l:65, r:20, t:20, b:55 }},
  plot_bgcolor:'white', paper_bgcolor:'white', hovermode:'closest'
}}, {{ responsive:true }});
</script></body></html>
"""
    return html


# ---------------------------------------------------------------------------
# Main app
# ---------------------------------------------------------------------------

def main():
    st.set_page_config(page_title='I-D Threshold Editor', layout='wide')
    st.title('I-D Threshold Editor')

    pontos_df = load_pontos()
    manual_df = load_manual_thresholds()
    station_ids = sorted(pontos_df['id_estacao'].unique())

    # ---- Sidebar: Station ----
    st.sidebar.header('Station')
    station_id = st.sidebar.selectbox('Select station', station_ids)

    station_data = pontos_df[pontos_df['id_estacao'] == station_id]
    d_values = sorted(station_data['duracao_h'].unique())
    i_min = float(station_data['intensidade_max_mm_h'].min())
    i_max = float(station_data['intensidade_max_mm_h'].max())
    d_min = float(min(d_values))
    d_max = float(max(d_values))

    log_i_min = float(np.log10(i_min))
    log_i_max = float(np.log10(i_max))

    # Load saved threshold
    saved = manual_df[manual_df['id_estacao'] == station_id]
    has_saved = not saved.empty and not np.isnan(saved.iloc[0]['a'])

    if has_saved:
        saved_a = float(saved.iloc[0]['a'])
        saved_b = float(saved.iloc[0]['b'])
        def_i1 = float(np.clip(saved_a * (d_min ** (-saved_b)), i_min, i_max))
        def_i2 = float(np.clip(saved_a * (d_max ** (-saved_b)), i_min, i_max))
        def_log_i1 = float(np.log10(def_i1))
        def_log_i2 = float(np.log10(def_i2))
        st.sidebar.info(f'Saved: a={saved_a:.4f}, b={saved_b:.4f}')
    else:
        i_median = float(station_data['intensidade_max_mm_h'].median())
        def_log_i1 = float(np.log10(i_median))
        def_log_i2 = float(np.log10(max(i_median * 0.5, i_min)))

    # ---- Sidebar: Sliders ----
    st.sidebar.markdown('---')
    st.sidebar.header('Threshold Line')

    log_i1 = st.sidebar.slider(
        f'Intensity at D={d_min:.2f}h (log₁₀)',
        min_value=log_i_min, max_value=log_i_max,
        value=def_log_i1, step=0.005, format='%.3f',
    )
    st.sidebar.caption(f'I₁ = {10**log_i1:.2f} mm/h')

    log_i2 = st.sidebar.slider(
        f'Intensity at D={d_max:.2f}h (log₁₀)',
        min_value=log_i_min, max_value=log_i_max,
        value=def_log_i2, step=0.005, format='%.3f',
    )
    st.sidebar.caption(f'I₂ = {10**log_i2:.2f} mm/h')

    i1 = 10 ** log_i1
    i2 = 10 ** log_i2
    a, b = points_to_ab(d_min, i1, d_max, i2)

    # ---- Chart ----
    esa_d, esa_i, ea_d, ea_i = get_station_chart_data(station_id, pontos_df)

    x_pad = 0.15
    x_min = 10 ** (np.log10(d_min) - x_pad)
    x_max = 10 ** (np.log10(d_max) + x_pad)

    line_d = np.logspace(np.log10(x_min), np.log10(x_max), 150).tolist()
    line_i = [a * (d ** (-b)) for d in line_d] if not np.isnan(a) else [0] * 150

    html = build_chart_html(esa_d, esa_i, ea_d, ea_i, line_d, line_i,
                            x_min, x_max)
    components.html(html, height=520, scrolling=False)

    # ---- Metrics ----
    if not np.isnan(a):
        m = compute_metrics(station_data, a, b)
        cols = st.columns(7)
        for col, (label, val) in zip(cols, [
            ('Recall', f'{m["recall"]:.2f}'),
            ('Precision', f'{m["precision"]:.2f}'),
            ('F1', f'{m["f1"]:.2f}'),
            ('TP', m['tp']), ('FP', m['fp']),
            ('FN', m['fn']), ('TN', m['tn']),
        ]):
            col.metric(label, val)

        st.markdown(f'**I = {a:.3f} × D⁻{b:.3f}** &emsp; a={a:.6f} &emsp; b={b:.6f}')

    # ---- Sidebar: Save ----
    st.sidebar.markdown('---')
    if st.sidebar.button('Save Threshold', disabled=np.isnan(a)):
        save_threshold(station_id, a, b)
        st.sidebar.success(f'Saved: a={a:.4f}, b={b:.4f}')
        st.rerun()

    # ---- Sidebar: Export ----
    st.sidebar.markdown('---')
    if st.sidebar.button('Compute Metrics & Export'):
        with st.spinner('Running metrics script...'):
            result = subprocess.run(
                ['python', METRICS_SCRIPT],
                capture_output=True, text=True, cwd=os.getcwd()
            )
        if result.returncode == 0:
            st.sidebar.success('threshold_parameters.csv updated!')
        else:
            st.sidebar.error('Script failed')
        with st.sidebar.expander('Script output'):
            st.code(result.stdout + result.stderr)


if __name__ == '__main__':
    main()
