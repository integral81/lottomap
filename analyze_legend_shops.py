import json
import os
import re

db_path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json"
index_path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\index.html"

# 1. Load data
with open(db_path, "r", encoding="utf-8") as f:
    data = json.load(f)

with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

# 2. Extract ROADVIEW_PRESETS
match = re.search(r"const ROADVIEW_PRESETS = \[(.*?)\];", content, re.DOTALL)
if not match:
    print("ROADVIEW_PRESETS not found")
    exit(1)

presets_raw = match.group(1)
# Simple parser for the list (since it's JS-like)
# Looking for lines like { name: "...", addr: "...", panoId: ..., pov: { ... } }
preset_lines = re.findall(r'\{ name: "(.*?)", addr: "(.*?)".*?\}', presets_raw)

print(f"Total presets found: {len(preset_lines)}")

# 3. Analyze shops
report = []
for name, addr in preset_lines:
    # Find all entries for this shop
    matches = [s for s in data if name in s["n"] and (addr[:10] in s["a"] or s["a"][:10] in addr)]
    
    if not matches:
        # Retry with just name if no match
        matches = [s for s in data if name == s["n"]]
        
    win_count = len(matches)
    coords = set([(s["lat"], s["lng"]) for s in matches])
    povs = set([s.get("pov", {}).get("id") for s in matches if "pov" in s])
    
    report.append({
        "name": name,
        "addr": addr,
        "wins": win_count,
        "unique_coords": len(coords),
        "coords": list(coords),
        "unique_povs": len(povs),
        "pov_ids": list(povs)
    })

# 4. Filter "Legend" shops (e.g. wins >= 5 or today's additions)
# We consider the ones at the top (today's additions) as high priority
# Plus any others with high win counts
legend_report = [r for r in report if r["wins"] >= 5]

print("\n--- Legend Shops Analysis (5+ Wins) ---")
for r in sorted(legend_report, key=lambda x: x["wins"], reverse=True):
    status = "OK" if r["unique_coords"] == 1 and r["unique_povs"] == 1 else "CONSISTENCY ISSUE"
    print(f"Shop: {r['name']} ({r['wins']} wins) | Coords: {r['unique_coords']} | POVs: {r['unique_povs']} | Status: {status}")
    if status != "OK":
        print(f"  Details: Coords: {r['coords']}, POVs: {r['pov_ids']}")

# 5. Check if any shop has NO POV in data but is in presets
# (Shouldn't happen if my scripts ran correctly)
