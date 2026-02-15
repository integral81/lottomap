
import json
import os

# Data for '행운복권방' (인제)
target_name = "행운복권방"
target_addr_part = "인제군 북면 원통리 681-5"
target_addr_preset = "강원 인제군 북면"
panoid = "1196203792"
pan = 216.8
tilt = -5.2
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
        if target_name == item.get('n') and ("인제" in item.get('a', '') and "북면" in item.get('a', '')):
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
        if f'name: "{target_name}"' in line and (target_addr_preset in line or "681-5" in line):
            new_line = f'            {{ name: "{target_name}", addr: "{target_addr_preset}", panoId: {panoid}, pov: {{ pan: {pan}, tilt: {tilt}, zoom: {zoom} }} }},\n'
            new_lines.append(new_line)
            found = True
            print(f"Found and updated {target_name} (인제) in index.html presets.")
        else:
            new_lines.append(line)
            
    if found:
        with open('index.html', 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
    else:
        print(f"{target_name} (인제) not found in index.html ROADVIEW_PRESETS.")
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
        if f'"name": "{target_name}"' in line and ("인제" in line or "북면" in line or "681-5" in line):
            skip_mode = True
            count += 1
            print(f"Removing {target_name} (인제) from admin list.")
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
