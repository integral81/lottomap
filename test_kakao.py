import requests
import pandas as pd

KAKAO_API_KEY = "d70d1805bba48840393cec5aa84bca53"

def test_kakao(address):
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    params = {"query": address}
    response = requests.get(url, headers=headers, params=params)
    print(f"Address: {address}")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

df = pd.read_excel('lotto_results_kinov.xlsx')
sample_addresses = df['소재지'].unique()[:5]
for addr in sample_addresses:
    test_kakao(addr)
