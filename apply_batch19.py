import json
import os

f_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
f_js = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'

def load_data():
    with open(f_json, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(f_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    with open(f_js, 'w', encoding='utf-8') as f:
        f.write('const lottoData = ' + json.dumps(data, ensure_ascii=False) + ';')

def main():
    data = load_data()
    updated_count = 0

    # 1. Register Samnye Lotto
    samnye = { "name": "삼례로또복권", "addr": "전북 완주군 동학로 32", "panoid": 1179832694, "pov": { "pan": 113.30, "tilt": 3.07, "zoom": 0 } }
    
    found_samnye = False
    for s in data:
        if "삼례로또복권" in s.get('n', ''):
             s['panoid'] = samnye['panoid']
             pov_data = samnye['pov'].copy()
             pov_data['id'] = samnye['panoid']
             s['pov'] = pov_data
             updated_count += 1
             found_samnye = True
             print(f"Registered: {s['n']}")
             break
    
    if not found_samnye:
        print("[WARN] Samnye Lotto not found in DB!")

    # 2. Close Byeoksan Blooming
    target_blooming = "로또복권벽산블루밍"
    target_addr = "갈마로 262"
    
    found_blooming = False
    for s in data:
        if target_blooming in s.get('n', '') and target_addr in s.get('a', ''):
            if not s.get('closed'):
                s['closed'] = True
                updated_count += 1
                print(f"Marked as CLOSED: {s['n']}")
            else:
                print(f"Already CLOSED: {s['n']}")
            found_blooming = True
            break
            
    if not found_blooming:
         print(f"[WARN] {target_blooming} not found in DB!")

    if updated_count > 0:
        save_data(data)
        print(f"Total updates: {updated_count}")
    else:
        print("No changes needed.")

if __name__ == "__main__":
    main()
