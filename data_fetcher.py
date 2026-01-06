import yfinance as yf

def fetch_stock_data(ticker, period='1y', interval='1d'):
    # 获取最近1年的股票数据
    try:
        # 核心下载行
        stock_data = yf.download(ticker, period=period, interval=interval)
        
        if stock_data is None or stock_data.empty:
            return None

        # 数据清洗逻辑
        stock_data = stock_data.dropna()
        
        if stock_data.empty:
            return None

        # 处理多层索引 (yfinance 在某些版本或特定参数下会返回 MultiIndex)
        if hasattr(stock_data.columns, 'nlevels') and stock_data.columns.nlevels > 1:
            stock_data.columns = stock_data.columns.droplevel(1)
            
        if 'Adj Close' in stock_data.columns:
            stock_data.rename(columns={'Close':'Original Close','Adj Close':'Close'}, inplace=True)
        stock_data.columns = [x.lower() for x in stock_data.columns]
        return stock_data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None
