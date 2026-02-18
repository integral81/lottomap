
import json
import os

def update_pov_batch(new_povs):
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    for pov in new_povs:
        name = pov['name']
        addr = pov['addr']
        pano_id = pov['panoid']
        pov_data = pov['pov']
        
        # Find matches by name and partial address
        # We need to find all entries for this shop (since they might have been merged or kept separate)
        found = False
        for item in data:
            if item.get('n') == name and (addr in item.get('a', '') or item.get('a', '') in addr):
                item['pov'] = {
                    "id": pano_id,
                    "pan": pov_data['pan'],
                    "tilt": pov_data['tilt'],
                    "zoom": pov_data['zoom']
                }
                found = True
        
        if found:
            updated_count += 1
            print(f"Updated POV for: {name} ({addr})")
        else:
            print(f"WARNING: No matches found for {name} | {addr}")

    if updated_count > 0:
        # Save JSON
        with open('lotto_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
            
        # Sync JS
        js_content = 'const lottoData = ' + json.dumps(data, ensure_ascii=False) + ';';
        with open('lotto_data.js', 'w', encoding='utf-8') as f:
            f.write(js_content)
        print(f"Successfully synced {updated_count} shops.")
    else:
        print("No updates made.")

# Data from user
new_povs = [
    { "name": "가로가판대제57호(구)", "addr": "서울 중구 세종대로14길 6-2", "panoid": 1198683779, "pov": { "pan": 4.36, "tilt": 3.48, "zoom": 3 } },
    { "name": "가로매점", "addr": "서울 종로구 종로 186 우리은행 우리은행앞 가판", "panoid": 1028628074, "pov": { "pan": 211.47, "tilt": 10.18, "zoom": -3 } },
]

update_pov_batch(new_povs)
