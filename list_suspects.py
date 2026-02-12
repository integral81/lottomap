
import json

data = json.load(open('verification_results_all.json', encoding='utf-8'))
try:
    dc = json.load(open('double_check_results.json', encoding='utf-8'))
    already_checked = [f"{d['n']}|{d['a']}" for d in dc]
except FileNotFoundError:
    already_checked = []

# Find all suspicious shops (not CONFIRMED)
to_check = [d for d in data if d['status'] != 'CONFIRMED'
            and f"{d['original']['n']}|{d['original']['a']}" not in already_checked]

# Sort by wins desc
to_check.sort(key=lambda x: x['original']['wins'], reverse=True)

# Write to file for clear viewing
with open('suspects_to_verify.txt', 'w', encoding='utf-8') as f:
    f.write(f"Total suspects to double-check: {len(to_check)}\n")
    for i, d in enumerate(to_check[:500]):
        wins = d['original']['wins']
        status = d['status']
        f.write(f"[{wins}W][{status}] {d['original']['n']} | {d['original']['a']}\n")

print(f"saved 500 suspects to suspects_to_verify.txt")
