
import json

# Target shop details
target_name = "로또천국"
target_addr = "충북 충주시 칠금동 849 충주공영버스터미널1층 터미널매점"

# POV data from user
pov_data = {
    "id": "1164453210",
    "pan": 303.44,
    "tilt": 2.25,
    "fov": 40
}

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    
    for item in data:
        # Match by name and partial address
        if target_name in item.get('n', '') and '칠금동 849' in item.get('a', ''):
            item['pov'] = pov_data
            updated_count += 1
            print(f"Updated: {item.get('n')} - {item.get('a')}")
    
    if updated_count > 0:
        with open('lotto_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\nSuccessfully updated {updated_count} entries.")
    else:
        print("No matching shops found.")

except Exception as e:
    print(f"Error: {e}")
