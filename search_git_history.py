
import subprocess

def search_history():
    targets = [
        "황금복권방", "복권명당", "가판점", "GS25", "목화휴게소", 
        "cu", "복권판매점", "뉴빅마트", "대박찬스"
    ]
    
    print("--- Searching Git History for Missing Shops ---")
    
    for t in targets:
        # Search commit messages
        cmd_msg = f'git log --grep="{t}" --oneline'
        try:
            res_msg = subprocess.check_output(cmd_msg, shell=True).decode('utf-8', errors='ignore')
            if res_msg.strip():
                print(f"\n[MATCH: Message] '{t}' found in:")
                print(res_msg)
        except:
            pass
            
        # Search content (pickaxe)
        cmd_code = f'git log -S "{t}" --oneline'
        try:
            res_code = subprocess.check_output(cmd_code, shell=True).decode('utf-8', errors='ignore')
            if res_code.strip():
                print(f"[MATCH: Code] '{t}' found in:")
                print(res_code)
        except:
            pass

if __name__ == "__main__":
    search_history()
