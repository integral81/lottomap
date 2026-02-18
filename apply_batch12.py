import json
import os

db_path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json"
js_path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js"

with open(db_path, "r", encoding="utf-8") as f:
    data = json.load(f)

new_povs = [
    { "name": "운수대통", "addr": "경기 군포시 군포로745번길 24", "panoid": "1175676242", "pov": { "pan": 321.44, "tilt": 4.25, "zoom": -3 } },
    { "name": "인더라인 로또", "addr": "인천 부평구 십정동 577-6", "panoid": "1198797088", "pov": { "pan": 283.28, "tilt": -0.18, "zoom": 0 } },
    { "name": "행운마트", "addr": "인천 동구 송림로 71-1", "panoid": "1199336752", "pov": { "pan": 338.98, "tilt": -1.36, "zoom": -2 } },
    { "name": "영화유통(1등복권방)", "addr": "경북 포항시 북구 양학천로 15", "panoid": "1187457532", "pov": { "pan": 32.63, "tilt": -4.20, "zoom": 0 } }
]

modified_names = set()
for pov in new_povs:
    count = 0
    for s in data:
        if pov["name"] in s["n"] and (pov["addr"][:10] in s["a"] or s["a"][:10] in pov["addr"]):
            s["pov"] = {
                "id": str(pov["panoid"]),
                "pan": pov["pov"]["pan"],
                "tilt": pov["pov"]["tilt"],
                "zoom": pov["pov"]["zoom"]
            }
            count += 1
    if count > 0:
        modified_names.add(pov["name"])
    print(f"Updated {pov['name']}: {count} entries.")

with open(db_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=0, separators=(",", ":"), ensure_ascii=False)

js_content = "var lottoData = " + json.dumps(data, ensure_ascii=False, indent=0, separators=(",", ":")) + ";"
with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"Total shops updated: {len(modified_names)}")
