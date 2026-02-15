import json

def register_batch_26():
    json_path = 'lotto_data.json'
    
    # Shop Data for Batch 26
    batch_data = [
        {
            "search_name": "제주대림점",
            "name": "제주대림점",
            "addr": "제주 제주시 과원북2길 48 (노형동)",
            "lat": 33.478723,
            "lng": 126.487608,
            "pov": {"id": "1182183945", "pan": 187.18, "tilt": 1.59, "zoom": -3}
        },
        {
            "search_name": "조례로또",
            "name": "조례로또복권방",
            "addr": "전남 순천시 봉화2길 58 (조례동)",
            "lat": 34.958393,
            "lng": 127.518114,
            "pov": {"id": "1205418189", "pan": 76.49, "tilt": -0.45, "zoom": -3}
        }
    ]
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for shop in batch_data:
            count = 0
            for item in data:
                name = item.get('n', '')
                addr = item.get('a', '')
                
                # Matching logic
                match = False
                if shop["search_name"] in name:
                    region = shop["addr"].split()[0]
                    if region in addr:
                        # Extra filters to avoid false positives
                        if shop["search_name"] == "제주대림점" and "제주" not in addr: continue
                        if shop["search_name"] == "조례로또" and "순천" not in addr: continue
                        match = True
                
                if match:
                    item['n'] = shop["name"]
                    item['a'] = shop["addr"]
                    item['lat'] = shop["lat"]
                    item['lng'] = shop["lng"]
                    item['pov'] = shop["pov"]
                    if 'closed' in item:
                        del item['closed']
                    count += 1
            print(f"Updated {count} records for {shop['name']}.")
            
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    register_batch_26()
