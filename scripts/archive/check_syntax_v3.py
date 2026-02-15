
import re

def check_syntax_robust():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    last_script_start = content.rfind('<script>')
    last_script_end = content.rfind('</script>')
    
    if last_script_start == -1:
        print("No script found")
        return

    js_code = content[last_script_start+8:last_script_end]
    
    # Simple state machine to ignore comments/strings
    state = 'NORMAL' # NORMAL, SINGLE_QUOTE, DOUBLE_QUOTE, BACKTICK, LINE_COMMENT, BLOCK_COMMENT
    stack = []
    
    lines = js_code.split('\n')
    
    # We will simulate char by char
    # This is rough but better than regex for https://
    
    full_text = js_code
    i = 0
    length = len(full_text)
    
    line_num = 1
    
    braces = 0
    parens = 0
    brackets = 0
    
    while i < length:
        char = full_text[i]
        
        if char == '\n':
            line_num += 1
            if state == 'LINE_COMMENT':
                state = 'NORMAL'
        
        if state == 'NORMAL':
            if char == '"': state = 'DOUBLE_QUOTE'
            elif char == "'": state = 'SINGLE_QUOTE'
            elif char == '`': state = 'BACKTICK'
            elif char == '/' and i+1 < length and full_text[i+1] == '/': 
                state = 'LINE_COMMENT'
                i += 1
            elif char == '/' and i+1 < length and full_text[i+1] == '*': 
                state = 'BLOCK_COMMENT'
                i += 1
            elif char == '{': braces += 1
            elif char == '}': braces -= 1
            elif char == '(': parens += 1
            elif char == ')': parens -= 1
            elif char == '[': brackets += 1
            elif char == ']': brackets -= 1
            
        elif state == 'DOUBLE_QUOTE':
            if char == '"' and full_text[i-1] != '\\': state = 'NORMAL'
        elif state == 'SINGLE_QUOTE':
            if char == "'" and full_text[i-1] != '\\': state = 'NORMAL'
        elif state == 'BACKTICK':
            if char == '`' and full_text[i-1] != '\\': state = 'NORMAL'
        elif state == 'BLOCK_COMMENT':
            if char == '*' and i+1 < length and full_text[i+1] == '/':
                state = 'NORMAL'
                i += 1
        
        i += 1

    print(f"Braces: {braces}")
    print(f"Parens: {parens}")
    print(f"Brackets: {brackets}")
    
    if braces == 0 and parens == 0 and brackets == 0:
        print("Syntax seems balanced.")
    else:
        print("Syntax UNBALANCED.")

if __name__ == "__main__":
    check_syntax_robust()
