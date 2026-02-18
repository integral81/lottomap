
import re

def main():
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by <script>
        scripts = re.split(r'<script.*?>', content)
        
        # We want the LAST script block (or the one containing openRoadview)
        target_script = ""
        for s in scripts:
            if "function openRoadview" in s:
                target_script = s.split('</script>')[0]
                break
        
        if target_script:
            with open('debug_script_2.js', 'w', encoding='utf-8') as f:
                f.write(target_script)
            print("Successfully extracted 2nd script to debug_script_2.js")
        else:
            print("Could not find openRoadview script block.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
