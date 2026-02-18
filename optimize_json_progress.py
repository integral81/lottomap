import json
import os
import time
import sys

# 한글 출력 깨짐 방지
sys.stdout.reconfigure(encoding='utf-8')

def report(percent, msg):
    print(f"■■■ [진행률 {percent}%] {msg}")
    time.sleep(0.5) # 사용자가 볼 수 있도록 0.5초 대기

target_file = 'lotto_data.json'

if not os.path.exists(target_file):
    print("❌ 파일을 찾을 수 없습니다.")
    sys.exit()

report(0, "대상 파일 분석 시작...")

# 20% - 파일 크기 확인 및 읽기 준비
original_size = os.path.getsize(target_file)
report(20, f"원본 크기 확인: {original_size/1024:.2f} KB. 메모리로 로딩합니다.")

# 40% - JSON 파싱
with open(target_file, 'r', encoding='utf-8') as f:
    data = json.load(f)
report(40, f"데이터 파싱 완료. 총 데이터 항목: {len(data):,}개")

# 60% - 메모리 상에서 최적화 수행
report(60, "공백 제거 및 최적화(Minify) 알고리즘 적용 중...")
# separators=(',', ':')를 사용하여 공백을 제거함
optimized_data = json.dumps(data, separators=(',', ':'), ensure_ascii=False)

# 80% - 파일 쓰기 준비
report(80, "최적화된 데이터를 파일에 덮어쓰기 하는 중...")
with open(target_file, 'w', encoding='utf-8') as f:
    f.write(optimized_data)

# 100% - 최종 결과 리포트
new_size = os.path.getsize(target_file)
reduction = original_size - new_size
reduction_percent = (1 - new_size/original_size) * 100

report(100, "작업 완료!")
print("\n" + "="*40)
print(f"📉 [최적화 결과 보고]")
print(f" - 이전 크기: {original_size/1024:.2f} KB")
print(f" - 현재 크기: {new_size/1024:.2f} KB")
print(f" - 줄어든 용량: {reduction/1024:.2f} KB (-{reduction_percent:.1f}%)")
print("="*40)
