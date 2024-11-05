# 技术指标
from talib import abstract 


#Overlap Studies Indexes 通常用于衡量趋势
def BBANDS (close, timeperiod=5, nbdevup=2.0, nbdevdn=2.0, matype=0,bandtype='upper'):
  '''
  close:收盘价
  timeperiod:周期
  matype:平均方法(bolling线的middle线 = MA，用于设定哪种类型的MA)
  MA_Type: 0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3 (Default=SMA)
  bandtype -> str: upper, middle, lower
  '''
  upper,middle,lower=abstract.BBANDS(close, timeperiod, nbdevup, nbdevdn, matype)
  if bandtype=='upper':
    return upper
  elif bandtype=='middle':
    return middle
  elif bandtype=='lower':
    return lower
  else:
    raise Exception ('BandtypeNotSupported')

def MA (close, timeperiod=30,matype=0):
  '''
  移动平均
  close:收盘价
  timeperiod:周期
  matype:平均方法(bolling线的middle线 = MA，用于设定哪种类型的MA)
  MA_Type: 0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3 (Default=SMA)
  '''
  return abstract.MA(close, timeperiod,matype)


def EMA (close, timeperiod=30):
  '''
  指数移动平均
  '''
  return abstract.EMA(close, timeperiod)

def DEMA (close, timeperiod=30):
  '''
  双移动平均线 DEMA = 2*EMA-EMA(EMA)
  '''
  return abstract.DEMA(close, timeperiod)

def KAMA (close, timeperiod=30):
  '''
  考夫曼自适应移动平均线
  '''
  return abstract.KAMA(close, timeperiod)

def MAVP (close, periods, minperiod=2.0, maxperiod=30, matype=0,):
  '''
  Moving average with variable period
  '''
  return abstract.MAVP(close, periods, minperiod, maxperiod, matype)

def HT_TRENDLINE (close):
  '''
  Hilbert Transform - Instantaneous Trendline
  '''
  return abstract.HT_TRENDLINE(close)

def MIDPOINT (close, timeperiod=14):
  '''
  MidPoint over period
  '''
  return abstract.MIDPOINT(close,timeperiod)

def MIDPRICE (high, low, timeperiod=14):
  '''
  Midpoint Price over period
  '''
  return abstract.MIDPRICE(high, low, timeperiod)

def SAR (high, low, acceleration=0, maximum=0):
  '''
  Parabolic SAR
  '''
  return abstract.SAR(high, low, acceleration, maximum)
  
def SAREXT (high, low, startvalue=0, offsetonreverse=0, accelerationinitlong=0, accelerationlong=0, accelerationmaxlong=0, accelerationinitshort=0, accelerationshort=0, accelerationmaxshort=0):
  '''
  Parabolic SAR - Extended
  '''
  return abstract.SAREXT(high, low, startvalue, offsetonreverse, accelerationinitlong, accelerationlong, accelerationmaxlong, accelerationinitshort, accelerationshort, accelerationmaxshort)

def SMA (close, timeperiod=30):
  '''
  Simple Moving Average
  '''
  return abstract.SMA(close, timeperiod)

def T_Three(close, timeperiod=5, vfactor=0):
  '''
  Triple Exponential Moving Average (T3)
  '''
  return abstract.T3(close, timeperiod, vfactor)

def TEMA (close, timeperiod=30):
  '''
  Triple Exponential Moving Average
  '''
  return abstract.TEMA(close, timeperiod)

def TRIMA (close, timeperiod=30):
  '''
  Triangular Moving Average
  '''
  return abstract.TRIMA(close, timeperiod)

def WMA (close, timeperiod=30):
  '''
  Weighted Moving Average
  '''
  return abstract.WMA(close, timeperiod)


# Momentum Indicators 通常用于衡量动量
def ADX (high, low, close, timeperiod=14):
  '''
  平均趋向指数 Average Directional Movement Index
  high:最高价；low:最低价；close：收盘价；timeperiod：时间周期
  '''
  return abstract.ADX(high, low, close, timeperiod)

def ADXR (high, low, close, timeperiod=14):
  '''
  平均趋向指数的趋向指数 Average Directional Movement Index Rating
  high:最高价；low:最低价；close：收盘价；timeperiod：时间周期
  '''
  return abstract.ADXR(high, low, close, timeperiod)

def APO (close, fastperiod=12, slowperiod=26, matype=0):
  '''
  价格震荡指数  Absolute Price Oscillator
  close：收盘价；fastperiod:快周期； slowperiod：慢周期
  '''
  return abstract.APO(close, fastperiod, slowperiod, matype)

def AROON (high, low, timeperiod=14,type='down'):
  '''
  阿隆指标 Aroon
  high:最高价；low:最低价；close：收盘价；timeperiod：时间周期, type: up | down 
  '''
  aroondown, aroonup = abstract.AROON(high, low, timeperiod)
  if type=='down':
    return aroondown
  elif type=='up':
    return aroonup
  else:
    raise Exception("TypeError")

