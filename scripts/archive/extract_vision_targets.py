
import json

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    shop_stats = {}
    for item in data:
        addr = item.get('a', '').strip()
        name = item.get('n', '').strip()
        if not addr: continue
        
        key = (name, addr)
        if key not in shop_stats:
            shop_stats[key] = {
                "name": name,
                "address": addr,
                "wins": 0,
                "has_pov": False,
                "lat": item.get('lat'),
                "lng": item.get('lng')
            }
        
        shop_stats[key]["wins"] += 1
        if 'pov' in item:
            shop_stats[key]["has_pov"] = True

    # Filter: Exactly 4 wins AND No POV
    target_shops = [v for k, v in shop_stats.items() if v['wins'] == 4 and not v['has_pov']]
    
    print(f"Total candidates to verify: {len(target_shops)}")
    
    with open('shops_to_verify_vision.json', 'w', encoding='utf-8') as f:
        json.dump(target_shops, f, ensure_ascii=False, indent=2)

except Exception as e:
    print(f"Error: {e}")
