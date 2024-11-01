# analyze the trend of the stock with the indicators from indicators.py
from indicators import calculate_trend_indicators
import pandas as pd

def analyze_trend(data):
    data = calculate_trend_indicators(data)

    return data

