import json

def register_emart24_deogi():
    json_path = 'lotto_data.json'
    target_name = "이마트24 일산덕이점"
    target_addr = "경기 고양시 일산서구 미래로 164 (덕이동)"
    target_lat = 37.693129
    target_lng = 126.746892
    pov_data = {
        "id": "1192804361",
        "pan": 148.8,
        "tilt": 6.9,
        "zoom": 0
    }
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        count = 0
        for item in data:
            name = item.get('n', '')
            addr = item.get('a', '')
            
            # Match Emart24/Deogi in Goyang/Ilsan
            # Searching for "이마트24" and ("덕이" or "미래로 164")
            if (("이마트24" in name or "이마트" in name) and "덕이" in name and "고양" in addr) or ("미래로 164" in addr):
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
            print(f"Successfully updated {count} records in lotto_data.json for {target_name}.")
        else:
            print("No matching records found in lotto_data.json.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    register_emart24_deogi()
