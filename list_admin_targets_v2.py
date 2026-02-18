import json
import os
import sys

# Ensure stdout uses utf-8
if sys.stdout.encoding != 'utf-8':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\admin_targets.json"
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        targets = json.load(f)
    for t in targets:
        print(f"Name: {t['name']} | Addr: {t['address']}")
else:
    print("Not found")
