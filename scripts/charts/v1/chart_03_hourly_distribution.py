"""
Chart 3: Hourly Distribution of Flood Events
Includes statistical annotations and potential reporting bias discussion
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from config import (setup_plot_style, COLORS, FONT_SIZES, FIGURE_SIZES,
                    DATA_PATHS, OUTPUT_DIR, FLOOD_TYPES, EVENT_TYPE_MAPPING,
                    STUDY_PERIOD, STUDY_LOCATION, add_sample_size_annotation, ALPHA)

def load_and_prepare_data():
    """Load and preprocess flood event data"""
    ocorrencias = pd.read_csv(DATA_PATHS['ocorrencias'])
    pops = pd.read_csv(DATA_PATHS['pops'], index_col=0)
    
    ocorrencias['data_inicio'] = pd.to_datetime(ocorrencias['data_inicio'])
    ocorrencias['data_fim'] = pd.to_datetime(ocorrencias['data_fim'])
    ocorrencias['tipo'] = ocorrencias['id_pop'].map(pops.set_index('id')['titulo'])
    
    ocorrencias = ocorrencias[ocorrencias['tipo'].isin(FLOOD_TYPES)]
    ocorrencias['tipo'] = ocorrencias['tipo'].replace(EVENT_TYPE_MAPPING)
    
    return ocorrencias

def calculate_hourly_stats(ocorrencias):
    """Calculate hourly statistics with significance testing"""
    ocorrencias['hour'] = ocorrencias['data_inicio'].dt.hour
    hourly_counts = ocorrencias['hour'].value_counts().sort_index()
    
    # Ensure all hours are represented
    all_hours = pd.Series(0, index=range(24))
    hourly_counts = hourly_counts.add(all_hours, fill_value=0).astype(int)
    
    # Chi-square test for uniform distribution
    expected = len(ocorrencias) / 24
    chi2, p_value = stats.chisquare(hourly_counts.values, f_exp=[expected] * 24)
    
    # Identify peak hours (>1 std above mean)
    mean_count = hourly_counts.mean()
    std_count = hourly_counts.std()
    threshold = mean_count + std_count
    peak_hours = hourly_counts[hourly_counts > threshold].index.tolist()
    
    return hourly_counts, chi2, p_value, peak_hours, mean_count, std_count

def create_hourly_distribution_chart(ocorrencias):
    """Create hourly distribution chart with statistical annotations"""
    setup_plot_style()
    
    hourly_counts, chi2, p_value, peak_hours, mean_count, std_count = calculate_hourly_stats(ocorrencias)
    
    fig, ax = plt.subplots(figsize=FIGURE_SIZES['wide'])
    
    # Create bar chart with peak hours highlighted
    colors = [COLORS['secondary'] if h in peak_hours else COLORS['primary'] for h in range(24)]
    bars = ax.bar(range(24), hourly_counts.values, color=colors, edgecolor='black', linewidth=0.5)
    
    # Add mean line
    ax.axhline(mean_count, color='gray', linestyle='--', linewidth=1.5, label=f'Mean: {mean_count:.1f}', alpha=0.7)
    
    # Add threshold line (mean + 1 std)
    threshold = mean_count + std_count
    ax.axhline(threshold, color='red', linestyle=':', linewidth=1.5, 
              label=f'Mean + 1σ: {threshold:.1f}', alpha=0.7)
    
    # Styling
    ax.set_xlabel('Hour of Day', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax.set_ylabel('Number of Events', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax.set_title(f'Hourly Distribution of Urban Flood Events\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'], fontweight='bold', pad=15)
    ax.set_xticks(range(24))
    ax.set_xticklabels([f'{h:02d}:00' for h in range(24)], rotation=45, ha='right')
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)
    ax.legend(loc='upper left', fontsize=FONT_SIZES['legend'])
    
    # Add chi-square test result
    sig_text = f'χ² = {chi2:.2f}, p < 0.001' if p_value < 0.001 else f'χ² = {chi2:.2f}, p = {p_value:.4f}'
    if p_value < ALPHA:
        sig_text += ' *'
    ax.text(0.98, 0.85, sig_text, transform=ax.transAxes, fontsize=FONT_SIZES['annotation'],
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray'))
    
    # Add peak hours annotation
    peak_text = f'Peak hours: {", ".join([f"{h:02d}:00" for h in peak_hours])}'
    ax.text(0.98, 0.75, peak_text, transform=ax.transAxes, fontsize=FONT_SIZES['annotation'],
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, edgecolor='gray'))
    
    add_sample_size_annotation(ax, len(ocorrencias), y=0.98)
    
    plt.tight_layout()
    return fig, hourly_counts, chi2, p_value, peak_hours

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias = load_and_prepare_data()
    print(f"Total flood events: {len(ocorrencias)}")
    
    print("\nCreating hourly distribution chart...")
    fig, hourly_counts, chi2, p_value, peak_hours = create_hourly_distribution_chart(ocorrencias)
    
    print("\nHourly distribution:")
    print(hourly_counts)
    print(f"\nChi-square test: χ² = {chi2:.2f}, p = {p_value:.6f}")
    print(f"Peak hours (>1 std above mean): {peak_hours}")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = f'{OUTPUT_DIR}/chart_03_hourly_distribution.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nChart saved to {output_path}")
    plt.close()

if __name__ == '__main__':
    main()
