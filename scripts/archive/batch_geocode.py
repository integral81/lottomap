
import json
import requests
import time

API_KEY = "84b62e85ed3ec32fca558717eda26006"

def geocode_addr(address):
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {API_KEY}"}
    params = {"query": address}
    try:
        r = requests.get(url, headers=headers, params=params, timeout=5)
        if r.status_code == 200:
            data = r.json()
            if data['documents']:
                doc = data['documents'][0]
                return float(doc['y']), float(doc['x']), "AddressAPI"
        return None, None, None
    except Exception:
        return None, None, None

def geocode_keyword(keyword, addr_hint=""):
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {API_KEY}"}
    query = f"{addr_hint} {keyword}".strip()
    params = {"query": query}
    try:
        r = requests.get(url, headers=headers, params=params, timeout=5)
        if r.status_code == 200:
            data = r.json()
            if data['documents']:
                doc = data['documents'][0]
                return float(doc['y']), float(doc['x']), "KeywordAPI"
        return None, None, None
    except Exception:
        return None, None, None

def process_geocoding():
    print("--- [EXECUTION] Batch Geocoding ---")
    try:
        with open('addrs_to_geocode.json', 'r', encoding='utf-8') as f:
            unique_addrs = json.load(f)
            
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            lotto_data = json.load(f)
            
        coord_map = {}
        failed_addrs = []
        
        # Internet Winner Special Handling
        DONGHAENG_ADDR = "서울특별시 서초구 남부순환로 2423"
        DONGHAENG_COORDS = (37.4815, 127.0145) # Approx for Seocho-gu HQ
        
        for addr in unique_addrs:
            if "dhlottery.co.kr" in addr or "인터넷" in addr:
                print(f"Mapping Internet Winner: {addr} -> HQ")
                coord_map[addr] = DONGHAENG_COORDS
                continue
            
            print(f"Geocoding: {addr}")
            lat, lng, method = geocode_addr(addr)
            
            if not lat:
                # Try short address
                short_addr = ' '.join(addr.split()[:4])
                print(f"  Retrying short: {short_addr}")
                lat, lng, method = geocode_addr(short_addr)
                
            if not lat:
                # Try keyword search (last part of address often is building name)
                keyword = addr.split()[-1]
                hint = ' '.join(addr.split()[:2])
                print(f"  Retrying keyword: {hint} {keyword}")
                lat, lng, method = geocode_keyword(keyword, hint)
                
            if lat:
                print(f"  Success ({method}): {lat}, {lng}")
                coord_map[addr] = (lat, lng)
            else:
                print(f"  Failed.")
                failed_addrs.append(addr)
            
            time.sleep(0.05)
            
        # Update lotto_data
        updated_count = 0
        for item in lotto_data:
            a = item.get('a')
            if not item.get('lat') and a in coord_map:
                item['lat'], item['lng'] = coord_map[a]
                updated_count += 1
                
        if updated_count > 0:
            with open('lotto_data.json', 'w', encoding='utf-8') as f:
                json.dump(lotto_data, f, indent=2, ensure_ascii=False)
            print(f"\nApplied coordinates to {updated_count} entries.")
            
        if failed_addrs:
            with open('failed_geocoding.json', 'w', encoding='utf-8') as f:
                json.dump(failed_addrs, f, indent=2, ensure_ascii=False)
            print(f"Saved {len(failed_addrs)} failed addresses to failed_geocoding.json")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    process_geocoding()
