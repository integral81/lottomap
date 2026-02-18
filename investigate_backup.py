import json

print("Investigating '온천장' in lotto_data.current.bak...")
try:
    with open('lotto_data.current.bak', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for s in data:
        if '온천장' in s.get('n', ''):
            print(f"Name: '{s['n']}'")
            print(f"POV: {s.get('pov')}")
            print("-" * 20)
            
except Exception as e:
    print(e)
