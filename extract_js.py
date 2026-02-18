
import re

def main():
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the last script tag which usually contains the main logic
        # Or look for the one that contains "var map;" or "function initMap" or "ROADVIEW_PRESETS"
        
        # Method 1: Split by <script> and check content
        scripts = re.split(r'<script.*?>', content)
        
        # We expect the main logic to be in one of the last blocks
        main_script = ""
        for s in scripts:
            if "ROADVIEW_PRESETS" in s or "window.onload" in s:
                main_script = s.split('</script>')[0]
                break
        
        if main_script:
            with open('debug_script.js', 'w', encoding='utf-8') as f:
                f.write(main_script)
            print("Successfully extracted script to debug_script.js")
        else:
            print("Could not find main script block.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
