# analyze the trend of the stock with the indicators from indicators.py
import numpy as np
from indicators import calculate_trend_indicators
import pandas as pd

def analyze_trend(data):
    data = calculate_trend_indicators(data) 

    trend_signals = ['ma100_ma20_signal','ma_slope_signal','ema_dif_dea_signal','rsi14_signal','boll_width_signal','trend_line_signal','volume_price_signal']

    # 计算趋势信号的累计和
    data['trend_signal'] = data[trend_signals].sum(axis=1)

    # 给出买卖强烈的型号，若有超过80%的信号为趋势向上，则强烈买入，若超过60%的信号为趋势向上，则买入，若超过80%的信号为趋势向下，则强烈卖出，若超过60%的信号为趋势向下，则卖出, 其他情况为持有
    conditions = [(data['trend_signal'] > len(trend_signals)*0.8),
                 (data['trend_signal'] > len(trend_signals)*0.6),
                 (data['trend_signal'] < -len(trend_signals)*0.8),
                 (data['trend_signal'] < -len(trend_signals)*0.6)]
    choices = ['strong_buy','buy','strong_sell','sell']
    data['buy_or_sell'] = np.select(conditions, choices, default='hold')

    return data

