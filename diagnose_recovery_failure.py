import json
import glob

keywords = ["온천장", "수완", "베스트원", "춘향", "서문큰장", "소화로", "동성아파트", "중흥파크", "시티프라자"]

print("Diagnosing backups for keywords...")
files = glob.glob('*.json') + glob.glob('*.bak')

results = {}

for fp in files:
    try:
        with open(fp, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for s in data:
            n = s.get('n', '')
            a = s.get('a', '')
            combined = n + " " + a
            
            for k in keywords:
                if k in combined:
                    if s.get('pov'):
                        # Found a candidate with POV
                        key = f"{k}|{fp}"
                        if key not in results:
                            print(f"[{fp}] POV found for '{k}': {n} / {a}")
                            # print(f"    POV: {s['pov']}")
    except:
        pass
