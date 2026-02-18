import json
import os

# Paths
db_path = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
js_path = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'
html_path = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\index.html'

with open(db_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 1. Update Bugang (부강 돈벼락)
bugang_pov = {'id': 1204485832, 'pan': 41.35, 'tilt': 3.80, 'zoom': 2}
upd_cnt = 0
for s in data:
    if '부강 돈벼락' in s.get('n', '') and '물금로 41' in s.get('a', ''):
        s['pov'] = bugang_pov
        upd_cnt += 1

if upd_cnt > 0:
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=0, separators=(',', ':'), ensure_ascii=False)
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write('var lottoData = ' + json.dumps(data, ensure_ascii=False, indent=0, separators=(',', ':')) + ';')
    print(f'DB: Updated {upd_cnt} entries for 부강 돈벼락.')

# 2. Update index.html
if os.path.exists(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    preset = '{ name: "부강 돈벼락", addr: "경남 양산시 물금로 41", panoId: 1204485832, pov: { pan: 41.35, tilt: 3.80, zoom: 2 } },'
    idx = html.find('const ROADVIEW_PRESETS = [')
    if idx != -1:
        bracket = html.find('[', idx)
        html = html[:bracket+1] + '\n            ' + preset + html[bracket+1:]
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print('HTML: Updated presets.')
