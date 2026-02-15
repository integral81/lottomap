
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
                "wins": 0,
                "has_pov": False,
                "pov_data": None
            }
        
        shop_stats[key]["wins"] += 1
        if 'pov' in item:
            shop_stats[key]["has_pov"] = True
            shop_stats[key]["pov_data"] = item['pov']

    # Filter for EXACTLY 4 wins
    target_shops = {k: v for k, v in shop_stats.items() if v['wins'] == 4}
    
    no_pov = [k for k, v in target_shops.items() if not v['has_pov']]
    has_pov = [k for k, v in target_shops.items() if v['has_pov']]
    
    print(f"Total 4-win shops: {len(target_shops)}")
    print(f" - Without POV: {len(no_pov)}")
    print(f" - With POV (To be verified): {len(has_pov)}")
    
    # Save target list for processing
    with open('verify_lotto_pov.json', 'w', encoding='utf-8') as f:
        json.dump({
            "no_pov": [{"n": k[0], "a": k[1]} for k in no_pov],
            "has_pov": [{"n": k[0], "a": k[1], "p": v['pov_data']} for k, v in target_shops.items() if v['has_pov']]
        }, f, ensure_ascii=False, indent=2)

except Exception as e:
    print(f"Error: {e}")
