
import json

def update_lotto_rest_final():
    json_path = 'lotto_data.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    target_name = "로또휴게실"
    # User provided: 경기 용인시 기흥구 용구대로 1885
    # PanoID: 1199447820
    # POV: Pan 282.0, Tilt 1.2
    
    updated_count = 0
    for item in data:
        if target_name in item['n']:
            # Force update
            item['pov'] = {
                "id": "1199447820",
                "pan": 282.0,
                "tilt": 1.2,
                "zoom": 0
            }
            # Optional: Update address if it's just "보라동" to full road name?
            # User output showed "경기 용인시 기흥구 용구대로 1885 (보라동 378-1)"
            # existing might be different. Let's trust local matching.
            updated_count += 1
            
    if updated_count > 0:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Updated {updated_count} entries for {target_name}")
    else:
        print(f"Could not find {target_name}")

if __name__ == "__main__":
    update_lotto_rest_final()
