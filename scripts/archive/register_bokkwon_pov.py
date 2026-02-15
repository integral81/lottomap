
import json

file_path = 'lotto_data.json'
target_name = '복권백화점'
target_addr_partial = '파주시 금촌' # Using partial match to be safe

pov_data = {
    "id": "1202862939",
    "pan": 103.0,
    "tilt": -3.6,
    "fov": 40
}

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    count = 0
    updated_items = []
    
    for item in data:
        name_match = target_name in item.get('n', '')
        addr_match = target_addr_partial in item.get('a', '')
        
        if name_match and addr_match:
            item['pov'] = pov_data
            count += 1
            updated_items.append(f"{item.get('n')} ({item.get('a')})")
            
    if count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Successfully updated {count} entries for '{target_name}'.")
        for item in updated_items:
            print(f" - Updated: {item}")
    else:
        print(f"No matching shop found for '{target_name}' using partial address '{target_addr_partial}'.")

except Exception as e:
    print(f"Error: {e}")
