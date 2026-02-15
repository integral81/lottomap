import json

# Read lotto_data.json to get the Daegu Bokgwon Department Store details
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# The one with 7 wins in Daegu
# Address: 대구 달서구 월배로 329-135
target_bw = None
bw_entries = [d for d in data if '복권백화점' in d['n'] and '대구' in d['a']]

# Find unique addresses and counts (just to be sure)
if not bw_entries:
    print("Could not find Daegu Bokgwon Department Store")
    exit()

# Get one entry for this shop to add to top_shops
restored_shop = bw_entries[0]
# Format for top_shops: n, a, lat, lng, w
shop_obj = {
    "n": restored_shop['n'],
    "a": restored_shop['a'],
    "lat": restored_shop['lat'],
    "lng": restored_shop['lng'],
    "w": 7 # We know it has 7 wins from previous check
}

# Read top_shops_131.json
with open('top_shops_131.json', 'r', encoding='utf-8') as f:
    top_shops = json.load(f)

# Add it back
top_shops.insert(0, shop_obj) # Add to top for visibility

# Save
with open('top_shops_131.json', 'w', encoding='utf-8') as f:
    json.dump(top_shops, f, ensure_ascii=False, indent=2)

print(f"Restored 1 shop. Total now: {len(top_shops)}")
