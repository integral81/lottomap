import json
import os

db_path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json"
js_path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js"
index_path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\index.html"

# 1. Update lotto_data.json
with open(db_path, "r", encoding="utf-8") as f:
    data = json.load(f)

new_addr = "대구 서구 서대구로 376"
new_pov = {
    "id": "1201585664",
    "pan": 89.48,
    "tilt": 3.05,
    "zoom": -1
}

count = 0
for s in data:
    if "세진전자통신" in s["n"]:
        s["a"] = new_addr
        s["pov"] = new_pov
        count += 1

print(f"Updated {count} entries for 세진전자통신 in lotto_data.json")

with open(db_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=0, separators=(",", ":"), ensure_ascii=False)

js_content = "var lottoData = " + json.dumps(data, ensure_ascii=False, indent=0, separators=(",", ":")) + ";"
with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content)

# 2. Update index.html
with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

# Update presets
import re

# Replace existing Sejin Electronics entries with one unified preset or update them
# The user wants this POV as the final version.
new_preset_line = '            { name: "세진전자통신", addr: "대구 서구 서대구로 376", panoId: 1201585664, pov: { pan: 89.48, tilt: 3.05, zoom: -1 } },'

# We'll replace lines containing "세진전자통신" in the presets array
lines = content.splitlines()
new_lines = []
skip_next = False
sejin_updated = False

for line in lines:
    if "세진전자통신" in line and "ROADVIEW_PRESETS" not in line:
        if not sejin_updated:
            new_lines.append(new_preset_line)
            sejin_updated = True
        continue
    new_lines.append(line)

with open(index_path, "w", encoding="utf-8") as f:
    f.write("\n".join(new_lines))

print("Updated index.html presets for 세진전자통신.")
