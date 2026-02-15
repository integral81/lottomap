import json
import re

def refresh_admin_targets_category3():
    json_path = 'lotto_data.json'
    js_path = 'admin_targets.js'
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # 1. Aggregate wins by (Name, Address)
        # We need to handle the fact that some shops might still have slightly different addresses if consolidation wasn't perfect.
        # But we did a big consolidation. Let's trust (Name, Address) grouping for now.
        
        shops = {}
        for item in data:
            name = item.get('n', '').strip()
            addr = item.get('a', '').strip()
            
            # Skip online shops immediately
            if "동행복권" in name or "인터넷" in name or "사이트" in name or "dhlottery" in name:
                continue
                
            key = (name, addr)
            
            if key not in shops:
                shops[key] = {
                    "count": 0,
                    "has_pov": False,
                    "lat": item.get('lat'),
                    "lng": item.get('lng')
                }
            
            shops[key]["count"] += 1
            if "pov" in item and item["pov"]:
                shops[key]["has_pov"] = True

        # 2. Filter Category 3 (3+ wins, No POV)
        targets = []
        for key, info in shops.items():
            name, addr = key
            if info["count"] >= 3 and not info["has_pov"]:
                targets.append({
                    "name": f"{name} ({info['count']}회)", # Append win count to name for visibility
                    "addr": addr,
                    "win_count": info["count"], # Keep raw count for sorting
                    "lat": info["lat"],
                    "lng": info["lng"]
                })
        
        # Sort by win count desc
        targets.sort(key=lambda x: x["win_count"], reverse=True)
        
        # 3. Write to JS
        js_content = "const adminTargets = [\n"
        for t in targets:
            # Escape quotes if necessary
            safe_name = t['name'].replace("'", "\\'")
            safe_addr = t['addr'].replace("'", "\\'")
            js_content += f"    {{ name: '{safe_name}', addr: '{safe_addr}' }},\n"
        js_content += "];"
        
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(js_content)
            
        print(f"Generated {len(targets)} targets for Category 3 (3+ wins, No POV, Offline).")
        # Print top 5 for verification
        for t in targets[:5]:
            print(f"- {t['name']}: {t['addr']}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    refresh_admin_targets_category3()
