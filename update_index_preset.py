import re
import os

path = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\index.html'
if not os.path.exists(path):
    print(f"File not found: {path}")
    exit(1)

content = open(path, 'r', encoding='utf-8').read()

# Pattern matching for the existing "매물도" preset
# Using name and panoId as anchors
old_entry_pattern = r'\{\s*name:\s*\"매물도\",.*?panoId:\s*1204407783,.*?\n\s*\},'

new_entry = '{ name: "매물도복권점", addr: "경남 통영시 통영해안로 225-1", panoId: 1204407778, pov: { pan: 20.49, tilt: 1.12, zoom: 2 }, customMessage: "기존 바다로또방(3회) 및 명당방(1200회)을 포함하여 총 5회의 1등 당첨을 기록 중인 대박 명당입니다." },'

new_content = re.sub(old_entry_pattern, new_entry, content, flags=re.DOTALL)

if content != new_content:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('Updated index.html successfully.')
else:
    # Try a broader pattern if specific one fails
    # Looking for the name only
    fallback_pattern = r'\{\s*name:\s*\"매물도\",.*?\n\s*\},'
    new_content = re.sub(fallback_pattern, new_entry, content, flags=re.DOTALL)
    if content != new_content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print('Updated index.html successfully (fallback).')
    else:
        print('Pattern not found in index.html.')
