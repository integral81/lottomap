
import os

def decode_safely():
    files = ['commit_42_povs.txt', 'commit_6_povs.txt', 'commit_3_povs.txt']
    
    for fname in files:
        if not os.path.exists(fname):
            print(f"Skipping {fname} (not found)")
            continue
            
        print(f"Decoding {fname}...")
        try:
            with open(fname, 'r', encoding='utf-8', errors='ignore') as f_in:
                content = f_in.read()
            
            out_name = fname.replace('.txt', '_safe.txt')
            with open(out_name, 'w', encoding='utf-8') as f_out:
                f_out.write(content)
                
            print(f"  -> Saved to {out_name}")
            
            # Simple search within python
            if "황금" in content:
                print(f"  [!] FOUND '황금' in {fname}")
            if "부산진구" in content:
                print(f"  [!] FOUND '부산진구' in {fname}")
            if "수성구" in content: # For Lottery Masterpiece
                print(f"  [!] FOUND '수성구' in {fname}")
                
        except Exception as e:
            print(f"  Error: {e}")

if __name__ == "__main__":
    decode_safely()
