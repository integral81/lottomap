import json
import os

# Batch 20 Data (13 items)
batch20 = [
    { "name": "보은로또판매점", "addr": "충북 보은군 보은로 167 주유소", "panoid": 1185150050, "pov": { "pan": 358.23, "tilt": 1.87, "zoom": 1 } },
    { "name": "오창중앙복권", "addr": "충북 청주시 청원구 중심상업로 47 103호", "panoid": 1169865274, "pov": { "pan": 260.64, "tilt": 1.36, "zoom": -1 } },
    { "name": "CU(횡성점)", "addr": "강원 횡성군 횡성읍 읍하리118-1", "panoid": 1197181644, "pov": { "pan": 296.12, "tilt": 1.53, "zoom": -1 } },
    { "name": "콘테인복권판매점", "addr": "충남 천안시 동남구 청수11로 13-11 건물 뒤편 콘테인커피숍 내", "panoid": 1194698267, "pov": { "pan": 83.39, "tilt": -6.45, "zoom": 3 } },
    { "name": "로또명당금왕점", "addr": "충북 음성군 탑골길 55 세븐일레븐 금왕점", "panoid": 1166726062, "pov": { "pan": 235.52, "tilt": -1.86, "zoom": 1 } },
    { "name": "407억당첨가판점", "addr": "강원 춘천시 중앙로2가 27-1 국민은행앞 가판", "panoid": 1195852185, "pov": { "pan": 100.19, "tilt": -3.51, "zoom": -1 } },
    { "name": "금도끼복권방", "addr": "경기 양평군 용문로 812", "panoid": 1176140330, "pov": { "pan": 164.45, "tilt": -3.91, "zoom": 1 } },
    { "name": "현대할인마트", "addr": "경기 이천시 신둔면 수광리 312-4", "panoid": 1174682704, "pov": { "pan": 65.64, "tilt": 2.99, "zoom": 0 } },
    { "name": "포유25다농점", "addr": "경기 오산시 운천로 80-5 거성그린프라자114호", "panoid": 1174696254, "pov": { "pan": 187.76, "tilt": 5.16, "zoom": -1 } },
    { "name": "현리행운복권방", "addr": "경기 가평군 조종희망로 14 엄마손해장국", "panoid": 1175787970, "pov": { "pan": 174.27, "tilt": 6.82, "zoom": -1 } },
    { "name": "로또복권짱", "addr": "경기 용인시 처인구 마평동 582-3", "panoid": 1198953405, "pov": { "pan": 63.36, "tilt": 2.43, "zoom": 1 } },
    { "name": "오로라복권방", "addr": "서울 광진구 뚝섬로 625 국민은행자양동지점 50m", "panoid": 1196541229, "pov": { "pan": 346.36, "tilt": 3.14, "zoom": 2 } },
    { "name": "둔전행운복권방", "addr": "경기 용인시 처인구 포곡로 110", "panoid": 1199431220, "pov": { "pan": 151.75, "tilt": 5.86, "zoom": 2 } }
]

f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
f_js = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'

def load_data():
    with open(f_json, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    # Save JSON
    with open(f_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    # Save JS
    with open(f_js, 'w', encoding='utf-8') as f:
        f.write('const lottoData = ' + json.dumps(data, ensure_ascii=False) + ';')

def main():
    try:
        data = load_data()
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    updated_count = 0
    not_found = []

    print(f"Total shops before: {len(data)}")

    for b in batch20:
        target_name = b['name']
        found = False
        
        # Simple Logic: Name + Local Address check
        # "강원 춘천시 중앙로2가 27-1 국민은행앞 가판" -> "중앙로2가" check
        addr_keyword = b['addr'].split(' ')[2] if len(b['addr'].split(' ')) > 2 else ""

        for s in data:
            if target_name in s.get('n', ''):
                # If name matches, check address loosely to confirm
                if addr_keyword == "" or addr_keyword in s.get('a', ''):
                     s['panoid'] = b['panoid']
                     pov_data = b['pov'].copy()
                     pov_data['id'] = b['panoid']
                     s['pov'] = pov_data
                     updated_count += 1
                     found = True
                     print(f"Updated: {s['n']}")
                     break
        
        if not found:
            not_found.append(b['name'])
            print(f"[WARN] Not found: {target_name}")

    save_data(data)
    print(f"Batch 20: Updated {updated_count} / {len(batch20)} shops.")
    if not_found:
        print("Missing:", not_found)

if __name__ == "__main__":
    main()
