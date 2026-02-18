import json
import os

f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
f_js = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'

def load_data():
    with open(f_json, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(f_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    with open(f_js, 'w', encoding='utf-8') as f:
        f.write('const lottoData = ' + json.dumps(data, ensure_ascii=False) + ';')

def main():
    data = load_data()
    original_count = len(data)
    
    # Target: 명당로또 (Icheon)
    target_name = "명당로또"
    target_addr_part = "청백리로84번길" # core part
    
    candidates = []
    for s in data:
        if target_name in s.get('n', '') and target_addr_part in s.get('a', ''):
            candidates.append(s)
            
    print(f"Found {len(candidates)} candidates for {target_name}")
    
    if len(candidates) > 1:
        # Keep the one with POV
        kept = None
        for c in candidates:
            if c.get('pov'):
                kept = c
                break
        
        if not kept:
            kept = candidates[0] # Default
            
        # Filter out others
        new_data = []
        removed = 0
        for s in data:
            if s in candidates and s != kept:
                print(f"Removing duplicate: {s['n']} (No POV or Duplicate)")
                removed += 1
            else:
                new_data.append(s)
        
        save_data(new_data)
        print(f"Fixed duplicates. Removed {removed} entries.")
    else:
        print("No duplicates found for this shop.")

if __name__ == "__main__":
    main()
