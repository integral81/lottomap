
import json

def fix_gunpo_haengun():
    file_path = 'lotto_data.json'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    # Daeyami Shop Info
    daeyami_addr = "경기 군포시 대야1로 3 1동"
    daeyami_lat = 37.323635
    daeyami_lng = 126.912624
    daeyami_rounds = [238, 309, 418, 774, 1008, 1029, 1040, 1101, 1102, 1104, 1129, 1147]

    # Sanbon Shop Info
    sanbon_addr = "경기 군포시 산본동 1055 108호"
    sanbon_lat = 37.3621434913221
    sanbon_lng = 126.938887467364
    sanbon_rounds = [441, 444, 544, 579]
    
    daeyami_count = 0
    sanbon_count = 0
    
    for item in data:
        if "행운복권" in item['n'] and "군포" in item['a']:
            r = item.get('r')
            if r in daeyami_rounds:
                item['a'] = daeyami_addr
                item['lat'] = daeyami_lat
                item['lng'] = daeyami_lng
                daeyami_count += 1
            elif r in sanbon_rounds:
                item['a'] = sanbon_addr
                item['lat'] = sanbon_lat
                item['lng'] = sanbon_lng
                sanbon_count += 1

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully fixed Gunpo Haengun Lotto data.")
    print(f"Daeyami: {daeyami_count} entries at {daeyami_addr}")
    print(f"Sanbon: {sanbon_count} entries at {sanbon_addr}")

if __name__ == "__main__":
    fix_gunpo_haengun()
