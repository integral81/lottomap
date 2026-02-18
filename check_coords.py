import json

def main():
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Target: 승리복권판매점
    target = next((s for s in data if '승리복권판매점' in s['n']), None)
    if target:
        print(f"Found: {target['n']}")
        print(f"Address: {target['a']}")
        print(f"Coords: {target['lat']}, {target['lng']}")
    else:
        print("Not found")

    # Diagnostic: Check for severe mismatches
    # Seoul Lat/Lng approx range: 37.4 ~ 37.7, 126.7 ~ 127.2
    # Busan Lat/Lng approx range: 35.0 ~ 35.3, 128.8 ~ 129.3
    
    print("\n--- Potential Mismatches ---")
    count = 0
    for s in data:
        addr = s.get('a', '')
        lat = s.get('lat', 0)
        lng = s.get('lng', 0)
        
        if '부산' in addr and (lat > 37 or lng < 128):
            print(f"[MISMATCH] {s['n']} ({addr}): {lat}, {lng} (Likely in Seoul/Gyeonggi)")
            count += 1
        elif '서울' in addr and (lat < 36):
            print(f"[MISMATCH] {s['n']} ({addr}): {lat}, {lng} (Likely in South)")
            count += 1
            
    print(f"Total potential mismatches found: {count}")

if __name__ == "__main__":
    main()
