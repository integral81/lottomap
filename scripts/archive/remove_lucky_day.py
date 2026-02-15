import json

# Read top_shops_131.json
with open('top_shops_131.json', 'r', encoding='utf-8') as f:
    shops = json.load(f)

# Identify target
target_name = "운좋은날"
target_addr_keyword = "강동구"

# Find candidates
candidates = [s for s in shops if target_name in s['n']]

print(f"Candidates found: {len(candidates)}")
for c in candidates:
    print(f"- {c['n']} ({c['a']}) - {c['w']} wins")

# Filter logic
filtered_shops = []
removed_shops = []

for shop in shops:
    if target_name in shop['n']:
        # If multiple candidates exist, check address
        if len(candidates) > 1:
            if target_addr_keyword in shop['a']:
                removed_shops.append(shop)
                continue
        else:
            # If only one or none, remove it (it must be the one)
            removed_shops.append(shop)
            continue
            
    filtered_shops.append(shop)

# Save back to file
with open('top_shops_131.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_shops, f, ensure_ascii=False, indent=2)

print(f"Removed {len(removed_shops)} shops")
print(f"Remaining shops: {len(filtered_shops)}")
