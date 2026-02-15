
import json

# 1. Register "씨유 대전반석역점"
# 2. Search for "아이러브" in Ulsan to compare 2nd and 3rd shops

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Update 씨유 대전반석역점
    cu_count = 0
    for item in data:
        if "씨유 대전반석역점" in item.get('n', '') and "반석로 10" in item.get('a', ''):
            item['pov'] = { "id": "1200979469", "pan": 38.43, "tilt": 5.00, "fov": 40 }
            cu_count += 1
    
    # Search for 아이러브 shops in Ulsan
    ulsan_shops = []
    for item in data:
        if "아이러브" in item.get('n', '') and "울산" in item.get('a', ''):
            ulsan_shops.append(item)
            
    print(f"Updated {cu_count} entries for 씨유 대전반석역점.")
    print(f"\nFound {len(ulsan_shops)} entries for '아이러브' in Ulsan:")
    for shop in ulsan_shops:
        print(json.dumps(shop, ensure_ascii=False))

    if cu_count > 0:
        with open('lotto_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

except Exception as e:
    print(f"Error: {e}")
