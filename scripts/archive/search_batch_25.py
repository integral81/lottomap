import json

def search_batch_25(shops):
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
    batch_25 = [
        {"name": "잉크와복권방", "addr": "충남 천안시 동남구"},
        {"name": "장군슈퍼", "addr": "경기 부천시 오정구"},
        {"name": "제일복권", "addr": "경남 양산시 중부동"},
        {"name": "제일슈퍼", "addr": "인천 연수구 동춘동"}
    ]
    search_batch_25(batch_25)
