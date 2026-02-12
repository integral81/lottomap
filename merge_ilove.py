
import json

def merge_ilove():
    file_path = 'lotto_data.json'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    # Target: Standardized name and address (유곡로 19-1)
    target_name = "아이러브마트복권방"
    target_addr = "울산 중구 유곡로 19-1"
    # Lat/Lng from rounds 1184 (using the one in lotto_data.json for 유곡로 19-1)
    target_lat = 35.5566987509391
    target_lng = 129.307118444756
    
    count = 0
    for item in data:
        if "아이러브" in item['n'] and "울산" in item['a']:
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
        print(f"Successfully merged {count} '아이러브' entries to: {target_addr}")
    else:
        print("No entries needed merging.")

if __name__ == "__main__":
    merge_ilove()
