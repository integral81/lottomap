
import json
import sys

# Windows console encoding fix
sys.stdout.reconfigure(encoding='utf-8')

def find_missing():
    with open('admin_targets.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('const adminTargets = [', '').replace('];', '')
    lines = content.strip().split(',\n')
    
    missing_count = 0
    print("Next 5 shops to process:")
    for line in lines:
        line = line.strip()
        if not line: continue
        if line.endswith(','): line = line[:-1]
        
        try:
            obj = json.loads(line)
            if 'pov' not in obj:
                print(f"- {obj['name']} ({obj['address']}) - {obj['wins']} wins")
                missing_count += 1
                if missing_count >= 5:
                    break
        except:
            continue

if __name__ == "__main__":
    find_missing()
