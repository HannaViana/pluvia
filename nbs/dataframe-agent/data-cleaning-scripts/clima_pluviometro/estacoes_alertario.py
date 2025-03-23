
'''
Thought: First, I need to inspect the dataframe to identify completely empty columns.

'''

df.isna().all()

'''
The columns 'data_inicio_operacao', 'data_fim_operacao', and 'data_atualizacao' are completely empty. I will drop them.

'''

df.drop(columns=['data_inicio_operacao', 'data_fim_operacao', 'data_atualizacao'], inplace=True)

'''
Now I will check for unusual representations of missing values in each column using the `unique` method.

'''

for col in df.columns:
    print(f"Column {col}: {df[col].unique()}")

'''
The columns 'latitude', 'longitude', 'cota', 'x', 'y', and 'endereco' contain NaN values, which is the expected notation. No unusual representations of missing values were found. The data is clean. Now I will save the cleaned dataframe.

'''

import os
os.makedirs('../../data/clean/clima_pluviometro', exist_ok=True)
df.to_csv('../../data/clean/clima_pluviometro/estacoes_alertario.csv', index=False)
