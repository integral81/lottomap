import json
import os
import sys

# Ensure stdout uses utf-8
if sys.stdout.encoding != 'utf-8':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\admin_targets.json"
keywords = ["구포", "영화", "큐마트", "씨스페이스", "범어사", "우리", "전하", "일레븐", "학동", "진해", "무선", "북구"]

if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        targets = json.load(f)
    print(f"Total entries: {len(targets)}")
    for t in targets:
        if any(k in t["name"] or k in t["address"] for k in keywords):
            print(f"Candidate: {t['name']} | Addr: {t['address']}")
else:
    print("File not found.")
