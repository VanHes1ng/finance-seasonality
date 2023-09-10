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
end_date = st.sidebar.date_input("End Date", pd.to_datetime('2050-01-01'))

# Download S&P 500 data from Yahoo Finance
ticker = "^GSPC"
data = yf.download(ticker, start=start_date, end=end_date)

# Set the app title and sidebar description
day_returns = data["Close"].pct_change()

negative_returns = day_returns[day_returns < 0]

# Calculate ROC (Rate of Change)
data["ROC"] = (((data["Close"] - data["Close"].shift(16)) / data["Close"].shift(16)) * 100)


# Z-Score
# Calculate 15-day Simple Moving Average (SMA)
data["SMA_15"] = data["Close"].rolling(window=15).mean()
# Calculate 15-day Rolling Standard Deviation
data["STD_15"] = data["Close"].rolling(window=15).std()
# Calculate Z scores
data["Z Score"] = ((data["Close"] - data["SMA_15"])/data["STD_15"])

# Sharpe Ratio
# Calculate 27-day Simple Moving Average of daily returns(SMA)
data["DR_27"] = day_returns.rolling(window=27).mean()
# Calculate 27-day Rolling Standard Deviation
data["STD_27"] = day_returns.rolling(window=27).std()
# Calculate Rolling Sharpe
data["Sharpe Ratio"] = (data["DR_27"]/data["STD_27"])*10

# Calculate 27-day Simple Moving Average of negative daily returns(SMA)
data["NDR_27"] = negative_returns.rolling(window=27).std()
# Calculate Rolling Sortino
data["Sortino Ratio"] = (data["DR_27"]/data["NDR_27"])*10
# Fill NaN values in Sortino Ratio with the last valid value (forward-fill)
data["Sortino Ratio"].fillna(method='ffill', inplace=True)

# MACD
# Calculate 12-day Simple Moving Average (SMA)
data["SMA_12"] = data["Close"].rolling(window=12).mean()
# Calculate 26-day Simple Moving Average (SMA)
data["SMA_26"] = data["Close"].rolling(window=26).mean()
# MACD
data["MACD"] = ((data["SMA_12"]-data["SMA_26"]).rolling(window=9).mean())


# Define a function to plot data using Plotly
def plot(x, y, title, line_color='blue', line_style='solid', is_histogram=False):
    # Get the name of the y column
    y_column_name = y.name
    
    # Create a Plotly figure for the data
    if is_histogram:
        data_fig = go.Figure(data=[go.Bar(x=x, y=y, marker=dict(color=line_color))])
    else:
        data_fig = go.Figure(data=[go.Scatter(x=x, y=y, mode='lines', line=dict(color=line_color, dash=line_style))])
    
    # Set the title of the chart using the provided title
    data_fig.update_layout(title=title)
    data_fig.update_layout(width=1000,height=800)
    # Display the chart in the Streamlit app
    st.plotly_chart(data_fig)

data["AVG"] = (data["ROC"]+data["Z Score"]+data["Sharpe Ratio"]+data["Sortino Ratio"]+data["MACD"])/5
data["AVG_6"] = data["AVG"].rolling(window=6).mean()

def plot_with_secondary_y(x, y1, y2, y3, title, y1_name='Primary Y-Axis', y2_name='Secondary Y-Axis', y3_name='Tertiary Y-Axis', y1_color='blue', y2_color='red', y3_color='green'):
    # Create a Plotly figure
    fig = go.Figure()
    
    # Add the first trace (y1) to the primary y-axis
    fig.add_trace(go.Scatter(x=x, y=y1, mode='lines', name=y1_name, line=dict(color=y1_color)))
    
    # Create a secondary y-axis
    fig.update_layout(yaxis=dict(title=y1_name, titlefont=dict(color=y1_color), showgrid=True), 
                      yaxis2=dict(title=y2_name, titlefont=dict(color=y2_color), overlaying='y', side='right', showgrid=False))  # Hide gridlines on secondary y-axis
    
    # Add the second trace (y2) to the secondary y-axis
    fig.add_trace(go.Scatter(x=x, y=y2, mode='lines', name=y2_name, line=dict(color=y2_color), yaxis='y2'))
    
    # Create a tertiary y-axis
    fig.update_layout(yaxis3=dict(title=y3_name, titlefont=dict(color=y3_color), overlaying='y', side='left', showgrid=False, showticklabels=False))  # Hide gridlines on tertiary y-axis
    
    # Add the third trace (y3) to the tertiary y-axis
    fig.add_trace(go.Scatter(x=x, y=y3, mode='lines', name=y3_name, line=dict(color=y3_color), yaxis='y3'))
    
    # Set the title of the chart
    fig.update_layout(title=title)
    fig.update_layout(width=1100,height=900)
    # Display the chart in the Streamlit app
    st.plotly_chart(fig)

# Example usage with three y-series and three y-axes
plot_with_secondary_y(data.index, data["Close"], data["AVG"], data["AVG_6"], "SPY Cycles", y1_name="Closing Price", y2_name="AVG", y3_name="", y1_color="white", y2_color="turquoise", y3_color="red")

st.markdown("### Indicators")

plot(data.index, data["ROC"], title="Rate of Change", line_color='green', line_style='solid')
plot(data.index, data["Z Score"], title="Z Score", line_color='purple', line_style='solid')
plot(data.index, data["Sharpe Ratio"], title="Sharpe Ratio", line_style='solid')
plot(data.index, data["Sortino Ratio"], title="Sortino Ratio", line_color='orange', line_style='solid')
plot(data.index, data["MACD"], title="MACD", line_color='blue', is_histogram=True)

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🦈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)