import json
import os

# Paths
db_path = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
js_path = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'

with open(db_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 1. Mark Seonbong as closed
upd_cnt = 0
for s in data:
    if '선봉로또' in s.get('n', '') and '삼산동 1468-6' in s.get('a', ''):
        s['closed'] = True
        upd_cnt += 1

if upd_cnt > 0:
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=0, separators=(',', ':'), ensure_ascii=False)
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write('var lottoData = ' + json.dumps(data, ensure_ascii=False, indent=0, separators=(',', ':')) + ';')
    print(f'DB: Marked {upd_cnt} entries for 선봉로또 as closed.')
else:
    print('No matching entries found for 선봉로또.')
