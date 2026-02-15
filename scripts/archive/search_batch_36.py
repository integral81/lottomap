import json

def search_batch_36(shops):
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
                
                # Match logic
                name_match = name_q[:2] in name # "홈돌", "화천", "황금"
                region_match = addr_q.split()[0] in addr if addr_q.split() else addr_q in addr
                
                if name_match and region_match:
                    results.append(item)
            
            print(f"Found {len(results)} records.")
            for r in results:
                print(json.dumps(r, ensure_ascii=False))
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    batch_36 = [
        {"name": "홈돌이로또복권", "addr": "경기 김포시 감정동"},
        {"name": "화천복권방", "addr": "강원 화천군 화천읍"},
        {"name": "황금대박점", "addr": "서울 노원구 공릉로"},
        {"name": "황금로또", "addr": "부산 동구 중앙대로251번길"},
        {"name": "황금복권", "addr": "강원 원주시 단계동"}
    ]
    search_batch_36(batch_36)
