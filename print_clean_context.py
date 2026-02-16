
def print_clean_context():
    fname = 'commit_42_povs_utf8.txt'
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
        
    keywords = ["129.03", "128.61", "127.49"]
    
    for k in keywords:
        idx = content.find(k)
        if idx != -1:
            print(f"--- Context for {k} ---")
            start = max(0, idx - 300)
            end = min(len(content), idx + 300)
            chunk = content[start:end]
            
            # Sanitize: replace non-ascii with ?
            clean_chunk = "".join([c if ord(c) < 128 else '?' for c in chunk])
            print(clean_chunk)
            print("-" * 40)
        else:
            print(f"Keyword {k} not found.")

if __name__ == "__main__":
    print_clean_context()
