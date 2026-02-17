import json
import os

# Batch 20 (13 items)
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

# Batch 21 (7 items)
batch21 = [
    { "name": "태일이엔지", "addr": "경기 수원시 권선구 권선동 1188 한양아파트상가 107호", "panoid": 1199997947, "pov": { "pan": 193.22, "tilt": 4.22, "zoom": 3 } },
    { "name": "다드림복권", "addr": "경기 김포시 월하로 930 1층 101호", "panoid": 1203372470, "pov": { "pan": 222.57, "tilt": -0.30, "zoom": 2 } },
    { "name": "대선세무경영사무소", "addr": "경기 안산시 상록구 석호로 189 101호", "panoid": 1204010688, "pov": { "pan": 35.01, "tilt": 2.51, "zoom": 0 } },
    { "name": "월드컵", "addr": "경기 수원시 팔달구 우만동 519-3", "panoid": 1199821926, "pov": { "pan": 215.93, "tilt": 1.25, "zoom": 0 } },
    { "name": "대박천하", "addr": "인천 연수구 새말로 37 103호", "panoid": 1200638747, "pov": { "pan": 57.93, "tilt": 6.28, "zoom": -3 } },
    { "name": "나눔로또한대점", "addr": "경기 안산시 상록구 중보로 57 한양대프라자106호", "panoid": 1203907732, "pov": { "pan": 237.21, "tilt": -0.67, "zoom": 2 } },
    { "name": "1등 복권", "addr": "경기 시흥시 배곧4로 32-27 105호", "panoid": 1175940131, "pov": { "pan": 297.94, "tilt": -0.86, "zoom": -1 } }
]

# Batch 22 (8 items)
batch22 = [
    { "name": "달성로또복권판매소", "addr": "충남 아산시 온천대로 1531", "panoid": 1176312793, "pov": { "pan": 356.92, "tilt": 1.94, "zoom": -1 } },
    { "name": "불티나", "addr": "강원 춘천시 후석로462번길 94-1", "panoid": 1196932660, "pov": { "pan": 175.45, "tilt": -1.62, "zoom": 1 } },
    { "name": "로또매점", "addr": "충남 당진시 송산로 723", "panoid": 1172172781, "pov": { "pan": 273.79, "tilt": -0.20, "zoom": 3 } },
    { "name": "둔포로또판매점", "addr": "충남 아산시 둔포면 둔포리 479-1 둔포로또판매점", "panoid": 1177065529, "pov": { "pan": 289.02, "tilt": 2.16, "zoom": 1 } },
    { "name": "로또.토토.블루베리", "addr": "경기 평택시 안현로서6길 7 대건빌딩 105호", "panoid": 1197499447, "pov": { "pan": 214.11, "tilt": 4.05, "zoom": 3 } },
    { "name": "프림", "addr": "경기 평택시 서해로 1402 GS편의점 내", "panoid": 1197405524, "pov": { "pan": 40.83, "tilt": -1.58, "zoom": 3 } },
    { "name": "명당로또", "addr": "경기 이천시 청백리로84번길 23 104호", "panoid": 1175129802, "pov": { "pan": 180.58, "tilt": 0.29, "zoom": 1 } },
    { "name": "황금 복권방", "addr": "경기 용인시 기흥구 상하동 483-1 어정프라자 103호", "panoid": 1199721821, "pov": { "pan": 237.93, "tilt": 1.96, "zoom": -3 } }
]

combined_batch = batch20 + batch21 + batch22

f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
f_js = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'

def load_data():
    try:
        with open(f_json, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return []

def save_data(data):
    try:
        with open(f_json, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        with open(f_js, 'w', encoding='utf-8') as f:
            f.write('const lottoData = ' + json.dumps(data, ensure_ascii=False) + ';')
        print("Data saved successfully.")
    except Exception as e:
        print(f"Error saving data: {e}")

def main():
    data = load_data()
    updated_count = 0
    not_found = []

    print(f"Total shops before: {len(data)}")

    for b in combined_batch:
        target_name = b['name']
        found = False
        
        # Address keyword for better matching
        addr_parts = b['addr'].split(' ')
        addr_keyword = addr_parts[2] if len(addr_parts) > 2 else ""

        for s in data:
            n1 = target_name.replace(' ', '')
            n2 = s.get('n', '').replace(' ', '')
            
            if (n1 in n2 or n2 in n1):
                 # Confirmatory check if generic name or mismatch risk
                 if "복권" in n1 and len(n1) < 5 and addr_keyword and addr_keyword not in s.get('a', ''):
                     continue 
                
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
    print(f"Combined Batch (20+21+22): Updated {updated_count} / {len(combined_batch)} shops.")
    if not_found:
        print("Missing:", not_found)

if __name__ == "__main__":
    main()
