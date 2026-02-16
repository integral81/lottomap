
import json

def register_hwanggeum():
    print("Registering 황금복권방 POV...")
    
    # Load lotto_data.json
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Target shop info
    target_name = "황금복권방"
    target_addr = "부산 부산진구 가야대로"
    
    # POV data
    pov_data = {
        "id": "1202246845",
        "pan": 352.11,
        "tilt": 2.53,
        "zoom": 1
    }
    
    # Update all matching records
    updated_count = 0
    for item in data:
        if target_name in item['n'] and target_addr in item['a']:
            item['pov'] = pov_data
            # Remove ★ from name if present
            item['n'] = item['n'].replace('★ ', '')
            updated_count += 1
    
    # Save back
    with open('lotto_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Updated {updated_count} records for {target_name}")
    
    # Regenerate admin list
    print("\nRegenerating admin_targets.js...")
    import subprocess
    subprocess.run(['python', 'generate_admin_list_final.py'], check=True)
    
    print("\n✅ Registration complete!")
    print(f"Shop: {target_name}")
    print(f"Address: {target_addr}")
    print(f"PanoID: {pov_data['id']}")
    print(f"POV: pan={pov_data['pan']}, tilt={pov_data['tilt']}, zoom={pov_data['zoom']}")

if __name__ == "__main__":
    register_hwanggeum()
