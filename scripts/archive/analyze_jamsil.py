import pandas as pd

# Read the Excel file
df = pd.read_excel('lotto_results_kinov.xlsx')

print("=== Column names ===")
print(df.columns.tolist())
print("\n=== Searching for '잠실매점' ===")

# Search for all variations of '잠실매점'
mask = df.iloc[:, 1].astype(str).str.contains('잠실', na=False)
jamsil_rows = df[mask]

print(f"\nFound {len(jamsil_rows)} rows containing '잠실':")
print("\n판매점명 unique values:")
print(jamsil_rows.iloc[:, 1].value_counts())

print("\n주소 unique values:")
print(jamsil_rows.iloc[:, 4].value_counts())

print("\n=== Sample rows ===")
print(jamsil_rows.head(20).to_string())

print("\n=== All unique 판매점명 containing '잠실매점' ===")
jamsil_maejeom_mask = df.iloc[:, 1].astype(str).str.contains('잠실매점', na=False)
print(df[jamsil_maejeom_mask].iloc[:, 1].unique())
print(f"\nTotal rows: {jamsil_maejeom_mask.sum()}")
