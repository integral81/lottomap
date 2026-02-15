import json

def audit_missing_pov():
    json_path = 'lotto_data.json'
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # 1. Group by unique shop (Name + Address seems best, or coords)
        # However, we've been consolidating into single entries.
        # But wait, lotto_data.json is a FLAT list of wins.
        # So we need to group by (name, address) to count wins.
        
        shops = {}
        for item in data:
            # unique key: name + address (standardized)
            # Use raw address for grouping if we trust our consolidation, 
            # but better to Group by 'n' and 'a' as they should be identical after consolidation.
            key = (item.get('n', ''), item.get('a', ''))
            
            if key not in shops:
                shops[key] = {
                    "count": 0,
                    "has_pov": False,
                    "items": []
                }
            
            shops[key]["count"] += 1
            if "pov" in item and item["pov"]:
                shops[key]["has_pov"] = True
            shops[key]["items"].append(item)

        # 2. Filter 3+ wins
        missing_pov_shops = []
        for key, info in shops.items():
            name, addr = key
            if info["count"] >= 3:
                if not info["has_pov"]:
                    missing_pov_shops.append({
                        "name": name,
                        "addr": addr,
                        "count": info["count"]
                    })
        
        print(f"Total Unique Shops with 3+ Wins: {len([s for s in shops.values() if s['count'] >= 3])}")
        print(f"Shops with 3+ Wins MISSING POV: {len(missing_pov_shops)}")
        
        if missing_pov_shops:
            print("\n--- List of Missing POV Shops (3+ Wins) ---")
            for shop in sorted(missing_pov_shops, key=lambda x: x['count'], reverse=True):
                print(f"{shop['name']} ({shop['addr']}): {shop['count']} wins")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    audit_missing_pov()
