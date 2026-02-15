
import json
import os

# Data for multiple shops
updates = [
    {
        "name": "행운복권",
        "addr_part": "제천시 의림동",
        "panoId": 1184953799,
        "pov": { "pan": 14.56, "tilt": 5.01, "zoom": 0 }
    },
    {
        "name": "행운복권방",
        "addr_part": "부산 중구 남포동5가",
        "panoId": 1202742263,
        "pov": { "pan": 162.33, "tilt": -1.85, "zoom": -2 }
    }
]

# 1. Update lotto_data.json
print("Updating lotto_data.json...")
try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for up in updates:
        count = 0
        for item in data:
            if up["name"] == item.get('n') and up["addr_part"] in item.get('a', ''):
                item['pov'] = { "id": str(up["panoId"]), "pan": up["pov"]["pan"], "tilt": up["pov"]["tilt"], "zoom": up["pov"]["zoom"] }
                count += 1
        print(f"Updated {count} entries for {up['name']} in lotto_data.json.")
            
    with open('lotto_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
except Exception as e:
    print(f"Error updating lotto_data.json: {e}")

# 2. Update index.html (ROADVIEW_PRESETS)
print("Updating index.html...")
try:
    with open('index.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        updated = False
        for up in updates:
            if f'name: "{up["name"]}"' in line and up["addr_part"][:5] in line:
                # Generate new line with appropriate short address
                short_addr = up["addr_part"]
                if up["name"] == "행운복권": short_addr = "충북 제천시 의림동"
                if up["name"] == "행운복권방": short_addr = "부산 중구 남포동5가"
                
                new_line = f'            {{ name: "{up["name"]}", addr: "{short_addr}", panoId: {up["panoId"]}, pov: {{ pan: {up["pov"]["pan"]}, tilt: {up["pov"]["tilt"]}, zoom: {up["pov"]["zoom"]} }} }},\n'
                new_lines.append(new_line)
                updated = True
                print(f"Updated {up['name']} in index.html.")
                break
        if not updated:
            new_lines.append(line)
            
    with open('index.html', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
except Exception as e:
    print(f"Error updating index.html: {e}")

# 3. Clean up admin_pov.html (allMissingShops)
print("Updating admin_pov.html...")
try:
    with open('admin_pov.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    skip_mode = False
    for line in lines:
        matched = False
        for up in updates:
            if f'"name": "{up["name"]}"' in line and up["addr_part"][:5] in line:
                skip_mode = True
                matched = True
                print(f"Removing {up['name']} from admin_pov.html list.")
                break
        
        if matched: continue
        
        if skip_mode:
            if '"has_coords": true' in line: continue
            if '},' in line or '}' in line:
                skip_mode = False
                continue
            continue
            
        new_lines.append(line)
    
    with open('admin_pov.html', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
except Exception as e:
    print(f"Error updating admin_pov.html: {e}")
