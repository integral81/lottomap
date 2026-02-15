
import json

def apply_all_unifications():
    print("--- [EXECUTION] Global Name Standardization ---")
    try:
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Unified mapping from all previous batches
        unified_mapping = {
            # Batch 1 & 2 Legend Shops & Rebrands
            "경남 김해시 인제로170번길 15-6 편의점 내": "씨스페이스 어방점",
            "경기 김포시 대곶면 율생리 350-5": "금강복권",
            "부산 해운대구 좌동 1317 경동G-PLUS아파트상가103": "경동플러스",
            "서울 중랑구 상봉동 108": "부영마트",
            "서울 중랑구 망우동 470-10": "CU(망우점)",
            "울산 남구 달동 1309-1": "CU(달동초이스점)",
            "경북 구미시 구미중앙로 72": "역전로또",
            "전남 여수시 신기동 128-5": "천하명당",
            "서울 강서구 화곡동 29-52": "세븐일레븐강서화곡예스점",
            "대구 동구 입석동 933-2": "CU(입석강변점)",
            "인천 연수구 송도동 2-6 송도프라자108호": "씨유송도프라자",
            "강원 동해시 발한동 39-14": "CU(동해발한점)",
            "서울 중랑구 망우로 410": "씨유 망우점2",
            
            # Batch 3 rebrands
            "전북 익산시 금마면 동고도리 697-4": "카카오복권방",
            "서울 강동구 명일동 341-5": "삼익마트",
            "부산 동래구 온천동 156-1": "세븐일레븐부산온천장역점",
            "서울 양천구 신정동 89-26": "신정마트",
            "부산 기장군 기장읍 동부리162-20": "기장슈퍼",
            "경기 의정부시 호원동 423 대명빌딩": "일등복권방",
            "충남 아산시 인주면 공세리 114-21": "행운마트",
            
            # Cosmetic unifications
            "부산 중구 자갈치로 33 501502호": "자갈치도깨비명당",
            "전남 여수시 학동서5길 2 큐마트내": "큐마트학동점로또",
            "서울 광진구 자양1동 219-2": "자양사거리 가로매점",
            "서울 강남구 삼성동 168": "GS25(삼성역점)",
            "제주 서귀포시 중문동 1964-4": "GS25(서귀중문)",
            "경북 경산시 삼풍동 509-4": "GS25(경산사동점)",
            "경남 창원시 성산구 중앙동 84-1": "GS25(창원코아)",
            "대전 유성구 원내동 343-11": "GS25(대전원내)",
            "경기 수원시 영통구 영통동 1038-1": "GS25(영통번영점)",
            "부산 중구 동광동3가 17-2": "씨스페이스(중앙제일점)"
        }
        
        updated_count = 0
        for item in data:
            addr = item.get('a', '').strip()
            if addr in unified_mapping:
                new_name = unified_mapping[addr]
                if item['n'] != new_name:
                    item['n'] = new_name
                    updated_count += 1
                    
        if updated_count > 0:
            with open('lotto_data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Applied {updated_count} global unifications.")
        else:
            print("No changes needed. Names are already standardized.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    apply_all_unifications()
