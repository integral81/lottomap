
import json

def register_batch_3_shops():
    """Register 3 shops with POV data"""
    
    shops_to_register = [
        {
            "name": "올인 (all in)",
            "addr": "경기 화성시 3.1만세로",
            "panoid": "1197247800",
            "pov": {"pan": 337.67, "tilt": 2.23, "zoom": 1}
        },
        {
            "name": "대박마트복권방",
            "addr": "충남 아산시 음봉로",
            "panoid": "1176849718",
            "pov": {"pan": 226.14, "tilt": 3.17, "zoom": 1}
        },
        {
            "name": "종합복권슈퍼",
            "addr": "경기 시흥시 마유로",
            "panoid": "1175861017",
            "pov": {"pan": 99.58, "tilt": 0.90, "zoom": 1}
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
    register_batch_3_shops()
