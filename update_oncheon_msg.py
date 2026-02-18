import json
import os

target_name = "세븐일레븐부산온천장역점"
target_msg = "📍 매장은 온천장역 역사(지하) 내부에 있습니다."

db_path = 'lotto_data.json'
js_path = 'lotto_data.js'
html_path = 'index.html'

try:
    with open(db_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    cnt = 0
    t_shop = None
    for s in data:
        if s.get('n') == target_name:
            s['customMessage'] = target_msg
            cnt += 1
            t_shop = s

    if cnt > 0:
        with open(db_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=0, separators=(',', ':'))
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write('var lottoData = ' + json.dumps(data, ensure_ascii=False, indent=0, separators=(',', ':')) + ';')
        print(f"Updated {cnt} entries in DB.")

        if os.path.exists(html_path) and t_shop:
            with open(html_path, 'r', encoding='utf-8') as f:
                html = f.read()
            
            p = t_shop.get('pov', {})
            pid = p.get('id') or p.get('panoid')
            pst = f'{{ name: "{target_name}", addr: "{t_shop["a"]}", panoid: {pid}, pov: {{ pan: {p.get("pan",0)}, tilt: {p.get("tilt",0)}, zoom: {p.get("zoom",0)} }}, customMessage: "{target_msg}" }},'
            
            idx = html.find('const ROADVIEW_PRESETS = [')
            if idx != -1:
                br = html.find('[', idx)
                html = html[:br+1] + '\n            ' + pst + html[br+1:]
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(html)
                print("HTML preset added.")
    else:
        print("Shop not found.")
except Exception as e:
    print(e)
