
import requests
import json
import time

KAKAO_API_KEY = "84b62e85ed3ec32fca558717eda26006"

def geocode_shops():
    with open('shops_1210.json', 'r', encoding='utf-8') as f:
        shops = json.load(f)
        
    results = []
    
    # Danielsa appears twice (2 winners)
    # So we will add it twice to the results later if needed, but for now let's just get coords.
    
    for shop in shops:
        query = f"{shop['region']} {shop['n']}"
        print(f"Searching: {query}")
        
        url = "https://dapi.kakao.com/v2/local/search/keyword.json"
        headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
        params = {"query": query}
        
        try:
            r = requests.get(url, headers=headers, params=params)
            data = r.json()
            
            if data['documents']:
                place = data['documents'][0]
                print(f"  Found: {place['place_name']} ({place['address_name']})")
                
                winner = {
                    "r": 1210,
                    "n": shop['n'], # Use original name or place['place_name']? Original is better for consistency if web search was accurate.
                    "a": place['address_name'], # Use Kakao address
                    "m": "자동", # Default to Auto for now
                    "lat": float(place['y']),
                    "lng": float(place['x'])
                }
                results.append(winner)
                
                # Special handling for Danielsa (2 hits)
                if "다니엘사" in shop['n']:
                    print("  Adding Duplicate for Danielsa")
                    winner2 = winner.copy()
                    winner2['m'] = "수동" # Often duplicates are manual
                    results.append(winner2)
            else:
                print("  NOT FOUND")
                # Fallback: try searching just name if region search failed?
                # Or just add without coords (will be hidden on map but present in data)
                winner = {
                    "r": 1210,
                    "n": shop['n'],
                    "a": shop['region'] + " (주소 미확인)",
                    "m": "자동",
                    "lat": 0.0,
                    "lng": 0.0
                }
                results.append(winner)

        except Exception as e:
            print(f"  Error: {e}")
            
        time.sleep(0.5)

    # Add Online winners (3)
    for _ in range(3):
        results.append({
            "r": 1210,
            "n": "인터넷 복권판매사이트",
            "a": "동행복권(dhlottery.co.kr)",
            "m": "자동", # Online is usually auto or manual?
            "lat": 0.0,
            "lng": 0.0
        })

    with open('round_1210_geocoded.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        
    print(f"Saved {len(results)} winners to round_1210_geocoded.json")

if __name__ == "__main__":
    geocode_shops()
