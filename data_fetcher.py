import yfinance as yf

def fetch_stock_data(ticker,period='1y',interval='1d'):
    # 获取最近1年的股票数据
    try:
        stock_data = yf.download(ticker, period=period, interval=interval)
        stock_data = stock_data.dropna()
        stock_data.columns = stock_data.columns.droplevel(1)
        stock_data.rename(columns={'Close':'Original Close','Adj Close':'Close'},inplace=True)
        stock_data.columns = [x.lower() for x in stock_data.columns]
        return stock_data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None
