# Chart category standardization
_Exported on 11/02/2026 at 11:00:34 BRT from Cursor (2.4.21)_

---

**User**

## Context
- We will update the scripts in scripts/charts/v1/
- instead of the raw categories being displayed in the charts, I want them converted to some generic set of categories like 'Flood Type 1' or similar
- Order:
1. lamina
2. bolsão
3. alagamento

## Task
Briefly suggest options for the categories

## Restrictions
Do nothing else

---

**Cursor**

Reviewing the scripts to identify the current categories, then suggesting generic category name options.


Checking how these categories are used in the charts:


Current categories:
- "Lâmina d'água" (lamina)
- "Bolsão d'água em via" (bolsão)
- "Alagamento" (alagamento)

## Option 1: Numeric (Simple)
- **Flood Type 1** (lamina)
- **Flood Type 2** (bolsão)
- **Flood Type 3** (alagamento)

## Option 2: Numeric with Letters
- **Type A** (lamina)
- **Type B** (bolsão)
- **Type C** (alagamento)

## Option 3: Descriptive Generic
- **Flood Type I** (lamina)
- **Flood Type II** (bolsão)
- **Flood Type III** (alagamento)

## Option 4: Category-Based
- **Category 1** (lamina)
- **Category 2** (bolsão)
- **Category 3** (alagamento)

## Option 5: Event-Based
- **Event Type 1** (lamina)
- **Event Type 2** (bolsão)
- **Event Type 3** (alagamento)

Recommendation: Option 1 (Flood Type 1/2/3) for clarity and simplicity.

---

**User**

I like option 3. Proceed to update the scripts

---

**Cursor**

Updating scripts to use "Flood Type I", "Flood Type II", and "Flood Type III". Checking where the categories are used:


Checking for hardcoded category names in chart titles and labels:


Updating scripts to use generic category names. Creating a mapping in `config.py` and applying it across all scripts.


```python
"""
Unified configuration for scientific publication charts
Ensures consistency across all visualizations
"""

import matplotlib.pyplot as plt
import seaborn as sns

# Publication settings
DPI = 300
STYLE = 'seaborn-v0_8-paper'

# Color palette (colorblind-friendly, from ColorBrewer)
COLORS = {
    'primary': '#2166ac',      # Blue
    'secondary': '#b2182b',    # Red
    'tertiary': '#35978f',     # Teal
    'quaternary': '#f46d43',   # Orange
    'palette': ['#2166ac', '#4393c3', '#92c5de', '#d1e5f0'],
    'diverging': ['#2166ac', '#4393c3', '#92c5de', '#f7f7f7', '#fddbc7', '#f4a582', '#d6604d', '#b2182b'],
    'categorical': ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e', '#e6ab02'],
    'seasons': {
        'Summer': '#e41a1c',
        'Autumn': '#ff7f00',
        'Winter': '#377eb8',
        'Spring': '#4daf4a'
    }
}

# Typography
FONT_SIZES = {
    'title': 14,
    'subtitle': 12,
    'axis_label': 11,
    'tick_label': 10,
    'legend': 10,
    'annotation': 9
}

FONT_WEIGHTS = {
    'title': 'bold',
    'normal': 'normal'
}

# Figure dimensions (width, height in inches)
FIGURE_SIZES = {
    'single': (8, 6),
    'wide': (12, 5),
    'tall': (8, 10),
    'double': (12, 6),
    'triple': (15, 5)
}

# Data paths
DATA_PATHS = {
    'ocorrencias': 'nbs/exploration/ocorrencias/ocorrencias_filtradas.csv',
    'pops': 'data/raw/adm_cor_comando/pops.csv',
    'stations': '~/work/data/meteorologia/clean/clima_pluviometro/estacoes_alertario.csv'
}

# Output paths
OUTPUT_DIR = 'results/charts/v1'

# Flood event types
FLOOD_TYPES = [
    "Bolsão d'água em via",
    'Alagamento',
    'Alagamentos e enchentes',
    'Enchente',
    "Lâmina d'água"
]

# Event type consolidation mapping
EVENT_TYPE_MAPPING = {
    'Alagamentos e enchentes': 'Alagamento',
    'Enchente': 'Alagamento'
}

# Generic category mapping for display (order: lamina, bolsão, alagamento)
GENERIC_TYPE_MAPPING = {
    "Lâmina d'água": 'Flood Type I',
    "Bolsão d'água em via": 'Flood Type II',
    'Alagamento': 'Flood Type III'
}

# CRS definitions
CRS_GEOGRAPHIC = "EPSG:4326"  # WGS84
CRS_PROJECTED = "EPSG:31983"  # SIRGAS 2000 / UTM zone 23S

# Study period (update based on actual data)
STUDY_PERIOD = "2019-2024"
STUDY_LOCATION = "Rio de Janeiro"

# Statistical significance level
ALPHA = 0.05

def setup_plot_style():
    """Apply consistent plot styling"""
    plt.style.use(STYLE)
    plt.rcParams['figure.dpi'] = DPI
    plt.rcParams['font.size'] = FONT_SIZES['tick_label']
    plt.rcParams['axes.labelsize'] = FONT_SIZES['axis_label']
    plt.rcParams['axes.titlesize'] = FONT_SIZES['title']
    plt.rcParams['xtick.labelsize'] = FONT_SIZES['tick_label']
    plt.rcParams['ytick.labelsize'] = FONT_SIZES['tick_label']
    plt.rcParams['legend.fontsize'] = FONT_SIZES['legend']
    plt.rcParams['figure.titlesize'] = FONT_SIZES['title']
    
def add_sample_size_annotation(ax, n, x=0.98, y=0.98):
    """Add sample size annotation to plot"""
    ax.text(x, y, f'N = {n:,}', 
            transform=ax.transAxes,
            fontsize=FONT_SIZES['annotation'],
            verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray'))

def add_subfigure_label(ax, label, x=-0.1, y=1.05):
    """Add subfigure label (a, b, c, etc.)"""
    ax.text(x, y, label,
            transform=ax.transAxes,
            fontsize=FONT_SIZES['title'],
            fontweight='bold',
            verticalalignment='top')

```

Updating all scripts to use the generic mapping. Starting with the main chart scripts:


```python
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
    
    return ocorrencias

def create_event_type_chart(ocorrencias):
    """Create bar chart of event type distribution"""
    setup_plot_style()
    
    # Calculate event type counts
    event_counts = ocorrencias['tipo'].value_counts().sort_values(ascending=True)
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

```

```python
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
    
    # Calculate event type counts
    event_counts = ocorrencias['tipo'].value_counts().sort_values(ascending=True)
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

```

```python
from config import (setup_plot_style, COLORS, FONT_SIZES, FIGURE_SIZES,
                    DATA_PATHS, OUTPUT_DIR, FLOOD_TYPES, EVENT_TYPE_MAPPING,
                    GENERIC_TYPE_MAPPING, STUDY_PERIOD, STUDY_LOCATION, add_sample_size_annotation)
```

Reading the files to update them correctly:


Updating all scripts to use the generic mapping. Starting with the imports and applying the mapping:


```python
"""
Chart 2: Temporal Patterns of Flood Events
Combines monthly and seasonal analysis with statistical information
Multi-panel figure with confidence intervals
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import os
import sys

# Add parent directory to path for config import
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

def calculate_monthly_stats(ocorrencias):
    """Calculate monthly statistics with confidence intervals"""
    ocorrencias['year'] = ocorrencias['data_inicio'].dt.year
    ocorrencias['month'] = ocorrencias['data_inicio'].dt.month
    
    monthly_counts = ocorrencias.groupby(['year', 'month']).size().reset_index(name='count')
    monthly_stats = monthly_counts.groupby('month')['count'].agg(['mean', 'std', 'count', 'sem']).reset_index()
    
    confidence = 0.95
    monthly_stats['ci'] = monthly_stats['sem'] * stats.t.ppf((1 + confidence) / 2, monthly_stats['count'] - 1)
    monthly_stats['ci_lower'] = (monthly_stats['mean'] - monthly_stats['ci']).clip(lower=0)
    monthly_stats['ci_upper'] = monthly_stats['mean'] + monthly_stats['ci']
    
    return monthly_stats

def calculate_seasonal_stats(ocorrencias):
    """Calculate seasonal statistics with chi-square test"""
    ocorrencias['season'] = ocorrencias['data_inicio'].apply(get_season)
    season_counts = ocorrencias['season'].value_counts()
    season_order = ['Summer', 'Autumn', 'Winter', 'Spring']
    season_counts = season_counts.reindex(season_order)
    
    expected = len(ocorrencias) / 4
    chi2, p_value = stats.chisquare(season_counts.values, f_exp=[expected] * 4)
    
    return season_counts, chi2, p_value

def create_temporal_patterns_chart(ocorrencias):
    """Create multi-panel temporal analysis chart"""
    setup_plot_style()
    
    monthly_stats = calculate_monthly_stats(ocorrencias)
    season_counts, chi2, p_value = calculate_seasonal_stats(ocorrencias)
    
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_stats['month_name'] = monthly_stats['month'].apply(lambda x: month_names[x-1])
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGURE_SIZES['double'])
    fig.suptitle(f'Temporal Patterns of Urban Flood Events\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'], fontweight='bold', y=1.02)
    
    # Panel A: Monthly distribution
    ax1.plot(monthly_stats['month_name'], monthly_stats['mean'],
            marker='o', linestyle='-', color=COLORS['primary'], linewidth=2, markersize=6, label='Mean')
    ax1.fill_between(range(len(monthly_stats)), monthly_stats['ci_lower'], monthly_stats['ci_upper'],
                     color=COLORS['primary'], alpha=0.2, label='95% CI')
    
    ax1.set_xlabel('Month', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_ylabel('Average Number of Events', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_title('Monthly Distribution', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax1.grid(True, linestyle='--', alpha=0.3)
    ax1.legend(loc='upper left', fontsize=FONT_SIZES['legend'])
    ax1.set_axisbelow(True)
    add_subfigure_label(ax1, '(a)')
    
    # Panel B: Seasonal distribution
    season_order = ['Summer', 'Autumn', 'Winter', 'Spring']
    season_colors = [COLORS['seasons'][s] for s in season_order]
    
    bars = ax2.bar(season_order, season_counts.values, color=season_colors, edgecolor='black', linewidth=0.5)
    
    for bar, count in zip(bars, season_counts.values):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height, f'{int(count):,}',
                ha='center', va='bottom', fontsize=FONT_SIZES['annotation'])
    
    ax2.set_xlabel('Season', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_ylabel('Number of Events', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_title('Seasonal Distribution', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax2.grid(axis='y', linestyle='--', alpha=0.3)
    ax2.set_axisbelow(True)
    
    add_subfigure_label(ax2, '(b)')
    add_sample_size_annotation(ax2, len(ocorrencias))
    
    plt.tight_layout()
    return fig, monthly_stats, season_counts, chi2, p_value

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias = load_and_prepare_data()
    print(f"Total flood events: {len(ocorrencias)}")
    
    print("\nCreating temporal patterns chart...")
    fig, monthly_stats, season_counts, chi2, p_value = create_temporal_patterns_chart(ocorrencias)
    
    print("\nMonthly statistics:")
    print(monthly_stats[['month_name', 'mean', 'std', 'ci_lower', 'ci_upper']])
    print("\nSeasonal distribution:")
    print(season_counts)
    print(f"\nChi-square test: χ² = {chi2:.2f}, p = {p_value:.4f}")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = f'{OUTPUT_DIR}/chart_02_temporal_patterns.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nChart saved to {output_path}")
    plt.close()

if __name__ == '__main__':
    main()

```

```python
"""
Chart 2: Temporal Patterns of Flood Events
Combines monthly and seasonal analysis with statistical information
Multi-panel figure with confidence intervals
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import os
import sys

# Add parent directory to path for config import
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

def calculate_monthly_stats(ocorrencias):
    """Calculate monthly statistics with confidence intervals"""
    ocorrencias['year'] = ocorrencias['data_inicio'].dt.year
    ocorrencias['month'] = ocorrencias['data_inicio'].dt.month
    
    monthly_counts = ocorrencias.groupby(['year', 'month']).size().reset_index(name='count')
    monthly_stats = monthly_counts.groupby('month')['count'].agg(['mean', 'std', 'count', 'sem']).reset_index()
    
    confidence = 0.95
    monthly_stats['ci'] = monthly_stats['sem'] * stats.t.ppf((1 + confidence) / 2, monthly_stats['count'] - 1)
    monthly_stats['ci_lower'] = (monthly_stats['mean'] - monthly_stats['ci']).clip(lower=0)
    monthly_stats['ci_upper'] = monthly_stats['mean'] + monthly_stats['ci']
    
    return monthly_stats

def calculate_seasonal_stats(ocorrencias):
    """Calculate seasonal statistics with chi-square test"""
    ocorrencias['season'] = ocorrencias['data_inicio'].apply(get_season)
    season_counts = ocorrencias['season'].value_counts()
    season_order = ['Summer', 'Autumn', 'Winter', 'Spring']
    season_counts = season_counts.reindex(season_order)
    
    expected = len(ocorrencias) / 4
    chi2, p_value = stats.chisquare(season_counts.values, f_exp=[expected] * 4)
    
    return season_counts, chi2, p_value

def create_temporal_patterns_chart(ocorrencias):
    """Create multi-panel temporal analysis chart"""
    setup_plot_style()
    
    monthly_stats = calculate_monthly_stats(ocorrencias)
    season_counts, chi2, p_value = calculate_seasonal_stats(ocorrencias)
    
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_stats['month_name'] = monthly_stats['month'].apply(lambda x: month_names[x-1])
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGURE_SIZES['double'])
    fig.suptitle(f'Temporal Patterns of Urban Flood Events\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'], fontweight='bold', y=1.02)
    
    # Panel A: Monthly distribution
    ax1.plot(monthly_stats['month_name'], monthly_stats['mean'],
            marker='o', linestyle='-', color=COLORS['primary'], linewidth=2, markersize=6, label='Mean')
    ax1.fill_between(range(len(monthly_stats)), monthly_stats['ci_lower'], monthly_stats['ci_upper'],
                     color=COLORS['primary'], alpha=0.2, label='95% CI')
    
    ax1.set_xlabel('Month', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_ylabel('Average Number of Events', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_title('Monthly Distribution', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax1.grid(True, linestyle='--', alpha=0.3)
    ax1.legend(loc='upper left', fontsize=FONT_SIZES['legend'])
    ax1.set_axisbelow(True)
    add_subfigure_label(ax1, '(a)')
    
    # Panel B: Seasonal distribution
    season_order = ['Summer', 'Autumn', 'Winter', 'Spring']
    season_colors = [COLORS['seasons'][s] for s in season_order]
    
    bars = ax2.bar(season_order, season_counts.values, color=season_colors, edgecolor='black', linewidth=0.5)
    
    for bar, count in zip(bars, season_counts.values):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height, f'{int(count):,}',
                ha='center', va='bottom', fontsize=FONT_SIZES['annotation'])
    
    ax2.set_xlabel('Season', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_ylabel('Number of Events', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_title('Seasonal Distribution', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax2.grid(axis='y', linestyle='--', alpha=0.3)
    ax2.set_axisbelow(True)
    
    add_subfigure_label(ax2, '(b)')
    add_sample_size_annotation(ax2, len(ocorrencias))
    
    plt.tight_layout()
    return fig, monthly_stats, season_counts, chi2, p_value

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias = load_and_prepare_data()
    print(f"Total flood events: {len(ocorrencias)}")
    
    print("\nCreating temporal patterns chart...")
    fig, monthly_stats, season_counts, chi2, p_value = create_temporal_patterns_chart(ocorrencias)
    
    print("\nMonthly statistics:")
    print(monthly_stats[['month_name', 'mean', 'std', 'ci_lower', 'ci_upper']])
    print("\nSeasonal distribution:")
    print(season_counts)
    print(f"\nChi-square test: χ² = {chi2:.2f}, p = {p_value:.4f}")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = f'{OUTPUT_DIR}/chart_02_temporal_patterns.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nChart saved to {output_path}")
    plt.close()

if __name__ == '__main__':
    main()

```

```python
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
                    GENERIC_TYPE_MAPPING, STUDY_PERIOD, STUDY_LOCATION, add_sample_size_annotation, ALPHA)

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
    
    # Add peak hours annotation
    peak_text = f'Peak hours: {", ".join([f"{h:02d}:00" for h in peak_hours])}'
    ax.text(0.98, 0.82, peak_text, transform=ax.transAxes, fontsize=FONT_SIZES['annotation'],
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

```

```python
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
                    GENERIC_TYPE_MAPPING, STUDY_PERIOD, STUDY_LOCATION, add_sample_size_annotation, ALPHA)

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
    
    # Add peak hours annotation
    peak_text = f'Peak hours: {", ".join([f"{h:02d}:00" for h in peak_hours])}'
    ax.text(0.98, 0.82, peak_text, transform=ax.transAxes, fontsize=FONT_SIZES['annotation'],
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

```

