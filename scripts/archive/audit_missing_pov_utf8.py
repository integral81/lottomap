import json
import sys

def audit_missing_pov_utf8():
    # Force UTF-8 for stdout
    sys.stdout.reconfigure(encoding='utf-8')
    
    json_path = 'lotto_data.json'
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        shops = {}
        for item in data:
            key = (item.get('n', ''), item.get('a', ''))
            
            if key not in shops:
                shops[key] = {
                    "count": 0,
                    "has_pov": False
                }
            
            shops[key]["count"] += 1
            if "pov" in item and item["pov"]:
                shops[key]["has_pov"] = True

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
        
        print(f"Total Missing POV (3+ wins): {len(missing_pov_shops)}")
        
        # Sort by wins desc
        sorted_shops = sorted(missing_pov_shops, key=lambda x: x['count'], reverse=True)
        
        print("\n--- Top 20 Missing POV Shops ---")
        for shop in sorted_shops[:20]:
            print(f"{shop['name']} ({shop['addr']}): {shop['count']} wins")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    audit_missing_pov_utf8()
