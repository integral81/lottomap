import json

def search_batch_34(shops):
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
                
                # Flexible matching: First few characters of name + region
                name_match = name_q[:3] in name or name in name_q
                region_match = addr_q.split()[0] in addr if addr_q.split() else addr_q in addr
                
                if name_match and region_match:
                    results.append(item)
            
            print(f"Found {len(results)} records.")
            for r in results:
                print(json.dumps(r, ensure_ascii=False))
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    batch_34 = [
        {"name": "행복한복권방", "addr": "전북 전주시 덕진구"},
        {"name": "행복한집", "addr": "경기 오산시 원동"},
        {"name": "행운 마트", "addr": "인천 남동구 만수2동"},
        {"name": "행운나라복권방", "addr": "경기 안양시 만안구"},
        {"name": "행운로또", "addr": "경기 김포시 약암로"},
        {"name": "행운로또복권", "addr": "경기 오산시 오산동"},
        {"name": "행운의집제1호점", "addr": "경북 안동시 동부동"},
        {"name": "행운편의점", "addr": "광주 북구 면앙로"},
        {"name": "혁신대박", "addr": "충북 음성군 원중로"},
        {"name": "현대슈퍼", "addr": "광주 서구 쌍촌동"}
    ]
    search_batch_34(batch_34)
