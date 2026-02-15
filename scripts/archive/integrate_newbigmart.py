
import json

# Target addresses and new standard address
OLD_ADDRS = [
    "부산 기장군 정관면 매학리 748-6번지 테라스상가1층119호",
    "부산 기장군 정관면 매학리748-6테라스상가1층119호",
    "부산 기장군 정관면 용수리 256-11",
    "부산 기장군 정관읍 매학리 748-6번지 테라스상가1층119호"
]
NEW_ADDR = "부산 기장군 정관읍 정관중앙로 48 106호"
NEW_LAT = 35.3210954459104
NEW_LNG = 129.179271340486

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated_count = 0
    for item in data:
        if "뉴빅마트" in item.get('n', ''):
            # Normalizing address for check
            addr = item.get('a', '')
            if any(old.replace(" ", "") in addr.replace(" ", "") for old in OLD_ADDRS) or "정관중앙로 48" in addr:
                item['a'] = NEW_ADDR
                item['lat'] = NEW_LAT
                item['lng'] = NEW_LNG
                updated_count += 1
                
    if updated_count > 0:
        with open('lotto_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Successfully integrated {updated_count} entries for '뉴빅마트' to the new address.")
    else:
        print("No matching entries found.")

except Exception as e:
    print(f"Error: {e}")
