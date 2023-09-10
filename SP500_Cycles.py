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

# Set the title for the Streamlit app
st.subheader("S&P500 Cycles")

# Create a sidebar for user settings
st.sidebar.header("Settings")

# User Inputs
# Allow the user to select a start date within the specified range
start_date = st.sidebar.date_input("Start Date", pd.to_datetime('1990-01-01'), min_value=pd.to_datetime('1960-01-01'), max_value=pd.to_datetime('2035-01-01'))

# Allow the user to select an end date
end_date = st.sidebar.date_input("End Date", pd.to_datetime('2024-01-01'))

# Download S&P 500 data from Yahoo Finance
ticker = "^GSPC"
data = yf.download(ticker, start=start_date, end=end_date)

# Set the app title and sidebar description
day_returns = data["Close"].pct_change()

# Calculate ROC (Rate of Change)
data["ROC"] = ((data["Close"] - data["Close"].shift(16)) / data["Close"].shift(16)) * 100


# Z-Score
# Calculate 15-day Simple Moving Average (SMA)
data["SMA_15"] = data["Close"].rolling(window=15).mean()
# Calculate 15-day Rolling Standard Deviation
data["STD_15"] = data["Close"].rolling(window=15).std()
# Calculate Z scores
data["Z_15"] = (data["Close"] - data["SMA_15"])/data["STD_15"]


# Define a function to plot data using Plotly
def plot(x, y):
    # Get the name of the y column
    y_column_name = y.name
    
    # Create a Plotly figure for the data
    data_fig = go.Figure(data=[go.Scatter(x=x, y=y)])
    
    # Set the title of the chart using the y column name
    data_fig.update_layout(title=f"{y_column_name} chart")
    
    # Display the chart in the Streamlit app
    st.plotly_chart(data_fig)

# Plot the closing price data
plot(data.index, data["Close"])

# Plot the ROC data
plot(data.index, data["ROC"])

# Plot the Z data
plot(data.index, data["Z_15"])