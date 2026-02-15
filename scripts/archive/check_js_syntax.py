
import re
import js2py

def check_syntax():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract script content
    # Assuming one main script block or finding the one with the error
    scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
    
    print(f"Found {len(scripts)} script blocks.")
    
    for i, script in enumerate(scripts):
        try:
            # We just want to check syntax, not run it.
            # js2py might be too heavy or fail on ES6+.
            # Let's use a simpler indentation check or just try to compile with node if available.
            pass
        except Exception as e:
            print(f"Script {i} error: {e}")

    # Better approach: Python's simple brace counter
    script_content = scripts[len(scripts)-1] # The main script is likely the last one
    
    lines = script_content.split('\n')
    open_braces = 0
    for line_idx, line in enumerate(lines):
        for char in line:
            if char == '{': open_braces += 1
            if char == '}': open_braces -= 1
        
        if open_braces < 0:
            print(f"Error: Closed more braces than opened at line {line_idx} (relative to script start)")
            print(f"Line content: {line.strip()}")
            return

    if open_braces > 0:
        print(f"Error: Unclosed braces found. Count: {open_braces}")
    else:
        print("Brace count is balanced.")

if __name__ == "__main__":
    check_syntax()
