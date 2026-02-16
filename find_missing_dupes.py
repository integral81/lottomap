import json
import math
from collections import defaultdict

def haversine_distance(lat1, lng1, lat2, lng2):
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lng2 - lng1)
    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

# Load data
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Aggregate by shop
shop_data = defaultdict(lambda: {
    'name': '', 'address': '', 'wins': 0, 'lat': 0, 'lng': 0, 'pov': None
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

# Filter: 3+ wins, NO POV
missing_shops = []
for shop in shop_data.values():
    if shop['wins'] >= 3 and not shop['pov']:
        missing_shops.append(shop)

print(f"Missing shops (3+ wins, NO POV): {len(missing_shops)}")

# Group by name
name_groups = defaultdict(list)
for shop in missing_shops:
    name_groups[shop['name']].append(shop)

# Find duplicates within 1km
duplicates = []
for name, shops in name_groups.items():
    if len(shops) <= 1:
        continue
    
    for i, s1 in enumerate(shops):
        for j, s2 in enumerate(shops):
            if i >= j:
                continue
            
            if s1['lat'] == 0 or s2['lat'] == 0:
                continue
            
            dist = haversine_distance(s1['lat'], s1['lng'], s2['lat'], s2['lng'])
            
            if dist <= 1000:
                duplicates.append({
                    'name': name,
                    'addr1': s1['address'],
                    'addr2': s2['address'],
                    'wins1': s1['wins'],
                    'wins2': s2['wins'],
                    'distance_m': round(dist, 1)
                })

duplicates.sort(key=lambda x: x['distance_m'])

print(f"\nDuplicates found (1km): {len(duplicates)}")
print(f"Potential reduction: {len(missing_shops)} -> {len(missing_shops) - len(duplicates)}")
print(f"\nTop 20:")
for dup in duplicates[:20]:
    print(f"\n{dup['name']} - {dup['distance_m']}m")
    print(f"  {dup['addr1']} ({dup['wins1']} wins)")
    print(f"  {dup['addr2']} ({dup['wins2']} wins)")

# Save
with open('missing_duplicates.json', 'w', encoding='utf-8') as f:
    json.dump(duplicates, f, ensure_ascii=False, indent=2)

print(f"\nSaved to: missing_duplicates.json")
