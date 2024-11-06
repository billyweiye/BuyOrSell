import json 
import pandas as pd 


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
