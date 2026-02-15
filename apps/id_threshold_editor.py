#!/usr/bin/env python3
"""
Manual I-D Threshold Editor

Streamlit app to manually draw intensity-duration threshold lines per station.
Two control points define the power-law curve I = a * D^(-b) in log-log space.

Run from project root:
    streamlit run apps/id_threshold_editor.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import subprocess
import os

# ---------------------------------------------------------------------------
# Paths (relative to project root)
# ---------------------------------------------------------------------------
ID_ANALYSIS_DIR = 'data/processed/id_analysis'
PONTOS_ID_PATH = f'{ID_ANALYSIS_DIR}/pontos_id_df.csv'
MANUAL_THRESHOLDS_PATH = f'{ID_ANALYSIS_DIR}/manual_thresholds.csv'
METRICS_SCRIPT = 'scripts/processing/compute_threshold_metrics.py'

# ---------------------------------------------------------------------------
# Colors (matching chart_12 style)
# ---------------------------------------------------------------------------
COLOR_ESA = '#4393c3'
COLOR_EA = '#d6604d'
COLOR_THRESHOLD = '#252525'
COLOR_CONTROL = '#f4a261'

# ---------------------------------------------------------------------------
# Data loading (cached)
# ---------------------------------------------------------------------------

@st.cache_data
def load_pontos():
    df = pd.read_csv(PONTOS_ID_PATH)
    return df


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


# ---------------------------------------------------------------------------
# Math helpers
# ---------------------------------------------------------------------------

def points_to_ab(d1, i1, d2, i2):
    """Derive power-law params from two (duration, intensity) control points."""
    if d1 == d2:
        return np.nan, np.nan
    log_d1, log_d2 = np.log(d1), np.log(d2)
    log_i1, log_i2 = np.log(i1), np.log(i2)
    b = -(log_i2 - log_i1) / (log_d2 - log_d1)
    a = i1 * (d1 ** b)
    return a, b


def ab_to_intensity(a, b, d_range):
    """Compute threshold intensities for a range of durations."""
    return a * (d_range ** (-b))


# ---------------------------------------------------------------------------
# Plot builder
# ---------------------------------------------------------------------------

def build_plot(station_data, d1, i1, d2, i2, a, b):
    esa = station_data[station_data['classificacao'] == 'ESA']
    ea = station_data[station_data['classificacao'] == 'EA']

    fig = go.Figure()

    # ESA points
    fig.add_trace(go.Scatter(
        x=esa['duracao_h'], y=esa['intensidade_max_mm_h'],
        mode='markers',
        name='No Flooding (ESA)',
        marker=dict(color=COLOR_ESA, size=6, opacity=0.6),
    ))

    # EA points
    fig.add_trace(go.Scatter(
        x=ea['duracao_h'], y=ea['intensidade_max_mm_h'],
        mode='markers',
        name='With Flooding (EA)',
        marker=dict(color=COLOR_EA, size=10, opacity=0.9,
                    line=dict(color='black', width=0.5)),
    ))

    # Threshold line
    if not (np.isnan(a) or np.isnan(b)):
        d_min = station_data['duracao_h'].min()
        d_max = station_data['duracao_h'].max()
        d_range = np.logspace(np.log10(d_min), np.log10(d_max), 200)
        i_range = ab_to_intensity(a, b, d_range)

        fig.add_trace(go.Scatter(
            x=d_range, y=i_range,
            mode='lines',
            name=f'Threshold: I = {a:.3f} × D^(-{b:.3f})',
            line=dict(color=COLOR_THRESHOLD, width=2.5),
        ))

        # Control points on the line
        fig.add_trace(go.Scatter(
            x=[d1, d2], y=[i1, i2],
            mode='markers',
            name='Control Points',
            marker=dict(color=COLOR_CONTROL, size=14, symbol='diamond',
                        line=dict(color='black', width=1.5)),
        ))

    fig.update_layout(
        xaxis=dict(type='log', title='Duration (h)', showgrid=True, gridcolor='#eee'),
        yaxis=dict(type='log', title='Max Intensity (mm/h)', showgrid=True, gridcolor='#eee'),
        legend=dict(x=0.01, y=0.99, bgcolor='rgba(255,255,255,0.85)',
                    bordercolor='gray', borderwidth=1),
        margin=dict(l=60, r=20, t=40, b=60),
        height=500,
        plot_bgcolor='white',
        paper_bgcolor='white',
    )

    return fig


# ---------------------------------------------------------------------------
# Main app
# ---------------------------------------------------------------------------

def main():
    st.set_page_config(page_title='I-D Threshold Editor', layout='wide')
    st.title('I-D Threshold Editor')

    pontos_df = load_pontos()
    manual_df = load_manual_thresholds()

    station_ids = sorted(pontos_df['id_estacao'].unique())

    # ---- Sidebar ----
    st.sidebar.header('Station')
    station_id = st.sidebar.selectbox('Select station', station_ids)

    station_data = pontos_df[pontos_df['id_estacao'] == station_id].copy()

    d_values = sorted(station_data['duracao_h'].unique())
    i_min = float(station_data['intensidade_max_mm_h'].min())
    i_max = float(station_data['intensidade_max_mm_h'].max())
    d_min = float(min(d_values))
    d_max = float(max(d_values))

    # Load saved threshold for this station if available
    saved = manual_df[manual_df['id_estacao'] == station_id]
    if not saved.empty and not np.isnan(saved.iloc[0]['a']):
        saved_a = float(saved.iloc[0]['a'])
        saved_b = float(saved.iloc[0]['b'])
        # Derive default control point intensities from saved a, b
        default_i1 = float(saved_a * (d_min ** (-saved_b)))
        default_i2 = float(saved_a * (d_max ** (-saved_b)))
        default_i1 = np.clip(default_i1, i_min, i_max)
        default_i2 = np.clip(default_i2, i_min, i_max)
    else:
        i_median = float(station_data['intensidade_max_mm_h'].median())
        default_i1 = i_median
        default_i2 = i_median * 0.5

    st.sidebar.markdown('---')
    st.sidebar.header('Control Point 1')
    st.sidebar.caption(f'Duration fixed at D₁ = {d_min:.2f} h (min)')
    log_i1 = st.sidebar.slider(
        'log(I₁)',
        min_value=float(np.log10(i_min)),
        max_value=float(np.log10(i_max)),
        value=float(np.log10(default_i1)),
        step=0.01,
        key='log_i1',
        format='%.2f',
    )
    i1 = 10 ** log_i1

    st.sidebar.markdown('---')
    st.sidebar.header('Control Point 2')
    st.sidebar.caption(f'Duration fixed at D₂ = {d_max:.2f} h (max)')
    log_i2 = st.sidebar.slider(
        'log(I₂)',
        min_value=float(np.log10(i_min)),
        max_value=float(np.log10(i_max)),
        value=float(np.log10(default_i2)),
        step=0.01,
        key='log_i2',
        format='%.2f',
    )
    i2 = 10 ** log_i2

    # Derive a, b
    a, b = points_to_ab(d_min, i1, d_max, i2)

    # ---- Main area ----
    col1, col2 = st.columns([3, 1])

    with col1:
        fig = build_plot(station_data, d_min, i1, d_max, i2, a, b)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('### Parameters')
        if not np.isnan(a) and not np.isnan(b):
            st.metric('a', f'{a:.4f}')
            st.metric('b', f'{b:.4f}')
            st.latex(r'I = {:.3f} \times D^{{-{:.3f}}}'.format(a, b))
        else:
            st.warning('Cannot compute line (D1 == D2)')

        n_ea = int((station_data['classificacao'] == 'EA').sum())
        n_esa = int((station_data['classificacao'] == 'ESA').sum())
        st.markdown('### Data')
        st.write(f'EA points: **{n_ea}**')
        st.write(f'ESA points: **{n_esa}**')

        # Check if already saved
        already_saved = not saved.empty and not np.isnan(saved.iloc[0]['a'])
        if already_saved:
            st.success('Threshold saved ✓')

        st.markdown('---')
        if st.button('💾 Save Threshold', disabled=np.isnan(a)):
            save_threshold(station_id, a, b)
            st.success(f'Saved: a={a:.4f}, b={b:.4f}')
            st.cache_data.clear()

        st.markdown('---')
        if st.button('⚙️ Compute Metrics & Export'):
            with st.spinner('Running metrics script...'):
                result = subprocess.run(
                    ['python', METRICS_SCRIPT],
                    capture_output=True, text=True, cwd=os.getcwd()
                )
            if result.returncode == 0:
                st.success('threshold_parameters.csv updated!')
            else:
                st.error('Script failed')
            with st.expander('Script output'):
                st.code(result.stdout + result.stderr)


if __name__ == '__main__':
    main()
