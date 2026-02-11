# Chart 11: Intensity-Duration (I-D) Analysis by Station

## Description
Individual scatter plots showing the relationship between rainfall duration and maximum intensity for each rain gauge station. Points are classified as:
- **EA (red)**: Events associated with flooding
- **ESA (blue)**: Events without flooding

## Purpose
- Visualize the intensity-duration relationship for different time windows (15min, 30min, 1h, 2h, 3h, 12h)
- Identify patterns that differentiate flooding events from non-flooding events
- Support the development of station-specific I-D thresholds for flood warnings

## Files
33 individual PNG files, one per station:
- `station_01.png` through `station_33.png`
- Files are named with zero-padded station IDs for proper sorting
- Stations are ordered by number of EA events (descending)

## Key Features
- **Log-log scale**: Both axes use logarithmic scale to better visualize the power-law relationship
- **Layered display**: ESA points plotted first (background), EA points on top (foreground) for emphasis
- **Event counts**: Legend shows sample sizes for EA and ESA classifications
- **Statistics box**: Bottom-left shows total EA/ESA event counts for the station

## Station Rankings (by EA events)
Top 5 stations with most flooding events:
1. Station 32: 39 EA events
2. Station 31: 24 EA events
3. Station 28: 22 EA events
4. Station 24: 19 EA events
5. Station 29: 15 EA events

## Data Source
Generated from: `data/processed/id_analysis/`
- `pontos_id_df.csv`: I-D points with classifications
- `classification_summary.csv`: Event counts by station

## Quality Standards
- High resolution (300 DPI) for publication
- Consistent color scheme across all charts
- Clear labels and annotations
- Professional scientific styling
