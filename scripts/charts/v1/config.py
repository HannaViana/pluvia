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
