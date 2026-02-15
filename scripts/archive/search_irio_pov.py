import requests

def search_irio_pov():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    # Bangbae-dong 454-20 (Hyoryeong-ro 34-gil 7)
    # Approx coords: 37.4795, 126.9965 (Bangbae Station area)
    # Let's search by address logic or just try a coord near 454-20
    # 454-20 is near Bangbae Station.
    
    # Using a known coord for Bangbae-dong 454-20
    url = f"https://map.kakao.com/link/roadview/37.481515,126.997232" 
    try:
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
        print(f"Roadview URL for Irio Market: {response.url}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    search_irio_pov()
