
def search_decoded():
    files = ['commit_42_povs_utf8.txt', 'commit_golden_pig_utf8.txt']
    targets = [
        "황금복권방", "복권명당", "가판점", "GS25", "목화휴게소", 
        "cu", "복권판매점", "뉴빅마트", "대박찬스", "로또휴게실"
    ]
    
    for fname in files:
        print(f"--- Scanning {fname} ---")
        try:
            with open(fname, 'r', encoding='utf-8') as f:
                content = f.read()
                
            for t in targets:
                if t in content:
                    print(f"  [FOUND] {t}")
                    # Extract context
                    idx = content.find(t)
                    # Try to find the start of the object {
                    start_obj = content.rfind('{', 0, idx)
                    # Try to find the end of the object }
                    end_obj = content.find('}', idx)
                    
                    if start_obj != -1 and end_obj != -1:
                        snippet = content[start_obj:end_obj+1]
                        # Clean up formatting
                        snippet = snippet.replace('\n+', '\n').replace('\n-', '\n')
                        print(f"    Object:\n{snippet}\n")
                else:
                    pass 
                    # print(f"  [NOT FOUND] {t}")
                    
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    search_decoded()
