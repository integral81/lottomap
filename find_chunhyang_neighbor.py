import json
import math

def get_dist(lat1, lon1, lat2, lon2):
    R = 6371
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat/2) * math.sin(dLat/2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Group by name
shops = {}
for item in data:
    name = item.get('n')
    if not name: continue
    
    if name not in shops:
        shops[name] = {
            'name': name,
            'address': item.get('a', ''),
            'lat': float(item.get('lat', 0)),
            'lng': float(item.get('lng', 0)),
            'wins': 0,
            'pov': item.get('pov'),
            'hidden': item.get('hidden', False),
            'closed': item.get('closed', False)
        }
    shops[name]['wins'] += 1
    # If any entry is closed, mark aggregated as closed? 
    # The JS logic: if (item.closed) mapObj[item.n].closed = true;
    if item.get('closed'):
        shops[name]['closed'] = True

SEOUL_LAT = 37.5665
SEOUL_LNG = 126.9780

valid_list = []
for name, s in shops.items():
    # Simulate the condition BEFORE Chunhyang was registered
    # If name is "춘향로또", we force it to be included (treat as no POV)
    has_pov = s['pov'] and (s['pov'].get('id') or s['pov'].get('panoid'))
    
    if name == "춘향로또":
        has_pov = False # Force include for finding neighbor
        
    if s['wins'] == 3 and not s['hidden'] and not s['closed'] and not has_pov:
        dist = get_dist(SEOUL_LAT, SEOUL_LNG, s['lat'], s['lng'])
        s['dist'] = dist
        valid_list.append(s)

# Sort descending distance
valid_list.sort(key=lambda x: x['dist'], reverse=True)

# Find Chunhyang
for i, s in enumerate(valid_list):
    if s['name'] == "춘향로또":
        print(f"Update: Found '춘향로또' at index {i}")
        if i > 0:
            prev = valid_list[i-1]
            print(f"Previous (Above): {prev['name']}")
            print(f"Address: {prev['address']}")
        else:
            print("Chunhyang is at the top of the list.")
        
        if i < len(valid_list) - 1:
            next_s = valid_list[i+1]
            print(f"Next (Below): {next_s['name']}")
