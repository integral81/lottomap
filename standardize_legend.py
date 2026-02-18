import json
import os
import re

db_path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json"
js_path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js"
index_path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\index.html"

# 1. Load data
with open(db_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Shops handled today (Legend and Final Batch)
today_shops = [
    # Batch 10
    "복터진날", "대구연쇄점", "동일통신", "싱글벙글 6/45", "동명로또", "돼지복권명당", "나이스로또복권", "금진슈퍼", "로또판매점(바이더웨이)",
    # Batch 11
    "가로판매점", "복권천국", "로또명당인주점", "돈벼락맞는곳", "천하명당", "대박찬스", "로또명당", "로또", "일등복권편의점", "로또휴게실", "복권왕국", "대박로또", "복권백화점", "주택복권방",
    # Sejin
    "세진전자통신",
    # Batch 12
    "운수대통", "인더라인 로또", "행운마트", "영화유통(1등복권방)"
]

# 2. Get the "Source of Truth" from index.html (Presets)
with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

presets_match = re.search(r"const ROADVIEW_PRESETS = \[(.*?)\];", content, re.DOTALL)
presets_raw = presets_match.group(1) if presets_match else ""

# Extract presets into a dict: name -> {addr, panoId, pov}
presets = {}
# Simple regex to extract name, addr, panoId, and pov block
# { name: "...", addr: "...", panoId: ..., pov: { ... } }
pattern = r'\{ name: "(.*?)", addr: "(.*?)", panoId: (.*?), pov: \{(.*?)\} \}'
matches = re.findall(pattern, presets_raw)

for name, addr, pano_id, pov_str in matches:
    # Parse pov_str: pan: 89.48, tilt: 3.05, zoom: -1
    pov_parts = re.findall(r'(\w+): ([\d\.-]+)', pov_str)
    pov_dict = {k: float(v) for k, v in pov_parts}
    presets[name] = {
        "addr": addr,
        "panoId": pano_id.strip(),
        "pov": pov_dict
    }

print(f"Loaded {len(presets)} source-of-truth presets.")

# 3. Propagate to lotto_data.json
updated_counts = {}
for name, source in presets.items():
    count = 0
    # First, find a reference entry with good coordinates if possible,
    # or just use the first entry we find.
    # Actually, for "Legend" shops, we might want to consolidate coordinates.
    target_coords = None
    
    # Pass 1: Find matching entries and pick first coordinates as target
    shop_entries = [s for s in data if name in s["n"] and (source["addr"][:10] in s["a"] or s["a"][:10] in source["addr"])]
    if not shop_entries:
        continue
        
    target_coords = (shop_entries[0]["lat"], shop_entries[0]["lng"])
    
    # Pass 2: Apply coordinates and POV to ALL entries
    for s in data:
        if name in s["n"] and (source["addr"][:10] in s["a"] or s["a"][:10] in source["addr"]):
            s["lat"] = target_coords[0]
            s["lng"] = target_coords[1]
            s["pov"] = {
                "id": str(source["panoId"]),
                "pan": source["pov"]["pan"],
                "tilt": source["pov"]["tilt"],
                "zoom": source["pov"]["zoom"]
            }
            count += 1
    updated_counts[name] = count

print(f"Updated total {sum(updated_counts.values())} entries across {len(updated_counts)} shops.")

# 4. Save results
with open(db_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=0, separators=(",", ":"), ensure_ascii=False)

js_content = "var lottoData = " + json.dumps(data, ensure_ascii=False, indent=0, separators=(",", ":")) + ";"
with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content)

# 5. Reorganize index.html
# Group today's shops and other high-win shops at the top
# But user said "오늘 등록한 최종버전으로 정리해주세요"
# I'll create a "Today's Finalized Legend" section

# We'll just sort them or move today's shops to a specific block if needed.
# For now, let's just ensure the presets array is clean (deduplicated).

new_presets_array = []
seen_names = set()

# First add today's shops in order
for ts in today_shops:
    if ts in presets and ts not in seen_names:
        p = presets[ts]
        line = f'            {{ name: "{ts}", addr: "{p["addr"]}", panoId: {p["panoId"]}, pov: {{ pan: {p["pov"]["pan"]}, tilt: {p["pov"]["tilt"]}, zoom: {p["pov"]["zoom"]} }} }},'
        new_presets_array.append(line)
        seen_names.add(ts)

# Then add the rest
# (Need to reload presets from raw to get non-parsed ones or just keep the ones we have)
# For simplicity, I'll just regenerate the array from the `presets` dict
for name, p in presets.items():
    if name not in seen_names:
        line = f'            {{ name: "{name}", addr: "{p["addr"]}", panoId: {p["panoId"]}, pov: {{ pan: {p["pov"]["pan"]}, tilt: {p["pov"]["tilt"]}, zoom: {p["pov"]["zoom"]} }} }},'
        new_presets_array.append(line)
        seen_names.add(ts)

# Replace the block in index.html
new_presets_block = "// --- Today's Finalized Legend Shops ---\n" + "\n".join(new_presets_array)
final_content = re.sub(r'const ROADVIEW_PRESETS = \[.*?\];', f'const ROADVIEW_PRESETS = [\n{new_presets_block}\n        ];', content, flags=re.DOTALL)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(final_content)

print("Organized index.html presets.")
