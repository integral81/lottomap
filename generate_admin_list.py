import json
import re

def generate_admin_targets():
    json_path = 'lotto_data.json'
    js_path = 'admin_targets.js'
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        shops = {}
        for item in data:
            name = item.get('n', '').strip()
            # Skip online
            if "동행복권" in name or "인터넷" in name or "dhlottery" in name:
                continue
                
            addr = item.get('a', '').strip()
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

        targets = []
        for key, info in shops.items():
            name, addr = key
            if info["count"] >= 3 and not info["has_pov"]:
                targets.append({
                    "name": name,
                    "address": addr, # Match HTML 'address'
                    "wins": info["count"], # Match HTML 'wins'
                    "lat": info["lat"],
                    "lng": info["lng"]
                })
        
        # Sort by win count desc
        targets.sort(key=lambda x: x["wins"], reverse=True)
        
        # Write JS
        js_content = "const adminTargets = [\n"
        for t in targets:
            # Safe stringify
            safe_name = t['name'].replace("'", "\\'")
            safe_addr = t['address'].replace("'", "\\'")
            lat = t['lat'] if t['lat'] else 'null'
            lng = t['lng'] if t['lng'] else 'null'
            
            js_content += f"    {{ name: '{safe_name}', address: '{safe_addr}', wins: {t['wins']}, lat: {lat}, lng: {lng} }},\n"
        js_content += "];"
        
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(js_content)
            
        print(f"Generated {len(targets)} targets with correct format (name, address, wins).")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_admin_targets()
