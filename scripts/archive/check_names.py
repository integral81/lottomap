
import re

def check_names():
    try:
        with open('admin_pov.html', 'r', encoding='utf-8') as f:
            content = f.read()
            
        names = ["목화휴게소", "복권나라", "오케이상사", "잠실매점"]
        for n in names:
            if n in content:
                print(f"Found: {n}")
            else:
                print(f"Not Found: {n}")
                
        # Find 8 wins
        # Need to handle potential whitespace/newlines
        # Using regex to find wins: 8 and look behind for name
        
        # Split by blocks again for safety
        blocks = content.split('},')
        for block in blocks:
            if '"wins": 8' in block or '"wins": 8,' in block:
                 name_m = re.search(r'"name": "([^"]+)"', block)
                 if name_m:
                     print(f"8 wins shop: {name_m.group(1)}")

            if '"wins": 7' in block:
                 name_m = re.search(r'"name": "([^"]+)"', block)
                 if name_m:
                     print(f"7 wins shop: {name_m.group(1)}")
                     
            if '"wins": 6' in block:
                 name_m = re.search(r'"name": "([^"]+)"', block)
                 if name_m:
                     print(f"6 wins shop: {name_m.group(1)}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_names()
