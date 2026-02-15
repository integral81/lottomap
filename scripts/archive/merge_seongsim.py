
import json

def merge_seongsim():
    file_path = 'lotto_data.json'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    # Target: Current valid location (불종로 78)
    target_addr = "경북 포항시 북구 불종로 78"
    target_lat = 36.0381442516156
    target_lng = 129.36800122423
    
    count = 0
    for item in data:
        if "성심상회" in item['n']:
            # Check if it needs updating
            if item['a'] != target_addr or item.get('lat') != target_lat:
                item['a'] = target_addr
                item['lat'] = target_lat
                item['lng'] = target_lng
                count += 1

    if count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Successfully merged {count} '성심상회' entries to: {target_addr}")
    else:
        print("No entries needed merging.")

if __name__ == "__main__":
    merge_seongsim()
