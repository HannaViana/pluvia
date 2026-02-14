# Chart 12: Intensity-Duration (I-D) Thresholds by Station

## Description
Individual scatter plots showing I-D points with fitted threshold curves. Each chart displays:
- **EA (red)**: Events with flooding
- **ESA (blue)**: Events without flooding  
- **Black line**: Fitted threshold curve following I = a × D^(-b)

## Purpose
- Visualize station-specific flood warning thresholds
- Show how well the threshold separates EA from ESA events
- Support operational flood prediction systems

## Threshold Model
**Power law equation**: I = a × D^(-b)

Where:
- **I** = Maximum intensity (mm/h)
- **D** = Duration (hours)
- **a, b** = Station-specific parameters fitted using logistic regression

## Files
33 individual PNG files, one per station:
- `station_01.png` through `station_33.png`
- Sorted by F1-score (best performing thresholds first)
- 6 stations have no valid threshold (only ESA or only EA events)

## Key Features
- **Log-log scale**: Visualizes power-law relationship
- **Threshold equation**: Shows fitted parameters (a, b)
- **Performance metrics**: Precision (P), Recall (R), F1-score
- **Confusion matrix**: TP, FP, FN, TN values in bottom-right
- **Layered display**: ESA background, EA foreground, threshold on top

## Best Performing Thresholds (by F1-score)
1. Station 32: F1=0.154 (a=0.153, b=-0.807)
2. Station 31: F1=0.086 (a=0.072, b=-0.748)
3. Station 29: F1=0.070 (a=0.061, b=-0.909)
4. Station 24: F1=0.068 (a=0.058, b=-0.708)
5. Station 18: F1=0.062 (a=0.054, b=-0.919)

## Interpretation
- **High Recall (R≈1.0)**: Thresholds capture nearly all EA events (good sensitivity)
- **Low Precision**: Many ESA events also exceed threshold (high false positive rate)
- **Low F1-scores**: Indicates significant overlap between EA and ESA in I-D space
- **Implication**: Flooding depends on factors beyond just intensity and duration

## Data Sources
- I-D points: `data/processed/id_analysis/pontos_id_df.csv`
- Fitted thresholds: `data/processed/id_analysis/threshold_parameters.csv`

## Quality Standards
- High resolution (300 DPI) for publication
- Consistent styling with scientific quality standards
- Clear annotations and performance metrics
- Professional color scheme
