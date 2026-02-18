
import json
import re

# Constants
TARGET_NAME = "세븐일레븐부산온천장역점"
NEW_POV = {
    "id": 1202578370,
    "pan": 122.0,
    "tilt": -2.0,
    "zoom": 0
}
NEW_MSG = "2층 개찰구쪽 매장있음!!"

# Path to files
JS_PATH = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'
HTML_PATH = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\index.html'

def update_js():
    try:
        with open(JS_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
            json_str = content.replace('window.lottoData =', '').strip().rstrip(';')
            data = json.loads(json_str)
        
        updated_count = 0
        for item in data:
            if item.get('n') == TARGET_NAME:
                item['pov'] = NEW_POV
                item['customMessage'] = NEW_MSG
                # Also ensure panoid key exists for legacy compatibility if needed
                item['panoid'] = NEW_POV['id']
                updated_count += 1
        
        if updated_count > 0:
            new_content = 'window.lottoData = ' + json.dumps(data, ensure_ascii=False, indent=0) + ';'
            with open(JS_PATH, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {updated_count} entries in lotto_data.js")
        else:
            print(f"Target {TARGET_NAME} not found in lotto_data.js")
            
    except Exception as e:
        print(f"Error updating JS: {e}")

def update_html():
    try:
        with open(HTML_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for ROADVIEW_PRESETS array
        # We need to find the entry for this shop and update it.
        # It's a string replacement using regex or simple string manipulation.
        
        # Regex to find the object. It's multi-line maybe?
        # Let's search for unique identifier like name: "세븐일레븐부산온천장역점"
        pattern = re.compile(r'\{[^}]*name:\s*"세븐일레븐부산온천장역점"[^}]*\}', re.DOTALL)
        
        match = pattern.search(content)
        if match:
            old_str = match.group(0)
            # update parameters inside the string
            # This is tricky with regex. Let's just reconstruct the string if we found it.
            # But the address might vary.
            # Let's try to locate it and replace the whole block if possible, or just properties.
            # Simpler approach: If it exists in presets, just replace the whole line if it's one line.
            # The presets are usually one line per shop in this file based on previous edits.
            pass # skipping complex regex. 
            
            # Alternative: Just append a new corrected preset at the end of the list and let it override? No, duplication.
            # Let's try to find line by line.
            
        lines = content.split('\n')
        new_lines = []
        updated = False
        for line in lines:
            if 'name: "세븐일레븐부산온천장역점"' in line:
                # Construct new line
                # Preserving indentation (checking whitespace)
                indent = line.split('{')[0]
                # We need address from the line or hardcode it?
                # Let's extract address from old line
                addr_match = re.search(r'addr:\s*"([^"]*)"', line)
                addr = addr_match.group(1) if addr_match else "부산 동래구 온천동 156-1 온천장역지하철 내"
                
                new_line = f'{indent}{{ name: "{TARGET_NAME}", addr: "{addr}", panoId: {NEW_POV["id"]}, pov: {{ pan: {NEW_POV["pan"]}, tilt: {NEW_POV["tilt"]}, zoom: {NEW_POV["zoom"]} }}, customMessage: "{NEW_MSG}" }},'
                new_lines.append(new_line)
                updated = True
                print("Updated HTML preset line.")
            else:
                new_lines.append(line)
        
        if updated:
            with open(HTML_PATH, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
        else:
            print("Target not found in HTML presets.")

    except Exception as e:
        print(f"Error updating HTML: {e}")

if __name__ == "__main__":
    update_js()
    update_html()
