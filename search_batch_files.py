import glob

targets = ['세븐일레븐', '제철', 'Goodday', '완월', '채널큐', '해피복권']

print("Searching Python files for targets...")
for py_file in glob.glob('apply_batch*.py'):
    with open(py_file, 'r', encoding='utf-8') as f:
        content = f.read()
        for t in targets:
            if t in content:
                print(f"Terms '{t}' found in {py_file}")
                # Print context
                lines = content.splitlines()
                for i, line in enumerate(lines):
                    if t in line:
                         print(f"  Line {i+1}: {line.strip()}")
