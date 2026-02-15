import json

# Read lotto_data.json to get Sejong Daebak Super details
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find the one with 7 wins (Sejong)
# Address contains '127-6'
target_db = None
db_entries = [d for d in data if '대박슈퍼' in d['n'] and '127-6' in d['a']]

if not db_entries:
    print("Could not find Sejong Daebak Super in lotto_data.json")
    # Fallback: manually construct based on known info if lookup fails
    # But usually it should be there.
    # Let's try to find by wins if name/addr fails due to encoding
    # 7 wins shop with '대박슈퍼' in name?
    # We saw it in logs: '대박슈퍼 (세종 세종시 금남면 용포리 127-6) - 7 wins'
    pass

if db_entries:
    restored_shop = db_entries[0]
    
    shop_obj = {
        "n": restored_shop['n'],
        "a": restored_shop['a'],
        "lat": restored_shop['lat'],
        "lng": restored_shop['lng'],
        "w": 7
    }

    # Read top_shops_131.json
    with open('top_shops_131.json', 'r', encoding='utf-8') as f:
        top_shops = json.load(f)

    # Check if exists
    exists = False
    for s in top_shops:
        if s['n'] == shop_obj['n'] and s['a'] == shop_obj['a']:
            exists = True
            break
            
    if not exists:
        top_shops.insert(0, shop_obj) # Add to top
        
        # Save
        with open('top_shops_131.json', 'w', encoding='utf-8') as f:
            json.dump(top_shops, f, ensure_ascii=False, indent=2)
            
        print(f"Restored Sejong Daebak Super. Total now: {len(top_shops)}")
    else:
        print("Sejong Daebak Super already exists.")
else:
    print("Failed to look up Sejong Daebak Super.")
