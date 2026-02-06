import pandas as pd
import json
from pathlib import Path

INPUT_FILE = "lotto_results_kinov_cleaned.csv"
CACHE_FILE = "geocoded_cache.xlsx"
OUTPUT_JSON = "lotto_data.json"

def main():
    print("Repairing/Re-exporting data...")
    
    # Try reading cache
    try:
        cache_df = pd.read_excel(CACHE_FILE)
        cache = {row['소재지']: (row['lat'], row['lon']) for _, row in cache_df.iterrows()}
        print(f"Loaded {len(cache)} cached locations.")
    except Exception as e:
        print(f"Failed to load cache: {e}")
        return

    # Load Source
    try:
        df = pd.read_csv(INPUT_FILE, encoding='utf-8')
    except:
        df = pd.read_csv(INPUT_FILE, encoding='cp949')

    # Normalize columns
    col_map = {
        df.columns[0]: '회차',
        df.columns[2]: '상호명',
        df.columns[3]: '당첨방식',
        df.columns[4]: '소재지'
    }
    df = df.rename(columns=col_map)
    
    json_data = []
    found_count = 0
    for _, row in df.iterrows():
        addr = row['소재지']
        if addr in cache:
            lat, lon = cache[addr]
            json_data.append({
                'r': int(row['회차']),
                'n': row['상호명'],
                'a': row['소재지'],
                'm': row['당첨방식'],
                'lat': lat,
                'lng': lon
            })
            found_count += 1
            
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
        
    print(f"Repair complete. Exported {len(json_data)} records to {OUTPUT_JSON}.")
    print(f"Successful geocoding for {found_count} out of {len(df)} total records.")

if __name__ == "__main__":
    main()
