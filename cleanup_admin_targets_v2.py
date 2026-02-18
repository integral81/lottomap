import json
import os

targets_json = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\admin_targets.json"
targets_js = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\admin_targets.js"

# Keywords and partial addresses for the 9 shops
registrations = [
    { "name": "복터진날", "addr": "부산 사하구 장림로 162-1" },
    { "name": "대구연쇄점", "addr": "부산 부산진구 중앙대로783번길 8" },
    { "name": "동일통신", "addr": "부산 해운대구 반여1동 1361-2" },
    { "name": "싱글벙글 6/45", "addr": "부산 연제구 연산동 1330-10" },
    { "name": "동명로또", "addr": "부산 사상구 사상로 90" },
    { "name": "돼지복권명당", "addr": "부산 기장군 해맞이로 365-1" },
    { "name": "나이스로또복권", "addr": "전남 여수시 이순신광장로 210" },
    { "name": "금진슈퍼", "addr": "전남 여수시 좌수영로 11" },
    { "name": "로또판매점(바이더웨이)", "addr": "부산 금정구 구서동 415-2" }
]

def is_match(target_name, target_addr, reg_name, reg_addr):
    # Match if the registration name is in target name, or vice versa
    # AND if the address has significant overlap
    name_match = reg_name in target_name or target_name in reg_name
    
    # Clean addresses for comparison (remove spaces)
    clean_target_addr = target_addr.replace(" ", "")
    clean_reg_addr = reg_addr.replace(" ", "")
    addr_match = clean_reg_addr in clean_target_addr or clean_target_addr in clean_reg_addr
    
    return name_match and addr_match

if os.path.exists(targets_json):
    with open(targets_json, "r", encoding="utf-8") as f:
        targets = json.load(f)
    
    initial_count = len(targets)
    new_targets = []
    removed_names = []
    
    for t in targets:
        matched = False
        for reg in registrations:
            if is_match(t["name"], t["address"], reg["name"], reg["addr"]):
                matched = True
                removed_names.append(t["name"])
                break
        if not matched:
            new_targets.append(t)
    
    if initial_count != len(new_targets):
        with open(targets_json, "w", encoding="utf-8") as f:
            json.dump(new_targets, f, indent=4, ensure_ascii=False)
        
        with open(targets_js, "w", encoding="utf-8") as f:
            f.write("window.allMissingShops = " + json.dumps(new_targets, indent=4, ensure_ascii=False) + ";")
        
        print(f"Removed {initial_count - len(new_targets)} shops: {', '.join(removed_names)}")
    else:
        print("Still no matches found with partial logic.")
else:
    print("admin_targets.json not found.")
