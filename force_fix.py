import json
import os

path_json = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.json'
path_js = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\lotto_data.js'

def fix():
    if not os.path.exists(path_json):
        print(f"Error: {path_json} not found")
        return

    with open(path_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated_count = 0
    for s in data:
        if s.get('n') == '넝쿨째(블루25 중앙점)':
            s['closed'] = True
            updated_count += 1
    
    if updated_count > 0:
        with open(path_json, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Updated {updated_count} records in {path_json}")
        
        with open(path_js, 'w', encoding='utf-8') as f:
            f.write('const lottoData = ' + json.dumps(data, ensure_ascii=False) + ';')
        print(f"Regenerated {path_js}")
    else:
        print("No matches found for '넝쿨째(블루25 중앙점)'")

if __name__ == "__main__":
    fix()
