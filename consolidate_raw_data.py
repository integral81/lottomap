import json
import pandas as pd
import os

# Paths
json_path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json"
xlsx_path = r"c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_results_kinov.xlsx"

# Mapping Definitions: (Search Name, Search Addr Fragment) -> (New Name, New Addr)
CONSOLIDATION_MAPPING = [
    {
        "search_name": "바다로또방",
        "search_addr": "서호동 177-358",
        "new_name": "매물도복권점",
        "new_addr": "경남 통영시 통영해안로 225-1 (서호동 177-336)"
    },
    {
        "search_name": "바다로또방",
        "search_addr": "통영해안로 229-2",
        "new_name": "매물도복권점",
        "new_addr": "경남 통영시 통영해안로 225-1 (서호동 177-336)"
    },
    {
        "search_name": "보람복권방",
        "search_addr": "삼산동 1567-6",
        "new_name": "보람복권방",
        "new_addr": "울산 남구 화합로194번길 18-1 (삼산동 1567-6 우리들마트 내)"
    },
    {
        "search_name": "베스토아(용전2호)",
        "search_addr": "용전동 63-3",
        "new_name": "베스토아(용전2호)",
        "new_addr": "대전 동구 동서대로 1689 복합터미널서관1층59호 (용전동 63-3)"
    },
    {
        "search_name": "복권나라",
        "search_addr": "용답동 14-1",
        "new_name": "복권나라",
        "new_addr": "서울 성동구 용답중앙15길 12-1 (용답동 14-30)"
    },
    {
        "search_name": "복권나라",
        "search_addr": "교동 448",
        "new_name": "복권나라",
        "new_addr": "전남 여수시 중앙로 62 (교동 448-2)"
    },
    {
        "search_name": "복권나라",
        "search_addr": "중앙로 62",
        "new_name": "복권나라",
        "new_addr": "전남 여수시 중앙로 62 (교동 448-2)"
    },
    {
        "search_name": "복권명당",
        "search_addr": "승두리 60-129",
        "new_name": "복권명당",
        "new_addr": "경기 안성시 공도읍 승두길 62 (승두리 60-129)"
    },
    {
        "search_name": "복권명당",
        "search_addr": "중촌동 21-18",
        "new_name": "복권명당",
        "new_addr": "대전 중구 목중로 47 (중촌동 21-18)"
    },
    {
        "search_name": "복권방",
        "search_addr": "인계동 1037-2",
        "new_name": "복권방",
        "new_addr": "경기 수원시 팔달구 인계로 213 (인계동 1037-2)"
    },
    {
        "search_name": "복권방",
        "search_addr": "신장동 427-169",
        "new_name": "복권방",
        "new_addr": "경기 하남시 신장로 122 (신장동 427-169)"
    },
    {
        "search_name": "복돼지복권방",
        "search_addr": "모현동1가 865",
        "new_name": "복돼지복권방",
        "new_addr": "전북 익산시 선화로1길 4 배산시티프라자 1층 107호"
    },
    {
        "search_name": "복권방",
        "search_addr": "배산시티프라자 배산시티프라자",
        "new_name": "복돼지복권방",
        "new_addr": "전북 익산시 선화로1길 4 배산시티프라자 1층 107호"
    },
    {
        "search_name": "부강 돈벼락",
        "search_addr": "물금로 41",
        "new_name": "부강 돈벼락",
        "new_addr": "경남 양산시 물금로 41 (물금리 800-5, 양우내안애5차 상가 108호)"
    }
]

def consolidate_json():
    print(f"Opening {json_path}...")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    modified_count = 0
    for entry in data:
        name = entry.get('n', '')
        addr = entry.get('a', '')
        
        for mapping in CONSOLIDATION_MAPPING:
            if mapping['search_name'] in name and mapping['search_addr'] in addr:
                entry['n'] = mapping['new_name']
                entry['a'] = mapping['new_addr']
                modified_count += 1
                break
                
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"JSON Consolidation Complete. Total records modified: {modified_count}")

def consolidate_xlsx():
    print(f"Opening {xlsx_path}...")
    try:
        df = pd.read_excel(xlsx_path)
    except:
        df = pd.read_excel(xlsx_path, engine='openpyxl')
        
    modified_count = 0
    
    # Based on inspection:
    # Index 2: Name
    # Index 4: Address
    name_col_idx = 2
    addr_col_idx = 4
    
    name_col = df.columns[name_col_idx]
    addr_col = df.columns[addr_col_idx]

    print(f"Using columns - Name: {name_col} (idx {name_col_idx}), Address: {addr_col} (idx {addr_col_idx})")

    for idx, row in df.iterrows():
        name = str(row[name_col])
        addr = str(row[addr_col])
        
        for mapping in CONSOLIDATION_MAPPING:
            if mapping['search_name'] in name and mapping['search_addr'] in addr:
                df.iloc[idx, name_col_idx] = mapping['new_name']
                df.iloc[idx, addr_col_idx] = mapping['new_addr']
                modified_count += 1
                break
                
    df.to_excel(xlsx_path, index=False)
    print(f"XLSX Consolidation Complete. Total records modified: {modified_count}")

if __name__ == "__main__":
    consolidate_json()
    consolidate_xlsx()
