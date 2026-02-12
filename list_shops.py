import json
from collections import Counter

def extract_shops():
    try:
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Count wins per shop (Name + Address)
        shop_counts = Counter()
        shop_info = {}
        
        for item in data:
            name = item.get('n', '').strip()
            addr = item.get('a', '').strip()
            key = (name, addr)
            shop_counts[key] += 1
            if key not in shop_info:
                shop_info[key] = {
                    'name': name,
                    'addr': addr,
                    'lat': item.get('lat'),
                    'lng': item.get('lng')
                }
        
        # Filter shops with 5 or more wins
        top_shops = []
        for key, count in shop_counts.items():
            if count >= 5:
                info = shop_info[key]
                info['win_count'] = count
                top_shops.append(info)
        
        # Sort by win count descending
        top_shops.sort(key=lambda x: x['win_count'], reverse=True)
        
        with open('top_shops_audit.json', 'w', encoding='utf-8') as f:
            json.dump(top_shops, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully extracted {len(top_shops)} top shops to top_shops_audit.json")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    extract_shops()
