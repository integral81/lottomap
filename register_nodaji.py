
import json

def register_nodaji():
    """Register 노다지복권방 with POV data"""
    
    shop_info = {
        "name": "노다지복권방",
        "addr": "경기 용인시 처인구",
        "panoid": "1198887321",
        "pov": {"pan": 155.74, "tilt": -3.51, "zoom": 2}
    }
    
    print(f"Registering {shop_info['name']}...")
    
    # Load data
    json_path = 'lotto_data.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    pov_data = {
        "id": shop_info['panoid'],
        "pan": shop_info['pov']['pan'],
        "tilt": shop_info['pov']['tilt'],
        "zoom": shop_info['pov']['zoom']
    }
    
    updated_count = 0
    for item in data:
        # Match by name and address prefix
        if shop_info['name'] in item['n'] and shop_info['addr'] in item['a']:
            item['pov'] = pov_data
            updated_count += 1
    
    if updated_count > 0:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[OK] {shop_info['name']}: {updated_count} entries updated")
    else:
        print(f"[WARN] {shop_info['name']}: No matching entries found")
    
    return updated_count

if __name__ == "__main__":
    register_nodaji()
