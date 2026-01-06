from data_fetcher import fetch_stock_data
import pandas as pd

def debug_fetch():
    ticker = '000001.SZ'
    print(f"Fetching data for {ticker}...")
    try:
        data = fetch_stock_data(ticker, period='1y', interval='1d')
        if data is not None:
            print("Fetch successful")
            print("Columns:", data.columns)
            print("Head:\n", data.head())
        else:
            print("Data is None")
    except Exception as e:
        print(f"Fetch failed: {e}")

if __name__ == "__main__":
    debug_fetch()
