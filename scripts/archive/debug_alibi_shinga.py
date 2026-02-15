
import json

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    count = 0
    for item in data:
        if "알리바이" in item.get('n', '') and "신가" in item.get('a', ''):
            print(f"R:{item['r']} N:{item['n']} A:{item['a']} L:{item.get('lat')} POV:{'pov' in item}")
            count += 1
    print(f"Total found with '신가': {count}")

except Exception as e:
    print(f"Error: {e}")
