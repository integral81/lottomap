
import os

def decode_and_search_v3():
    files = ['commit_42_povs.txt', 'commit_golden_pig.txt']
    targets = [
        "황금복권방", "복권명당", "가판점", "GS25", "목화휴게소", 
        "cu", "복권판매점", "뉴빅마트", "대박찬스", "로또휴게실"
    ]
    
    for fname in files:
        if not os.path.exists(fname): continue
        
        print(f"--- Processing {fname} ---")
        content = ""
        try:
            # Try UTF-16 first (PowerShell default)
            with open(fname, 'r', encoding='utf-16') as f:
                content = f.read()
            print("  -> Decoded as UTF-16")
        except:
            try:
                # Fallback to UTF-8
                with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                print("  -> Decoded as UTF-8")
            except:
                print("  -> Failed to decode")
                continue
                
                
        # Save to UTF-8 file
        out_name = fname.replace('.txt', '_utf8.txt')
        with open(out_name, 'w', encoding='utf-8') as f_out:
            f_out.write(content)
        print(f"  -> Saved decoded content to {out_name}")

if __name__ == "__main__":
    decode_and_search_v3()

