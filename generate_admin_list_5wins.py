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
            # Extract ROADVIEW_PRESETS array content
            match = re.search(r'const ROADVIEW_PRESETS = \[\s*(.*?)\s*\];', content, re.DOTALL)
            if match:
                preset_str = match.group(1)
                # Parse objects roughly
                # This is a bit hacky, but we just need names and addresses
                # lines like: { name: "...", addr: "...", ... },
                lines = preset_str.split('\n')
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith('//'): continue
                    
                    name_match = re.search(r'name:\s*"([^"]+)"', line)
                    addr_match = re.search(r'addr:\s*"([^"]+)"', line)
                    
                    if name_match and addr_match:
                        presets.append({
                            'name': name_match.group(1),
                            'addr': addr_match.group(1)
                        })
    except Exception as e:
        print(f"Error reading index.html: {e}")
    print(f"Loaded {len(presets)} presets from index.html")
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
    registered_keys = set()
    for p in presets:
        # We'll treat registered if normalized address matches
        registered_keys.add(normalize(p['addr']))
        # Also maybe name+addr?
    
    final_list = []
    for t in targets:
        t_key = normalize(t['address'])
        if t_key in registered_keys:
            continue
            
        # Double check fuzzy matching or substring?
        # For now, strict normalized address match.
        
        final_list.append(t)

    # Sort by wins desc
    final_list.sort(key=lambda x: x['wins'], reverse=True)
    
    print(f"Final targets count: {len(final_list)}")

    # 5. Write to admin_targets.js
    js_content = "const adminTargets = [\n"
    
    for shop in final_list:
        js_content += "  {\n"
        js_content += f'    "name": "{shop["name"]}",\n'
        js_content += f'    "address": "{shop["address"]}",\n'
        js_content += f'    "wins": {shop["wins"]},\n'
        js_content += f'    "lat": {shop["lat"] if shop["lat"] else "null"},\n'
        js_content += f'    "lng": {shop["lng"] if shop["lng"] else "null"}\n'
        js_content += "  },\n"
        
    js_content += "];\n"
    
    with open('admin_targets.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
        
    print("Successfully wrote admin_targets.js")

if __name__ == "__main__":
    main()