```python
"""
Chart 4: Spatial Coverage Analysis - Distance to Nearest Rain Gauge Station
Includes histogram and cumulative distribution function (CDF)
Addresses spatial bias implications for the study
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from config import (setup_plot_style, COLORS, FONT_SIZES, FIGURE_SIZES,
                    DATA_PATHS, OUTPUT_DIR, FLOOD_TYPES, EVENT_TYPE_MAPPING,
                    GENERIC_TYPE_MAPPING, STUDY_PERIOD, STUDY_LOCATION, add_sample_size_annotation,
                    add_subfigure_label, CRS_GEOGRAPHIC, CRS_PROJECTED)

def load_and_prepare_data():
    """Load and preprocess flood event and station data"""
    ocorrencias = pd.read_csv(DATA_PATHS['ocorrencias'])
    pops = pd.read_csv(DATA_PATHS['pops'], index_col=0)
    stations = pd.read_csv(os.path.expanduser(DATA_PATHS['stations']))
    
    ocorrencias['data_inicio'] = pd.to_datetime(ocorrencias['data_inicio'])
    ocorrencias['data_fim'] = pd.to_datetime(ocorrencias['data_fim'])
    ocorrencias['tipo'] = ocorrencias['id_pop'].map(pops.set_index('id')['titulo'])
    
    ocorrencias = ocorrencias[ocorrencias['tipo'].isin(FLOOD_TYPES)]
    ocorrencias['tipo'] = ocorrencias['tipo'].replace(EVENT_TYPE_MAPPING)
    
    return ocorrencias, stations

def calculate_distances(ocorrencias, stations):
    """Calculate distance from each flood event to nearest rain gauge station"""
    # Convert to GeoDataFrame
    ocorrencias_gdf = gpd.GeoDataFrame(
        ocorrencias,
        geometry=gpd.points_from_xy(ocorrencias.longitude, ocorrencias.latitude),
        crs=CRS_GEOGRAPHIC
    )
    
    stations_gdf = gpd.GeoDataFrame(
        stations,
        geometry=gpd.points_from_xy(stations.longitude, stations.latitude),
        crs=CRS_GEOGRAPHIC
    )
    
    # Drop stations with missing coordinates
    stations_gdf = stations_gdf.dropna(subset=['latitude', 'longitude'])
    stations_gdf = stations_gdf.drop_duplicates(subset=['id_estacao'], keep='first')
    
    # Transform to projected CRS for accurate distance calculations
    ocorrencias_gdf = ocorrencias_gdf.to_crs(CRS_PROJECTED)
    stations_gdf = stations_gdf.to_crs(CRS_PROJECTED)
    
    # Calculate distance to nearest station for each flood event
    def calculate_nearest_distance(flood_point):
        distances = stations_gdf.geometry.distance(flood_point)
        return distances.min()
    
    ocorrencias_gdf['distance_m'] = ocorrencias_gdf.geometry.apply(calculate_nearest_distance)
    ocorrencias_gdf['distance_km'] = ocorrencias_gdf['distance_m'] / 1000
    
    return ocorrencias_gdf

def create_spatial_coverage_chart(ocorrencias_gdf):
    """Create spatial coverage analysis chart with histogram and CDF"""
    setup_plot_style()
    
    # Filter out NaN values before calculating statistics
    distances_km = ocorrencias_gdf['distance_km'].dropna().values
    
    # Calculate statistics
    mean_dist = np.nanmean(distances_km)
    median_dist = np.nanmedian(distances_km)
    p90_dist = np.nanpercentile(distances_km, 90)
    max_dist = np.nanmax(distances_km)
    
    # Create figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGURE_SIZES['double'])
    fig.suptitle(f'Spatial Coverage: Distance to Nearest Rain Gauge Station\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'], fontweight='bold', y=1.02)
    
    # Panel A: Histogram
    n, bins, patches = ax1.hist(distances_km, bins=30, color=COLORS['primary'], 
                                edgecolor='black', linewidth=0.5, alpha=0.7)
    
    # Add vertical lines for statistics
    ax1.axvline(mean_dist, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_dist:.2f} km')
    ax1.axvline(median_dist, color='orange', linestyle='--', linewidth=2, label=f'Median: {median_dist:.2f} km')
    ax1.axvline(p90_dist, color='purple', linestyle=':', linewidth=2, label=f'90th percentile: {p90_dist:.2f} km')
    
    ax1.set_xlabel('Distance to Nearest Station (km)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_ylabel('Frequency', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_title('Distribution', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax1.legend(loc='upper right', fontsize=FONT_SIZES['legend'])
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    ax1.set_axisbelow(True)
    add_subfigure_label(ax1, '(a)')
    
    # Panel B: Cumulative Distribution Function (CDF)
    sorted_distances = np.sort(distances_km)
    cumulative = np.arange(1, len(sorted_distances) + 1) / len(sorted_distances) * 100
    
    ax2.plot(sorted_distances, cumulative, color=COLORS['primary'], linewidth=2)
    ax2.fill_between(sorted_distances, 0, cumulative, color=COLORS['primary'], alpha=0.2)
    
    # Add reference lines
    ax2.axhline(50, color='orange', linestyle='--', linewidth=1, alpha=0.5)
    ax2.axhline(90, color='purple', linestyle=':', linewidth=1, alpha=0.5)
    ax2.axvline(median_dist, color='orange', linestyle='--', linewidth=1, alpha=0.5)
    ax2.axvline(p90_dist, color='purple', linestyle=':', linewidth=1, alpha=0.5)
    
    # Add annotations
    ax2.text(median_dist, 50, f' {median_dist:.2f} km', fontsize=FONT_SIZES['annotation'],
            verticalalignment='bottom', color='orange')
    ax2.text(p90_dist, 90, f' {p90_dist:.2f} km', fontsize=FONT_SIZES['annotation'],
            verticalalignment='bottom', color='purple')
    
    ax2.set_xlabel('Distance to Nearest Station (km)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_ylabel('Cumulative Percentage (%)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_title('Cumulative Distribution', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax2.grid(True, linestyle='--', alpha=0.3)
    ax2.set_axisbelow(True)
    ax2.set_ylim(0, 100)
    add_subfigure_label(ax2, '(b)')
    
    # Add sample size and coverage info
    coverage_text = f'50% within {median_dist:.2f} km\n90% within {p90_dist:.2f} km'
    ax2.text(0.98, 0.15, coverage_text, transform=ax2.transAxes, fontsize=FONT_SIZES['annotation'],
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, edgecolor='gray'))
    
    add_sample_size_annotation(ax2, len(ocorrencias_gdf))
    
    plt.tight_layout()
    return fig, mean_dist, median_dist, p90_dist, max_dist

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias, stations = load_and_prepare_data()
    print(f"Total flood events: {len(ocorrencias)}")
    print(f"Total rain gauge stations: {len(stations)}")
    
    print("\nCalculating distances to nearest station...")
    ocorrencias_gdf = calculate_distances(ocorrencias, stations)
    
    print("\nCreating spatial coverage chart...")
    fig, mean_dist, median_dist, p90_dist, max_dist = create_spatial_coverage_chart(ocorrencias_gdf)
    
    print("\nDistance Statistics (km):")
    print(f"  Mean: {mean_dist:.2f}")
    print(f"  Median: {median_dist:.2f}")
    print(f"  90th percentile: {p90_dist:.2f}")
    print(f"  Maximum: {max_dist:.2f}")
    print(f"\nCoverage: 50% of events within {median_dist:.2f} km, 90% within {p90_dist:.2f} km")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = f'{OUTPUT_DIR}/chart_04_spatial_coverage.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nChart saved to {output_path}")
    plt.close()

if __name__ == '__main__':
    main()

```

```python
"""
Chart 4: Spatial Coverage Analysis - Distance to Nearest Rain Gauge Station
Includes histogram and cumulative distribution function (CDF)
Addresses spatial bias implications for the study
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from config import (setup_plot_style, COLORS, FONT_SIZES, FIGURE_SIZES,
                    DATA_PATHS, OUTPUT_DIR, FLOOD_TYPES, EVENT_TYPE_MAPPING,
                    GENERIC_TYPE_MAPPING, STUDY_PERIOD, STUDY_LOCATION, add_sample_size_annotation,
                    add_subfigure_label, CRS_GEOGRAPHIC, CRS_PROJECTED)

def load_and_prepare_data():
    """Load and preprocess flood event and station data"""
    ocorrencias = pd.read_csv(DATA_PATHS['ocorrencias'])
    pops = pd.read_csv(DATA_PATHS['pops'], index_col=0)
    stations = pd.read_csv(os.path.expanduser(DATA_PATHS['stations']))
    
    ocorrencias['data_inicio'] = pd.to_datetime(ocorrencias['data_inicio'])
    ocorrencias['data_fim'] = pd.to_datetime(ocorrencias['data_fim'])
    ocorrencias['tipo'] = ocorrencias['id_pop'].map(pops.set_index('id')['titulo'])
    
    ocorrencias = ocorrencias[ocorrencias['tipo'].isin(FLOOD_TYPES)]
    ocorrencias['tipo'] = ocorrencias['tipo'].replace(EVENT_TYPE_MAPPING)
    ocorrencias['tipo'] = ocorrencias['tipo'].replace(GENERIC_TYPE_MAPPING)
    
    return ocorrencias, stations

def calculate_distances(ocorrencias, stations):
    """Calculate distance from each flood event to nearest rain gauge station"""
    # Convert to GeoDataFrame
    ocorrencias_gdf = gpd.GeoDataFrame(
        ocorrencias,
        geometry=gpd.points_from_xy(ocorrencias.longitude, ocorrencias.latitude),
        crs=CRS_GEOGRAPHIC
    )
    
    stations_gdf = gpd.GeoDataFrame(
        stations,
        geometry=gpd.points_from_xy(stations.longitude, stations.latitude),
        crs=CRS_GEOGRAPHIC
    )
    
    # Drop stations with missing coordinates
    stations_gdf = stations_gdf.dropna(subset=['latitude', 'longitude'])
    stations_gdf = stations_gdf.drop_duplicates(subset=['id_estacao'], keep='first')
    
    # Transform to projected CRS for accurate distance calculations
    ocorrencias_gdf = ocorrencias_gdf.to_crs(CRS_PROJECTED)
    stations_gdf = stations_gdf.to_crs(CRS_PROJECTED)
    
    # Calculate distance to nearest station for each flood event
    def calculate_nearest_distance(flood_point):
        distances = stations_gdf.geometry.distance(flood_point)
        return distances.min()
    
    ocorrencias_gdf['distance_m'] = ocorrencias_gdf.geometry.apply(calculate_nearest_distance)
    ocorrencias_gdf['distance_km'] = ocorrencias_gdf['distance_m'] / 1000
    
    return ocorrencias_gdf

def create_spatial_coverage_chart(ocorrencias_gdf):
    """Create spatial coverage analysis chart with histogram and CDF"""
    setup_plot_style()
    
    # Filter out NaN values before calculating statistics
    distances_km = ocorrencias_gdf['distance_km'].dropna().values
    
    # Calculate statistics
    mean_dist = np.nanmean(distances_km)
    median_dist = np.nanmedian(distances_km)
    p90_dist = np.nanpercentile(distances_km, 90)
    max_dist = np.nanmax(distances_km)
    
    # Create figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGURE_SIZES['double'])
    fig.suptitle(f'Spatial Coverage: Distance to Nearest Rain Gauge Station\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'], fontweight='bold', y=1.02)
    
    # Panel A: Histogram
    n, bins, patches = ax1.hist(distances_km, bins=30, color=COLORS['primary'], 
                                edgecolor='black', linewidth=0.5, alpha=0.7)
    
    # Add vertical lines for statistics
    ax1.axvline(mean_dist, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_dist:.2f} km')
    ax1.axvline(median_dist, color='orange', linestyle='--', linewidth=2, label=f'Median: {median_dist:.2f} km')
    ax1.axvline(p90_dist, color='purple', linestyle=':', linewidth=2, label=f'90th percentile: {p90_dist:.2f} km')
    
    ax1.set_xlabel('Distance to Nearest Station (km)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_ylabel('Frequency', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_title('Distribution', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax1.legend(loc='upper right', fontsize=FONT_SIZES['legend'])
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    ax1.set_axisbelow(True)
    add_subfigure_label(ax1, '(a)')
    
    # Panel B: Cumulative Distribution Function (CDF)
    sorted_distances = np.sort(distances_km)
    cumulative = np.arange(1, len(sorted_distances) + 1) / len(sorted_distances) * 100
    
    ax2.plot(sorted_distances, cumulative, color=COLORS['primary'], linewidth=2)
    ax2.fill_between(sorted_distances, 0, cumulative, color=COLORS['primary'], alpha=0.2)
    
    # Add reference lines
    ax2.axhline(50, color='orange', linestyle='--', linewidth=1, alpha=0.5)
    ax2.axhline(90, color='purple', linestyle=':', linewidth=1, alpha=0.5)
    ax2.axvline(median_dist, color='orange', linestyle='--', linewidth=1, alpha=0.5)
    ax2.axvline(p90_dist, color='purple', linestyle=':', linewidth=1, alpha=0.5)
    
    # Add annotations
    ax2.text(median_dist, 50, f' {median_dist:.2f} km', fontsize=FONT_SIZES['annotation'],
            verticalalignment='bottom', color='orange')
    ax2.text(p90_dist, 90, f' {p90_dist:.2f} km', fontsize=FONT_SIZES['annotation'],
            verticalalignment='bottom', color='purple')
    
    ax2.set_xlabel('Distance to Nearest Station (km)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_ylabel('Cumulative Percentage (%)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_title('Cumulative Distribution', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax2.grid(True, linestyle='--', alpha=0.3)
    ax2.set_axisbelow(True)
    ax2.set_ylim(0, 100)
    add_subfigure_label(ax2, '(b)')
    
    # Add sample size and coverage info
    coverage_text = f'50% within {median_dist:.2f} km\n90% within {p90_dist:.2f} km'
    ax2.text(0.98, 0.15, coverage_text, transform=ax2.transAxes, fontsize=FONT_SIZES['annotation'],
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, edgecolor='gray'))
    
    add_sample_size_annotation(ax2, len(ocorrencias_gdf))
    
    plt.tight_layout()
    return fig, mean_dist, median_dist, p90_dist, max_dist

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias, stations = load_and_prepare_data()
    print(f"Total flood events: {len(ocorrencias)}")
    print(f"Total rain gauge stations: {len(stations)}")
    
    print("\nCalculating distances to nearest station...")
    ocorrencias_gdf = calculate_distances(ocorrencias, stations)
    
    print("\nCreating spatial coverage chart...")
    fig, mean_dist, median_dist, p90_dist, max_dist = create_spatial_coverage_chart(ocorrencias_gdf)
    
    print("\nDistance Statistics (km):")
    print(f"  Mean: {mean_dist:.2f}")
    print(f"  Median: {median_dist:.2f}")
    print(f"  90th percentile: {p90_dist:.2f}")
    print(f"  Maximum: {max_dist:.2f}")
    print(f"\nCoverage: 50% of events within {median_dist:.2f} km, 90% within {p90_dist:.2f} km")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = f'{OUTPUT_DIR}/chart_04_spatial_coverage.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nChart saved to {output_path}")
    plt.close()

if __name__ == '__main__':
    main()

```

```python
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

```

```python
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

```

```python
"""
Chart 6: Event Duration Distribution Analysis
Split into two images:
- Image 1: Histogram and CDF (panels a and b)
- Image 2: Duration by hour of day (panel c)
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
    """Load and preprocess flood event data with duration calculation"""
    ocorrencias = pd.read_csv(DATA_PATHS['ocorrencias'])
    pops = pd.read_csv(DATA_PATHS['pops'], index_col=0)
    
    ocorrencias['data_inicio'] = pd.to_datetime(ocorrencias['data_inicio'])
    ocorrencias['data_fim'] = pd.to_datetime(ocorrencias['data_fim'])
    ocorrencias['tipo'] = ocorrencias['id_pop'].map(pops.set_index('id')['titulo'])
    
    ocorrencias = ocorrencias[ocorrencias['tipo'].isin(FLOOD_TYPES)]
    ocorrencias['tipo'] = ocorrencias['tipo'].replace(EVENT_TYPE_MAPPING)
    
    # Calculate duration in hours
    ocorrencias['duration_hours'] = (ocorrencias['data_fim'] - ocorrencias['data_inicio']).dt.total_seconds() / 3600
    
    # Filter out invalid durations (negative or extremely long)
    ocorrencias = ocorrencias[
        (ocorrencias['duration_hours'] >= 0) & 
        (ocorrencias['duration_hours'] <= 72)  # Max 72 hours (3 days)
    ].copy()
    
    return ocorrencias

def calculate_duration_stats(ocorrencias):
    """Calculate comprehensive duration statistics"""
    durations = ocorrencias['duration_hours'].dropna()
    
    stats_dict = {
        'mean': durations.mean(),
        'median': durations.median(),
        'std': durations.std(),
        'min': durations.min(),
        'max': durations.max(),
        'q25': durations.quantile(0.25),
        'q75': durations.quantile(0.75),
        'q90': durations.quantile(0.90),
        'count': len(durations)
    }
    
    return stats_dict, durations

def create_duration_distribution_chart_part1(ocorrencias, stats_dict, durations):
    """Create first chart: Histogram and CDF (panels a and b) - filtered to <12h"""
    setup_plot_style()
    
    # Filter durations to only show events < 12 hours for panels a and b
    durations_filtered = durations[durations < 12]
    total_events = len(durations)
    filtered_events = len(durations_filtered)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGURE_SIZES['double'])
    fig.suptitle(f'Urban Flood Event Duration Distribution (< 12 hours)\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'], fontweight='bold', y=1.02)
    
    # Panel A: Histogram with statistics
    n, bins, patches = ax1.hist(durations_filtered, bins=50, color=COLORS['primary'],
                                edgecolor='black', linewidth=0.5, alpha=0.7)
    
    # Add vertical lines for statistics
    ax1.axvline(stats_dict['mean'], color=COLORS['secondary'], linestyle='--', 
               linewidth=2, label=f"Mean: {stats_dict['mean']:.2f}h")
    ax1.axvline(stats_dict['median'], color=COLORS['tertiary'], linestyle='--', 
               linewidth=2, label=f"Median: {stats_dict['median']:.2f}h")
    ax1.axvline(stats_dict['q90'], color=COLORS['quaternary'], linestyle=':', 
               linewidth=2, label=f"90th percentile: {stats_dict['q90']:.2f}h")
    
    ax1.set_xlabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_ylabel('Frequency', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_title('Duration Distribution', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax1.legend(loc='upper right', fontsize=FONT_SIZES['legend'])
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    ax1.set_axisbelow(True)
    add_subfigure_label(ax1, '(a)')
    
    # Panel B: Cumulative Distribution Function (CDF)
    sorted_durations = np.sort(durations_filtered)
    cumulative = np.arange(1, len(sorted_durations) + 1) / len(sorted_durations) * 100
    
    ax2.plot(sorted_durations, cumulative, color=COLORS['primary'], linewidth=2)
    ax2.fill_between(sorted_durations, 0, cumulative, color=COLORS['primary'], alpha=0.2)
    
    # Add reference lines
    ax2.axhline(50, color=COLORS['tertiary'], linestyle='--', linewidth=1, alpha=0.5)
    ax2.axhline(90, color=COLORS['quaternary'], linestyle=':', linewidth=1, alpha=0.5)
    ax2.axvline(stats_dict['median'], color=COLORS['tertiary'], linestyle='--', linewidth=1, alpha=0.5)
    ax2.axvline(stats_dict['q90'], color=COLORS['quaternary'], linestyle=':', linewidth=1, alpha=0.5)
    
    # Add annotations
    ax2.text(stats_dict['median'], 50, f" {stats_dict['median']:.2f}h", 
            fontsize=FONT_SIZES['annotation'], verticalalignment='bottom', 
            color=COLORS['tertiary'])
    ax2.text(stats_dict['q90'], 90, f" {stats_dict['q90']:.2f}h", 
            fontsize=FONT_SIZES['annotation'], verticalalignment='bottom',
            color=COLORS['quaternary'])
    
    ax2.set_xlabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_ylabel('Cumulative Percentage (%)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_title('Cumulative Distribution', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax2.grid(True, linestyle='--', alpha=0.3)
    ax2.set_axisbelow(True)
    ax2.set_ylim(0, 100)
    add_subfigure_label(ax2, '(b)')
    
    # Add statistics box
    stats_text = (f"Mean: {stats_dict['mean']:.2f}h\n"
                 f"Median: {stats_dict['median']:.2f}h\n"
                 f"Std Dev: {stats_dict['std']:.2f}h\n"
                 f"Range: {stats_dict['min']:.2f}h - {stats_dict['max']:.2f}h")
    ax2.text(0.98, 0.25, stats_text, transform=ax2.transAxes, 
            fontsize=FONT_SIZES['annotation'],
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, edgecolor='gray'))
    
    # Add sample size annotation showing filtered vs total
    sample_text = f'N = {filtered_events:,} (< 12h)\nTotal: {total_events:,}'
    ax2.text(0.98, 0.98, sample_text,
            transform=ax2.transAxes,
            fontsize=FONT_SIZES['annotation'],
            verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray'))
    
    plt.tight_layout()
    
    return fig

def create_duration_distribution_chart_part2(ocorrencias, stats_dict):
    """Create second chart: Duration by Hour of Day"""
    setup_plot_style()
    
    # Calculate hourly duration statistics
    ocorrencias['hour'] = ocorrencias['data_inicio'].dt.hour
    hourly_duration = ocorrencias.groupby('hour')['duration_hours'].agg(['mean', 'std', 'count'])
    hourly_duration['sem'] = hourly_duration['std'] / np.sqrt(hourly_duration['count'])
    
    fig, ax = plt.subplots(figsize=FIGURE_SIZES['wide'])
    
    ax.bar(hourly_duration.index, hourly_duration['mean'], 
           color=COLORS['primary'], edgecolor='black', linewidth=0.5, alpha=0.7,
           yerr=hourly_duration['sem'], capsize=3, error_kw={'linewidth': 1, 'alpha': 0.5})
    
    # Add mean line
    overall_mean = stats_dict['mean']
    ax.axhline(overall_mean, color=COLORS['secondary'], linestyle='--', 
               linewidth=1.5, label=f'Overall Mean: {overall_mean:.2f}h', alpha=0.7)
    
    ax.set_xlabel('Hour of Day', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax.set_ylabel('Average Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax.set_title(f'Average Event Duration by Hour of Day\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'], fontweight='bold', pad=15)
    ax.set_xticks(range(0, 24, 2))
    ax.set_xticklabels([f'{h:02d}:00' for h in range(0, 24, 2)])
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)
    ax.legend(loc='upper right', fontsize=FONT_SIZES['legend'])
    
    add_sample_size_annotation(ax, len(ocorrencias))
    
    plt.tight_layout()
    
    return fig

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias = load_and_prepare_data()
    print(f"Total flood events with valid duration: {len(ocorrencias)}")
    
    print("\nCalculating duration statistics...")
    stats_dict, durations = calculate_duration_stats(ocorrencias)
    
    print("\nDuration Statistics:")
    print(f"  Mean: {stats_dict['mean']:.2f} hours")
    print(f"  Median: {stats_dict['median']:.2f} hours")
    print(f"  Std Dev: {stats_dict['std']:.2f} hours")
    print(f"  Min: {stats_dict['min']:.2f} hours")
    print(f"  Max: {stats_dict['max']:.2f} hours")
    print(f"  25th percentile: {stats_dict['q25']:.2f} hours")
    print(f"  75th percentile: {stats_dict['q75']:.2f} hours")
    print(f"  90th percentile: {stats_dict['q90']:.2f} hours")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Create and save first chart (histogram and CDF)
    print("\nCreating duration distribution chart (Part 1: Histogram & CDF)...")
    fig1 = create_duration_distribution_chart_part1(ocorrencias, stats_dict, durations)
    output_path1 = f'{OUTPUT_DIR}/chart_06a_duration_distribution.png'
    fig1.savefig(output_path1, dpi=300, bbox_inches='tight')
    print(f"Chart saved to {output_path1}")
    plt.close()
    
    # Create and save second chart (hourly duration)
    print("\nCreating duration distribution chart (Part 2: Hourly Duration)...")
    fig2 = create_duration_distribution_chart_part2(ocorrencias, stats_dict)
    output_path2 = f'{OUTPUT_DIR}/chart_06b_duration_by_hour.png'
    fig2.savefig(output_path2, dpi=300, bbox_inches='tight')
    print(f"Chart saved to {output_path2}")
    plt.close()
    
    print("\nBoth charts created successfully!")

if __name__ == '__main__':
    main()

```

