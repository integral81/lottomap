
import json

def merge_bukmun():
    file_path = 'lotto_data.json'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    # Target: Current verified location (정조로 927-1)
    target_addr = "경기 수원시 장안구 정조로 927-1"
    target_lat = 37.2902970908823
    target_lng = 127.012826577136
    
    count = 0
    for item in data:
        # Match "북문복권방" or address 311-12
        is_bukmun = "북문복권방" in item['n']
        is_addr_match = "311-12" in item.get('a', '') or (item.get('lat') and abs(item['lat'] - 37.290279) < 0.0001)
        
        if is_bukmun or is_addr_match:
            # Check if it needs updating
            if item['a'] != target_addr or item.get('lat') != target_lat:
                item['a'] = target_addr
                item['n'] = "북문복권방" # Standardize name too
                item['lat'] = target_lat
                item['lng'] = target_lng
                count += 1

    if count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Successfully merged {count} '북문복권방' entries to: {target_addr}")
    else:
        # Check total wins now
        total_wins = sum(1 for d in data if d['n'] == "북문복권방")
        print(f"No entries needed merging. Total wins for '북문복권방' already at {total_wins}.")

if __name__ == "__main__":
    merge_bukmun()
