
import json
from collections import defaultdict

def generate_final_admin_list():
    print("Generating admin_targets.js... (Excluding ALL shops with POV)")
    
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # First, aggregate by shop (name + address)
    shop_data = defaultdict(lambda: {
        'name': '',
        'address': '',
        'wins': 0,
        'lat': 0,
        'lng': 0,
        'pov': None,
        'rounds': []
    })
    
    for item in data:
        name = item['n']
        addr = item['a']
        key = f"{name}|{addr}"
        
        # Aggregate
        shop_data[key]['name'] = name
        shop_data[key]['address'] = addr
        shop_data[key]['wins'] += 1
        shop_data[key]['lat'] = item.get('lat', 0)
        shop_data[key]['lng'] = item.get('lng', 0)
        shop_data[key]['rounds'].append(item.get('r', 0))
        
        # Keep POV if exists
        if item.get('pov') and item['pov'].get('id') != 'N/A':
            shop_data[key]['pov'] = item['pov']
            
    # Categories
    gapan = []
    golden = []
    rest = []
    missing = []
    
    excluded_count = 0
    
    for key, shop in shop_data.items():
        # Filter: Only 3+ wins
        if shop['wins'] < 3:
            continue
            
        # CRITICAL: Exclude if POV exists
        if shop['pov']:
            excluded_count += 1
            continue
        
        # Construct target object
        obj = {
            "name": shop['name'],
            "address": shop['address'],
            "wins": shop['wins'],
            "lat": shop['lat'],
            "lng": shop['lng']
        }
        
        # Classification
        if "가판점" in shop['name'] and "구로구" in shop['address']:
            gapan.append(obj)
        elif "황금복권방" in shop['name'] and "부산" in shop['address']:
            golden.append(obj)
        elif "로또휴게실" in shop['name'] and "용인" in shop['address']:
            rest.append(obj)
        else:
            missing.append(obj)
            
    # Sort missing by wins (descending), then group by same shop name
    def sort_and_group_by_name(items):
        if not items:
            return []
        sorted_items = sorted(items, key=lambda x: x.get('wins', 0), reverse=True)
        result = []
        processed = set()
        for item in sorted_items:
            if id(item) in processed: continue
            result.append(item)
            processed.add(id(item))
            current_name = item['name']
            for other in sorted_items:
                if id(other) in processed: continue
                if other['name'] == current_name:
                    result.append(other)
                    processed.add(id(other))
        return result
    
    missing = sort_and_group_by_name(missing)
    
    # Combine
    final_list = gapan + golden + rest + missing
    
    # Write JS
    js_content = "const adminTargets = [\n"
    for item in final_list:
        js_content += f"    {json.dumps(item, ensure_ascii=False)},\n"
    js_content += "];"
    
    with open('admin_targets.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
        
    print(f"Total Pending: {len(final_list)} (Gapan: {len(gapan)}, Golden: {len(golden)}, Rest: {len(rest)}, Missing: {len(missing)})")
    print(f"Excluded (Already Completed): {excluded_count}")

if __name__ == "__main__":
    generate_final_admin_list()