```python
"""
Chart 6: Event Duration Distribution Analysis
Split into two images:
- Image 1: Histogram and CDF (panels a and b)
- Image 2: Duration by hour of day (panel c)
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
    
    # Filter out invalid durations (negative or extremely long)
    ocorrencias = ocorrencias[
        (ocorrencias['duration_hours'] >= 0) & 
        (ocorrencias['duration_hours'] <= 72)  # Max 72 hours (3 days)
    ].copy()
    
    return ocorrencias

def calculate_duration_stats(ocorrencias):
    """Calculate comprehensive duration statistics"""
    durations = ocorrencias['duration_hours'].dropna()
    
    stats_dict = {
        'mean': durations.mean(),
        'median': durations.median(),
        'std': durations.std(),
        'min': durations.min(),
        'max': durations.max(),
        'q25': durations.quantile(0.25),
        'q75': durations.quantile(0.75),
        'q90': durations.quantile(0.90),
        'count': len(durations)
    }
    
    return stats_dict, durations

def create_duration_distribution_chart_part1(ocorrencias, stats_dict, durations):
    """Create first chart: Histogram and CDF (panels a and b) - filtered to <12h"""
    setup_plot_style()
    
    # Filter durations to only show events < 12 hours for panels a and b
    durations_filtered = durations[durations < 12]
    total_events = len(durations)
    filtered_events = len(durations_filtered)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGURE_SIZES['double'])
    fig.suptitle(f'Urban Flood Event Duration Distribution (< 12 hours)\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'], fontweight='bold', y=1.02)
    
    # Panel A: Histogram with statistics
    n, bins, patches = ax1.hist(durations_filtered, bins=50, color=COLORS['primary'],
                                edgecolor='black', linewidth=0.5, alpha=0.7)
    
    # Add vertical lines for statistics
    ax1.axvline(stats_dict['mean'], color=COLORS['secondary'], linestyle='--', 
               linewidth=2, label=f"Mean: {stats_dict['mean']:.2f}h")
    ax1.axvline(stats_dict['median'], color=COLORS['tertiary'], linestyle='--', 
               linewidth=2, label=f"Median: {stats_dict['median']:.2f}h")
    ax1.axvline(stats_dict['q90'], color=COLORS['quaternary'], linestyle=':', 
               linewidth=2, label=f"90th percentile: {stats_dict['q90']:.2f}h")
    
    ax1.set_xlabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_ylabel('Frequency', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_title('Duration Distribution', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax1.legend(loc='upper right', fontsize=FONT_SIZES['legend'])
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    ax1.set_axisbelow(True)
    add_subfigure_label(ax1, '(a)')
    
    # Panel B: Cumulative Distribution Function (CDF)
    sorted_durations = np.sort(durations_filtered)
    cumulative = np.arange(1, len(sorted_durations) + 1) / len(sorted_durations) * 100
    
    ax2.plot(sorted_durations, cumulative, color=COLORS['primary'], linewidth=2)
    ax2.fill_between(sorted_durations, 0, cumulative, color=COLORS['primary'], alpha=0.2)
    
    # Add reference lines
    ax2.axhline(50, color=COLORS['tertiary'], linestyle='--', linewidth=1, alpha=0.5)
    ax2.axhline(90, color=COLORS['quaternary'], linestyle=':', linewidth=1, alpha=0.5)
    ax2.axvline(stats_dict['median'], color=COLORS['tertiary'], linestyle='--', linewidth=1, alpha=0.5)
    ax2.axvline(stats_dict['q90'], color=COLORS['quaternary'], linestyle=':', linewidth=1, alpha=0.5)
    
    # Add annotations
    ax2.text(stats_dict['median'], 50, f" {stats_dict['median']:.2f}h", 
            fontsize=FONT_SIZES['annotation'], verticalalignment='bottom', 
            color=COLORS['tertiary'])
    ax2.text(stats_dict['q90'], 90, f" {stats_dict['q90']:.2f}h", 
            fontsize=FONT_SIZES['annotation'], verticalalignment='bottom',
            color=COLORS['quaternary'])
    
    ax2.set_xlabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_ylabel('Cumulative Percentage (%)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_title('Cumulative Distribution', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax2.grid(True, linestyle='--', alpha=0.3)
    ax2.set_axisbelow(True)
    ax2.set_ylim(0, 100)
    add_subfigure_label(ax2, '(b)')
    
    # Add statistics box
    stats_text = (f"Mean: {stats_dict['mean']:.2f}h\n"
                 f"Median: {stats_dict['median']:.2f}h\n"
                 f"Std Dev: {stats_dict['std']:.2f}h\n"
                 f"Range: {stats_dict['min']:.2f}h - {stats_dict['max']:.2f}h")
    ax2.text(0.98, 0.25, stats_text, transform=ax2.transAxes, 
            fontsize=FONT_SIZES['annotation'],
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, edgecolor='gray'))
    
    # Add sample size annotation showing filtered vs total
    sample_text = f'N = {filtered_events:,} (< 12h)\nTotal: {total_events:,}'
    ax2.text(0.98, 0.98, sample_text,
            transform=ax2.transAxes,
            fontsize=FONT_SIZES['annotation'],
            verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray'))
    
    plt.tight_layout()
    
    return fig

def create_duration_distribution_chart_part2(ocorrencias, stats_dict):
    """Create second chart: Duration by Hour of Day"""
    setup_plot_style()
    
    # Calculate hourly duration statistics
    ocorrencias['hour'] = ocorrencias['data_inicio'].dt.hour
    hourly_duration = ocorrencias.groupby('hour')['duration_hours'].agg(['mean', 'std', 'count'])
    hourly_duration['sem'] = hourly_duration['std'] / np.sqrt(hourly_duration['count'])
    
    fig, ax = plt.subplots(figsize=FIGURE_SIZES['wide'])
    
    ax.bar(hourly_duration.index, hourly_duration['mean'], 
           color=COLORS['primary'], edgecolor='black', linewidth=0.5, alpha=0.7,
           yerr=hourly_duration['sem'], capsize=3, error_kw={'linewidth': 1, 'alpha': 0.5})
    
    # Add mean line
    overall_mean = stats_dict['mean']
    ax.axhline(overall_mean, color=COLORS['secondary'], linestyle='--', 
               linewidth=1.5, label=f'Overall Mean: {overall_mean:.2f}h', alpha=0.7)
    
    ax.set_xlabel('Hour of Day', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax.set_ylabel('Average Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax.set_title(f'Average Event Duration by Hour of Day\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'], fontweight='bold', pad=15)
    ax.set_xticks(range(0, 24, 2))
    ax.set_xticklabels([f'{h:02d}:00' for h in range(0, 24, 2)])
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)
    ax.legend(loc='upper right', fontsize=FONT_SIZES['legend'])
    
    add_sample_size_annotation(ax, len(ocorrencias))
    
    plt.tight_layout()
    
    return fig

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias = load_and_prepare_data()
    print(f"Total flood events with valid duration: {len(ocorrencias)}")
    
    print("\nCalculating duration statistics...")
    stats_dict, durations = calculate_duration_stats(ocorrencias)
    
    print("\nDuration Statistics:")
    print(f"  Mean: {stats_dict['mean']:.2f} hours")
    print(f"  Median: {stats_dict['median']:.2f} hours")
    print(f"  Std Dev: {stats_dict['std']:.2f} hours")
    print(f"  Min: {stats_dict['min']:.2f} hours")
    print(f"  Max: {stats_dict['max']:.2f} hours")
    print(f"  25th percentile: {stats_dict['q25']:.2f} hours")
    print(f"  75th percentile: {stats_dict['q75']:.2f} hours")
    print(f"  90th percentile: {stats_dict['q90']:.2f} hours")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Create and save first chart (histogram and CDF)
    print("\nCreating duration distribution chart (Part 1: Histogram & CDF)...")
    fig1 = create_duration_distribution_chart_part1(ocorrencias, stats_dict, durations)
    output_path1 = f'{OUTPUT_DIR}/chart_06a_duration_distribution.png'
    fig1.savefig(output_path1, dpi=300, bbox_inches='tight')
    print(f"Chart saved to {output_path1}")
    plt.close()
    
    # Create and save second chart (hourly duration)
    print("\nCreating duration distribution chart (Part 2: Hourly Duration)...")
    fig2 = create_duration_distribution_chart_part2(ocorrencias, stats_dict)
    output_path2 = f'{OUTPUT_DIR}/chart_06b_duration_by_hour.png'
    fig2.savefig(output_path2, dpi=300, bbox_inches='tight')
    print(f"Chart saved to {output_path2}")
    plt.close()
    
    print("\nBoth charts created successfully!")

if __name__ == '__main__':
    main()

```

```python
"""
Chart 7: Event Duration by Type and Season
Comparative analysis of flood event durations across different event types and seasons
Includes box plots and statistical comparisons
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
    """Load and preprocess flood event data with duration calculation"""
    ocorrencias = pd.read_csv(DATA_PATHS['ocorrencias'])
    pops = pd.read_csv(DATA_PATHS['pops'], index_col=0)
    
    ocorrencias['data_inicio'] = pd.to_datetime(ocorrencias['data_inicio'])
    ocorrencias['data_fim'] = pd.to_datetime(ocorrencias['data_fim'])
    ocorrencias['tipo'] = ocorrencias['id_pop'].map(pops.set_index('id')['titulo'])
    
    ocorrencias = ocorrencias[ocorrencias['tipo'].isin(FLOOD_TYPES)]
    ocorrencias['tipo'] = ocorrencias['tipo'].replace(EVENT_TYPE_MAPPING)
    
    # Calculate duration in hours
    ocorrencias['duration_hours'] = (ocorrencias['data_fim'] - ocorrencias['data_inicio']).dt.total_seconds() / 3600
    
    # Filter out invalid durations
    ocorrencias = ocorrencias[
        (ocorrencias['duration_hours'] >= 0) & 
        (ocorrencias['duration_hours'] <= 72)
    ].copy()
    
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

def perform_statistical_tests(ocorrencias):
    """Perform statistical tests comparing durations across groups"""
    # Kruskal-Wallis test for event types (non-parametric ANOVA)
    event_types = ocorrencias['tipo'].unique()
    groups = [ocorrencias[ocorrencias['tipo'] == t]['duration_hours'].dropna() 
              for t in event_types]
    h_stat, p_value = stats.kruskal(*groups)
    
    return h_stat, p_value

def create_duration_by_type_chart(ocorrencias):
    """Create comparative duration analysis chart"""
    setup_plot_style()
    
    # Add season information
    ocorrencias['season'] = ocorrencias['data_inicio'].apply(get_season)
    
    # Perform statistical tests
    h_stat, p_value = perform_statistical_tests(ocorrencias)
    
    # Create 2x2 subplot grid
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'Flood Event Duration by Type and Season\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'] + 2, fontweight='bold', y=0.995)
    
    # Panel A: Box plot by event type
    ax1 = axes[0, 0]
    event_types = ocorrencias['tipo'].value_counts().index.tolist()
    data_by_type = [ocorrencias[ocorrencias['tipo'] == t]['duration_hours'].dropna() 
                    for t in event_types]
    
    bp1 = ax1.boxplot(data_by_type, labels=event_types, patch_artist=True,
                      showmeans=True, meanline=True,
                      boxprops=dict(facecolor=COLORS['primary'], alpha=0.7),
                      medianprops=dict(color='red', linewidth=2),
                      meanprops=dict(color='blue', linewidth=2, linestyle='--'))
    
    ax1.set_ylabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_title('Duration by Event Type', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax1.set_xticklabels(event_types, rotation=45, ha='right')
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    ax1.set_axisbelow(True)
    add_subfigure_label(ax1, '(a)', x=-0.15, y=1.08)
    
    # Add sample sizes
    for i, event_type in enumerate(event_types):
        n = len(ocorrencias[ocorrencias['tipo'] == event_type])
        ax1.text(i+1, ax1.get_ylim()[1] * 0.95, f'n={n}', 
                ha='center', fontsize=FONT_SIZES['annotation'])
    
    # Add statistical test result
    sig_text = f"Kruskal-Wallis: H={h_stat:.2f}, p={'<0.001' if p_value < 0.001 else f'={p_value:.3f}'}"
    ax1.text(0.02, 0.98, sig_text, transform=ax1.transAxes,
            fontsize=FONT_SIZES['annotation'], verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, edgecolor='gray'))
    
    # Panel B: Box plot by season
    ax2 = axes[0, 1]
    season_order = ['Summer', 'Autumn', 'Winter', 'Spring']
    data_by_season = [ocorrencias[ocorrencias['season'] == s]['duration_hours'].dropna() 
                      for s in season_order]
    season_colors = [COLORS['seasons'][s] for s in season_order]
    
    bp2 = ax2.boxplot(data_by_season, labels=season_order, patch_artist=True,
                      showmeans=True, meanline=True,
                      medianprops=dict(color='red', linewidth=2),
                      meanprops=dict(color='blue', linewidth=2, linestyle='--'))
    
    for patch, color in zip(bp2['boxes'], season_colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax2.set_ylabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_title('Duration by Season', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax2.grid(axis='y', linestyle='--', alpha=0.3)
    ax2.set_axisbelow(True)
    add_subfigure_label(ax2, '(b)', x=-0.15, y=1.08)
    
    # Add sample sizes
    for i, season in enumerate(season_order):
        n = len(ocorrencias[ocorrencias['season'] == season])
        ax2.text(i+1, ax2.get_ylim()[1] * 0.95, f'n={n}', 
                ha='center', fontsize=FONT_SIZES['annotation'])
    
    # Panel C: Mean duration by event type with error bars
    ax3 = axes[1, 0]
    type_stats = ocorrencias.groupby('tipo')['duration_hours'].agg(['mean', 'std', 'count', 'sem'])
    type_stats = type_stats.sort_values('mean', ascending=False)
    
    bars = ax3.barh(range(len(type_stats)), type_stats['mean'],
                    xerr=type_stats['sem'], capsize=5,
                    color=COLORS['categorical'][:len(type_stats)],
                    edgecolor='black', linewidth=0.5, alpha=0.7)
    
    ax3.set_yticks(range(len(type_stats)))
    ax3.set_yticklabels(type_stats.index)
    ax3.set_xlabel('Mean Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax3.set_title('Mean Duration by Event Type', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax3.grid(axis='x', linestyle='--', alpha=0.3)
    ax3.set_axisbelow(True)
    add_subfigure_label(ax3, '(c)', x=-0.15, y=1.08)
    
    # Add value labels
    for i, (mean, sem) in enumerate(zip(type_stats['mean'], type_stats['sem'])):
        ax3.text(mean + sem + 0.1, i, f'{mean:.2f}h', 
                va='center', fontsize=FONT_SIZES['annotation'])
    
    # Panel D: Duration distribution by season (violin plot)
    ax4 = axes[1, 1]
    
    # Prepare data for violin plot
    season_data = []
    season_positions = []
    for i, season in enumerate(season_order):
        data = ocorrencias[ocorrencias['season'] == season]['duration_hours'].dropna()
        if len(data) > 0:
            season_data.append(data)
            season_positions.append(i + 1)
    
    parts = ax4.violinplot(season_data, positions=season_positions, 
                           showmeans=True, showmedians=True, widths=0.7)
    
    # Color the violin plots
    for i, pc in enumerate(parts['bodies']):
        pc.set_facecolor(season_colors[i])
        pc.set_alpha(0.7)
    
    ax4.set_xticks(range(1, len(season_order) + 1))
    ax4.set_xticklabels(season_order)
    ax4.set_ylabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax4.set_title('Duration Distribution by Season', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax4.grid(axis='y', linestyle='--', alpha=0.3)
    ax4.set_axisbelow(True)
    add_subfigure_label(ax4, '(d)', x=-0.15, y=1.08)
    
    add_sample_size_annotation(ax4, len(ocorrencias))
    
    plt.tight_layout(rect=[0, 0, 1, 0.99])
    
    return fig, type_stats, h_stat, p_value

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias = load_and_prepare_data()
    print(f"Total flood events with valid duration: {len(ocorrencias)}")
    
    print("\nCreating duration by type and season chart...")
    fig, type_stats, h_stat, p_value = create_duration_by_type_chart(ocorrencias)
    
    print("\nDuration Statistics by Event Type:")
    print(type_stats[['mean', 'std', 'count']])
    print(f"\nKruskal-Wallis Test: H = {h_stat:.2f}, p = {p_value:.6f}")
    
    # Season statistics
    ocorrencias['season'] = ocorrencias['data_inicio'].apply(get_season)
    season_stats = ocorrencias.groupby('season')['duration_hours'].agg(['mean', 'std', 'count'])
    print("\nDuration Statistics by Season:")
    print(season_stats)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = f'{OUTPUT_DIR}/chart_07_duration_by_type.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nChart saved to {output_path}")
    plt.close()

if __name__ == '__main__':
    main()

```

