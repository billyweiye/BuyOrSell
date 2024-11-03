import streamlit as st
from data_fetcher import fetch_stock_data
from indicators import calculate_trend_indicators
from trend_analysis import analyze_trend
from visualization import plot_trend_analysis

st.title("🎈 Buy Or Sell")

# add an button for users to select the stock they want to test
stock_selections={
    '台积电':'TSM'
}

#股票查询部分
with st.container():
    select_col, query_button_col = st.columns([3, 1])  # 创建两列，第一列宽度是第二列的三倍

    with select_col:
        selected_stock = st.selectbox('请选择一个股票:', stock_selections.keys())
    with query_button_col:
        query_button=st.button('查询')

if query_button:


    selected_stock_code=stock_selections.get(selected_stock)

    stock_data=fetch_stock_data(selected_stock_code,'2y','1d')


    stock_analysis= (
        stock_data
        .pipe(calculate_trend_indicators)
        .pipe(analyze_trend)
        .reset_index()
        .rename(columns={"Date":'date'})
        )


    fig=plot_trend_analysis(stock_analysis)

    st.pyplot(fig)