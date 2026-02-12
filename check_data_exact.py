import json

with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=== Exact Data for '왕대박복권방' in 문경 ===")
for s in data:
    if '왕대박' in s['n'] and '문경' in s['a']:
        print(f"Name: [{s['n']}]")
        print(f"Addr: [{s['a']}]")
        print(f"Key: [{s['n']}|{s['a']}]")
        print("-" * 20)
