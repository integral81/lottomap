import os
import shutil
import glob

def cleanup_files():
    # Define directories
    scripts_dir = "scripts"
    trash_dir = "trash" # For truly temp stuff if needed, but user said delete logic. I'll move to scripts/archive for safety.
    archive_dir = os.path.join(scripts_dir, "archive")
    
    os.makedirs(archive_dir, exist_ok=True)
    
    # Core files to KEEP in root
    whitelist = [
        "auto_update.py",
        "scraper_v3.py", 
        "lotto_utils.py", # Future
        "register_shop.py", # Future
        "cleanup_files.py", # Self
        "server.py", # If exists
        "main.py", # If exists
    ]
    
    # Patterns to move to scripts/archive
    # Basically everything else that is .py
    # We will be aggressive but exclude whitelist
    
    all_py_files = glob.glob("*.py")
    
    moved_count = 0
    for f in all_py_files:
        if f in whitelist:
            continue
            
        # safety check for auto_update.py again
        if "auto_update" in f:
            continue
            
        src = f
        dst = os.path.join(archive_dir, f)
        
        try:
            shutil.move(src, dst)
            moved_count += 1
            # print(f"Moved {src} -> {dst}")
        except Exception as e:
            print(f"Failed to move {src}: {e}")
            
    print(f"Moved {moved_count} Python scripts to {archive_dir}")

    # Also move some .html logs or temp files?
    # Keep .html, .js, .json in root for now as they might be used by index.html or admin tools
    # Move specific temp htmls
    temp_htmls = glob.glob("debug_*.html") + glob.glob("test_*.html") + glob.glob("round_*.html")
    for f in temp_htmls:
        if "index.html" in f or "admin" in f or "lotto_map" in f: continue
        try:
            shutil.move(f, os.path.join(archive_dir, f))
        except: pass

if __name__ == "__main__":
    cleanup_files()
