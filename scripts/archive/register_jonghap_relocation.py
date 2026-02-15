import json

def register_jonghap_new():
    json_path = 'lotto_data.json'
    target_name = "종합가판점"
    target_addr = "서울 동대문구 왕산로 206 가로판매대 (전농동 620-26 앞)"
    # Coordinates for Exit 5 location (from R1133)
    target_lat = 37.579697
    target_lng = 127.044971
    pov_data = {
        "id": "1198200114",
        "pan": 36.6,
        "tilt": 0.0,
        "zoom": 0
    }
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        count = 0
        for item in data:
            name = item.get('n', '')
            addr = item.get('a', '')
            # Match 종합가판점 in 청량리/전농동
            if "종합가판점" in name and ("청량리" in addr or "전농동" in addr):
                item['n'] = target_name
                item['a'] = target_addr
                item['lat'] = target_lat
                item['lng'] = target_lng
                item['pov'] = pov_data
                if 'closed' in item:
                    del item['closed']
                count += 1
                
        if count > 0:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Successfully updated {count} records in lotto_data.json for {target_name} at Exit 5.")
        else:
            print("No matching records found in lotto_data.json.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    register_jonghap_new()
