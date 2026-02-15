
import json

file_path = 'lotto_data.json'
pov_data = {
    "id": "1198106497",
    "pan": 243.3,
    "tilt": -3.8,
    "fov": 40
}

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    count = 0
    for item in data:
        if '오케이상사' in item.get('n', ''):
            item['pov'] = pov_data
            count += 1
            
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Updated {count} entries directly in {file_path}")

except Exception as e:
    print(f"Error: {e}")
