import subprocess
import json
import re

def search_history():
    target_snippet = "156-1"
    target_snippet_2 = "1428"
    
    print(f"Searching git history for '{target_snippet}' with POV data...")
    
    # Get all commit hashes
    cmd = ["git", "rev-list", "--all", "--max-count=100"] 
    result = subprocess.run(cmd, capture_output=True, text=True)
    commits = result.stdout.strip().split('\n')
    
    found_commits = []
    
    for commit in commits:
        if not commit: continue
        
        # List files changed in this commit
        cmd_files = ["git", "show", "--name-only", "--pretty=format:", commit]
        res_files = subprocess.run(cmd_files, capture_output=True, text=True)
        files = res_files.stdout.strip().split('\n')
        
        for filepath in files:
            if not filepath or not (filepath.endswith('.py') or filepath.endswith('.json')):
                continue
                
            # Read file content at this commit
            try:
                cmd_show = ["git", "show", f"{commit}:{filepath}"]
                res_show = subprocess.run(cmd_show, capture_output=True, encoding='utf-8', errors='ignore')
                content = res_show.stdout
                
                if (target_snippet in content or target_snippet_2 in content):
                    # Check if POV structure exists nearby
                    # We look for "pov": { or 'pov': { within the content
                    if "pov" in content:
                        print(f"[FOUND] Commit: {commit[:7]} File: {filepath}")
                        # Extract context
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if (target_snippet in line or target_snippet_2 in line):
                                # Print 5 lines before and after
                                start = max(0, i - 15)
                                end = min(len(lines), i + 15)
                                print(f"  Context around line {i+1}:")
                                for j in range(start, end):
                                    print(f"    {lines[j].strip()}")
                                found_commits.append((commit, filepath))
                                break # One match per file/commit sufficient
            except Exception as e:
                pass

    if not found_commits:
        print("No robust POV data found in history.")

if __name__ == "__main__":
    search_history()
