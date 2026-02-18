import json

f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'

with open(f_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

search_parts = ['Goodday', '굿데이', '완월', '채널', '해피', '도소매', '옥좌']

for part in search_parts:
    print(f"--- Part: {part} ---")
    matches = []
    for s in data:
        if part in s.get('n', ''):
            matches.append(s)
    
    for m in matches:
        has_pov = bool(m.get('panoid') or (m.get('pov') and m.get('pov').get('id')))
        print(f"  Name: {m.get('n')}, Addr: {m.get('a')}, Wins: {m.get('wins', 1)}, POV: {has_pov}")

# Also check for 3-win aggregation in admin_pov.html style
print("\n=== Simulating Aggregation for Target Shops ===")
map_obj = {}
for item in data:
    name = item.get('n')
    if not name: continue
    if name not in map_obj:
        map_obj[name] = {
            'name': name, 'addr': item.get('a'), 'wins': 0, 
            'has_pov': bool(item.get('panoid') or (item.get('pov') and item.get('pov').get('id'))),
            'closed': item.get('closed', False)
        }
    map_obj[name]['wins'] += 1
    if item.get('closed'): map_obj[name]['closed'] = True
    if item.get('panoid') or (item.get('pov') and item.get('pov').get('id')):
        map_obj[name]['has_pov'] = True

for part in search_parts:
    print(f"--- Aggregated Part: {part} ---")
    for name, stats in map_obj.items():
        if part in name:
            print(f"  Name: {name}, Total Wins: {stats['wins']}, Registered: {stats['has_pov']}, Closed: {stats['closed']}")
