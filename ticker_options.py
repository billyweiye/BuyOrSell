import json 
import pandas as pd 
import yfinance as yf
import os
from datetime import datetime, timedelta
import streamlit as st


# 缓存文件路径
ETF_CACHE_FILE = "us_etf_cache.json"
CACHE_EXPIRY_DAYS = 7  # 缓存有效期为7天


def _load_etf_cache():
    """加载缓存的ETF数据"""
    if os.path.exists(ETF_CACHE_FILE):
        try:
            with open(ETF_CACHE_FILE, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
                cache_time = datetime.fromisoformat(cache_data.get('timestamp', '2000-01-01'))
                if datetime.now() - cache_time < timedelta(days=CACHE_EXPIRY_DAYS):
                    return cache_data.get('etfs', {})
        except (json.JSONDecodeError, ValueError, KeyError):
            pass
    return None


def _save_etf_cache(etf_dict):
    """保存ETF数据到缓存"""
    cache_data = {
        'timestamp': datetime.now().isoformat(),
        'etfs': etf_dict
    }
    try:
        with open(ETF_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Warning: Failed to save ETF cache: {e}")


def _fetch_etfs_from_yfinance():
    """使用 yfinance Lookup 获取美国市场的 ETF 列表"""
    etf_selections = {}
    
    try:
        # 使用 yfinance 的 Lookup 功能获取 ETF 列表
        lookup = yf.Lookup("ETF")  # 搜索 ETF 关键字
        etf_results = lookup.get_etf(count=250)  # 获取最多 250 个 ETF
        
        if etf_results is not None and not etf_results.empty:
            for _, row in etf_results.iterrows():
                symbol = row.get('symbol', '')
                name = row.get('name', '') or row.get('longname', '') or symbol
                if symbol:
                    display_name = f"{name} ({symbol})" if name and name != symbol else symbol
                    etf_selections[display_name] = symbol
                    
    except Exception as e:
        print(f"Error fetching ETFs from yfinance Lookup: {e}")
        
        # 尝试备用方法：使用预定义的 screener
        try:
            # 获取一些常见的 ETF screener 结果
            result = yf.screen("top_mutual_funds", size=100)
            if result and 'quotes' in result:
                for quote in result['quotes']:
                    symbol = quote.get('symbol', '')
                    name = quote.get('longName') or quote.get('shortName') or symbol
                    quote_type = quote.get('quoteType', '')
                    # 只添加 ETF 类型
                    if symbol and quote_type == 'ETF':
                        display_name = f"{name} ({symbol})" if name != symbol else symbol
                        etf_selections[display_name] = symbol
        except Exception as e2:
            print(f"Error with backup ETF fetch: {e2}")
    
    return etf_selections


def _get_fallback_etfs():
    """备用 ETF 列表，当 API 获取失败时使用"""
    return {
        # 贵金属 ETF
        "SPDR Gold Shares (GLD)": "GLD",
        "iShares Silver Trust (SLV)": "SLV",
        "Aberdeen Physical Platinum (PPLT)": "PPLT",
        
        # 大盘指数 ETF
        "Vanguard S&P 500 ETF (VOO)": "VOO",
        "SPDR S&P 500 ETF (SPY)": "SPY",
        "iShares Core S&P 500 ETF (IVV)": "IVV",
        "Invesco QQQ - 纳斯达克100 (QQQ)": "QQQ",
        "Vanguard Total Stock Market ETF (VTI)": "VTI",
        "iShares Russell 2000 ETF - 小盘股 (IWM)": "IWM",
        "SPDR Dow Jones Industrial ETF (DIA)": "DIA",
        
        # 行业 ETF
        "Technology Select Sector SPDR (XLK)": "XLK",
        "Financial Select Sector SPDR (XLF)": "XLF",
        "Health Care Select Sector SPDR (XLV)": "XLV",
        "Energy Select Sector SPDR (XLE)": "XLE",
        "Consumer Discretionary SPDR (XLY)": "XLY",
        "Consumer Staples SPDR (XLP)": "XLP",
        "Industrial Select SPDR (XLI)": "XLI",
        "Materials Select SPDR (XLB)": "XLB",
        "Utilities Select SPDR (XLU)": "XLU",
        "Real Estate Select SPDR (XLRE)": "XLRE",
        
        # 国际市场 ETF
        "iShares MSCI Emerging Markets (EEM)": "EEM",
        "Vanguard FTSE Emerging Markets (VWO)": "VWO",
        "iShares MSCI EAFE - 发达市场 (EFA)": "EFA",
        "iShares China Large-Cap (FXI)": "FXI",
        "KraneShares China Internet (KWEB)": "KWEB",
        
        # 债券 ETF
        "iShares 20+ Year Treasury Bond (TLT)": "TLT",
        "iShares 7-10 Year Treasury Bond (IEF)": "IEF",
        "iShares Investment Grade Corporate (LQD)": "LQD",
        "Vanguard Total Bond Market (BND)": "BND",
        
        # 大宗商品 ETF
        "United States Oil Fund (USO)": "USO",
        "United States Natural Gas Fund (UNG)": "UNG",
        "Invesco DB Commodity Index (DBC)": "DBC",
        
        # 波动率 ETF
        "iPath S&P 500 VIX Short-Term (VXX)": "VXX",
        
        # 杠杆 ETF
        "ProShares UltraPro QQQ 3x (TQQQ)": "TQQQ",
        "ProShares UltraPro Short QQQ 3x (SQQQ)": "SQQQ",
        "Direxion Semiconductor Bull 3X (SOXL)": "SOXL",
        "Direxion Semiconductor Bear 3X (SOXS)": "SOXS",
    }


@st.cache_data(ttl=86400)  # 缓存24小时
def us_etfs():
    """
    返回美国市场可交易的 ETF 列表
    优先从 yfinance API 获取，失败时使用缓存或备用列表
    """
    # 1. 首先尝试从本地缓存加载
    cached_etfs = _load_etf_cache()
    
    # 2. 如果缓存有效且数据量足够，直接返回
    if cached_etfs and len(cached_etfs) >= 50:
        return cached_etfs
    
    # 3. 尝试从 yfinance API 获取
    etf_selections = _fetch_etfs_from_yfinance()
    
    # 4. 如果 API 获取成功且数据量足够，保存到缓存
    if etf_selections and len(etf_selections) >= 20:
        _save_etf_cache(etf_selections)
        return etf_selections
    
    # 5. 如果 API 失败，尝试使用过期的缓存
    if cached_etfs:
        return cached_etfs
    
    # 6. 最后使用备用列表
    fallback = _get_fallback_etfs()
    _save_etf_cache(fallback)
    return fallback


#US
def us_stocks():
    stock_selections={}
    with open("us_stock_meta.json",'r') as f:
        stock_meta=json.load(f)
    for stock in stock_meta:
        stock_selections[stock.get("name")]=stock.get("ticker")
    
    return stock_selections

#CHINA
def china_stocks():
    stock_selections={}
    df=pd.read_csv("all_stock_list_china.csv") 
    df.dropna(subset='ticker',inplace=True)
    df=df.loc[df['ticker'].str.contains('.bj')==False]
    stock_meta=df.to_dict('records')
    for stock in stock_meta:
        stock_selections[stock.get("name")]=stock.get("ticker")
    
    return stock_selections


# HK
def hk_stocks():
    stock_selections={}
    df=pd.read_csv("stock_hk.csv") 
    df.dropna(subset='ticker',inplace=True)
    stock_meta=df.to_dict('records')
    for stock in stock_meta:
        stock_selections[stock.get("name")]=stock.get("ticker")
    
    return stock_selections
