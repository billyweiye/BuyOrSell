# calculate trend indicators in one function with ta_metrics
import numpy as np
from ta_metrics import MA,EMA,BBANDS,RSI,MACD,STOCH,WILLR,BIAS,CCI,PSY

def calculate_trend_indicators(data): 
    '''
    计算趋势指标
    data: pd.DataFrame, 包含股票数据
    return: pd.DataFrame, 包含趋势指标
    signal: int, 1表示金叉，0表示死叉 
    '''
    data['ma100'] = MA(data['close'],timeperiod=100)
    data['ma20'] = MA(data['close'],timeperiod=20)
    # 均线黄金交叉
    data['ma100_ma20_diff'] = data['ma100'] - data['ma20']
    conditions=[(data['ma100_ma20_diff']>0) & (data['ma100_ma20_diff'].shift(1) < 0),(data['ma100_ma20_diff']<0) & (data['ma100_ma20_diff'].shift(1) > 0)]
    choices=[-1,1]
    data['ma100_ma20_signal'] =np.select(conditions,choices,default=0) # 均线黄金交叉信号 50日均线上穿200日均线为1，金叉，50日均线下穿200日均线为-1，死叉

    # 计算均线的斜率 
    data['20_MA_slope']=data['ma20'].rolling(window=10).apply(lambda x: (x[-1]-x[0])/10,raw=True) 
    data['100_MA_slope']=data['ma100'].rolling(window=10).apply(lambda x: (x[-1]-x[0])/10,raw=True) 
    # 均线斜率信号
    conditions = [(data['20_MA_slope'] > 0) & (data['100_MA_slope'] > 0) & (data['close'] > data['ma20']),
                 (data['20_MA_slope'] < 0) & (data['100_MA_slope'] < 0) & (data['close'] < data['ma20'])]
    choices = [1, -1]
    data['ma_slope_signal'] = np.select(conditions, choices, default=0) # 均线斜率信号 上升为1，下降为-1    
    
    # DIF与DEA的交叉  1.计算12日和26日的EMA  2.DIF=12日EMA-26日EMA  3.计算DIF的9日EMA, 即DEA  4.DIF与DEA的交叉
    data['macd_a']=MACD(data['close'])
    data['ema_dif'] = EMA(data['close'],12) - EMA(data['close'],26)
    data['ema_dea'] = EMA(data['ema_dif'],9)
    data['macd'] = data['ema_dif'] - data['ema_dea']
    # data['macd_signal'] = data['macd'].apply(lambda x: 1 if x > 0 else -1) # DIF与DEA的交叉信号 DIF>DEA为1 金叉，DIF<DEA为-1 死叉
    data['ema_dif_slope']=data['ema_dif'].rolling(window=10).apply(lambda x: (x[-1]-x[0])/10,raw=True) 
    data['ema_dea_slope']=data['ema_dea'].rolling(window=10).apply(lambda x: (x[-1]-x[0])/10,raw=True) 
    conditions=[(data['macd']>0) & (data['macd'].shift(1) < 0),(data['macd']<0) & (data['macd'].shift(1) > 0)]
    choices=[1,-1]
    data['macd_signal'] = np.select(conditions,choices,default=0)


    # RSI
    data['rsi14'] = RSI(data['close'],timeperiod=14) # 14日RSI
    # RSI quantile
    data['rsi14_25'] =data['rsi14'].expanding(min_periods=30).apply(lambda x: x.quantile(0.25))
    data['rsi14_50'] =data['rsi14'].expanding(min_periods=30).apply(lambda x: x.quantile(0.5))
    data['rsi14_75'] =data['rsi14'].expanding(min_periods=30).apply(lambda x: x.quantile(0.75))
    # # RSI超卖
    # data['rsi14_over_sell'] = data['rsi14'].apply(lambda x: 1 if x < 30 else 0) # RSI超卖信号 
    # # RSI超买
    # data['rsi14_over_buy'] = data['rsi14'].apply(lambda x: -1 if x > 70 else 0) # RSI超买信号
    # RSI趋势信号
    conditions=[
        (data['rsi14']<=data['rsi14_25']),
        (data['rsi14']>=data['rsi14_25']) & (data['rsi14']<data['rsi14_50']),
        (data['rsi14']>=data['rsi14_50']) & (data['rsi14']<data['rsi14_75']),
        (data['rsi14']>=data['rsi14_75'])
    ]
    choices=[2,1,-1,-2]
    data['rsi14_signal'] = np.select(conditions,choices,default=0)

    #KDJ 指标
    data['K'] = STOCH(data['high'], data['low'], data['close'],
                                fastk_period=9, slowk_period=3, slowk_matype=0,
                                slowd_period=3, slowd_matype=0,type='slowk')
    data['D'] = STOCH(data['high'], data['low'], data['close'],
                                fastk_period=9, slowk_period=3, slowk_matype=0,
                                slowd_period=3, slowd_matype=0,type='slowd')
    # 计算 J 值
    data['J'] = 3 * data['K'] - 2 * data['D']
    data['kdj_signal'] = np.where((data['K'] > data['D']) & (data['K'].shift(1) <= data['D'].shift(1)), 1, 
                          np.where((data['K'] < data['D']) & (data['K'].shift(1) >= data['D'].shift(1)), -1, 0))
    
    #WILLIAM指标
    # 以14日周期为例
    data['WR'] = WILLR(data['high'], data['low'], data['close'], timeperiod=14)

    # 生成买入和卖出信号
    data['wr_signal'] = np.where((data['WR'] < -80) & (data['WR'].shift(1) >= -80), 1, 
                            np.where((data['WR'] > -20) & (data['WR'].shift(1) <= -20), -1, 0))
    
    # BIAS乖离率指标
    data['bias_12']=BIAS(data['close'],timeperiod=12)
    # 设定买入和卖出信号的阈值
    buy_threshold = -6
    sell_threshold = 6
    # 生成买入和卖出信号
    data['bias_12_signal'] = np.where(data['bias_12'] < buy_threshold, 1,
                            np.where(data['bias_12'] > sell_threshold, -1, 0))
    
    # CCI指标
    data['cci_20'] = CCI(data['high'], data['low'], data['close'], timeperiod=20)
    # 设置买入和卖出信号的阈值
    buy_threshold = -100
    sell_threshold = 100

    # 生成买入和卖出信号
    data['cci_20_signal'] = np.where((data['cci_20'] < buy_threshold) & (data['cci_20'].shift(1) >= buy_threshold), 1,
                            np.where((data['cci_20'] > sell_threshold) & (data['cci_20'].shift(1) <= sell_threshold), -1, 0))
    
    #PSY指标
    # 计算12日PSY指标
    data['psy_12'] = PSY(data['close'], period=12)
    # 设置买入和卖出信号的阈值
    buy_threshold = 30
    sell_threshold = 70
    # 生成买入和卖出信号
    data['psy_12_signal'] = np.where(data['psy_12'] < buy_threshold, 1,
                            np.where(data['psy_12'] > sell_threshold, -1, 0))



    # 布林带
    # data['boll_upper'] = BBANDS(data['close'],timeperiod=20,nbdevup=2.0,nbdevdn=2.0,bandtype='upper') # 布林带上线
    # data['boll_lower'] = BBANDS(data['close'],timeperiod=20,nbdevup=2.0,nbdevdn=2.0,bandtype='lower') # 布林带下线
    # data['boll_middle'] = BBANDS(data['close'],timeperiod=20,nbdevup=2.0,nbdevdn=2.0,bandtype='middle') # 布林带中线
    # data['boll_width'] = (data['boll_upper'] - data['boll_lower']) / data['boll_middle']  # 布林带开口扩大
    # data['boll_width_diff'] = data['boll_width'].diff()
    # data['boll_width_signal'] = data['boll_width_diff'].apply(lambda x: -1 if x > 0 else 1) # 布林带开口扩大信号 开口扩大为1，代表上涨趋势结束，开口缩小为-1，代表下降趋势结束
    
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

