import json

def search_shops(queries):
    json_path = 'lotto_data.json'
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for q in queries:
            print(f"\nSearching for: {q}")
            results = []
            for item in data:
                name = item.get('n', '')
                addr = item.get('a', '')
                if q in name or q in addr:
                    results.append(item)
            
            print(f"Found {len(results)} records.")
            for r in results:
                print(json.dumps(r, ensure_ascii=False))
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    search_shops(["삼호복권", "쌍문동 96-43", "삼성복권방", "동두천", "어수로 100-1"])
