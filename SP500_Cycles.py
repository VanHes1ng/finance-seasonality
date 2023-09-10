import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from scipy.interpolate import CubicSpline
import numpy as np
import matplotlib.pyplot as plt
import monthly_returns_heatmap as mrh
import calendar

st.subheader("S&P500 Cycles")

st.sidebar.header("Settings")

# User Inputs
start_date = st.sidebar.date_input("Start Date", pd.to_datetime('1990-01-01'),min_value=pd.to_datetime('1960-01-01'), max_value=pd.to_datetime('2035-01-01'))
end_date = st.sidebar.date_input("End Date", pd.to_datetime('2024-01-01'))

# Download S&P 500 data from Yahoo Finance
ticker = "^GSPC"
data = yf.download(ticker, start=start_date, end=end_date)

# Set the app title and sidebar description
day_returns = data["Close"].pct_change()

# ROC (16)
roc = ((data["Close"]-data["Close"][-16])/data["Close"][-16])*100
roc = (go.Figure(data=[go.Line(x=data.index, y=roc)]))

st.plotly_chart(roc)