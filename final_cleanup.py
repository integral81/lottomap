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
    s = s.replace(" ", "")
    # Normalize common variations
    s = s.replace("점", "")
    s = s.replace("방", "")
    s = re.sub(r'(복권|로또|행운|나눔|LOTTO|lotto)', '', s, flags=re.IGNORECASE)
    return s

def get_addr_key(addr):
    if not addr: return ""
    parts = addr.split(" ")
    # Key: City + District + (Optional: Road Name core if available)
    # e.g. "경기 수원시 권선구 권선동" -> "경기수원시권선구"
    if len(parts) >= 2:
        base = (parts[0] + parts[1]).replace(" ", "")
        if len(parts) > 2:
             base += parts[2].replace(" ", "")
        return base
    return addr.replace(" ", "")

def main():
    data = load_data()
    print(f"Total entries before: {len(data)}")
    
    unique_shops = {}
    duplicates_found = 0
    merged_shops = 0

    for idx, s in enumerate(data):
        name = s.get('n', '')
        addr = s.get('a', '')
        
        norm_name = normalize_string(name)
        addr_key = get_addr_key(addr)
        
        if not norm_name: # Fallback for names like "Lotto" that get wiped
             norm_name = name.replace(" ", "")

        fingerprint = f"{norm_name}_{addr_key}"
        
        if fingerprint not in unique_shops:
            unique_shops[fingerprint] = s
        else:
            duplicates_found += 1
            existing = unique_shops[fingerprint]
            
            # --- MERGE LOGIC ---
            has_pov_existing = ('pov' in existing and existing['pov']) or ('panoid' in existing and existing['panoid'])
            has_pov_current = ('pov' in s and s['pov']) or ('panoid' in s and s['panoid'])
            
            # 1. Prefer POV
            if has_pov_current and not has_pov_existing:
                # Keep Current (it has POV)
                # Transfer Max Wins
                s['wins'] = max(int(existing.get('wins', 0) or 0), int(s.get('wins', 0) or 0))
                unique_shops[fingerprint] = s
                print(f"[Merge] Replacing {existing['n']} with {s['n']} (Newer has POV)")
                merged_shops += 1
            
            elif has_pov_current and has_pov_existing:
                # Both have POV? Keep the one with more specific POV data keys
                # Or simply keep existing to be stable, but merge wins
                existing['wins'] = max(int(existing.get('wins', 0) or 0), int(s.get('wins', 0) or 0))
                # If current has 'tilt/zoom' and existing doesn't, upgrade?
                print(f"[Merge] Merging duplicate POVs {s['n']} into {existing['n']}")
                merged_shops += 1
            
            else:
                # Neither has POV, or Only Existing has POV
                # Keep Existing, merge wins
                existing['wins'] = max(int(existing.get('wins', 0) or 0), int(s.get('wins', 0) or 0))
                print(f"[Drop] Dropping duplicate {s['n']} (Kept {existing['n']})")
                merged_shops += 1

    cleaned_data = list(unique_shops.values())
    
    print("-" * 30)
    print(f"Total entries after: {len(cleaned_data)}")
    print(f"Duplicates removed: {len(data) - len(cleaned_data)}")
    
    save_data(cleaned_data)

if __name__ == "__main__":
    main()
