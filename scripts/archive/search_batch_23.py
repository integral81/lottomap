import json

def search_batch_23(shops):
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
                if name_q in name and (addr_q[:2] in addr):
                    results.append(item)
            
            print(f"Found {len(results)} records.")
            for r in results:
                print(json.dumps(r, ensure_ascii=False))
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    batch_23 = [
        {"name": "원동슈퍼", "addr": "충남 보령시 대천동"},
        {"name": "원스탑", "addr": "서울 송파구 잠실동"},
        {"name": "월드 복권방", "addr": "서울 강서구 곰달래로53길"},
        {"name": "월드마트", "addr": "충북 청주시 흥덕구"},
        {"name": "유방매표소", "addr": "경기 용인시 처인구"}
    ]
    search_batch_23(batch_23)
