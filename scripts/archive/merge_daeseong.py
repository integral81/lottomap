
import json

def merge_daeseong():
    file_path = 'lotto_data.json'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    # Target: Current valid location (구성로 75-1)
    target_addr = "경기 용인시 기흥구 구성로 75-1"
    target_lat = 37.2949073386736
    target_lng = 127.117903169762
    
    count = 0
    for item in data:
        if "대성기획" in item['n']:
            # Check if it needs updating
            if item['a'] != target_addr or item.get('lat') != target_lat:
                item['a'] = target_addr
                item['lat'] = target_lat
                item['lng'] = target_lng
                count += 1

    if count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Successfully merged {count} '대성기획' entries to: {target_addr}")
    else:
        print("No entries needed merging.")

if __name__ == "__main__":
    merge_daeseong()
