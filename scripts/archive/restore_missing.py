
import json

def restore_missing_winners():
    print("--- [EXECUTION] Restoring Missing Winners ---")
    try:
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            lotto_data = json.load(f)
            
        with open('missing_winners_report.json', 'r', encoding='utf-8') as f:
            missing_winners = json.load(f)
            
        # Create a coordinate cache from current data
        coord_cache = {}
        for item in lotto_data:
            addr = item.get('a', '').strip()
            if addr and item.get('lat'):
                coord_cache[addr] = (item['lat'], item['lng'])
        
        restored_count = 0
        restored_items = []
        
        for m in missing_winners:
            # Skip online sites if they provide no value to the map, but user wants 100% accuracy.
            # I will include them with a special tag or just as-is.
            
            new_item = {
                "r": m['r'],
                "n": m['n'],
                "a": m['a'],
                "m": "수동" if "인터넷" in m['n'] else "알수없음", # Defaulting to manual for online, unknown for missing others
                "lat": None,
                "lng": None
            }
            
            # Try to get coords from cache
            if m['a'] in coord_cache:
                new_item['lat'], new_item['lng'] = coord_cache[m['a']]
            
            restored_items.append(new_item)
            restored_count += 1
            
        lotto_data.extend(restored_items)
        
        # Sort by round descending for cleanliness
        lotto_data.sort(key=lambda x: x['r'], reverse=True)
        
        with open('lotto_data.json', 'w', encoding='utf-8') as f:
            json.dump(lotto_data, f, indent=2, ensure_ascii=False)
            
        print(f"Successfully restored {restored_count} winners.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    restore_missing_winners()
