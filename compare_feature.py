
import json
import os

def compare_feature_branch():
    print("Comparing Feature Branch Data...")
    
    # Try multiple encodings
    encodings = ['utf-16', 'utf-8', 'cp949']
    feature_data = None
    
    for enc in encodings:
        try:
            with open('lotto_data_feature.json', 'r', encoding=enc) as f:
                feature_data = json.load(f)
            print(f"Successfully loaded JSON with {enc} encoding.")
            break
        except Exception as e:
            # print(f"Failed with {enc}: {e}")
            pass
            
    if not feature_data:
        print("Failed to load feature data with any encoding.")
        return

    targets = [
        "황금복권방", "복권명당", "가판점", "GS25", "목화휴게소", 
        "cu", "복권판매점", "뉴빅마트", "대박찬스", "로또휴게실"
    ]
    
    print(f"\n--- Checking Targets in FEATURE_BRANCH ---")
    found_count = 0
    for t in targets:
        found = False
        for item in feature_data:
            if t in item.get('n', ''):
                pov = item.get('pov')
                if pov:
                    print(f"  [FOUND] {item['n']} ({item['a']}) HAS POV! (ID: {pov.get('id') or pov.get('panoId')})")
                    found = True
                    # If found, save for recovery
                else:
                    # print(f"  [PARTIAL] {t} found but NO POV.")
                    pass
        if found:
            found_count += 1

    print(f"\nTotal Found in FEATURE_BRANCH: {found_count} / {len(targets)}")

if __name__ == "__main__":
    compare_feature_branch()
