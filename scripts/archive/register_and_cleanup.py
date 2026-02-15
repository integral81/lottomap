import json

def register_batch_22():
    json_path = 'lotto_data.json'
    
    # Shop Data for Batch 22
    batch_data = [
        {
            "search_name": "용두천하",
            "name": "용두천하",
            "addr": "광주 북구 하서로 373 (양산동)",
            "lat": 35.208358,
            "lng": 126.873485,
            "pov": {"id": "1198462057", "pan": 168.0, "tilt": 4.8, "zoom": 0}
        },
        {
            "search_name": "욱일슈퍼",
            "name": "욱일슈퍼",
            "addr": "인천 부평구 일신동 110-5",
            "lat": 37.484616,
            "lng": 126.746732,
            "pov": {"id": "1198799894", "pan": 201.17, "tilt": 4.75, "zoom": -3}
        },
        {
            "search_name": "운수대통",
            "name": "운수대통",
            "addr": "경기 수원시 권선구 호매실동 87-2",
            "lat": 37.268996,
            "lng": 126.958729,
            "pov": {"id": "1199807944", "pan": 328.10, "tilt": 4.63, "zoom": -3}
        }
    ]
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for shop in batch_data:
            count = 0
            for item in data:
                name = item.get('n', '')
                addr = item.get('a', '')
                
                # Matching
                match = False
                if shop["search_name"] in name:
                    region = shop["addr"].split()[0]
                    if region in addr:
                        # Extra filter for 용두천하 (Gwangju only)
                        if shop["search_name"] == "용두천하" and "광주" not in addr:
                            continue
                        # Extra filter for 운수대통 (Suwon only)
                        if shop["search_name"] == "운수대통" and "수원" not in addr:
                            continue
                        match = True
                
                if match:
                    item['n'] = shop["name"]
                    item['a'] = shop["addr"]
                    item['lat'] = shop["lat"]
                    item['lng'] = shop["lng"]
                    item['pov'] = shop["pov"]
                    if 'closed' in item:
                        del item['closed']
                    count += 1
            print(f"Updated {count} records for {shop['name']}.")
            
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Error updating lotto_data.json: {e}")

def cleanup_admin_targets():
    js_path = 'admin_targets.js'
    target_name = "용두천하"
    
    try:
        with open(js_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        start_marker = "window.allMissingShops = ["
        end_marker = "];"
        start_idx = content.find(start_marker) + len(start_marker)
        end_idx = content.rfind(end_marker)
        
        if start_idx == -1 or end_idx == -1:
            print("Could not find list in admin_targets.js")
            return
            
        list_str = content[start_idx:end_idx].strip()
        
        import ast
        try:
            missing_shops = ast.literal_eval("[" + list_str + "]")
        except Exception as e:
            # If literal_eval fails due to JS syntax, use a simpler approach
            print(f"Parsing failed: {e}. Trying simple index-based removal.")
            return

        # Find index of target_name
        target_idx = -1
        for i, shop in enumerate(missing_shops):
            if shop.get('name') == target_name:
                target_idx = i
                break
        
        if target_idx == -1:
            print(f"Could not find '{target_name}' in the list.")
            return
            
        # Remove everything from start to target_idx (inclusive)
        removed_shops = missing_shops[:target_idx+1]
        remaining_shops = missing_shops[target_idx+1:]
        
        # Write back
        new_content = "window.allMissingShops = " + json.dumps(remaining_shops, ensure_ascii=False, indent=4) + ";"
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"Removed {len(removed_shops)} shops (up to '{target_name}') from admin_targets.js.")
        print(f"Remaining shops: {len(remaining_shops)}")
        
    except Exception as e:
        print(f"Error cleaning up admin_targets.js: {e}")

if __name__ == "__main__":
    register_batch_22()
    cleanup_admin_targets()
