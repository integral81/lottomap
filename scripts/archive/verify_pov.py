
import json

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    count = 0
    for item in data:
        if '오케이상사' in item.get('n', '') and 'pov' in item:
            count += 1
            print(f"Verified POV for: {item.get('n')} - {item.get('pov')}")
            
    print(f"Total entries with POV for '오케이상사': {count}")

except Exception as e:
    print(f"Error: {e}")
