import json

with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Group by coordinates
coord_groups = {}
for entry in data:
    # Use rounded coords to catch slight variations?
    # No, the error was exact copy-paste of coords.
    key = f"{entry['lat']},{entry['lng']}"
    if key not in coord_groups:
        coord_groups[key] = set()
    coord_groups[key].add(entry['n'])

# Check for meaningful overlaps
print("=== Checking for Coordinate Collisions ===")
collisions_found = False
for key, names in coord_groups.items():
    if len(names) > 1:
        # Filter out minor variations (e.g. spacing differences)
        # Simple check: take first 2 chars
        prefixes = set(n[:2] for n in names)
        if len(prefixes) > 1:
            print(f"\nCoordinate: {key}")
            print(f"Stores: {names}")
            collisions_found = True

if not collisions_found:
    print("\nNo significant coordinate collisions found.")

# Verify World Cup Lottery
print("\n=== Verifying World Cup Lottery ===")
wc_entries = [d for d in data if '월드컵' in d['n'] and '복권방' in d['n']]
for entry in wc_entries:
    print(f"Name: {entry['n']}, Lat: {entry['lat']}, Lng: {entry['lng']}, Addr: {entry['a']}")
