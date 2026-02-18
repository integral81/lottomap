import json

target_name = "세븐일레븐 수완점"
target_data = {
    "panoid": 1200028569,
    "pov": { "pan": 195.05, "tilt": -5.34, "zoom": 0 },
    "closed": True
}

json_path = 'lotto_data.json'
js_path = 'lotto_data.js'

def update_shop():
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        updated_count = 0
        for s in data:
            # Match by name or address part (Suwan-dong 1428)
            if "세븐일레븐 수완점" in s.get('n', '') or "수완동 1428" in s.get('a', ''):
                s['panoid'] = target_data['panoid']
                s['pov'] = target_data['pov'].copy()
                s['pov']['id'] = target_data['panoid']
                s['closed'] = True
                updated_count += 1
                print(f"Updated: {s['n']} (Wins: {s.get('wins')}) -> Marked CLOSED")
                
        if updated_count > 0:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            with open(js_path, 'w', encoding='utf-8') as f:
                f.write('const lottoData = ' + json.dumps(data, ensure_ascii=False) + ';')
                
            print(f"Successfully updated {updated_count} entries.")
        else:
            print(f"Shop '{target_name}' not found.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_shop()
