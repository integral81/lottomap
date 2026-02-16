import json
import re

def main():
    try:
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading lotto_data.json: {e}")
        return

    # Aggregate just by address to find unique shops
    shop_count = {}
    
    for entry in data:
        name = entry.get('n', '').strip()
        addr = entry.get('a', '').strip()
        
        if not addr: continue
        if "인터넷" in name or "동행복권" in addr: continue
        
        # Strip spaces from address for consistent key
        key = re.sub(r'\s+', '', addr)
        
        if key not in shop_count:
            shop_count[key] = {
                'name': name,
                'addr': addr,
                'wins': 0,
                'rounds': []
            }
        
        shop_count[key]['wins'] += 1
        shop_count[key]['rounds'].append(entry.get('r'))
        
        # If earlier entry had name but this one doesn't, keep name? 
        # Or if later one has name? Usually name is consistent or empty.
        if name and not shop_count[key]['name']:
             shop_count[key]['name'] = name

    # Search for Seocho-dong
    print("Searching for '서초동' shops with 3+ wins...")
    found_any = False
    
    for k, v in shop_count.items():
        if "서초동" in v['addr'] and v['wins'] >= 3:
            found_any = True
            print(f"Found: Name='{v['name']}' Addr='{v['addr']}' Wins: {v['wins']}")
            print(f"  Rounds: {v['rounds'][:5]} ...")
            
    if not found_any:
        print("No Seocho-dong shops found with 3+ wins.")

    # Also search for "1571" specifically
    print("\nSearching for '1571' in address...")
    for k, v in shop_count.items():
        if "1571" in v['addr']:
            print(f"Found by 1571: Name='{v['name']}' Addr='{v['addr']}' Wins: {v['wins']}")

if __name__ == "__main__":
    main()
