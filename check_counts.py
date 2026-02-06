import pandas as pd
df = pd.read_excel('lotto_results_kinov.xlsx')
unique_count = len(df.groupby(['상호명', '소재지']))
print(f"Total rows: {len(df)}")
print(f"Unique shops: {unique_count}")

cache_df = pd.read_excel('geocoded_cache.xlsx')
print(f"Cache size: {len(cache_df)}")
