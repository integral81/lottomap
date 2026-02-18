import json
import os

targets_json = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\admin_targets.json"
targets_js = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\admin_targets.js"

registered_names = {
    "복터진날", "대구연쇄점", "동일통신", "싱글벙글 6/45", "동명로또", 
    "돼지복권명당", "나이스로또복권", "금진슈퍼", "로또판매점(바이더웨이)"
}

if os.path.exists(targets_json):
    with open(targets_json, "r", encoding="utf-8") as f:
        targets = json.load(f)
    
    new_targets = [t for t in targets if t["name"] not in registered_names]
    
    with open(targets_json, "w", encoding="utf-8") as f:
        json.dump(new_targets, f, indent=4, ensure_ascii=False)
    
    with open(targets_js, "w", encoding="utf-8") as f:
        f.write("window.allMissingShops = " + json.dumps(new_targets, indent=4, ensure_ascii=False) + ";")
    
    print(f"Removed {len(targets) - len(new_targets)} shops from admin target list.")
else:
    print("admin_targets.json not found.")
