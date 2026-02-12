import json

# 1. Update lotto_data.json
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Target: Daegu Ildeung Lotto
# Unified Address: Daemyeongcheon-ro 220
tgt_addr = "대구 달서구 대명천로 220"
# Coordinates from existing data (both are almost same, use the one from Daemyeongcheon-ro)
tgt_lat = 35.84220335202
tgt_lng = 128.53619207262

target_name = "일등복권편의점"
match_keyword1 = "대명천로"
match_keyword2 = "본리동"

updated_count = 0
for entry in data:
    if target_name in entry['n'] and ('대구' in entry['a']):
        # If address contains '본리동' (old), update to new
        if match_keyword2 in entry['a']:
            entry['a'] = tgt_addr
            entry['lat'] = tgt_lat
            entry['lng'] = tgt_lng
            updated_count += 1
        # If address is already new but maybe coords differ slightly, unify coords too
        elif match_keyword1 in entry['a']:
            entry['lat'] = tgt_lat
            entry['lng'] = tgt_lng
            # Just to be sure
            updated_count += 1

with open('lotto_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Unified {updated_count} entries for Ildeung Lotto")

# 2. Update top_shops_131.json (Remove)
with open('top_shops_131.json', 'r', encoding='utf-8') as f:
    top_shops = json.load(f)

filtered_shops = []
removed_count = 0

for shop in top_shops:
    if target_name in shop['n'] and '대구' in shop['a']:
        removed_count += 1
    else:
        filtered_shops.append(shop)

with open('top_shops_131.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_shops, f, ensure_ascii=False, indent=2)

print(f"Removed {removed_count} shops from top_shops_131.json")
