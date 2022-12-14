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
from statsmodels.tsa.arima.model import ARIMA

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
st.markdown("#### Current rate:")
col1_0, col2_0, col3_0, col4_0, col5_0 = st.columns(5)
col1_0.metric("BRL", np.round(current_price[['BRL=X']].iloc[-1].to_numpy(),2))
col2_0.metric("RUB", np.round(current_price[['RUB=X']].iloc[-1].to_numpy(),2))
col3_0.metric("INR", np.round(current_price[['INR=X']].iloc[-1].to_numpy(),2))
col4_0.metric("CNY", np.round(current_price[['CNY=X']].iloc[-1].to_numpy(),2))
col5_0.metric("ZAR", np.round(current_price[['ZAR=X']].iloc[-1].to_numpy(),2))
st.markdown("#### Prediction rate:")
col1_0, col2_0, col3_0, col4_0, col5_0 = st.columns(5)
# Parameter definition
o = {'BRL=X': (1,1,1), 'CNY=X': (1,1,1), 'INR=X':(1,1,1), \
    'ZAR=X': (1,0,1), 'RUB=X': (3,1,1)}
    
model_arima = {}
model_fit = {}
predictions = {}
history = {}
for i in data:
    history[i] = data[i].to_list()
    model_arima[i] = ARIMA(history[i], order=o[i])
    model_fit[i] = model_arima[i].fit()
    predictions[i] = model_fit[i].forecast()[0]
    
col1_0.metric("BRL", np.round(predictions['BRL=X'],2), np.round(predictions['BRL=X'] - current_price[['BRL=X']].iloc[-1].to_numpy()[0],4))
col2_0.metric("RUB", np.round(predictions['RUB=X'],2), np.round(predictions['RUB=X'] - current_price[['RUB=X']].iloc[-1].to_numpy()[0],4))
col3_0.metric("INR", np.round(predictions['INR=X'],2), np.round(predictions['INR=X'] - current_price[['INR=X']].iloc[-1].to_numpy()[0],4))
col4_0.metric("CNY", np.round(predictions['CNY=X'],2), np.round(predictions['CNY=X'] - current_price[['CNY=X']].iloc[-1].to_numpy()[0],4))
col5_0.metric("ZAR", np.round(predictions['ZAR=X'],2), np.round(predictions['ZAR=X'] - current_price[['ZAR=X']].iloc[-1].to_numpy()[0],4))

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

# Correlation plot
col1_3, col2_3 = st.columns(2)

Ind_corr1 = data.loc[d1:d2, :].corr()
plt.figure(figsize=(7,7))
sns.color_palette("coolwarm", as_cmap=True)
mask = np.triu(np.ones_like(Ind_corr1.corr()))
fig11, ax11 = plt.subplots()
ax11 = sns.heatmap(Ind_corr1, annot = True, center=0, cmap="coolwarm", mask=mask)

Ind_cov1 = data_returns.loc[d1:d2, :].cov()
plt.figure(figsize=(7,7))
sns.color_palette("coolwarm", as_cmap=True)
mask = np.triu(np.ones_like(Ind_cov1.corr()))
fig12, ax12 = plt.subplots()
ax12 = sns.heatmap(Ind_cov1, annot = True, center=0, cmap="coolwarm", mask=mask)

with col1_3:
    st.markdown("##### Covariance matrix")
    st.pyplot(fig12)

with col2_3:
    st.markdown("##### Correlation matrix")
    st.pyplot(fig11)

st.markdown("##### Basic statistical measures:")
    
describe_data = data.loc[d1:d2, :].describe()
describe_data.loc['median'] = data.loc[d1:d2, :].median()
kurtosis1 = pd.Series(sp.stats.kurtosis(data.loc[d1:d2, :].select_dtypes(exclude=['object']).to_numpy()))
kurtosis1.index = data.columns[0:]
describe_data.loc['kurtosis'] = kurtosis1
skewness1 = pd.Series(sp.stats.skew(data.loc[d1:d2, :].select_dtypes(exclude=['object']).to_numpy()))
skewness1.index = data.columns[0:]
describe_data.loc['skewness'] = skewness1

st.write(describe_data)


st.markdown("#### On return series:")
st.line_chart(data_returns[options].loc[d1:d2, :])
# Correlation plot
col1_3, col2_3 = st.columns(2)

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

with col1_3:
    st.markdown("##### Covariance matrix")
    st.pyplot(fig1)

with col2_3:
    st.markdown("##### Correlation matrix")
    st.pyplot(fig)

st.markdown("##### Basic statistical measures:")
    
describe_data_return = data_returns.loc[d1:d2, :].describe()
describe_data_return.loc['median'] = data_returns.loc[d1:d2, :].median()
kurtosis2 = pd.Series(sp.stats.kurtosis(data_returns.loc[d1:d2, :].select_dtypes(exclude=['object']).to_numpy()))
kurtosis2.index = data_returns.columns[0:]
describe_data_return.loc['kurtosis'] = kurtosis2
skewness2 = pd.Series(sp.stats.skew(data_returns.loc[d1:d2, :].select_dtypes(exclude=['object']).to_numpy()))
skewness2.index = data_returns.columns[0:]
describe_data_return.loc['skewness'] = skewness2

st.write(describe_data_return)