
import json
import os

def register_pov():
    file_path = 'lotto_data.json'
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updates = [
        {
            "n": "짱복권",
            "a": "서울 종로구 종로 269",
            "id": 1197814790,
            "pan": 4.65,
            "tilt": 13.24,
            "zoom": -1
        },
        {
            "n": "행운복권마트",
            "a": "서울 종로구 지봉로 58",
            "id": 1198160604,
            "pan": 90.88,
            "tilt": 0.42,
            "zoom": 3
        },
        {
            "n": "에스비 상사",
            "a": "서울 중구 퇴계로86길 29",
            "id": 1198788739,
            "pan": 113.35,
            "tilt": 3.79,
            "zoom": -2
        },
        {
            "n": "로또복권판매소",
            "a": "서울 마포구 도화동 37",
            "id": 1197820607,
            "pan": 192.94,
            "tilt": -5.36,
            "zoom": 1
        }
    ]

    count = 0
    for u in updates:
        for entry in data:
            name_match = u['n'] in entry.get('n', '')
            addr_match = u['a'].replace(' ', '') in entry.get('a', '').replace(' ', '')
            
            if name_match and addr_match:
                entry['pov'] = {
                    "id": u['id'],
                    "pan": u['pan'],
                    "tilt": u['tilt'],
                    "zoom": u['zoom']
                }
                count += 1
                
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=0) # Use indent 0 or none for compact format if needed, but let's keep it readable-ish or match original
        
    print(f"Updated {count} entries in lotto_data.json")

if __name__ == "__main__":
    register_pov()
