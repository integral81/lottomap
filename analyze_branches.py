
import subprocess
import json

def analyze_branches():
    branches = [
        "feature/roadview-260210-2단계", 
        "backup-260210-1단계",
        "main" 
    ]
    
    # Also check current local file
    try:
        with open('lotto_data.json', 'r', encoding='utf-8') as f:
            local = json.load(f)
            count_local = sum(1 for i in local if i.get('pov'))
            print(f"LOCAL FILE: {len(local)} items, {count_local} POVs")
    except:
        print("Local file error")

    for br in branches:
        cmd = ["git", "show", f"{br}:lotto_data.json"]
        print(f"\nAnalyzing branch: {br}")
        try:
            raw = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
            
            # Decode
            try: content = raw.decode('utf-8')
            except: content = raw.decode('utf-16')
            content = content.replace('\ufeff', '')
            
            data = json.loads(content)
            
            # Count POVs
            pov_count = sum(1 for i in data if i.get('pov'))
            print(f"  -> Items: {len(data)}")
            print(f"  -> POVs: {pov_count}")
            
            # Check for "Golden Lottery" specifically
            gold = next((i for i in data if "황금복권방" in i['n']), None)
            if gold:
                print(f"  -> Golden Lottery: Found (POV: {gold.get('pov')})")
            else:
                print(f"  -> Golden Lottery: Not Found")
                
        except Exception as e:
            print(f"  -> Error: {e}")

if __name__ == "__main__":
    analyze_branches()
