
'''
Thought: First, I'll inspect the dataframe's info and head to understand its structure and identify potential issues.

'''

print(df.info())
print(df.head())


'''
`data_fim_operacao` has many missing values, but it's not entirely empty, so I won't drop it. I'll check for unique values in each column to see if there are any unusual representations of missing values.

'''

for col in df.columns:
    print(f"Unique values in {col}: {df[col].unique()}")


'''
The unique values check confirms that missing values are represented as `NaN`. Now I will convert the date columns to datetime objects.

'''

df['data_inicio_operacao'] = pd.to_datetime(df['data_inicio_operacao'])
df['data_fim_operacao'] = pd.to_datetime(df['data_fim_operacao'])
df['data_atualizacao'] = pd.to_datetime(df['data_atualizacao'])
print(df.dtypes)


'''
I forgot to import pandas. I'll do that and retry the previous action.

'''

import pandas as pd
df['data_inicio_operacao'] = pd.to_datetime(df['data_inicio_operacao'])
df['data_fim_operacao'] = pd.to_datetime(df['data_fim_operacao'])
df['data_atualizacao'] = pd.to_datetime(df['data_atualizacao'])
print(df.dtypes)


'''
The data types are now correct. I will save the cleaned dataframe.

'''

import os
os.makedirs('../../data/clean/clima_estacao_meteorologica', exist_ok=True)
df.to_csv('../../data/clean/clima_estacao_meteorologica/estacoes_inmet.csv', index=False)

