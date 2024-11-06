import streamlit as st
from data_fetcher import fetch_stock_data
from indicators import calculate_trend_indicators
from trend_analysis import analyze_trend
from visualization import plot_trend_analysis
import json 
from ticker_options import us_stocks,china_stocks,hk_stocks





# 创建一个标题
st.markdown('<h1 class="text-4xl font-bold text-center mt-4">🎈 Buy Or Sell</h1>', unsafe_allow_html=True)

#设置状态

#可选市场状态
available_markets=['us_market','china_market','hk_market']
for market in available_markets:
    if market not in st.session_state:
        st.session_state[market]=False

def stock_selection_state(market):
    for m in available_markets:
        if m==market:
            st.session_state[m]=True
        else:
            st.session_state[m]=False


with st.container():
    us,cn,hk,_,_,_,_,_=st.columns([1,1.5,1,2,2,1,1,1])
    with us:
        st.button('US',on_click=stock_selection_state,args=('us_market',))
    with cn:
        st.button('CHINA',on_click=stock_selection_state,args=('china_market',))
    with hk:
        st.button('HK',on_click=stock_selection_state,args=('hk_market',))

stock_selections={}


if st.session_state['us_market']:
    stock_selections=us_stocks()

if st.session_state['china_market']:
    stock_selections=china_stocks()

if st.session_state['hk_market']:
    stock_selections=hk_stocks()

# stock_selections={
#     '台积电':'TSM',
#     '安集科技':'688019.ss'
# }

#股票查询部分
with st.container(height=100):
   # row1=st.columns(1)
    select_col, query_button_col = st.columns([3, 1])  # 创建两列，第一列宽度是第二列的三倍

    with select_col:
        selected_stock = st.selectbox(label='stock_selector', placeholder ='请选择',options= stock_selections.keys(),label_visibility='collapsed')
    with query_button_col:
        query_button=st.button('查询',use_container_width=True,type='primary')

st.divider()  # 👈 Draws a horizontal rule


with st.container():
    if query_button:


        selected_stock_code=stock_selections.get(selected_stock)

        try:
            stock_data=fetch_stock_data(selected_stock_code,'5y','1d')
        except Exception as e:
            st.popover("Something Went Wrong!!")

        if stock_data.empty:
            st.popover("This Stock Is Not Available!")
        else:
            stock_analysis= (
                stock_data
                .pipe(calculate_trend_indicators)
                .pipe(analyze_trend)
                .reset_index()
                .rename(columns={"Date":'date'})
                )
            
            current_recommendation=stock_analysis['buy_or_sell'].iloc[-1:].values[0]


            fig=plot_trend_analysis(stock_analysis)

            st.pyplot(fig)

            st.divider()  # 👈 Draws a horizontal rule

            st.write(current_recommendation.upper())