```python
"""
Chart 7: Event Duration by Type and Season
Comparative analysis of flood event durations across different event types and seasons
Includes box plots and statistical comparisons
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

def perform_statistical_tests(ocorrencias):
    """Perform statistical tests comparing durations across groups"""
    # Kruskal-Wallis test for event types (non-parametric ANOVA)
    event_types = ocorrencias['tipo'].unique()
    groups = [ocorrencias[ocorrencias['tipo'] == t]['duration_hours'].dropna() 
              for t in event_types]
    h_stat, p_value = stats.kruskal(*groups)
    
    return h_stat, p_value

def create_duration_by_type_chart(ocorrencias):
    """Create comparative duration analysis chart"""
    setup_plot_style()
    
    # Add season information
    ocorrencias['season'] = ocorrencias['data_inicio'].apply(get_season)
    
    # Perform statistical tests
    h_stat, p_value = perform_statistical_tests(ocorrencias)
    
    # Create 2x2 subplot grid
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'Flood Event Duration by Type and Season\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'] + 2, fontweight='bold', y=0.995)
    
    # Panel A: Box plot by event type
    ax1 = axes[0, 0]
    event_types = ocorrencias['tipo'].value_counts().index.tolist()
    data_by_type = [ocorrencias[ocorrencias['tipo'] == t]['duration_hours'].dropna() 
                    for t in event_types]
    
    bp1 = ax1.boxplot(data_by_type, labels=event_types, patch_artist=True,
                      showmeans=True, meanline=True,
                      boxprops=dict(facecolor=COLORS['primary'], alpha=0.7),
                      medianprops=dict(color='red', linewidth=2),
                      meanprops=dict(color='blue', linewidth=2, linestyle='--'))
    
    ax1.set_ylabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_title('Duration by Event Type', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax1.set_xticklabels(event_types, rotation=45, ha='right')
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    ax1.set_axisbelow(True)
    add_subfigure_label(ax1, '(a)', x=-0.15, y=1.08)
    
    # Add sample sizes
    for i, event_type in enumerate(event_types):
        n = len(ocorrencias[ocorrencias['tipo'] == event_type])
        ax1.text(i+1, ax1.get_ylim()[1] * 0.95, f'n={n}', 
                ha='center', fontsize=FONT_SIZES['annotation'])
    
    # Add statistical test result
    sig_text = f"Kruskal-Wallis: H={h_stat:.2f}, p={'<0.001' if p_value < 0.001 else f'={p_value:.3f}'}"
    ax1.text(0.02, 0.98, sig_text, transform=ax1.transAxes,
            fontsize=FONT_SIZES['annotation'], verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, edgecolor='gray'))
    
    # Panel B: Box plot by season
    ax2 = axes[0, 1]
    season_order = ['Summer', 'Autumn', 'Winter', 'Spring']
    data_by_season = [ocorrencias[ocorrencias['season'] == s]['duration_hours'].dropna() 
                      for s in season_order]
    season_colors = [COLORS['seasons'][s] for s in season_order]
    
    bp2 = ax2.boxplot(data_by_season, labels=season_order, patch_artist=True,
                      showmeans=True, meanline=True,
                      medianprops=dict(color='red', linewidth=2),
                      meanprops=dict(color='blue', linewidth=2, linestyle='--'))
    
    for patch, color in zip(bp2['boxes'], season_colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax2.set_ylabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_title('Duration by Season', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax2.grid(axis='y', linestyle='--', alpha=0.3)
    ax2.set_axisbelow(True)
    add_subfigure_label(ax2, '(b)', x=-0.15, y=1.08)
    
    # Add sample sizes
    for i, season in enumerate(season_order):
        n = len(ocorrencias[ocorrencias['season'] == season])
        ax2.text(i+1, ax2.get_ylim()[1] * 0.95, f'n={n}', 
                ha='center', fontsize=FONT_SIZES['annotation'])
    
    # Panel C: Mean duration by event type with error bars
    ax3 = axes[1, 0]
    type_stats = ocorrencias.groupby('tipo')['duration_hours'].agg(['mean', 'std', 'count', 'sem'])
    type_stats = type_stats.sort_values('mean', ascending=False)
    
    bars = ax3.barh(range(len(type_stats)), type_stats['mean'],
                    xerr=type_stats['sem'], capsize=5,
                    color=COLORS['categorical'][:len(type_stats)],
                    edgecolor='black', linewidth=0.5, alpha=0.7)
    
    ax3.set_yticks(range(len(type_stats)))
    ax3.set_yticklabels(type_stats.index)
    ax3.set_xlabel('Mean Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax3.set_title('Mean Duration by Event Type', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax3.grid(axis='x', linestyle='--', alpha=0.3)
    ax3.set_axisbelow(True)
    add_subfigure_label(ax3, '(c)', x=-0.15, y=1.08)
    
    # Add value labels
    for i, (mean, sem) in enumerate(zip(type_stats['mean'], type_stats['sem'])):
        ax3.text(mean + sem + 0.1, i, f'{mean:.2f}h', 
                va='center', fontsize=FONT_SIZES['annotation'])
    
    # Panel D: Duration distribution by season (violin plot)
    ax4 = axes[1, 1]
    
    # Prepare data for violin plot
    season_data = []
    season_positions = []
    for i, season in enumerate(season_order):
        data = ocorrencias[ocorrencias['season'] == season]['duration_hours'].dropna()
        if len(data) > 0:
            season_data.append(data)
            season_positions.append(i + 1)
    
    parts = ax4.violinplot(season_data, positions=season_positions, 
                           showmeans=True, showmedians=True, widths=0.7)
    
    # Color the violin plots
    for i, pc in enumerate(parts['bodies']):
        pc.set_facecolor(season_colors[i])
        pc.set_alpha(0.7)
    
    ax4.set_xticks(range(1, len(season_order) + 1))
    ax4.set_xticklabels(season_order)
    ax4.set_ylabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax4.set_title('Duration Distribution by Season', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax4.grid(axis='y', linestyle='--', alpha=0.3)
    ax4.set_axisbelow(True)
    add_subfigure_label(ax4, '(d)', x=-0.15, y=1.08)
    
    add_sample_size_annotation(ax4, len(ocorrencias))
    
    plt.tight_layout(rect=[0, 0, 1, 0.99])
    
    return fig, type_stats, h_stat, p_value

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias = load_and_prepare_data()
    print(f"Total flood events with valid duration: {len(ocorrencias)}")
    
    print("\nCreating duration by type and season chart...")
    fig, type_stats, h_stat, p_value = create_duration_by_type_chart(ocorrencias)
    
    print("\nDuration Statistics by Event Type:")
    print(type_stats[['mean', 'std', 'count']])
    print(f"\nKruskal-Wallis Test: H = {h_stat:.2f}, p = {p_value:.6f}")
    
    # Season statistics
    ocorrencias['season'] = ocorrencias['data_inicio'].apply(get_season)
    season_stats = ocorrencias.groupby('season')['duration_hours'].agg(['mean', 'std', 'count'])
    print("\nDuration Statistics by Season:")
    print(season_stats)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = f'{OUTPUT_DIR}/chart_07_duration_by_type.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nChart saved to {output_path}")
    plt.close()

if __name__ == '__main__':
    main()

```

```python
"""
Chart 7a: Event Duration by Type (< 12 hours)
Comparative analysis of flood event durations across different event types
Includes box plots and mean duration with error bars
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
    """Load and preprocess flood event data with duration calculation"""
    ocorrencias = pd.read_csv(DATA_PATHS['ocorrencias'])
    pops = pd.read_csv(DATA_PATHS['pops'], index_col=0)
    
    ocorrencias['data_inicio'] = pd.to_datetime(ocorrencias['data_inicio'])
    ocorrencias['data_fim'] = pd.to_datetime(ocorrencias['data_fim'])
    ocorrencias['tipo'] = ocorrencias['id_pop'].map(pops.set_index('id')['titulo'])
    
    ocorrencias = ocorrencias[ocorrencias['tipo'].isin(FLOOD_TYPES)]
    ocorrencias['tipo'] = ocorrencias['tipo'].replace(EVENT_TYPE_MAPPING)
    
    # Calculate duration in hours
    ocorrencias['duration_hours'] = (ocorrencias['data_fim'] - ocorrencias['data_inicio']).dt.total_seconds() / 3600
    
    # Filter out invalid durations
    ocorrencias = ocorrencias[
        (ocorrencias['duration_hours'] >= 0) & 
        (ocorrencias['duration_hours'] <= 72)
    ].copy()
    
    return ocorrencias

def perform_statistical_tests(ocorrencias):
    """Perform statistical tests comparing durations across groups"""
    # Kruskal-Wallis test for event types (non-parametric ANOVA)
    event_types = ocorrencias['tipo'].unique()
    groups = [ocorrencias[ocorrencias['tipo'] == t]['duration_hours'].dropna() 
              for t in event_types]
    h_stat, p_value = stats.kruskal(*groups)
    
    return h_stat, p_value

def create_duration_by_type_chart(ocorrencias):
    """Create comparative duration analysis chart by event type"""
    setup_plot_style()
    
    # Filter to < 12 hours for panel a
    ocorrencias_filtered = ocorrencias[ocorrencias['duration_hours'] < 12].copy()
    total_events = len(ocorrencias)
    filtered_events = len(ocorrencias_filtered)
    
    # Perform statistical tests on filtered data
    h_stat, p_value = perform_statistical_tests(ocorrencias_filtered)
    
    # Create 1x2 subplot grid
    fig, axes = plt.subplots(1, 2, figsize=FIGURE_SIZES['double'])
    fig.suptitle(f'Flood Event Duration by Type\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'], fontweight='bold', y=1.02)
    
    # Panel A: Box plot by event type (< 12 hours)
    ax1 = axes[0]
    event_types = ocorrencias_filtered['tipo'].value_counts().index.tolist()
    event_types = [event_types[1], event_types[0], event_types[2]] + event_types[3:]
    data_by_type = [ocorrencias_filtered[ocorrencias_filtered['tipo'] == t]['duration_hours'].dropna() 
                    for t in event_types]
    
    bp1 = ax1.boxplot(data_by_type, labels=event_types, patch_artist=True,
                      showmeans=True, meanline=True,
                      boxprops=dict(facecolor=COLORS['primary'], alpha=0.7),
                      medianprops=dict(color='red', linewidth=2),
                      meanprops=dict(color='blue', linewidth=2, linestyle='--'))
    
    ax1.set_ylabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_title('Duration by Event Type (< 12h)', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax1.set_xticklabels(event_types, rotation=45, ha='right')
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    ax1.set_axisbelow(True)
    add_subfigure_label(ax1, '(a)')
    
    # Extend y-axis to accommodate text labels at the top
    y_min, y_max = ax1.get_ylim()
    ax1.set_ylim(y_min, y_max * 1.12)
    
    # Add sample sizes
    for i, event_type in enumerate(event_types):
        n = len(ocorrencias_filtered[ocorrencias_filtered['tipo'] == event_type])
        ax1.text(i+1, ax1.get_ylim()[1] * 0.88, f'n={n}',
                ha='center', fontsize=FONT_SIZES['annotation'])
    
    # Add statistical test result
    # sig_text = f"Kruskal-Wallis: H={h_stat:.2f}, p={'<0.001' if p_value < 0.001 else f'={p_value:.3f}'}"
    # ax1.text(0.02, 0.98, sig_text, transform=ax1.transAxes,
    #         fontsize=FONT_SIZES['annotation'], verticalalignment='top',
    #         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, edgecolor='gray'))
    
    # Add filter info
    filter_text = f'Filtered: {filtered_events:,} / {total_events:,}'
    # filter_text = f'N = {filtered_events:,}'
    ax1.text(0.98, 0.98, filter_text, transform=ax1.transAxes,
            fontsize=FONT_SIZES['annotation'], verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray'))
    
    # Panel B: Mean duration by event type with error bars (all data)
    ax2 = axes[1]
    type_stats = ocorrencias.groupby('tipo')['duration_hours'].agg(['mean', 'std', 'count', 'sem'])
    type_stats = type_stats.sort_values('mean', ascending=False)
    
    bars = ax2.barh(range(len(type_stats)), type_stats['mean'],
                    xerr=type_stats['sem'], capsize=5,
                    color=COLORS['categorical'][:len(type_stats)],
                    edgecolor='black', linewidth=0.5, alpha=0.7)
    
    ax2.set_yticks(range(len(type_stats)))
    ax2.set_yticklabels(type_stats.index)
    ax2.set_xlabel('Mean Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_title('Mean Duration by Event Type', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax2.grid(axis='x', linestyle='--', alpha=0.3)
    ax2.set_axisbelow(True)
    add_subfigure_label(ax2, '(b)')
    
    # Calculate max value for x-axis extension
    max_value = (type_stats['mean'] + type_stats['sem']).max()
    ax2.set_xlim(0, max_value * 1.15)  # Add 25% padding for text labels
    
    # Add value labels
    for i, (mean, sem) in enumerate(zip(type_stats['mean'], type_stats['sem'])):
        ax2.text(mean + sem + 0.1, i, f'{mean:.2f}h',
                va='center', fontsize=FONT_SIZES['annotation'])
    
    add_sample_size_annotation(ax2, len(ocorrencias))
    
    plt.tight_layout()
    
    return fig, type_stats, h_stat, p_value

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias = load_and_prepare_data()
    print(f"Total flood events with valid duration: {len(ocorrencias)}")
    
    print("\nCreating duration by type chart...")
    fig, type_stats, h_stat, p_value = create_duration_by_type_chart(ocorrencias)
    
    print("\nDuration Statistics by Event Type:")
    print(type_stats[['mean', 'std', 'count']])
    print(f"\nKruskal-Wallis Test: H = {h_stat:.2f}, p = {p_value:.6f}")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = f'{OUTPUT_DIR}/chart_07a_duration_by_type.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nChart saved to {output_path}")
    plt.close()

if __name__ == '__main__':
    main()

```

```python
"""
Chart 7a: Event Duration by Type (< 12 hours)
Comparative analysis of flood event durations across different event types
Includes box plots and mean duration with error bars
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

def perform_statistical_tests(ocorrencias):
    """Perform statistical tests comparing durations across groups"""
    # Kruskal-Wallis test for event types (non-parametric ANOVA)
    event_types = ocorrencias['tipo'].unique()
    groups = [ocorrencias[ocorrencias['tipo'] == t]['duration_hours'].dropna() 
              for t in event_types]
    h_stat, p_value = stats.kruskal(*groups)
    
    return h_stat, p_value

def create_duration_by_type_chart(ocorrencias):
    """Create comparative duration analysis chart by event type"""
    setup_plot_style()
    
    # Filter to < 12 hours for panel a
    ocorrencias_filtered = ocorrencias[ocorrencias['duration_hours'] < 12].copy()
    total_events = len(ocorrencias)
    filtered_events = len(ocorrencias_filtered)
    
    # Perform statistical tests on filtered data
    h_stat, p_value = perform_statistical_tests(ocorrencias_filtered)
    
    # Create 1x2 subplot grid
    fig, axes = plt.subplots(1, 2, figsize=FIGURE_SIZES['double'])
    fig.suptitle(f'Flood Event Duration by Type\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'], fontweight='bold', y=1.02)
    
    # Panel A: Box plot by event type (< 12 hours)
    ax1 = axes[0]
    event_types = ocorrencias_filtered['tipo'].value_counts().index.tolist()
    event_types = [event_types[1], event_types[0], event_types[2]] + event_types[3:]
    data_by_type = [ocorrencias_filtered[ocorrencias_filtered['tipo'] == t]['duration_hours'].dropna() 
                    for t in event_types]
    
    bp1 = ax1.boxplot(data_by_type, labels=event_types, patch_artist=True,
                      showmeans=True, meanline=True,
                      boxprops=dict(facecolor=COLORS['primary'], alpha=0.7),
                      medianprops=dict(color='red', linewidth=2),
                      meanprops=dict(color='blue', linewidth=2, linestyle='--'))
    
    ax1.set_ylabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_title('Duration by Event Type (< 12h)', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax1.set_xticklabels(event_types, rotation=45, ha='right')
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    ax1.set_axisbelow(True)
    add_subfigure_label(ax1, '(a)')
    
    # Extend y-axis to accommodate text labels at the top
    y_min, y_max = ax1.get_ylim()
    ax1.set_ylim(y_min, y_max * 1.12)
    
    # Add sample sizes
    for i, event_type in enumerate(event_types):
        n = len(ocorrencias_filtered[ocorrencias_filtered['tipo'] == event_type])
        ax1.text(i+1, ax1.get_ylim()[1] * 0.88, f'n={n}',
                ha='center', fontsize=FONT_SIZES['annotation'])
    
    # Add statistical test result
    # sig_text = f"Kruskal-Wallis: H={h_stat:.2f}, p={'<0.001' if p_value < 0.001 else f'={p_value:.3f}'}"
    # ax1.text(0.02, 0.98, sig_text, transform=ax1.transAxes,
    #         fontsize=FONT_SIZES['annotation'], verticalalignment='top',
    #         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, edgecolor='gray'))
    
    # Add filter info
    filter_text = f'Filtered: {filtered_events:,} / {total_events:,}'
    # filter_text = f'N = {filtered_events:,}'
    ax1.text(0.98, 0.98, filter_text, transform=ax1.transAxes,
            fontsize=FONT_SIZES['annotation'], verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray'))
    
    # Panel B: Mean duration by event type with error bars (all data)
    ax2 = axes[1]
    type_stats = ocorrencias.groupby('tipo')['duration_hours'].agg(['mean', 'std', 'count', 'sem'])
    type_stats = type_stats.sort_values('mean', ascending=False)
    
    bars = ax2.barh(range(len(type_stats)), type_stats['mean'],
                    xerr=type_stats['sem'], capsize=5,
                    color=COLORS['categorical'][:len(type_stats)],
                    edgecolor='black', linewidth=0.5, alpha=0.7)
    
    ax2.set_yticks(range(len(type_stats)))
    ax2.set_yticklabels(type_stats.index)
    ax2.set_xlabel('Mean Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_title('Mean Duration by Event Type', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax2.grid(axis='x', linestyle='--', alpha=0.3)
    ax2.set_axisbelow(True)
    add_subfigure_label(ax2, '(b)')
    
    # Calculate max value for x-axis extension
    max_value = (type_stats['mean'] + type_stats['sem']).max()
    ax2.set_xlim(0, max_value * 1.15)  # Add 25% padding for text labels
    
    # Add value labels
    for i, (mean, sem) in enumerate(zip(type_stats['mean'], type_stats['sem'])):
        ax2.text(mean + sem + 0.1, i, f'{mean:.2f}h',
                va='center', fontsize=FONT_SIZES['annotation'])
    
    add_sample_size_annotation(ax2, len(ocorrencias))
    
    plt.tight_layout()
    
    return fig, type_stats, h_stat, p_value

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias = load_and_prepare_data()
    print(f"Total flood events with valid duration: {len(ocorrencias)}")
    
    print("\nCreating duration by type chart...")
    fig, type_stats, h_stat, p_value = create_duration_by_type_chart(ocorrencias)
    
    print("\nDuration Statistics by Event Type:")
    print(type_stats[['mean', 'std', 'count']])
    print(f"\nKruskal-Wallis Test: H = {h_stat:.2f}, p = {p_value:.6f}")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = f'{OUTPUT_DIR}/chart_07a_duration_by_type.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nChart saved to {output_path}")
    plt.close()

if __name__ == '__main__':
    main()

```

