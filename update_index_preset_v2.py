import os

path = r'c:\Users\이승민\OneDrive\Desktop\KINOV_Lotto_Map\index.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_entry = '            { name: "매물도복권점", addr: "경남 통영시 통영해안로 225-1", panoId: 1204407778, pov: { pan: 20.49, tilt: 1.12, zoom: 2 }, customMessage: "기존 바다로또방(3회) 및 명당방(1200회)을 포함하여 총 5회의 1등 당첨을 기록 중인 대박 명당입니다." },\n'

found = False
for i, line in enumerate(lines):
    if '1204407783' in line:
        lines[i] = new_entry
        found = True
        break

if found:
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print('Updated index.html successfully targeting line.')
else:
    print('PanoID 1204407783 not found.')
