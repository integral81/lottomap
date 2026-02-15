import json
import re
import os
import math

DATA_FILE = 'lotto_data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def normalize_address(addr):
    if not isinstance(addr, str): return ""
    addr = addr.strip()
    # Basic normalization
    addr = re.sub(r'(\d+)번지', r'\1', addr)
    addr = re.sub(r'(\d+-\d+)번지', r'\1', addr)
    addr = re.sub(r'\s(\d+)층$', '', addr)
    addr = re.sub(r'\s지하\s*(\d*)층?$', '', addr)
    return addr

def search_shops(query, data=None):
    if data is None: data = load_data()
    results = []
    for item in data:
        n = item.get('n', '')
        a = item.get('a', '')
        if query in n or query in a:
            results.append(item)
    return results

def get_shop_key(item):
    """Returns a tuple (name, address) for unique identification."""
    return (item.get('n', '').strip(), item.get('a', '').strip())

def group_by_shop(data):
    """Groups win records by shop (Name + Address)."""
    groups = {}
    for item in data:
        key = get_shop_key(item)
        if key not in groups:
            groups[key] = []
        groups[key].append(item)
    return groups

def update_shop_pov(name_query, addr_query, pov_data, data=None):
    """
    Updates POV for shops matching name and address query.
    pov_data: { "pan":..., "tilt":..., "zoom":..., "panoId":... }
    """
    if data is None: data = load_data()
    count = 0
    
    # Handle both dictionary and object input for pov_data if needed
    # Ensure standard format: "pov": {"pan":..., "tilt":..., "zoom":...}, "panoid":...
    # In data, 'pov' is strictly the viewpoint. 'panoid' might be root level?
    # Wait, existing data structure check:
    # item['pov'] = { "pan":.., "tilt":.., "zoom":.., "panoId":.. } usually?
    # Or item['id']?
    # Let's check a sample.
    
    for item in data:
        if name_query in item.get('n', '') and addr_query in item.get('a', ''):
            if "pov" not in item: item["pov"] = {}
            
            # Update POV fields
            if "pan" in pov_data: item["pov"]["pan"] = pov_data["pan"]
            if "tilt" in pov_data: item["pov"]["tilt"] = pov_data["tilt"]
            if "zoom" in pov_data: item["pov"]["zoom"] = pov_data["zoom"]
            if "panoId" in pov_data: item["pov"]["panoId"] = pov_data["panoId"]
            
            # Also update lat/lng if provided
            if "lat" in pov_data: item["lat"] = pov_data["lat"]
            if "lng" in pov_data: item["lng"] = pov_data["lng"]
            
            count += 1
            
    return count, data

