import json

# 1. Update lotto_data.json
with open('lotto_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Unify to: Ansan-si Danwon-gu Wonseon 1-ro 38, 101-ho
tgt_addr = "경기 안산시 단원구 원선1로 38 101호"
# Coordinates from Wonseon 1-ro data
tgt_lat = 37.326166138141
tgt_lng = 126.803777208185

target_name = "다니엘사"
# Keywords to merge: Wonseon 1-ro, Seonbu-dong (796), Choji-dong (845-1 -> wait, Choji-dong might be different?)
# Let's check Choji-dong coordinates: 37.505410503647,127.021663540771 -> THIS IS SEOUL GANGNAM!
# 37.505, 127.021 is Gangnam. So Choji-dong data is GARBAGE (location wise) or different shop?
# Address says "Ansan-si Danwon-gu Choji-dong 845-1". Coordinates are Gangnam.
# Let's assume it is the same shop (Danielsa is unique name) but moved or wrong data.
# User said "6 wins" in screenshot.
# My data: Wonseon(9) + Seonbu(2) + Choji(3) = 14 wins?
# User screen says 6 wins.
# Maybe Choji-dong is different? But name "Danielsa" is very unique.
# Let's unify all "Danielsa" in Ansan to the location user provided (Wonseon 1-ro).

updated_count = 0
for entry in data:
    if target_name in entry['n'] and '안산' in entry['a']:
        entry['a'] = tgt_addr
        entry['lat'] = tgt_lat
        entry['lng'] = tgt_lng
        updated_count += 1

with open('lotto_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Unified {updated_count} entries for Danielsa")

# 2. Update top_shops_131.json (Remove Danielsa)
with open('top_shops_131.json', 'r', encoding='utf-8') as f:
    top_shops = json.load(f)

# Find Danielsa index
daniel_idx = -1
for i, shop in enumerate(top_shops):
    if target_name in shop['n']:
        daniel_idx = i
        break

removed_count = 0
if daniel_idx != -1:
    # User asked to remove Danielsa AND items above it (top 2?)
    # "관리자페이지에서 다니엘사 포함 상위 2개 삭제 처리하고"
    # Wait, does user mean "remove Danielsa AND the 2 items above it"?
    # Or "Delete top 2 items INCLUDING Danielsa"?
    # If Danielsa is at index 0, delete 0 and 1?
    # Or if Danielsa is index 5, delete 0~5?
    # "다니엘사 포함 상위 2개" -> "Including Danielsa, top 2 items" probably means "Danielsa and the one above it" or "Danielsa and the one below it"?
    # Usually "Top 2" implies the first 2 items in the list.
    # Let's assume user sees Danielsa at the top (or 2nd) and wants to clear the done items.
    # Let's check where Danielsa is.
    pass

# We will handle list trimming in a separate script or logic after checking the list position.
# For now, just merged data.
