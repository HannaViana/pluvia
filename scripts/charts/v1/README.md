# Improved Charts for Scientific Publication - Version 1

## Overview

This directory contains improved chart generation scripts designed for scientific publication. The charts address critical weaknesses identified in the original visualization set and follow best practices for academic publications.

## Key Improvements

### 1. **Consolidated Chart Set**
- **Expanded to 11 chart scripts** (from original 5) generating 14 total images with duration analysis
- Each chart provides unique, complementary insights
- Better narrative flow and logical progression
- Duration analysis split into focused, interpretable visualizations
- Event type-specific analysis for detailed comparisons (combined and separate views)

### 2. **Enhanced Statistical Rigor**
- **Confidence intervals** (95% CI) for temporal patterns
- **Sample sizes** clearly displayed on all charts
- Statistical tests performed during analysis (not displayed on charts for clarity)

### 3. **Improved Visual Design**
- **Unified color palette** (colorblind-friendly from ColorBrewer)
- **Consistent typography** and font sizes across all charts
- **Standardized dimensions** for publication compatibility
- **Subfigure labels** (a, b, c) for multi-panel figures
- **Professional styling** using seaborn-paper theme

### 4. **Better Chart Types**
- **Replaced pie charts with bar charts** for accurate categorical comparison
- **Added cumulative distribution function (CDF)** for spatial coverage analysis
- **Multi-panel figures** to show complementary views efficiently

### 5. **Publication-Ready Features**
- **Comprehensive titles** including location and time period
- **Clear axis labels** with units
- **Grid lines** for easier reading
- **Annotations** for key statistics and findings
- **High resolution** (300 DPI) output

## Chart Descriptions

### Chart 1: Event Type Distribution
**File:** [`chart_01_event_types.py`](chart_01_event_types.py)  
**Output:** `results/charts/v1/chart_01_event_types.png`

**Improvements over original:**
- Horizontal bar chart instead of pie chart (more accurate comparison)
- Includes both counts and percentages
- Sample size annotation
- Clear value labels

**Key findings:**
- N = 4,868 flood events
- "Bolsão d'água em via" dominates (86.6%)
- Clear hierarchy of event types

---

### Chart 2: Temporal Patterns
**File:** [`chart_02_temporal_patterns.py`](chart_02_temporal_patterns.py)  
**Output:** `results/charts/v1/chart_02_temporal_patterns.png`

**Improvements over original:**
- **Panel (a):** Monthly distribution with 95% confidence intervals
- **Panel (b):** Seasonal distribution with clear visual comparison
- Eliminates redundancy (combined 5 temporal charts into 1)
- Non-negative confidence bounds

**Key findings:**
- Strong seasonal pattern (Summer: 47.9%, Winter: 6.3%)
- Peak months: February (108 events avg), March (87), January (74)
- Clear seasonal variation in flood occurrence

---

### Chart 3: Hourly Distribution
**File:** [`chart_03_hourly_distribution.py`](chart_03_hourly_distribution.py)  
**Output:** `results/charts/v1/chart_03_hourly_distribution.png`

**Improvements over original:**
- Mean and threshold lines (mean + 1σ)
- Peak hours highlighted in red
- Clear identification of peak and low activity periods

**Key findings:**
- Strong diurnal pattern with evening concentration
- Peak hours: 17:00-21:00 (evening rush hour)
- Minimum: 03:00-08:00 (early morning)
- Potential reporting bias during business hours

---

### Chart 4: Spatial Coverage Analysis
**File:** [`chart_04_spatial_coverage.py`](chart_04_spatial_coverage.py)  
**Output:** `results/charts/v1/chart_04_spatial_coverage.png`

**Improvements over original:**
- **Panel (a):** Histogram with mean, median, and 90th percentile
- **Panel (b):** Cumulative distribution function (CDF)
- Coverage statistics clearly annotated
- Addresses spatial bias implications

**Key findings:**
- 50% of events within median distance to nearest station
- 90% coverage distance clearly marked
- Important for understanding data quality and spatial representativeness

---

### Chart 5: Hourly Distribution by Season
**File:** [`chart_05_hourly_by_season.py`](chart_05_hourly_by_season.py)
**Output:** `results/charts/v1/chart_05_hourly_by_season.png`

**New addition:**
- **Four-panel figure** (2x2 grid) showing hourly patterns for each season
- Each panel includes mean, threshold lines, and peak hour identification
- Season-specific color coding with peak hours highlighted

**Key findings:**
- **Summer (N=2,330):** Strong evening peak (17:00-20:00), 243 events at 19:00
- **Autumn (N=1,534):** Evening peak shifts later (19:00-22:00), 113 events at 20:00
- **Winter (N=307):** Weaker pattern, morning peak (06:00-07:00), 26 events at 16:00
- **Spring (N=697):** Mixed pattern with peaks at 10:00, 17:00, and 22:00
- All seasons show distinct non-uniform hourly distributions

---

### Chart 6: Event Duration Distribution
**File:** [`chart_06_duration_distribution.py`](chart_06_duration_distribution.py)
**Output:** `results/charts/v1/chart_06a_duration_distribution.png`, `results/charts/v1/chart_06b_duration_by_hour.png`

