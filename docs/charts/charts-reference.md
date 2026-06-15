# Charts Reference Documentation

This document provides detailed information about the key charts used in the flood analysis project, including their location, data sources, and processing logic.

## Data Sources

All charts use the following primary data sources:

- **Main Dataset**: `data/meteorologia/clean/adm_cor_comando/ocorrencias.csv`
- **Event Types (POPs)**: `data/raw/adm_cor_comando/pops.csv`
- **Neighborhoods Shapefile**: `data/meteorologia/clean/dados_mestres/bairro.shp`

## Common Data Processing

All charts share the following preprocessing steps (found in each Python file):

**Location**: Lines 24-44 in [`preliminary.py`](nbs/exploration/ocorrencias/preliminary.py:24-44), [`temporal.py`](nbs/exploration/ocorrencias/temporal.py:29-53), and [`spatial.py`](nbs/exploration/ocorrencias/spatial.py:24-44)

```python
# Convert datetime fields
ocorrencias['data_inicio'] = pd.to_datetime(ocorrencias['data_inicio'])
ocorrencias['data_fim'] = pd.to_datetime(ocorrencias['data_fim'])

# Map event type
ocorrencias['tipo'] = ocorrencias['id_pop'].map(pops.set_index('id')['titulo'])

# Filter flood events
flood_types = [
    "Bolsão d'água em via",
    'Alagamento',
    'Alagamentos e enchentes',
    'Enchente',
    "Lâmina d'água"
]
ocorrencias = ocorrencias[ocorrencias['tipo'].isin(flood_types)]
ocorrencias['tipo'] = ocorrencias['tipo'].replace('Alagamentos e enchentes', 'Alagamento').replace('Enchente', 'Alagamento')
```

**Additional temporal features** (Lines 89-114 in all files):
- Duration calculation (seconds and minutes)
- Hour, day of week, month, year extraction
- Season assignment (Summer, Autumn, Winter, Spring)

---

## Chart 1: Pie Chart - Percentage Share of Event Types

**Source File**: [`preliminary.py`](nbs/exploration/ocorrencias/preliminary.py:332-360)

**Code Lines**: 332-360

**Chart Title**: "Distribuição Percentual dos Tipos de Evento"

**Data Processing**:
- **Input**: Preprocessed `ocorrencias` DataFrame
- **Aggregation**: Event type counts and percentages (Lines 167-174)
  ```python
  event_type_counts = ocorrencias['tipo'].value_counts().to_frame()
  event_type_percentages = (ocorrencias['tipo'].value_counts(normalize=True) * 100).to_frame()
  ```

**Visualization Code**:
```python
# Lines 332-360
labels = event_type_counts.index
sizes = event_type_counts['count'].values
colors = plt.cm.viridis([0.2, 0.6, 0.9])

fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(sizes, autopct='%1.1f%%', pctdistance=0.8, 
                                   startangle=90, colors=colors,
                                   wedgeprops=dict(width=0.4, edgecolor='w'))
```

**Output**: Donut chart showing percentage distribution of three flood event types

---

## Chart 2: Tendência de Eventos por Estação do Ano

**Source File**: [`temporal.py`](nbs/exploration/ocorrencias/temporal.py:438-518)

**Code Lines**: 438-518

**Chart Title**: "Tendência de Eventos por Estação do Ano"

**Data Processing**:
- **Input**: Preprocessed `ocorrencias` DataFrame
- **Season Assignment** (Lines 446-456):
  ```python
  def get_season(date):
      month = date.month
      if month in [12, 1, 2]: return 'Summer'
      elif month in [3, 4, 5]: return 'Autumn'
      elif month in [6, 7, 8]: return 'Winter'
      else: return 'Spring'
  ```
- **Aggregation** (Lines 467-485): Group by season-year label and count events
- **Chronological Ordering**: Events sorted by season_order timestamp

**Visualization Code**:
```python
# Lines 492-518
sns.lineplot(
    data=events_per_season,
    x='season_order',
    y='count',
    marker='o',
    markersize=6,
    linewidth=2,
    color='steelblue',
    ax=ax
)
```

**Output**: Line chart showing event trends across seasons over multiple years

---

## Chart 3: Tendência Média Mensal de Eventos com Variância

