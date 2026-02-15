
import json

def find_happy_addr():
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Address keywords: 산이리, 초월읍, 행복한
    targets = ["\uc0b0\uc774\ub9ac", "\ucd08\uc6d4\uc74d", "\ud589\ubcfc\ud55c"]
    
    results = {}
    for e in data:
        n = e.get('n', '')
        a = e.get('a', '')
        match = False
        for t in targets:
            if t in a or t in n:
                match = True
                break
        
        if match:
            k = f"{n}|{a}"
            if k not in results:
                results[k] = {"n": n, "a": a, "w": 0}
            results[k]["w"] += 1
            
    for s in results.values():
        en = s['n'].encode('ascii', 'xmlcharrefreplace').decode()
        ea = s['a'].encode('ascii', 'xmlcharrefreplace').decode()
        print(f"[{s['w']} wins] {en} | {ea}")

if __name__ == "__main__":
    find_happy_addr()
