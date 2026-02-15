
import json

def search_nodaji():
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    targets = ["\ub178\ub2e4\uc9c4", "\ub178\ub2e4\uc9c0"] # 노다진, 노다지
    addr_target = "735-1"
    
    results = {}
    for e in data:
        n = e.get('n', '')
        a = e.get('a', '')
        match = False
        for t in targets:
            if t in n: match = True
        if addr_target in a:
            match = True
            
        if match:
            k = f"{n}|{a}"
            if k not in results:
                results[k] = {"n": n, "a": a, "w": 0, "lat": e.get('lat'), "lng": e.get('lng')}
            results[k]["w"] += 1
            
    for s in results.values():
        en = s['n'].encode('ascii', 'xmlcharrefreplace').decode()
        ea = s['a'].encode('ascii', 'xmlcharrefreplace').decode()
        print(f"[{s['w']} wins] {en} | {ea} | {s['lat']}, {s['lng']}")

if __name__ == "__main__":
    search_nodaji()
