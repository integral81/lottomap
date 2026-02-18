import json
import os

file_path = 'lotto_data.json'

try:
    # Read with utf-8 (or try fallback if it fails)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='cp949') as f:
            data = json.load(f)

    # Write back explicitly as UTF-8 without BOM, ensure_ascii=False for readability
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=0)
    
    print("Successfully re-saved lotto_data.json as UTF-8.")
    
except Exception as e:
    print(f"Error: {e}")
