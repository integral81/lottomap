import pandas as pd

# Load the data
df = pd.read_excel('lotto_results_kinov.xlsx')

# Display statistics
print(f"Total records: {len(df)}")
print(f"Round range: {df['회차'].min()} ~ {df['회차'].max()}")
print(f"\nUnique shops: {df['상호명'].nunique()}")
print(f"\nTop 10 records:")
print(df.head(10).to_string(index=False))

# Check for shops with multiple wins
shop_counts = df.groupby(['상호명', '소재지']).size().reset_index(name='당첨횟수')
multiple_wins = shop_counts[shop_counts['당첨횟수'] > 1].sort_values('당첨횟수', ascending=False)

print(f"\n\nShops with multiple 1st prize wins: {len(multiple_wins)}")
if len(multiple_wins) > 0:
    print("\nTop shops:")
    print(multiple_wins.head(10).to_string(index=False))
