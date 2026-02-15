
import json

def extract_remaining():
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Target shop names (approximations)
    targets = [
        "\uc7a0\uc2e4\ub9e4\uc810",           # 잠실매점
        "\ub178\ub2e4\uc131\ubcf5\uad8c\ubc29", # 노다지복권방 (Note: found earlier as "노다지복권방" but let's be flexible)
        "\ub178\ub2e4\uc9c0\ubcf5\uad8c\ubc29",
        "\uba54\ud2b8\ub85c\uc13c\ud130\uc810",   # 메트로센터점
        "\ud589\ubcf5\ud55c\uc0ac\ub78c\ub4e4"    # 행복한사람들
    ]
    
    counts = {}
    for e in data:
        n = e.get('n', '')
        a = e.get('a', '')
        for t in targets:
            if t in n:
                k = f"{n}|{a}"
                if k not in counts:
                     counts[k] = {"n": n, "a": a, "w": 0}
                counts[k]["w"] += 1
                
    results = [s for s in counts.values() if s["w"] >= 4]
    
    for s in results:
        en = s['n'].encode('ascii', 'xmlcharrefreplace').decode()
        ea = s['a'].encode('ascii', 'xmlcharrefreplace').decode()
        print(f"[{s['w']} wins] {en} | {ea}")

if __name__ == "__main__":
    extract_remaining()
