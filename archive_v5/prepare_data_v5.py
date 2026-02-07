import pandas as pd
import json
from pathlib import Path

# --- CONFIGURATION ---
INPUT_FILE = "temp_data.xlsx" 
OUTPUT_JSON = "lotto_data.json"
CACHE_FILE = "geocoded_cache_healthy.xlsx" 

def main():
    print("Regenerating lotto data with strict JSON compliance (NaN fix)...")
    
    # 1. Load Data
    df = pd.read_excel(INPUT_FILE)
    
    # Map columns correctly
    df = df.rename(columns={
        df.columns[0]: 'r', # Round
        df.columns[2]: 'n', # Name
        df.columns[3]: 'm', # Method
        df.columns[4]: 'a'  # Address
    })
    
    # Fill NaN values with empty strings to avoid invalid JSON output
    df = df.fillna('')
    
    # 2. Load Cache
    cache = {}
    if Path(CACHE_FILE).exists():
        cache_df = pd.read_excel(CACHE_FILE)
        # Ensure cache also doesn't have NaNs for lat/lng (though they shouldn't)
        cache_df = cache_df.dropna(subset=['lat', 'lng'])
        cache = {row['a']: (row['lat'], row['lng']) for _, row in cache_df.iterrows()}
        print(f"Loaded {len(cache)} cached locations.")

    # 3. Build Final JSON
    json_data = []
    skipped = 0
    for _, row in df.iterrows():
        addr = row['a']
        if addr in cache:
            lat, lng = cache[addr]
            json_data.append({
                'r': int(row['r']),
                'n': str(row['n']),
                'a': str(row['a']),
                'm': str(row['m']),
                'lat': float(lat),
                'lng': float(lng)
            })
        else:
            skipped += 1
            
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        # allow_nan=False ensures we catch any remaining NaNs immediately
        json.dump(json_data, f, ensure_ascii=False, indent=2, allow_nan=False)
    
    print(f"Success! Exported {len(json_data)} records to {OUTPUT_JSON}")
    if skipped > 0:
        print(f"Warning: Skipped {skipped} records due to missing geocodes.")

if __name__ == "__main__":
    main()
