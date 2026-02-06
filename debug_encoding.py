import pandas as pd
df = pd.read_excel('lotto_results_kinov.xlsx')
print("Column Names:", df.columns.tolist())
print("First 5 rows:")
print(df.head())
