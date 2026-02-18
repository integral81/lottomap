import json
import os
import re

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

def normalize_name(name):
    # Remove spaces and common suffixes for better matching
    name = name.replace(' ', '')
    name = re.sub(r'(복권방|복권판매점|판매점|복권)$', '', name)
    return name

def main():
    data = load_data()
    original_count = len(data)
    
    # Strategy: Group by "Normalized Name + City/Gu"
    # If duplicates found:
    # 1. Keep the one WITH POV.
    # 2. If multiple have POV, keep the one with recent update or ID (not easily trackable, so keep with most info)
    # 3. If none have POV, keep the one with most wins (if available) or first found.
    # 4. Merge details (if one has 'wins' and other doesn't)

    unique_shops = {}
    duplicates_removed = 0
    
    for s in data:
        # Create a unique key
        name_key = normalize_name(s.get('n', ''))
        addr_parts = s.get('a', '').split(' ')
        addr_key = "".join(addr_parts[:2]) if len(addr_parts) >= 2 else s.get('a', '') # City + Gu
        
        unique_id = f"{name_key}_{addr_key}"
        
        if unique_id not in unique_shops:
            unique_shops[unique_id] = s
        else:
            existing = unique_shops[unique_id]
            
            # Decide which to keep
            keep_existing = True
            
            # Criteria 1: POV existence
            if not existing.get('pov') and s.get('pov'):
                keep_existing = False # Swap to new because it has POV
            elif existing.get('pov') and not s.get('pov'):
                keep_existing = True
            
            # Criteria 2: PanoID existence (stronger than generic POV)
            elif not existing.get('panoid') and s.get('panoid'):
                keep_existing = False
            
            # Merge Logic (Wins)
            total_wins = max(existing.get('wins', 0), s.get('wins', 0)) # Simple max
            
            if keep_existing:
                existing['wins'] = total_wins
                # Merge pano if missing
                if not existing.get('panoid') and s.get('panoid'):
                    existing['panoid'] = s['panoid']
                    existing['pov'] = s['pov']
                print(f"Removing Duplicate: {s['n']} ({s['a']}) -> Keeping {existing['n']}")
            else:
                s['wins'] = total_wins
                # Merge pano if missing (from existing)
                if not s.get('panoid') and existing.get('panoid'):
                    s['panoid'] = existing['panoid']
                    s['pov'] = existing['pov']
                
                print(f"Removing Duplicate: {existing['n']} ({existing['a']}) -> Keeping {s['n']}")
                unique_shops[unique_id] = s
            
            duplicates_removed += 1

    new_data = list(unique_shops.values())
    
    print(f"Original: {original_count}")
    print(f"New: {len(new_data)}")
    print(f"Removed: {duplicates_removed}")
    
    if duplicates_removed > 0:
        save_data(new_data)
        print("Cleanup Saved.")
    else:
        print("No duplicates found with current strict logic.")

if __name__ == "__main__":
    main()
