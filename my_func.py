import yfinance as yf
import pandas as pd
import numpy as np

# Download data from yfinance
def data_download(tickers, period):
    yf_data = yf.Tickers(tickers)
    yf_data_hist = yf_data.history(period=period, interval = "1d");
    return pd.DataFrame(yf_data_hist["Close"].dropna())

# Calculate the return series    
def calc_return(data):
    data_returns = data.copy()
    data_returns= data_returns.pct_change()
    data_returns.replace([np.inf, - np.inf], np.nan, inplace = True)
    return data_returns.dropna()
    
# Normal test with the significant level of 0.05
# Using D’Agostino’s K-squared test
def normal_test(data, name):
    k, p = stats.normaltest(data)
    if p > 0.05:
        print("The ", name, " series is normal distribution", p)
    else:
        print("The ", name, " series isn't a normal distribution", p)
        
def ma_calc(data,currency):
    data['SMA100'] = data[[currency]].rolling(window=100).mean()
    data['EMA100'] = data[[currency]].ewm(span=100, adjust=False).mean()
    data['SMA20'] = data[[currency]].rolling(window=20).mean()
    data['EMA20'] = data[[currency]].ewm(span=20, adjust=False).mean()
    return data