import json

with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Searching for '하늘' in shop names...")
found = False
for shop in data:
    if '하늘' in shop['n']:
        print(f"Found: {shop['n']} / {shop['a']} / Wins: {shop.get('1st', 0)}")
        found = True

if not found:
    print("No shop found with '하늘' in verification list.")
    
print("\nSearching for '421' (Baekyang-daero hint) in addresses...")
for shop in data:
    if '421' in shop['a'] and '부산' in shop['a']:
        print(f"Address Match: {shop['n']} / {shop['a']}")
