
import json

def merge_haengun_gunpo():
    file_path = 'lotto_data.json'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    # Standardized Target Info (The newer address)
    target_name = "행운복권"
    target_addr = "경기 군포시 대야1로 3 1동"
    target_lat = 37.323635
    target_lng = 126.912624
    
    count = 0
    rounds = []
    for item in data:
        # Match by name and location (Gunpo)
        if "행운복권" in item['n'] and "군포" in item['a']:
            item['n'] = target_name
            item['a'] = target_addr
            item['lat'] = target_lat
            item['lng'] = target_lng
            rounds.append(item['r'])
            count += 1

    if count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Successfully merged {count} '행운복권' (Gunpo) entries to: {target_addr}")
        print(f"Consolidated rounds: {sorted(list(set(rounds)))}")
    else:
        print("No entries needed merging.")

if __name__ == "__main__":
    merge_haengun_gunpo()
