import json
import os

f_js = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'

if not os.path.exists(f_js):
    print("Error: lotto_data.js not found")
    exit(1)

with open(f_js, 'r', encoding='utf-8') as f:
    # Extract JSON part from "const lottoData = [...];"
    content = f.read().strip()
    if content.startswith('const lottoData = '):
        json_str = content[len('const lottoData = '):].rstrip(';')
        data = json.loads(json_str)
        
        # Check specific samples
        target_names = ['Goodday', '완월로또', '채널큐', '해피복권', '도소매복권방', '옥좌로또점']
        for name in target_names:
            matches = [s for s in data if name in s.get('n', '')]
            if matches:
                sample = matches[0]
                has_id = sample.get('pov', {}).get('id') if isinstance(sample.get('pov'), dict) else None
                print(f"Name: {sample.get('n')}, Wins: {len(matches)}, POV ID: {has_id}")
            else:
                print(f"Name: {name} - No matches found")
    else:
        print("Error: Invalid JS format")
