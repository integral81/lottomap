import json

def investigate_happy_24(name_q, region_q):
    json_path = 'lotto_data.json'
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        print(f"Searching for: {name_q} in {region_q}")
        results = []
        for item in data:
            name = item.get('n', '')
            addr = item.get('a', '')
            if name_q in name and region_q in addr:
                results.append(item)
        
        print(f"Found {len(results)} records in lotto_data.json.")
        for r in results:
            print(json.dumps(r, ensure_ascii=False))
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    investigate_happy_24("해피+24시편의점", "광주")
