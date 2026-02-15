import json

def search_batch_30(shops):
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
                if name_q[:3] in name and (addr_q[:4] in addr or addr_q.split()[1] in addr):
                    results.append(item)
            
            print(f"Found {len(results)} records.")
            for r in results:
                print(json.dumps(r, ensure_ascii=False))
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    batch_30 = [
        {"name": "코리아마트(비산점)", "addr": "대구 서구 비산동"},
        {"name": "코사마트금강점", "addr": "대구 달서구 용산로"},
        {"name": "태원정보통신", "addr": "서울 중랑구 상봉2동"}
    ]
    search_batch_30(batch_30)
