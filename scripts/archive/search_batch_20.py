import json

def search_batch_20(shops):
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
                if name_q in name or (addr_q[:4] in addr and (name_q[:2] in name)):
                    results.append(item)
            
            print(f"Found {len(results)} records.")
            for r in results:
                print(json.dumps(r, ensure_ascii=False))
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    batch_20 = [
        {"name": "여기있었네복권방", "addr": "전북 김제시 남북로"},
        {"name": "열두보석복권방", "addr": "경기 용인시 기흥구"},
        {"name": "영훈슈퍼마켓", "addr": "서울 도봉구 창3동"},
        {"name": "예술로또", "addr": "강원 영월군 영월읍"},
        {"name": "예스복권방", "addr": "경기 남양주시 별내중앙로"},
        {"name": "온천로또복권", "addr": "충남 예산군 덕산면"}
    ]
    search_batch_20(batch_20)
