import streamlit as st
import numpy as np
import scipy as sp
import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import seaborn as sns
from my_func import *
import plotly.express as px

currency = 'INR=X'
st.markdown("# India")
st.write("This page provied detail statistical analysis about India USD/INR pair")

# Initialization data
# Download data
if 'data' not in st.session_state:
    st.session_state['data'] = data_download('BRL=X,RUB=X,INR=X,CNY=X,ZAR=X', '12y')
data = st.session_state['data']
# Calculate return series
if 'data_returns' not in st.session_state:
    st.session_state['data_returns'] = calc_return(data)
data_returns = st.session_state['data_returns']

with st.sidebar:
    st.markdown("##### Data cleaning: ")
    outlier = st.checkbox('Remove Outlier')    
    if outlier:
        data = data.dropna()
        data = data[(np.abs(sp.stats.zscore(data)) < 3).all(axis=1)]
        data_returns = calc_return(data)

# Plot the data series
col1_1, col2_1 = st.columns(2)

with col1_1:
    options = st.multiselect(
    'Indicators:',
    ['SMA100', 'EMA100', 'SMA20', 'EMA20'],
    ['SMA100'])
    
with col2_1:
    d1 = st.date_input(
    "Start date:",
    datetime.date.today()-relativedelta(months=+120))
    d2 = st.date_input(
    "End date:",
    datetime.date.today())

st.write("#### USD/INR Exchange rate:")
datanew = ma_calc(data.copy(),currency)

options.append(currency)
col1_2, col2_2 = st.columns([3, 1])
with col1_2:
    st.write("**Exchange rate:**")
    st.line_chart(datanew[options].loc[d1:d2, :])
with col2_2:
    st.write("**Return:**")
    st.line_chart(data_returns[[currency]].loc[d1:d2, :])

st.write("#### For return series:")

st.write("**Stationary test (ADF) with significant level of 0.05:**")
st.write(adf_test(data_returns[[currency]].loc[d1:d2, :],currency))
st.write("**Stationary test (KPSS) with significant level of 0.05**:")
st.write(kpss_test(data_returns[[currency]].loc[d1:d2, :],currency))
    
st.markdown("#### Histogram with boxplot:")
fig = px.histogram(data_returns[[currency]], x=currency, marginal="box")
st.plotly_chart(fig)
    #,use_container_width=True)
st.write("**Normal test (D’Agostino’s K-squared test) with significant level of 0.05:**")
st.write(normal_test(data_returns[[currency]].loc[d1:d2, :],currency))

st.markdown("#### Pacf and Acf plot:")
col1_3, col2_3 = st.columns(2)    
with col1_3:
    st.plotly_chart(create_corr_plot(data_returns[[currency]].loc[d1:d2, :]),use_container_width=True)
with col2_3:
    st.plotly_chart(create_corr_plot(data_returns[[currency]].loc[d1:d2, :], plot_pacf=True),use_container_width=True)    