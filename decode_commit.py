
def decode_and_search():
    files = ['commit_42_povs.txt', 'commit_3_povs.txt']
    targets = ["황금복권방", "로또휴게실", "복권명당", "가판점", "목화휴게소"]
    
    for fname in files:
        print(f"--- Scanning {fname} ---")
        try:
            with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            with open(fname.replace('.txt', '_clean.txt'), 'w', encoding='utf-8') as f_out:
                f_out.write(content)
                
            for t in targets:
                if t in content:
                    print(f"  [FOUND] {t}")
                    # Try to extract context (5 lines before/after)
                    idx = content.find(t)
                    start = max(0, idx - 500)
                    end = min(len(content), idx + 500)
                    print(f"    Context:\n{content[start:end]}\n")
                else:
                    print(f"  [NOT FOUND] {t}")
                    
        except Exception as e:
            print(f"Error reading {fname}: {e}")

if __name__ == "__main__":
    decode_and_search()
