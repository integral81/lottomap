
def print_context():
    fname = 'commit_42_povs_utf8.txt'
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
        
    keyword = "129.03"
    idx = content.find(keyword)
    if idx != -1:
        print(f"--- Context for {keyword} ---")
        start = max(0, idx - 500)
        end = min(len(content), idx + 500)
        print(content[start:end])
    else:
        print(f"Keyword {keyword} not found.")

if __name__ == "__main__":
    print_context()
