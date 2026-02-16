from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.target_start = 2230
        self.target_end = 2450
        self.current_line = 1

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            attr_dict = dict(attrs)
            id_val = attr_dict.get('id', '')
            class_val = attr_dict.get('class', '')
            if self.current_line >= self.target_start:
                print(f"{self.current_line}: START <div id='{id_val}' class='{class_val}'> (Stack depth: {len(self.stack)})")
            self.stack.append((tag, self.current_line, id_val))

    def handle_endtag(self, tag):
        if tag == 'div':
            if self.stack:
                start_tag, start_line, start_id = self.stack.pop()
                if self.current_line >= self.target_start:
                    print(f"{self.current_line}: END </div> (Matches {start_id} from line {start_line})")

    def handle_data(self, data):
        self.current_line += data.count('\n')

    def feed(self, data):
        # We need to manually count lines because handle_data doesn't capture all newlines in tags
        # So we'll iterate line by line instead? 
        # No, HTMLParser doesn't give line numbers easily.
        # Let's just do a simple manual parse of indentation/tags for this range.
        pass

def manual_check():
    with open('index.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    stack = []
    for i, line in enumerate(lines):
        lineno = i + 1
        if lineno < 2230: continue
        if lineno > 2450: break
        
        stripped = line.strip()
        # Very naive check
        starts = stripped.count('<div')
        ends = stripped.count('</div')
        
        # This is too simple for nested on same line, but let's try to track IDs
        if '<div' in stripped:
            if 'id="' in stripped:
                import re
                m = re.search(r'id="([^"]+)"', stripped)
                id_val = m.group(1) if m else "?"
                print(f"{lineno}: OPEN {id_val}")
                stack.append(id_val)
            else:
                print(f"{lineno}: OPEN (no-id)")
                stack.append("div")
        
        if '</div' in stripped:
            if stack:
                popped = stack.pop()
                print(f"{lineno}: CLOSE matches {popped}")
            else:
                print(f"{lineno}: CLOSE (Stack Empty!)")

if __name__ == "__main__":
    manual_check()
