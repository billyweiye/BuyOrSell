# analyze the trend of the stock with the indicators from indicators.py
from indicators import calculate_trend_indicators
import pandas as pd

def analyze_trend(data):
    data = calculate_trend_indicators(data) 

    trend_signals = ['ma200_ma50_signal','ma_slope_signal','ema_dif_dea_signal','rsi14_signal','boll_width_signal','trend_line_signal','volume_price_signal']

    # 计算趋势信号的累计和
    data['trend_signal'] = data[trend_signals].sum(axis=1)

    return data

