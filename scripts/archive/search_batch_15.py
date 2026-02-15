import json

def search_batch_15(shops):
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
                # Flexible match: name match OR (address match AND partial name match)
                if name_q in name or (addr_q in addr and (name_q[:2] in name)):
                    results.append(item)
            
            print(f"Found {len(results)} records.")
            for r in results:
                print(json.dumps(r, ensure_ascii=False))
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    batch_15 = [
        {"name": "새상무복권", "addr": "광주 서구 치평로"},
        {"name": "서울구가-17가판", "addr": "서울 구로구 구로동로"},
        {"name": "서울로또방", "addr": "충북 옥천군 삼금로"},
        {"name": "서해로또방", "addr": "경기 화성시 화성로"},
        {"name": "성강동인", "addr": "경기 하남시 신장로"}
    ]
    search_batch_15(batch_15)
