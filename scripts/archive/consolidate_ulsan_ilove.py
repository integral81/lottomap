
import json

# Consolidate target: "아이러브마트복권방" (Latest name)
# Includes old name "아이러브복권방" and all address variants in Ulsan
target_name_final = "아이러브마트복권방"
target_addr_final = "울산 중구 유곡로 19-1"

# POV Data (User provided Pan 177.67 for the mart, 174.28 for the old name. 
# We'll use the latest one 177.67)
pov_data = {
    "id": "1202037951",
    "pan": 177.67,
    "tilt": 0.09,
    "fov": 40
}

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    for item in data:
        name = item.get('n', '')
        addr = item.get('a', '')
        
        # Match "아이러브" + "울산"
        if "아이러브" in name and "울산" in addr:
            # Standardize name and address to the latest one
            item['n'] = target_name_final
            item['a'] = target_addr_final
            item['pov'] = pov_data
            # Set consistent coordinates (User provided coords from martyr were same)
            item['lat'] = 35.5566987509391
            item['lng'] = 129.307118444756
            updated_count += 1
            
    if updated_count > 0:
        with open('lotto_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Successfully consolidated and updated {updated_count} entries for {target_name_final}.")
    else:
        print("No matching shops found for consolidation.")

except Exception as e:
    print(f"Error: {e}")
