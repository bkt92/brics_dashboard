import streamlit as st
import numpy as np
import scipy as sp
import pandas as pd
import time
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
from dateutil.relativedelta import relativedelta
from my_func import *

st.title('BRICS Forex Overview 💹')
st.markdown("##### *This is overview page about the BRICS forex market*")

# Initialization data
# Download data
if 'data' not in st.session_state:
    st.session_state['data'] = data_download('BRL=X,RUB=X,INR=X,CNY=X,ZAR=X', '12y')
data = st.session_state['data']
# Calculate return series
if 'data_returns' not in st.session_state:
    st.session_state['data_returns'] = calc_return(data)
data_returns = st.session_state['data_returns']

# Current price and prediction
current_price = data_download('BRL=X,RUB=X,INR=X,CNY=X,ZAR=X', '3d').dropna()
st.markdown("#### Current rate and prediction (up/down compare to current price):")
col1_0, col2_0, col3_0, col4_0, col5_0 = st.columns(5)
col1_0.metric("BRL", np.round(current_price[['BRL=X']].iloc[-1].to_numpy(),2), "1%")
col2_0.metric("RUB", np.round(current_price[['RUB=X']].iloc[-1].to_numpy(),2), "-8%")
col3_0.metric("INR", np.round(current_price[['INR=X']].iloc[-1].to_numpy(),2), "4%")
col4_0.metric("CNY", np.round(current_price[['CNY=X']].iloc[-1].to_numpy(),2), "4%")
col5_0.metric("ZAR", np.round(current_price[['ZAR=X']].iloc[-1].to_numpy(),2), "4%")

with st.sidebar:
    st.markdown("##### Data cleaning: ")
    outlier = st.checkbox('Remove Outlier')    
    if outlier:
        data = data.dropna()
        data = data[(np.abs(sp.stats.zscore(data)) < 3).all(axis=1)]
        data_returns = calc_return(data)

st.markdown("#### 1 USD exchange rate plot:")
# Plot the data series
col1_1, col2_1 = st.columns(2)

with col1_1:
    options = st.multiselect(
    'Choose currency to plot:',
    ['BRL', 'RUB', 'INR', 'CNY', 'ZAR'],
    ['BRL', 'RUB', 'INR', 'CNY', 'ZAR'])
options = [option + '=X' for option in options]
    
with col2_1:
    d1 = st.date_input(
    "Start date:",
    datetime.date.today()-relativedelta(months=+120))
    d2 = st.date_input(
    "End date:",
    datetime.date.today())

st.line_chart(data[options].loc[d1:d2, :])

# Cumulated return plot
st.markdown("#### Cumulated return:")
st.line_chart(data_returns.add(1).cumprod().loc[d1:d2, :])

# Correlation plot
col1_2, col2_2 = st.columns(2)

Ind_corr = data_returns.loc[d1:d2, :].corr()
plt.figure(figsize=(7,7))
sns.color_palette("coolwarm", as_cmap=True)
mask = np.triu(np.ones_like(Ind_corr.corr()))
fig, ax = plt.subplots()
ax = sns.heatmap(Ind_corr, annot = True, center=0, cmap="coolwarm", mask=mask)


Ind_cov = data_returns.loc[d1:d2, :].cov()
plt.figure(figsize=(7,7))
sns.color_palette("coolwarm", as_cmap=True)
mask = np.triu(np.ones_like(Ind_cov.corr()))
fig1, ax1 = plt.subplots()
ax1 = sns.heatmap(Ind_cov, annot = True, center=0, cmap="coolwarm", mask=mask)

with col1_2:
    st.markdown("#### Covariance matrix")
    st.pyplot(fig1)

with col2_2:
    st.markdown("#### Correlation matrix")
    st.pyplot(fig)