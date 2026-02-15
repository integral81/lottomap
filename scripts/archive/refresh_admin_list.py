
import json

# Read admin_pov.html
with open('admin_pov.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Find the start and end of the allMissingShops list
start_marker = 'let allMissingShops = ['
end_marker = '];'

start_idx = html_content.find(start_marker)
if start_idx == -1:
    print("Could not find start marker")
    exit(1)

# Find the matching closing bracket
# We can't just find the next '];' because there might be nested arrays or strings containing it.
# But for this specific file structure, scanning for the next '];' AFTER the start should work if the list is well-formed.
# Let's try to parse the JSON content first.

# Extract the JSON array string
list_start = start_idx + len(start_marker)
list_end = html_content.find(end_marker, list_start)

if list_end == -1:
    print("Could not find end marker")
    exit(1)

json_str = html_content[list_start:list_end]

# Clean up trailing commas if any (JSON standard doesn't allow them, but JS does)
# Python json decoder is strict. 
# We might be better off loading the `shops_4wins_missing_pov.json` if we have it?
# Or we can just re-generate the list from `lotto_data.json` checking for `pov`.

# Better approach:
# 1. Load lotto_data.json
# 2. Filter for 4 wins AND missing 'pov'
# 3. Generate new list
# 4. Replace in HTML

# Let's reuse find_4wins_pov.py logic but adapted for update
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
                "has_coords": False
            }
        
        shop_stats[addr]["wins"] += 1
        if item.get('lat') and item.get('lng'):
             shop_stats[addr]["has_coords"] = True
             
        if 'pov' in item:
            shop_stats[addr]["has_pov"] = True

    # Filter 4+ wins and missing POV
    missing_pov_shops = []
    for addr, info in shop_stats.items():
        if info['wins'] >= 4 and not info['has_pov']:
            missing_pov_shops.append({
                "name": info['name'],
                "address": addr,
                "wins": info['wins'],
                "lat": info['lat'],
                "lng": info['lng'],
                "has_coords": info['has_coords']
            })
            
    # Sort by name, but keep '뉴빅마트' at top
    missing_pov_shops.sort(key=lambda x: (x['name'] != '뉴빅마트', x['name']))
    
    print(f"Found {len(missing_pov_shops)} shops missing POV.")
    
    # Generate JS string
    new_js_variable = f"let allMissingShops = {json.dumps(missing_pov_shops, ensure_ascii=False, indent=4)}"
    
    # Replace in HTML
    new_html_content = html_content[:start_idx] + new_js_variable + html_content[list_end+1:]
    
    with open('admin_pov.html', 'w', encoding='utf-8') as f:
        f.write(new_html_content)
        
    print("Updated admin_pov.html with clean list (New Big Mart prioritization applied).")

except Exception as e:
    print(f"Error: {e}")
