import json

# 1. Update lotto_data.json
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

target_name = "행운복권방 보생당건강원"
# Source (old) address signature
src_addr_part = "부송동"
# Target (new) address
tgt_addr = "전북 익산시 무왕로 1268"
# Target coordinates (from existing Muwang-ro entries)
tgt_lat = 35.9603454488036
tgt_lng = 126.997229871301

updated_count = 0
for entry in data:
    if target_name in entry['n']:
        # If it's the old address, update it
        if src_addr_part in entry['a']:
            entry['a'] = tgt_addr
            entry['lat'] = tgt_lat
            entry['lng'] = tgt_lng
            updated_count += 1

with open('lotto_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Updated {updated_count} entries in lotto_data.json")

# 2. Update top_shops_131.json (Remove if exists)
with open('top_shops_131.json', 'r', encoding='utf-8') as f:
    top_shops = json.load(f)

filtered_shops = [s for s in top_shops if target_name not in s['n']]
removed_count = len(top_shops) - len(filtered_shops)

with open('top_shops_131.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_shops, f, ensure_ascii=False, indent=2)

print(f"Removed {removed_count} shops from top_shops_131.json")
