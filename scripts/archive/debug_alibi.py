
import json

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for item in data:
        if "알리바이" in item.get('n', '') and 'pov' not in item:
            print(f"R:{item['r']} N:{item['n']} A:{item['a']} L:{item.get('lat')} G:{item.get('lng')}")

except Exception as e:
    print(f"Error: {e}")
