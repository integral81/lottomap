
import json

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    found = []
    for item in data:
        if "알리바이" in item.get('n', '') and "광산구" in item.get('a', ''):
            if 'pov' not in item:
                found.append(item)
                
    print(f"Total remain without POV: {len(found)}")
    for item in found:
        print(f"R:{item['r']} N:{item['n']} A:{item['a']} L:{item.get('lat')}")

except Exception as e:
    print(f"Error: {e}")
