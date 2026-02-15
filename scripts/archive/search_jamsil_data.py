
import json

def search_jamsil():
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    targets = ["\uc7a0\uc2e4\ub9e4\uc810"] # 잠실매점
    addr_target = "269"
    
    results = {}
    for e in data:
        n = e.get('n', '')
        a = e.get('a', '')
        match = False
        for t in targets:
            if t in n: match = True
        if addr_target in a and "\uc1a1\ud30c" in a: # 송파
            match = True
            
        if match:
            k = f"{n}|{a}"
            if k not in results:
                results[k] = {"n": n, "a": a, "w": 0, "lat": e.get('lat'), "lng": e.get('lng'), "pov": 'pov' in e}
            results[k]["w"] += 1
            
    for s in results.values():
        en = s['n'].encode('ascii', 'xmlcharrefreplace').decode()
        ea = s['a'].encode('ascii', 'xmlcharrefreplace').decode()
        print(f"[{s['w']} wins] POV:{s['pov']} | {en} | {ea} | {s['lat']}, {s['lng']}")

if __name__ == "__main__":
    search_jamsil()
