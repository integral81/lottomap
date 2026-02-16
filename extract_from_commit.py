
import json
import re

def extract_povs():
    targets = [
        "황금복권방", "복권명당", "가판점(2호선)", "GS25(청주주성점)", 
        "목화휴게소", "cu(수성그린점)", "복권판매점", "CU(구미원평점)", 
        "뉴빅마트", "대박찬스", "로또휴게실"
    ]
    
    with open('commit_42_povs_safe.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        
    found_data = []
    
    # Simple block extraction logic
    # Look for name: "Target" and extract the block
    
    lines = content.split('\n')
    for i, line in enumerate(lines):
        for t in targets:
            if t in line and '"name":' in line:
                # Found a potential match. Extract the block { ... }
                # The block usually spans ~5-6 lines
                block_str = ""
                for j in range(max(0, i-1), min(len(lines), i+10)):
                    block_str += lines[j] + "\n"
                    if "}," in lines[j] or "}" in lines[j]:
                        if j > i: # Ensure we capture the closing brace
                            break
                
                # Clean up the block string to be valid JSON-like
                # Remove + or - at start of lines (git diff markers)
                clean_block = ""
                for l in block_str.split('\n'):
                    l = l.strip()
                    if l.startswith('+') or l.startswith('-'):
                        l = l[1:]
                    clean_block += l + "\n"
                
                print(f"--- Found {t} ---")
                print(clean_block[:200] + "...")
                found_data.append(clean_block)

    # Also check commit_6_povs_safe.txt
    try:
        with open('commit_6_povs_safe.txt', 'r', encoding='utf-8') as f:
            content6 = f.read()
        lines6 = content6.split('\n')
        for i, line in enumerate(lines6):
            if "복권명당" in line and '"name":' in line: # Lottery Masterpiece
                 print("--- Found 복권명당 in Commit 6 ---")
                 # Extract logic (omitted for brevity, just print line)
                 print(line)
    except:
        pass

if __name__ == "__main__":
    extract_povs()
