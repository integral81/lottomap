import json
import os
import re

db_path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json"
js_path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js"
index_path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\index.html"

# 1. Update lotto_data.json
with open(db_path, "r", encoding="utf-8") as f:
    data = json.load(f)

shop_name = "일등복권방"
shop_addr = "경기 시흥시 시청로68번길 4 1층 124호"
new_pov = {
    "id": "1175988907",
    "pan": 43.68,
    "tilt": 6.67,
    "zoom": -2
}
custom_msg = "매장은 건물 내부에 있음!!"

count = 0
for s in data:
    # Match by name and address (first 10 chars for safety)
    if shop_name in s["n"] and (shop_addr[:15] in s["a"] or s["a"][:15] in shop_addr):
        s["pov"] = new_pov
        s["customMessage"] = custom_msg
        count += 1

print(f"Updated {count} entries for {shop_name} in lotto_data.json")

with open(db_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=0, separators=(",", ":"), ensure_ascii=False)

js_content = "var lottoData = " + json.dumps(data, ensure_ascii=False, indent=0, separators=(",", ":")) + ";"
with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content)

# 2. Update index.html presets
with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

new_preset = f'            {{ name: "{shop_name}", addr: "{shop_addr}", panoId: {new_pov["id"]}, pov: {{ pan: {new_pov["pan"]}, tilt: {new_pov["tilt"]}, zoom: {new_pov["zoom"]} }}, customMessage: "{custom_msg}" }},'

# Insert at the top of ROADVIEW_PRESETS
insert_pos = content.find("const ROADVIEW_PRESETS = [")
if insert_pos != -1:
    opening_bracket_pos = content.find("[", insert_pos)
    new_content = content[:opening_bracket_pos+1] + "\n" + new_preset + content[opening_bracket_pos+1:]
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Updated index.html presets.")
else:
    print("ROADVIEW_PRESETS not found in index.html.")
