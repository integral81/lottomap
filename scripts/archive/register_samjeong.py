import json

def register_samjeong():
    json_path = 'lotto_data.json'
    target_name = "삼정그린환경"
    target_addr = "서울 강동구 성내로 66 (오스카상가 136호)" # Road name for Oscar Sangga
    target_lat = 37.527399
    target_lng = 127.135552
    pov_data = {
        "id": "1198563874",
        "pan": 280.0,
        "tilt": -5.0,
        "zoom": 0
    }
    
    search_queries = ["삼정그린", "성내3동 428-5", "오스카상가"]
    
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
    register_samjeong()
