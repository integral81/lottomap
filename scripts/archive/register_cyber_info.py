import json

def register_cyber_info():
    json_path = 'lotto_data.json'
    target_name = "사이버정보통신"
    target_addr = "부산 부산진구 동평로 411 (백조상가동 103-1호)"
    target_lat = 35.174067
    target_lng = 129.070238
    pov_data = {
        "id": "1202364869",
        "pan": 25.5,
        "tilt": -1.1,
        "zoom": 0
    }
    
    search_queries = ["사이버정보", "동평로 411", "양정동 406", "406-4"]
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        count = 0
        for item in data:
            name = item.get('n', '')
            addr = item.get('a', '')
            if any(q in name or q in addr for q in search_queries):
                # Update record
                item['n'] = target_name
                item['a'] = target_addr
                item['lat'] = target_lat
                item['lng'] = target_lng
                item['pov'] = pov_data
                count += 1
                
        if count > 0:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Successfully updated {count} records for {target_name}.")
        else:
            print("No matching records found to update.")
            
    except Exception as e:
        print(f"Error updating lotto_data.json: {e}")

if __name__ == "__main__":
    register_cyber_info()
