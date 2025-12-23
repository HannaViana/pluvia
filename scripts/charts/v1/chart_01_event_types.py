"""
Chart 1: Event Type Distribution
Replaces pie chart with bar chart for better categorical comparison
Includes sample sizes and percentage labels
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

# Add parent directory to path for config import
sys.path.insert(0, os.path.dirname(__file__))
from config import (setup_plot_style, COLORS, FONT_SIZES, FIGURE_SIZES,
                    DATA_PATHS, OUTPUT_DIR, FLOOD_TYPES, EVENT_TYPE_MAPPING,
                    GENERIC_TYPE_MAPPING, STUDY_PERIOD, STUDY_LOCATION, add_sample_size_annotation)

def load_and_prepare_data():
    """Load and preprocess flood event data"""
    # Load data
    ocorrencias = pd.read_csv(DATA_PATHS['ocorrencias'])
    pops = pd.read_csv(DATA_PATHS['pops'], index_col=0)
    
    # Preprocessing
    ocorrencias['data_inicio'] = pd.to_datetime(ocorrencias['data_inicio'])
    ocorrencias['data_fim'] = pd.to_datetime(ocorrencias['data_fim'])
    ocorrencias['tipo'] = ocorrencias['id_pop'].map(pops.set_index('id')['titulo'])
    
    # Filter flood events
    ocorrencias = ocorrencias[ocorrencias['tipo'].isin(FLOOD_TYPES)]
    
    # Consolidate event types
    ocorrencias['tipo'] = ocorrencias['tipo'].replace(EVENT_TYPE_MAPPING)
    
    # Apply generic category mapping
    ocorrencias['tipo'] = ocorrencias['tipo'].replace(GENERIC_TYPE_MAPPING)
    
    return ocorrencias

def create_event_type_chart(ocorrencias):
    """Create bar chart of event type distribution"""
    setup_plot_style()
    
    # Define order for flood types
    flood_type_order = ['Flood Type I', 'Flood Type II', 'Flood Type III']
    
    # Calculate event type counts and sort by predefined order
    event_counts = ocorrencias['tipo'].value_counts()
    # Reindex to ensure correct order, only including types that exist
    event_counts = event_counts.reindex([t for t in flood_type_order if t in event_counts.index])
    total_events = len(ocorrencias)
    percentages = (event_counts / total_events * 100)
    
    # Create figure
    fig, ax = plt.subplots(figsize=FIGURE_SIZES['single'])
    
    # Create horizontal bar chart
    bars = ax.barh(range(len(event_counts)), event_counts.values, 
                   color=COLORS['categorical'][:len(event_counts)],
                   edgecolor='black', linewidth=0.5)
    
    # Add value labels with percentages
    for i, (count, pct) in enumerate(zip(event_counts.values, percentages.values)):
        ax.text(count + total_events * 0.01, i,
                f'{count:,} ({pct:.1f}%)',
                va='center', fontsize=FONT_SIZES['annotation'])
    
    # Extend x-axis to accommodate text labels
    max_count = event_counts.values.max()
    ax.set_xlim(0, max_count * 1.21)  # Add 15% padding for text labels
    
    # Styling
    ax.set_yticks(range(len(event_counts)))
    ax.set_yticklabels(event_counts.index, fontsize=FONT_SIZES['tick_label'])
    ax.set_xlabel('Number of Events', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax.set_title(f'Distribution of Urban Flood Event Types\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'], fontweight='bold', pad=15)
    
    # Add grid for easier reading
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)
    
    # Add sample size annotation
    add_sample_size_annotation(ax, total_events)
    
    # Adjust layout
    plt.tight_layout()
    
    return fig

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias = load_and_prepare_data()
    
    print(f"Total flood events: {len(ocorrencias)}")
    print("\nEvent type distribution:")
    print(ocorrencias['tipo'].value_counts())
    
    print("\nCreating chart...")
    fig = create_event_type_chart(ocorrencias)
    
    # Save
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = f'{OUTPUT_DIR}/chart_01_event_types.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Chart saved to {output_path}")
    plt.close()

if __name__ == '__main__':
    main()
