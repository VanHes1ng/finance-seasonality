# Import necessary libraries
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from scipy.signal import savgol_filter

# Set up the Streamlit app configuration
st.set_page_config(
    page_title="S&P Cycles",
    page_icon="🐉",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': "https://twitter.com/sxJEoRg7wwLR6ug",
        'Report a bug': "https://twitter.com/sxJEoRg7wwLR6ug",
        'About': "S&P Cycles is not a financial advisor"
    }
)

# Set the title for the Streamlit app
st.subheader("S&P500 Cycles")

# Create a sidebar for user settings
st.sidebar.header("Settings")

# User Inputs

# Allow the user to select a start date within the specified range
start_date = st.sidebar.date_input("Start Date", pd.to_datetime('2021-01-01'), min_value=pd.to_datetime('1960-01-01'), max_value=pd.to_datetime('2035-01-01'))

# Allow the user to select an end date
end_date = st.sidebar.date_input("End Date", pd.to_datetime('2050-01-01'))

st.sidebar.subheader("Weights")
roc_w = st.sidebar.number_input('ROC Weight', 1, 100, 1)
z_w   = st.sidebar.number_input('Z Score Weight', 1, 100, 1)
sr_w  = st.sidebar.number_input('Sharpe Score Weight', 1, 100, 1)
sor_w = st.sidebar.number_input('Sortino Weight', 1, 100, 1)
mac_w = st.sidebar.number_input('MACD Weight', 1, 100, 1)

st.sidebar.subheader("Smooth AVG")
your_window_length = st.sidebar.number_input('Window length', 1, 100, 30)
your_polyorder     = st.sidebar.number_input('Polyorder', 1, 100, 5)

# Download S&P 500 data from Yahoo Finance
ticker = "^GSPC"
data = yf.download(ticker, start=start_date, end=end_date)

# Calculate daily returns
day_returns = data["Close"].pct_change()

# Calculate negative returns
negative_returns = day_returns[day_returns < 0]

# Calculate Rate of Change (ROC)
data["ROC"] = (((data["Close"] - data["Close"].shift(16)) / data["Close"].shift(16)) * 100)

# Calculate Z-Score
data["SMA_15"] = data["Close"].rolling(window=15).mean()
data["STD_15"] = data["Close"].rolling(window=15).std()
data["Z Score"] = ((data["Close"] - data["SMA_15"]) / data["STD_15"])

# Calculate Sharpe Ratio
data["DR_27"] = day_returns.rolling(window=27).mean()
data["STD_27"] = day_returns.rolling(window=27).std()
data["Sharpe Ratio"] = (data["DR_27"] / data["STD_27"])

# Calculate Sortino Ratio
data["NDR_27"] = negative_returns.rolling(window=27).std()
data["Sortino Ratio"] = (data["DR_27"] / data["NDR_27"])
data["Sortino Ratio"].fillna(method='ffill', inplace=True)

# Calculate MACD
data["SMA_12"] = data["Close"].rolling(window=12).mean()
data["SMA_26"] = data["Close"].rolling(window=26).mean()
data["MACD"] = ((data["SMA_12"] - data["SMA_26"]).rolling(window=9).mean())

# Define a function to plot data using Plotly
def plot(x, y, title, line_color='blue', line_style='solid', is_histogram=False):
    y_column_name = y.name  # Get the name of the y column
    
    if is_histogram:
        data_fig = go.Figure(data=[go.Bar(x=x, y=y, marker=dict(color=line_color))])
    else:
        data_fig = go.Figure(data=[go.Scatter(x=x, y=y, mode='lines', line=dict(color=line_color, dash=line_style))])
    
    data_fig.update_layout(title=title, width=1000, height=800)
    st.plotly_chart(data_fig)

# Calculate a weighted average of indicators
data["AVG"] = (data["ROC"] * roc_w + data["Z Score"] * z_w + data["Sharpe Ratio"] ** sr_w + data["Sortino Ratio"] * sor_w + data["MACD"] * mac_w) / 5
data["AVG_6"] = data["AVG"].rolling(window=6).mean()


# Apply the Savitzky-Golay filter to AVG and AVG_6
data["AVG"] = savgol_filter(data["AVG"], your_window_length, your_polyorder)
data["AVG_6"] = savgol_filter(data["AVG_6"], your_window_length, your_polyorder)

# Define a function to plot data with secondary y-axes
def plot_with_secondary_y(x, y1, y2, y3, title, y1_name='Primary Y-Axis', y2_name='Secondary Y-Axis', y3_name='Tertiary Y-Axis', y1_color='blue', y2_color='red', y3_color='green'):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=x, y=y1, mode='lines', name=y1_name, line=dict(color=y1_color)))
    
    fig.update_layout(
        yaxis=dict(title=y1_name, titlefont=dict(color=y1_color), showgrid=True),
        yaxis2=dict(title=y2_name, titlefont=dict(color=y2_color), overlaying='y', side='right', showgrid=False)
    )
    
    fig.add_trace(go.Scatter(x=x, y=y2, mode='lines', name=y2_name, line=dict(color=y2_color), yaxis='y2'))
    
    fig.update_layout(
        yaxis3=dict(title=y3_name, titlefont=dict(color=y3_color), overlaying='y', side='left', showgrid=False, showticklabels=False)
    )
    
    fig.add_trace(go.Scatter(x=x, y=y3, mode='lines', name=y3_name, line=dict(color=y3_color), yaxis='y3'))
    
    fig.update_layout(title=title, width=1100, height=900)
    st.plotly_chart(fig)

# Example usage with three y-series and three y-axes
plot_with_secondary_y(data.index, data["Close"], data["AVG"], data["AVG_6"], "SPY Cycles", y1_name="Closing Price", y2_name="AVG", y3_name="", y1_color="white", y2_color="turquoise", y3_color="red")

st.markdown("### Indicators")

# Plot individual indicators
plot(data.index, data["ROC"], title="Rate of Change", line_color='green', line_style='solid')
plot(data.index, data["Z Score"], title="Z Score", line_color='purple', line_style='solid')
plot(data.index, data["Sharpe Ratio"], title="Sharpe Ratio", line_style='solid')
plot(data.index, data["Sortino Ratio"], title="Sortino Ratio", line_color='orange', line_style='solid')
plot(data.index, data["MACD"], title="MACD", line_color='blue', is_histogram=True)
