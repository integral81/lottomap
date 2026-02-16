
import re

def search_numbers():
    fname = 'commit_42_povs_utf8.txt'
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
        
    targets = {
        "Lotto Rest Area (PanoID)": "1199447820",
        "Golden Lottery (Lng)": "129.03",
        "Rest Area (Lat)": "37.256" # 37.256... for Lotto Rest Area
    }
    
    for name, value in targets.items():
        if value in content:
            print(f"[FOUND] {name}: {value}")
            # Context
            idx = content.find(value)
            start = max(0, idx - 300)
            end = min(len(content), idx + 300)
            print(content[start:end])
            print("-" * 40)
        else:
            print(f"[NOT FOUND] {name}: {value}")

if __name__ == "__main__":
    search_numbers()
