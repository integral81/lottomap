
import json
from collections import defaultdict

def generate_final_admin_list_aggregated():
    print("Generating admin_targets.js with prioritized list (Aggregated Wins & Strict Sort)...")
    
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Helper to extract region
    def get_region_key(addr):
        parts = addr.split()
        if len(parts) >= 2:
            return f"{parts[0]} {parts[1]}"
        return "Unknown"

    # Aggegate data by Shop
    shops = defaultdict(lambda: {
        "name": "", "address": "", "wins": 0, 
        "lat": 0, "lng": 0, "pov": None
    })
    
    for item in data:
        name = item['n']
        addr = item['a']
        
        # Group by Name + Region (Strong Grouping)
        region = get_region_key(addr)
        n_name = name.replace(" ", "")
        
        key = f"{n_name}|{region}"
        
        shop = shops[key]
        shop['name'] = name
        shop['address'] = addr
        shop['wins'] += 1
        
        # Keep the latest coords/pov if available
        if item.get('lat'): shop['lat'] = item['lat']
        if item.get('lng'): shop['lng'] = item['lng']
        if item.get('pov'): shop['pov'] = item['pov']

    # Lists
    top_priority = [] # Pinned
    general_list = [] # Sorted by wins
    
    # Sort all shops by wins descending first
    sorted_shops = sorted(shops.values(), key=lambda x: x['wins'], reverse=True)
    
    for item in sorted_shops:
        wins = item['wins']
        name = item['name']
        addr = item['address']
        lat = item['lat']
        lng = item['lng']
        has_pov = True if item.get('pov') else False
        
        # Skip if Recovered/Registered (Has POV) - check this FIRST
        if has_pov:
            continue
        
        # 1. Check Pinned (Gapanjeom Sindorim) - only if NOT registered
        is_pinned = False
        
        # Tolerance 0.001
        if 37.507 < lat < 37.509 and 126.890 < lng < 126.892:
             if "가판점" in name:
                 item['name'] = "★(1순위) " + item['name']
                 top_priority.append(item)
                 is_pinned = True
             
        if is_pinned:
            continue
            
        # 3. Filter Low Wins
        if wins < 5:
            continue

        # 4. Process General List
        # Highlight Special Names
        if "가판점" in name and "구로구" in addr:
            item['name'] = "★ " + item['name']
        elif "황금복권방" in name and "부산" in addr:
            item['name'] = "★ " + item['name']
        elif "로또휴게실" in name and "용인" in addr:
            item['name'] = "★ " + item['name']
            
        # Prepare Object
        obj = {
            "name": item['name'],
            "address": addr,
            "wins": wins,
            "lat": item['lat'],
            "lng": item['lng']
        }
        
        general_list.append(obj)
            
    # Combine: Top Priority + General Sorted
    final_list = top_priority + general_list
    
    # Write JS
    js_content = "const adminTargets = [\n"
    for item in final_list:
        # cleanup keys for JS
        clean_item = {
            "name": item.get('name'),
            "address": item.get('address'),
            "wins": item.get('wins'),
            "lat": item.get('lat'),
            "lng": item.get('lng')
        }
        if item.get('panoId'):
            clean_item['panoId'] = item['panoId']
        if item.get('pov'):
            clean_item['pov'] = item['pov']
            
        js_content += f"    {json.dumps(clean_item, ensure_ascii=False)},\n"
    js_content += "];"
    
    with open('admin_targets.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
        
    print(f"Total: {len(final_list)} (Pinned: {len(top_priority)}, General: {len(general_list)})")
    if top_priority:
        print(f"PINNED: {top_priority[0]['name']}")

if __name__ == "__main__":
    generate_final_admin_list_aggregated()
