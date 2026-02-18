import json
import os

path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\admin_targets.json"
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        targets = json.load(f)
    for t in targets:
        # Check for keywords in either name or address
        keywords = ["복터진", "대구", "동일", "싱글", "동명", "돼지", "나이스", "금진", "바이더", "부산", "여수"]
        if any(k in t["name"] or k in t["address"] for k in keywords):
            print(f"Name: {t['name']} | Addr: {t['address']}")
else:
    print("Not found")
