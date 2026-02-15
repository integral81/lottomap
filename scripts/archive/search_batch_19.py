import json

def search_batch_19(shops):
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
    batch_19 = [
        {"name": "씨유제주 제일점", "addr": "제주 제주시 신산로"},
        {"name": "아띠로또판매점", "addr": "충남 천안시 서북구"},
        {"name": "안성휴게소 복권판매점(부산방향)", "addr": "경기 안성시 경부고속도로"},
        {"name": "양산덕계점(로또)", "addr": "경남 양산시 평산동"},
        {"name": "에버빌마트", "addr": "경북 안동시 정하동"},
        {"name": "엘도라도복권점문점", "addr": "서울 광진구 중곡동"}
    ]
    search_batch_19(batch_19)
