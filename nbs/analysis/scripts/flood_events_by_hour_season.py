import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def get_season(date):
    month = date.month
    day = date.day

    if (month == 3 and day >= 20) or (month > 3 and month < 6) or (month == 6 and day < 21):
        return 'Autumn'
    elif (month == 6 and day >= 21) or (month > 6 and month < 9) or (month == 9 and day < 23):
        return 'Winter'
    elif (month == 9 and day >= 23) or (month > 9 and month < 12) or (month == 12 and day < 21):
        return 'Spring'
    else:
        return 'Summer'

def main():
    # Define paths
    ocorrencias_path = 'nbs/exploration/ocorrencias/ocorrencias_filtradas.csv'
    pops_path = 'data/raw/adm_cor_comando/pops.csv'
    output_chart_directory = 'nbs/analysis/charts/'
    chart_filename = 'flood_events_by_hour_season.png'
    output_chart_path = os.path.join(output_chart_directory, chart_filename)

    # Create output directory if it doesn't exist
    os.makedirs(output_chart_directory, exist_ok=True)

    # Load data
    ocorrencias = pd.read_csv(ocorrencias_path)
    pops = pd.read_csv(pops_path, index_col=0)

    # Process data
    ocorrencias['data_inicio'] = pd.to_datetime(ocorrencias['data_inicio'])
    ocorrencias['tipo'] = ocorrencias['id_pop'].map(pops.set_index('id')['titulo'])
    ocorrencias = ocorrencias[ocorrencias['tipo'].isin(["Bolsão d'água em via", 'Alagamento', 'Enchente', 'Alagamentos e enchentes'])]

    # Feature engineering
    ocorrencias['hour'] = ocorrencias['data_inicio'].dt.hour
    ocorrencias['season'] = ocorrencias['data_inicio'].apply(get_season)

    # Group and count
    events_by_hour_season = ocorrencias.groupby(['season', 'hour']).size().reset_index(name='event_count')

    # Create the chart
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(15, 8))

    sns.lineplot(data=events_by_hour_season, x='hour', y='event_count', hue='season', ax=ax, marker='o')

    ax.set_title('Count of Flood Events by Hour of the Day and Season', fontsize=16)
    ax.set_xlabel('Hour of the Day', fontsize=12)
    ax.set_ylabel('Count of Flood Events', fontsize=12)
    ax.set_xticks(range(0, 24))
    ax.legend(title='Season')
    plt.tight_layout()

    # Save the chart
    plt.savefig(output_chart_path)
    print(f"Chart saved to {output_chart_path}")

if __name__ == '__main__':
    main()