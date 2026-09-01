"""
지역별 기온 트렌드 대시보드
실행: streamlit run app.py

analysis.ipynb를 먼저 한 번 끝까지 실행해서
data/combined_weather.csv 파일이 생성되어 있어야 합니다.
"""

import pandas as pd
import streamlit as st

st.set_page_config(page_title="지역별 기온 트렌드", layout="wide")

st.title("지역별 기온 트렌드 대시보드")
st.caption("데이터 출처: Open-Meteo Historical Weather API")


@st.cache_data
def load_data():
    df = pd.read_csv("data/combined_weather.csv")
    df["time"] = pd.to_datetime(df["time"])
    return df


try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "data/combined_weather.csv 파일을 찾을 수 없습니다. "
        "먼저 analysis.ipynb를 처음부터 끝까지 실행해주세요."
    )
    st.stop()

# ── 사이드바 필터 ──────────────────────────────
st.sidebar.header("필터")

all_regions = sorted(df["region"].unique())
selected_regions = st.sidebar.multiselect(
    "지역 선택", options=all_regions, default=all_regions
)

variable_options = {
    "평균 기온": "temperature_2m_mean",
    "최고 기온": "temperature_2m_max",
    "최저 기온": "temperature_2m_min",
    "강수량": "precipitation_sum",
}
selected_variable_label = st.sidebar.radio("변수 선택", options=list(variable_options.keys()))
selected_variable = variable_options[selected_variable_label]

min_date = df["time"].min().date()
max_date = df["time"].max().date()
date_range = st.sidebar.slider(
    "기간 선택",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
)

# ── 필터 적용 ──────────────────────────────
filtered = df[
    (df["region"].isin(selected_regions))
    & (df["time"].dt.date >= date_range[0])
    & (df["time"].dt.date <= date_range[1])
]

if filtered.empty:
    st.warning("선택한 조건에 해당하는 데이터가 없습니다. 필터를 조정해주세요.")
    st.stop()

# ── 시계열 그래프 ──────────────────────────────
st.subheader(f"{selected_variable_label} 추이 ({date_range[0]} ~ {date_range[1]})")

pivot = filtered.pivot_table(index="time", columns="region", values=selected_variable)
st.line_chart(pivot)

# ── 요약 통계 ──────────────────────────────
st.subheader("지역별 요약 통계")
summary = filtered.groupby("region")[selected_variable].agg(
    ["mean", "max", "min", "std"]
).round(2)
summary.columns = ["평균", "최고", "최저", "표준편차"]
st.dataframe(summary)

st.caption(
    "왼쪽 사이드바에서 지역, 변수, 기간을 바꿔가며 탐색해보세요."
)
