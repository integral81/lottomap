import json

def audit_legends():
    try:
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        shops = {}
        for entry in data:
            addr = entry.get('a', 'unknown')
            name = entry.get('n', 'unknown')
            key = f"{addr}|{name}"
            
            if key not in shops:
                shops[key] = {
                    'name': name,
                    'addr': addr,
                    'wins': 0,
                    'pov': None
                }
            
            shops[key]['wins'] += 1
            if entry.get('pov'):
                shops[key]['pov'] = entry['pov']
        
        # Identify Legends (10+ wins)
        legends = [v for v in shops.values() if v['wins'] >= 10]
        missing_legends = [v for v in legends if not v['pov']]
        
        # Identify Gold (5+ wins)
        gold = [v for v in shops.values() if 5 <= v['wins'] < 10]
        missing_gold = [v for v in gold if not v['pov']]

        print(f"Total Unique Shops: {len(shops)}")
        print(f"Legend Shops (10+ wins): {len(legends)} (Missing POV: {len(missing_legends)})")
        print(f"Gold Shops (5-9 wins): {len(gold)} (Missing POV: {len(missing_gold)})")
        
        if missing_legends:
            print("\n--- Missing POV Legends ---")
            for shop in sorted(missing_legends, key=lambda x: x['wins'], reverse=True):
                print(f"[{shop['wins']}회] {shop['name']} - {shop['addr']}")
        
        if missing_gold:
            print("\n--- Missing POV Gold Shops (Top 10) ---")
            for shop in sorted(missing_gold, key=lambda x: x['wins'], reverse=True)[:10]:
                print(f"[{shop['wins']}회] {shop['name']} - {shop['addr']}")
        
        if not missing_legends and not missing_gold:
            print("\nAll 5+ win shops have POV registered! 🎉".encode('utf-8').decode('utf-8'))

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    audit_legends()
