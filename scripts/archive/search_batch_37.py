import json

def search_batch_37(shops):
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
                
                # Match logic
                name_match = name_q[:2] in name 
                region_match = addr_q.split()[0] in addr if addr_q.split() else addr_q in addr
                
                if name_match and region_match:
                    results.append(item)
            
            print(f"Found {len(results)} records.")
            for r in results:
                print(json.dumps(r, ensure_ascii=False))
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    batch_37 = [
        {"name": "흥건슈퍼", "addr": "전북 전주시 완산구"},
        {"name": "희망복권방", "addr": "전남 나주시 풍물시장1길"}
    ]
    search_batch_37(batch_37)
