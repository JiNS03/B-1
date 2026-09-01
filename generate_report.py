"""
REPORT.md 자동 생성 스크립트

사용법:
1. analysis.ipynb를 먼저 끝까지 실행해서 data/combined_weather.csv를 만들어둡니다.
2. 아래 "여기부터 직접 입력하세요" 구간의 내용을 본인 분석 내용으로 채웁니다.
3. 터미널에서 실행: python generate_report.py
4. 실행할 때마다 최신 데이터 통계 + 방금 입력한 인사이트가 합쳐진 REPORT.md가 새로 만들어집니다.
"""

import pandas as pd

# ============================================================
# 여기부터 직접 입력하세요 (자유롭게 수정 가능)
# ============================================================

ANALYSIS_TOPIC = "대전, 서울, 부산, 제주 4개 지역의 일별 기온 데이터를 비교해, 지역별 기후 특성과 시간에 따른 변화 추세를 확인해보고자 함"

QUESTIONS = [
    "4개 지역 중 기온 변동성(표준편차)이 가장 큰 지역과 작은 지역은 어디이며, 그 차이는 어느 정도인가?",
    "월별로 봤을 때 지역 간 기온 차이가 가장 크게 벌어지는 달과 가장 비슷해지는 달은 언제인가?",
    "2022년부터 최근까지 여름/겨울 기온 피크에 뚜렷한 상승 추세가 있는가?",
]

DATA_CLEANING_NOTES = """
- 결측치: (여기에 df.isnull().sum() 결과를 보고 직접 기입)
- 이상치: (여기에 describe() 결과를 보고 직접 기입)
- 컬럼명 정리: Open-Meteo CSV 컬럼명에 포함된 단위(°C, mm) 표기를 제거함
"""

# 인사이트: 관찰(observation)에는 반드시 숫자를 포함시키세요.
# 아래 자동 통계 출력 결과를 참고해서 채우면 정확한 숫자를 넣기 쉽습니다.
INSIGHTS = [
    {
        "observation": "(예: 1월 기준 서울은 평균 약 X°C, 제주는 약 Y°C로 Z°C 차이가 났다.)",
        "hypothesis": "(왜 그런 결과가 나왔을지 가설)",
        "action": "(다음에 무엇을 더 확인하면 좋을지 제안)",
    },
    {
        "observation": "",
        "hypothesis": "",
        "action": "",
    },
    {
        "observation": "",
        "hypothesis": "",
        "action": "",
    },
]

CONCLUSION = "(전체 분석을 한두 문단으로 요약)"

LIMITATIONS = "(데이터/분석 방법의 한계점을 기입)"

AI_USAGE_LOG = [
    {
        "task": "데이터 로딩 함수 및 지역 통합 코드 작성",
        "reason": "반복적인 CSV 파싱 코드 작성 시간 절감",
        "verification": "직접 실행해 shape/컬럼명이 예상과 일치하는지 확인",
    },
    {
        "task": "가상환경/에러 디버깅",
        "reason": "에러 메시지 해석 시간 절감",
        "verification": "제안받은 수정 코드를 실행해 에러 해소 여부 확인",
    },
    {
        "task": "그래프 해석 문장 형식(관찰/해석/제안) 구성 지원",
        "reason": "관찰과 해석을 구분해 서술하는 형식 참고",
        "verification": "그래프의 실제 수치와 대조하여 관찰 문장을 실제 값으로 교체",
    },
]

# ============================================================
# 여기서부터는 자동 처리 영역입니다 (수정하지 않아도 됩니다)
# ============================================================

df = pd.read_csv("data/combined_weather.csv")
df["time"] = pd.to_datetime(df["time"])

regions = sorted(df["region"].unique())
n_per_region = df[df["region"] == regions[0]].shape[0]
total_rows = df.shape[0]
missing_count = int(df.isnull().sum().sum())
date_min = df["time"].min().date()
date_max = df["time"].max().date()

std_by_region = df.groupby("region")["temperature_2m_mean"].std().round(2).sort_values()
mean_by_region_month = (
    df.groupby(["region", df["time"].dt.month])["temperature_2m_mean"].mean().round(1)
)

print("=" * 50)
print("자동 계산된 통계 (인사이트 작성에 참고하세요)")
print("=" * 50)
print(f"기간: {date_min} ~ {date_max}")
print(f"지역당 데이터 수: {n_per_region}일 / 전체: {total_rows}행")
print(f"결측치 총 개수: {missing_count}개")
print("\n지역별 기온 표준편차(변동성):")
print(std_by_region.to_string())
print("\n지역별 월평균 기온:")
print(mean_by_region_month.unstack(level=0).round(1))
print("=" * 50)

questions_md = "\n".join(f"{i+1}. {q}" for i, q in enumerate(QUESTIONS))

insights_md = ""
for i, ins in enumerate(INSIGHTS, start=1):
    insights_md += f"""
### 인사이트 {i}
- 관찰(Fact): {ins['observation']}
- 해석(가설): {ins['hypothesis']}
- 다음 행동/제안: {ins['action']}
"""

ai_log_rows = "\n".join(
    f"| {log['task']} | {log['reason']} | {log['verification']} |" for log in AI_USAGE_LOG
)

report = f"""# 지역별 기온 트렌드 분석 리포트

## 1. 분석 주제 및 선정 이유

{ANALYSIS_TOPIC}

## 2. 분석 질문

{questions_md}

## 3. 데이터 설명

- 출처: Open-Meteo Historical Weather API
- 지역: {', '.join(regions)}
- 기간: {date_min} ~ {date_max}
- 데이터 수: 지역당 {n_per_region}일, 전체 {total_rows}행
- 주요 컬럼: temperature_2m_max/min/mean(°C), precipitation_sum(mm)

## 4. 데이터 정제
{DATA_CLEANING_NOTES}

## 5. 적용한 시계열 분석 기법

1. 이동평균 (7일/30일) — 단기 노이즈를 줄이고 계절적 추세를 확인하기 위해 적용
2. 월별/지역별 집계 통계 및 변동성(표준편차) — 지역 간 패턴 차이를 정량적으로 비교하기 위해 적용

## 6. 시각화

### 시각화 1: 지역별 30일 이동평균 기온 추이
![지역별 추이](images/01_region_trend.png)

### 시각화 2: 지역별 월평균 기온
![월평균](images/02_monthly_avg_by_region.png)

### 시각화 3: 지역별 기온 변동성
![변동성](images/03_volatility_by_region.png)

## 7. 인사이트
{insights_md}
## 8. 결론 및 한계점

- 결론: {CONCLUSION}
- 한계점: {LIMITATIONS}

## 9. 보너스: 웹 대시보드

- 실행 방법: `streamlit run app.py`
- 지역 / 기간 / 변수(평균·최고·최저기온, 강수량) 3가지 조건을 자유롭게 조합해 탐색 가능

## 10. AI 사용 로그

| 사용 작업 | 사용 이유 | 검증 방법 |
|---|---|---|
{ai_log_rows}

## 참고 사항

- 데이터 출처: Open-Meteo (CC BY 4.0, 출처 표기 필요)
- 실행 환경 및 방법: README.md 참고
"""

with open("REPORT.md", "w", encoding="utf-8") as f:
    f.write(report)

print("\nREPORT.md 생성 완료!")
