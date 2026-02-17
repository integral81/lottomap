import json
import os

# Batch 17 Data (22 items)
batch17 = [
    { "name": "참깨열쇠.복권", "addr": "전북 전주시 완산구 용리로 43", "panoid": 1172302536, "pov": { "pan": 357.71, "tilt": 4.98, "zoom": 0 } },
    { "name": "대박천국", "addr": "전북 군산시 가도로 217", "panoid": 1171644308, "pov": { "pan": 260.67, "tilt": 3.93, "zoom": 2 } },
    { "name": "롯데마트", "addr": "전북 군산시 하나운로 43", "panoid": 1172194058, "pov": { "pan": 283.24, "tilt": -10.19, "zoom": 2 } },
    { "name": "농산물직판장", "addr": "전북 군산시 백토로 128", "panoid": 1172192901, "pov": { "pan": 261.48, "tilt": -9.79, "zoom": 2 } },
    { "name": "G(금정)마트휴게실", "addr": "전북 군산시 조촌로 66", "panoid": 1172256365, "pov": { "pan": 129.97, "tilt": 4.79, "zoom": -2 } },
    { "name": "1등명당", "addr": "충남 서천군 장항로 220", "panoid": 1177595058, "pov": { "pan": 223.16, "tilt": -1.62, "zoom": -3 } },
    { "name": "동해복권방", "addr": "강원 강릉시 하평길 40", "panoid": 1194108909, "pov": { "pan": 224.86, "tilt": -2.98, "zoom": 1 } },
    { "name": "한성로또복권", "addr": "강원 정선군 고한9길 40", "panoid": 1195506525, "pov": { "pan": 24.35, "tilt": 8.38, "zoom": -1 } },
    { "name": "영약국", "addr": "충남 금산군 인삼로 104", "panoid": 1179421132, "pov": { "pan": 193.43, "tilt": 3.79, "zoom": -1 } },
    { "name": "777천하명당", "addr": "충남 서천군 충절로 54", "panoid": 1177545967, "pov": { "pan": 180.25, "tilt": 9.54, "zoom": 1 } },
    { "name": "스타복권방", "addr": "충남 논산시 안심로 72", "panoid": 1177120927, "pov": { "pan": 80.30, "tilt": 1.25, "zoom": 3 } },
    { "name": "동명슈퍼", "addr": "강원 속초시 동명동 458-6", "panoid": 1196861285, "pov": { "pan": 269.58, "tilt": 0.30, "zoom": 1 } },
    { "name": "강경복권방", "addr": "충남 논산시 계백로 126-1", "panoid": 1176941418, "pov": { "pan": 122.38, "tilt": 0.02, "zoom": -1 } },
    { "name": "주공24시편의방", "addr": "대전 동구 판암동 204 판암주공아파트2차상가", "panoid": 1201327224, "pov": { "pan": 53.68, "tilt": 4.32, "zoom": 0 } },
    { "name": "천하명당복권방역전점", "addr": "대전 동구 대전로 815", "panoid": 1201475129, "pov": { "pan": 53.45, "tilt": 2.50, "zoom": -2 } },
    { "name": "8888로또", "addr": "대전 서구 월평북로 77", "panoid": 1200997013, "pov": { "pan": 96.60, "tilt": 0.25, "zoom": 0 } },
    { "name": "세종로또복권방", "addr": "세종 금남면 용포리 88-17", "panoid": 1200677245, "pov": { "pan": 263.34, "tilt": 5.63, "zoom": -2 } },
    { "name": "CU(제천역점)", "addr": "충북 제천시 화산동 208-1", "panoid": 1185322618, "pov": { "pan": 190.69, "tilt": 2.99, "zoom": 0 } },
    { "name": "천금복권방", "addr": "충북 청주시 상당구 쇠내로 150-1", "panoid": 1170132121, "pov": { "pan": 235.59, "tilt": -0.57, "zoom: -2 } },
    { "name": "행운의명당로-토토", "addr": "충북 청주시 서원구 모충로 36", "panoid": 1170179519, "pov": { "pan": 168.17, "tilt": 3.29, "zoom: -1 } },
    { "name": "필로또복권", "addr": "충남 서산시 호수공원6로 64", "panoid": 1177737016, "pov": { "pan": 190.83, "tilt": -0.61, "zoom": 0 } },
    { "name": "대소원로또", "addr": "충북 충주시 중원대로 4373 휴게소내 컨테이너", "panoid": 1163997864, "pov": { "pan": 228.60, "tilt": 1.08, "zoom": 0 } }
]

f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
f_js = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'

def load_data():
    with open(f_json, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    # Save JSON (compact for readability)
    with open(f_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    # Save JS
    with open(f_js, 'w', encoding='utf-8') as f:
        f.write('const lottoData = ' + json.dumps(data, ensure_ascii=False) + ';')

def main():
    data = load_data()
    updated_count = 0
    
    print(f"Total shops before: {len(data)}")

    for b in batch17:
        target_name = b['name']
        found = False
        
        for s in data:
            if target_name in s.get('n', ''):
                # Optionally check address if names allow ambiguity
                # For now, trust fuzzy name match within data
                 s['panoid'] = b['panoid']
                 pov_data = b['pov'].copy()
                 pov_data['id'] = b['panoid']
                 s['pov'] = pov_data
                 updated_count += 1
                 found = True
                 break
        
        if not found:
            print(f"Not found in DB: {target_name}")

    save_data(data)
    print(f"Batch 17: Updated {updated_count} shops.")

if __name__ == "__main__":
    main()
