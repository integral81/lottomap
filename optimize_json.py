import json
import os

target_file = 'lotto_data.json'

def optimize():
    if not os.path.exists(target_file):
        print(f"File not found: {target_file}")
        return

    original_size = os.path.getsize(target_file)
    print(f"Original Size: {original_size / 1024:.2f} KB")

    # Read data
    with open(target_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Write data with NO indentation (minified)
    with open(target_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, separators=(',', ':'), ensure_ascii=False)

    new_size = os.path.getsize(target_file)
    print(f"Optimized Size: {new_size / 1024:.2f} KB")
    print(f"Reduction: {(original_size - new_size) / 1024:.2f} KB ({(1 - new_size/original_size)*100:.2f}%)")

if __name__ == "__main__":
    optimize()
