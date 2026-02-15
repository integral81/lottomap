
import json

target_name = "알리바이"
target_addr_variants = ["신가동 986-4", "수완로 253"]

pov_data = {
    "id": "1199874246",
    "pan": 109.05,
    "tilt": -8.24,
    "fov": 110 # wide
}

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    for item in data:
        name = item.get('n', '')
        addr = item.get('a', '')
        
        # Match "알리바이" in Gwangju Gwangsan-gu
        if target_name in name and ("광산구" in addr):
            # Check if it's the Shinga-dong/Suwan-ro shop (based on current coords or addr)
            # Suwan-ro 253 and Shinga-dong 986-4 use very similar coords
            lat = item.get('lat', 0)
            if 35.185 < lat < 35.186:
                item['pov'] = pov_data
                updated_count += 1
            
    if updated_count > 0:
        with open('lotto_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Successfully updated {updated_count} entries for {target_name} (Gwangju Alibi).")
    else:
        print(f"No matching shop found for {target_name}.")

except Exception as e:
    print(f"Error: {e}")
