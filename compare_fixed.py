
import json
import os

def compare_fixed():
    print("Comparing Fixed Feature Data...")
    
    try:
        with open('lotto_data_fixed.json', 'r', encoding='utf-8') as f:
            feature_data = json.load(f)
            
        print(f"Successfully loaded {len(feature_data)} records.")
        
        targets = [
            "황금복권방", "복권명당", "가판점", "GS25", "목화휴게소", 
            "cu", "복권판매점", "뉴빅마트", "대박찬스", "로또휴게실"
        ]
        
        print(f"\n--- Checking Targets in FEATURE_BRANCH ---")
        found_data = []
        
        for t in targets:
            for item in feature_data:
                if t in item.get('n', ''):
                    pov = item.get('pov')
                    if pov:
                        print(f"  [FOUND] {item['n']} HAS POV! (ID: {pov.get('id') or pov.get('panoId')})")
                        found_data.append(item)
                        break

        # If found, save them
        if found_data:
            with open('recovered_from_feature.json', 'w', encoding='utf-8') as f:
                 json.dump(found_data, f, indent=2, ensure_ascii=False)
            print(f"Saved {len(found_data)} recovered items.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    compare_fixed()
