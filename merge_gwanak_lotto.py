import json

# 1. Update lotto_data.json
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Unify to: Nambusunhwan-ro 1739-9
tgt_addr = "서울 관악구 남부순환로 1739-9"
tgt_lat = 37.4828013647636
tgt_lng = 126.943500830574

target_name = "복권나라"
# Keywords to merge
keywords = ["1739-9", "926-25"]

updated_count = 0
for entry in data:
    if target_name in entry['n'] and '관악' in entry['a']:
        # Check if address matches target keywords
        should_update = False
        for k in keywords:
            if k in entry['a']:
                should_update = True
                break
        
        if should_update:
            entry['a'] = tgt_addr
            entry['lat'] = tgt_lat
            entry['lng'] = tgt_lng
            updated_count += 1

with open('lotto_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Unified {updated_count} entries for Gwanak Lottery Nara")

# 2. Update top_shops_131.json (Remove if exists)
with open('top_shops_131.json', 'r', encoding='utf-8') as f:
    top_shops = json.load(f)

filtered_shops = []
removed_count = 0

for shop in top_shops:
    # Remove if name matches and address matches any keyword
    if target_name in shop['n'] and '관악' in shop['a']:
        filtered_shops.append(shop) # Don't remove blindly, check address
        # Actually, let's remove it if it matches our merged targets
        # But top_shops might have old address
        is_target = False
        for k in keywords:
            if k in shop['a']:
                is_target = True
                break
        if is_target:
            filtered_shops.pop() # Remove the one we just added
            removed_count += 1
    else:
        filtered_shops.append(shop)

# Wait, the logic above is a bit weird. Let's rewrite cleaner.
filtered_shops = []
removed_shops_list = []
for shop in top_shops:
    if target_name in shop['n'] and '관악' in shop['a']:
        is_target = False
        for k in keywords:
            if k in shop['a']:
                is_target = True
                break
        if is_target:
            removed_shops_list.append(shop)
            continue # Skip adding
            
    filtered_shops.append(shop)

with open('top_shops_131.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_shops, f, ensure_ascii=False, indent=2)

print(f"Removed {len(removed_shops_list)} shops from top_shops_131.json")
for s in removed_shops_list:
    print(f"- {s['n']} ({s['a']})")
