
import json
import shutil

def merge_data():
    # Backup first
    shutil.copy('lotto_data.json', 'lotto_data.json.bak')
    
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        main_data = json.load(f)
        
    with open('round_1210_geocoded.json', 'r', encoding='utf-8') as f:
        new_data = json.load(f)
        
    # Check if 1210 already exists to avoid duplicates (though it shouldn't)
    existing_1210 = any(x['r'] == 1210 for x in main_data)
    
    if existing_1210:
        print("Round 1210 already exists in data! Removing old entries first.")
        main_data = [x for x in main_data if x['r'] != 1210]
        
    # Append new data
    main_data.extend(new_data)
    
    # Sort by round descending, then name
    main_data.sort(key=lambda x: (-x['r'], x['n']))
    
    with open('lotto_data.json', 'w', encoding='utf-8') as f:
        json.dump(main_data, f, ensure_ascii=False, indent=2) # Use indent for readability
        
    print(f"Merged {len(new_data)} entries. Total records: {len(main_data)}")

if __name__ == "__main__":
    merge_data()
