
import json

# Define the target shop details
target_name = "CU(대림중앙점)"
target_addr = "서울 영등포구 대림3동 775-7 서초한강아파트"

# User provided
pov_value = {
    "panoid": 1198470102,
    "pov": { "pan": 291.72, "tilt": -2.06, "zoom": -3 }
}

# Standardized format based on previous usage
formatted_pov = {
    "id": str(pov_value["panoid"]),
    "pan": pov_value["pov"]["pan"],
    "tilt": pov_value["pov"]["tilt"],
    "fov": 40 
}

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    
    for item in data:
        # Check name and address. 
        # Using a flexible matching strategy.
        shop_name = item.get('n', '').replace(' ', '')
        search_name = target_name.replace(' ', '')
        
        shop_addr = item.get('a', '').replace(' ', '')
        # Extract core parts of address for matching
        # "서울 영등포구 대림3동 775-7" -> "대림", "775-7"
        
        is_name_match = search_name in shop_name
        
        # Address matching: check for significant part "775-7"
        is_addr_match = "775-7" in shop_addr
             
        if is_name_match and is_addr_match:
            item['pov'] = formatted_pov
            updated_count += 1
            print(f"Updated POV for: {item.get('n')} - {item.get('a')}")
            
    if updated_count > 0:
        with open('lotto_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Successfully updated {updated_count} entries.")
    else:
        print("No matching shops found.")

except Exception as e:
    print(f"Error: {e}")
