import json

def register_batch_24():
    json_path = 'lotto_data.json'
    
    # Shop Data for Batch 24
    batch_data = [
        {
            "search_name": "이삭",
            "name": "이삭",
            "addr": "전남 목포시 통일대로 54 (옥암동)",
            "lat": 34.809945,
            "lng": 126.455232,
            "pov": {"id": "1192651961", "pan": 221.20, "tilt": 9.74, "zoom": 1}
        },
        {
            "search_name": "이플러스",
            "name": "이플러스",
            "addr": "경기 수원시 영통구 매탄로 153-14",
            "lat": 37.274277,
            "lng": 127.044325,
            "pov": {"id": "1200019054", "pan": 202.04, "tilt": 7.86, "zoom": 1}
        },
        {
            "search_name": "일등복권",
            "name": "일등복권",
            "addr": "경기 양주시 송랑로 223 (만송동)",
            "lat": 37.804486,
            "lng": 127.085310,
            "pov": {"id": "1204065490", "pan": 167.43, "tilt": 6.54, "zoom": 3}
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
                        if shop["search_name"] == "이삭" and "목포" not in addr: continue
                        if shop["search_name"] == "이플러스" and "수원" not in addr: continue
                        if shop["search_name"] == "일등복권" and "양주" not in addr: continue
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
    register_batch_24()
