
import json

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        lotto_data = json.load(f)
        
    shop_stats = {} 
    for item in lotto_data:
        addr = item.get('a', '').strip()
        name = item.get('n', '').strip()
        if not addr: continue
        
        if addr not in shop_stats:
            shop_stats[addr] = {
                "name": name, 
                "wins": 0, 
                "has_pov": False,
                "lat": item.get('lat'),
                "lng": item.get('lng'),
                "has_coords": item.get('lat') is not None
            }
        shop_stats[addr]["wins"] += 1
        if 'pov' in item:
            shop_stats[addr]["has_pov"] = True

    # Final list criteria:
    # 1. Exactly 4 wins and no POV
    # 2. Plus 'New Big Mart' (prioritized)
    missing_pov_shops = []
    for addr, info in shop_stats.items():
        # Include exactly 4 wins missing POV OR New Big Mart if still missing POV
        if (info['wins'] == 4 and not info['has_pov']) or (info['name'] == '뉴빅마트' and not info['has_pov']):
            missing_pov_shops.append({
                "name": info['name'],
                "address": addr,
                "wins": info['wins'],
                "lat": info['lat'],
                "lng": info['lng'],
                "has_coords": info['has_coords']
            })
            
    # Sort: New Big Mart first, then by name
    missing_pov_shops.sort(key=lambda x: (x['name'] != '뉴빅마트', x['name']))
    
    # 1. READ HTML
    with open('admin_pov.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 2. FIND MARKERS
    start_line = -1
    end_line = -1
    for i, line in enumerate(lines):
        if 'let allMissingShops = [' in line:
            start_line = i
        if start_line != -1 and '];' in line:
            end_line = i
            break
            
    if start_line != -1 and end_line != -1:
        # Re-generate the entire variable block
        new_block = f"        let allMissingShops = {json.dumps(missing_pov_shops, ensure_ascii=False, indent=4)};\n"
        new_lines = lines[:start_line] + [new_block] + lines[end_line+1:]
        
        with open('admin_pov.html', 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"✅ Recovery success: {len(missing_pov_shops)} shops restored to list.")
    else:
        print("❌ Error: Could not find markers in HTML.")

except Exception as e:
    print(f"Error: {e}")
