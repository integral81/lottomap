
import subprocess
import json
import re

def direct_extract():
    # Git command to get raw content
    cmd = ["git", "show", "feature/roadview-260210-2단계:lotto_data.json"]
    
    print("Running git show via subprocess...")
    try:
        # Capture raw bytes
        raw = subprocess.check_output(cmd)
        print(f"Captured {len(raw)} bytes.")
        
        # Decode
        content = ""
        decoded_enc = "unknown"
        
        # Try UTF-16 LE (common for Windows generated files in this repo)
        try:
            content = raw.decode('utf-16')
            decoded_enc = "utf-16"
        except:
            try:
                content = raw.decode('utf-8')
                decoded_enc = "utf-8"
            except:
                content = raw.decode('cp949', errors='ignore')
                decoded_enc = "cp949"
                
        print(f"Decoded as {decoded_enc}.")
        
        # Cleanup
        content = content.replace('\ufeff', '')
        
        # JSON Load
        data = []
        try:
            data = json.loads(content)
            print(f"Parsed JSON: {len(data)} items.")
        except Exception as e:
            print(f"JSON Parse Error: {e}")
            # Fallback: Regex search if JSON fails
            print("Attempting Regex Search on raw content...")
            
        # Target Check
        targets = [
            "황금복권방", "복권명당", "가판점", "GS25", "목화휴게소", 
            "cu", "복권판매점", "뉴빅마트", "대박찬스", "로또휴게실"
        ]
        
        found_data = []
        
        if data:
            # JSON Search
            for item in data:
                n = item.get('n', '')
                for t in targets:
                    if t in n:
                        pov = item.get('pov')
                        if pov:
                            print(f"  [JSON MATCH] {n} HAS POV: {pov}")
                            found_data.append(item)
        else:
            # Regex Search
            for t in targets:
                # Look for name and pov pattern near it
                # This is hard on raw string but let's try
                if t in content:
                    print(f"  [TEXT MATCH] {t} found in text (Context pending)")
                    
        # Save results
        if found_data:
            with open('recovered_feature_direct.json', 'w', encoding='utf-8') as f:
                json.dump(found_data, f, indent=2, ensure_ascii=False)
            print(f"Saved {len(found_data)} recovered items.")
            
    except subprocess.CalledProcessError as e:
        print(f"Git Error: {e}")

if __name__ == "__main__":
    direct_extract()
