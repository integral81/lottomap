import json

def search_batch_27(shops):
    json_path = 'lotto_data.json'
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for shop in shops:
            name_q = shop["name"]
            addr_q = shop["addr"]
            print(f"\nSearching for: {name_q} ({addr_q})")
            results = []
            for item in data:
                name = item.get('n', '')
                addr = item.get('a', '')
                # flexible matching
                if name_q[:2] in name and (addr_q[:2] in addr):
                    results.append(item)
            
            print(f"Found {len(results)} records.")
            for r in results:
                print(json.dumps(r, ensure_ascii=False))
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    batch_27 = [
        {"name": "좋은터", "addr": "인천 계양구 효서로"},
        {"name": "주몽동명", "addr": "경기 용인시 수지구"},
        {"name": "중구-가로가판대-37", "addr": "서울 중구 남대문로"},
        {"name": "중흥마트", "addr": "광주 북구 문산로"},
        {"name": "지에스(GS)25 진동에이스점", "addr": "경남 창원시 마산합포구"},
        {"name": "지에스25 신매태왕점로또", "addr": "대구 수성구 욱수천로"},
        {"name": "진대박 로또복권방", "addr": "울산 동구 대송로"},
        {"name": "진도로또", "addr": "전남 진도군 진도읍"}
    ]
    search_batch_27(batch_27)
