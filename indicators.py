# calculate trend indicators in one function with ta_metrics
from ta_metrics import MA,EMA,BBANDS,RSI

def calculate_trend_indicators(data): 
    '''
    计算趋势指标
    data: pd.DataFrame, 包含股票数据
    return: pd.DataFrame, 包含趋势指标
    signal: int, 1表示金叉，0表示死叉 
    '''
    data['ma200'] = MA(data['close'],timeperiod=200)
    data['ma50'] = MA(data['close'],timeperiod=50)
    # 均线黄金交叉
    data['ma200_ma50_diff'] = data['ma200'] - data['ma50']
    data['ma200_ma50_signal'] = data['ma200_ma50_diff'].apply(lambda x: 0 if x > 0 else 1) # 均线黄金交叉信号
    # 均线整体向上
    data['ma200_ma50_diff_cumsum'] = data['ma200_ma50_diff'].cumsum()
    data['ma200_ma50_signal'] = data['ma200_ma50_diff_cumsum'].apply(lambda x: 1 if x > 0 else 0) # 均线整体向上信号
    # DIF与DEA的交叉  1.计算12日和26日的EMA  2.DIF=12日EMA-26日EMA  3.计算DIF的9日EMA, 即DEA  4.DIF与DEA的交叉
    data['ema_dif'] = EMA(data['close'],12) - EMA(data['close'],26)
    data['ema_dea'] = EMA(data['ema_dif'],9)
    data['ema_dif_dea_diff'] = data['ema_dif'] - data['ema_dea']
    data['ema_dif_dea_signal'] = data['ema_dif_dea_diff'].apply(lambda x: 1 if x > 0 else 0) # DIF与DEA的交叉信号
    # RSI
    data['rsi14'] = RSI(data['close'],timeperiod=14) # 14日RSI 
    # RSI超卖
    data['rsi14_over_sell'] = data['rsi14'].apply(lambda x: 1 if x < 30 else 0) # RSI超卖信号 
    # RSI超买
    data['rsi14_over_buy'] = data['rsi14'].apply(lambda x: 1 if x > 70 else 0) # RSI超买信号
    # 布林带
    data['boll_upper'] = BBANDS(data['close'],timeperiod=20,nbdevup=2.0,nbdevdn=2.0,bandtype='upper') # 布林带上线
    data['boll_lower'] = BBANDS(data['close'],timeperiod=20,nbdevup=2.0,nbdevdn=2.0,bandtype='lower') # 布林带下线
    data['boll_middle'] = BBANDS(data['close'],timeperiod=20,nbdevup=2.0,nbdevdn=2.0,bandtype='middle') # 布林带中线
    data['boll_width'] = (data['boll_upper'] - data['boll_lower']) / data['boll_middle']  # 布林带开口扩大
    data['boll_width_diff'] = data['boll_width'].diff()
    data['boll_width_signal'] = data['boll_width_diff'].apply(lambda x: 1 if x > 0 else 0) # 布林带开口扩大信号
    # 绘制趋势线
    data['trend_line'] = data['close'].rolling(window=10).mean()
    data['trend_line_diff'] = data['trend_line'].diff()
    data['trend_line_signal'] = data['trend_line_diff'].apply(lambda x: 1 if x > 0 else 0) # 趋势线信号 
    # 成交量放大
    data['volume_diff'] = data['volume'].diff()
    data['volume_signal'] = data['volume_diff'].apply(lambda x: 1 if x > 0 else 0) # 成交量放大信号


    return data

