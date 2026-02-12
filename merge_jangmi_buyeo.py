
import json

def merge_jangmi_buyeo():
    file_path = 'lotto_data.json'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    # Target: Standardized name and address (충남 부여군 부여읍 계백로 265)
    target_name = "장미슈퍼"
    target_addr = "충남 부여군 부여읍 계백로 265"
    # Lat/Lng from rounds 1160 (most recent address format in data)
    target_lat = 36.276372384131
    target_lng = 126.909418515443
    
    count = 0
    for item in data:
        if "장미슈퍼" in item['n'] and "부여" in item['a']:
            # Check if it needs updating
            if item['a'] != target_addr or item['n'] != target_name or item.get('lat') != target_lat:
                item['n'] = target_name
                item['a'] = target_addr
                item['lat'] = target_lat
                item['lng'] = target_lng
                count += 1

    if count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Successfully merged {count} '장미슈퍼' (Buyeo) entries to: {target_addr}")
    else:
        print("No entries needed merging.")

if __name__ == "__main__":
    merge_jangmi_buyeo()
