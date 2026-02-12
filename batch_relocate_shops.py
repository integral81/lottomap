
import json
import requests
import time

# Note: Using the provided Kakao API key correctly
KAKAO_API_KEY = "84b62e85ed3ec32fca558717eda26006"

def geocode_address(address):
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    params = {"query": address}
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['documents']:
                doc = data['documents'][0]
                return {
                    'lat': float(doc['y']),
                    'lng': float(doc['x']),
                    'address': doc['address_name'] # Standardized address
                }
    except Exception as e:
        print(f"Error geocoding {address}: {e}")
    return None

def extract_new_address(comment):
    # Extracts address from comments like "OOO로 이전 확인" or "OOO에서 영업 중"
    # Basic logic: Remove suffix phrases
    suffixes = ['로 이전', '에서 영업', '으로 이전', '로 주소', '에서 확인', '확인', '정정']
    addr = comment
    for s in suffixes:
        if s in addr:
            addr = addr.split(s)[0].strip()
    # Remove '현 ' prefix if exists
    if addr.startswith('현 '):
        addr = addr[2:]
    return addr.strip()

def main():
    try:
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Failed to load data: {e}")
        return

    updated_count = 0
    failed_list = []

    for idx, item in enumerate(data):
        if 'pending_relocation' in item:
            comment = item['pending_relocation']
            # Heuristic: try to get address from comment
            new_addr_candidate = extract_new_address(comment)

            if not new_addr_candidate:
                continue
            
            # IMPROVEMENT: If new address lacks region info (City/District), prepend from old address
            # Check if address starts with region (Simple check: length > 2 and no numbers in first word)
            first_word = new_addr_candidate.split()[0] if new_addr_candidate else ""
            old_addr_parts = item.get('a', '').split()
            
            # If new address looks like just a road name (e.g., "중앙대로 1520")
            # We prepend the first two parts of old address (e.g., "부산 사하구")
            if len(first_word) < 5 and not any(char.isdigit() for char in first_word):
                 # This is a weak check, but effective for "RoadName 123" vs "City District RoadName 123"
                 pass
            
            # Stronger check: If header doesn't match known administrative regions (Si/Do)
            # Or if it's too short. Let's just try merging if geocoding fails?
            # Better approach: Try raw first. If fail, Prepend Region.
            
            print(f"[{idx}] Processing: {item['n']}")
            print(f"   Target Addr: {new_addr_candidate}")
            
            geo_result = geocode_address(new_addr_candidate)
            
            # RETRY LOGIC with Region Prepending
            if not geo_result and len(old_addr_parts) >= 2:
                # Construct: "City District" + " " + "New Address"
                region_prefix = f"{old_addr_parts[0]} {old_addr_parts[1]}"
                refined_addr = f"{region_prefix} {new_addr_candidate}"
                print(f"   > Retrying with prefix: {refined_addr}")
                geo_result = geocode_address(refined_addr)
                if geo_result:
                    new_addr_candidate = geo_result['address'] # Updates to full address

            if geo_result:
                print(f"  > Success: {geo_result['address']} ({geo_result['lat']}, {geo_result['lng']})")
                item['a'] = new_addr_candidate  # Update address text
                item['lat'] = geo_result['lat']
                item['lng'] = geo_result['lng']
                
                # Add a flag to indicate this was automatically moved
                item['relocated_verified'] = True 
                
                # Keep the comment but maybe rename key or remove it?
                # For now, let's keep pending_relocation as a record, or remove it to clean up?
                # User asked to "execute", implies finishing the move.
                del item['pending_relocation'] 
                
                updated_count += 1
            else:
                print(f"  > Failed to geocode: {new_addr_candidate}")
                failed_list.append({'name': item['n'], 'addr': new_addr_candidate})
            
            time.sleep(0.1) # Rate limit

    with open('lotto_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n--- Batch Relocation Complete ---")
    print(f"Successfully moved: {updated_count} entries")
    print(f"Failed to geocode: {len(failed_list)} entries")
    if failed_list:
        print("Failures:", json.dumps(failed_list, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
