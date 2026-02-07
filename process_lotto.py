import pandas as pd
import os
import sys

def format_official_lotto_file(input_path):
    """
    동행복권 공식 홈페이지에서 다운로드한 엑셀 파일(XLS/HTML)을 
    사용자님이 요청하신 6자리 당첨 번호만 포함된 깔끔한 엑셀로 변환합니다.
    """
    output_path = "lotto_historic_numbers_1_1209_Final.xlsx"
    
    if not os.path.exists(input_path):
        print(f"[오류] 파일을 찾을 수 없습니다: {input_path}")
        return

    print(f"[*] '{input_path}' 파일을 읽어오는 중입니다...")
    
    try:
        # 공식 엑셀 파일은 실제로는 HTML 테이블 형식이므로 read_html을 사용합니다.
        # 인코딩은 대부부 EUC-KR(cp949) 또는 UTF-8입니다.
        try:
            with open(input_path, 'rb') as f:
                content = f.read()
            html_content = content.decode('cp949', errors='replace')
        except:
            with open(input_path, 'r', encoding='utf-8', errors='replace') as f:
                html_content = f.read()

        # HTML에서 테이블 추출
        dfs = pd.read_html(html_content)
        if not dfs:
            print("[오류] 파일에서 데이터 테이블을 찾을 수 없습니다.")
            return
            
        df = dfs[0]
        
        # 데이터 정제 및 6자리 번호 추출
        # 공식 엑셀 구조 (컬럼 인덱스 기준): 
        # 1: 회차, 13~18: 당첨번호 1~6
        processed_data = []
        for index, row in df.iterrows():
            try:
                round_val = str(row[1]).strip()
                if round_val.isdigit():
                    processed_data.append({
                        '회차': int(round_val),
                        '추첨일': row[2],
                        '번호1': int(row[13]),
                        '번호2': int(row[14]),
                        '번호3': int(row[15]),
                        '번호4': int(row[16]),
                        '번호5': int(row[17]),
                        '번호6': int(row[18])
                    })
            except:
                continue
        
        if not processed_data:
            print("[오류] 데이터 행을 추출하지 못했습니다. 공식 파일이 맞는지 확인해주세요.")
            return

        # 최종 엑셀 저장
        df_final = pd.DataFrame(processed_data)
        df_final = df_final.sort_values(by='회차', ascending=False)
        df_final.to_excel(output_path, index=False)
        
        print(f"\n[성공] 깔끔하게 정리된 엑셀 파일이 생성되었습니다!")
        print(f"경로: {os.path.abspath(output_path)}")
        print("\n--- 데이터 미리보기 (최신 5회차) ---")
        print(df_final.head(5).to_string(index=False))

    except Exception as e:
        print(f"[예외 발생] {str(e)}")

if __name__ == "__main__":
    # 다운로드 받은 파일명을 여기에 입력하거나 명령행 인자로 전달하세요.
    target = "lotto_history.xls" 
    if len(sys.argv) > 1:
        target = sys.argv[1]
    
    format_official_lotto_file(target)