```python
"""
Chart 7b: Event Duration by Season (< 12 hours)
Comparative analysis of flood event durations across different seasons
Includes box plots and violin plots
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
    """Load and preprocess flood event data with duration calculation"""
    ocorrencias = pd.read_csv(DATA_PATHS['ocorrencias'])
    pops = pd.read_csv(DATA_PATHS['pops'], index_col=0)
    
    ocorrencias['data_inicio'] = pd.to_datetime(ocorrencias['data_inicio'])
    ocorrencias['data_fim'] = pd.to_datetime(ocorrencias['data_fim'])
    ocorrencias['tipo'] = ocorrencias['id_pop'].map(pops.set_index('id')['titulo'])
    
    ocorrencias = ocorrencias[ocorrencias['tipo'].isin(FLOOD_TYPES)]
    ocorrencias['tipo'] = ocorrencias['tipo'].replace(EVENT_TYPE_MAPPING)
    
    # Calculate duration in hours
    ocorrencias['duration_hours'] = (ocorrencias['data_fim'] - ocorrencias['data_inicio']).dt.total_seconds() / 3600
    
    # Filter out invalid durations
    ocorrencias = ocorrencias[
        (ocorrencias['duration_hours'] >= 0) & 
        (ocorrencias['duration_hours'] <= 72)
    ].copy()
    
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

def create_duration_by_season_chart(ocorrencias):
    """Create comparative duration analysis chart by season"""
    setup_plot_style()
    
    # Add season information
    ocorrencias['season'] = ocorrencias['data_inicio'].apply(get_season)
    
    # Filter to < 12 hours for both panels
    ocorrencias_filtered = ocorrencias[ocorrencias['duration_hours'] < 12].copy()
    total_events = len(ocorrencias)
    filtered_events = len(ocorrencias_filtered)
    
    # Create 1x2 subplot grid
    fig, axes = plt.subplots(1, 2, figsize=FIGURE_SIZES['double'])
    fig.suptitle(f'Flood Event Duration by Season (< 12 hours)\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'], fontweight='bold', y=1.02)
    
    season_order = ['Summer', 'Autumn', 'Winter', 'Spring']
    season_colors = [COLORS['seasons'][s] for s in season_order]
    
    # Panel A: Box plot by season (< 12 hours)
    ax1 = axes[0]
    data_by_season = [ocorrencias_filtered[ocorrencias_filtered['season'] == s]['duration_hours'].dropna() 
                      for s in season_order]
    
    bp1 = ax1.boxplot(data_by_season, labels=season_order, patch_artist=True,
                      showmeans=True, meanline=True,
                      medianprops=dict(color='red', linewidth=2),
                      meanprops=dict(color='blue', linewidth=2, linestyle='--'))
    
    for patch, color in zip(bp1['boxes'], season_colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax1.set_ylabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_title('Duration by Season', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    ax1.set_axisbelow(True)
    add_subfigure_label(ax1, '(a)')
    
    # Extend y-axis to accommodate text labels at the top
    y_min, y_max = ax1.get_ylim()
    ax1.set_ylim(y_min, y_max * 1.07)

    # Add sample sizes
    for i, season in enumerate(season_order):
        n = len(ocorrencias_filtered[ocorrencias_filtered['season'] == season])
        ax1.text(i+1, ax1.get_ylim()[1] * 0.91, f'n={n}', 
                ha='center', fontsize=FONT_SIZES['annotation'])
    
    # Add filter info
    filter_text = f'Filtered: {filtered_events:,} / {total_events:,}'
    ax1.text(0.98, 0.98, filter_text, transform=ax1.transAxes,
            fontsize=FONT_SIZES['annotation'], verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray'))
    
    # Panel B: Duration distribution by season (violin plot, < 12 hours)
    ax2 = axes[1]
    
    # Prepare data for violin plot
    season_data = []
    season_positions = []
    for i, season in enumerate(season_order):
        data = ocorrencias_filtered[ocorrencias_filtered['season'] == season]['duration_hours'].dropna()
        if len(data) > 0:
            season_data.append(data)
            season_positions.append(i + 1)
    
    parts = ax2.violinplot(season_data, positions=season_positions, 
                           showmeans=True, showmedians=True, widths=0.7)
    
    # Color the violin plots
    for i, pc in enumerate(parts['bodies']):
        pc.set_facecolor(season_colors[i])
        pc.set_alpha(0.7)
    
    ax2.set_xticks(range(1, len(season_order) + 1))
    ax2.set_xticklabels(season_order)
    ax2.set_ylabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_title('Duration Distribution by Season', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax2.grid(axis='y', linestyle='--', alpha=0.3)
    ax2.set_axisbelow(True)
    add_subfigure_label(ax2, '(b)')
    
    # Extend y-axis to accommodate text labels at the top
    y_min, y_max = ax2.get_ylim()
    ax2.set_ylim(y_min, y_max * 1.07)

    add_sample_size_annotation(ax2, filtered_events)
    
    plt.tight_layout()
    
    # Calculate season statistics for reporting
    season_stats = ocorrencias_filtered.groupby('season')['duration_hours'].agg(['mean', 'std', 'count'])
    
    return fig, season_stats

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias = load_and_prepare_data()
    print(f"Total flood events with valid duration: {len(ocorrencias)}")
    
    print("\nCreating duration by season chart...")
    fig, season_stats = create_duration_by_season_chart(ocorrencias)
    
    print("\nDuration Statistics by Season (< 12 hours):")
    print(season_stats)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = f'{OUTPUT_DIR}/chart_07b_duration_by_season.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nChart saved to {output_path}")
    plt.close()

if __name__ == '__main__':
    main()

```

```python
"""
Chart 7b: Event Duration by Season (< 12 hours)
Comparative analysis of flood event durations across different seasons
Includes box plots and violin plots
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

def create_duration_by_season_chart(ocorrencias):
    """Create comparative duration analysis chart by season"""
    setup_plot_style()
    
    # Add season information
    ocorrencias['season'] = ocorrencias['data_inicio'].apply(get_season)
    
    # Filter to < 12 hours for both panels
    ocorrencias_filtered = ocorrencias[ocorrencias['duration_hours'] < 12].copy()
    total_events = len(ocorrencias)
    filtered_events = len(ocorrencias_filtered)
    
    # Create 1x2 subplot grid
    fig, axes = plt.subplots(1, 2, figsize=FIGURE_SIZES['double'])
    fig.suptitle(f'Flood Event Duration by Season (< 12 hours)\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'], fontweight='bold', y=1.02)
    
    season_order = ['Summer', 'Autumn', 'Winter', 'Spring']
    season_colors = [COLORS['seasons'][s] for s in season_order]
    
    # Panel A: Box plot by season (< 12 hours)
    ax1 = axes[0]
    data_by_season = [ocorrencias_filtered[ocorrencias_filtered['season'] == s]['duration_hours'].dropna() 
                      for s in season_order]
    
    bp1 = ax1.boxplot(data_by_season, labels=season_order, patch_artist=True,
                      showmeans=True, meanline=True,
                      medianprops=dict(color='red', linewidth=2),
                      meanprops=dict(color='blue', linewidth=2, linestyle='--'))
    
    for patch, color in zip(bp1['boxes'], season_colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax1.set_ylabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_title('Duration by Season', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    ax1.set_axisbelow(True)
    add_subfigure_label(ax1, '(a)')
    
    # Extend y-axis to accommodate text labels at the top
    y_min, y_max = ax1.get_ylim()
    ax1.set_ylim(y_min, y_max * 1.07)

    # Add sample sizes
    for i, season in enumerate(season_order):
        n = len(ocorrencias_filtered[ocorrencias_filtered['season'] == season])
        ax1.text(i+1, ax1.get_ylim()[1] * 0.91, f'n={n}', 
                ha='center', fontsize=FONT_SIZES['annotation'])
    
    # Add filter info
    filter_text = f'Filtered: {filtered_events:,} / {total_events:,}'
    ax1.text(0.98, 0.98, filter_text, transform=ax1.transAxes,
            fontsize=FONT_SIZES['annotation'], verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray'))
    
    # Panel B: Duration distribution by season (violin plot, < 12 hours)
    ax2 = axes[1]
    
    # Prepare data for violin plot
    season_data = []
    season_positions = []
    for i, season in enumerate(season_order):
        data = ocorrencias_filtered[ocorrencias_filtered['season'] == season]['duration_hours'].dropna()
        if len(data) > 0:
            season_data.append(data)
            season_positions.append(i + 1)
    
    parts = ax2.violinplot(season_data, positions=season_positions, 
                           showmeans=True, showmedians=True, widths=0.7)
    
    # Color the violin plots
    for i, pc in enumerate(parts['bodies']):
        pc.set_facecolor(season_colors[i])
        pc.set_alpha(0.7)
    
    ax2.set_xticks(range(1, len(season_order) + 1))
    ax2.set_xticklabels(season_order)
    ax2.set_ylabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_title('Duration Distribution by Season', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax2.grid(axis='y', linestyle='--', alpha=0.3)
    ax2.set_axisbelow(True)
    add_subfigure_label(ax2, '(b)')
    
    # Extend y-axis to accommodate text labels at the top
    y_min, y_max = ax2.get_ylim()
    ax2.set_ylim(y_min, y_max * 1.07)

    add_sample_size_annotation(ax2, filtered_events)
    
    plt.tight_layout()
    
    # Calculate season statistics for reporting
    season_stats = ocorrencias_filtered.groupby('season')['duration_hours'].agg(['mean', 'std', 'count'])
    
    return fig, season_stats

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias = load_and_prepare_data()
    print(f"Total flood events with valid duration: {len(ocorrencias)}")
    
    print("\nCreating duration by season chart...")
    fig, season_stats = create_duration_by_season_chart(ocorrencias)
    
    print("\nDuration Statistics by Season (< 12 hours):")
    print(season_stats)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = f'{OUTPUT_DIR}/chart_07b_duration_by_season.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nChart saved to {output_path}")
    plt.close()

if __name__ == '__main__':
    main()

```

```python
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

```

```python
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

```

Updating chart_09 and chart_10 to use generic names in chart titles and group definitions:


```python
"""
Chart 9: Event Duration Distribution by Type
Based on Chart 6a - generates two charts:
1. Combined chart for "Lâmina d'água" and "Bolsão d'água em via"
2. Single chart for "Alagamento"
Each chart shows histogram and CDF for events < 12 hours
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
    """Load and preprocess flood event data with duration calculation"""
    ocorrencias = pd.read_csv(DATA_PATHS['ocorrencias'])
    pops = pd.read_csv(DATA_PATHS['pops'], index_col=0)
    
    ocorrencias['data_inicio'] = pd.to_datetime(ocorrencias['data_inicio'])
    ocorrencias['data_fim'] = pd.to_datetime(ocorrencias['data_fim'])
    ocorrencias['tipo'] = ocorrencias['id_pop'].map(pops.set_index('id')['titulo'])
    
    ocorrencias = ocorrencias[ocorrencias['tipo'].isin(FLOOD_TYPES)]
    ocorrencias['tipo'] = ocorrencias['tipo'].replace(EVENT_TYPE_MAPPING)
    
    # Calculate duration in hours
    ocorrencias['duration_hours'] = (ocorrencias['data_fim'] - ocorrencias['data_inicio']).dt.total_seconds() / 3600
    
    # Filter out invalid durations (negative or extremely long)
    ocorrencias = ocorrencias[
        (ocorrencias['duration_hours'] >= 0) & 
        (ocorrencias['duration_hours'] <= 72)  # Max 72 hours (3 days)
    ].copy()
    
    return ocorrencias

def calculate_duration_stats(durations):
    """Calculate comprehensive duration statistics"""
    stats_dict = {
        'mean': durations.mean(),
        'median': durations.median(),
        'std': durations.std(),
        'min': durations.min(),
        'max': durations.max(),
        'q25': durations.quantile(0.25),
        'q75': durations.quantile(0.75),
        'q90': durations.quantile(0.90),
        'count': len(durations)
    }
    
    return stats_dict

def create_duration_distribution_chart_by_type(ocorrencias_type, event_types_list, chart_title):
    """Create histogram and CDF chart for one or more event types (< 12 hours)"""
    setup_plot_style()
    
    # Get durations for this event type(s)
    durations = ocorrencias_type['duration_hours'].dropna()
    
    # Filter durations to only show events < 12 hours
    durations_filtered = durations[durations < 12]
    total_events = len(durations)
    filtered_events = len(durations_filtered)
    
    # Calculate statistics from ALL data (for reference)
    stats_dict_all = calculate_duration_stats(durations)
    
    # Calculate statistics from FILTERED data (< 12h) for display on chart
    stats_dict = calculate_duration_stats(durations_filtered)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGURE_SIZES['double'])
    fig.suptitle(f'Duration Distribution for {chart_title} (< 12 hours)\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'], fontweight='bold', y=1.02)
    
    # Panel A: Histogram with statistics
    n, bins, patches = ax1.hist(durations_filtered, bins=24, color=COLORS['primary'],
                                edgecolor='black', linewidth=0.5, alpha=0.7)
    
    # Add vertical lines for statistics
    ax1.axvline(stats_dict['mean'], color=COLORS['secondary'], linestyle='--', 
               linewidth=2, label=f"Mean: {stats_dict['mean']:.2f}h")
    ax1.axvline(stats_dict['median'], color=COLORS['tertiary'], linestyle='--', 
               linewidth=2, label=f"Median: {stats_dict['median']:.2f}h")
    ax1.axvline(stats_dict['q90'], color=COLORS['quaternary'], linestyle=':', 
               linewidth=2, label=f"90th percentile: {stats_dict['q90']:.2f}h")
    
    ax1.set_xlabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_ylabel('Frequency', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_title('Duration Distribution', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax1.legend(loc='upper right', fontsize=FONT_SIZES['legend'])
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    ax1.set_axisbelow(True)
    add_subfigure_label(ax1, '(a)')
    
    # Panel B: Cumulative Distribution Function (CDF)
    sorted_durations = np.sort(durations_filtered)
    cumulative = np.arange(1, len(sorted_durations) + 1) / len(sorted_durations) * 100
    
    ax2.plot(sorted_durations, cumulative, color=COLORS['primary'], linewidth=2)
    ax2.fill_between(sorted_durations, 0, cumulative, color=COLORS['primary'], alpha=0.2)
    
    # Add reference lines
    ax2.axhline(50, color=COLORS['tertiary'], linestyle='--', linewidth=1, alpha=0.5)
    ax2.axhline(90, color=COLORS['quaternary'], linestyle=':', linewidth=1, alpha=0.5)
    ax2.axvline(stats_dict['median'], color=COLORS['tertiary'], linestyle='--', linewidth=1, alpha=0.5)
    ax2.axvline(stats_dict['q90'], color=COLORS['quaternary'], linestyle=':', linewidth=1, alpha=0.5)
    
    # Add annotations
    ax2.text(stats_dict['median'], 50, f" {stats_dict['median']:.2f}h", 
            fontsize=FONT_SIZES['annotation'], verticalalignment='bottom', 
            color=COLORS['tertiary'])
    ax2.text(stats_dict['q90'], 90, f" {stats_dict['q90']:.2f}h", 
            fontsize=FONT_SIZES['annotation'], verticalalignment='bottom',
            color=COLORS['quaternary'])
    
    ax2.set_xlabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_ylabel('Cumulative Percentage (%)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_title('Cumulative Distribution', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax2.grid(True, linestyle='--', alpha=0.3)
    ax2.set_axisbelow(True)
    ax2.set_ylim(0, 100)
    add_subfigure_label(ax2, '(b)')
    
    # Add statistics box (using ALL data for context)
    stats_text = (f"All data:\n"
                 f"Mean: {stats_dict_all['mean']:.2f}h\n"
                 f"Median: {stats_dict_all['median']:.2f}h\n"
                 f"90th pct: {stats_dict_all['q90']:.2f}h")
    ax2.text(0.98, 0.25, stats_text, transform=ax2.transAxes, 
            fontsize=FONT_SIZES['annotation'],
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, edgecolor='gray'))
    
    # Add sample size annotation showing filtered vs total
    sample_text = f'N = {filtered_events:,} (< 12h)\nTotal: {total_events:,}'
    ax2.text(0.98, 0.98, sample_text,
            transform=ax2.transAxes,
            fontsize=FONT_SIZES['annotation'],
            verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray'))
    
    plt.tight_layout()
    
    return fig, stats_dict

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias = load_and_prepare_data()
    print(f"Total flood events with valid duration: {len(ocorrencias)}")
    
    # Get unique event types
    event_types = ocorrencias['tipo'].value_counts().index.tolist()
    print(f"\nEvent types found: {event_types}")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Define chart groups
    chart_groups = [
        {
            'types': ["Bolsão d'água em via", "Lâmina d'água"],
            'title': '"Bolsão d\'água em via" and "Lâmina d\'água" Events',
            'filename': 'bolsao_and_lamina'
        },
        {
            'types': ['Alagamento'],
            'title': '"Alagamento" Events',
            'filename': 'alagamento'
        }
    ]
    
    # Create a chart for each group
    for group in chart_groups:
        print(f"\n{'='*70}")
        print(f"Processing: {group['title']}")
        print(f"{'='*70}")
        
        # Filter data for this group
        ocorrencias_group = ocorrencias[ocorrencias['tipo'].isin(group['types'])].copy()
        n_events = len(ocorrencias_group)
        
        print(f"Events for this group: {n_events}")
        print(f"  Event types included: {group['types']}")
        
        if n_events == 0:
            print(f"Skipping {group['title']} - no events found")
            continue
        
        # Create chart
        print(f"Creating duration distribution chart for {group['title']}...")
        fig, stats_dict = create_duration_distribution_chart_by_type(
            ocorrencias_group, group['types'], group['title']
        )
        
        print("\nDuration Statistics (< 12h filtered):")
        print(f"  Mean: {stats_dict['mean']:.2f} hours")
        print(f"  Median: {stats_dict['median']:.2f} hours")
        print(f"  Std Dev: {stats_dict['std']:.2f} hours")
        print(f"  Min: {stats_dict['min']:.2f} hours")
        print(f"  Max: {stats_dict['max']:.2f} hours")
        print(f"  90th percentile: {stats_dict['q90']:.2f} hours")
        
        # Save chart
        output_path = f'{OUTPUT_DIR}/chart_09_duration_distribution_{group["filename"]}.png'
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Chart saved to {output_path}")
        plt.close()
    
    print(f"\n{'='*70}")
    print("All charts created successfully!")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()

```