def AROONOSC (high, low, timeperiod=14):
  '''
  阿隆振荡 Aroon Oscillator
  '''
  return abstract.AROONOSC(high, low, timeperiod)

def BOP (open, high, low, close):
  '''
  均势指标 Balance Of Power
  '''
  return abstract.BOP(open, high, low, close)

def CCI (high, low, close, timeperiod=14):
  '''
  顺势指标 Commodity Channel Index
  '''
  return abstract.CCI(high, low, close, timeperiod)

def CMO (close, timeperiod=14):
  '''
  钱德动量摆动指标 Chande Momentum Oscillator
  '''
  return abstract.CMO(close, timeperiod)

def DX (high, low, close, timeperiod=14):
  '''
  动向指标或趋向指标 Directional Movement Index
  '''
  return abstract.DX(high, low, close, timeperiod)

def MACD (close, fastperiod=12, slowperiod=26, signalperiod=9,type='macd'):
  '''
  平滑异同移动平均线 Moving Average Convergence/Divergence
  high:最高价；low:最低价；close：收盘价；fastperiod:快周期； slowperiod：慢周期 , type: 'macd','signal','hist'
  '''
  macd, macdsignal, macdhist= abstract.MACD(close, fastperiod, slowperiod, signalperiod)
  if type=='macd':
    return macd
  elif type=='signal':
    return macdsignal
  elif type=='hist':
    return macdhist
  else:
    raise Exception("TypeError")
def MACDEXT (close, fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9, signalmatype=0,type='macd'):
  '''
  MA类型下的MACD MACD with controllable MA type
  '''
  macd, macdsignal, macdhist =abstract.MACDEXT(close, fastperiod, fastmatype, slowperiod, slowmatype, signalperiod, signalmatype)
  if type=='macd':
    return macd
  elif type=='signal':
    return macdsignal
  elif type=='hist':
    return macdhist
  else:
    raise Exception("TypeError") 

def MACDFIX (close, signalperiod=9,type='macd'):
  '''
  Moving Average Convergence/Divergence Fix 12/26
  '''
  macd, macdsignal, macdhist = MACDFIX(close, signalperiod)
  if type=='macd':
    return macd
  elif type=='signal':
    return macdsignal
  elif type=='hist':
    return macdhist
  else:
    raise Exception("TypeError") 

def MFI (high, low, close, volume, timeperiod=14):
  '''
  资金流量指标 Money Flow Index
  '''
  return abstract.MFI(high, low, close, volume, timeperiod)

def MINUS_DI (high, low, close, timeperiod=14):
  '''
  DMI 中的DI指标 负方向指标 Minus Directional Indicator
  '''
  return abstract.MINUS_DI(high, low, close, timeperiod)

def MINUS_DM(high, low, timeperiod=14):
  '''
  上升动向值 Minus Directional Movement
  '''
  return abstract.MINUS_DM(high, low, timeperiod)

def MOM (close, timeperiod=10):
  '''
  上升动向值 Momentum
  '''
  return abstract.MOM(close, timeperiod)

def PLUS_DI (high, low, close, timeperiod=14):
  '''
  Plus Directional Indicator
  '''
  return abstract.PLUS_DI(high, low, close, timeperiod)

def PLUS_DM (high, low, timeperiod=14):
  '''
  Plus Directional Movement
  '''
  return abstract.PLUS_DM(high, low, timeperiod)

def PPO (close, fastperiod=12, slowperiod=26, matype=0):
  '''
  价格震荡百分比指数 Percentage Price Oscillator
  '''
  return abstract.PPO(close, fastperiod=12, slowperiod=26, matype=0)

def ROC(close, timeperiod=10):
  '''
  变动率指标 Rate of change : ((price/prevPrice)-1)*100
  '''
  return abstract.ROC(close, timeperiod)

def ROCP (close, timeperiod=10):
  '''
  变动百分比 Rate of change Percentage: (price-prevPrice)/prevPrice
  '''
  return abstract.ROCP(close, timeperiod)

def ROCR (close, timeperiod=10):
  '''
  变动百分率  Rate of change ratio: (price/prevPrice)
  '''
  return abstract.ROCR(close, timeperiod)

def ROCR100 (close, timeperiod=10):
  '''
  变动百分率（*100） Rate of change ratio 100 scale: (price/prevPrice)*100
  '''
  return abstract.ROCR100(close, timeperiod)

def RSI (close, timeperiod=14):
  '''
  相对强弱指数 Relative Strength Index
  这个指数的值在0-100之间，通常认为超过70为超买，低于30为超卖
  '''
  return abstract.RSI(close, timeperiod)

