
import json

def exclude_online_site():
    """Exclude 인터넷 복권판매사이트 from admin list by marking it as registered"""
    
    target_name = "인터넷 복권판매사이트"
    
    print(f"Excluding {target_name} from admin list...")
    
    # Load data
    json_path = 'lotto_data.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Mark with a special POV to exclude from admin list
    updated_count = 0
    for item in data:
        if target_name in item['n']:
            # Add a dummy POV to mark as "processed" (not for roadview)
            item['pov'] = {
                "id": "N/A",
                "pan": 0,
                "tilt": 0,
                "zoom": 0,
                "note": "Online site - no roadview"
            }
            updated_count += 1
    
    if updated_count > 0:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[OK] Excluded {updated_count} entries from admin list")
    
    return updated_count

if __name__ == "__main__":
    exclude_online_site()
