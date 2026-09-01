# 지역별 기온 트렌드 분석 (대전/서울/부산/제주)

## 데이터 출처
- Open-Meteo Historical Weather API (https://open-meteo.com/en/docs/historical-weather-api)
- 기간: 2022-01-01 ~ 최신
- 라이선스: Open-Meteo 데이터는 CC BY 4.0으로 제공됨 (출처 표기 조건)

## 실행 방법

### 1. 가상환경 활성화
```
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

### 2. 라이브러리 설치
```
pip install -r requirements.txt
```

### 3. 분석 노트북 실행
`analysis.ipynb`를 VS Code(또는 Jupyter)에서 열고 위에서부터 순서대로 셀을 실행합니다.
실행하면 `data/combined_weather.csv`와 `images/` 폴더에 그래프가 생성됩니다.

### 4. 웹 대시보드 실행
```
streamlit run app.py
```
브라우저가 자동으로 열리며, 지역/기간/변수를 선택해 그래프를 탐색할 수 있습니다.

## 폴더 구조
```
data/       원본 CSV (지역별) + combined_weather.csv (통합본)
images/     분석 노트북에서 생성한 시각화 이미지
analysis.ipynb   핵심 분석 (질문 정의, 정제, 시계열 분석, 시각화, 인사이트)
app.py           Streamlit 웹 대시보드 (보너스)
REPORT.md        최종 분석 리포트
```
