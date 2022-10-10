import yfinance as yf
import pandas as pd
import numpy as np
import scipy as sp
from statsmodels.tsa.stattools import pacf, acf
import plotly.graph_objects as go

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
    k, p = sp.stats.normaltest(data)
    if p > 0.05:
        return "The "+ str(name)+ " series is normal distribution. "+ "p-value: "+ str(np.round(p,4))
    else:
        return "The "+ str(name)+ " series isn't normal distribution. "+ "p-value: "+ str(np.round(p,4))

# Calculate moving average        
def ma_calc(data,currency):
    data['SMA100'] = data[[currency]].rolling(window=100).mean()
    data['EMA100'] = data[[currency]].ewm(span=100, adjust=False).mean()
    data['SMA20'] = data[[currency]].rolling(window=20).mean()
    data['EMA20'] = data[[currency]].ewm(span=20, adjust=False).mean()
    return data

# Plot acf and pacf    
# From: https://community.plotly.com/t/plot-pacf-plot-acf-autocorrelation-plot-and-lag-plot/24108/2
def create_corr_plot(series, plot_pacf=False):
    corr_array = pacf(series.dropna(), alpha=0.05) if plot_pacf else acf(series.dropna(), alpha=0.05)
    lower_y = corr_array[1][:,0] - corr_array[0]
    upper_y = corr_array[1][:,1] - corr_array[0]

    fig = go.Figure()
    [fig.add_scatter(x=(x,x), y=(0,corr_array[0][x]), mode='lines',line_color='#3f3f3f') 
     for x in range(len(corr_array[0]))]
    fig.add_scatter(x=np.arange(len(corr_array[0])), y=corr_array[0], mode='markers', marker_color='#1f77b4',
                   marker_size=12)
    fig.add_scatter(x=np.arange(len(corr_array[0])), y=upper_y, mode='lines', line_color='rgba(255,255,255,0)')
    fig.add_scatter(x=np.arange(len(corr_array[0])), y=lower_y, mode='lines',fillcolor='rgba(32, 146, 230,0.3)',
            fill='tonexty', line_color='rgba(255,255,255,0)')
    fig.update_traces(showlegend=False)
    fig.update_xaxes(range=[-1,42])
    fig.update_yaxes(zerolinecolor='#000000')
    
    title='Partial Autocorrelation (PACF)' if plot_pacf else 'Autocorrelation (ACF)'
    fig.update_layout(title=title)
    return fig
    
# ADF test
from statsmodels.tsa.stattools import adfuller

def adf_test(timeseries, name):
    print("Results of Dickey-Fuller Test:")
    dftest = adfuller(timeseries, autolag="AIC")
    dfoutput = pd.Series(
        dftest[0:4],
        index=[
            "Test Statistic",
            "p-value",
            "#Lags Used",
            "Number of Observations Used",
        ],
    )
    for key, value in dftest[4].items():
        dfoutput["Critical Value (%s)" % key] = value

    #print(dfoutput)
    if dftest[1] > 0.05:
        return "The "+ str(name)+ " series isn't stationary. " + "p-value: " + str(np.round(dftest[1],4))
    else:
        return "The "+ str(name)+ " series is stationary. " + "p-value: " + str(np.round(dftest[1],4))
        
# KPSS test
from statsmodels.tsa.stattools import kpss

def kpss_test(timeseries,name):
    print("Results of KPSS Test:")
    kpsstest = kpss(timeseries, regression="c", nlags="auto")
    kpss_output = pd.Series(
        kpsstest[0:3], index=["Test Statistic", "p-value", "Lags Used"]
    )
    for key, value in kpsstest[3].items():
        kpss_output["Critical Value (%s)" % key] = value
    #print(kpss_output)
    if kpsstest[1] > 0.05:
        return "The "+ str(name)+ " series is stationary. " + "p-value: "+ str(np.round(kpsstest[1],4))
    else:
        return "The "+ str(name)+ " series isn't stationary. " + "p-value: " + str(np.round(kpsstest[1],4))