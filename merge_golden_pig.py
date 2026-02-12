
import json

def merge_golden_pig():
    file_path = 'lotto_data.json'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    # Target info (Current Location: Geoje-dong 70-6)
    target_addr_keyword = "거제동 70-6"
    target_lat = 35.194867326912
    target_lng = 129.080392311637
    # Note: We'll use the full address string from the existing target entry if we find it, otherwise construct one.
    
    # Find exact target address string first to be consistent
    target_full_addr = None
    for item in data:
        if "황금돼지" in item['n'] and target_addr_keyword in item['a']:
            target_full_addr = item['a']
            break
    
    if not target_full_addr:
        target_full_addr = "부산 연제구 거제동 70-6" # Fallback
        print("Warning: Exact target entry not found, using fallback address.")

    print(f"Target Location: {target_full_addr} ({target_lat}, {target_lng})")

    # Source info (Old Location: Geoje-dong 36-8)
    source_addr_keyword = "거제동 36-8"
    
    count = 0
    for item in data:
        if "황금돼지" in item['n'] and source_addr_keyword in item['a']:
            print(f"Moving entry {item['r']}회 from '{item['a']}' -> Target")
            item['a'] = target_full_addr
            item['lat'] = target_lat
            item['lng'] = target_lng
            count += 1

    if count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\nSuccessfully moved {count} old entries to the current location.")
    else:
        print("\nNo old entries found to move.")

if __name__ == "__main__":
    merge_golden_pig()
