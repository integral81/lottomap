import json
import os

target_chunhyang = {
    "name": "춘향로또",
    "addr": "전북 남원시 동림로 102-1",
    "pov": { "id": 1205553870, "pan": 55.63, "tilt": 6.68, "zoom": 1 }
}

target_seomun = {
    "name": "복권판매소",
    "addr": "대구 서구 국채보상로 438",
    "pov": { "id": 1201562079, "pan": 249.70, "tilt": 7.83, "zoom": 1 }
}

db_path = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
js_path = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'
html_path = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\index.html'

def update_db():
    try:
        with open(db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        upd_cnt = 0
        for s in data:
            # 1. Chunhyang Lotto
            if "춘향로또" in s.get('n', ''):
                s['pov'] = target_chunhyang['pov']
                upd_cnt += 1
                print(f"Updated Chunhyang Lotto: {s['n']}")
            
            # 2. Bokkwon Panmaeso (Seomun Big Market)
            if "복권판매소" in s.get('n', '') and "국채보상로 438" in s.get('a', ''):
                s['pov'] = target_seomun['pov']
                upd_cnt += 1
                print(f"Updated Seomun Big Market: {s['n']}")

        if upd_cnt > 0:
            with open(db_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=0, separators=(',', ':'), ensure_ascii=False)
            
            with open(js_path, 'w', encoding='utf-8') as f:
                f.write('var lottoData = ' + json.dumps(data, ensure_ascii=False, indent=0, separators=(',', ':')) + ';')
            
            print(f"Successfully updated {upd_cnt} entries in DB.")
        else:
            print("No matching shops found.")

    except Exception as e:
        print(f"Error updating DB: {e}")

def update_html():
    # Adding to presets in index.html for quick access
    try:
        if os.path.exists(html_path):
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()

            new_presets = []
            new_presets.append(f'{{ name: "{target_chunhyang["name"]}", addr: "{target_chunhyang["addr"]}", panoid: {target_chunhyang["pov"]["id"]}, pov: {{ pan: {target_chunhyang["pov"]["pan"]}, tilt: {target_chunhyang["pov"]["tilt"]}, zoom: {target_chunhyang["pov"]["zoom"]} }} }},')
            new_presets.append(f'{{ name: "{target_seomun["name"]}", addr: "{target_seomun["addr"]}", panoid: {target_seomun["pov"]["id"]}, pov: {{ pan: {target_seomun["pov"]["pan"]}, tilt: {target_seomun["pov"]["tilt"]}, zoom: {target_seomun["pov"]["zoom"]} }} }},')
            
            preset_block = "\n            ".join(new_presets)
            
            idx = content.find('const ROADVIEW_PRESETS = [')
            if idx != -1:
                bracket_pos = content.find('[', idx)
                new_content = content[:bracket_pos+1] + '\n            ' + preset_block + content[bracket_pos+1:]
                
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print("Added to HTML presets.")
            else:
                print("Could not find ROADVIEW_PRESETS in index.html")
    except Exception as e:
        print(f"Error updating HTML: {e}")

if __name__ == "__main__":
    update_db()
    update_html()
