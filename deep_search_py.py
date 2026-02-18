import glob
import re

def search_py_files():
    target_addr_fragment = "156-1"
    target_addr_fragment_2 = "1428"
    
    print(f"Searching for '{target_addr_fragment}' or '{target_addr_fragment_2}' in ALL .py files...")
    
    py_files = glob.glob('*.py')
    
    found_any = False
    
    for filename in py_files:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if target_addr_fragment in content or target_addr_fragment_2 in content:
                print(f"\n[FOUND] File: {filename}")
                # Print context around the match
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if target_addr_fragment in line or target_addr_fragment_2 in line:
                        print(f"  Line {i+1}: {line.strip()}")
                        found_any = True
        except UnicodeDecodeError:
            # Try cp949 fallback
            try:
                with open(filename, 'r', encoding='cp949') as f:
                    content = f.read()
                if target_addr_fragment in content or target_addr_fragment_2 in content:
                    print(f"\n[FOUND] File: {filename} (cp949)")
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if target_addr_fragment in line or target_addr_fragment_2 in line:
                            print(f"  Line {i+1}: {line.strip()}")
                            found_any = True
            except:
                pass
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            
    if not found_any:
        print("\n[FAILURE] No Python file contains these addresses directly.")

if __name__ == "__main__":
    search_py_files()
