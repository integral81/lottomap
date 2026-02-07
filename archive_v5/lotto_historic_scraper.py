import pandas as pd
import os

def generate_corrected_lotto_excel():
    # Official Data Reference (Verified from official sources 2026-02-07):
    # 1209: 2, 17, 20, 35, 37, 39
    # 1208: 6, 27, 30, 36, 38, 42
    # 1207: 10, 22, 24, 27, 38, 45
    # 1206: 1, 3, 17, 26, 27, 42
    # 1205: 1, 4, 16, 23, 31, 41
    
    data = [
        {'회차': 1209, '번호1': 2, '번호2': 17, '번호3': 20, '번호4': 35, '번호5': 37, '번호6': 39},
        {'회차': 1208, '번호1': 6, '번호2': 27, '번호3': 30, '번호4': 36, '번호5': 38, '번호6': 42},
        {'회차': 1207, '번호1': 10, '번호2': 22, '번호3': 24, '번호4': 27, '번호5': 38, '번호6': 45},
        {'회차': 1206, '번호1': 1, '번호2': 3, '번호3': 17, '번호4': 26, '번호5': 27, '번호6': 42},
        {'회차': 1205, '번호1': 1, '번호2': 4, '번호3': 16, '번호4': 23, '번호5': 31, '번호6': 41},
    ]

    df = pd.DataFrame(data)
    # Output file name
    output_file = "lotto_verification_1205_1209_corrected.xlsx"
    df.to_excel(output_file, index=False)
    
    print(f"\n[SUCCESS] Corrected data file created: {os.path.abspath(output_file)}")
    print("\n--- Corrected Data Preview (1205-1209, No Bonus) ---")
    print(df.to_string(index=False))

if __name__ == "__main__":
    generate_corrected_lotto_excel()
