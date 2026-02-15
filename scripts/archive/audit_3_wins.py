import json
import re

def audit():
    # Load lotto_data.json
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        lotto_data = json.load(f)
        
    # Load index.html to find existing roadview presets
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Extract ROADVIEW_PRESETS content
    preset_match = re.search(r'const ROADVIEW_PRESETS = \[(.*?)\];', html_content, re.DOTALL)
    if not preset_match:
        print("Error: Could not find ROADVIEW_PRESETS in index.html")
        return
    
    preset_text = preset_match.group(1)
    
    # Extract names and addresses from presets using regex
    registered = set()
    for m in re.finditer(r'name:\s*"([^"]+)",\s*addr:\s*"([^"]+)"', preset_text):
        name = m.group(1).strip()
        addr = m.group(2).strip()
        # Use first 2 words (city + district) for more flexible matching
        addr_key = ' '.join(addr.split()[:2])
        registered.add((name, addr_key))
        
    # Manual exclusions for integrated or problematic shops
    EXCLUSIONS = {
        ("바다로또방", "경남 통영시"), # Integrated into 매물도복권점
        ("복권나라", "서울 성동구"), # Yongdap-dong relocation (integrated as 5-win shop)
        ("복권나라", "전남 여수시"), # Gyo-dong relocation/split (integrated as 5-win shop)
        ("복권명당", "경기 안성시"), # Seungdu-gil split (integrated as 4-win shop)
        ("복권명당", "대전 중구"),   # Mokjung-ro split (integrated as 4-win shop)
        ("복권방", "경기 수원시"),   # Ingye-ro split (integrated as 4-win shop)
        ("복권방", "서울 구로구"),   # Guro-dong (isClosed: true)
    }
        
    print(f"Total registered presets found in index.html: {len(registered)}")

    # Calculate win counts per shop from lotto_data
    shop_wins = {}
    for item in lotto_data:
        key = (item['n'].strip(), item['a'].strip())
        shop_wins[key] = shop_wins.get(key, 0) + 1
        
    missing_3 = []
    
    # Filter for physical shops with exactly 3 wins
    for (name, addr), wins in shop_wins.items():
        original_addr = addr # Keep track for coordinate lookup before addr_key modification
        if wins != 3:
            continue
            
        # Check exclusions
        addr_key = ' '.join(addr.split()[:2])
        if (name, addr_key) in EXCLUSIONS:
            continue
            
        # Check if it's an online site
        if 'dhlottery' in addr or '동행복권' in name or '인터넷' in name:
            continue
        
        # Use first 2 words for matching (more flexible)
        addr_key = ' '.join(addr.split()[:2])
        if (name, addr_key) in registered:
            continue
            
        target = {
            "name": name,
            "address": addr,
            "wins": wins,
            "lat": 0,
            "lng": 0
        }
        
        # Get coords from first occurrence (using original address for lookup in lotto_data)
        for item in lotto_data:
            if item['n'] == name and item['a'] == original_addr: # Use original_addr for lookup
                target['lat'] = item['lat']
                target['lng'] = item['lng']
                break
        
        missing_3.append(target)
            
    # Sort by name
    missing_3.sort(key=lambda x: x['name'])
    
    print(f"Missing 3 win shops: {len(missing_3)}")
    
    with open('admin_targets.json', 'w', encoding='utf-8') as f:
        json.dump(missing_3, f, ensure_ascii=False, indent=4)
        
    # Also save as .js for local file compatibility in admin_pov.html
    with open('admin_targets.js', 'w', encoding='utf-8') as f:
        f.write('window.allMissingShops = ' + json.dumps(missing_3, ensure_ascii=False, indent=4) + ';')
        
    print(f"Saved {len(missing_3)} targets to admin_targets.json and admin_targets.js")
    
    # Output first 10 for preview
    if missing_3:
        print("\n3회 당첨 매장 (처음 10개):")
        for s in missing_3[:10]:
            print(f"- {s['name']}: {s['address']}")

if __name__ == "__main__":
    audit()
