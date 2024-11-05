# analyze the trend of the stock with the indicators from indicators.py
import numpy as np
from indicators import calculate_trend_indicators
import pandas as pd

def analyze_trend(data):
    data = calculate_trend_indicators(data) 

    trend_signals = ['ma100_ma20_signal','ma_slope_signal','macd_signal','rsi14_signal','kdj_signal','wr_signal','bias_12_signal','cci_20_signal','psy_12_signal','trend_line_signal','volume_price_signal']

    # 计算趋势信号的累计和
    data['trend_signal'] = data[trend_signals].sum(axis=1)

    # 给出买卖强烈的型号，若有超过80%的信号为趋势向上，则强烈买入，若超过60%的信号为趋势向上，则买入，若超过80%的信号为趋势向下，则强烈卖出，若超过60%的信号为趋势向下，则卖出, 其他情况为持有
    # 当天的计算结果代表第二天的交易信号，所以往后shift一天
    data['trend_signal']=data['trend_signal'].shift(1)
    conditions = [(data['trend_signal'] >= len(trend_signals)*0.5),
                 (data['trend_signal'] > 0),
                 (data['trend_signal'] <= -len(trend_signals)*0.5),
                 (data['trend_signal'] < 0)
                 ]
    choices = ['strong_buy','buy','strong_sell','sell']
    data['buy_or_sell'] = np.select(conditions, choices, default='hold')

    return data