**New addition:**
- **Part 1 (Panels a & b):** Histogram and CDF for events < 12 hours
- **Part 2:** Average duration by hour of day
- Comprehensive duration statistics with mean, median, and percentiles
- Filter annotation showing events < 12 hours vs total

**Key findings:**
- Duration distribution heavily skewed toward short events
- Most events resolve within a few hours
- Hourly variation in average event duration

---

### Chart 7a: Event Duration by Type
**File:** [`chart_07a_duration_by_type.py`](chart_07a_duration_by_type.py)
**Output:** `results/charts/v1/chart_07a_duration_by_type.png`

**New addition:**
- **Panel (a):** Box plot by event type (< 12 hours only)
- **Panel (b):** Mean duration by event type with error bars (all data)
- Kruskal-Wallis test for statistical comparison
- Sample sizes displayed for each event type

**Key findings:**
- Significant differences in duration across event types
- Box plots reveal distribution characteristics for short-duration events
- Mean durations provide overall comparison including longer events

---

### Chart 7b: Event Duration by Season
**File:** [`chart_07b_duration_by_season.py`](chart_07b_duration_by_season.py)
**Output:** `results/charts/v1/chart_07b_duration_by_season.png`

**New addition:**
- **Panel (a):** Box plot by season (< 12 hours only)
- **Panel (b):** Violin plot showing distribution by season (< 12 hours only)
- Season-specific color coding
- Sample sizes displayed for each season

**Key findings:**
- Seasonal variations in event duration patterns
- Violin plots reveal distribution shapes and multimodality
- Both panels filtered to < 12 hours for focus on typical events

---

### Chart 8: Event Duration Categories
**File:** [`chart_08_duration_categories.py`](chart_08_duration_categories.py)
**Output:** `results/charts/v1/chart_08_duration_categories.png`

**New addition:**
- Granular categorization of event durations
- More detailed breakdown for 1-6 hour range
- Counts and percentages for each category
- Gradient color scheme indicating duration length

**Key findings:**
- Clear distribution across duration categories
- Majority of events in specific duration ranges
- Useful for operational planning and response

---

### Chart 9: Event Duration Distribution by Type
**File:** [`chart_09_duration_distribution_by_type.py`](chart_09_duration_distribution_by_type.py)
**Output:**
- `results/charts/v1/chart_09_duration_distribution_bolsao_and_lamina.png`
- `results/charts/v1/chart_09_duration_distribution_alagamento.png`

**New addition:**
- Based on Chart 6a design
- **Two charts:** one combining "Bolsão d'água em via" and "Lâmina d'água", another for "Alagamento"
- Each chart has **Panel (a):** Histogram and **Panel (b):** CDF for events < 12 hours
- Comprehensive duration statistics with mean, median, and percentiles
- Filter annotation showing events < 12 hours vs total

**Key findings:**
- Event type-specific duration patterns revealed
- "Alagamento" events show significantly longer durations compared to other types
- "Bolsão d'água" and "Lâmina d'água" have similar duration characteristics
- Useful for resource allocation and response planning by event type

---

### Chart 10: Event Duration Categories by Type
**File:** [`chart_10_duration_categories_by_type.py`](chart_10_duration_categories_by_type.py)
**Output:**
- `results/charts/v1/chart_10_duration_categories_bolsao_and_lamina.png`
- `results/charts/v1/chart_10_duration_categories_alagamento.png`

**New addition:**
- Based on Chart 8 design
- **Two charts:** one combining "Bolsão d'água em via" and "Lâmina d'água", another for "Alagamento"
- Granular categorization of event durations (< 1h, 1-2h, 2-3h, etc.)
- Counts and percentages for each category
- Gradient color scheme indicating duration length

**Key findings:**
- Event type-specific distribution across duration categories
- "Alagamento" events more evenly distributed across longer duration categories
- "Bolsão d'água" and "Lâmina d'água" concentrated in shorter duration ranges (1-3 hours)
- Critical for developing type-specific response protocols

---

## File Structure

```
scripts/charts/v1/
├── README.md                                # This file
├── config.py                                # Unified configuration module
├── chart_01_event_types.py                 # Event type distribution
├── chart_02_temporal_patterns.py           # Monthly & seasonal patterns
├── chart_03_hourly_distribution.py         # Hourly distribution (overall)
├── chart_04_spatial_coverage.py            # Distance to stations
├── chart_05_hourly_by_season.py            # Hourly distribution by season
├── chart_06_duration_distribution.py       # Duration distribution (histogram & CDF)
├── chart_07a_duration_by_type.py           # Duration by event type
├── chart_07b_duration_by_season.py         # Duration by season
├── chart_08_duration_categories.py         # Duration categories
├── chart_09_duration_distribution_by_type.py  # Duration distribution per event type (3 charts)
├── chart_10_duration_categories_by_type.py    # Duration categories per event type (3 charts)
├── generate_all_charts.py                  # Master script
└── requirements.txt                         # Python dependencies

results/charts/v1/
├── chart_01_event_types.png
├── chart_02_temporal_patterns.png
├── chart_03_hourly_distribution.png
├── chart_04_spatial_coverage.png
├── chart_05_hourly_by_season.png
├── chart_06a_duration_distribution.png
├── chart_06b_duration_by_hour.png
├── chart_07a_duration_by_type.png
├── chart_07b_duration_by_season.png
├── chart_08_duration_categories.png
├── chart_09_duration_distribution_bolsao_and_lamina.png
├── chart_09_duration_distribution_alagamento.png
├── chart_10_duration_categories_bolsao_and_lamina.png
└── chart_10_duration_categories_alagamento.png
```

