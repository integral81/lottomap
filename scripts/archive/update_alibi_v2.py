
import json

provider_name = "알리바이"
# Main shop addresses: 수완로 253, 신가동 986-4, etc.
pov_data = {
    "id": "1199874246",
    "pan": 109.05,
    "tilt": -8.24,
    "fov": 110
}

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    for item in data:
        name = item.get('n', '')
        addr = item.get('a', '')
        lat = item.get('lat', 0)
        
        # Match main Alibi in Gwangsan-gu
        if "알리바이" in name and "광산구" in addr:
            # Check for Shinga/Suwan location
            if ("신가동" in addr or "수완" in addr or (35.185 <= lat <= 35.186)):
                item['pov'] = pov_data
                updated_count += 1
            
    if updated_count > 0:
        with open('lotto_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Successfully updated {updated_count} entries for the main Alibi shop.")
    else:
        print("No matches found.")

except Exception as e:
    print(f"Error: {e}")
