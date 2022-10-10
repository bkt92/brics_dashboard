import streamlit as st
import numpy as np

st.markdown("# South Africa")
st.write("This page provied detail statistical analysis about South Africa forex market")

# Initialization data
# Download data
if 'data' not in st.session_state:
    st.session_state['data'] = data_download('BRL=X,RUB=X,INR=X,CNY=X,ZAR=X', '12y')
# Calculate return series
if 'data_returns' not in st.session_state:
    data_returns = data.copy()
    data_returns= data_returns.pct_change()
    data_returns.replace([np.inf, - np.inf], np.nan, inplace = True)
    data_returns = data_returns.dropna()
    st.session_state['data_returns'] = data_returns
# Get data
data = st.session_state['data']
data_returns = st.session_state['data_returns']