## Usage

### Generate All Charts

```bash
# From project root
./venv/bin/python scripts/charts/v1/generate_all_charts.py
```

### Generate Individual Charts

```bash
# From project root
./venv/bin/python scripts/charts/v1/chart_01_event_types.py
./venv/bin/python scripts/charts/v1/chart_02_temporal_patterns.py
./venv/bin/python scripts/charts/v1/chart_03_hourly_distribution.py
./venv/bin/python scripts/charts/v1/chart_04_spatial_coverage.py
./venv/bin/python scripts/charts/v1/chart_05_hourly_by_season.py
./venv/bin/python scripts/charts/v1/chart_06_duration_distribution.py
./venv/bin/python scripts/charts/v1/chart_07a_duration_by_type.py
./venv/bin/python scripts/charts/v1/chart_07b_duration_by_season.py
./venv/bin/python scripts/charts/v1/chart_08_duration_categories.py
./venv/bin/python scripts/charts/v1/chart_09_duration_distribution_by_type.py
./venv/bin/python scripts/charts/v1/chart_10_duration_categories_by_type.py
```

## Dependencies

```
pandas
matplotlib
seaborn
numpy
scipy
geopandas
```

Install with:
```bash
./venv/bin/pip install -r scripts/charts/v1/requirements.txt
```

## Configuration

All visual styling is centralized in [`config.py`](config.py):

- **Colors:** Colorblind-friendly palette from ColorBrewer
- **Typography:** Consistent font sizes and weights
- **Dimensions:** Standardized figure sizes
- **Paths:** Data and output directories
- **Constants:** Study period, location, significance level

To modify styling across all charts, edit [`config.py`](config.py).

## Comparison with Original Charts

| Original | Issues | Improved Version |
|----------|--------|------------------|
| Chart 1 (Pie) | Pie chart, no context | Chart 1: Bar chart with percentages |
| Chart 2-5 (Temporal) | Redundant, no statistics | Chart 2: Combined with CI & visual comparison |
| Chart 6 (Hourly) | No error bars, no peak identification | Chart 3: With mean lines & peak hours |
| Chart 7 (Monthly) | Duplicate of Chart 3 | **Removed** (redundant) |
| Chart 8 (Distance) | Histogram only, no CDF | Chart 4: Histogram + CDF with coverage |
| - | Missing seasonal hourly analysis | Chart 5: Hourly by season (NEW) |
| - | Missing duration analysis | Charts 6, 7a, 7b, 8, 9, 10: Duration analysis (NEW) |

**Result:** 8 original charts → 11 chart scripts generating 14 images with duration analysis, better design, and new insights

## Scientific Publication Checklist

- [x] High resolution (300 DPI)
- [x] Colorblind-friendly palette
- [x] Consistent typography
- [x] Sample sizes displayed
- [x] Statistical tests performed in analysis
- [x] Confidence intervals shown (where applicable)
- [x] Subfigure labels (a, b, c)
- [x] Comprehensive titles with context
- [x] Clear axis labels with units
- [x] Professional styling
- [x] No redundant information
- [x] Logical narrative flow

## Notes for Publication

1. **Figure Captions:** Add detailed captions in your manuscript explaining each panel and key findings

2. **Statistical Reporting:** Include the following in your methods section:
   - Statistical tests were performed to assess distribution patterns (results available in analysis scripts)
   - 95% confidence intervals for temporal averages
   - Distance calculations using SIRGAS 2000 / UTM zone 23S projection

3. **Limitations:** Discuss potential reporting bias in hourly distribution (business hours effect)

4. **Spatial Coverage:** Address implications of distance to rain gauge stations for data quality

5. **Color Accessibility:** All charts use colorblind-friendly palettes suitable for grayscale printing

## Future Improvements

Potential enhancements for version 2:
- Add trend analysis with Mann-Kendall test
- Include inter-annual variability analysis
- Add spatial autocorrelation analysis
- Create combined figure for manuscript (all 4 charts in one)
- Add event duration analysis
- Include neighborhood-level analysis

## Citation

When using these charts in publications, ensure proper attribution of:
- Data sources (COR, AlertaRio)
- Analysis methods
- Software used (Python, matplotlib, seaborn, geopandas)

## Contact

For questions or suggestions about these visualizations, please refer to the main project README.

---

**Version:** 1.0  
**Date:** 2025-12-20  
**Status:** Production-ready for scientific publication
