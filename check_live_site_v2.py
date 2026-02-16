
import requests
import json

def check_live_site_v2():
    urls = [
        "http://www.k-inov.com/lottomap/lotto_data.json",
        "http://www.k-inov.com/lottomap/data.json",
        "http://www.k-inov.com/lotto_data.json",
        "http://www.k-inov.com/data.json"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    print("Checking Live Site Data...")
    
    for url in urls:
        try:
            print(f"Fetching {url}...")
            r = requests.get(url, headers=headers, timeout=10)
            print(f"  Status: {r.status_code}")
            if r.status_code == 200:
                print(f"  Content Type: {r.headers.get('Content-Type')}")
                print(f"  Length: {len(r.content)} bytes")
                try:
                    data = r.json()
                    print(f"  Success! Found {len(data)} items.")
                    
                    # Check Targets
                    targets = ["황금복권방", "복권명당", "로또휴게실"]
                    found_count = 0
                    for t in targets:
                        for item in data:
                            if t in item.get('n', ''):
                                if item.get('pov'):
                                    print(f"    [LIVE MATCH] {item['n']} has POV!")
                                    found_count += 1
                                    
                    # Save it
                    with open('lotto_data_live_v2.json', 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    return
                except:
                    print("  Failed to parse JSON")
        except Exception as e:
            print(f"  Error: {e}")

if __name__ == "__main__":
    check_live_site_v2()
