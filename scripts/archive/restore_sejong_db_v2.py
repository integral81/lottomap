import json

# Read lotto_data.json
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Count wins
win_counts = {}
shop_info = {}

for entry in data:
    # Use name+address as key
    # If encoding is messed up, the key will be messed up too, but consistently
    key = f"{entry['n']}|{entry['a']}"
    if key not in win_counts:
        win_counts[key] = 0
        shop_info[key] = entry
    win_counts[key] += 1

# Filter for 7 wins
targets = []
for key, count in win_counts.items():
    if count == 7:
        targets.append(shop_info[key])

# Find the one that looks like Daebak Super
# Even if text is garbled, we can look for specific byte sequences or just print all 7-win shops
# But we know Sejong might have '127-6' in address.
found_shop = None
for shop in targets:
    # Check if '대박' is in name OR if it matches known Sejong address pattern
    if '대박' in shop['n'] or '127-6' in shop['a']:
        found_shop = shop
        break
    
    # Fallback: check if the name is short (like '대박슈퍼' - 4 chars) and address has '세종' (might be broken)
    # Let's just print all 7-win candidates to debug if not found
    
if found_shop:
    print(f"Found target shop: {found_shop['n']} ({found_shop['a']})")
    
    shop_obj = {
        "n": found_shop['n'],
        "a": found_shop['a'],
        "lat": found_shop['lat'],
        "lng": found_shop['lng'],
        "w": 7
    }
    
    # Add to top shops
    with open('top_shops_131.json', 'r', encoding='utf-8') as f:
        top_shops = json.load(f)
        
    # Check duplicate
    exists = False
    for s in top_shops:
        if s['n'] == shop_obj['n'] and s['a'] == shop_obj['a']:
            exists = True
            break
            
    if not exists:
        top_shops.insert(0, shop_obj)
        with open('top_shops_131.json', 'w', encoding='utf-8') as f:
            json.dump(top_shops, f, ensure_ascii=False, indent=2)
        print(f"Restored! Total shops: {len(top_shops)}")
    else:
        print("Shop already in list.")

else:
    print("Could not find any 7-win shop matching criteria.")
    print("Listing all 7-win shops:")
    for t in targets:
        print(f"- {t['n']} ({t['a']})")
