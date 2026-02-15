
import json

target_name = "탑로또"
target_addr_parts = ["상동동", "상문동", "중앙로 1787"]

new_pov = { "id": "1204692322", "pan": 204.23, "tilt": 2.01, "fov": 110 }

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    for item in data:
        name = item.get('n', '')
        addr = item.get('a', '')
        
        # Match '탑로또' in Geoje
        if target_name in name and ("거제" in addr) and any(part in addr for part in target_addr_parts):
            item['pov'] = new_pov
            updated_count += 1
            
    if updated_count > 0:
        with open('lotto_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Successfully updated {updated_count} entries for {target_name} in Geoje.")
    else:
        print(f"No matching shop found for {target_name} in Geoje.")

except Exception as e:
    print(f"Error: {e}")
