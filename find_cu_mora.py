import json

with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Searching for 'CU' and '421' in Busan...")
for shop in data:
    if '421' in shop['a'] and '부산' in shop['a'] and 'CU' in shop['n']:
         print(f"Found: {shop['n']} / {shop['a']} / Wins: {shop.get('1st', 0)}")
         if 'pov' in shop:
             print(f"  Existing POV: {shop['pov']}")
         else:
             print("  NO POV")
