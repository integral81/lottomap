import json

f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'

with open(f_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Search terms based on the user's screenshot and list
items_to_check = [
    {"name": "Goodday", "jibun": "반지동 82-16", "road": "반지동 82-16"}, # User's screenshot shows Jibun
    {"name": "완월", "jibun": "", "road": "고운로 175"},
    {"name": "채널큐", "jibun": "", "road": "산호남로 11-1"},
    {"name": "해피", "jibun": "양덕동 17-3", "road": ""},
    {"name": "도소매", "jibun": "광영동 759-4", "road": ""},
    {"name": "옥좌", "jibun": "내외로 10", "road": "내외로 10"}
]

for item in items_to_check:
    print(f"=== Checking for: {item['name']} ===")
    matches = []
    for s in data:
        # Check by name part
        if item['name'] in s.get('n', ''):
            matches.append(s)
            continue
        # Check by address parts
        if (item['jibun'] and item['jibun'] in s.get('a', '')) or (item['road'] and item['road'] in s.get('a', '')):
            matches.append(s)
    
    # Sort and print
    for m in matches:
        print(f"  [{'REG' if m.get('panoid') else 'PENDING'}] Name: {m.get('n')}, Addr: {m.get('a')}, Wins: {m.get('wins', 1)}")
    print("-" * 30)

# Also find shops with 3 wins that don't have POV to see what's currently in the admin list
print("\n=== Current 3-Win Shops without POV (Partial List) ===")
pending_3_wins = [s for s in data if s.get('wins') == 3 and not s.get('panoid')]
for s in pending_3_wins[:20]:
    print(f"  Name: {s.get('n')}, Addr: {s.get('a')}")
