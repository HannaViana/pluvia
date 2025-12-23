"""
Chart 8: Event Duration Categories
Simple bar chart showing distribution of events by duration categories
More granular categorization between 1-6 hours
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from config import (setup_plot_style, COLORS, FONT_SIZES, FIGURE_SIZES,
                    DATA_PATHS, OUTPUT_DIR, FLOOD_TYPES, EVENT_TYPE_MAPPING,
                    GENERIC_TYPE_MAPPING, STUDY_PERIOD, STUDY_LOCATION, add_sample_size_annotation)

def load_and_prepare_data():
    """Load and preprocess flood event data with duration calculation"""
    ocorrencias = pd.read_csv(DATA_PATHS['ocorrencias'])
    pops = pd.read_csv(DATA_PATHS['pops'], index_col=0)
    
    ocorrencias['data_inicio'] = pd.to_datetime(ocorrencias['data_inicio'])
    ocorrencias['data_fim'] = pd.to_datetime(ocorrencias['data_fim'])
    ocorrencias['tipo'] = ocorrencias['id_pop'].map(pops.set_index('id')['titulo'])
    
    ocorrencias = ocorrencias[ocorrencias['tipo'].isin(FLOOD_TYPES)]
    ocorrencias['tipo'] = ocorrencias['tipo'].replace(EVENT_TYPE_MAPPING)
    ocorrencias['tipo'] = ocorrencias['tipo'].replace(GENERIC_TYPE_MAPPING)
    
    # Calculate duration in hours
    ocorrencias['duration_hours'] = (ocorrencias['data_fim'] - ocorrencias['data_inicio']).dt.total_seconds() / 3600
    
    # Filter out invalid durations
    ocorrencias = ocorrencias[
        (ocorrencias['duration_hours'] >= 0) & 
        (ocorrencias['duration_hours'] <= 72)
    ].copy()
    
    return ocorrencias

def categorize_duration(duration):
    """Categorize event duration into granular categories"""
    if duration < 1:
        return '< 1h'
    elif duration < 2:
        return '1-2h'
    elif duration < 3:
        return '2-3h'
    elif duration < 4:
        return '3-4h'
    elif duration < 5:
        return '4-5h'
    elif duration < 6:
        return '5-6h'
    elif duration < 12:
        return '6-12h'
    elif duration < 24:
        return '12-24h'
    else:
        return '> 24h'

def create_duration_categories_chart(ocorrencias):
    """Create bar chart of event duration categories"""
    setup_plot_style()
    
    # Apply categorization
    ocorrencias['duration_category'] = ocorrencias['duration_hours'].apply(categorize_duration)
    
    # Define category order
    category_order = ['< 1h', '1-2h', '2-3h', '3-4h', '4-5h', '5-6h', 
                     '6-12h', '12-24h', '> 24h']
    
    # Count events per category
    category_counts = ocorrencias['duration_category'].value_counts()
    category_counts = category_counts.reindex(category_order, fill_value=0)
    
    total_events = len(ocorrencias)
    percentages = (category_counts / total_events * 100)
    
    # Create figure
    fig, ax = plt.subplots(figsize=FIGURE_SIZES['single'])
    
    # Create bar chart with gradient colors
    colors = plt.cm.YlOrRd(np.linspace(0.3, 0.9, len(category_order)))
    bars = ax.bar(range(len(category_counts)), category_counts.values,
                  color=colors, edgecolor='black', linewidth=0.5)
    
    # Add value labels with counts and percentages
    for i, (count, pct) in enumerate(zip(category_counts.values, percentages.values)):
        ax.text(i, count + total_events * 0.01,
                f'{count:,}\n({pct:.1f}%)',
                ha='center', va='bottom', fontsize=FONT_SIZES['annotation'])
    
    # Styling
    ax.set_xticks(range(len(category_counts)))
    ax.set_xticklabels(category_counts.index, fontsize=FONT_SIZES['tick_label'], rotation=45, ha='right')
    ax.set_xlabel('Duration Category', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax.set_ylabel('Number of Events', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax.set_title(f'Distribution of Urban Flood Events by Duration Category\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'], fontweight='bold', pad=15)
    
    # Add grid for easier reading
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)
    
    # Extend y-axis to accommodate text labels
    max_count = category_counts.values.max()
    ax.set_ylim(0, max_count * 1.15)
    
    # Add sample size annotation
    add_sample_size_annotation(ax, total_events)
    
    # Add statistics box
    median_duration = ocorrencias['duration_hours'].median()
    mean_duration = ocorrencias['duration_hours'].mean()
    stats_text = f'Median: {median_duration:.2f}h\nMean: {mean_duration:.2f}h'
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
            fontsize=FONT_SIZES['annotation'], verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray'))
    
    # Adjust layout
    plt.tight_layout()
    
    return fig, category_counts, percentages

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias = load_and_prepare_data()
    
    print(f"Total flood events: {len(ocorrencias)}")
    
    print("\nCreating duration categories chart...")
    fig, category_counts, percentages = create_duration_categories_chart(ocorrencias)
    
    print("\nDuration category distribution:")
    for category, count, pct in zip(category_counts.index, category_counts.values, percentages.values):
        print(f"  {category:>8}: {count:>5,} events ({pct:>5.1f}%)")
    
    # Save
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = f'{OUTPUT_DIR}/chart_08_duration_categories.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nChart saved to {output_path}")
    plt.close()

if __name__ == '__main__':
    main()
