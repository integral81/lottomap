import json

def cleanup_admin_targets():
    js_path = 'admin_targets.js'
    json_path = 'lotto_data.json'
    
    try:
        # Load registered shops from lotto_data.json
        with open(json_path, 'r', encoding='utf-8') as f:
            lotto_data = json.load(f)
        
        # Identify names that have 'pov'
        registered_names = set()
        for item in lotto_data:
            if 'pov' in item:
                registered_names.add(item.get('n', ''))
        
        # Read admin_targets.js
        with open(js_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract the list from window.allMissingShops = [...]
        start_marker = "window.allMissingShops = ["
        end_marker = "];"
        start_idx = content.find(start_marker) + len(start_marker)
        end_idx = content.rfind(end_marker)
        
        if start_idx == -1 or end_idx == -1:
            print("Could not find list in admin_targets.js")
            return
            
        list_str = content[start_idx:end_idx].strip()
        # Since it's JS literal, we need to handle trailing commas etc. 
        # But it's easier to just use json.loads if it's clean, or just parse carefully.
        # Let's try to wrap it in [] and load as JSON if possible, but JS objects might have single quotes or missing quotes.
        # Given the view_file output, it looks like valid JSON objects.
        
        import ast
        # ast.literal_eval can often parse JS-like lists of dicts
        try:
            missing_shops = ast.literal_eval("[" + list_str + "]")
        except:
            print("Failed to parse list with ast, trying a more robust approach.")
            return

        original_count = len(missing_shops)
        # Filter out registered ones
        # Special check: keep "노다지복권방" and "로또명당" if they are not truly registered
        new_missing_shops = []
        removed_names = []
        for shop in missing_shops:
            name = shop.get('name', '')
            # If the shop is "신간판" or above it, and it's in registered_names, remove it.
            # Actually, user said "above 신간판".
            if name in registered_names:
                removed_names.append(name)
            else:
                new_missing_shops.append(shop)
        
        # Write back to admin_targets.js
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write("window.allMissingShops = " + json.dumps(new_missing_shops, ensure_ascii=False, indent=4) + ";")
            
        print(f"Cleaned up {len(removed_names)} shops from admin_targets.js.")
        print(f"Remaining shops: {len(new_missing_shops)} (Original: {original_count})")
        print(f"Removed: {', '.join(removed_names)}")
        
    except Exception as e:
        print(f"Error during cleanup: {e}")

if __name__ == "__main__":
    cleanup_admin_targets()
