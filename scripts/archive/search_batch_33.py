import json

def search_batch_33(shops):
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
                if name_q[:3] in name and (addr_q[:4] in addr or addr_q.split()[1] in addr if len(addr_q.split()) > 1 else addr_q in addr):
                    results.append(item)
            
            print(f"Found {len(results)} records.")
            for r in results:
                print(json.dumps(r, ensure_ascii=False))
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    batch_33 = [
        {"name": "하이로또", "addr": "서울 금천구 금하로"},
        {"name": "하프타임(괴정점)", "addr": "부산 사하구 괴정동"},
        {"name": "학동복권나라", "addr": "전남 여수시 흥국로"},
        {"name": "한경종합광고", "addr": "서울 송파구 삼전동"},
        {"name": "한국인세계대박복권", "addr": "인천 연수구 옥련동"},
        {"name": "한마음", "addr": "서울 관악구 봉천동"},
        {"name": "한아름매점", "addr": "충남 홍성군 광천읍"}
    ]
    search_batch_33(batch_33)
