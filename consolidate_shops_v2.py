
import json
import re

def consolidate_shops_v2():
    print("Starting consolidation process V2...")
    
    json_path = 'lotto_data.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    print(f"Total records: {len(data)}")
    
    # helper
    def clean_addr(addr):
        # Remove (...) content
        base = re.sub(r'\s*\(.*?\)', '', addr).strip()
        # Also maybe remove postal codes if present? Usually not.
        return base

    # 1. Group by (Name, CleanAddress)
    groups = {}
    
    for item in data:
        name = item['n']
        raw_addr = item['a']
        c_addr = clean_addr(raw_addr)
        
        # Key: (Name, CleanAddress)
        key = (name, c_addr)
        
        if key not in groups:
            groups[key] = []
        groups[key].append(item)
        
    print(f"Unique Shop Groups found: {len(groups)}")
    
    # 2. Iterate groups and unify
    updated_records = []
    
    for key, items in groups.items():
        # key = (name, clean_addr)
        target_name = key[0]
        target_addr = key[1]
        
        # Find master data (coords/pov)
        master_pov = None
        master_lat = 0
        master_lng = 0
        
        # Check if any item has valid POV
        for it in items:
            if it.get('pov'):
                master_pov = it['pov']
            if it.get('lat'):
                master_lat = it['lat']
            if it.get('lng'):
                master_lng = it['lng']
                
        # Apply to all items in group
        for it in items:
            it['n'] = target_name
            it['a'] = target_addr # standardized
            
            if master_pov:
                it['pov'] = master_pov
            if master_lat:
                it['lat'] = master_lat
            if master_lng:
                it['lng'] = master_lng
                
            updated_records.append(it)
            
    # 3. Save
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(updated_records, f, indent=2, ensure_ascii=False)
        
    print("Consolidation V2 Complete. Saved to lotto_data.json")

if __name__ == "__main__":
    consolidate_shops_v2()
