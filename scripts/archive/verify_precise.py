
import re

def verify_precise():
    html_path = 'index.html'
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    targets = [
        {"n": "로또열풍", "a": "내당동"},
        {"n": "행운복권방", "a": "진교면"},
        {"n": "명당본점", "a": "세교동"},
        {"n": "잠실매점", "a": "잠실역"},
        {"n": "메트로센터점", "a": "덕산동"}
    ]

    for t in targets:
        # Look for { name: "...", addr: "..." }
        # Pattern to find object starting with the name
        pattern = rf'\{{ name: "{t["n"]}", addr: ".*?{t["a"]}.*?".*?\}}'
        match = re.search(pattern, content)
        if match:
            print(f"MATCH FOUND: {t['n']} ({t['a']})")
        else:
            print(f"MISSING: {t['n']} ({t['a']})")

if __name__ == "__main__":
    verify_precise()
