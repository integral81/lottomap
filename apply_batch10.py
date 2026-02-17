import json
import os

path_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
path_js = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'

batch10 = [
    {"name": "Goodday복권전문점", "addr": "경남 창원시 성산구 반지동 82-16", "panoid": 1204230685, "pov": {"pan": 313.55, "tilt": 4.31, "zoom": -3}},
    {"name": "완월로또", "addr": "경남 창원시 마산합포구 고운로 175 한미초록빌라 세븐일레븐 내", "panoid": 1204767224, "pov": {"pan": 324.20, "tilt": 9.81, "zoom": -1}},
    {"name": "채널큐", "addr": "경남 창원시 마산합포구 산호남로 11-1", "panoid": 1204699861, "pov": {"pan": 32.90, "tilt": 3.33, "zoom": -3}},
    {"name": "해피복권", "addr": "경남 창원시 마산회원구 양덕동 17-3 양덕편의점 내", "panoid": 1204617908, "pov": {"pan": 57.36, "tilt": -8.23, "zoom": -3}},
    {"name": "도소매복권방", "addr": "전남 광양시 광영동 759-4", "panoid": 1205328607, "pov": {"pan": 127.71, "tilt": 4.93, "zoom": -2}},
    {"name": "천하명당(팔용점)", "addr": "경남 창원시 의창구 사화로 26", "panoid": 1205179331, "pov": {"pan": 29.83, "tilt": 0.95, "zoom": -1}},
    {"name": "복권나라동성점", "addr": "전남 순천시 연향번영길 94 동성아파트 상가113호", "panoid": 1205415089, "pov": {"pan": 93.17, "tilt": -3.98, "zoom": -2}},
    {"name": "알짜마트왕지점", "addr": "전남 순천시 왕궁길 60 중흥파크상가 309-101호", "panoid": 1205227059, "pov": {"pan": 66.59, "tilt": 8.26, "zoom": -2}},
    {"name": "제철로또대리점", "addr": "전남 광양시 광장로 125 시티프라자A동116호", "panoid": 1205201774, "pov": {"pan": 172.43, "tilt": -1.62, "zoom": 3}}
]

def apply_batch():
    if not os.path.exists(path_json):
        print(f"Error: {path_json} not found")
        return

    with open(path_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated_count = 0
    for s in data:
        for b in batch10:
            if b['name'] in s.get('n', '') and (b['addr'][:10] in s.get('a', '')):
                s['panoid'] = b['panoid']
                s['pov'] = b['pov']
                updated_count += 1
    
    if updated_count > 0:
        with open(path_json, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Updated {updated_count} records in {path_json}")
        
        with open(path_js, 'w', encoding='utf-8') as f:
            f.write('const lottoData = ' + json.dumps(data, ensure_ascii=False) + ';')
        print(f"Regenerated {path_js}")
    else:
        print("No matches found for Batch 10")

if __name__ == "__main__":
    apply_batch()
