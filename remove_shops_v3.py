import json

# Read top_shops_131.json
with open('top_shops_131.json', 'r', encoding='utf-8') as f:
    shops = json.load(f)

# Targets to remove
remove_targets = ['목화휴게소', '복권백화점']

# Filter out completed shops
filtered_shops = []
removed_count = 0

for shop in shops:
    should_remove = False
    for target in remove_targets:
        if target in shop['n']:
            should_remove = True
            break
    
    if should_remove:
        removed_count += 1
    else:
        filtered_shops.append(shop)

# Save back to file
with open('top_shops_131.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_shops, f, ensure_ascii=False, indent=2)

print(f"Removed {removed_count} shops")
print(f"Remaining shops: {len(filtered_shops)}")