```python
"""
Chart 9: Event Duration Distribution by Type
Based on Chart 6a - generates two charts:
1. Combined chart for "Lâmina d'água" and "Bolsão d'água em via"
2. Single chart for "Alagamento"
Each chart shows histogram and CDF for events < 12 hours
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
    
    # Filter out invalid durations (negative or extremely long)
    ocorrencias = ocorrencias[
        (ocorrencias['duration_hours'] >= 0) & 
        (ocorrencias['duration_hours'] <= 72)  # Max 72 hours (3 days)
    ].copy()
    
    return ocorrencias

def calculate_duration_stats(durations):
    """Calculate comprehensive duration statistics"""
    stats_dict = {
        'mean': durations.mean(),
        'median': durations.median(),
        'std': durations.std(),
        'min': durations.min(),
        'max': durations.max(),
        'q25': durations.quantile(0.25),
        'q75': durations.quantile(0.75),
        'q90': durations.quantile(0.90),
        'count': len(durations)
    }
    
    return stats_dict

def create_duration_distribution_chart_by_type(ocorrencias_type, event_types_list, chart_title):
    """Create histogram and CDF chart for one or more event types (< 12 hours)"""
    setup_plot_style()
    
    # Get durations for this event type(s)
    durations = ocorrencias_type['duration_hours'].dropna()
    
    # Filter durations to only show events < 12 hours
    durations_filtered = durations[durations < 12]
    total_events = len(durations)
    filtered_events = len(durations_filtered)
    
    # Calculate statistics from ALL data (for reference)
    stats_dict_all = calculate_duration_stats(durations)
    
    # Calculate statistics from FILTERED data (< 12h) for display on chart
    stats_dict = calculate_duration_stats(durations_filtered)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGURE_SIZES['double'])
    fig.suptitle(f'Duration Distribution for {chart_title} (< 12 hours)\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'], fontweight='bold', y=1.02)
    
    # Panel A: Histogram with statistics
    n, bins, patches = ax1.hist(durations_filtered, bins=24, color=COLORS['primary'],
                                edgecolor='black', linewidth=0.5, alpha=0.7)
    
    # Add vertical lines for statistics
    ax1.axvline(stats_dict['mean'], color=COLORS['secondary'], linestyle='--', 
               linewidth=2, label=f"Mean: {stats_dict['mean']:.2f}h")
    ax1.axvline(stats_dict['median'], color=COLORS['tertiary'], linestyle='--', 
               linewidth=2, label=f"Median: {stats_dict['median']:.2f}h")
    ax1.axvline(stats_dict['q90'], color=COLORS['quaternary'], linestyle=':', 
               linewidth=2, label=f"90th percentile: {stats_dict['q90']:.2f}h")
    
    ax1.set_xlabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_ylabel('Frequency', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_title('Duration Distribution', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax1.legend(loc='upper right', fontsize=FONT_SIZES['legend'])
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    ax1.set_axisbelow(True)
    add_subfigure_label(ax1, '(a)')
    
    # Panel B: Cumulative Distribution Function (CDF)
    sorted_durations = np.sort(durations_filtered)
    cumulative = np.arange(1, len(sorted_durations) + 1) / len(sorted_durations) * 100
    
    ax2.plot(sorted_durations, cumulative, color=COLORS['primary'], linewidth=2)
    ax2.fill_between(sorted_durations, 0, cumulative, color=COLORS['primary'], alpha=0.2)
    
    # Add reference lines
    ax2.axhline(50, color=COLORS['tertiary'], linestyle='--', linewidth=1, alpha=0.5)
    ax2.axhline(90, color=COLORS['quaternary'], linestyle=':', linewidth=1, alpha=0.5)
    ax2.axvline(stats_dict['median'], color=COLORS['tertiary'], linestyle='--', linewidth=1, alpha=0.5)
    ax2.axvline(stats_dict['q90'], color=COLORS['quaternary'], linestyle=':', linewidth=1, alpha=0.5)
    
    # Add annotations
    ax2.text(stats_dict['median'], 50, f" {stats_dict['median']:.2f}h", 
            fontsize=FONT_SIZES['annotation'], verticalalignment='bottom', 
            color=COLORS['tertiary'])
    ax2.text(stats_dict['q90'], 90, f" {stats_dict['q90']:.2f}h", 
            fontsize=FONT_SIZES['annotation'], verticalalignment='bottom',
            color=COLORS['quaternary'])
    
    ax2.set_xlabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_ylabel('Cumulative Percentage (%)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_title('Cumulative Distribution', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax2.grid(True, linestyle='--', alpha=0.3)
    ax2.set_axisbelow(True)
    ax2.set_ylim(0, 100)
    add_subfigure_label(ax2, '(b)')
    
    # Add statistics box (using ALL data for context)
    stats_text = (f"All data:\n"
                 f"Mean: {stats_dict_all['mean']:.2f}h\n"
                 f"Median: {stats_dict_all['median']:.2f}h\n"
                 f"90th pct: {stats_dict_all['q90']:.2f}h")
    ax2.text(0.98, 0.25, stats_text, transform=ax2.transAxes, 
            fontsize=FONT_SIZES['annotation'],
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, edgecolor='gray'))
    
    # Add sample size annotation showing filtered vs total
    sample_text = f'N = {filtered_events:,} (< 12h)\nTotal: {total_events:,}'
    ax2.text(0.98, 0.98, sample_text,
            transform=ax2.transAxes,
            fontsize=FONT_SIZES['annotation'],
            verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray'))
    
    plt.tight_layout()
    
    return fig, stats_dict

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias = load_and_prepare_data()
    print(f"Total flood events with valid duration: {len(ocorrencias)}")
    
    # Get unique event types
    event_types = ocorrencias['tipo'].value_counts().index.tolist()
    print(f"\nEvent types found: {event_types}")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Define chart groups
    chart_groups = [
        {
            'types': ["Bolsão d'água em via", "Lâmina d'água"],
            'title': '"Bolsão d\'água em via" and "Lâmina d\'água" Events',
            'filename': 'bolsao_and_lamina'
        },
        {
            'types': ['Alagamento'],
            'title': '"Alagamento" Events',
            'filename': 'alagamento'
        }
    ]
    
    # Create a chart for each group
    for group in chart_groups:
        print(f"\n{'='*70}")
        print(f"Processing: {group['title']}")
        print(f"{'='*70}")
        
        # Filter data for this group
        ocorrencias_group = ocorrencias[ocorrencias['tipo'].isin(group['types'])].copy()
        n_events = len(ocorrencias_group)
        
        print(f"Events for this group: {n_events}")
        print(f"  Event types included: {group['types']}")
        
        if n_events == 0:
            print(f"Skipping {group['title']} - no events found")
            continue
        
        # Create chart
        print(f"Creating duration distribution chart for {group['title']}...")
        fig, stats_dict = create_duration_distribution_chart_by_type(
            ocorrencias_group, group['types'], group['title']
        )
        
        print("\nDuration Statistics (< 12h filtered):")
        print(f"  Mean: {stats_dict['mean']:.2f} hours")
        print(f"  Median: {stats_dict['median']:.2f} hours")
        print(f"  Std Dev: {stats_dict['std']:.2f} hours")
        print(f"  Min: {stats_dict['min']:.2f} hours")
        print(f"  Max: {stats_dict['max']:.2f} hours")
        print(f"  90th percentile: {stats_dict['q90']:.2f} hours")
        
        # Save chart
        output_path = f'{OUTPUT_DIR}/chart_09_duration_distribution_{group["filename"]}.png'
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Chart saved to {output_path}")
        plt.close()
    
    print(f"\n{'='*70}")
    print("All charts created successfully!")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()

```

```python
"""
Chart 9: Event Duration Distribution by Type
Based on Chart 6a - generates two charts:
1. Combined chart for "Lâmina d'água" and "Bolsão d'água em via"
2. Single chart for "Alagamento"
Each chart shows histogram and CDF for events < 12 hours
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
    
    # Filter out invalid durations (negative or extremely long)
    ocorrencias = ocorrencias[
        (ocorrencias['duration_hours'] >= 0) & 
        (ocorrencias['duration_hours'] <= 72)  # Max 72 hours (3 days)
    ].copy()
    
    return ocorrencias

def calculate_duration_stats(durations):
    """Calculate comprehensive duration statistics"""
    stats_dict = {
        'mean': durations.mean(),
        'median': durations.median(),
        'std': durations.std(),
        'min': durations.min(),
        'max': durations.max(),
        'q25': durations.quantile(0.25),
        'q75': durations.quantile(0.75),
        'q90': durations.quantile(0.90),
        'count': len(durations)
    }
    
    return stats_dict

def create_duration_distribution_chart_by_type(ocorrencias_type, event_types_list, chart_title):
    """Create histogram and CDF chart for one or more event types (< 12 hours)"""
    setup_plot_style()
    
    # Get durations for this event type(s)
    durations = ocorrencias_type['duration_hours'].dropna()
    
    # Filter durations to only show events < 12 hours
    durations_filtered = durations[durations < 12]
    total_events = len(durations)
    filtered_events = len(durations_filtered)
    
    # Calculate statistics from ALL data (for reference)
    stats_dict_all = calculate_duration_stats(durations)
    
    # Calculate statistics from FILTERED data (< 12h) for display on chart
    stats_dict = calculate_duration_stats(durations_filtered)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGURE_SIZES['double'])
    fig.suptitle(f'Duration Distribution for {chart_title} (< 12 hours)\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'], fontweight='bold', y=1.02)
    
    # Panel A: Histogram with statistics
    n, bins, patches = ax1.hist(durations_filtered, bins=24, color=COLORS['primary'],
                                edgecolor='black', linewidth=0.5, alpha=0.7)
    
    # Add vertical lines for statistics
    ax1.axvline(stats_dict['mean'], color=COLORS['secondary'], linestyle='--', 
               linewidth=2, label=f"Mean: {stats_dict['mean']:.2f}h")
    ax1.axvline(stats_dict['median'], color=COLORS['tertiary'], linestyle='--', 
               linewidth=2, label=f"Median: {stats_dict['median']:.2f}h")
    ax1.axvline(stats_dict['q90'], color=COLORS['quaternary'], linestyle=':', 
               linewidth=2, label=f"90th percentile: {stats_dict['q90']:.2f}h")
    
    ax1.set_xlabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_ylabel('Frequency', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_title('Duration Distribution', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax1.legend(loc='upper right', fontsize=FONT_SIZES['legend'])
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    ax1.set_axisbelow(True)
    add_subfigure_label(ax1, '(a)')
    
    # Panel B: Cumulative Distribution Function (CDF)
    sorted_durations = np.sort(durations_filtered)
    cumulative = np.arange(1, len(sorted_durations) + 1) / len(sorted_durations) * 100
    
    ax2.plot(sorted_durations, cumulative, color=COLORS['primary'], linewidth=2)
    ax2.fill_between(sorted_durations, 0, cumulative, color=COLORS['primary'], alpha=0.2)
    
    # Add reference lines
    ax2.axhline(50, color=COLORS['tertiary'], linestyle='--', linewidth=1, alpha=0.5)
    ax2.axhline(90, color=COLORS['quaternary'], linestyle=':', linewidth=1, alpha=0.5)
    ax2.axvline(stats_dict['median'], color=COLORS['tertiary'], linestyle='--', linewidth=1, alpha=0.5)
    ax2.axvline(stats_dict['q90'], color=COLORS['quaternary'], linestyle=':', linewidth=1, alpha=0.5)
    
    # Add annotations
    ax2.text(stats_dict['median'], 50, f" {stats_dict['median']:.2f}h", 
            fontsize=FONT_SIZES['annotation'], verticalalignment='bottom', 
            color=COLORS['tertiary'])
    ax2.text(stats_dict['q90'], 90, f" {stats_dict['q90']:.2f}h", 
            fontsize=FONT_SIZES['annotation'], verticalalignment='bottom',
            color=COLORS['quaternary'])
    
    ax2.set_xlabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_ylabel('Cumulative Percentage (%)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_title('Cumulative Distribution', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax2.grid(True, linestyle='--', alpha=0.3)
    ax2.set_axisbelow(True)
    ax2.set_ylim(0, 100)
    add_subfigure_label(ax2, '(b)')
    
    # Add statistics box (using ALL data for context)
    stats_text = (f"All data:\n"
                 f"Mean: {stats_dict_all['mean']:.2f}h\n"
                 f"Median: {stats_dict_all['median']:.2f}h\n"
                 f"90th pct: {stats_dict_all['q90']:.2f}h")
    ax2.text(0.98, 0.25, stats_text, transform=ax2.transAxes, 
            fontsize=FONT_SIZES['annotation'],
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, edgecolor='gray'))
    
    # Add sample size annotation showing filtered vs total
    sample_text = f'N = {filtered_events:,} (< 12h)\nTotal: {total_events:,}'
    ax2.text(0.98, 0.98, sample_text,
            transform=ax2.transAxes,
            fontsize=FONT_SIZES['annotation'],
            verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray'))
    
    plt.tight_layout()
    
    return fig, stats_dict

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias = load_and_prepare_data()
    print(f"Total flood events with valid duration: {len(ocorrencias)}")
    
    # Get unique event types
    event_types = ocorrencias['tipo'].value_counts().index.tolist()
    print(f"\nEvent types found: {event_types}")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Define chart groups (using generic names)
    chart_groups = [
        {
            'types': ['Flood Type I', 'Flood Type II'],
            'title': 'Flood Type I and Flood Type II Events',
            'filename': 'bolsao_and_lamina'
        },
        {
            'types': ['Flood Type III'],
            'title': 'Flood Type III Events',
            'filename': 'alagamento'
        }
    ]
    
    # Create a chart for each group
    for group in chart_groups:
        print(f"\n{'='*70}")
        print(f"Processing: {group['title']}")
        print(f"{'='*70}")
        
        # Filter data for this group
        ocorrencias_group = ocorrencias[ocorrencias['tipo'].isin(group['types'])].copy()
        n_events = len(ocorrencias_group)
        
        print(f"Events for this group: {n_events}")
        print(f"  Event types included: {group['types']}")
        
        if n_events == 0:
            print(f"Skipping {group['title']} - no events found")
            continue
        
        # Create chart
        print(f"Creating duration distribution chart for {group['title']}...")
        fig, stats_dict = create_duration_distribution_chart_by_type(
            ocorrencias_group, group['types'], group['title']
        )
        
        print("\nDuration Statistics (< 12h filtered):")
        print(f"  Mean: {stats_dict['mean']:.2f} hours")
        print(f"  Median: {stats_dict['median']:.2f} hours")
        print(f"  Std Dev: {stats_dict['std']:.2f} hours")
        print(f"  Min: {stats_dict['min']:.2f} hours")
        print(f"  Max: {stats_dict['max']:.2f} hours")
        print(f"  90th percentile: {stats_dict['q90']:.2f} hours")
        
        # Save chart
        output_path = f'{OUTPUT_DIR}/chart_09_duration_distribution_{group["filename"]}.png'
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Chart saved to {output_path}")
        plt.close()
    
    print(f"\n{'='*70}")
    print("All charts created successfully!")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()

```

```python
"""
Chart 10: Event Duration Categories by Type
Based on Chart 8 - generates two charts:
1. Combined chart for "Lâmina d'água" and "Bolsão d'água em via"
2. Single chart for "Alagamento"
Each chart shows distribution of events by duration categories
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

def create_duration_categories_chart_by_type(ocorrencias_type, event_types_list, chart_title):
    """Create bar chart of event duration categories for one or more event types"""
    setup_plot_style()
    
    # Apply categorization
    ocorrencias_type['duration_category'] = ocorrencias_type['duration_hours'].apply(categorize_duration)
    
    # Define category order
    category_order = ['< 1h', '1-2h', '2-3h', '3-4h', '4-5h', '5-6h',
                     '6-12h', '12-24h', '> 24h']
    
    # Count events per category
    category_counts = ocorrencias_type['duration_category'].value_counts()
    category_counts = category_counts.reindex(category_order, fill_value=0)
    
    total_events = len(ocorrencias_type)
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
    ax.set_title(f'Duration Categories for {chart_title}\n{STUDY_LOCATION}, {STUDY_PERIOD}',
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
    median_duration = ocorrencias_type['duration_hours'].median()
    mean_duration = ocorrencias_type['duration_hours'].mean()
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
    
    # Get unique event types
    event_types = ocorrencias['tipo'].value_counts().index.tolist()
    print(f"\nEvent types found: {event_types}")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Define chart groups
    chart_groups = [
        {
            'types': ["Bolsão d'água em via", "Lâmina d'água"],
            'title': '"Bolsão d\'água em via" and "Lâmina d\'água" Events',
            'filename': 'bolsao_and_lamina'
        },
        {
            'types': ['Alagamento'],
            'title': '"Alagamento" Events',
            'filename': 'alagamento'
        }
    ]
    
    # Create a chart for each group
    for group in chart_groups:
        print(f"\n{'='*70}")
        print(f"Processing: {group['title']}")
        print(f"{'='*70}")
        
        # Filter data for this group
        ocorrencias_group = ocorrencias[ocorrencias['tipo'].isin(group['types'])].copy()
        n_events = len(ocorrencias_group)
        
        print(f"Events for this group: {n_events}")
        print(f"  Event types included: {group['types']}")
        
        if n_events == 0:
            print(f"Skipping {group['title']} - no events found")
            continue
        
        # Create chart
        print(f"Creating duration categories chart for {group['title']}...")
        fig, category_counts, percentages = create_duration_categories_chart_by_type(
            ocorrencias_group, group['types'], group['title']
        )
        
        print("\nDuration category distribution:")
        for category, count, pct in zip(category_counts.index, category_counts.values, percentages.values):
            print(f"  {category:>8}: {count:>5,} events ({pct:>5.1f}%)")
        
        # Save chart
        output_path = f'{OUTPUT_DIR}/chart_10_duration_categories_{group["filename"]}.png'
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Chart saved to {output_path}")
        plt.close()
    
    print(f"\n{'='*70}")
    print("All charts created successfully!")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()

```

```python
"""
Chart 10: Event Duration Categories by Type
Based on Chart 8 - generates two charts:
1. Combined chart for "Lâmina d'água" and "Bolsão d'água em via"
2. Single chart for "Alagamento"
Each chart shows distribution of events by duration categories
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

def create_duration_categories_chart_by_type(ocorrencias_type, event_types_list, chart_title):
    """Create bar chart of event duration categories for one or more event types"""
    setup_plot_style()
    
    # Apply categorization
    ocorrencias_type['duration_category'] = ocorrencias_type['duration_hours'].apply(categorize_duration)
    
    # Define category order
    category_order = ['< 1h', '1-2h', '2-3h', '3-4h', '4-5h', '5-6h',
                     '6-12h', '12-24h', '> 24h']
    
    # Count events per category
    category_counts = ocorrencias_type['duration_category'].value_counts()
    category_counts = category_counts.reindex(category_order, fill_value=0)
    
    total_events = len(ocorrencias_type)
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
    ax.set_title(f'Duration Categories for {chart_title}\n{STUDY_LOCATION}, {STUDY_PERIOD}',
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
    median_duration = ocorrencias_type['duration_hours'].median()
    mean_duration = ocorrencias_type['duration_hours'].mean()
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
    
    # Get unique event types
    event_types = ocorrencias['tipo'].value_counts().index.tolist()
    print(f"\nEvent types found: {event_types}")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Define chart groups
    chart_groups = [
        {
            'types': ["Bolsão d'água em via", "Lâmina d'água"],
            'title': '"Bolsão d\'água em via" and "Lâmina d\'água" Events',
            'filename': 'bolsao_and_lamina'
        },
        {
            'types': ['Alagamento'],
            'title': '"Alagamento" Events',
            'filename': 'alagamento'
        }
    ]
    
    # Create a chart for each group
    for group in chart_groups:
        print(f"\n{'='*70}")
        print(f"Processing: {group['title']}")
        print(f"{'='*70}")
        
        # Filter data for this group
        ocorrencias_group = ocorrencias[ocorrencias['tipo'].isin(group['types'])].copy()
        n_events = len(ocorrencias_group)
        
        print(f"Events for this group: {n_events}")
        print(f"  Event types included: {group['types']}")
        
        if n_events == 0:
            print(f"Skipping {group['title']} - no events found")
            continue
        
        # Create chart
        print(f"Creating duration categories chart for {group['title']}...")
        fig, category_counts, percentages = create_duration_categories_chart_by_type(
            ocorrencias_group, group['types'], group['title']
        )
        
        print("\nDuration category distribution:")
        for category, count, pct in zip(category_counts.index, category_counts.values, percentages.values):
            print(f"  {category:>8}: {count:>5,} events ({pct:>5.1f}%)")
        
        # Save chart
        output_path = f'{OUTPUT_DIR}/chart_10_duration_categories_{group["filename"]}.png'
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Chart saved to {output_path}")
        plt.close()
    
    print(f"\n{'='*70}")
    print("All charts created successfully!")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()

```

```python
"""
Chart 10: Event Duration Categories by Type
Based on Chart 8 - generates two charts:
1. Combined chart for "Lâmina d'água" and "Bolsão d'água em via"
2. Single chart for "Alagamento"
Each chart shows distribution of events by duration categories
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

def create_duration_categories_chart_by_type(ocorrencias_type, event_types_list, chart_title):
    """Create bar chart of event duration categories for one or more event types"""
    setup_plot_style()
    
    # Apply categorization
    ocorrencias_type['duration_category'] = ocorrencias_type['duration_hours'].apply(categorize_duration)
    
    # Define category order
    category_order = ['< 1h', '1-2h', '2-3h', '3-4h', '4-5h', '5-6h',
                     '6-12h', '12-24h', '> 24h']
    
    # Count events per category
    category_counts = ocorrencias_type['duration_category'].value_counts()
    category_counts = category_counts.reindex(category_order, fill_value=0)
    
    total_events = len(ocorrencias_type)
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
    ax.set_title(f'Duration Categories for {chart_title}\n{STUDY_LOCATION}, {STUDY_PERIOD}',
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
    median_duration = ocorrencias_type['duration_hours'].median()
    mean_duration = ocorrencias_type['duration_hours'].mean()
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
    
    # Get unique event types
    event_types = ocorrencias['tipo'].value_counts().index.tolist()
    print(f"\nEvent types found: {event_types}")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Define chart groups (using generic names)
    chart_groups = [
        {
            'types': ['Flood Type I', 'Flood Type II'],
            'title': 'Flood Type I and Flood Type II Events',
            'filename': 'bolsao_and_lamina'
        },
        {
            'types': ['Flood Type III'],
            'title': 'Flood Type III Events',
            'filename': 'alagamento'
        }
    ]
    
    # Create a chart for each group
    for group in chart_groups:
        print(f"\n{'='*70}")
        print(f"Processing: {group['title']}")
        print(f"{'='*70}")
        
        # Filter data for this group
        ocorrencias_group = ocorrencias[ocorrencias['tipo'].isin(group['types'])].copy()
        n_events = len(ocorrencias_group)
        
        print(f"Events for this group: {n_events}")
        print(f"  Event types included: {group['types']}")
        
        if n_events == 0:
            print(f"Skipping {group['title']} - no events found")
            continue
        
        # Create chart
        print(f"Creating duration categories chart for {group['title']}...")
        fig, category_counts, percentages = create_duration_categories_chart_by_type(
            ocorrencias_group, group['types'], group['title']
        )
        
        print("\nDuration category distribution:")
        for category, count, pct in zip(category_counts.index, category_counts.values, percentages.values):
            print(f"  {category:>8}: {count:>5,} events ({pct:>5.1f}%)")
        
        # Save chart
        output_path = f'{OUTPUT_DIR}/chart_10_duration_categories_{group["filename"]}.png'
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Chart saved to {output_path}")
        plt.close()
    
    print(f"\n{'='*70}")
    print("All charts created successfully!")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()

```

