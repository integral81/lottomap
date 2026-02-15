import json

def search_batch_17(shops):
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
                if name_q in name or (addr_q in addr and (name_q[:2] in name)):
                    results.append(item)
            
            print(f"Found {len(results)} records.")
            for r in results:
                print(json.dumps(r, ensure_ascii=False))
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    batch_17 = [
        {"name": "스카이편의점", "addr": "경기 안양시 만안구"},
        {"name": "스포츠베팅샵", "addr": "서울 서초구 양재동"},
        {"name": "승일유통", "addr": "충북 청주시 흥덕구"}
    ]
    search_batch_17(batch_17)
