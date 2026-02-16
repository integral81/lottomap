
import json
import re

def consolidate_data():
    print("Starting consolidation process...")
    
    json_path = 'lotto_data.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    print(f"Original entries: {len(data)}")
    
    # helper to clean address for grouping
    def clean_addr(addr):
        # Remove (...) content which is usually legacy address
        # e.g., "용구대로 1885 (보라동 378-1)" -> "용구대로 1885"
        base = re.sub(r'\s*\(.*?\)', '', addr).strip()
        return base

    # Group by (Name, CleanAddress)
    # We use a dictionary where key = (name, clean_addr)
    # Value = list of items
    groups = {}
    
    for item in data:
        name = item['n']
        raw_addr = item['a']
        c_addr = clean_addr(raw_addr)
        
        # Key for consolidation
        key = (name, c_addr)
        
        if key not in groups:
            groups[key] = []
        groups[key].append(item)
        
    merged_data = []
    merged_count = 0
    
    for key, items in groups.items():
        if len(items) == 1:
            merged_data.append(items[0])
            continue
            
        # Multiple entries found! Merge them.
        merged_count += 1
        # print(f"Merging {len(items)} items for {key[0]}...")
        
        # 1. Base item (prefer the one with POV or the one with longest/most complete info?)
        # Strategy:
        # - Address: Use the CLEAN address (Road Name) as requested.
        # - Wins: Sum them up. (But wait, json doesn't have 'wins' count, it has rows.
        #   Actually, the JSON structure is List of Wins. 
        #   Wait, if `lotto_data.json` is a list of wins (round by round), we CANNOT merge them into one row 
        #   UNLESS this file is a summary file.
        #   Let's check the file content again.
        #   The grep output showed:
        #   { "n": "로또휴게실", "m": "자동", "a": "...", "r": 1211 ... }
        #   This defines a WIN. It is NOT a shop list. It is a WIN LIST.
        #   
        #   CRITICAL: If it's a win list, we just need to UNIFY THE ADDRESS/NAME Strings.
        #   We don't "merge rows" into one. We "standardize the columns" so that when we aggregate later, they group together.
        
        target_name = key[0]
        target_addr = key[1] # The clean road address
        
        # Find if any item has POV info. If so, apply to ALL.
        master_pov = None
        master_coords = None
        
        for it in items:
            if it.get('pov'):
                master_pov = it['pov']
            if it.get('lat') and it.get('lng'):
                master_coords = (it['lat'], it['lng'])
                
        # Update ALL items in this group to have the same Name/Address/POV
        for it in items:
            it['n'] = target_name
            it['a'] = target_addr # Standardize to Road Addr
            if master_pov:
                it['pov'] = master_pov
            if master_coords:
                it['lat'] = master_coords[0]
                it['lng'] = master_coords[1]
                
            merged_data.append(it)
            
    # Write back
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, indent=2, ensure_ascii=False)
        
    print(f"Consolidation complete. Standardized address for {merged_count} groups.")

if __name__ == "__main__":
    consolidate_data()
