import pandas as pd
import json
import os

HISTORIC_FILE = "lotto_historic_numbers_1_1209_Final.xlsx"
OUTPUT_JSON = "lotto_history.json"

def build_json():
    if not os.path.exists(HISTORIC_FILE):
        print(f"Error: {HISTORIC_FILE} not found.")
        return

    try:
        df = pd.read_excel(HISTORIC_FILE)
        
        # Structure: { "1210": [1, 2, 3, 4, 5, 6], ... }
        history_map = {}
        
        for _, row in df.iterrows():
            round_num = int(row['회차'])
            # Assuming columns like 번호1, 번호2... match the file structure
            numbers = [
                int(row['번호1']), int(row['번호2']), int(row['번호3']), 
                int(row['번호4']), int(row['번호5']), int(row['번호6'])
            ]
            history_map[str(round_num)] = numbers
            
        with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
            json.dump(history_map, f, ensure_ascii=False, indent=None) # Minified for web
            
        print(f"Successfully created {OUTPUT_JSON} with {len(history_map)} rounds.")
        
    except Exception as e:
        print(f"Error building JSON: {e}")

if __name__ == "__main__":
    build_json()
