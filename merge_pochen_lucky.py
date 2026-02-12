import json

# 1. Update lotto_data.json
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Common Target Address & Coordinates (Based on User POV location - Jukyeobsan-ro)
# From previous check: x=127.1475, y=37.8288 is Igok-ri 127-6 -> Jukyeobsan-ro area
# Existing data has: 37.828862, 127.147507
tgt_addr = "경기 포천시 소흘읍 죽엽산로 438"
tgt_lat = 37.8288621438774
tgt_lng = 127.147507150439

updated_count = 0
for entry in data:
    # Target criteria: Name contains '행운복권방' AND Address contains '포천' or '소흘'
    if '행운복권방' in entry['n'] and ('포천' in entry['a'] or '소흘' in entry['a']):
        # Update to unified data
        entry['a'] = tgt_addr
        entry['lat'] = tgt_lat
        entry['lng'] = tgt_lng
        updated_count += 1

with open('lotto_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Unified {updated_count} entries for Pocheon Lucky Lotto")

# 2. Update top_shops_131.json (Remove if exists to clean up)
# We will NOT add it back here, because we want it removed from the TODO list.
# But we should check if there were multiple entries in top_shops?
with open('top_shops_131.json', 'r', encoding='utf-8') as f:
    top_shops = json.load(f)

# Filter out ANY Pocheon Lucky Lotto
filtered_shops = []
removed_count = 0

for shop in top_shops:
    if '행운복권방' in shop['n'] and ('포천' in shop['a'] or '소흘' in shop['a']):
        removed_count += 1
    else:
        filtered_shops.append(shop)

with open('top_shops_131.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_shops, f, ensure_ascii=False, indent=2)

print(f"Removed {removed_count} shops from top_shops_131.json")
