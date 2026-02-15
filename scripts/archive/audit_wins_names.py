
import re

def audit_high_wins():
    try:
        with open('admin_pov.html', 'r', encoding='utf-8') as f:
            content = f.read()

        # Simple regex to find blocks
        # We look for "wins": N where N >= 5
        # And capture name/address around it
        # Since the file is formatted, we can iterate line by line or use block regex
        
        # Let's try splitting by object start "{"
        blocks = content.split('{')
        
        results = []
        for block in blocks:
            if '"wins":' not in block: continue
            
            wins_match = re.search(r'"wins":\s*(\d+)', block)
            if not wins_match: continue
            
            wins = int(wins_match.group(1))
            if wins < 5: continue
            
            name_match = re.search(r'"name":\s*"([^"]+)"', block)
            addr_match = re.search(r'"address":\s*"([^"]+)"', block)
            
            if name_match:
                name = name_match.group(1)
                addr = addr_match.group(1) if addr_match else "?"
                results.append(f"- {name} ({addr}): {wins}회")

        print(f"Found {len(results)} shops with 5+ wins:")
        for r in results:
            print(r)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    audit_high_wins()
