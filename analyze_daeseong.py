
import json

def check_daeseong():
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    results = [d for d in data if '대성기획' in d['n'] and '용인' in d['a']]
    print(f"Found {len(results)} entries for '대성기획' in Yongin:")
    rounds = sorted([d['r'] for d in results])
    print(f"Rounds: {rounds}")
    for d in results:
        print(f"Round {d['r']}: {d['a']}")

    # Check if there are other suspicious names in the same address
    # Address is usually "경기 용인시 기흥구 구성로 75-1" or similar
    addresses = set(d['a'] for d in results)
    print(f"\nAddresses found: {addresses}")
    
    # Check for other shops at the same building/address
    print("\nChecking for other shops at these addresses:")
    for addr in addresses:
        # Extract base address like "구성로 75-1"
        if "구성로" in addr:
            base = "구성로 75-1"
            others = [d for d in data if base in d.get('a', '') and '대성기획' not in d['n']]
            if others:
                print(f"Other shops found at {base}:")
                for o in others:
                    print(f"{o['n']} | {o['a']} | Round {o['r']}")
            else:
                print(f"No other shops found at {base}")

check_daeseong()
