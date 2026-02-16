import json
import re
import os

def normalize(text):
    if not text: return ""
    return re.sub(r'\s+', '', str(text)).strip()

def load_index_presets():
    presets = []
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Robust Parsing: Find all { name: "...", addr: "..." } patterns globally
            # This avoids issues with block capturing regex failing on comments or nested brackets
            matches = re.finditer(r'name:\s*"([^"]+)",\s*addr:\s*"([^"]+)"', content)
            
            for m in matches:
                name = m.group(1).strip()
                addr = m.group(2).strip()
                presets.append({'name': name, 'addr': addr})
                
    except Exception as e:
        print(f"Error reading index.html: {e}")
        
    print(f"Loaded {len(presets)} presets from index.html (Robust Parse)")
    return presets

def main():
    # 1. Load Lotto Data
    try:
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("lotto_data.json not found.")
        return

    # 2. Aggregate Wins
    shop_stats = {}
    
    for entry in data:
        name = entry.get('n', '').strip()
        addr = entry.get('a', '').strip()
        lat = entry.get('lat')
        lng = entry.get('lng')
        
        if not name or not addr: continue
        if "인터넷" in name or "동행복권" in addr: continue
        
        # Key by address implies unique shop usually, but names can change.
        # Let's use name+addr as key for now to be safe, or just addr?
        # Address is more stable.
        
        # Normalize address for key
        key = normalize(addr)
        
        if key not in shop_stats:
            shop_stats[key] = {
                'name': name,
                'address': addr,
                'wins': 0,
                'lat': lat,
                'lng': lng
            }
        
        shop_stats[key]['wins'] += 1
        # Update name if it changes? (Keep latest? Or most frequent? Just keep one)
        # Update lat/lng if missing
        if not shop_stats[key]['lat'] and lat:
            shop_stats[key]['lat'] = lat
            shop_stats[key]['lng'] = lng

    print(f"Total unique shops found: {len(shop_stats)}")

    # 3. Filter 5+ Wins
    targets = [s for s in shop_stats.values() if s['wins'] >= 5]
    print(f"Shops with 5+ wins: {len(targets)}")

    # 4. Exclude Registered
    presets = load_index_presets()
    registered_names = [p['name'] for p in presets]
    registered_addrs = [normalize(p['addr']) for p in presets]
    
    # 2. Filter for 4+ wins AND not in presets
    targets = []
    count_excluded_name = 0
    count_excluded_addr = 0
    
    print(f"Filtering against {len(registered_names)} registered shops...")
    
    for k, v in shop_stats.items():
        if v['wins'] >= 4:
            t_name = v['name']
            t_addr = v['address']
        else:
            continue
            
        t_name_norm = normalize(t_name)
        t_addr_norm = normalize(t_addr)
        
        # 1. Name Match (Normalized Exact OR Partial)
        is_name_match = False
        
        for r_name in registered_names:
            r_name_norm = normalize(r_name)
            
            # Skip very short names for partial safety (but exact match is okay)
            if len(t_name_norm) <= 2 or len(r_name_norm) <= 2:
                if t_name_norm == r_name_norm:
                    is_name_match = True
                    break
                continue
            
            # Check contains relationship on normalized strings
            if t_name_norm in r_name_norm or r_name_norm in t_name_norm:
                is_name_match = True
                # print(f"Excluded by Name: {t_name} matches {r_name}")
                break
                
        if "세방매점" in t_name:
            print(f"DEBUG: Processing {t_name}")
            print(f"  is_name_match: {is_name_match}")
            if not is_name_match:
                 print("  Searching in registered_names:")
                 for r in registered_names:
                     if "세방" in r:
                         print(f"    - Found candidate: {r}")

        if is_name_match:
            count_excluded_name += 1
            print(f"EXCLUDED: {t_name}")
            continue
            
        # 2. Address Match (Loose)
        # Check if t_addr_norm is inside any registered_addr OR vice versa
        is_registered = False
        for r_addr in registered_addrs:
            if len(r_addr) < 5: continue # Skip too short addresses to avoid false positives
            if t_addr_norm in r_addr or r_addr in t_addr_norm:
                is_registered = True
                print(f"EXCLUDED (Addr): {t_name}")
                break
        
        if is_registered:
            count_excluded_addr += 1
            print(f"EXCLUDED (Addr): {t_name}")
            continue
            
        targets.append({
            'name': t_name,
            'address': t_addr,
            'wins': v['wins'],
            'lat': v['lat'],
            'lng': v['lng']
        })

    print(f"Excluded {count_excluded_name} by Name, {count_excluded_addr} by Address.")

    # Sort by wins desc
    targets.sort(key=lambda x: x['wins'], reverse=True)
    
    print(f"Final targets count (4+ wins): {len(targets)}")

    # 5. Write to admin_targets.js
    js_content = "const adminTargets = [\n"
    
    for t in targets:
        js_content += "  {\n"
        js_content += f'    "name": "{t["name"]}",\n'
        js_content += f'    "address": "{t["address"]}",\n'
        js_content += f'    "wins": {t["wins"]},\n'
        js_content += f'    "lat": {t["lat"] if t["lat"] else "null"},\n'
        js_content += f'    "lng": {t["lng"] if t["lng"] else "null"}\n'
        js_content += "  },\n"
        
    js_content += "];\n"
    
    with open('admin_targets.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
        
    print("Successfully wrote admin_targets.js")

if __name__ == "__main__":
    main()
