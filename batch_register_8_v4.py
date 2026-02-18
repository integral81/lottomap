import json
import os

db_path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json"
js_path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js"

with open(db_path, "r", encoding="utf-8") as f:
    data = json.load(f)

new_povs = [
    { "name": "구포라인점", "addr": "부산 북구 구포동 700-148", "panoid": "1202526432", "pov": { "pan": 255.82, "tilt": 3.43, "zoom": 1 } },
    { "name": "영화복권", "addr": "경남 창원시 진해구 안청남로 14", "panoid": "1204354980", "pov": { "pan": 175.08, "tilt": 0.44, "zoom": 1 } },
    { "name": "로또구포점", "addr": "부산 북구 덕천2길 23-3", "panoid": "1202240178", "pov": { "pan": 2.70, "tilt": 1.64, "zoom": -3 } },
    { "name": "큐마트학동점로또", "addr": "전남 여수시 학동서5길 2", "panoid": "1131607851", "pov": { "pan": 298.29, "tilt": -8.06, "zoom": 0 } },
    { "name": "씨스페이스(범어사역점)", "addr": "부산 금정구 남산동 21-4", "panoid": "1202570280", "pov": { "pan": 268.49, "tilt": 3.29, "zoom": 1 } },
    { "name": "우리로또복권방", "addr": "전남 여수시 무선중앙로 71", "panoid": "1205657400", "pov": { "pan": 358.65, "tilt": 8.13, "zoom": 1 } },
    { "name": "천하복권방", "addr": "울산 동구 전하로 29", "panoid": "1202146730", "pov": { "pan": 219.93, "tilt": -1.81, "zoom": -3 } },
    { "name": "일레븐마트무선점", "addr": "전남 여수시 성산로 19", "panoid": "1205608266", "pov": { "pan": 327.53, "tilt": -3.95, "zoom": -3 } }
]

modified_names = set()
for pov in new_povs:
    count = 0
    for s in data:
        # Match by name and partial address
        if pov["name"] in s["n"] and (pov["addr"] in s["a"] or s["a"] in pov["addr"]):
            s["pov"] = {
                "id": pov["panoid"],
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
