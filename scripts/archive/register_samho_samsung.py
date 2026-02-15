import json

def register_shops():
    json_path = 'lotto_data.json'
    
    # Shop 1: 삼호복권 (Dobong-gu)
    # Wins confirmed in data: 831, 760, 512
    # Resolved POV: panoid=1197861479, pan=297.6, tilt=-0.9
    samho_queries = ["삼호복권", "쌍문동 96-43"]
    samho_pov = {"id": "1197861479", "pan": 297.6, "tilt": -0.9, "zoom": 0}
    samho_addr = "서울 도봉구 도봉로 457 (쌍문동 96-43)"
    samho_lat = 37.646826
    samho_lng = 127.033197
    
    # Shop 2: 삼성복권방 (Dongducheon)
    # Wins confirmed in data: 1207, 811, 299, 282
    # POV provided by user: panoid: 1175702518, pov: { pan: 208.89, tilt: -0.50, zoom: -3 }
    samsung_queries = ["삼성복권방", "생연동 100-1", "어수로 100-1", "생연동 686-17"]
    samsung_pov = {"id": "1175702518", "pan": 208.89, "tilt": -0.50, "zoom": -3}
    samsung_addr = "경기 동두천시 어수로 100-1 (생연동)"
    samsung_lat = 37.902766
    samsung_lng = 127.051403
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        samho_count = 0
        samsung_count = 0
        
        for item in data:
            name = item.get('n', '')
            addr = item.get('a', '')
            
            # Update 삼호복권 (Filter by Dobong area to avoid Mokpo Samho)
            if any(q in name or q in addr for q in samho_queries) and ("서울" in addr or "도봉" in addr):
                item['n'] = "삼호복권"
                item['a'] = samho_addr
                item['lat'] = samho_lat
                item['lng'] = samho_lng
                item['pov'] = samho_pov
                samho_count += 1
                
            # Update 삼성복권방 (Filter by Dongducheon area)
            elif any(q in name or q in addr for q in samsung_queries) and ("동두천" in addr or "생연" in addr):
                item['n'] = "삼성복권방"
                item['a'] = samsung_addr
                item['lat'] = samsung_lat
                item['lng'] = samsung_lng
                item['pov'] = samsung_pov
                samsung_count += 1
                
        if samho_count > 0 or samsung_count > 0:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Successfully updated {samho_count} records for 삼호복권 and {samsung_count} records for 삼성복권방.")
        else:
            print("No matching records found to update.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    register_shops()
