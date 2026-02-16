
import json
import requests

def find_gapan_and_check_api():
    # 1. Search Local Data
    print("--- Searching '가판점' in lotto_data.json ---")
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    candidates = []
    for item in data:
        if "가판점" in item['n']:
            # Check for Sindorim clues in address or name
            if "신도림" in item['a'] or "구로" in item['a'] or "2호선" in item['n']:
                print(f"Candidate: {item['n']} | Addr: {item['a']} | ID: {item.get('pov', {}).get('id')}")
                candidates.append(item)
                
    if not candidates:
        print("No obvious 'Sindorim Gapanjeom' found in local data. Listing first 5 'Gapanjeom':")
        count = 0
        for item in data:
            if "가판점" in item['n']:
                print(f"  {item['n']} ({item['a']})")
                count += 1
                if count >= 5: break

    # 2. Check Internal API
    place_id = "26506631"
    url = f"https://place.map.kakao.com/main/v/{place_id}"
    print(f"\n--- Fetching Internal API: {url} ---")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": f"https://place.map.kakao.com/{place_id}"
    }
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            basic = data.get('basicInfo', {})
            rv = basic.get('roadview', {})
            
            print(f"Name: {basic.get('kakaotalkname') or basic.get('name')}")
            print(f"Addr: {basic.get('address', {}).get('newaddr', {}).get('newaddrfull')} | {basic.get('address', {}).get('region', {}).get('fullname')}")
            
            if rv:
                print(f"FOUND Roadview! ID: {rv.get('panoid')}")
                # Save it
                save_gapan_update(rv.get('panoid'), basic.get('wpointx'), basic.get('wpointy'))
            else:
                print("No Roadview in API.")
                # But maybe we have coords?
                print(f"Coords: {basic.get('wpointx')}, {basic.get('wpointy')}")
                if basic.get('wpointx'):
                    save_gapan_update(None, basic.get('wpointx'), basic.get('wpointy'))
        else:
            print(f"API Failed: {r.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

def save_gapan_update(pid, wx, wy):
    # WCONGNAMUL to WGS84?
    # No, let's just use the PanoID if found.
    # If only coords, we need to convert or finding PanoID via JS in verification HTML.
    
    # Let's save to a temp file for next step
    infos = {"pid": pid, "wx": wx, "wy": wy}
    with open('gapan_info.json', 'w', encoding='utf-8') as f:
        json.dump(infos, f)
    print("Saved gapan_info.json")

if __name__ == "__main__":
    find_gapan_and_check_api()
