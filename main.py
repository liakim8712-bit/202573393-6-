import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rc


def setup_korean_font():
    """한글 깨짐 방지를 위한 글꼴 설정"""
    plt.rcParams['axes.unicode_minus'] = False
    # Windows: 'Malgun Gothic', Mac: 'AppleGothic'
    rc('font', family='Malgun Gothic')


def load_data():
    """CSV 파일 업로드 및 데이터 로드"""
    uploaded_file = st.file_uploader("CSV 파일을 업로드하세요.", type=['csv'])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        return df
    return None


def create_scatter_plot(df, x_col, y_col, color_col, show_regression):
    """산점도 및 추세선 시각화 실행 함수"""
    fig, ax = plt.subplots(figsize=(8, 5))

    if show_regression:
        # sns.regplot의 인자값 scatter_kws (오타 수정 완료)
        sns.regplot(data=df, x=x_col, y=y_col, ax=ax,
                    scatter_kws={'s': 50, 'alpha': 0.5},
                    line_kws={"color": "red"})

        # 색상 구분 항목이 있을 경우 산점도 레이어 추가
        if color_col and color_col != "없음":
            sns.scatterplot(data=df, x=x_col, y=y_col, hue=color_col, ax=ax, s=60)
    else:
        sns.scatterplot(data=df, x=x_col, y=y_col, hue=color_col if color_col != "없음" else None, ax=ax, s=60)

    ax.set_title(f"[{x_col}]와(과) [{y_col}]의 상관관계 분석")
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    st.pyplot(fig)


def main():
    # 페이지 레이아웃 넓게 설정
    st.set_page_config(layout="wide")
    st.title("산점도 활용하기 프로그램")
    setup_korean_font()

    df = load_data()

    if df is not None:
        # 1. 데이터 미리보기 (상단 전폭 배치)
        with st.expander("원본 데이터 확인하기 (상위 5행)"):
            st.write(df.head())

        st.divider()

        # 2. 시각화 설정 및 결과창 나란히 배치 (비율 1:2)
        # vertical_alignment="top"으로 설정하여 삐뚤어지지 않게 맞춤
        col1, col2 = st.columns([1, 2], vertical_alignment="top")

        with col1:
            st.subheader("📊 산점도 설정")
            columns = df.columns.tolist()

            x_axis = st.selectbox("X축 (설명 변수) 선택", columns)
            y_axis = st.selectbox("Y축 (반응 변수) 선택", columns)
            color_axis = st.selectbox("색상 구분 기준 (선택)", ["없음"] + columns)
            show_reg = st.checkbox("추세선(회귀선) 표시", value=True)

            generate_btn = st.button("그래프 생성하기", use_container_width=True)

        with col2:
            st.subheader("📈 시각화 결과")
            if generate_btn:
                create_scatter_plot(df, x_axis, y_axis, color_axis, show_reg)
            else:
                st.info("왼쪽 설정을 확인한 후 '그래프 생성하기' 버튼을 눌러주세요.")


if __name__ == "__main__":
    main()