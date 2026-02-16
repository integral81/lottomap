import json
from collections import defaultdict

def generate_final_admin_list():
    print("Generating admin_targets.js with PRIORITY...")
    
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Aggregate data
    shop_data = defaultdict(lambda: {
        'name': '', 'address': '', 'wins': 0, 'lat': 0, 'lng': 0, 'pov': None, 'rounds': []
    })
    
    for item in data:
        key = f"{item['n']}|{item['a']}"
        shop_data[key]['name'] = item['n']
        shop_data[key]['address'] = item['a']
        shop_data[key]['wins'] += 1
        shop_data[key]['lat'] = item.get('lat', 0)
        shop_data[key]['lng'] = item.get('lng', 0)
        if item.get('pov') and item['pov'].get('id') != 'N/A':
            shop_data[key]['pov'] = item['pov']

    # Filter targets (3+ wins, No POV)
    all_targets = []
    
    for shop in shop_data.values():
        if shop['wins'] < 3: continue
        if shop['pov']: continue
        
        all_targets.append({
            "name": shop['name'],
            "address": shop['address'],
            "wins": shop['wins'],
            "lat": shop['lat'],
            "lng": shop['lng']
        })

    # --- Priority Handling ---
    priority_list = []
    regular_list = []
    
    for t in all_targets:
        is_paju_nodaji = '파주시 문산읍' in t['address'] and '노다지' in t['name']
        is_osan_nodaji = '오산시 오산로' in t['address'] and '노다지' in t['name'] # Using new address
        # Also check old address just in case
        is_osan_nodaji_old = '오산동 394' in t['address'] and '노다지' in t['name']
        
        if is_paju_nodaji or is_osan_nodaji or is_osan_nodaji_old:
            # t['name'] = f"★ {t['name']}" # User requested REMOVAL of stars
            priority_list.append(t)
        else:
            regular_list.append(t)
            
    # Sort Regular List by Wins
    regular_list.sort(key=lambda x: x['wins'], reverse=True)
    
    # Combine: Priority FIRST
    combined_list = priority_list + regular_list
    
    # Apply exclusion logic
    EXCLUDE_ADDRS = ["세종로475번길 2"] # Yeoju Sky Lotto (Active but Roadview invisible - User requested removal from admin)
    
    final_list = []
    for shop in combined_list:
        is_excluded = False
        for ex_addr in EXCLUDE_ADDRS:
            if ex_addr in shop['address']:
                is_excluded = True
                break
        
        if not is_excluded:
            final_list.append(shop)
    
    # Write to File
    js_content = "const adminTargets = " + json.dumps(final_list, ensure_ascii=False, indent=2) + ";"
    with open('admin_targets.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
        
    print(f"Generated {len(final_list)} targets.")
    print(f"Priority Targets: {len(priority_list)}")
    for p in priority_list:
        print(f" - {p['name']} ({p['address']})")

if __name__ == "__main__":
    generate_final_admin_list()
