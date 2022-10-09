import streamlit as st
import numpy as np
import yfinance as yf
import pandas as pd
import time
import seaborn as sns
import matplotlib.pyplot as plt

st.title('BRICS Forex Overview 💹')
st.markdown("##### *This is overview page about the BRICS forex market*")

st.markdown("### Exchange rate plot:")
def data_download(tickers, period):
    yf_data = yf.Tickers(tickers)
    yf_data_hist = yf_data.history(period=period, interval = "1d");
    return pd.DataFrame(yf_data_hist["Close"])
 
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
    period = st.selectbox('Time Period: ', ['1mo', '1y', '5y', '10y'], index = 3)
data = data_download('BRL=X,RUB=X,INR=X,CNY=X,ZAR=X', period)
st.line_chart(data[options])

# Calculate return series 

data_returns = data.copy()
data_returns= data_returns.pct_change()
data_returns.replace([np.inf, - np.inf], np.nan, inplace = True)
data_returns = data_returns.dropna()

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