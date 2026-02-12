import json

# Read top_shops_131.json
with open('top_shops_131.json', 'r', encoding='utf-8') as f:
    shops = json.load(f)

# Targets to remove
targets = ['다니엘사']

filtered_shops = []
removed_shops = []

for shop in shops:
    should_remove = False
    for target in targets:
        if target in shop['n']:
            should_remove = True
            break
            
    if should_remove:
        removed_shops.append(shop)
    else:
        filtered_shops.append(shop)

# Save back to file
with open('top_shops_131.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_shops, f, ensure_ascii=False, indent=2)

print(f"Removed {len(removed_shops)} shops")
print(f"Remaining shops: {len(filtered_shops)}")

for s in removed_shops:
    print(f"- {s['n']} ({s['a']})")
