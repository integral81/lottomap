
import json

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    count = 0
    for item in data:
        lat = item.get('lat', 0)
        if 35.185 <= lat <= 35.186:
            if "알리바이" in item.get('n', ''):
                print(f"R:{item['r']} N:{item['n']} A:{item['a']} L:{lat} POV:{'pov' in item}")
                count += 1
    print(f"Total found in coord range: {count}")

except Exception as e:
    print(f"Error: {e}")
