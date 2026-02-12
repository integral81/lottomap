import json

# Read top_shops_131.json
with open('top_shops_131.json', 'r', encoding='utf-8') as f:
    shops = json.load(f)

# Find index of '하늘로또'
target_index = -1
for i, shop in enumerate(shops):
    if '하늘로또' in shop['n']:
        target_index = i
        break

if target_index == -1:
    print("Could not find '하늘로또'")
else:
    # Remove everything BEFORE target_index
    # shops[:target_index] -> items to remove
    # shops[target_index:] -> items to keep
    
    removed_items = shops[:target_index]
    kept_items = shops[target_index:]
    
    with open('top_shops_131.json', 'w', encoding='utf-8') as f:
        json.dump(kept_items, f, ensure_ascii=False, indent=2)
        
    print(f"Removed {len(removed_items)} items before '하늘로또'")
    print(f"Remaining items: {len(kept_items)}")
    
    for item in removed_items:
        print(f"Removed: {item['n']} ({item['a']})")
