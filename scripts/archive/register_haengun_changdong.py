
import json
import os

# Data for '행운복권방' (창동)
target_name = "행운복권방"
target_addr_part = "도봉구 창동 134-36"
panoid = "1197759123"
pan = 334.7
tilt = -0.9
zoom = 0

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
    for line in lines:
        if f'name: "{target_name}"' in line and ("도봉구" in line or "창동" in line):
            # This should not happen if not already in presets, but just in case
            new_line = f'            {{ name: "{target_name}", addr: "서울 도봉구 창동", panoId: {panoid}, pov: {{ pan: {pan}, tilt: {tilt}, zoom: {zoom} }} }},\n'
            new_lines.append(new_line)
            found = True
            print(f"Found and updated {target_name} (창동) in index.html presets.")
        else:
            new_lines.append(line)
            
    if not found:
        # Add to the end of the list (before the closing bracket)
        final_lines = []
        for i, line in enumerate(new_lines):
            if "];" in line and i > 2600: # Heuristic for presets list end
                final_lines.append(f'            {{ name: "{target_name}", addr: "서울 도봉구 창동", panoId: {panoid}, pov: {{ pan: {pan}, tilt: {tilt}, zoom: {zoom} }} }},\n')
                final_lines.append(line)
                found = True
            else:
                final_lines.append(line)
        new_lines = final_lines

    if found:
        with open('index.html', 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"Added/Updated {target_name} in index.html.")
    else:
        print(f"{target_name} (창동) not found in index.html ROADVIEW_PRESETS and couldn't find insertion point.")
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
        if f'"name": "{target_name}"' in line and ("도봉구" in line or "창동" in line or "134-36" in line):
            skip_mode = True
            count += 1
            print(f"Removing {target_name} (창동) from admin list.")
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
