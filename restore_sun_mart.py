import json

# Read lotto_data.json to get the 5-win Sun Mart details
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# The one with 5 wins
# Address looks like 청주시 흥덕구 가경동...
target_sun = None
sun_entries = [d for d in data if d['n'] == '썬마트']

# Find unique addresses and counts
addr_counts = {}
for entry in sun_entries:
    addr = entry['a']
    if addr not in addr_counts:
        addr_counts[addr] = 0
    addr_counts[addr] += 1

# Identify the address with 5 wins
target_addr = "Unknown"
for addr, count in addr_counts.items():
    if count == 5:
        target_addr = addr
        break

if target_addr == "Unknown":
    print("Could not find Sun Mart with 5 wins")
    exit()

print(f"Restoring Sun Mart with 5 wins (Addr: {target_addr})")

# Get one entry for this shop to add to top_shops
restored_shop = next(d for d in sun_entries if d['a'] == target_addr)
# Format for top_shops: n, a, lat, lng, w
shop_obj = {
    "n": restored_shop['n'],
    "a": restored_shop['a'],
    "lat": restored_shop['lat'],
    "lng": restored_shop['lng'],
    "w": 5
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
