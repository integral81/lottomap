
import json
import os

# Data for multiple shops (including the previously pending one)
updates = [
    {
        "name": "행운복권",
        "addr_part": "군포시 대야미동",
        "panoId": 1175680167,
        "pov": { "pan": 302.40, "tilt": 7.50, "zoom": -1 }
    },
    {
        "name": "행운복권방",
        "addr_part": "의정부시 용현동",
        "panoId": 1174558837,
        "pov": { "pan": 255.27, "tilt": -1.13, "zoom": -3 }
    },
    {
        "name": "행운을주는사람들",
        "addr_part": "충주시 연수동",
        "panoId": 1165060593,
        "pov": { "pan": 232.92, "tilt": 3.33, "zoom": -3 }
    },
    {
        "name": "형제상회",
        "addr_part": "대전 서구 용문동",
        "panoId": 1201235032,
        "pov": { "pan": 231.57, "tilt": 11.75, "zoom": -3 }
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
        print(f"Updated {count} entries for {up['name']} ({up['addr_part']}) in lotto_data.json.")
            
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
            if f'name: "{up["name"]}"' in line and (up["addr_part"][:5] in line or up["addr_part"] in line):
                # Use standard address format
                short_addr = up["addr_part"]
                if up["name"] == "행운복권": short_addr = "경기 군포시 대야미동"
                if up["name"] == "행운복권방": short_addr = "경기 의정부시 용현동"
                if up["name"] == "행운을주는사람들": short_addr = "충북 충주시 연수동"
                if up["name"] == "형제상회": short_addr = "대전 서구 용문동"
                
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
            if f'"name": "{up["name"]}"' in line and (up["addr_part"][:5] in line or up["addr_part"] in line):
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
