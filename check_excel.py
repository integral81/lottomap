import pandas as pd

df = pd.read_excel('lotto_results_kinov.xlsx')
print(f'Total records: {len(df)}')
print(f'Round range: {df["회차"].min()} ~ {df["회차"].max()}')
print('\nFirst 10 rows:')
print(df.head(10))
print('\nLast 10 rows:')
print(df.tail(10))
