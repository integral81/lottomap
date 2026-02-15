
import re

def audit_high_wins():
    try:
        with open('admin_pov.html', 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find all wins
        # Pattern: "wins": N,
        wins = re.findall(r'"wins":\s*(\d+)', content)
        wins = [int(w) for w in wins]
        
        high_wins = [w for w in wins if w >= 5]
        print(f"Total remaining items: {len(wins)}")
        print(f"Items with 5+ wins: {len(high_wins)}")
        
        if len(high_wins) > 0:
            print("Note: There are still shops with 5+ wins unregistered.")
        else:
            print("All shops with 5+ wins have been registered!")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    audit_high_wins()
