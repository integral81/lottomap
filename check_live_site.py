
import requests
import json
import os

def check_live_data():
    base_url = "http://www.k-inov.com/lottomap/"
    files_to_check = ["lotto_data.json", "data.json", "admin_targets.js", "index.html"]
    
    print(f"Checking live site: {base_url}")
    
    found_data = []
    
    for fname in files_to_check:
        url = base_url + fname
        try:
            print(f"Fetching {url}...")
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                print(f"  [SUCCESS] Found {fname} ({len(r.content)} bytes)")
                
                # If it's the main data file, analyze it
                if fname == "lotto_data.json":
                    try:
                        data = r.json()
                        print(f"  -> Parsed JSON with {len(data)} records.")
                        # Check for our missing friends
                        check_targets(data, "LIVE_SITE")
                        
                        # Save it locally for comparison
                        with open('lotto_data_live.json', 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=2, ensure_ascii=False)
                            
                    except:
                        print("  -> Failed to parse JSON")
            else:
                print(f"  [MISSING] {fname} (Status {r.status_code})")
        except Exception as e:
            print(f"  [ERROR] {e}")

def check_targets(data, source_name):
    targets = [
        "황금복권방", "복권명당", "가판점", "GS25", "목화휴게소", 
        "cu", "복권판매점", "뉴빅마트", "대박찬스", "로또휴게실"
    ]
    
    print(f"\n--- Checking Targets in {source_name} ---")
    for t in targets:
        found = False
        for item in data:
            if t in item.get('n', ''):
                # Check if it has POV
                pov = item.get('pov')
                if pov:
                    print(f"  [FOUND] {t} HAS POV! (ID: {pov.get('id') or pov.get('panoId')})")
                    found = True
                else:
                    print(f"  [PARTIAL] {t} found but NO POV.")
                    found = True
        if not found:
             pass # print(f"  [MISSING] {t}")

if __name__ == "__main__":
    check_live_data()
