import json
import os

db_path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json"
js_path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js"

with open(db_path, "r", encoding="utf-8") as f:
    data = json.load(f)

new_povs = [
    { "name": "복터진날", "addr": "부산 사하구 장림로 162-1", "panoid": "1202461118", "pov": { "pan": 131.58, "tilt": 3.84, "zoom": -1 } },
    { "name": "대구연쇄점", "addr": "부산 부산진구 중앙대로783번길 8", "panoid": "1202521545", "pov": { "pan": 58.86, "tilt": -0.64, "zoom": 2 } },
    { "name": "동일통신", "addr": "부산 해운대구 반여1동 1361-2", "panoid": "1202252207", "pov": { "pan": 80.63, "tilt": -0.40, "zoom": 0 } },
    { "name": "싱글벙글 6/45", "addr": "부산 연제구 연산동 1330-10", "panoid": "1202572760", "pov": { "pan": 324.08, "tilt": -3.02, "zoom": 1 } },
    { "name": "동명로또", "addr": "부산 사상구 사상로 90", "panoid": "1202163254", "pov": { "pan": 45.53, "tilt": -4.50, "zoom": 0 } },
    { "name": "돼지복권명당", "addr": "부산 기장군 해맞이로 365-1", "panoid": "1201909624", "pov": { "pan": 331.26, "tilt": -0.49, "zoom": 0 } },
    { "name": "나이스로또복권", "addr": "전남 여수시 이순신광장로 210", "panoid": "1164703398", "pov": { "pan": 101.56, "tilt": -8.26, "zoom": 0 } },
    { "name": "금진슈퍼", "addr": "전남 여수시 좌수영로 11", "panoid": "1205274554", "pov": { "pan": 272.72, "tilt": 4.27, "zoom": 0 } },
    { "name": "로또판매점(바이더웨이)", "addr": "부산 금정구 구서동 415-2", "panoid": "1202567242", "pov": { "pan": 280.79, "tilt": 1.67, "zoom": -3 } }
]

modified_names = set()
for pov in new_povs:
    count = 0
    for s in data:
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
