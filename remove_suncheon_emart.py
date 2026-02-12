import json

# Read top_shops_131.json
with open('top_shops_131.json', 'r', encoding='utf-8') as f:
    shops = json.load(f)

# Targets to remove: "이마트24 순천산단점" or similar
# Filter by "순천" and check address

filtered_shops = []
removed_shops = []

for shop in shops:
    # Check if "순천" is in address and ("이마트" in name or "알리바이" in name?)
    # Let's be broad first and print what we remove
    if '순천' in shop['a'] and ('이마트' in shop['n'] or '산단' in shop['a']):
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
