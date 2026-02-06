import pandas as pd
import json

def match_and_salvage():
    print("Attempting to salvage coordinates from previous corrupted run...")
    
    # 1. Load Healthy Excel
    df_healthy = pd.read_excel('temp_data.xlsx')
    # Column mapping
    df_healthy = df_healthy.rename(columns={
        df_healthy.columns[0]: 'r', # Round
        df_healthy.columns[2]: 'n', # Name
        df_healthy.columns[4]: 'a'  # Address
    })
    
    # Add a position index within each round
    df_healthy['pos'] = df_healthy.groupby('r').cumcount()

    # 2. Load Salvaged JSON (if it exists)
    try:
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            data_corrupt = json.load(f)
    except Exception as e:
        print(f"Could not load salvaged JSON: {e}")
        return

    # Convert corrupt data to DataFrame to easily add position
    df_corrupt = pd.DataFrame(data_corrupt)
    if df_corrupt.empty:
        print("Salvaged JSON is empty.")
        return
        
    df_corrupt['pos'] = df_corrupt.groupby('r').cumcount()
    
    # 3. Join by (Round, Position)
    # This assumes the order within each round is the same, which it should be.
    merged = pd.merge(df_healthy, df_corrupt[['r', 'pos', 'lat', 'lng']], on=['r', 'pos'], how='inner')
    
    print(f"Matched {len(merged)} records out of {len(df_healthy)} total records.")
    
    # 4. Extract into a healthy cache
    # Address -> (Lat, Lng)
    new_cache_data = []
    unique_matches = merged[['a', 'lat', 'lng']].drop_duplicates(subset=['a'])
    
    print(f"Found {len(unique_matches)} unique addresses with salvageable coordinates.")
    
    # 5. Save to geocoded_cache_healthy.xlsx
    # If file exists, merge with existing
    cache_path = 'geocoded_cache_healthy.xlsx'
    if pd.io.common.file_exists(cache_path):
        old_cache = pd.read_excel(cache_path)
        combined = pd.concat([old_cache, unique_matches], ignore_index=True).drop_duplicates(subset=['a'])
        combined.to_excel(cache_path, index=False)
        print(f"Updated healthy cache with salvaged data. Total: {len(combined)}")
    else:
        unique_matches.to_excel(cache_path, index=False)
        print(f"Created healthy cache with salvaged data. Total: {len(unique_matches)}")

if __name__ == "__main__":
    match_and_salvage()
