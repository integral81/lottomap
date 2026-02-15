
import json
import re

def normalize(text):
    if not text: return ""
    # Remove whitespace and parentheses for lenient matching
    return re.sub(r'[\s\(\)\[\]]', '', text).lower()

def audit_exhaustive():
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Parse presets
    presets_match = re.search(r'const ROADVIEW_PRESETS = \[(.*?)\];', html, re.DOTALL)
    presets = []
    if presets_match:
        objects = re.findall(r'\{(.*?)\}', presets_match.group(1), re.DOTALL)
        for obj in objects:
            n = normalize(re.search(r'name:\s*"(.*?)"', obj).group(1)) if re.search(r'name:\s*"(.*?)"', obj) else ""
            a = normalize(re.search(r'addr:\s*"(.*?)"', obj).group(1)) if re.search(r'addr:\s*"(.*?)"', obj) else ""
            v = bool(re.search(r'panoId|imageUrl|customLink', obj))
            c = bool(re.search(r'isClosed:\s*true', obj))
            presets.append({"n": n, "a": a, "v": v, "c": c})

    # Group data
    shops = {}
    for e in data:
        n = e.get('n', '').strip()
        a = e.get('a', '').strip()
        k = f"{n}|{a}"
        if k not in shops:
            shops[k] = {"n": n, "a": a, "wins": 0, "pov": False, "closed": e.get('isClosed', False)}
        shops[k]["wins"] += 1
        if 'pov' in e: shops[k]["pov"] = True

    missing = []
    for k, s in shops.items():
        if s["wins"] >= 4:
            has_visual = s["pov"]
            is_closed = s["closed"]
            
            if not has_visual and not is_closed:
                # Check presets with normalization
                sn_norm = normalize(s["n"])
                sa_norm = normalize(s["a"])
                FoundInPreset = False
                for p in presets:
                    if sn_norm in p["n"] or p["n"] in sn_norm:
                        # Names match partially, check address
                        if sa_norm[:10] in p["a"] or p["a"][:10] in sa_norm:
                            if p["v"] or p["c"]:
                                FoundInPreset = True
                                break
                if not FoundInPreset:
                    missing.append(s)

    print(f"REPORT: {len(missing)} shops missing visual data.")
    for m in missing:
        print(f"[{m['wins']} wins] {m['n']} - {m['a']}")

if __name__ == "__main__":
    audit_exhaustive()