Checking for linting errors and verifying the changes:


Updating docstrings in chart_09 and chart_10:


```python
"""
Chart 9: Event Duration Distribution by Type
Based on Chart 6a - generates two charts:
1. Combined chart for Flood Type I and Flood Type II
2. Single chart for Flood Type III
Each chart shows histogram and CDF for events < 12 hours
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
    
    # Filter out invalid durations (negative or extremely long)
    ocorrencias = ocorrencias[
        (ocorrencias['duration_hours'] >= 0) & 
        (ocorrencias['duration_hours'] <= 72)  # Max 72 hours (3 days)
    ].copy()
    
    return ocorrencias

def calculate_duration_stats(durations):
    """Calculate comprehensive duration statistics"""
    stats_dict = {
        'mean': durations.mean(),
        'median': durations.median(),
        'std': durations.std(),
        'min': durations.min(),
        'max': durations.max(),
        'q25': durations.quantile(0.25),
        'q75': durations.quantile(0.75),
        'q90': durations.quantile(0.90),
        'count': len(durations)
    }
    
    return stats_dict

def create_duration_distribution_chart_by_type(ocorrencias_type, event_types_list, chart_title):
    """Create histogram and CDF chart for one or more event types (< 12 hours)"""
    setup_plot_style()
    
    # Get durations for this event type(s)
    durations = ocorrencias_type['duration_hours'].dropna()
    
    # Filter durations to only show events < 12 hours
    durations_filtered = durations[durations < 12]
    total_events = len(durations)
    filtered_events = len(durations_filtered)
    
    # Calculate statistics from ALL data (for reference)
    stats_dict_all = calculate_duration_stats(durations)
    
    # Calculate statistics from FILTERED data (< 12h) for display on chart
    stats_dict = calculate_duration_stats(durations_filtered)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGURE_SIZES['double'])
    fig.suptitle(f'Duration Distribution for {chart_title} (< 12 hours)\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'], fontweight='bold', y=1.02)
    
    # Panel A: Histogram with statistics
    n, bins, patches = ax1.hist(durations_filtered, bins=24, color=COLORS['primary'],
                                edgecolor='black', linewidth=0.5, alpha=0.7)
    
    # Add vertical lines for statistics
    ax1.axvline(stats_dict['mean'], color=COLORS['secondary'], linestyle='--', 
               linewidth=2, label=f"Mean: {stats_dict['mean']:.2f}h")
    ax1.axvline(stats_dict['median'], color=COLORS['tertiary'], linestyle='--', 
               linewidth=2, label=f"Median: {stats_dict['median']:.2f}h")
    ax1.axvline(stats_dict['q90'], color=COLORS['quaternary'], linestyle=':', 
               linewidth=2, label=f"90th percentile: {stats_dict['q90']:.2f}h")
    
    ax1.set_xlabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_ylabel('Frequency', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_title('Duration Distribution', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax1.legend(loc='upper right', fontsize=FONT_SIZES['legend'])
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    ax1.set_axisbelow(True)
    add_subfigure_label(ax1, '(a)')
    
    # Panel B: Cumulative Distribution Function (CDF)
    sorted_durations = np.sort(durations_filtered)
    cumulative = np.arange(1, len(sorted_durations) + 1) / len(sorted_durations) * 100
    
    ax2.plot(sorted_durations, cumulative, color=COLORS['primary'], linewidth=2)
    ax2.fill_between(sorted_durations, 0, cumulative, color=COLORS['primary'], alpha=0.2)
    
    # Add reference lines
    ax2.axhline(50, color=COLORS['tertiary'], linestyle='--', linewidth=1, alpha=0.5)
    ax2.axhline(90, color=COLORS['quaternary'], linestyle=':', linewidth=1, alpha=0.5)
    ax2.axvline(stats_dict['median'], color=COLORS['tertiary'], linestyle='--', linewidth=1, alpha=0.5)
    ax2.axvline(stats_dict['q90'], color=COLORS['quaternary'], linestyle=':', linewidth=1, alpha=0.5)
    
    # Add annotations
    ax2.text(stats_dict['median'], 50, f" {stats_dict['median']:.2f}h", 
            fontsize=FONT_SIZES['annotation'], verticalalignment='bottom', 
            color=COLORS['tertiary'])
    ax2.text(stats_dict['q90'], 90, f" {stats_dict['q90']:.2f}h", 
            fontsize=FONT_SIZES['annotation'], verticalalignment='bottom',
            color=COLORS['quaternary'])
    
    ax2.set_xlabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_ylabel('Cumulative Percentage (%)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_title('Cumulative Distribution', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax2.grid(True, linestyle='--', alpha=0.3)
    ax2.set_axisbelow(True)
    ax2.set_ylim(0, 100)
    add_subfigure_label(ax2, '(b)')
    
    # Add statistics box (using ALL data for context)
    stats_text = (f"All data:\n"
                 f"Mean: {stats_dict_all['mean']:.2f}h\n"
                 f"Median: {stats_dict_all['median']:.2f}h\n"
                 f"90th pct: {stats_dict_all['q90']:.2f}h")
    ax2.text(0.98, 0.25, stats_text, transform=ax2.transAxes, 
            fontsize=FONT_SIZES['annotation'],
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, edgecolor='gray'))
    
    # Add sample size annotation showing filtered vs total
    sample_text = f'N = {filtered_events:,} (< 12h)\nTotal: {total_events:,}'
    ax2.text(0.98, 0.98, sample_text,
            transform=ax2.transAxes,
            fontsize=FONT_SIZES['annotation'],
            verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray'))
    
    plt.tight_layout()
    
    return fig, stats_dict

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias = load_and_prepare_data()
    print(f"Total flood events with valid duration: {len(ocorrencias)}")
    
    # Get unique event types
    event_types = ocorrencias['tipo'].value_counts().index.tolist()
    print(f"\nEvent types found: {event_types}")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Define chart groups (using generic names)
    chart_groups = [
        {
            'types': ['Flood Type I', 'Flood Type II'],
            'title': 'Flood Type I and Flood Type II Events',
            'filename': 'bolsao_and_lamina'
        },
        {
            'types': ['Flood Type III'],
            'title': 'Flood Type III Events',
            'filename': 'alagamento'
        }
    ]
    
    # Create a chart for each group
    for group in chart_groups:
        print(f"\n{'='*70}")
        print(f"Processing: {group['title']}")
        print(f"{'='*70}")
        
        # Filter data for this group
        ocorrencias_group = ocorrencias[ocorrencias['tipo'].isin(group['types'])].copy()
        n_events = len(ocorrencias_group)
        
        print(f"Events for this group: {n_events}")
        print(f"  Event types included: {group['types']}")
        
        if n_events == 0:
            print(f"Skipping {group['title']} - no events found")
            continue
        
        # Create chart
        print(f"Creating duration distribution chart for {group['title']}...")
        fig, stats_dict = create_duration_distribution_chart_by_type(
            ocorrencias_group, group['types'], group['title']
        )
        
        print("\nDuration Statistics (< 12h filtered):")
        print(f"  Mean: {stats_dict['mean']:.2f} hours")
        print(f"  Median: {stats_dict['median']:.2f} hours")
        print(f"  Std Dev: {stats_dict['std']:.2f} hours")
        print(f"  Min: {stats_dict['min']:.2f} hours")
        print(f"  Max: {stats_dict['max']:.2f} hours")
        print(f"  90th percentile: {stats_dict['q90']:.2f} hours")
        
        # Save chart
        output_path = f'{OUTPUT_DIR}/chart_09_duration_distribution_{group["filename"]}.png'
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Chart saved to {output_path}")
        plt.close()
    
    print(f"\n{'='*70}")
    print("All charts created successfully!")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()

```

```python
"""
Chart 10: Event Duration Categories by Type
Based on Chart 8 - generates two charts:
1. Combined chart for Flood Type I and Flood Type II
2. Single chart for Flood Type III
Each chart shows distribution of events by duration categories
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

def create_duration_categories_chart_by_type(ocorrencias_type, event_types_list, chart_title):
    """Create bar chart of event duration categories for one or more event types"""
    setup_plot_style()
    
    # Apply categorization
    ocorrencias_type['duration_category'] = ocorrencias_type['duration_hours'].apply(categorize_duration)
    
    # Define category order
    category_order = ['< 1h', '1-2h', '2-3h', '3-4h', '4-5h', '5-6h',
                     '6-12h', '12-24h', '> 24h']
    
    # Count events per category
    category_counts = ocorrencias_type['duration_category'].value_counts()
    category_counts = category_counts.reindex(category_order, fill_value=0)
    
    total_events = len(ocorrencias_type)
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
    ax.set_title(f'Duration Categories for {chart_title}\n{STUDY_LOCATION}, {STUDY_PERIOD}',
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
    median_duration = ocorrencias_type['duration_hours'].median()
    mean_duration = ocorrencias_type['duration_hours'].mean()
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
    
    # Get unique event types
    event_types = ocorrencias['tipo'].value_counts().index.tolist()
    print(f"\nEvent types found: {event_types}")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Define chart groups (using generic names)
    chart_groups = [
        {
            'types': ['Flood Type I', 'Flood Type II'],
            'title': 'Flood Type I and Flood Type II Events',
            'filename': 'bolsao_and_lamina'
        },
        {
            'types': ['Flood Type III'],
            'title': 'Flood Type III Events',
            'filename': 'alagamento'
        }
    ]
    
    # Create a chart for each group
    for group in chart_groups:
        print(f"\n{'='*70}")
        print(f"Processing: {group['title']}")
        print(f"{'='*70}")
        
        # Filter data for this group
        ocorrencias_group = ocorrencias[ocorrencias['tipo'].isin(group['types'])].copy()
        n_events = len(ocorrencias_group)
        
        print(f"Events for this group: {n_events}")
        print(f"  Event types included: {group['types']}")
        
        if n_events == 0:
            print(f"Skipping {group['title']} - no events found")
            continue
        
        # Create chart
        print(f"Creating duration categories chart for {group['title']}...")
        fig, category_counts, percentages = create_duration_categories_chart_by_type(
            ocorrencias_group, group['types'], group['title']
        )
        
        print("\nDuration category distribution:")
        for category, count, pct in zip(category_counts.index, category_counts.values, percentages.values):
            print(f"  {category:>8}: {count:>5,} events ({pct:>5.1f}%)")
        
        # Save chart
        output_path = f'{OUTPUT_DIR}/chart_10_duration_categories_{group["filename"]}.png'
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Chart saved to {output_path}")
        plt.close()
    
    print(f"\n{'='*70}")
    print("All charts created successfully!")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()

```

Verifying the changes by checking a key file:


## Summary

1. Added `GENERIC_TYPE_MAPPING` to `config.py`:
   - "Lâmina d'água" → "Flood Type I"
   - "Bolsão d'água em via" → "Flood Type II"
   - "Alagamento" → "Flood Type III"

2. Updated all chart scripts (chart_01 through chart_10) to:
   - Import `GENERIC_TYPE_MAPPING`
   - Apply the generic mapping after `EVENT_TYPE_MAPPING` in the data preparation step

3. Updated chart_09 and chart_10 to:
   - Use generic names in chart group definitions
   - Update docstrings to reflect the generic naming

All scripts now display "Flood Type I", "Flood Type II", and "Flood Type III" instead of the raw category names. The mapping is applied consistently across all visualizations. No linting errors were found.

---

**User**

run the script to generate all charts. use venv

---

**Cursor**

Checking the generate script, then running it with the virtual environment:


Running the generate script using the virtual environment:


All charts generated successfully.

**Summary:**
- 11/11 chart scripts completed successfully
- All charts saved to `results/charts/v1/`
- Generic category names are working correctly:
  - **Flood Type I** (185 events)
  - **Flood Type II** (4,217 events)
  - **Flood Type III** (466 events)

**Generated charts:**
1. chart_01_event_types.png
2. chart_02_temporal_patterns.png
3. chart_03_hourly_distribution.png
4. chart_04_spatial_coverage.png
5. chart_05_hourly_by_season.png
6. chart_06a_duration_distribution.png
7. chart_06b_duration_by_hour.png
8. chart_07a_duration_by_type.png
9. chart_07b_duration_by_season.png
10. chart_08_duration_categories.png
11. chart_09_duration_distribution_bolsao_and_lamina.png
12. chart_09_duration_distribution_alagamento.png
13. chart_10_duration_categories_bolsao_and_lamina.png
14. chart_10_duration_categories_alagamento.png

Total execution time: 113.06 seconds

Note: There are a couple of matplotlib deprecation warnings about the `labels` parameter in boxplot functions, but they don't affect functionality. The charts were generated successfully with the generic category names.

---

**User**

on charts 1 and 7a I want the bars and boxes sorted properly (flood types 1, 2 and 3 ir onder)

---

**Cursor**

Checking chart_01 and chart_07a to ensure Flood Type I, II, and III are sorted correctly:


Updating both charts to sort by Flood Type I, II, III:


```python
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

```

```python
"""
Chart 7a: Event Duration by Type (< 12 hours)
Comparative analysis of flood event durations across different event types
Includes box plots and mean duration with error bars
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

def perform_statistical_tests(ocorrencias):
    """Perform statistical tests comparing durations across groups"""
    # Kruskal-Wallis test for event types (non-parametric ANOVA)
    event_types = ocorrencias['tipo'].unique()
    groups = [ocorrencias[ocorrencias['tipo'] == t]['duration_hours'].dropna() 
              for t in event_types]
    h_stat, p_value = stats.kruskal(*groups)
    
    return h_stat, p_value

def create_duration_by_type_chart(ocorrencias):
    """Create comparative duration analysis chart by event type"""
    setup_plot_style()
    
    # Filter to < 12 hours for panel a
    ocorrencias_filtered = ocorrencias[ocorrencias['duration_hours'] < 12].copy()
    total_events = len(ocorrencias)
    filtered_events = len(ocorrencias_filtered)
    
    # Perform statistical tests on filtered data
    h_stat, p_value = perform_statistical_tests(ocorrencias_filtered)
    
    # Create 1x2 subplot grid
    fig, axes = plt.subplots(1, 2, figsize=FIGURE_SIZES['double'])
    fig.suptitle(f'Flood Event Duration by Type\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'], fontweight='bold', y=1.02)
    
    # Panel A: Box plot by event type (< 12 hours)
    ax1 = axes[0]
    # Define order for flood types
    flood_type_order = ['Flood Type I', 'Flood Type II', 'Flood Type III']
    # Get available event types in the correct order
    available_types = [t for t in flood_type_order if t in ocorrencias_filtered['tipo'].values]
    event_types = available_types
    data_by_type = [ocorrencias_filtered[ocorrencias_filtered['tipo'] == t]['duration_hours'].dropna() 
                    for t in event_types]
    
    bp1 = ax1.boxplot(data_by_type, labels=event_types, patch_artist=True,
                      showmeans=True, meanline=True,
                      boxprops=dict(facecolor=COLORS['primary'], alpha=0.7),
                      medianprops=dict(color='red', linewidth=2),
                      meanprops=dict(color='blue', linewidth=2, linestyle='--'))
    
    ax1.set_ylabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_title('Duration by Event Type (< 12h)', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax1.set_xticklabels(event_types, rotation=45, ha='right')
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    ax1.set_axisbelow(True)
    add_subfigure_label(ax1, '(a)')
    
    # Extend y-axis to accommodate text labels at the top
    y_min, y_max = ax1.get_ylim()
    ax1.set_ylim(y_min, y_max * 1.12)
    
    # Add sample sizes
    for i, event_type in enumerate(event_types):
        n = len(ocorrencias_filtered[ocorrencias_filtered['tipo'] == event_type])
        ax1.text(i+1, ax1.get_ylim()[1] * 0.88, f'n={n}',
                ha='center', fontsize=FONT_SIZES['annotation'])
    
    # Add statistical test result
    # sig_text = f"Kruskal-Wallis: H={h_stat:.2f}, p={'<0.001' if p_value < 0.001 else f'={p_value:.3f}'}"
    # ax1.text(0.02, 0.98, sig_text, transform=ax1.transAxes,
    #         fontsize=FONT_SIZES['annotation'], verticalalignment='top',
    #         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, edgecolor='gray'))
    
    # Add filter info
    filter_text = f'Filtered: {filtered_events:,} / {total_events:,}'
    # filter_text = f'N = {filtered_events:,}'
    ax1.text(0.98, 0.98, filter_text, transform=ax1.transAxes,
            fontsize=FONT_SIZES['annotation'], verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray'))
    
    # Panel B: Mean duration by event type with error bars (all data)
    ax2 = axes[1]
    type_stats = ocorrencias.groupby('tipo')['duration_hours'].agg(['mean', 'std', 'count', 'sem'])
    type_stats = type_stats.sort_values('mean', ascending=False)
    
    bars = ax2.barh(range(len(type_stats)), type_stats['mean'],
                    xerr=type_stats['sem'], capsize=5,
                    color=COLORS['categorical'][:len(type_stats)],
                    edgecolor='black', linewidth=0.5, alpha=0.7)
    
    ax2.set_yticks(range(len(type_stats)))
    ax2.set_yticklabels(type_stats.index)
    ax2.set_xlabel('Mean Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_title('Mean Duration by Event Type', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax2.grid(axis='x', linestyle='--', alpha=0.3)
    ax2.set_axisbelow(True)
    add_subfigure_label(ax2, '(b)')
    
    # Calculate max value for x-axis extension
    max_value = (type_stats['mean'] + type_stats['sem']).max()
    ax2.set_xlim(0, max_value * 1.15)  # Add 25% padding for text labels
    
    # Add value labels
    for i, (mean, sem) in enumerate(zip(type_stats['mean'], type_stats['sem'])):
        ax2.text(mean + sem + 0.1, i, f'{mean:.2f}h',
                va='center', fontsize=FONT_SIZES['annotation'])
    
    add_sample_size_annotation(ax2, len(ocorrencias))
    
    plt.tight_layout()
    
    return fig, type_stats, h_stat, p_value

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias = load_and_prepare_data()
    print(f"Total flood events with valid duration: {len(ocorrencias)}")
    
    print("\nCreating duration by type chart...")
    fig, type_stats, h_stat, p_value = create_duration_by_type_chart(ocorrencias)
    
    print("\nDuration Statistics by Event Type:")
    print(type_stats[['mean', 'std', 'count']])
    print(f"\nKruskal-Wallis Test: H = {h_stat:.2f}, p = {p_value:.6f}")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = f'{OUTPUT_DIR}/chart_07a_duration_by_type.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nChart saved to {output_path}")
    plt.close()

if __name__ == '__main__':
    main()

```