**Source File**: [`temporal.py`](nbs/exploration/ocorrencias/temporal.py:564-600)

**Code Lines**: 564-600

**Chart Title**: "Tendência Média Mensal de Eventos com Variância"

**Data Processing**:
- **Input**: Preprocessed `ocorrencias` DataFrame
- **Monthly Aggregation** (Lines 342-370):
  ```python
  # Extract year and month
  ocorrencias['year'] = ocorrencias['data_inicio'].dt.year
  ocorrencias['month'] = ocorrencias['data_inicio'].dt.month
  
  # Group by year and month
  monthly_counts = ocorrencias.groupby(['year', 'month']).size().reset_index(name='count')
  
  # Compute mean and std per month (across years)
  monthly_stats = monthly_counts.groupby('month')['count'].agg(['mean', 'std']).reset_index()
  monthly_stats['upper'] = monthly_stats['mean'] + monthly_stats['std']
  monthly_stats['lower'] = monthly_stats['mean'] - monthly_stats['std']
  ```

**Visualization Code**:
```python
# Lines 577-600
ax.plot(monthly_stats['month_name_pt'], monthly_stats['mean'],
        marker='o', linestyle='-', color='steelblue', label='Média de Eventos por Mês')

ax.fill_between(monthly_stats['month_name_pt'], monthly_stats['lower'], monthly_stats['upper'],
                color='steelblue', alpha=0.15, label='Variância (±1 desvio padrão)')
```

**Output**: Line chart with variance band showing average monthly event counts

---

## Chart 4: Tendência Média de Eventos por Semana do Ano

**Source File**: [`temporal.py`](nbs/exploration/ocorrencias/temporal.py:644-688)

**Code Lines**: 644-688

**Chart Title**: "Tendência Média de Eventos por Semana do Ano"

**Data Processing**:
- **Input**: Preprocessed `ocorrencias` DataFrame
- **Week Extraction** (Lines 655-661):
  ```python
  ocorrencias['week_of_year'] = ocorrencias['data_inicio'].dt.isocalendar().week
  events_per_week_avg = (
      ocorrencias.groupby('week_of_year')
      .size()
      .reset_index(name='count')
      .sort_values('week_of_year')
  )
  ```

**Visualization Code**:
```python
# Lines 666-688
sns.lineplot(
    data=events_per_week_avg,
    x='week_of_year',
    y='count',
    marker='o',
    markersize=5,
    linewidth=2,
    color='steelblue',
    ax=ax
)
```

**Output**: Line chart showing event counts aggregated by week of year (1-52/53)

---

## Chart 5: Análise Sazonal das Ocorrências de Inundação

**Source File**: [`temporal.py`](nbs/exploration/ocorrencias/temporal.py:763-834)

**Code Lines**: 763-834

**Chart Title**: "Análise Sazonal das Ocorrências de Inundação"

**Data Processing**:
- **Input**: Preprocessed `ocorrencias` DataFrame
- **Season Assignment** (Lines 772-781):
  ```python
  def get_season(date):
      month = date.month
      if month in [12, 1, 2]: return 'Summer'
      elif month in [3, 4, 5]: return 'Autumn'
      elif month in [6, 7, 8]: return 'Winter'
      else: return 'Spring'
  
  ocorrencias['season'] = ocorrencias['data_inicio'].apply(get_season)
  ```
- **Aggregation** (Lines 787-793): Count events per season with reindexing for consistent order

**Visualization Code**:
```python
# Lines 806-834
# Bar chart (ax1)
ax1.bar(events_per_season_sorted.index, events_per_season_sorted['count'], color=colors)

# Pie chart (ax2)
ax2.pie(events_per_season_sorted['count'], labels=events_per_season_sorted.index,
        autopct='%1.1f%%', pctdistance=0.8, startangle=90, colors=colors,
        wedgeprops=dict(width=0.4, edgecolor='w'))
```

**Output**: Combined bar chart and donut chart showing seasonal distribution

---

## Chart 6: Distribuição Horária dos Eventos

**Source File**: [`temporal.py`](nbs/exploration/ocorrencias/temporal.py:882-901)

**Code Lines**: 882-901

**Chart Title**: "Distribuição Horária dos Eventos"

