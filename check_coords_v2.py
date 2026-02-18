import json

def main():
    try:
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return
    
    # Target: 승리복권판매점
    target = next((s for s in data if '승리복권판매점' in s.get('n', '')), None)
    if target:
        print(f"Found: {target['n']}")
        print(f"Address: {target.get('a', 'No Address')}")
        print(f"Coords: {target.get('lat', 'None')}, {target.get('lng', 'None')}")
    else:
        print("Target '승리복권판매점' not found in JSON.")

    print("\n--- Potential Mismatches ---")
    count = 0
    
    # Define bounding boxes roughly
    # Seoul/Gyeonggi: lat 36.5+, lng 126.0+
    # Busan/Gyeongsang: lat < 36.0, lng > 128.0
    # Jeolla: lat < 36.0, lng < 128.0
    
    mismatches = []
    
    for s in data:
        addr = s.get('a', '')
        lat = s.get('lat')
        lng = s.get('lng')
        
        if lat is None or lng is None:
            continue
            
        try:
            lat = float(lat)
            lng = float(lng)
        except:
            continue
            
        # 1. Busan address but high latitude (Seoul?)
        if '부산' in addr and lat > 36.5:
             msg = f"[BUSAN_ERROR] {s['n']} ({addr}): {lat}, {lng}"
             print(msg)
             mismatches.append(s)
             count += 1
             
        # 2. Seoul address but low latitude (South?)
        elif '서울' in addr and lat < 36.0:
             msg = f"[SEOUL_ERROR] {s['n']} ({addr}): {lat}, {lng}"
             print(msg)
             mismatches.append(s)
             count += 1
             
    print(f"Total mismatches found: {count}")
    
    if mismatches:
        with open('mismatched_shops.json', 'w', encoding='utf-8') as f:
            json.dump(mismatches, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
