import json

def search_batch_28(shops):
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
                if name_q[:2] in name and (addr_q[:2] in addr):
                    results.append(item)
            
            print(f"Found {len(results)} records.")
            for r in results:
                print(json.dumps(r, ensure_ascii=False))
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    batch_28 = [
        {"name": "진성식품", "addr": "충북 제천시 중앙로1가"},
        {"name": "진양상회", "addr": "경북 영주시 선비로"},
        {"name": "차부상회", "addr": "경기 김포시 통진읍"},
        {"name": "천복당", "addr": "경기 오산시 원동"},
        {"name": "천사로또방", "addr": "경기 남양주시 금곡동"}
    ]
    search_batch_28(batch_28)