**Data Processing**:
- **Input**: Preprocessed `ocorrencias` DataFrame
- **Hour Extraction** (Line 165): `ocorrencias['hour_start'] = ocorrencias['data_inicio'].dt.hour`
- **Aggregation** (Line 891): `hourly_distribution = ocorrencias['hour_start'].value_counts().sort_index()`

**Visualization Code**:
```python
# Lines 893-901
ax1 = sns.barplot(x=hourly_distribution.index, y=hourly_distribution.values, color='steelblue')
ax1.set_title('Distribuição Horária dos Eventos', fontsize=14, weight='bold')
ax1.set_xlabel('Hora do Dia', fontsize=12)
ax1.set_ylabel('Número de Eventos', fontsize=12)
```

**Output**: Bar chart showing event counts by hour of day (0-23)

---

## Chart 7: Distribuição Mensal dos Eventos

**Source File**: [`temporal.py`](nbs/exploration/ocorrencias/temporal.py:917-934)

**Code Lines**: 917-934

**Chart Title**: "Distribuição Mensal dos Eventos"

**Data Processing**:
- **Input**: Preprocessed `ocorrencias` DataFrame
- **Month Extraction** (Line 167): `ocorrencias['month'] = ocorrencias['data_inicio'].dt.month_name()`
- **Aggregation** (Lines 922-923):
  ```python
  monthly_distribution = ocorrencias['month'].value_counts().sort_index()
  monthly_distribution.index = month_order_en
  ```

**Visualization Code**:
```python
# Lines 925-934
ax3 = sns.barplot(x=meses_pt_full, y=monthly_distribution.values, color='steelblue')
ax3.set_title('Distribuição Mensal dos Eventos', fontsize=14, weight='bold')
ax3.set_xlabel('Mês', fontsize=12)
ax3.set_ylabel('Número de Eventos', fontsize=12)
```

**Output**: Bar chart showing event counts by month (January-December)

---

## Chart 8: Distribuição da Distância à Estação Pluviométrica Mais Próxima

**Status**: ⚠️ **Not Found in Provided Files**

This chart was not located in the three Python files analyzed (`preliminary.py`, `temporal.py`, `spatial.py`). It may be in a different notebook or script not yet converted to Python format.

**Suggested Search Locations**:
- Check for notebooks with "pluviometro" or "distance" in the filename
- Look in `nbs/exploration/alertario/` directory
- Search for spatial join operations with rain gauge station data

---

## Usage with AI Agents

To reference these charts in another AI agent chat, provide:

1. **File Path**: The relative path from project root (e.g., `nbs/exploration/ocorrencias/temporal.py`)
2. **Line Numbers**: The specific line range for the chart code
3. **Data Dependencies**: The preprocessing steps and data sources listed above
4. **Context**: This document as a reference for understanding the complete workflow

### Example Prompt Template:

```
I need to modify the "Tendência Média Mensal de Eventos com Variância" chart.
The code is in nbs/exploration/ocorrencias/temporal.py, lines 564-600.
The data processing logic is in lines 342-370 of the same file.
Please refer to docs/charts/charts-reference.md for full context.
```

---

## Notes

- All charts use matplotlib/seaborn with the `seaborn-v0_8-paper` style
- DPI is set to 300 for publication quality
- Portuguese labels are used for titles and axes
- Color palettes are chosen for colorblind accessibility where possible
- The project uses ISO 8601 datetime format internally

---

## Chart 24: API Alert Zones per Sub-bacia — Seasonal Thresholds (Fixed K=0.85)

**Source File**: [`scripts/charts/v1/chart_24_api_alert_zones_per_subbacia_fixed_k.py`](scripts/charts/v1/chart_24_api_alert_zones_per_subbacia_fixed_k.py)

**Output Directory**: `results/charts/v1/chart_24_api_alert_zones_per_subbacia_fixed_k/`

**Data Sources**:
- `data/processed/api_analysis_subbacia/api_analysis_events_subbacia.csv`
- `data/processed/api_analysis_subbacia/api_threshold_parameters_seasonal_fixed_k.csv`

**Description**: One figure per sub-bacia (2×5 grid, 10 time-steps). Each panel shows all events (EA and ESA) plotted against `api_5d` (5-day antecedent API, K=0.85 fixed). Four pairs of horizontal threshold lines (upper_tol and lower_tol) are drawn for each season in distinct colours. Provides an annual overview of how seasonal thresholds compare relative to the full event cloud.

