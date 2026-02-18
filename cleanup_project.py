import os
import shutil
import datetime

# Configuration
ARCHIVE_DIR = "archive_20260217"
ROOT_DIR = "."

# Patterns to STRICTLY KEEP (4+ Wins, POV info, Core System)
# These files will NOT be moved.
KEEP_PATTERNS = [
    "lotto_data.json",              # Main DB
    "index.html",                   # Main Map
    "view_verification.bat",        # Current User Tool
    "verify_real_roadview.html",    # Current User Tool
    "verify_success_batch.html",    # Current User Tool
    "pov_extractor.py",             # Active Script
    "update_and_verify.py",         # Active Script
    "debug_verification.py",        # Active Script
    "task.md",                      # Task tracking
    "shops_4wins",                  # User Request: 4+ Wins
    "missing_4win",                 # User Request: 4+ Wins
    "verification_results_4wins",   # User Request: 4+ Wins
    "README.md",
    ".gitignore",
    ".git",
    ".github",
    "cleanup_project.py"            # Self
]

# Extensions/Prefixes to likely archive if not in keep list
# We will check if the filename starts with these prefixes.
ARCHIVE_PREFIXES = [
    "update_", "verify_", "check_", "find_", "register_", "backup_", 
    "lotto_data_backup", "analyze_", "report_", "create_", "extract_", 
    "resolve_", "restore_", "recover_", "generate_", "test_", "count_",
    "embed_", "calc_", "audit_", "decode_", "smart_", "simple_", "ultra_"
]

ARCHIVE_EXTENSIONS = [".bak"] # Always archive these extensions

def setup_archive():
    if not os.path.exists(ARCHIVE_DIR):
        os.makedirs(ARCHIVE_DIR)
        print(f"Created archive directory: {ARCHIVE_DIR}")

def is_kept(filename):
    # Check exact matches or substring matches for 4-win files
    for pattern in KEEP_PATTERNS:
        if pattern == filename:
            return True
        if "4wins" in filename or "4win" in filename: # Special check for 4wins patterns
            return True
    return False

def run_cleanup():
    setup_archive()
    
    moved_count = 0
    kept_count = 0
    
    files = os.listdir(ROOT_DIR)
    
    for filename in files:
        file_path = os.path.join(ROOT_DIR, filename)
        
        # Skip directories and the archive dir itself
        if not os.path.isfile(file_path):
            continue
            
        # 1. Check if it's in the KEEP list (Priority 1)
        if is_kept(filename):
            print(f"[KEEP] {filename}")
            kept_count += 1
            continue
            
        # 2. Archive Candidates
        # Logic: Archive old batch scripts, backups, temp htmls
        should_archive = False
        
        name, ext = os.path.splitext(filename)
        
        # Check prefixes
        for prefix in ARCHIVE_PREFIXES:
            if filename.startswith(prefix):
                should_archive = True
                break
        
        # Check extensions
        if ext in ARCHIVE_EXTENSIONS:
            should_archive = True
            
        # HTML files that are not index.html or the active verification files (which are kept above)
        if ext == ".html" and filename != "index.html":
             should_archive = True

        if should_archive:
            try:
                shutil.move(file_path, os.path.join(ARCHIVE_DIR, filename))
                print(f"[MOVED] {filename} -> {ARCHIVE_DIR}/")
                moved_count += 1
            except Exception as e:
                print(f"[ERROR] Could not move {filename}: {e}")
        else:
            print(f"[SKIP] {filename} (Not in archive criteria)")
            kept_count += 1

    print(f"\nCleanup Complete.")
    print(f"Moved: {moved_count} files")
    print(f"Kept: {kept_count} files")

if __name__ == "__main__":
    run_cleanup()
