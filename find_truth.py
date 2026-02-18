import os

search_term = "세븐일레븐부산온천장역점"
print(f"Searching for '{search_term}' in ALL files...")

found_files = []

for root, dirs, files in os.walk("."):
    for file in files:
        if ".git" in root: continue
        filepath = os.path.join(root, file)
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if search_term in content:
                    print(f"FOUND in: {filepath}")
                    found_files.append(filepath)
                    # Print context
                    lines = content.splitlines()
                    for i, line in enumerate(lines):
                        if search_term in line:
                            print(f"  Line {i+1}: {line.strip()[:200]}")
        except Exception as e:
            pass

print(f"\nTotal files containing term: {len(found_files)}")
