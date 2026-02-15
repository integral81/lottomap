import pandas as pd

# Read the Excel file
df = pd.read_excel('lotto_results_kinov.xlsx')

# Print column names to see what we have
print("Column names:")
print(df.columns.tolist())
print("\nFirst few rows:")
print(df.head())
