
import json

def merge_dream_suwon():
    file_path = 'lotto_data.json'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    # Target: Seryu-dong 130
    target_addr = "경기 수원시 권선구 세류동 130"
    target_lat = 37.2638040961291
    target_lng = 127.014235447463
    
    count = 0
    for item in data:
        # Match "드림" in Suwon Seryu-dong or Seryu3-dong 130
        if item['n'] == "드림" and "수원" in item['a'] and "130" in item['a']:
            if item['a'] != target_addr or item.get('lat') != target_lat:
                item['a'] = target_addr
                item['lat'] = target_lat
                item['lng'] = target_lng
                count += 1

    if count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Successfully merged {count} '드림' (Suwon) entries to: {target_addr}")
    else:
        print("No entries needed merging.")

if __name__ == "__main__":
    merge_dream_suwon()
