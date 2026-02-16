
import json

def ultra_process():
    """
    Ultra processing: Clean up shop names with POV registered
    - Remove '★ ' prefix
    - Remove '(복구) ' prefix
    - Regenerate admin list
    """
    print("Starting Ultra processing...")
    
    # Load lotto_data.json
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Clean up shop names
    cleaned_count = 0
    for item in data:
        original_name = item['n']
        cleaned_name = original_name
        
        # Remove prefixes
        if cleaned_name.startswith('★ '):
            cleaned_name = cleaned_name[2:]  # Remove '★ '
        if cleaned_name.startswith('(복구) '):
            cleaned_name = cleaned_name[5:]  # Remove '(복구) '
        
        if cleaned_name != original_name:
            item['n'] = cleaned_name
            cleaned_count += 1
    
    # Save back
    with open('lotto_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Cleaned {cleaned_count} shop names")
    
    # Regenerate admin list
    print("\nRegenerating admin_targets.js...")
    import subprocess
    result = subprocess.run(['python', 'generate_admin_list_final.py'], 
                          capture_output=True, text=True, encoding='utf-8')
    print(result.stdout)
    
    print("\nUltra processing complete!")
    print("- Shop names cleaned")
    print("- Admin list regenerated")
    print("- Ready for next registration")

if __name__ == "__main__":
    ultra_process()
