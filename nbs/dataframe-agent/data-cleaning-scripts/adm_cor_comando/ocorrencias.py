
'''
Thought: Convert 'data_inicio' and 'data_fim' to datetime objects and fill missing 'data_fim'.


'''

import pandas as pd
df['data_inicio'] = pd.to_datetime(df['data_inicio'])
df['data_fim'] = pd.to_datetime(df['data_fim'])
df['data_fim'] = df['data_fim'].fillna(df['data_inicio'] + pd.Timedelta(hours=1))
print(df[['data_inicio', 'data_fim']].head())



'''
Fill missing values in 'descricao', 'gravidade', 'tipo', and 'bairro'.


'''

df['descricao'] = df['descricao'].fillna('Sem descrição')
df['gravidade'] = df['gravidade'].fillna('Sem classificação')
df['tipo'] = df['tipo'].fillna('Sem tipo')
df['bairro'] = df['bairro'].fillna('Sem bairro')
print(df[['descricao', 'gravidade', 'tipo', 'bairro']].head())


'''
Fill invalid coordinates with NaN. Valid coordinates belong to the proper range (e.i. belong to Rio de Janeiro city).


'''

# Define approximate latitude/longitude boundaries for Rio de Janeiro
min_lat, max_lat = -23.05, -22.75
min_lon, max_lon = -43.7, -43.1

# Filter out invalid coordinates
df.loc[~df['latitude'].between(min_lat, max_lat) | ~df['longitude'].between(min_lon, max_lon), ['latitude', 'longitude']] = float('nan')

print(df[['latitude', 'longitude']].head())


'''
Create 'prazo_num' and clean 'prazo'.


'''

df['prazo_num'] = pd.to_numeric(df['prazo'], errors='coerce')
df['prazo'] = df['prazo'].apply(lambda x: x if x in ['Curto', 'Medio', 'Longo'] else 'Desconhecido')
print(df[['prazo', 'prazo_num']].head())
print(df['prazo'].unique())

