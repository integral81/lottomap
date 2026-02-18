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
    
    # Target: Chamkkae Key Lottery
    # New User Request: pan 5.05, tilt -2.74
    target_name = "참깨열쇠"
    new_pov = { "id": 1172302536, "pan": 5.05, "tilt": -2.74, "zoom": 0 }
    
    updated = False
    for s in data:
        if target_name in s.get('n', ''):
             print(f"Updating {s['n']} POV...")
             print(f"Old: {s.get('pov')}")
             s['pov'] = new_pov
             s['panoid'] = 1172302536 # Ensure matches
             print(f"New: {s.get('pov')}")
             updated = True
             break
    
    if updated:
        save_data(data)
        print("Update successful.")
    else:
        print("Shop not found.")

if __name__ == "__main__":
    main()
