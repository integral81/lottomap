import json
import os

targets_json = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\admin_targets.json"
targets_js = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\admin_targets.js"

# Keywords and partial addresses for the 8 shops
registrations = [
    { "name": "구포라인점", "addr": "부산 북구 구포동 700-148" },
    { "name": "영화복권", "addr": "경남 창원시 진해구 안청남로 14" },
    { "name": "로또구포점", "addr": "부산 북구 덕천2길 23-3" },
    { "name": "큐마트학동점로또", "addr": "전남 여수시 학동서5길 2" },
    { "name": "씨스페이스(범어사역점)", "addr": "부산 금정구 남산동 21-4" },
    { "name": "우리로또복권방", "addr": "전남 여수시 무선중앙로 71" },
    { "name": "천하복권방", "addr": "울산 동구 전하로 29" },
    { "name": "일레븐마트무선점", "addr": "전남 여수시 성산로 19" }
]

def is_match(target_name, target_addr, reg_name, reg_addr):
    # Match if registration name is in target name, or vice versa
    name_match = reg_name in target_name or target_name in reg_name
    
    # Clean addresses for comparison
    clean_target_addr = target_addr.replace(" ", "").replace("-", "")
    clean_reg_addr = reg_addr.replace(" ", "").replace("-", "")
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
        
        print(f"Removed {initial_count - len(new_targets)} shops from admin target list.")
        print(f"Removed: {', '.join(removed_names)}")
    else:
        print("No matches found for cleanup in Batch 4.")
else:
    print("admin_targets.json not found.")
