import json

def search_batch_31(shops):
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
    batch_31 = [
        {"name": "터미널복권방", "addr": "전북 정읍시 연지8길"},
        {"name": "토토복권", "addr": "대구 서구 달서로12길"},
        {"name": "풍전슈퍼", "addr": "경기 부천시 원미구"}
    ]
    search_batch_31(batch_31)
