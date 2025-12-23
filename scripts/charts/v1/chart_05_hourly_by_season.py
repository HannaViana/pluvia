"""
Chart 5: Hourly Distribution by Season
Four-panel figure showing hourly patterns for each season
Reveals seasonal variations in flood timing
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
                    GENERIC_TYPE_MAPPING, STUDY_PERIOD, STUDY_LOCATION, add_sample_size_annotation,
                    add_subfigure_label, ALPHA)

def load_and_prepare_data():
    """Load and preprocess flood event data"""
    ocorrencias = pd.read_csv(DATA_PATHS['ocorrencias'])
    pops = pd.read_csv(DATA_PATHS['pops'], index_col=0)
    
    ocorrencias['data_inicio'] = pd.to_datetime(ocorrencias['data_inicio'])
    ocorrencias['data_fim'] = pd.to_datetime(ocorrencias['data_fim'])
    ocorrencias['tipo'] = ocorrencias['id_pop'].map(pops.set_index('id')['titulo'])
    
    ocorrencias = ocorrencias[ocorrencias['tipo'].isin(FLOOD_TYPES)]
    ocorrencias['tipo'] = ocorrencias['tipo'].replace(EVENT_TYPE_MAPPING)
    ocorrencias['tipo'] = ocorrencias['tipo'].replace(GENERIC_TYPE_MAPPING)
    
    return ocorrencias

def get_season(date):
    """Assign season based on month (Southern Hemisphere)"""
    month = date.month
    if month in [12, 1, 2]:
        return 'Summer'
    elif month in [3, 4, 5]:
        return 'Autumn'
    elif month in [6, 7, 8]:
        return 'Winter'
    else:
        return 'Spring'

def calculate_hourly_stats_by_season(ocorrencias):
    """Calculate hourly statistics for each season"""
    ocorrencias['hour'] = ocorrencias['data_inicio'].dt.hour
    ocorrencias['season'] = ocorrencias['data_inicio'].apply(get_season)
    
    season_stats = {}
    season_order = ['Summer', 'Autumn', 'Winter', 'Spring']
    
    for season in season_order:
        season_data = ocorrencias[ocorrencias['season'] == season]
        hourly_counts = season_data['hour'].value_counts().sort_index()
        
        # Ensure all hours are represented
        all_hours = pd.Series(0, index=range(24))
        hourly_counts = hourly_counts.add(all_hours, fill_value=0).astype(int)
        
        # Chi-square test for uniform distribution
        expected = len(season_data) / 24
        chi2, p_value = stats.chisquare(hourly_counts.values, f_exp=[expected] * 24)
        
        # Identify peak hours (>1 std above mean)
        mean_count = hourly_counts.mean()
        std_count = hourly_counts.std()
        threshold = mean_count + std_count
        peak_hours = hourly_counts[hourly_counts > threshold].index.tolist()
        
        season_stats[season] = {
            'hourly_counts': hourly_counts,
            'chi2': chi2,
            'p_value': p_value,
            'peak_hours': peak_hours,
            'mean': mean_count,
            'std': std_count,
            'n_events': len(season_data)
        }
    
    return season_stats

def create_hourly_by_season_chart(ocorrencias):
    """Create 2x2 grid of hourly distributions by season"""
    setup_plot_style()
    
    season_stats = calculate_hourly_stats_by_season(ocorrencias)
    season_order = ['Summer', 'Autumn', 'Winter', 'Spring']
    
    # Create 2x2 subplot grid
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'Hourly Distribution of Urban Flood Events by Season\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'] + 2, fontweight='bold', y=0.995)
    
    # Flatten axes for easier iteration
    axes_flat = axes.flatten()
    
    # Subplot labels
    subplot_labels = ['(a)', '(b)', '(c)', '(d)']
    
    for idx, season in enumerate(season_order):
        ax = axes_flat[idx]
        stats_dict = season_stats[season]
        hourly_counts = stats_dict['hourly_counts']
        peak_hours = stats_dict['peak_hours']
        mean_count = stats_dict['mean']
        std_count = stats_dict['std']
        chi2 = stats_dict['chi2']
        p_value = stats_dict['p_value']
        n_events = stats_dict['n_events']
        
        # Create bar chart with peak hours highlighted
        colors = [COLORS['secondary'] if h in peak_hours else COLORS['seasons'][season] 
                 for h in range(24)]
        bars = ax.bar(range(24), hourly_counts.values, color=colors, 
                     edgecolor='black', linewidth=0.5, alpha=0.8)
        
        # Add mean line
        ax.axhline(mean_count, color='gray', linestyle='--', linewidth=1.5, 
                  label=f'Mean: {mean_count:.1f}', alpha=0.7)
        
        # Add threshold line (mean + 1 std)
        threshold = mean_count + std_count
        ax.axhline(threshold, color='red', linestyle=':', linewidth=1.5, 
                  label=f'Mean + 1σ: {threshold:.1f}', alpha=0.7)
        
        # Styling
        ax.set_xlabel('Hour of Day', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
        ax.set_ylabel('Number of Events', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
        ax.set_title(f'{season} (N = {n_events:,})', 
                    fontsize=FONT_SIZES['subtitle'], fontweight='bold', pad=10)
        ax.set_xticks([0, 6, 12, 18, 23])
        ax.set_xticklabels(['00:00', '06:00', '12:00', '18:00', '23:00'])
        ax.grid(axis='y', linestyle='--', alpha=0.3)
        ax.set_axisbelow(True)
        ax.legend(loc='upper left', fontsize=FONT_SIZES['annotation'])
        
        # Add peak hours annotation if any
        if peak_hours:
            peak_text = f'Peak: {", ".join([f"{h:02d}h" for h in peak_hours[:3]])}'
            if len(peak_hours) > 3:
                peak_text += '...'
            ax.text(0.02, 0.98, peak_text, transform=ax.transAxes, 
                   fontsize=FONT_SIZES['annotation'],
                   verticalalignment='top', horizontalalignment='left',
                   bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, edgecolor='gray'))
        
        # Add subfigure label
        add_subfigure_label(ax, subplot_labels[idx], x=-0.12, y=1.08)
    
    plt.tight_layout(rect=[0, 0, 1, 0.99])
    
    return fig, season_stats

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias = load_and_prepare_data()
    print(f"Total flood events: {len(ocorrencias)}")
    
    print("\nCreating hourly distribution by season chart...")
    fig, season_stats = create_hourly_by_season_chart(ocorrencias)
    
    print("\nSeasonal hourly statistics:")
    print("="*70)
    for season, stats in season_stats.items():
        print(f"\n{season}:")
        print(f"  Events: {stats['n_events']:,}")
        print(f"  Mean hourly count: {stats['mean']:.2f}")
        print(f"  Std dev: {stats['std']:.2f}")
        print(f"  Chi-square: χ² = {stats['chi2']:.2f}, p = {stats['p_value']:.6f}")
        print(f"  Peak hours: {stats['peak_hours']}")
        print(f"  Top 3 hours: {stats['hourly_counts'].nlargest(3).to_dict()}")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = f'{OUTPUT_DIR}/chart_05_hourly_by_season.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nChart saved to {output_path}")
    plt.close()

if __name__ == '__main__':
    main()
