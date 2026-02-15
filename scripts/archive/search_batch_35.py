import json

def search_batch_35(shops):
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
                
                name_match = name_q[:3] in name
                region_match = addr_q.split()[0] in addr
                
                if name_match and region_match:
                    results.append(item)
            
            print(f"Found {len(results)} records.")
            for r in results:
                print(json.dumps(r, ensure_ascii=False))
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    batch_35 = [
        {"name": "현아상회", "addr": "부산 남구 용호동"},
        {"name": "호반할인마트", "addr": "광주 광산구 도산동"}
    ]
    search_batch_35(batch_35)
