import json
import os

f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
f_js = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'

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
    with open(f_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated_count = 0
    for b in batch10:
        target_name = b['name']
        # Extract keywords from name (remove parentheses)
        clean_name = target_name.split('(')[0]
        
        found = False
        for s in data:
            s_name = s.get('n', '')
            # Relaxed Name Match: target in source OR source in target
            if (clean_name in s_name or s_name in clean_name):
                # City Check (to avoid cross-region false positives)
                b_city = b['addr'].split(' ')[1] # e.g. "창원시"
                s_addr = s.get('a', '')
                if b_city in s_addr:
                    s['panoid'] = b['panoid']
                    s['pov'] = b['pov'].copy()
                    s['pov']['id'] = b['panoid']
                    updated_count += 1
                    found = True
                    print(f"Updated: {s_name} ({s_addr})")
        
        if not found:
            print(f"[WARN] Not found: {target_name}")

    if updated_count > 0:
        with open(f_json, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        with open(f_js, 'w', encoding='utf-8') as f:
            f.write('const lottoData = ' + json.dumps(data, ensure_ascii=False) + ';')
        print(f"Batch 10: Updated {updated_count} records.")
    else:
        print("Batch 10: No updates made.")

if __name__ == "__main__":
    apply_batch()
