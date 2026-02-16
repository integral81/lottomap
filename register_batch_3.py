
import json

def register_batch_shops():
    """Register multiple shops with POV data"""
    
    shops_to_register = [
        {
            "name": "세진전자통신",
            "addr": "대구 서구 서대구로",
            "panoid": "1201585664",
            "pov": {"pan": 92.52, "tilt": 6.34, "zoom": -3}
        },
        {
            "name": "잠실매점",
            "addr": "서울 송파구 올림픽로",
            "panoid": "1197820702",
            "pov": {"pan": 331.27, "tilt": -2.34, "zoom": -3}
        },
        {
            "name": "오천억복권방",
            "addr": "광주 서구 상무대로",
            "panoid": "1200299139",
            "pov": {"pan": 346.40, "tilt": -7.51, "zoom": -3}
        }
    ]
    
    print(f"Registering {len(shops_to_register)} shops...")
    
    # Load data
    json_path = 'lotto_data.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total_updated = 0
    
    for shop_info in shops_to_register:
        target_name = shop_info['name']
        target_addr_key = shop_info['addr']
        pov_data = {
            "id": shop_info['panoid'],
            "pan": shop_info['pov']['pan'],
            "tilt": shop_info['pov']['tilt'],
            "zoom": shop_info['pov']['zoom']
        }
        
        updated_count = 0
        for item in data:
            # Match by name and address prefix
            if target_name in item['n'] and target_addr_key in item['a']:
                item['pov'] = pov_data
                updated_count += 1
        
        if updated_count > 0:
            print(f"  [OK] {target_name}: {updated_count} entries updated")
            total_updated += updated_count
        else:
            print(f"  [WARN] {target_name}: No matching entries found")
    
    # Save
    if total_updated > 0:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n[OK] Total {total_updated} entries updated in lotto_data.json")
    
    return total_updated

if __name__ == "__main__":
    register_batch_shops()
