import json

# Read lotto_data.json
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Calculate win counts for all shops
win_counts = {}
shop_info = {} # Key: "Name|Address", Value: {lat, lng, name, address}

for entry in data:
    key = f"{entry['n']}|{entry['a']}"
    if key not in win_counts:
        win_counts[key] = 0
        shop_info[key] = entry
    win_counts[key] += 1

# Targets to check for restoration
target_names = ['행운복권방', '대박슈퍼']
# Exclude current work targets (already done)
exclude_keywords = ['포천', '인천', '강릉'] 
# Note: 진평양행 is unique (only Gangneung likely), but included in logic for safety

restored_shops = []

for key, count in win_counts.items():
    if count < 5:
        continue # Only interested in top shops
    
    name = shop_info[key]['n']
    address = shop_info[key]['a']
    
    # Check if this shop matches our target names
    is_target_name = False
    for target in target_names:
        if target in name:
            is_target_name = True
            break
            
    if not is_target_name:
        continue
        
    # Check if this is one of the excluded ones (already processed)
    is_excluded = False
    for keyword in exclude_keywords:
        if keyword in address:
            is_excluded = True
            break
            
    if is_excluded:
        print(f"Skipping (Already Processed): {name} ({address}) - {count} wins")
        continue

    # If we are here, it's a shop that was wrongly deleted!
    print(f"Restoring: {name} ({address}) - {count} wins")
    
    shop_obj = {
        "n": name,
        "a": address,
        "lat": shop_info[key]['lat'],
        "lng": shop_info[key]['lng'],
        "w": count
    }
    restored_shops.append(shop_obj)

# Add to top_shops_131.json
if restored_shops:
    with open('top_shops_131.json', 'r', encoding='utf-8') as f:
        top_shops = json.load(f)
        
    # Check if already exists to avoid duplication (just in case)
    current_keys = set([f"{s['n']}|{s['a']}" for s in top_shops])
    
    added_count = 0
    for shop in restored_shops:
        key = f"{shop['n']}|{shop['a']}"
        if key not in current_keys:
            top_shops.insert(0, shop)
            added_count += 1
            
    with open('top_shops_131.json', 'w', encoding='utf-8') as f:
        json.dump(top_shops, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully restored {added_count} shops.")
    print(f"Total shops in list: {len(top_shops)}")
else:
    print("No shops needed restoration.")
