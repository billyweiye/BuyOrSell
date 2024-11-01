# calculate trend indicators in one function with ta_metrics
import numpy as np
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
    data['ma200_ma50_signal'] = data['ma200_ma50_diff'].apply(lambda x: -1 if x > 0 else 1) # 均线黄金交叉信号 50日均线上穿200日均线为1，金叉，50日均线下穿200日均线为-1，死叉
    # 计算均线的斜率 
    data['50_MA_slope']=data['ma50'].rolling(window=10).apply(lambda x: (x[-1]-x[0])/10,raw=True) 
    data['200_MA_slope']=data['ma200'].rolling(window=10).apply(lambda x: (x[-1]-x[0])/10,raw=True) 
    # 均线斜率信号
    data['ma_slope_signal'] = np.where(
        (data['50_MA_slope'] > 0) & (data['200_MA_slope'] > 0) & (data['close'] > data['ma200']), 1,
        (data['50_MA_slope'] < 0) & (data['200_MA_slope'] < 0) & (data['close'] < data['ma200']), -1,0
    )
    # DIF与DEA的交叉  1.计算12日和26日的EMA  2.DIF=12日EMA-26日EMA  3.计算DIF的9日EMA, 即DEA  4.DIF与DEA的交叉
    data['ema_dif'] = EMA(data['close'],12) - EMA(data['close'],26)
    data['ema_dea'] = EMA(data['ema_dif'],9)
    data['ema_dif_dea_diff'] = data['ema_dif'] - data['ema_dea']
    data['ema_dif_dea_signal'] = data['ema_dif_dea_diff'].apply(lambda x: 1 if x > 0 else -1) # DIF与DEA的交叉信号 DIF>DEA为1 金叉，DIF<DEA为-1 死叉
    # RSI
    data['rsi14'] = RSI(data['close'],timeperiod=14) # 14日RSI 
    # RSI超卖
    data['rsi14_over_sell'] = data['rsi14'].apply(lambda x: 1 if x < 30 else 0) # RSI超卖信号 
    # RSI超买
    data['rsi14_over_buy'] = data['rsi14'].apply(lambda x: -1 if x > 70 else 0) # RSI超买信号
    # RSI趋势信号
    data['rsi14_signal'] = data['rsi14_over_sell'] + data['rsi14_over_buy'] # RSI趋势信号 超卖为-1，超买为1 
    # 布林带
    data['boll_upper'] = BBANDS(data['close'],timeperiod=20,nbdevup=2.0,nbdevdn=2.0,bandtype='upper') # 布林带上线
    data['boll_lower'] = BBANDS(data['close'],timeperiod=20,nbdevup=2.0,nbdevdn=2.0,bandtype='lower') # 布林带下线
    data['boll_middle'] = BBANDS(data['close'],timeperiod=20,nbdevup=2.0,nbdevdn=2.0,bandtype='middle') # 布林带中线
    data['boll_width'] = (data['boll_upper'] - data['boll_lower']) / data['boll_middle']  # 布林带开口扩大
    data['boll_width_diff'] = data['boll_width'].diff()
    data['boll_width_signal'] = data['boll_width_diff'].apply(lambda x: 1 if x > 0 else -1) # 布林带开口扩大信号 开口扩大为1，代表上升趋势，开口缩小为-1，代表下降趋势
    # 趋势线信号
    data['trend_line'] = data['close'].rolling(window=10).mean()
    data['trend_line_diff'] = data['trend_line'].diff()
    data['trend_line_signal'] = data['trend_line_diff'].apply(lambda x: 1 if x > 0 else -1) # 趋势线信号 上升为1，下降为-1
    # 量增价升 与 量缩价缩 信号
    data['volume_diff'] = data['volume'].diff()
    data['price_diff'] = data['close'].diff()
    #当 volumn_diff > 0 且 price_diff > 0 时，为量增价升 赋值1，当 volumn_diff < 0 且 price_diff < 0 时，为量缩价缩 赋值-1
    data['volume_price_signal'] = np.where(
    (data['volume_diff'] > 0) & (data['price_diff'] > 0), 1, 
    np.where((data['volume_diff'] < 0) & (data['price_diff'] < 0), -1, 0))




    return data

