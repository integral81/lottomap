import json

# Read top_shops_131.json
with open('top_shops_131.json', 'r', encoding='utf-8') as f:
    shops = json.load(f)

# Targets to remove
# Name-based removal
remove_targets = ['복권백화점', '영화유통', '종합복권슈퍼']

# Filter out completed shops
filtered_shops = []
removed_count = 0

for shop in shops:
    should_remove = False
    
    # Special handling for 복권백화점 to target only the Daegu one
    if '복권백화점' in shop['n']:
        if '대구' in shop['a'] and '달서구' in shop['a']:
            should_remove = True
    else:
        # Check other targets
        for target in remove_targets:
            if target != '복권백화점' and target in shop['n']:
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
