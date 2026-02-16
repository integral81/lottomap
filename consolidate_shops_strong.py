
import json
import re

def consolidate_shops_strong():
    print("Starting Strong Consolidation (Name + Region)...")
    
    json_path = 'lotto_data.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Helper to extract region
    def get_region_key(addr):
        # Split by space
        parts = addr.split()
        if len(parts) >= 2:
            # e.g. "경기 용인시 기흥구 ..." -> "경기 용인시 기흥구"
            # e.g. "서울 구로구 ..." -> "서울 구로구"
            # Take first 2 parts usually safely defines the district
            return f"{parts[0]} {parts[1]}"
        return "Unknown"

    # Group by (Name, Region)
    groups = {}
    
    for item in data:
        name = item['n']
        addr = item['a']
        
        region = get_region_key(addr)
        
        # Key: (Name, Region)
        # normalize name (remove spaces?)
        n_name = name.replace(" ", "")
        
        key = (n_name, region)
        
        if key not in groups:
            groups[key] = []
        groups[key].append(item)
        
    print(f"Identified {len(groups)} unique Name+Region groups.")
    
    merged_count = 0
    updated_records = []
    
    # Track stats
    multi_addr_groups = 0
    
    for key, items in groups.items():
        # Decide Master
        master_item = None
        
        # Prioritize:
        # 1. Has POV
        # 2. Road Address (guessing by pattern?) usually longer or standard?
        # Actually, if we have a POV, that address is likely the one we worked on (Road Name verified).
        
        candidates_with_pov = [i for i in items if i.get('pov')]
        
        if candidates_with_pov:
            # Pick the first one with POV as master
            master_item = candidates_with_pov[0]
        else:
            # No POV, just pick the first one matching "Road Name" pattern if possible?
            # Or just the first one.
            # Let's try to pick one that has 'lat'/'lng' if others don't
            candidates_with_coords = [i for i in items if i.get('lat')]
            if candidates_with_coords:
                master_item = candidates_with_coords[0]
            else:
                master_item = items[0]
                
        # Master Attributes
        m_name = master_item['n']
        m_addr = master_item['a']
        m_pov = master_item.get('pov')
        m_lat = master_item.get('lat')
        m_lng = master_item.get('lng')
        
        # Check if this group had disparate addresses
        unique_addrs = set(i['a'] for i in items)
        if len(unique_addrs) > 1:
            multi_addr_groups += 1
            # print(f"Merging addresses for {m_name}: {unique_addrs} -> {m_addr}")
            
        # Update ALL items
        for it in items:
            it['n'] = m_name
            it['a'] = m_addr # Unify Address
            
            if m_pov:
                it['pov'] = m_pov
            if m_lat:
                it['lat'] = m_lat
            if m_lng:
                it['lng'] = m_lng
                
            updated_records.append(it)
            
    # Save
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(updated_records, f, indent=2, ensure_ascii=False)
        
    print(f"Strong Consolidation Complete.")
    print(f"Merged {multi_addr_groups} groups that had fragmented addresses.")
    print(f"Total entries preserved: {len(updated_records)}")

if __name__ == "__main__":
    consolidate_shops_strong()
