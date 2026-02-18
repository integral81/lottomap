import json
import glob

# Address keywords for missing shops
# 세븐일레븐부산온천장역점: 부산 동래구 온천동 156-1
# 세븐일레븐 수완점: 광주 광산구 수완동 1428
# 베스트원: 전남 영광군 영광읍 남천리 315
# 춘향로또: 전북 남원시 동림로 102-1 (?) Check screenshot
# 복권판매소(서문큰장네거리): 대구 서구 국채보상로 438
# 청구마트: 대구 북구 검단로 34
# 월드복권: ??

addr_keywords = {
    "156-1": "세븐일레븐부산온천장역",
    "1428": "세븐일레븐 수완점",
    "315": "베스트원",
    "102-1": "춘향로또",
    "438": "서문큰장",
    "34": "청구마트"
}

print("Mining backups by ADDRESS...")
files = glob.glob('*.json') + glob.glob('*.bak')

found_povs = {}

for fp in files:
    try:
        with open(fp, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for s in data:
            addr = s.get('a', '')
            for k, tag in addr_keywords.items():
                if k in addr:
                    if s.get('pov'):
                         # Store specifically using the Tag
                         # We want the BEST POV (maybe latest?)
                         # Let's just print found ones first
                         print(f"[{fp}] FOUND POV for {tag} ({s['n']})")
                         # Store if not present
                         if tag not in found_povs:
                             found_povs[tag] = s
    except:
        pass

if found_povs:
    print("\nRecovered Data:")
    for tag, s in found_povs.items():
        print(f"{tag}: {s['pov']}")
else:
    print("\nNo POVs found by address search.")
