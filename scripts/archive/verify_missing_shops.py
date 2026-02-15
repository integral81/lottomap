
import re
import os

def verify():
    html_path = 'index.html'
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    missing_candidates = [
        "인터넷 복권판매사이트",
        "인터넷복권판매사이트",
        "잠실매점",
        "로또열풍",
        "행운복권방",
        "메트로센터점",
        "행복한사람들",
        "명당본점"
    ]

    for cand in missing_candidates:
        if cand in content:
            print(f"Found '{cand}' in index.html")
        else:
            print(f"FAILED to find '{cand}' in index.html")

if __name__ == "__main__":
    verify()
