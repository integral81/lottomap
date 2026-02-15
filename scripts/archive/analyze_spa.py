import json

# Read lotto_data.json
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find all '스파' entries
spa_entries = [d for d in data if d['n'] == '스파']

print(f"Found {len(spa_entries)} entries with name '스파'")
print("\nGrouping by coordinates:")

# Group by coordinates
coords_map = {}
for entry in spa_entries:
    coord_key = f"{entry['lat']},{entry['lng']}"
    if coord_key not in coords_map:
        coords_map[coord_key] = {
            'lat': entry['lat'],
            'lng': entry['lng'],
            'addr': entry['a'],
            'rounds': []
        }
    coords_map[coord_key]['rounds'].append(entry['r'])

print(f"\nUnique coordinate sets: {len(coords_map)}")
for i, (coord_key, info) in enumerate(coords_map.items(), 1):
    print(f"\n{i}. Coordinates: {coord_key}")
    print(f"   Address: {info['addr']}")
    print(f"   Rounds: {info['rounds']} (count: {len(info['rounds'])})")
