
import json

def analyze_wangdaebak():
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 1. Search for "왕대박복권" in Incheon Bupyeong
    results = [d for d in data if '왕대박' in d['n'] and '부평' in d.get('a', '')]
    print(f"--- Search results for '왕대박' in Bupyeong, Incheon ---")
    print(f"Total entries: {len(results)}")
    
    rounds = sorted([d['r'] for d in results])
    print(f"Rounds: {rounds}")
    for d in results:
        print(f"Round {d['r']}: {d['n']} | {d['a']}")

    # 2. Search for any other shops at the target address (십정동 577-6)
    target_addr = "577-6"
    others = [d for d in data if target_addr in d.get('a', '') and '인천' in d.get('a', '')]
    print(f"\n--- Other entries at address containing '{target_addr}' in Incheon ---")
    for d in others:
        print(f"Round {d['r']}: {d['n']} | {d['a']}")

    # 3. Check for address variations or nearby locations
    # Some might be "십정동 577"
    variations = [d for d in data if '십정동 577' in d.get('a', '')]
    print(f"\n--- Entries at '십정동 577' variations ---")
    for d in variations:
        print(f"Round {d['r']}: {d['n']} | {d['a']}")

analyze_wangdaebak()
