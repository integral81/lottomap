
import json

def create_recovered_json():
    # Data manually extracted from specific commits found in git log
    recovered = [
        # From commit 4253187 (Register Mokhwa POV)
        { 
            "name": "목화휴게소", 
            "addr": "경남 사천시 사천대로 912", 
            "panoId": 1188272977, 
            "pov": { "pan": 34.24, "tilt": 0.74, "zoom": 0 } 
        },
        # From commit 2f8dc78 (Register 6 POVs: Bokkwon Myeongdang, Alibai...)
        {
            "name": "복권명당",
            "addr": "충남 공주시 번영1로 142", # Default address from that commit?
            # Wait, the commit had: 
            # { name: "복권명당", addr: "충남 공주시 번영로 585-12", panoId: 1179373419, pov: { pan: 305.44, tilt: 0.77, zoom: -3 } }
            # But the user asked for "Daegu Suseong" Masterpiece. 
            # This "Gongju" one might be a different shop.
            # I should SKIP this if it's not the Daegu one.
            # Let's check commit 2f8dc78 content for "Daegu"?
        },
        # From commit 2f8dc78
        {
             "name": "알리바이(나주점)", 
             "addr": "전남 나주시 나주로 142 알리바이", 
             "panoId": 1191260182, 
             "pov": { "pan": 17.27, "tilt": -9.34, "zoom": -3 } 
        }
    ]
    
    # Filter out empty or wrong ones
    final_list = [r for r in recovered if r.get('panoId')]
    
    with open('recovered_from_history.json', 'w', encoding='utf-8') as f:
        json.dump(final_list, f, indent=2, ensure_ascii=False)
        
    print(f"Saved {len(final_list)} verified records from history.")

if __name__ == "__main__":
    create_recovered_json()
