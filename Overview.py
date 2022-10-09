import streamlit as st
import numpy as np
import yfinance as yf
import pandas as pd
import time
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
from dateutil.relativedelta import relativedelta

st.title('BRICS Forex Overview 💹')
st.markdown("##### *This is overview page about the BRICS forex market*")

def data_download(tickers, period):
    yf_data = yf.Tickers(tickers)
    yf_data_hist = yf_data.history(period=period, interval = "1d");
    return pd.DataFrame(yf_data_hist["Close"])
    
# Download data
data = data_download('BRL=X,RUB=X,INR=X,CNY=X,ZAR=X', '12y')
    
current_price = data_download('BRL=X,RUB=X,INR=X,CNY=X,ZAR=X', '3d').dropna()
st.markdown("### Current rate and prediction (up/down compare to current price):")
col1_0, col2_0, col3_0, col4_0, col5_0 = st.columns(5)
col1_0.metric("BRL", np.round(current_price[['BRL=X']].iloc[-1].to_numpy(),2), "1%")
col2_0.metric("RUB", np.round(current_price[['RUB=X']].iloc[-1].to_numpy(),2), "-8%")
col3_0.metric("INR", np.round(current_price[['INR=X']].iloc[-1].to_numpy(),2), "4%")
col4_0.metric("CNY", np.round(current_price[['CNY=X']].iloc[-1].to_numpy(),2), "4%")
col5_0.metric("ZAR", np.round(current_price[['ZAR=X']].iloc[-1].to_numpy(),2), "4%")

st.markdown("### 1 USD exchange rate plot:")
 
# Plot the data series
col1_1, col2_1 = st.columns(2)

with col1_1:
    options = st.multiselect(
    'Choose currency to plot:',
    ['BRL', 'RUB', 'INR', 'CNY', 'ZAR'],
    ['BRL', 'RUB', 'INR', 'CNY', 'ZAR'])
tickers = ''
options = [option + '=X' for option in options]
    
with col2_1:
    d1 = st.date_input(
    "Start date:",
    datetime.date.today()-relativedelta(months=+12))
    d2 = st.date_input(
    "End date:",
    datetime.date.today())


st.line_chart(data[options].loc[d1:d2, :])

# Calculate return series 

data_returns = data.copy()
data_returns= data_returns.pct_change()
data_returns.replace([np.inf, - np.inf], np.nan, inplace = True)
data_returns = data_returns.dropna()

# Cumulated return
st.line_chart(data_returns.add(1).cumprod().loc[d1:d2, :])

# Correlation plot
col1_2, col2_2 = st.columns(2)

Ind_cov = data_returns.corr()
plt.figure(figsize=(7,7))
sns.color_palette("coolwarm", as_cmap=True)
mask = np.triu(np.ones_like(Ind_cov.corr()))
fig, ax = plt.subplots()
ax = sns.heatmap(Ind_cov, annot = True, center=0, cmap="coolwarm", mask=mask)

with col1_2:
    st.markdown("#### Covariance matrix")
    st.pyplot(fig)

with col2_2:
    st.markdown("#### Correlation matrix")
    st.pyplot(fig)