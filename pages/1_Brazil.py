import streamlit as st
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import seaborn as sns

st.markdown("# Brazil")
st.write("This page provied detail statistical analysis about Brazil forex market")

# Plot the data series
col1_1, col2_1 = st.columns(2)

with col1_1:
    options = st.multiselect(
    'Indicates to display:',
    ['SMA100', 'EMA100', 'SMA20', 'EMA20'],
    ['SMA100'])
    
with col2_1:
    d1 = st.date_input(
    "Start date:",
    datetime.date.today()-relativedelta(months=+120))
    d2 = st.date_input(
    "End date:",
    datetime.date.today())
    
data = st.session_state['data']
data_returns = st.session_state['data_returns']

i100day_SMA = data[['BRL=X']].rolling(window=100).mean()
i100day_EMA = data[['BRL=X']].ewm(span=100, adjust=False).mean()
i20day_SMA = data[['BRL=X']].rolling(window=20).mean()
i20day_EMA = data[['BRL=X']].ewm(span=20, adjust=False).mean()

fig, ax = plt.subplots()
#figsize=(10,10)
ax.plot(data.loc[d1:d2, :].index, data.loc[d1:d2, 'BRL=X'], label='Idx')
if "SMA100" in options:
    ax.plot(i100day_SMA.loc[d1:d2, :].index, i100day_SMA.loc[d1:d2, 'BRL=X'], 
        label = '100-days SMA',linestyle= '--') 
if "EMA100" in options:
    ax.plot(i100day_EMA.loc[d1:d2, :].index, i100day_EMA.loc[d1:d2, 'BRL=X'], 
        label = '100-days SMA',linestyle= '--')         
if "SMA20" in options:
    ax.plot(i20day_SMA.loc[d1:d2, :].index, i20day_SMA.loc[d1:d2, 'BRL=X'], 
        label = '20-days SMA',linestyle= '--')
if "EMA20" in options:
    ax.plot(i20day_EMA.loc[d1:d2, :].index, i20day_EMA.loc[d1:d2, 'BRL=X'], 
        label = '20-days EMA',linestyle= ':', color = 'k')

ax.legend(loc='best')
ax.set_ylabel('BRL')

st.pyplot(fig)

fig1 = plt.figure()
sns.histplot(data = data_returns[['BRL=X']], kde = True)
#ax1.title('BRL Return')
st.pyplot(fig1)
