import json
import os

path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\admin_targets.json"
keywords = ["복터진", "대구", "동일", "싱글", "동명", "돼지", "나이스", "금진", "바이더", "162-1", "783", "1361", "1330", "90", "365", "210", "11", "415"]

if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        targets = json.load(f)
    print(f"Total entries: {len(targets)}")
    for t in targets:
        if any(k in t["name"] or k in t["address"] for k in keywords):
            print(f"Match found: {t['name']} | {t['address']}")
else:
    print("File not found.")
