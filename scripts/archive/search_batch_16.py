import json

def search_batch_16(shops):
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
                # Flexible match
                if name_q in name or (addr_q in addr and (name_q[:3] in name)):
                    results.append(item)
            
            print(f"Found {len(results)} records.")
            for r in results:
                print(json.dumps(r, ensure_ascii=False))
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    batch_16 = [
        {"name": "세류보석복권방", "addr": "경기 수원시 권선구"},
        {"name": "세방매점", "addr": "경북 경주시 용강동"},
        {"name": "세븐일레븐광양시청점", "addr": "전남 광양시 중동"},
        {"name": "세븐일레븐화성봉담수기점", "addr": "경기 화성시 세자로"}
    ]
    search_batch_16(batch_16)
