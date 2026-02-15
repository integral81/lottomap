
import json
import os

# Data for '하당복권방'
target_name = "하당복권방"
target_addr_part = "옥암" # Using partial to match both old and new addresses
panoid = "1192600420"
pan = 304.76
tilt = 1.45
zoom = -3

pov_data = {
    "id": panoid,
    "pan": pan,
    "tilt": tilt,
    "zoom": zoom
}

# 1. Update lotto_data.json
print("Updating lotto_data.json...")
try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    for item in data:
        if target_name == item.get('n') and target_addr_part in item.get('a', ''):
            item['pov'] = pov_data
            updated_count += 1
            
    if updated_count > 0:
        with open('lotto_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Successfully updated {updated_count} entries in lotto_data.json.")
    else:
        print("No matching entries found in lotto_data.json.")
except Exception as e:
    print(f"Error updating lotto_data.json: {e}")

# 2. Update index.html (ROADVIEW_PRESETS)
print("Updating index.html...")
try:
    with open('index.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    found = False
    new_lines = []
    # { name: "하당복권방", addr: "전남 목포시 옥암동", panoId: 1192538904, pov: { pan: 41.70, tilt: -0.67, zoom: -3 } },
    for line in lines:
        if 'name: "하당복권방"' in line:
            new_line = f'            {{ name: "{target_name}", addr: "전남 목포시 옥암동", panoId: {panoid}, pov: {{ pan: {pan}, tilt: {tilt}, zoom: {zoom} }} }},\n'
            new_lines.append(new_line)
            found = True
            print("Found and updated 하당복권방 in index.html presets.")
        else:
            new_lines.append(line)
            
    if found:
        with open('index.html', 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
    else:
        print("하당복권방 not found in index.html ROADVIEW_PRESETS.")
except Exception as e:
    print(f"Error updating index.html: {e}")

# 3. Clean up admin_pov.html (allMissingShops)
print("Updating admin_pov.html...")
try:
    with open('admin_pov.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    skip_mode = False
    count = 0
    for line in lines:
        if '"name": "하당복권방"' in line:
            skip_mode = True
            count += 1
            continue 
        
        if skip_mode:
            if '"has_coords": true' in line:
                continue
            if '},' in line or '}' in line:
                skip_mode = False
                continue
            continue
            
        new_lines.append(line)
    
    if count > 0:
        with open('admin_pov.html', 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"Removed {count} entries from admin_pov.html.")
except Exception as e:
    print(f"Error updating admin_pov.html: {e}")
