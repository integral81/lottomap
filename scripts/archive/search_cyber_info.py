import json

def search_shop():
    search_queries = ["사이버정보", "동평로 411", "양정동 406", "406-4"]
    
    try:
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        results = []
        for item in data:
            name = item.get('n', '')
            addr = item.get('a', '')
            if any(q in name or q in addr for q in search_queries):
                results.append(item)
                
        print(f"Found {len(results)} records in lotto_data.json:")
        for r in results:
            print(json.dumps(r, ensure_ascii=False))
            
    except Exception as e:
        print(f"Error searching lotto_data.json: {e}")

if __name__ == "__main__":
    search_shop()
