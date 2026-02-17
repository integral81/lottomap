import json
import os

# Batch 18 Data (12 items)
batch18 = [
    { "name": "명동역5번출구가판", "addr": "서울 중구 퇴계로 115", "panoid": 1198729421, "pov": { "pan": 334.09, "tilt": -3.01, "zoom": 2 } },
    { "name": "가판100호", "addr": "서울 중구 을지로 113-4", "panoid": 1198732333, "pov": { "pan": 30.96, "tilt": -9.37, "zoom": -2 } },
    { "name": "꿈이현실로", "addr": "서울 중구 청계천로 182", "panoid": 1198688984, "pov": { "pan": 250.69, "tilt": 3.08, "zoom": 1 } },
    { "name": "아현역3번출구앞가판점", "addr": "서울 마포구 마포대로 249 아현산업정보학교 아현역3번출구앞", "panoid": 1197537359, "pov": { "pan": 186.25, "tilt": 5.73, "zoom": 3 } },
    { "name": "샛별복권방", "addr": "서울 중구 동호로10길 12", "panoid": 1198891820, "pov": { "pan": 118.62, "tilt": -1.30, "zoom": -3 } },
    { "name": "그랜드마트앞가판점", "addr": "서울 마포구 신촌로 94", "panoid": 1197520772, "pov": { "pan": 272.06, "tilt": 3.49, "zoom": -3 } },
    { "name": "제일식품", "addr": "서울 서대문구 증가로 143", "panoid": 1198136579, "pov": { "pan": 188.18, "tilt": -1.68, "zoom": -2 } },
    { "name": "복권천국방", "addr": "서울 마포구 서교동 480-1", "panoid": 1197902490, "pov": { "pan": 161.78, "tilt": 1.24, "zoom": -2 } },
    { "name": "복권천하", "addr": "서울 강북구 월계로7나길 23", "panoid": 1197620206, "pov": { "pan": 212.05, "tilt": 1.96, "zoom": -3 } },
    { "name": "교통카드", "addr": "서울 서초구 강남대로 517", "panoid": 1197784045, "pov": { "pan": 216.62, "tilt": -8.29, "zoom": 0 } },
    { "name": "보경식품", "addr": "서울 강북구 미아동 207-2", "panoid": 1197862466, "pov": { "pan": 261.64, "tilt": -0.62, "zoom": 0 } },
    { "name": "행운대박복권", "addr": "서울 영등포구 영신로19길 8-1", "panoid": 1198468345, "pov": { "pan": 309.21, "tilt": -0.50, "zoom": -3 } }
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

def match_target(data, batch_item):
    target_name = batch_item['name']
    # Extract a unique part of address for safer matching
    # e.g. "서울 중구 퇴계로 115" -> "퇴계로 115"
    addr_parts = batch_item['addr'].split(' ')
    if len(addr_parts) > 2:
        target_addr_part = f"{addr_parts[2]} {addr_parts[3]}" if len(addr_parts) > 3 else addr_parts[2]
    else:
        target_addr_part = batch_item['addr']

    for s in data:
        # 1. Name Match (Loose)
        name_match = (target_name.replace(' ', '') in s.get('n', '').replace(' ', '')) or \
                     (s.get('n', '').replace(' ', '') in target_name.replace(' ', ''))
        
        # 2. Address Match (Crucial for generic names)
        addr_match = target_addr_part in s.get('a', '')

        if name_match and addr_match:
            return s
    return None

def main():
    data = load_data()
    updated_count = 0
    not_found = []

    print(f"Total shops before: {len(data)}")

    for b in batch18:
        s = match_target(data, b)
        if s:
            s['panoid'] = b['panoid']
            pov_data = b['pov'].copy()
            pov_data['id'] = b['panoid']
            s['pov'] = pov_data
            updated_count += 1
            print(f"Updated: {s['n']} ({s.get('a')})")
        else:
            not_found.append(b['name'])
            # Try to print potential candidates
            print(f"[WARN] Not found: {b['name']} ({b['addr']})")
    
    save_data(data)
    print(f"Batch 18: Updated {updated_count} / {len(batch18)} shops.")
    if not_found:
        print("Missing shops:", not_found)

if __name__ == "__main__":
    main()
