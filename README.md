# 지역별 기온 트렌드 분석 (대전/서울/부산/제주)

## 데이터 출처 및 수집 방법

- Open-Meteo Historical Weather API (https://open-meteo.com/en/docs/historical-weather-api)
- 기간: 2022-01-01 ~ 2026-08-29
- 라이선스: Open-Meteo 데이터는 CC BY 4.0으로 제공됨 (출처 표기 조건)
- 회원가입/API 키 없이 아래와 같은 URL로 직접 CSV 다운로드 가능 (좌표만 바꾸면 다른 지역도 동일하게 받을 수 있음):

```
https://archive-api.open-meteo.com/v1/archive?latitude=36.35&longitude=127.38&start_date=2022-01-01&end_date=2026-08-29&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum&timezone=Asia%2FSeoul&format=csv
```

| 지역 | latitude | longitude |
|---|---|---|
| 대전 | 36.35 | 127.38 |
| 서울 | 37.57 | 126.98 |
| 부산 | 35.18 | 129.08 |
| 제주 | 33.50 | 126.53 |

다운로드한 CSV는 `data/{지역명}_weather_2022_2026.csv` 형식으로 `data/` 폴더에 저장합니다.

## 실행 환경

- Python 3.10 이상 (개발 환경: Python 3.13.15)
- 주요 라이브러리 및 버전은 `requirements.txt` 참고 (`pip freeze`로 고정된 버전 목록)

## 실행 방법

### 1. 가상환경 활성화
```
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

### 2. 라이브러리 설치 (버전 고정됨)
```
pip install -r requirements.txt
```

### 3. 분석 노트북 실행
`analysis.ipynb`를 VS Code(또는 Jupyter)에서 열고 위에서부터 순서대로 셀을 실행합니다.

**노트북 단계별 요약**

| 단계 | 주요 함수/파라미터 | 산출물 |
|---|---|---|
| 1. 데이터 불러오기 | `load_open_meteo_csv()` — CSV 내 `time`으로 시작하는 줄을 자동 탐지해 `skiprows`로 헤더 지정, `pd.concat()`으로 4개 지역 통합 | 통합 DataFrame (6808행) |
| 2. 기본 정보/결측치 확인 | `df.isnull().sum()`, `df.describe()` | 결측치 0개, 이상치 없음 확인 |
| 3-1. 이동평균 | `groupby('region')['temperature_2m_mean'].transform(lambda x: x.rolling(7 또는 30).mean())` | `ma7`, `ma30` 컬럼 |
| 3-2. 월별 집계 | `dt.to_period('M')` 기준 `groupby().mean()` | 지역×월 평균기온 |
| 3-3. 변화율 | `groupby('region')['temp_mean'].diff()` | 전월 대비 변화량 |
| 3-3. STL 분해 | `statsmodels.tsa.seasonal.STL(sub, period=365, robust=True)` | 추세/계절성/잔차 분리, `images/04_stl_decomposition.png` |
| 4. 시각화 | `matplotlib.pyplot` (`plt.plot`, `plt.bar`) | `images/01~04` PNG 4종 |
| 5. 인사이트 작성 | 마크다운 셀에 직접 서술 | REPORT.md 7번 섹션 재료 |

실행하면 `data/combined_weather.csv`와 `images/` 폴더의 그래프 4종이 생성됩니다.

### 4. 리포트 생성 (선택)
통계 수치를 자동 반영해 REPORT.md를 다시 생성하고 싶다면:
```
python generate_report.py
```

### 5. 웹 대시보드 실행
```
streamlit run app.py
```
브라우저가 자동으로 열리며, 지역/기간/변수를 선택해 그래프를 탐색할 수 있습니다.
(`data/combined_weather.csv`가 먼저 생성되어 있어야 합니다.)

## 폴더 구조
```
data/       원본 CSV (지역별) + combined_weather.csv (통합본)
images/     분석 노트북에서 생성한 시각화 이미지 4종
analysis.ipynb       핵심 분석 (질문 정의, 정제, 시계열 분석, 시각화, 인사이트)
app.py                Streamlit 웹 대시보드 (보너스)
generate_report.py    REPORT.md 자동 생성 스크립트
REPORT.md             최종 분석 리포트
requirements.txt      의존성 목록 (버전 고정)
```