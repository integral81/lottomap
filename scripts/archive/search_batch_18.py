import json

def search_batch_18(shops):
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
    batch_18 = [
        {"name": "신나는복권방", "addr": "경기 파주시 문향로"},
        {"name": "신명", "addr": "서울 강서구 방화2동"},
        {"name": "신신마트편의점", "addr": "전남 목포시 철로마을길"},
        {"name": "신천하명당", "addr": "충남 예산군 발연로"}
    ]
    search_batch_18(batch_18)
