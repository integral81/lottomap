
import json

def merge_wangdaebak_incheon():
    file_path = 'lotto_data.json'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    # Standardized Target Info
    target_name = "왕대박복권"
    target_addr = "인천 부평구 십정동 577-6"
    target_lat = 37.4773513046613
    target_lng = 126.709834722586
    
    # We want to merge "왕대박복권" and "베스트 로또" at 577-6
    # And potentially "왕대박복권" at 십정동 108 if we decide it's the same, 
    # but for now let's focus on 577-6 as it's the primary "New Big Mart" candidate.
    
    count = 0
    rounds = []
    for item in data:
        # Match by address containing "577-6" and "십정동"
        if "577-6" in item.get('a', '') and "십정동" in item.get('a', ''):
            item['n'] = target_name
            item['a'] = target_addr
            item['lat'] = target_lat
            item['lng'] = target_lng
            rounds.append(item['r'])
            count += 1

    if count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Successfully merged {count} entries at {target_addr} to: {target_name}")
        print(f"Consolidated rounds: {sorted(list(set(rounds)))}")
    else:
        print("No entries needed merging.")

if __name__ == "__main__":
    merge_wangdaebak_incheon()
