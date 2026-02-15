
import json
import re

def clean_name(name):
    name = name.lower().replace(" ", "")
    name = re.sub(r'\(.*?\)', '', name)
    name = name.replace("점", "").replace("로또", "").replace("복권", "")
    return name

def apply_batch_3_updates():
    print("--- [EXECUTION] Applying Batch 3 Research & Cosmetic Results ---")
    try:
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Research-based updates for Batch 3
        batch_3_updates = {
            "전북 익산시 금마면 동고도리 697-4": "카카오복권방",
            "서울 강동구 명일동 341-5": "삼익마트",
            "부산 동래구 온천동 156-1": "세븐일레븐부산온천장역점",
            "서울 양천구 신정동 89-26": "신정마트",
            "부산 기장군 기장읍 동부리162-20": "기장슈퍼",
            "경기 의정부시 호원동 423 대명빌딩": "일등복권방",
            "충남 아산시 인주면 공세리 114-21": "행운마트",
            "경북 포항시 북구 죽도동 42-17": "CU(포항오거리)",
            "강원 원주시 명륜동 751": "CU(원주명륜점)",
            "서울 중구 묵정동 18-9": "CU(소피텔점)",
            "대전 유성구 원내동 228-8": "씨유 대전원내점"
        }
        
        # Cosmetic unifications for Batch 3
        batch_3_cosmetic = {
            "경남 창원시 성산구 중앙동 84-1": "GS25(창원코아)",
            "대전 유성구 원내동 343-11": "GS25(대전원내)",
            "경기 수원시 연통구 영통동 1038-1": "GS25(영통번영점)", # Fix typo "연통구" if needed, but match key
            "경기 수원시 영통구 영통동 1038-1": "GS25(영통번영점)", 
            "부산 중구 동광동3가 17-2": "씨스페이스(중앙제일점)"
        }
        
        all_updates = {**batch_3_updates, **batch_3_cosmetic}
        
        updated_count = 0
        for item in data:
            addr = item.get('a', '').strip()
            if addr in all_updates:
                new_name = all_updates[addr]
                if item['n'] != new_name:
                    item['n'] = new_name
                    updated_count += 1
        
        if updated_count > 0:
            with open('lotto_data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Applied {updated_count} Batch 3 updates.")
        else:
            print("No changes needed for Batch 3.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    apply_batch_3_updates()
