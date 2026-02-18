import json
import os

try:
    with open('lotto_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create JS file content
    js_content = f"const lottoData = {json.dumps(data, ensure_ascii=False)};"
    
    with open('lotto_data.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
        
    print(f"Successfully created lotto_data.js with {len(data)} records.")
    
except Exception as e:
    print(f"Error: {e}")
