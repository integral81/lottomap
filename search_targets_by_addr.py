import json
import os
import sys

# Ensure stdout uses utf-8
if sys.stdout.encoding != 'utf-8':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\admin_targets.json"
keywords = ["장림로", "중앙대로783", "반여1동", "연산동", "사상로 90", "해맞이로 365", "이순신광장로", "좌수영로 11", "구서동 415"]

if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        targets = json.load(f)
    for t in targets:
        if any(k in t["address"] for k in keywords):
            print(f"Name: {t['name']} | Addr: {t['address']}")
else:
    print("Not found")
