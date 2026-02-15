import json

def search_batch_29(shops):
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
                if name_q[:4] in name and (addr_q[:2] in addr):
                    results.append(item)
            
            print(f"Found {len(results)} records.")
            for r in results:
                print(json.dumps(r, ensure_ascii=False))
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    batch_29 = [
        {"name": "천안역로또토토복권방", "addr": "충남 천안시 동남구"},
        {"name": "천하제일복권명당연무점", "addr": "충남 논산시 연무읍"},
        {"name": "최강복권&아이스크림", "addr": "경기 고양시 덕양구"}
    ]
    search_batch_29(batch_29)
