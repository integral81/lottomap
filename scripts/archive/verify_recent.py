
import re

def verify_recent():
    html_path = 'index.html'
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    targets = [
        "행운을주는사람들",
        "형제상회",
        "행운복권방"
    ]

    for t in targets:
        if t in content:
            print(f"CONFIRMED: '{t}' is in index.html")
        else:
            print(f"MISSING: '{t}' is NOT in index.html")

if __name__ == "__main__":
    verify_recent()
