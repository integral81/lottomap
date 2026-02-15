import pandas as pd

# Read the Excel file
df = pd.read_excel('lotto_results_kinov.xlsx')

# Find rows with 잠실매점
mask = df['판매점명'].str.contains('잠실매점', na=False)

print(f'Found {mask.sum()} rows with 잠실매점')

if mask.sum() > 0:
    print("\nCurrent data:")
    print(df[mask][['판매점명', '주소', '위도', '경도']].iloc[0])
    
    # Update coordinates
    df.loc[mask, '위도'] = 37.5144273491608
    df.loc[mask, '경도'] = 127.100611434725
    
    # Save back to Excel
    df.to_excel('lotto_results_kinov.xlsx', index=False)
    
    print("\nUpdated coordinates to:")
    print("위도: 37.5144273491608")
    print("경도: 127.100611434725")
else:
    print("No rows found with 잠실매점")
