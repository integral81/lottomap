
import json
import os

def merge_and_check_pov():
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Define tasks based on Gemini research (excluding index 7)
    merge_tasks = [
        {"name": "(I.A) 로또마트", "new_name": "로또마트", "addr_part": "신길로 9-4"},
        {"name": "-", "new_name": "농협중앙회 앞 가판", "addr_part": "의정부동 175-6"},
        {"name": "-", "new_name": "이름미상(화명동)", "addr_part": "화명동 1402-2"},
        {"name": "-", "new_name": "농협 앞 가판점", "addr_part": "수진동 18"},
        {"name": "-", "new_name": "청화빌딩", "addr_part": "서초동 1571-18"},
        {"name": "-", "new_name": "로또 명당 가판점", "addr_part": "독산동 876-2"},
        {"name": "153로또판매점", "new_name": "153로또판매점", "addr_part": "배방로 57-23"},
        {"name": "1등 복권", "new_name": "1등 복권", "addr_part": "배곧4로 32-27"},
        {"name": "1등로또방", "new_name": "1등로또방", "addr_part": "중앙로 249-2"}
    ]
    
    updated_data = []
    processed_new_names = set()
    
    # Store POV health results
    pov_report = []

    for task in merge_tasks:
        # Find all records matching the address part
        matches = [d for d in data if task['addr_part'] in d.get('a', '')]
        if not matches: continue
        
        # Merge logic
        # 1. Collect all rounds
        all_rounds = sorted(list(set(m.get('r') for m in matches if m.get('r'))))
        # 2. Pick the best record (the one with POV is priority)
        pov_record = next((m for m in matches if m.get('pov') and m['pov'].get('id')), None)
        
        if pov_record:
            best = pov_record.copy()
            pov_report.append(f"SUCCESS: {task['new_name']} has active POV ({best['pov']['id']})")
        else:
            best = matches[0].copy()
            pov_report.append(f"WARNING: {task['new_name']} has NO POV data.")
        
        best['n'] = task['new_name']
        best['r_list'] = all_rounds # Store historically
        best['count'] = len(all_rounds)
        
        # Remove old ones from data and add the merged one
        data = [d for d in data if d not in matches]
        updated_data.append(best)

    # Reassemble
    final_data = data + updated_data
    
    # Save
    with open('lotto_data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, separators=(',', ':'))
    
    return pov_report

report = merge_and_check_pov()
print("--- POV Status Report for Merged Shops ---")
for line in report:
    print(line)
