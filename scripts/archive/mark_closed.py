
import json
import os

target_name = "교통카드판매대"
target_addr_part = "고덕동 210-1"

# 1. Update lotto_data.json
print("Updating lotto_data.json...")
try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    for item in data:
        if target_name in item.get('n', '') and target_addr_part in item.get('a', ''):
            item['isClosed'] = True
            updated_count += 1
            
    if updated_count > 0:
        with open('lotto_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Successfully marked {updated_count} entries as closed in lotto_data.json.")
    else:
        print("No matching entries found in lotto_data.json.")
except Exception as e:
    print(f"Error updating lotto_data.json: {e}")

# 2. Update index.html (ROADVIEW_PRESETS)
print("Updating index.html...")
try:
    with open('index.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_entry = f'            {{ name: "{target_name}", addr: "서울 강동구 고덕동 210-1", isClosed: true, customMessage: "현재 폐점되었습니다 (구서울승합종점앞 가판대)." }},\n'
    
    # Check if already exists, else append
    found = False
    updated_lines = []
    for line in lines:
        if target_name in line and target_addr_part in line:
            updated_lines.append(new_entry)
            found = True
            print("Updated existing entry in index.html.")
        else:
            updated_lines.append(line)
            
    if not found:
        # Insert before ROADVIEW_PRESETS closure if not found
        # Let's find end of presets
        final_lines = []
        appended = False
        for i, line in enumerate(updated_lines):
            final_lines.append(line)
            if 'const ROADVIEW_PRESETS = [' in line and not appended:
                final_lines.append(new_entry)
                appended = True
                print("Added new closed entry to index.html ROADVIEW_PRESETS.")
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.writelines(final_lines)
    else:
        with open('index.html', 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)

except Exception as e:
    print(f"Error updating index.html: {e}")

# 3. Clean up admin_pov.html
print("Cleaning up admin_pov.html...")
try:
    with open('admin_pov.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    skip_mode = False
    removed_count = 0
    for line in lines:
        if '"name": "' + target_name + '"' in line and target_addr_part in line:
            skip_mode = True
            removed_count += 1
            continue
        
        if skip_mode:
            if '"has_coords": true' in line:
                continue
            if '},' in line or '}' in line:
                skip_mode = False
                continue
            continue
        
        new_lines.append(line)
        
    if removed_count > 0:
        with open('admin_pov.html', 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"Removed {removed_count} entries from admin_pov.html.")
except Exception as e:
    print(f"Error updating admin_pov.html: {e}")
