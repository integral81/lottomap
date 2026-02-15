
import re

def audit_high_wins():
    try:
        with open('admin_pov.html', 'r', encoding='utf-8') as f:
            content = f.read()

        blocks = content.split('},')
        results = []
        
        for block in blocks:
            if '"wins":' in block:
                try:
                    wins_match = re.search(r'"wins":\s*(\d+)', block)
                    if wins_match:
                        wins = int(wins_match.group(1))
                        if wins >= 5:
                            name_match = re.search(r'"name":\s*"([^"]+)"', block)
                            addr_match = re.search(r'"address":\s*"([^"]+)"', block)
                            if name_match and addr_match:
                                name = name_match.group(1)
                                addr = addr_match.group(1)
                                results.append(f"- {name} ({addr}): {wins}회")
                except:
                    pass

        with open('remaining_5_wins.txt', 'w', encoding='utf-8') as f:
            f.write(f"Total: {len(results)}\n")
            for r in results:
                f.write(r + "\n")
                
    except Exception as e:
        with open('remaining_5_wins.txt', 'w', encoding='utf-8') as f:
            f.write(f"Error: {e}")

if __name__ == "__main__":
    audit_high_wins()