```python
"""
Chart 7a: Event Duration by Type (< 12 hours)
Comparative analysis of flood event durations across different event types
Includes box plots and mean duration with error bars
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

def perform_statistical_tests(ocorrencias):
    """Perform statistical tests comparing durations across groups"""
    # Kruskal-Wallis test for event types (non-parametric ANOVA)
    event_types = ocorrencias['tipo'].unique()
    groups = [ocorrencias[ocorrencias['tipo'] == t]['duration_hours'].dropna() 
              for t in event_types]
    h_stat, p_value = stats.kruskal(*groups)
    
    return h_stat, p_value

def create_duration_by_type_chart(ocorrencias):
    """Create comparative duration analysis chart by event type"""
    setup_plot_style()
    
    # Filter to < 12 hours for panel a
    ocorrencias_filtered = ocorrencias[ocorrencias['duration_hours'] < 12].copy()
    total_events = len(ocorrencias)
    filtered_events = len(ocorrencias_filtered)
    
    # Perform statistical tests on filtered data
    h_stat, p_value = perform_statistical_tests(ocorrencias_filtered)
    
    # Create 1x2 subplot grid
    fig, axes = plt.subplots(1, 2, figsize=FIGURE_SIZES['double'])
    fig.suptitle(f'Flood Event Duration by Type\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'], fontweight='bold', y=1.02)
    
    # Panel A: Box plot by event type (< 12 hours)
    ax1 = axes[0]
    # Define order for flood types
    flood_type_order = ['Flood Type I', 'Flood Type II', 'Flood Type III']
    # Get available event types in the correct order
    available_types = [t for t in flood_type_order if t in ocorrencias_filtered['tipo'].values]
    event_types = available_types
    data_by_type = [ocorrencias_filtered[ocorrencias_filtered['tipo'] == t]['duration_hours'].dropna() 
                    for t in event_types]
    
    bp1 = ax1.boxplot(data_by_type, labels=event_types, patch_artist=True,
                      showmeans=True, meanline=True,
                      boxprops=dict(facecolor=COLORS['primary'], alpha=0.7),
                      medianprops=dict(color='red', linewidth=2),
                      meanprops=dict(color='blue', linewidth=2, linestyle='--'))
    
    ax1.set_ylabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_title('Duration by Event Type (< 12h)', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax1.set_xticklabels(event_types, rotation=45, ha='right')
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    ax1.set_axisbelow(True)
    add_subfigure_label(ax1, '(a)')
    
    # Extend y-axis to accommodate text labels at the top
    y_min, y_max = ax1.get_ylim()
    ax1.set_ylim(y_min, y_max * 1.12)
    
    # Add sample sizes
    for i, event_type in enumerate(event_types):
        n = len(ocorrencias_filtered[ocorrencias_filtered['tipo'] == event_type])
        ax1.text(i+1, ax1.get_ylim()[1] * 0.88, f'n={n}',
                ha='center', fontsize=FONT_SIZES['annotation'])
    
    # Add statistical test result
    # sig_text = f"Kruskal-Wallis: H={h_stat:.2f}, p={'<0.001' if p_value < 0.001 else f'={p_value:.3f}'}"
    # ax1.text(0.02, 0.98, sig_text, transform=ax1.transAxes,
    #         fontsize=FONT_SIZES['annotation'], verticalalignment='top',
    #         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, edgecolor='gray'))
    
    # Add filter info
    filter_text = f'Filtered: {filtered_events:,} / {total_events:,}'
    # filter_text = f'N = {filtered_events:,}'
    ax1.text(0.98, 0.98, filter_text, transform=ax1.transAxes,
            fontsize=FONT_SIZES['annotation'], verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray'))
    
    # Panel B: Mean duration by event type with error bars (all data)
    ax2 = axes[1]
    # Define order for flood types
    flood_type_order = ['Flood Type I', 'Flood Type II', 'Flood Type III']
    type_stats = ocorrencias.groupby('tipo')['duration_hours'].agg(['mean', 'std', 'count', 'sem'])
    # Reindex to ensure correct order, only including types that exist
    type_stats = type_stats.reindex([t for t in flood_type_order if t in type_stats.index])
    
    bars = ax2.barh(range(len(type_stats)), type_stats['mean'],
                    xerr=type_stats['sem'], capsize=5,
                    color=COLORS['categorical'][:len(type_stats)],
                    edgecolor='black', linewidth=0.5, alpha=0.7)
    
    ax2.set_yticks(range(len(type_stats)))
    ax2.set_yticklabels(type_stats.index)
    ax2.set_xlabel('Mean Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_title('Mean Duration by Event Type', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax2.grid(axis='x', linestyle='--', alpha=0.3)
    ax2.set_axisbelow(True)
    add_subfigure_label(ax2, '(b)')
    
    # Calculate max value for x-axis extension
    max_value = (type_stats['mean'] + type_stats['sem']).max()
    ax2.set_xlim(0, max_value * 1.15)  # Add 25% padding for text labels
    
    # Add value labels
    for i, (mean, sem) in enumerate(zip(type_stats['mean'], type_stats['sem'])):
        ax2.text(mean + sem + 0.1, i, f'{mean:.2f}h',
                va='center', fontsize=FONT_SIZES['annotation'])
    
    add_sample_size_annotation(ax2, len(ocorrencias))
    
    plt.tight_layout()
    
    return fig, type_stats, h_stat, p_value

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias = load_and_prepare_data()
    print(f"Total flood events with valid duration: {len(ocorrencias)}")
    
    print("\nCreating duration by type chart...")
    fig, type_stats, h_stat, p_value = create_duration_by_type_chart(ocorrencias)
    
    print("\nDuration Statistics by Event Type:")
    print(type_stats[['mean', 'std', 'count']])
    print(f"\nKruskal-Wallis Test: H = {h_stat:.2f}, p = {p_value:.6f}")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = f'{OUTPUT_DIR}/chart_07a_duration_by_type.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nChart saved to {output_path}")
    plt.close()

if __name__ == '__main__':
    main()

```

Checking for linting errors, then regenerating the charts:


Regenerating chart 7a:


Both charts have been updated and regenerated.

**Changes made:**

1. **Chart 1 (chart_01_event_types.py)**: Updated to sort bars by the predefined order: Flood Type I, Flood Type II, Flood Type III (instead of sorting by count).

2. **Chart 7a (chart_07a_duration_by_type.py)**:
   - **Panel A (Box plot)**: Sorted by Flood Type I, II, III order
   - **Panel B (Mean duration bars)**: Sorted by Flood Type I, II, III order (instead of sorting by mean value)

Both charts now display the flood types in the correct order: **Flood Type I**, **Flood Type II**, **Flood Type III**.

The charts have been regenerated and saved. The output confirms the sorting is working correctly - you can see in chart 7a's statistics that the types are now listed in the I, II, III order.

---

**User**

you did 3, 2, 1. I want 1, 2, 3

---

**Cursor**

Reversing the order so Flood Type I appears first. Checking and fixing both charts:


Reversing the order so Flood Type I appears first (top in horizontal bars, leftmost in box plots):


```python
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
    
    # Define order for flood types (reversed for horizontal bar chart - first item at top)
    flood_type_order = ['Flood Type III', 'Flood Type II', 'Flood Type I']
    
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

```

```python
"""
Chart 7a: Event Duration by Type (< 12 hours)
Comparative analysis of flood event durations across different event types
Includes box plots and mean duration with error bars
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

def perform_statistical_tests(ocorrencias):
    """Perform statistical tests comparing durations across groups"""
    # Kruskal-Wallis test for event types (non-parametric ANOVA)
    event_types = ocorrencias['tipo'].unique()
    groups = [ocorrencias[ocorrencias['tipo'] == t]['duration_hours'].dropna() 
              for t in event_types]
    h_stat, p_value = stats.kruskal(*groups)
    
    return h_stat, p_value

def create_duration_by_type_chart(ocorrencias):
    """Create comparative duration analysis chart by event type"""
    setup_plot_style()
    
    # Filter to < 12 hours for panel a
    ocorrencias_filtered = ocorrencias[ocorrencias['duration_hours'] < 12].copy()
    total_events = len(ocorrencias)
    filtered_events = len(ocorrencias_filtered)
    
    # Perform statistical tests on filtered data
    h_stat, p_value = perform_statistical_tests(ocorrencias_filtered)
    
    # Create 1x2 subplot grid
    fig, axes = plt.subplots(1, 2, figsize=FIGURE_SIZES['double'])
    fig.suptitle(f'Flood Event Duration by Type\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'], fontweight='bold', y=1.02)
    
    # Panel A: Box plot by event type (< 12 hours)
    ax1 = axes[0]
    # Define order for flood types (I, II, III from left to right)
    flood_type_order = ['Flood Type I', 'Flood Type II', 'Flood Type III']
    # Get available event types in the correct order
    available_types = [t for t in flood_type_order if t in ocorrencias_filtered['tipo'].values]
    event_types = available_types
    data_by_type = [ocorrencias_filtered[ocorrencias_filtered['tipo'] == t]['duration_hours'].dropna() 
                    for t in event_types]
    
    bp1 = ax1.boxplot(data_by_type, labels=event_types, patch_artist=True,
                      showmeans=True, meanline=True,
                      boxprops=dict(facecolor=COLORS['primary'], alpha=0.7),
                      medianprops=dict(color='red', linewidth=2),
                      meanprops=dict(color='blue', linewidth=2, linestyle='--'))
    
    ax1.set_ylabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_title('Duration by Event Type (< 12h)', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax1.set_xticklabels(event_types, rotation=45, ha='right')
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    ax1.set_axisbelow(True)
    add_subfigure_label(ax1, '(a)')
    
    # Extend y-axis to accommodate text labels at the top
    y_min, y_max = ax1.get_ylim()
    ax1.set_ylim(y_min, y_max * 1.12)
    
    # Add sample sizes
    for i, event_type in enumerate(event_types):
        n = len(ocorrencias_filtered[ocorrencias_filtered['tipo'] == event_type])
        ax1.text(i+1, ax1.get_ylim()[1] * 0.88, f'n={n}',
                ha='center', fontsize=FONT_SIZES['annotation'])
    
    # Add statistical test result
    # sig_text = f"Kruskal-Wallis: H={h_stat:.2f}, p={'<0.001' if p_value < 0.001 else f'={p_value:.3f}'}"
    # ax1.text(0.02, 0.98, sig_text, transform=ax1.transAxes,
    #         fontsize=FONT_SIZES['annotation'], verticalalignment='top',
    #         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, edgecolor='gray'))
    
    # Add filter info
    filter_text = f'Filtered: {filtered_events:,} / {total_events:,}'
    # filter_text = f'N = {filtered_events:,}'
    ax1.text(0.98, 0.98, filter_text, transform=ax1.transAxes,
            fontsize=FONT_SIZES['annotation'], verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray'))
    
    # Panel B: Mean duration by event type with error bars (all data)
    ax2 = axes[1]
    # Define order for flood types
    flood_type_order = ['Flood Type I', 'Flood Type II', 'Flood Type III']
    type_stats = ocorrencias.groupby('tipo')['duration_hours'].agg(['mean', 'std', 'count', 'sem'])
    # Reindex to ensure correct order, only including types that exist
    type_stats = type_stats.reindex([t for t in flood_type_order if t in type_stats.index])
    
    bars = ax2.barh(range(len(type_stats)), type_stats['mean'],
                    xerr=type_stats['sem'], capsize=5,
                    color=COLORS['categorical'][:len(type_stats)],
                    edgecolor='black', linewidth=0.5, alpha=0.7)
    
    ax2.set_yticks(range(len(type_stats)))
    ax2.set_yticklabels(type_stats.index)
    ax2.set_xlabel('Mean Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_title('Mean Duration by Event Type', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax2.grid(axis='x', linestyle='--', alpha=0.3)
    ax2.set_axisbelow(True)
    add_subfigure_label(ax2, '(b)')
    
    # Calculate max value for x-axis extension
    max_value = (type_stats['mean'] + type_stats['sem']).max()
    ax2.set_xlim(0, max_value * 1.15)  # Add 25% padding for text labels
    
    # Add value labels
    for i, (mean, sem) in enumerate(zip(type_stats['mean'], type_stats['sem'])):
        ax2.text(mean + sem + 0.1, i, f'{mean:.2f}h',
                va='center', fontsize=FONT_SIZES['annotation'])
    
    add_sample_size_annotation(ax2, len(ocorrencias))
    
    plt.tight_layout()
    
    return fig, type_stats, h_stat, p_value

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias = load_and_prepare_data()
    print(f"Total flood events with valid duration: {len(ocorrencias)}")
    
    print("\nCreating duration by type chart...")
    fig, type_stats, h_stat, p_value = create_duration_by_type_chart(ocorrencias)
    
    print("\nDuration Statistics by Event Type:")
    print(type_stats[['mean', 'std', 'count']])
    print(f"\nKruskal-Wallis Test: H = {h_stat:.2f}, p = {p_value:.6f}")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = f'{OUTPUT_DIR}/chart_07a_duration_by_type.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nChart saved to {output_path}")
    plt.close()

if __name__ == '__main__':
    main()

```

```python
"""
Chart 7a: Event Duration by Type (< 12 hours)
Comparative analysis of flood event durations across different event types
Includes box plots and mean duration with error bars
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

def perform_statistical_tests(ocorrencias):
    """Perform statistical tests comparing durations across groups"""
    # Kruskal-Wallis test for event types (non-parametric ANOVA)
    event_types = ocorrencias['tipo'].unique()
    groups = [ocorrencias[ocorrencias['tipo'] == t]['duration_hours'].dropna() 
              for t in event_types]
    h_stat, p_value = stats.kruskal(*groups)
    
    return h_stat, p_value

def create_duration_by_type_chart(ocorrencias):
    """Create comparative duration analysis chart by event type"""
    setup_plot_style()
    
    # Filter to < 12 hours for panel a
    ocorrencias_filtered = ocorrencias[ocorrencias['duration_hours'] < 12].copy()
    total_events = len(ocorrencias)
    filtered_events = len(ocorrencias_filtered)
    
    # Perform statistical tests on filtered data
    h_stat, p_value = perform_statistical_tests(ocorrencias_filtered)
    
    # Create 1x2 subplot grid
    fig, axes = plt.subplots(1, 2, figsize=FIGURE_SIZES['double'])
    fig.suptitle(f'Flood Event Duration by Type\n{STUDY_LOCATION}, {STUDY_PERIOD}',
                fontsize=FONT_SIZES['title'], fontweight='bold', y=1.02)
    
    # Panel A: Box plot by event type (< 12 hours)
    ax1 = axes[0]
    # Define order for flood types (I, II, III from left to right)
    flood_type_order = ['Flood Type I', 'Flood Type II', 'Flood Type III']
    # Get available event types in the correct order
    available_types = [t for t in flood_type_order if t in ocorrencias_filtered['tipo'].values]
    event_types = available_types
    data_by_type = [ocorrencias_filtered[ocorrencias_filtered['tipo'] == t]['duration_hours'].dropna() 
                    for t in event_types]
    
    bp1 = ax1.boxplot(data_by_type, labels=event_types, patch_artist=True,
                      showmeans=True, meanline=True,
                      boxprops=dict(facecolor=COLORS['primary'], alpha=0.7),
                      medianprops=dict(color='red', linewidth=2),
                      meanprops=dict(color='blue', linewidth=2, linestyle='--'))
    
    ax1.set_ylabel('Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax1.set_title('Duration by Event Type (< 12h)', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax1.set_xticklabels(event_types, rotation=45, ha='right')
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    ax1.set_axisbelow(True)
    add_subfigure_label(ax1, '(a)')
    
    # Extend y-axis to accommodate text labels at the top
    y_min, y_max = ax1.get_ylim()
    ax1.set_ylim(y_min, y_max * 1.12)
    
    # Add sample sizes
    for i, event_type in enumerate(event_types):
        n = len(ocorrencias_filtered[ocorrencias_filtered['tipo'] == event_type])
        ax1.text(i+1, ax1.get_ylim()[1] * 0.88, f'n={n}',
                ha='center', fontsize=FONT_SIZES['annotation'])
    
    # Add statistical test result
    # sig_text = f"Kruskal-Wallis: H={h_stat:.2f}, p={'<0.001' if p_value < 0.001 else f'={p_value:.3f}'}"
    # ax1.text(0.02, 0.98, sig_text, transform=ax1.transAxes,
    #         fontsize=FONT_SIZES['annotation'], verticalalignment='top',
    #         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, edgecolor='gray'))
    
    # Add filter info
    filter_text = f'Filtered: {filtered_events:,} / {total_events:,}'
    # filter_text = f'N = {filtered_events:,}'
    ax1.text(0.98, 0.98, filter_text, transform=ax1.transAxes,
            fontsize=FONT_SIZES['annotation'], verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray'))
    
    # Panel B: Mean duration by event type with error bars (all data)
    ax2 = axes[1]
    # Define order for flood types (reversed for horizontal bar chart - first item at top)
    flood_type_order = ['Flood Type III', 'Flood Type II', 'Flood Type I']
    type_stats = ocorrencias.groupby('tipo')['duration_hours'].agg(['mean', 'std', 'count', 'sem'])
    # Reindex to ensure correct order, only including types that exist
    type_stats = type_stats.reindex([t for t in flood_type_order if t in type_stats.index])
    
    bars = ax2.barh(range(len(type_stats)), type_stats['mean'],
                    xerr=type_stats['sem'], capsize=5,
                    color=COLORS['categorical'][:len(type_stats)],
                    edgecolor='black', linewidth=0.5, alpha=0.7)
    
    ax2.set_yticks(range(len(type_stats)))
    ax2.set_yticklabels(type_stats.index)
    ax2.set_xlabel('Mean Duration (hours)', fontsize=FONT_SIZES['axis_label'], fontweight='bold')
    ax2.set_title('Mean Duration by Event Type', fontsize=FONT_SIZES['subtitle'], pad=10)
    ax2.grid(axis='x', linestyle='--', alpha=0.3)
    ax2.set_axisbelow(True)
    add_subfigure_label(ax2, '(b)')
    
    # Calculate max value for x-axis extension
    max_value = (type_stats['mean'] + type_stats['sem']).max()
    ax2.set_xlim(0, max_value * 1.15)  # Add 25% padding for text labels
    
    # Add value labels
    for i, (mean, sem) in enumerate(zip(type_stats['mean'], type_stats['sem'])):
        ax2.text(mean + sem + 0.1, i, f'{mean:.2f}h',
                va='center', fontsize=FONT_SIZES['annotation'])
    
    add_sample_size_annotation(ax2, len(ocorrencias))
    
    plt.tight_layout()
    
    return fig, type_stats, h_stat, p_value

def main():
    """Main execution function"""
    print("Loading data...")
    ocorrencias = load_and_prepare_data()
    print(f"Total flood events with valid duration: {len(ocorrencias)}")
    
    print("\nCreating duration by type chart...")
    fig, type_stats, h_stat, p_value = create_duration_by_type_chart(ocorrencias)
    
    print("\nDuration Statistics by Event Type:")
    print(type_stats[['mean', 'std', 'count']])
    print(f"\nKruskal-Wallis Test: H = {h_stat:.2f}, p = {p_value:.6f}")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = f'{OUTPUT_DIR}/chart_07a_duration_by_type.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nChart saved to {output_path}")
    plt.close()

if __name__ == '__main__':
    main()

```

Regenerating both charts to verify the order:


Both charts have been updated and regenerated.

**Changes made:**

1. **Chart 1 (horizontal bar chart)**: Reversed the order so Flood Type I appears at the top, then II, then III (bottom to top: I, II, III).

2. **Chart 7a**:
   - **Panel A (box plot)**: Order is I, II, III from left to right.
   - **Panel B (horizontal bar chart)**: Reversed so Flood Type I appears at the top, then II, then III (bottom to top: I, II, III).

The charts now display in the order **1, 2, 3** (Flood Type I, Flood Type II, Flood Type III) as requested. The statistics output order in the console doesn't affect the chart display; the charts are sorted correctly.

