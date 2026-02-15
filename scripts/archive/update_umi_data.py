import pandas as pd
import json

def update_umi_super():
    json_path = 'lotto_data.json'
    excel_path = 'lotto_results_kinov.xlsx'
    
    target_name = "우미슈퍼"
    new_addr = "광주 서구 풍암동 1132 우미아파트상가 118동 101호"
    target_lat = 35.126734
    target_lng = 126.881128
    pov_data = {
        "id": "1198285521",
        "pan": 158.3,
        "tilt": 5.4,
        "zoom": 0
    }

    # 1. Update lotto_data.json
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        count_json = 0
        for item in data:
            if "우미슈퍼" in item.get('n', '') and "광주" in item.get('a', ''):
                item['n'] = target_name
                item['a'] = new_addr
                item['lat'] = target_lat
                item['lng'] = target_lng
                item['pov'] = pov_data
                count_json += 1
                
        if count_json > 0:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Updated {count_json} records in {json_path}")

        # 2. Update Excel
        df = pd.read_excel(excel_path)
        mask = (df['상호명'].str.contains('우미슈퍼', na=False)) & (df['소재지'].str.contains('광주', na=False))
        df.loc[mask, '소재지'] = new_addr
        df.to_excel(excel_path, index=False)
        print(f"Updated {mask.sum()} records in {excel_path}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_umi_super()
