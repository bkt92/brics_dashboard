import streamlit as st
import numpy as np
import datetime

st.markdown("# Brazil")
st.write("This page provied detail statistical analysis about Brazil forex market")

d = st.date_input(
    "When's your birthday",
    datetime.date(2019, 7, 6))
st.write('Your birthday is:', d)