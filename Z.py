# Import necessary libraries
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from scipy.signal import savgol_filter
from PIL import Image
import datetime
import numpy as np

# Set up the Streamlit app configuration
st.set_page_config(
    page_title="SPY Volatility",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': "https://twitter.com/sxJEoRg7wwLR6ug",
        'Report a bug': "https://twitter.com/sxJEoRg7wwLR6ug",
        'About': "This site is not a financial advisor"
    }
)

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

def space(number):
    if number == 1:
        st.write("#")
    if number == 2: 
        st.write("#")
        st.write("#")
    if number == 3: 
        st.write("#")
        st.write("#")    
        st.write("#")
    if number == 4: 
        st.write("#")
        st.write("#")    
        st.write("#")
        st.write("#")

col1,  col2,  col3, _  = st.columns([1, 4, 3, 0.5])
col11, col22, col33, _ = st.columns([1, 4, 3, 0.5])


# Inputs
with col3:
    space(4)
    st.markdown("""
            This system is designed to provide valuable insights into future market movements,
            enabling users to make informed decisions regarding their investments without directly executing trades. 
            It leverages the VIX (CBOE Volatility Index) as a key indicator for predicting trends, 
            in the SPY (S&P 500 ETF) market.

            When the VIX indicates decreasing volatility, suggesting a more stable market environment, 
            the system implies that SPY may experience an upward trend. 
            This information aids users in considering investment strategies that align with potential market improvements.
            Conversely, when the VIX suggests increasing volatility, indicating potential market turbulence, 
            the system helps users consider strategies that account for potential market downturns.""")
    year = st.slider("Select Start Year:", 1960, 2023, 2020)
start_year = datetime.datetime(year, 1, 1)

# Get data
spy = download_data("^GSPC", start_year)
vix = download_data("^VIX", start_year)

data = pd.DataFrame()
data["SPY"] = spy["Adj Close"]
data["VIX"] = vix["Close"]

data["Z"] = z_score(data["VIX"], 20)


with col2:
    st.title("SPY volatility direction")
    st.subheader("SPY")
    st.line_chart(data, y = "SPY", color="#26afd1",height = 300, use_container_width=True)

with col22:
    st.markdown("***")
    st.subheader("VIX")
    st.line_chart(data, y = "VIX", color= "#d1a626", height = 300, use_container_width=True)
    st.line_chart(data, y = "Z", color="#26d128", height = 250, use_container_width=True)
    
    st.markdown("***")
    colu1, colu2 = st.columns([1, 1.5])
    with colu1:
        z_sc = np.round(data["Z"].iloc[-1], 2)
        delta = np.round(data["Z"].iloc[-1] - data["Z"].iloc[-2], 2)
        st.metric(label="Z-Score", value=z_sc, delta=delta,
        delta_color="normal")
    with colu2:
        if z_sc > 0 and delta < 0:
            st.write("Z score positive and decrising")

with col33:
    st.markdown("***")
    st.subheader("CBOE Volatility Index")
    st.markdown("""VIX is the ticker symbol and the popular name for the Chicago Board Options Exchange's CBOE Volatility Index, 
                a popular measure of the stock market's expectation of volatility based on S&P 500 index options. 
                It is calculated and disseminated on a real-time basis by the CBOE, and is often referred to as the fear index or fear gauge.
                To summarize, 
                 VIX is a volatility index derived from S&P 500 options for the 30 days following the measurement date,
                 with the price of each option representing the market's expectation of 30-day forward-looking volatility.
                 The resulting VIX index formulation provides a measure of expected market volatility 
                 on which expectations of further stock market volatility in the near future might be based""")
    space(2)
    st.markdown("**Z Scores of VIX**")
    st.markdown("""Z-score is a statistical measurement that describes a value's relationship to the mean of a group of values. 
                Z-score is measured in terms of standard deviations from the mean. If a Z-score is 0, 
                it indicates that the data point's score is identical to the mean score. 
                A Z-score of 1.0 would indicate a value that is one standard deviation from the mean.
                Z-scores may be positive or negative, with a positive value indicating the score is above the mean 
                 and a negative score indicating it is below the mean.""")

with col22:
    st.markdown("***")
    st.write(
        "About\n",
        "\nThis site is not a financial advisor\n",
        "\nMade with Streamlit v1.26.0 https://streamlit.io\n",
        "\nCopyright 2023 Snowflake Inc. All rights reserved.\n"
    )
