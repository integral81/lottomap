import json
import math

def get_dist(lat1, lon1, lat2, lon2):
    R = 6371
    # Check for invalid coords
    if not lat2 or not lon2: return 0
    try:
        lat1, lon1 = float(lat1), float(lon1)
        lat2, lon2 = float(lat2), float(lon2)
    except:
        return 0

    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat/2) * math.sin(dLat/2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

shops = {}
SEOUL_LAT = 37.5665
SEOUL_LNG = 126.9780

for item in data:
    name = item.get('n')
    if not name: continue
    
    # Check if 'lat' or 'lng' exist and are valid numbers
    lat = item.get('lat')
    lng = item.get('lng')
    if lat is None or lng is None: continue

    if name not in shops:
        shops[name] = {
            'name': name,
            'address': item.get('a', ''),
            'lat': lat,
            'lng': lng,
            'wins': 0,
            'pov': item.get('pov'),
            'hidden': item.get('hidden', False),
            'closed': item.get('closed', False)
        }
    
    shops[name]['wins'] += 1
    if item.get('closed'):
        shops[name]['closed'] = True

sorted_list = []
# Recreate admin_pov logic
for name, s in shops.items():
    # If Chunhyang Lotto, force show as if POV missing
    force_show = (name == "춘향로또") or (name == "복권판매소") # Also the other shop user mentioned, just in case
    
    # Check if pov exists (skip if it does, unless forced)
    # The logic in JS: !(s.pov && (s.pov.id || s.pov.panoid))
    has_pov = False
    if s.get('pov'):
        if isinstance(s['pov'], dict):
            if s['pov'].get('id') or s['pov'].get('panoid'):
                has_pov = True
    
    if force_show: has_pov = False

    if s['wins'] == 3 and not s['hidden'] and not s['closed'] and not has_pov:
        dist = get_dist(SEOUL_LAT, SEOUL_LNG, s['lat'], s['lng'])
        s['dist'] = dist
        sorted_list.append(s)

sorted_list.sort(key=lambda x: x['dist'], reverse=True)

found = False
for i, s in enumerate(sorted_list):
    if s['name'] == "춘향로또":
        print(f"Found '춘향로또' at index {i}")
        if i > 0:
            prev = sorted_list[i-1]
            print(f"Previous (Above): {prev['name']}")
            print(f"Address: {prev['address']}")
        else:
            print("Top of List")
        if i < len(sorted_list) - 1:
            next_s = sorted_list[i+1]
            print(f"Next (Below): {next_s['name']}")
        found = True
        break

if not found:
    print("Could not find '춘향로또' in the recreated list.")