---

## Chart 25: I-D Thresholds per Sub-bacia — Seasonal (Fixed K=0.85)

**Source File**: [`scripts/charts/v1/chart_25_api_id_thresholds_per_subbacia_fixed_k.py`](scripts/charts/v1/chart_25_api_id_thresholds_per_subbacia_fixed_k.py)

**Output Directory**: `results/charts/v1/chart_25_api_id_thresholds_per_subbacia_fixed_k/`

**Data Sources**:
- `data/processed/api_analysis_subbacia/api_analysis_events_subbacia.csv`
- `data/processed/api_analysis_subbacia/api_threshold_parameters_seasonal_fixed_k.csv`

**Description**: One figure per sub-bacia with 2 panels — (a) without tolerance levels and (b) with tolerance levels. EA/ESA events are shown as scatter in log-log intensity × duration space. Four coloured threshold line pairs (upper and lower) are overlaid for each season. Analogous to Chart 20 but adapted for the seasonal fixed-K methodology.

---

## Chart 26: Seasonal Threshold Summary — Fixed K=0.85

**Source File**: [`scripts/charts/v1/chart_26_seasonal_thresholds_fixed_k.py`](scripts/charts/v1/chart_26_seasonal_thresholds_fixed_k.py)

**Output Directory**: `results/charts/v1/chart_26_seasonal_thresholds_fixed_k/`

**Data Sources**:
- `data/processed/api_analysis_subbacia/api_threshold_parameters_seasonal_fixed_k.csv`
- `data/processed/api_analysis_subbacia/api_threshold_parameters_per_subbacia.csv` (annual reference)

**Description**: Single summary figure with three panels:
- **(a)** Bar chart of mean POD / FAR / Score by season, with annual reference dashed lines.
- **(b)** Box plot of lower_tol distribution by season and time-step (log scale), with annual mean line per duration.
- **(c)** Stacked bar of best antecedent days (1–10) distribution by season — replaces the K-distribution panel from Chart 21 since K is fixed.

Analogous to Chart 21 but for the fixed-K seasonal methodology.

---

## Chart 27: I-D Thresholds by Season per Sub-bacia — Fixed K=0.85

**Source File**: [`scripts/charts/v1/chart_27_seasonal_id_thresholds_per_subbacia_fixed_k.py`](scripts/charts/v1/chart_27_seasonal_id_thresholds_per_subbacia_fixed_k.py)

**Output Directory**: `results/charts/v1/chart_27_seasonal_id_thresholds_fixed_k/`

**Data Sources**:
- `data/processed/api_analysis_subbacia/api_analysis_events_subbacia.csv`
- `data/processed/api_analysis_subbacia/api_threshold_parameters_seasonal_fixed_k.csv`

**Description**: One figure per sub-bacia with 4 panels (one per season). Each panel shows EA/ESA scatter in log-log intensity × duration space, overlaid with upper_tol and lower_tol lines for that season. Structure is identical to Chart 22; only the parameter source changes.

---

## Chart 28: API Alert Zones by Season per Sub-bacia — Fixed K=0.85

**Source File**: [`scripts/charts/v1/chart_28_seasonal_alert_zones_per_subbacia_fixed_k.py`](scripts/charts/v1/chart_28_seasonal_alert_zones_per_subbacia_fixed_k.py)

**Output Directory**: `results/charts/v1/chart_28_seasonal_alert_zones_fixed_k/`

**Data Sources**:
- `data/processed/api_analysis_subbacia/api_analysis_events_subbacia.csv`
- `data/processed/api_analysis_subbacia/api_threshold_parameters_seasonal_fixed_k.csv`

**Description**: One large figure per sub-bacia with a 10×4 grid (rows = time-steps, columns = seasons). Each cell shows the API × intensity scatter for that season with four alert zones (red/orange/yellow/blue fills) and the fitted exponential curve I = a·exp(b·API) + c. API values are read directly from pre-computed `api_{n}d` columns in the events CSV (no K recomputation). Analogous to Chart 23 but uses fixed K=0.85 implicitly via the pre-computed columns.

---

## Last Updated

2026-06-08
