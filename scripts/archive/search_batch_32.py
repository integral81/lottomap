import json

def search_batch_32(shops):
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
    batch_32 = [
        {"name": "하나마트(하남4번로)", "addr": "광주 광산구 장덕동"},
        {"name": "하나복권(가로판매점)", "addr": "서울 영등포구 여의나루로"}
    ]
    search_batch_32(batch_32)
