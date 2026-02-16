
import json

def register_batch_2_shops():
    """Register 2 shops with POV data"""
    
    shops_to_register = [
        {
            "name": "행운복권방 보생당건강원",
            "addr": "전북 익산시 무왕로",
            "panoid": "1179789585",
            "pov": {"pan": 199.53, "tilt": 2.73, "zoom": 1}
        },
        {
            "name": "한꿈복권방",
            "addr": "울산 중구 번영로",
            "panoid": "1202017790",
            "pov": {"pan": 148.21, "tilt": -0.82, "zoom": 2}
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
    register_batch_2_shops()
