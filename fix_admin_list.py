import json

target_file = 'top_shops_131.json'
target_name = '우리들공업탑점'

try:
    with open(target_file, 'r', encoding='utf-8') as f:
        shops = json.load(f)
    
    idx = -1
    for i, s in enumerate(shops):
        if target_name in s['n']:
            idx = i
            break
    
    if idx != -1:
        # Keep from our target shop onwards
        new_shops = shops[idx:]
        print(f"Kept {len(new_shops)} shops starting from {target_name}.")
        
        # Add back Happy People (Remind)
        restore = {
            'n': '행복한사람들 (흥부네)', 
            'a': '경기 광주시 경충대로 763', 
            'lat': 37.3555798712105, 
            'lng': 127.32540015887
        }
        new_shops.insert(0, restore)
        print("Restored '행복한사람들 (흥부네)' to the top as requested.")
        
        with open(target_file, 'w', encoding='utf-8') as f:
            json.dump(new_shops, f, ensure_ascii=False, indent=2)
        print("Successfully updated top_shops_131.json.")
    else:
        print(f"Error: '{target_name}' not found in the list.")

except Exception as e:
    print(f"Error: {e}")
