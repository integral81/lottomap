
import json

def fix_erroneous_tags():
    try:
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    count = 0
    erroneous_text = "중앙대로 1520"
    preserved_shop = "로또오션"

    for item in data:
        if 'pending_relocation' not in item:
            continue
            
        comment = item['pending_relocation']
        
        # Check if this is the erroneous "Jungang-daero 1520" tag
        if erroneous_text in comment:
            # EXCEPTION: If it is the real "Lotto Ocean" shop in Busan (Yeonsan-dong), keep it!
            # We check name and address keywords to be safe
            is_real_ocean = (preserved_shop in item['n']) and ('연산' in item['a'])
            
            if is_real_ocean:
                print(f"Keeping valid relocation tag for: {item['n']} ({item['a']})")
                continue
            
            # For all others, DELETE the tag
            print(f"Removing erroneous tag from: {item['n']} ({item['a']})")
            del item['pending_relocation']
            count += 1

    with open('lotto_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n--- Cleanup Complete ---")
    print(f"Removed erroneous 'pending_relocation' tags from {count} shops.")
    print("These shops will remain at their original location.")

if __name__ == "__main__":
    fix_erroneous_tags()
