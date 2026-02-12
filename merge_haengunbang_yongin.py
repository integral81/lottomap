
import json

def merge_haengunbang_yongin():
    file_path = 'lotto_data.json'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    # Standardized Target Info
    target_name = "행운방"
    target_addr = "경기 용인시 기흥구 보정동 1804-4 엘림프라자 101호"
    # Lat/Lng from the most consistent recent entries
    target_lat = 37.3204918797968
    target_lng = 127.108422409053
    
    count = 0
    rounds = []
    for item in data:
        # Match by name and general location (address containing "보정동" and name containing "행운방")
        if "행운방" in item['n'] and "보정동" in item['a']:
            item['n'] = target_name
            item['a'] = target_addr
            item['lat'] = target_lat
            item['lng'] = target_lng
            rounds.append(item['r'])
            count += 1

    if count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Successfully merged {count} '행운방' (Yongin) entries to: {target_addr}")
        print(f"Consolidated rounds: {sorted(list(set(rounds)))}")
    else:
        print("No entries needed merging.")

if __name__ == "__main__":
    merge_haengunbang_yongin()
