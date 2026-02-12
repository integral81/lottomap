
import json

def merge_newbigmart():
    file_path = 'lotto_data.json'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    # Target: Current valid location (748-5 / 정관중앙로 48)
    # Using coords from the most frequent recent entries
    target_addr = "부산 기장군 정관읍 정관중앙로 48 106호"
    target_lat = 35.3210954459104
    target_lng = 129.179271340486
    
    count = 0
    for item in data:
        if "뉴빅마트" in item['n']:
            # Check if it needs updating
            if item['a'] != target_addr or item.get('lat') != target_lat:
                item['a'] = target_addr
                item['lat'] = target_lat
                item['lng'] = target_lng
                count += 1

    if count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Successfully merged {count} '뉴빅마트' entries to: {target_addr}")
        
        # After merging, we should also update the admin tool data if necessary
        # But since the admin tool's top_shops_4wins.json is a static snapshot,
        # it might still show the old entries until regenerated.
        # I will manually remove them from admin_roadview.html's embedded data.
    else:
        print("No entries needed merging.")

if __name__ == "__main__":
    merge_newbigmart()
