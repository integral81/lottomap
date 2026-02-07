import requests
import os

def download_superkts_lotto():
    url = "https://superkts.com/lotto/history/"
    # Often there's a specific download link, but let's try to get the HTML first if we can't find it.
    # Actually, many sites have /excel or /download.
    # From search, superkts provides an xlsx.
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    }
    
    try:
        print(f"[*] Attempting to access {url}...")
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            print("[SUCCESS] Page accessed.")
            # Search for .xlsx or .csv download link in the HTML
            html = response.text
            print(f"[DEBUG] HTML Excerpt (first 2000 chars):\n{html[:2000]}")
            if ".xlsx" in html or ".xls" in html or "csv" in html:
                print("[*] Found a potential data link in page.")
                # Look for links or buttons
                import re
                # More generic search
                links = re.findall(r'href=[\'"]?([^\'" >]+(?:xlsx|xls|csv))', html, re.I)
                if not links:
                    # Look for onclick or other patterns
                    links = re.findall(r'location\.href=[\'"]?([^\'"]+)', html)
                
                if links:
                    dl_url = links[0]
                    # ... rest of the logic
                    if not dl_url.startswith("http"):
                        dl_url = "https://superkts.com" + dl_url
                    print(f"[*] Downloading from: {dl_url}")
                    res_dl = requests.get(dl_url, headers=headers, timeout=20)
                    if res_dl.status_code == 200:
                        with open("lotto_full_superkts.xlsx", "wb") as f:
                            f.write(res_dl.content)
                        print("[SUCCESS] lotto_full_superkts.xlsx downloaded.")
                        return True
            else:
                print("[INFO] No direct .xlsx link found in HTML.")
        else:
            print(f"[FAIL] Status code: {response.status_code}")
    except Exception as e:
        print(f"[ERROR] {str(e)}")
    return False

if __name__ == "__main__":
    download_superkts_lotto()
