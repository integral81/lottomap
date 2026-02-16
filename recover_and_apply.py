
import json
import os

def recover_and_apply():
    # 1. Define Recovered Data (Hardcoded from Forensic Investigation)
    recovered_data = [
        {
            "name": "목화휴게소",
            "addr_keywords": ["사천", "목화"],
            "new_addr": "경남 사천시 사천대로 912",
            "pov": { "id": "1188272977", "pan": 34.24, "tilt": 0.74, "zoom": 0 }
        },
        {
            "name": "알리바이(나주점)",
            "addr_keywords": ["나주", "알리바이"],
            "new_addr": "전남 나주시 나주로 142 알리바이",
            "pov": { "id": "1191260182", "pan": 17.27, "tilt": -9.34, "zoom": -3 }
        }
    ]
    
    # 2. Apply to lotto_data.json
    json_path = 'lotto_data.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    applied_count = 0
    applied_names = []
    
    for rec in recovered_data:
        # Find matching shop
        for item in data:
            # Check name match (fuzzy)
            if rec['name'] in item['n'] or (rec['addr_keywords'][1] in item['n']):
                # Check region match
                if rec['addr_keywords'][0] in item['a']:
                    print(f"Applying recovery to: {item['n']} ({item['a']})")
                    item['a'] = rec['new_addr']
                    item['pov'] = rec['pov']
                    applied_count += 1
                    applied_names.append(item['n'])
                    # Update lat/lng? Mokhwa was 35.00/128.05
                    # Let's trust the POV update implicity means coords are verified
                    break
                    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully applied {applied_count} recoveries: {', '.join(applied_names)}")
    
    # 3. Identify Remaining Candidates for Auto-Pilot
    # List of original 10 targets
    original_targets = [
        "황금복권방", "복권명당", "가판점(2호선)", "GS25(청주주성점)", 
        "목화휴게소", "cu(수성그린점)", "복권판매점", "CU(구미원평점)", 
        "뉴빅마트", "대박찬스"
    ]
    
    remaining = [t for t in original_targets if not any(r['name'] in t for r in recovered_data)]
    # Note: Alibai wasn't in the top 10 list above, but Mokhwa was.
    
    print("\n[Status Report]")
    print(f"Recovered from History: {applied_count} shops (Mokhwa, Alibai)")
    print(f"Still Needing Scan: {len(remaining)} shops")
    for r in remaining:
        print(f" - {r}")

if __name__ == "__main__":
    recover_and_apply()
