
import json
from collections import Counter

def find_4wins_missing_pov():
    print("--- Finding 4-Wins Shops Missing POV ---")
    try:
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            lotto_data = json.load(f)
            
        # 1. Aggregate wins and check existing POV
        shop_stats = {} # "address": {name, wins, has_pov, lat, lng}
        
        for item in lotto_data:
            addr = item.get('a', '').strip()
            name = item.get('n', '').strip()
            if not addr: continue
            
            if addr not in shop_stats:
                shop_stats[addr] = {
                    "name": name, 
                    "wins": 0, 
                    "has_pov": False,
                    "lat": item.get('lat'),
                    "lng": item.get('lng')
                }
            
            shop_stats[addr]["wins"] += 1
            if 'pov' in item:
                shop_stats[addr]["has_pov"] = True
                
        # 2. Filter for exactly 4 wins AND no POV
        targets = []
        for addr, info in shop_stats.items():
            if info['wins'] == 4 and not info['has_pov']:
                targets.append({
                    "name": info['name'],
                    "address": addr,
                    "wins": info['wins'],
                    "lat": info['lat'],
                    "lng": info['lng'],
                    "has_coords": (info['lat'] is not None and info['lng'] is not None)
                })
        
        # Sort by name for easier reading
        targets.sort(key=lambda x: x['name'])
        
        print(f"Total shops with 4 wins: {len([s for s in shop_stats.values() if s['wins'] == 4])}")
        print(f"Shops with 4 wins MISSING POV: {len(targets)}")
        
        # 3. Save to a temporary JSON file to be used for updating HTML
        with open('shops_4wins_missing_pov.json', 'w', encoding='utf-8') as f:
            json.dump(targets, f, indent=4, ensure_ascii=False)
            
        print("Saved list to 'shops_4wins_missing_pov.json'")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_4wins_missing_pov()
