import json
import pandas as pd
import requests
import os
import re

# --- CONFIGURATION ---
JSON_FILE = "lotto_data.json"
EXCEL_FILE = "temp_data.xlsx"
CACHE_FILE = "geocoded_cache_healthy.xlsx"
KAKAO_API_KEY = os.environ.get("KAKAO_REST_API_KEY")

def normalize_address(addr):
    if not isinstance(addr, str): return addr
    addr = addr.strip()
    addr = re.sub(r'(\d+)번지', r'\1', addr)
    addr = re.sub(r'(\d+-\d+)번지', r'\1', addr)
    addr = re.sub(r'\s(\d+)층$', '', addr)
    addr = re.sub(r'\s지하\s*(\d*)층?$', '', addr)
    addr = addr.rstrip('., ')
    if addr.endswith('번지'): addr = addr[:-2].strip()
    return addr

def geocode(address, api_key, cache):
    if address in cache:
        return cache[address]
    
    if not api_key:
        return None, None
    
    if "동행복권" in address:
        return None, None

    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {api_key}"}
    params = {"query": address}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        data = response.json()
        if data.get('documents'):
            pos = data['documents'][0]
            lat, lng = float(pos['y']), float(pos['x'])
            cache[address] = (lat, lng)
            return lat, lng
    except Exception as e:
        print(f"Geocoding error for {address}: {e}")
    
    return None, None

def main():
    # WINNERS DATA FOR ROUND 1210
    round_num = 1210
    
    winners = []
    
    # Auto (13 records)
    # Internet (1)
    winners.append({'n': '인터넷 복권판매사이트', 'm': '자동', 'a': '동행복권(dhlottery.co.kr)'})
    
    # Physical (12)
    auto_stores = [
        ("행운식품", "서울 관악구 신원로3길 21"),
        ("용꿈돼지꿈", "서울 마포구 마포대로 112-5"),
        ("부일카서비스", "부산 동구 자성로133번길 35"),
        ("베스토아(용전2호)", "대전 동구 동서대로 1689"),
        ("로또명당 일산점", "경기 고양시 일산서구 일중로15번길 86"),
        ("신의 축복", "경기 남양주시 사릉로34번길 24"),
        ("공원슈퍼", "경기 수원시 장안구 팔달로 255"),
        ("탄현대박로또복권", "경기 파주시 방촌로 661"),
        ("천하명당복권방", "충남 홍성군 조양로 180"),
        ("대광복권판매점", "전남 강진군 중앙로 83"),
        ("드림복권", "경남 김해시 장유로 288"),
        ("로또플렉스 시티세븐점", "경남 창원시 성산구 원이대로 320")
    ]
    for n, a in auto_stores:
        winners.append({'n': n, 'm': '자동', 'a': normalize_address(a)})

    # Semi-Auto (1 record)
    winners.append({'n': '로또명당반', 'm': '반자동', 'a': normalize_address('경기 남양주시 금강로 1557')})

    # Manual (10 records)
    # Internet (2)
    winners.append({'n': '인터넷 복권판매사이트', 'm': '수동', 'a': '동행복권(dhlottery.co.kr)'})
    winners.append({'n': '인터넷 복권판매사이트', 'm': '수동', 'a': '동행복권(dhlottery.co.kr)'})
    
    # Physical (8 records from 7 locations - Danielsa has 2)
    manual_stores = [
        ("소망복권", "서울 구로구 경인로35길 83"),
        ("씨스페이스 응암역점", "서울 은평구 연서로 9"),
        ("미라클", "인천 서구 심곡로49번길 2"),
        ("리맥스복권방", "경기 구리시 경춘로 239"),
        ("다니엘사", "경기 안산시 단원구 원선1로 38"), # 1st
        ("다니엘사", "경기 안산시 단원구 원선1로 38"), # 2nd
        ("행복충전소", "경기 평택시 탄현로 332-2"),
        ("왕대박복권방", "경북 문경시 중앙로 156")
    ]
    for n, a in manual_stores:
        winners.append({'n': n, 'm': '수동', 'a': normalize_address(a)})

    print(f"Prepared {len(winners)} records for round {round_num}.")
    
    # Add round number
    for w in winners:
        w['r'] = round_num

    # 3. Load Cache
    cache = {}
    if os.path.exists(CACHE_FILE):
        try:
            cache_df = pd.read_excel(CACHE_FILE)
            cache = {row['a']: (row['lat'], row['lng']) for _, row in cache_df.iterrows()}
        except: pass

    # 4. Geocode
    final_records = []
    for rec in winners:
        lat, lng = geocode(rec['a'], KAKAO_API_KEY, cache)
        if lat and lng:
            rec['lat'] = lat
            rec['lng'] = lng
        final_records.append(rec) # Append even if no lat/lng (e.g. Internet)

    # 5. Merge and Save
    # JSON
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            all_data = json.load(f)
    else:
        all_data = []
        
    # Check if 1210 already exists to avoid dupes
    all_data = [d for d in all_data if d['r'] != round_num]
    
    # Add new
    all_data.extend(final_records)
    all_data.sort(key=lambda x: x['r'], reverse=True)
    
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    # Excel
    if os.path.exists(EXCEL_FILE):
        df_old = pd.read_excel(EXCEL_FILE)
        # Remove 1210 if exists
        df_old = df_old[df_old['회차'] != round_num]
    else:
        df_old = pd.DataFrame()
        
    new_df_data = []
    for r in final_records:
        new_df_data.append([r['r'], None, r['n'], r['m'], r['a']])
    
    columns = ['회차', '순번', '상호명', '구분', '소재지'] # Adjust if needed matching temp_data
    if not df_old.empty:
        columns = df_old.columns[:5]
        
    df_new = pd.DataFrame(new_df_data, columns=columns)
    
    if not df_old.empty:
        df_combined = pd.concat([df_new, df_old], ignore_index=True)
    else:
        df_combined = df_new
        
    df_combined.to_excel(EXCEL_FILE, index=False)

    # Update Cache
    if cache:
        new_cache_df = pd.DataFrame([{'a': k, 'lat': v[0], 'lng': v[1]} for k, v in cache.items()])
        new_cache_df.to_excel(CACHE_FILE, index=False)

    print(f"Successfully manually added {len(final_records)} records for round {round_num}.")

if __name__ == "__main__":
    main()