def STOCH(high, low, close, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0,type='slowk'):
  '''
  随机指标,俗称KD Stochastic
  这个指数的值在0-100之间，通常认为超过80为超买，低于20为超卖
  '''
  slowk, slowd = abstract.STOCH(high, low, close, fastk_period, slowk_period, slowk_matype, slowd_period, slowd_matype)
  if type=='slowk':
    return slowk
  elif type=='slowd':
    return slowd
  else:
    raise Exception("TypeError")

def STOCHF (high, low, close, fastk_period=5, fastd_period=3, fastd_matype=0,type='fastk'):
  '''
  快速随机指标 Stochastic Fast
  '''
  fastk, fastd = STOCHF(high, low, close, fastk_period, fastd_period, fastd_matype)
  if type=='fastk':
    return fastk
  elif type=='fastd':
    return fastd
  else:
    raise Exception("TypeError")
  
def STOCHRSI (close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0 , type='fastk'):
  '''
  随机相对强弱指数 Stochastic Relative Strength Index
  '''
  fastk, fastd = STOCHRSI(close, timeperiod, fastk_period, fastd_period, fastd_matype)
  if type=='fastk':
    return fastk
  elif type=='fastd':
    return fastd
  else:
    raise Exception("TypeError")

def TRIX (close, timeperiod=30):
  '''
  1-day Rate-Of-Change (ROC) of a Triple Smooth EMA
  '''
  return abstract.TRIX(close, timeperiod)

def ULTOSC (high, low, close, timeperiod1=7, timeperiod2=14, timeperiod3=28):
  '''
  终极波动指标 Ultimate Oscillator
  '''
  return abstract.ULTOSC(high, low, close, timeperiod1, timeperiod2, timeperiod3)

def WILLR (high, low, close, timeperiod=14):
  '''
  威廉指标 Williams' %R
  '''
  return abstract.WILLR(high, low, close, timeperiod)

def BIAS(close,timeperiod=12):
  return (close - close.rolling(timeperiod, min_periods=timeperiod).mean())/ close.rolling(timeperiod, min_periods=timeperiod).mean()*100

def RANK(close,timeperiod=250):
  if len(close)>timeperiod:
    rank= [i.rank()[-1] for i in close.rolling(timeperiod,min_periods=timeperiod)]
    rank[:(timeperiod-1)]=[np.nan]*(timeperiod-1)
    return rank
  else:
    return [np.nan]*len(close)
  

def PSY(close, period=12):
    # 计算上涨天数
    up_days = (close.diff() > 0).rolling(window=period).sum()
    # 计算PSY值
    psy = (up_days / period) * 100
    return psy

# Volume Indicators 通常用于衡量交易量
def AD(high, low, close, volume):
  '''
  Chaikin A/D Line 累积/派发线（Accumulation/Distribution Line）
  Marc Chaikin提出的一种平衡交易量指标，以当日的收盘价位来估算成交流量，用于估定一段时间内该证券累积的资金流量。
  A/D = 昨日A/D + 多空对比 * 今日成交量 多空对比 = [（收盘价- 最低价） - （最高价 - 收盘价）] / （最高价 - 最低价)
  '''
  return abstract.AD(high, low, close, volume)

def ADOSC (high, low, close, volume, fastperiod=3, slowperiod=10):
  '''
  Chaikin A/D Oscillator Chaikin震荡指标
  将资金流动情况与价格行为相对比，检测市场中资金流入和流出的情况
  fastperiod A/D - slowperiod A/D
  '''
  return abstract.ADOSC(high, low, close, volume, fastperiod, slowperiod)

def OBV (close, volume):
  '''
  On Balance Volume 能量潮
  Joe Granville提出，通过统计成交量变动的趋势推测股价趋势
  '''
  return abstract.OBV(close, volume)




# Volatility Indicators   通常用于衡量波动性
def ATR (high, low, close, timeperiod=14):
  '''
  Average True Range真实波动幅度均值
  真实波动幅度均值（ATR)是 以 N 天的指数移动平均数平均後的交易波动幅度。 计算公式：一天的交易幅度只是单纯地 最大值 - 最小值。
  而真实波动幅度则包含昨天的收盘价，若其在今天的幅度之外：
  真实波动幅度 = max(最大值,昨日收盘价) − min(最小值,昨日收盘价) 真实波动幅度均值便是「真实波动幅度」的 N 日 指数移动平均数。

  '''
  return abstract.ATR(high, low, close, timeperiod)

def NATR (high, low, close, timeperiod=14):
  '''
  Normalized Average True Range归一化波动幅度均值
  '''
  return abstract.NATR(high, low, close, timeperiod)

def TRANGE (high, low, close):
  '''
  True Range
  '''
  return abstract.TRANGE(high, low, close)
 
