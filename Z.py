# Import necessary libraries
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from scipy.signal import savgol_filter
from PIL import Image
import datetime
import numpy as np

# Define a function to download S&P 500 data
@st.cache_data(ttl=3600)
def download_data(ticker, start):
    data = yf.download(ticker, start= start)
    return data

def z_score(src, length):
    #The standard deviation is the square root of the average of the squared deviations from the mean, i.e., std = sqrt(mean(x)), where x = abs(a - a.mean())**2.
    basis = src.rolling(length).mean()
    x = np.abs(src - basis)**2
    stdv = np.sqrt(x.rolling(length).mean())
    z = (src-basis)/ stdv
    return z

col1, col2, col3 = st.columns([1, 3, 2])

# Inputs
with col2:
    year = st.slider("Start Year", 1960, 2030, 2023)
start_year = datetime.datetime(year, 1, 1)

# Get data
spy = download_data("^GSPC", start_year)
vix = download_data("^VIX", start_year)

data = pd.DataFrame()
data["SPY"] = spy["Adj Close"]
data["VIX"] = vix["Close"]

data["Z"] = z_score(data["VIX"], 20)


with col2:
    st.subheader("SPY")
    st.line_chart(data, y = "SPY", color="#26afd1",height = 300, use_container_width=True)

    st.subheader("VIX")
    st.line_chart(data, y = "VIX", color= "#d1a626", height = 300, use_container_width=True)
    st.line_chart(data, y = "Z", color="#26d128", height = 150, use_container_width=True)

with col3:
    st.markdown("SPY and VIX data")