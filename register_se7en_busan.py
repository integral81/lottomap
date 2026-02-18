import json

# Target Data
target_name = "세븐일레븐부산온천장역점"
target_data = {
    "name": "세븐일레븐부산온천장역점",
    "addr": "부산 동래구 온천동 156-1 온천장역지하철 내",
    "panoid": 1202578370,
    "pov": { "pan": 128.83, "tilt": 3.01, "zoom": -3 },
    "roadview_msg": "2층 개찰구 바로 옆 대합실!!"
}

json_path = 'lotto_data.json'
js_path = 'lotto_data.js'

def update_shop():
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        updated_count = 0
        for s in data:
            # Loose match for safety
            if target_name in s.get('n', '') or "온천동 156-1" in s.get('a', ''):
                s['panoid'] = target_data['panoid']
                s['pov'] = target_data['pov'].copy()
                s['pov']['id'] = target_data['panoid']
                s['roadview_msg'] = target_data['roadview_msg']
                updated_count += 1
                print(f"Updated: {s['n']} (Wins: {s.get('wins')})")
                
        if updated_count > 0:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            with open(js_path, 'w', encoding='utf-8') as f:
                f.write('const lottoData = ' + json.dumps(data, ensure_ascii=False) + ';')
                
            print(f"Successfully updated {updated_count} entries for '{target_name}'.")
        else:
            print(f"Shop '{target_name}' not found in data.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_shop()
