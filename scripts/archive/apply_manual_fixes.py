
import json

def apply_tier3_manual_fixes():
    print("--- [EXECUTION] Applying Tier-3 Researched Fixes ---")
    try:
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        fixes = {
            "서울 서초구 잠원동 69-12": "서울 서초구 신반포로 205",
            "제주 제주시 일도2동 1047-4": "제주 제주시 신산로 16",
            "경기 의왕시 삼동 193-14": "경기 의왕시 삼동 193-1", # Slight adjustment for building matching
            "경기 광주시 경안동 30-2": "경기 광주시 경안로 16", # 월드컵복권방 road name
            "대구 남구 이천동 193-19": "대구 남구 이천로 25", # 로또명당 road name
            "부산 남구 대연4동 1168-14": "부산 남구 대연동 1168-1", 
            "충남 보령시 동대동 828-4": "충남 보령시 희망로 45", # 보령복권방 road name
            "경남 창원시 소답동 16-9": "경남 창원시 의창구 의안로2번길 17",
            "경남 양산시 중주동 693-2": "경남 양산시 서창로 142", # 복권천국 road name
            "경북 경산시 하양읍 금락리 118": "경북 경산시 하양읍 하양로 51", # 부흥청과 road name
            "서울 강북구 미아동 688-5": "서울 강북구 삼양로 162" # 슈퍼전자 road name
        }
        
        updated_count = 0
        for item in data:
            addr = item.get('a', '').strip()
            if addr in fixes:
                item['a'] = fixes[addr]
                updated_count += 1
                
        if updated_count > 0:
            with open('lotto_data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Updated {updated_count} manual addresses to Road Names for final try.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    apply_tier3_manual_fixes()
