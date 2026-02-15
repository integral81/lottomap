
import json

# Target shop details
target_name = "GS25(두정메트로점)"
target_addr = "충남 천안시 서북구 성정동 1451"

# POV data from resolved URL
pov_data = {
    "id": "1195535891",
    "pan": 24.4,
    "tilt": 0.5,
    "fov": 40  # Standard FOV (zoom 0 = default view)
}

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    
    for item in data:
        # Match by name and address
        if target_name in item.get('n', '') and '성정동 1451' in item.get('a', ''):
            item['pov'] = pov_data
            updated_count += 1
            print(f"Updated: {item.get('n')} - {item.get('a')}")
    
    if updated_count > 0:
        with open('lotto_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n✅ Successfully updated {updated_count} entries.")
    else:
        print("❌ No matching shops found.")

except Exception as e:
    print(f"Error: {e}")
