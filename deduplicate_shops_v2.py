import json
import re
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

def normalize_string(s):
    if not s: return ""
    # Remove all whitespace
    s = s.replace(" ", "")
    # Remove common suffixes/prefixes to find "core" name
    s = re.sub(r'(복권방|복권판매점|복권|판매점|점|행운|나눔|로또|lotto|LOTTO)', '', s)
    return s

def get_addr_key(addr):
    if not addr: return ""
    parts = addr.split(" ")
    # Use City + District (e.g., 경기 수원시 -> 경기수원시)
    if len(parts) >= 2:
        return (parts[0] + parts[1]).replace(" ", "")
    return addr.replace(" ", "")

def main():
    data = load_data()
    print(f"Total entries before: {len(data)}")
    
    # Dictionary to hold the 'best' version of each shop
    # Key = NormalizedName + AddressKey
    unique_shops = {}
    duplicates_found = 0
    merged_shops = 0

    for idx, s in enumerate(data):
        name = s.get('n', '')
        addr = s.get('a', '')
        
        # Create a loose fingerprint for the shop
        norm_name = normalize_string(name)
        addr_key = get_addr_key(addr)
        
        # Fallback: if normalized name is empty (e.g. store named just "Lotto"), use original
        if not norm_name: norm_name = name.replace(" ", "")
        
        fingerprint = f"{norm_name}_{addr_key}"
        
        if fingerprint not in unique_shops:
            unique_shops[fingerprint] = s
        else:
            duplicates_found += 1
            existing = unique_shops[fingerprint]
            
            # --- MERGE LOGIC ---
            
            # 1. Prefer the one with POV/PanoID
            has_pov_existing = 'pov' in existing or 'panoid' in existing
            has_pov_current = 'pov' in s or 'panoid' in s
            
            # If current has POV but existing doesn't, swap them (keep current)
            if has_pov_current and not has_pov_existing:
                # But first, maximize 'wins' from existing
                s['wins'] = max(int(existing.get('wins', 0) or 0), int(s.get('wins', 0) or 0))
                # Update map
                unique_shops[fingerprint] = s
                print(f"[Merge] Replacing {existing['n']} with {s['n']} (Has POV)")
                merged_shops += 1
                continue
            
            # If both have POV, check who has specific 'pov' dict (not just panoid)
            if has_pov_current and has_pov_existing:
                 if 'pov' in s and 'pov' not in existing:
                     # Current is better populated
                     s['wins'] = max(int(existing.get('wins', 0) or 0), int(s.get('wins', 0) or 0))
                     unique_shops[fingerprint] = s
                     print(f"[Merge] Upgrading {existing['n']} to {s['n']} (Better POV data)")
                     merged_shops += 1
                     continue

            # Default: Keep 'existing', but merge data from 's'
            
            # Merge Wins
            existing['wins'] = max(int(existing.get('wins', 0) or 0), int(s.get('wins', 0) or 0))
            
            # Merge PanoID/POV if existing lacks it (safety net)
            if not has_pov_existing and has_pov_current:
                 existing['panoid'] = s.get('panoid')
                 existing['pov'] = s.get('pov')
            
            print(f"[Drop] Dropping duplicate {s['n']} (Merged into {existing['n']})")
            merged_shops += 1

    # Convert back to list
    cleaned_data = list(unique_shops.values())
    
    print("-" * 30)
    print(f"Total entries after: {len(cleaned_data)}")
    print(f"Duplicates removed: {len(data) - len(cleaned_data)}")
    
    save_data(cleaned_data)

if __name__ == "__main__":
    main()
