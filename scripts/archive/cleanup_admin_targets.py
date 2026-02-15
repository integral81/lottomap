import json
import re

def cleanup_admin_targets():
    js_path = 'admin_targets.js'
    json_path = 'lotto_data.json'
    
    try:
        with open(js_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract the array from window.allMissingShops = [ ... ];
        match = re.search(r'window\.allMissingShops\s*=\s*(\[.*\]);', content, re.DOTALL)
        if not match:
            print("Could not find window.allMissingShops in admin_targets.js")
            return
        
        targets_str = match.group(1)
        # Convert JS-like object to JSON (might need handling for trailing commas or single quotes, but usually my JS is clean)
        # Let's try to parse it directly or with a more robust parser if needed.
        # Actually, standard json.loads might fail if there's trailing commas.
        try:
            targets = json.loads(targets_str)
        except:
            # Simple cleanup for trailing commas
            clean_str = re.sub(r',\s*\]', ']', targets_str)
            clean_str = re.sub(r',\s*\}', '}', clean_str)
            targets = json.loads(clean_str)
            
        with open(json_path, 'r', encoding='utf-8') as f:
            lotto_data = json.load(f)
            
        registered_names = set()
        for item in lotto_data:
            if 'pov' in item:
                registered_names.add(item.get('n'))
        
        new_targets = []
        removed_count = 0
        for shop in targets:
            name = shop.get('name')
            # Check if this shop (or a variant) is registered with POV
            is_registered = False
            if name in registered_names:
                is_registered = True
            else:
                # Flexible check: same name prefix and region
                addr = shop.get('address', '')
                region = addr.split()[0] if addr else ''
                for reg_name in registered_names:
                    if name[:3] in reg_name and region in addr:
                        is_registered = True
                        break
            
            if is_registered:
                removed_count += 1
                print(f"Removing registered shop: {name}")
            else:
                new_targets.append(shop)
                
        # Write back to js
        new_content = f"window.allMissingShops = {json.dumps(new_targets, ensure_ascii=False, indent=4)};"
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"\nSuccessfully removed {removed_count} shops. {len(new_targets)} shops remaining.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    cleanup_admin_targets()
