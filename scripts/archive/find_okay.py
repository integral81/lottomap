
import json

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    found = []
    for item in data:
        if '오케이상사' in item.get('n', '') or '오케이' in item.get('n', ''):
            found.append(item)
            
    print(f"Found {len(found)} entries matching '오케이'.")
    for fp in found:
        print(f"Name: {fp.get('n')}, Addr: {fp.get('a')}")

except Exception as e:
    print(f"Error: {e}")
