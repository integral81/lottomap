import json

def register_batch_28():
    json_path = 'lotto_data.json'
    
    # Shop Data for Batch 28
    batch_data = [
        {
            "search_name": "진성식품",
            "name": "진성식품",
            "addr": "충북 제천시 의병대로 115-1 (중앙로1가)",
            "lat": 37.136071,
            "lng": 128.209974,
            "pov": {"id": "1185296414", "pan": 198.26, "tilt": 1.11, "zoom": -3}
        },
        {
            "search_name": "진양상회",
            "name": "진양상회",
            "addr": "경북 영주시 선비로 68",
            "lat": 36.811229,
            "lng": 128.624088,
            "pov": {"id": "1167665273", "pan": 302.18, "tilt": 1.72, "zoom": -3}
        },
        {
            "search_name": "차부상회",
            "name": "차부상회",
            "addr": "경기 김포시 통진읍 조강로 50",
            "lat": 37.690349,
            "lng": 126.600338,
            "pov": {"id": "1203538717", "pan": 21.93, "tilt": -0.66, "zoom": -3}
        },
        {
            "search_name": "천복당",
            "name": "천복당",
            "addr": "경기 오산시 성호대로 103 (원동)",
            "lat": 37.146216,
            "lng": 127.074172,
            "pov": {"id": "1174696473", "pan": 187.21, "tilt": 9.51, "zoom": -3}
        },
        {
            "search_name": "천사로또방",
            "name": "천사로또방",
            "addr": "경기 남양주시 경춘로 994 (금곡동)",
            "lat": 37.636189,
            "lng": 127.211079,
            "pov": {"id": "1203244935", "pan": 172.29, "tilt": -2.90, "zoom": -3}
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
                    region = shop["addr"].split()[0] # 충북, 경북, 경기 등
                    if region in addr:
                        # City check
                        city = shop["addr"].split()[1] # 제천시, 영주시, 김포시 등
                        if city in addr:
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
    register_batch_28()
