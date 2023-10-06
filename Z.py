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

col1,  col2,  col3  = st.columns([1, 3, 2])
col11, col22, col33 = st.columns([1, 3, 2])

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
with col22:
    st.subheader("VIX")
    st.line_chart(data, y = "VIX", color= "#d1a626", height = 300, use_container_width=True)
    st.line_chart(data, y = "Z", color="#26d128", height = 150, use_container_width=True)

with col33:
    st.subheader("CBOE Volatility Index")
    st.markdown("""VIX is the ticker symbol and the popular name for the Chicago Board Options Exchange's CBOE Volatility Index, 
                a popular measure of the stock market's expectation of volatility based on S&P 500 index options. 
                It is calculated and disseminated on a real-time basis by the CBOE, and is often referred to as the fear index or fear gauge.
                To summarize, 
                 VIX is a volatility index derived from S&P 500 options for the 30 days following the measurement date,
                 with the price of each option representing the market's expectation of 30-day forward-looking volatility.
                 The resulting VIX index formulation provides a measure of expected market volatility 
                 on which expectations of further stock market volatility in the near future might be based""")
    st.subheader("")
    st.markdown("**Z Scores of VIX**")
    st.markdown("""In statistics, the standard score is the number of standard deviations by which the value of a raw score 
                (i.e., an observed value or data point)
                 is above or below the mean value of what is being observed or measured. 
                Raw scores above the mean have positive standard scores, while those below the mean have negative standard scores.""")