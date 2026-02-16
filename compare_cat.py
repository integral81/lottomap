
import json

def compare_cat():
    print("Comparing CAT Data...")
    try:
        # Check file size
        import os
        size = os.path.getsize('lotto_data_CAT.json')
        print(f"File size: {size} bytes")
        
        
        # Robust Read
        with open('lotto_data_CAT.json', 'rb') as f:
            raw = f.read()
            
        # Try to detect encoding or just replace errors
        try:
            content = raw.decode('utf-16')
        except:
            try:
                content = raw.decode('utf-8')
            except:
                content = raw.decode('utf-8', errors='ignore')
                
        # Remove BOM if present
        content = content.replace('\ufeff', '')
        
        # Aggressive Control Character Removal
        # Remove 0x00-0x1F except \n(0x0A), \r(0x0D), \t(0x09)
        import re
        content = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', content)
        
        feature_data = json.loads(content)
                
        print(f"Loaded {len(feature_data)} records.")
        
        targets = [
            "황금복권방", "복권명당", "가판점", "GS25", "목화휴게소", 
            "cu", "복권판매점", "뉴빅마트", "대박찬스", "로또휴게실"
        ]
        
        found_data = []
        for t in targets:
            for item in feature_data:
                if t in item.get('n', ''):
                    pov = item.get('pov')
                    if pov:
                        print(f"  [FOUND] {item['n']} HAS POV! ({pov.get('id') or pov.get('panoId')})")
                        found_data.append(item)
                        # Don't break here, we might find multiple GS25s
                        
        print(f"Total Found from Feature Branch: {len(found_data)}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    compare_cat()

