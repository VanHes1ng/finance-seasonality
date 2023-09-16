# Import necessary libraries
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from scipy.signal import savgol_filter
from PIL import Image
import datetime

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

# Define a function to download S&P 500 data
def download_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

# Define a function to calculate weighted average of indicators
def calculate_weighted_avg(data, weights):
    avg = sum(data[indicator] * weight for indicator, weight in weights.items())
    return avg / sum(weights.values())

# Define a function to apply the Savitzky-Golay filter
def apply_savgol_filter(data, column, window_length, polyorder):
    smoothed_data = savgol_filter(data[column], window_length, polyorder)
    data[column] = smoothed_data

# Define a function to plot data using Plotly
def plot(x, y, title, line_color='blue', line_style='solid', is_histogram=False):
    y_column_name = y.name  # Get the name of the y column
    
    if is_histogram:
        data_fig = go.Figure(data=[go.Bar(x=x, y=y, marker=dict(color=line_color))])
    else:
        data_fig = go.Figure(data=[go.Line(x=x, y=y, mode='lines', line=dict(color=line_color, dash=line_style))])
    
    data_fig.update_layout(title=title)
    st.plotly_chart(data_fig, use_container_width=True, theme=None)

# Define a function to plot data with secondary y-axes
def plot_with_secondary_y(x, y1, y2, y3, title, y1_name='Primary Y-Axis', y2_name='Secondary Y-Axis', y3_name='Tertiary Y-Axis', y1_color='blue', y2_color='red', y3_color='green'):
    fig = go.Figure()
    
    fig = go.Figure(data=[go.Candlestick(x=x,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Adj Close'])])
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_layout(
        yaxis =dict(title=y1_name, titlefont=dict(color=y1_color), showgrid=False),
        yaxis2=dict(title=y2_name, titlefont=dict(color=y2_color), overlaying='y', side='right', showgrid=False)
    )
    
    fig.add_trace(go.Line(x=x, y=y2, mode='lines', name=y2_name, line=dict(color=y2_color), yaxis='y2'))
    
    fig.update_layout(
        yaxis3=dict(title=y3_name, titlefont=dict(color=y3_color), overlaying='y', side='left', showgrid=False, showticklabels=False)
    )
    
    fig.add_trace(go.Line(x=x, y=y3, mode='lines', name=y3_name, line=dict(color=y3_color), yaxis='y3'))
    
    fig.update_layout(title=title)
    st.plotly_chart(fig, use_container_width=True)




# Main content
st.header(':green[SPY] Economic Cycles', divider='rainbow')
st.subheader(':gray[Special Edition]')

# Sidebar
image = Image.open('pngegg.png')
st.sidebar.image(image)
st.sidebar.header("Settings")

# User Inputs
option = st.selectbox(
    'Plotting Indicator:',
    ('AVG', 'ROC', 'Sortino', 'Sharpe', 'MACD', 'Z Score'))

year = st.slider("Start Year", min_value=1960, max_value=2023, value=2022, step=1)
start_date = st.sidebar.date_input("Start Date", datetime.date(year, 1, 1), min_value=datetime.date(1960, 1, 1), max_value=datetime.date(2050, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.date(2050, 1, 1))


st.sidebar.subheader("Weights")
weights = {
    "ROC": st.sidebar.number_input('ROC Weight', 1, 100, 10),
    "Z Score": st.sidebar.number_input('Z Score Weight', 1, 100, 70),
    "Sharpe Ratio": st.sidebar.number_input('Sharpe Score Weight', 1, 100, 50),
    "Sortino Ratio": st.sidebar.number_input('Sortino Weight', 1, 100, 100),
    "MACD": st.sidebar.number_input('MACD Weight', 1, 100, 1)
}

st.sidebar.subheader("Smooth AVG")
window_length = st.sidebar.number_input('Window length', 1, 100, 40)
polyorder = st.sidebar.number_input('Polyorder', 1, 100, 6)



# Download S&P 500 data
ticker = "^GSPC"
data = download_data(ticker, start_date, end_date)




# Calculate daily returns
day_returns = data["Adj Close"].pct_change()

# Calculate negative returns
negative_returns = day_returns[day_returns < 0]

# Calculate indicators
data["ROC"] = (((data["Adj Close"] - data["Adj Close"].shift(16)) / data["Adj Close"].shift(16)) * 100)
data["SMA_15"] = data["Adj Close"].rolling(window=15).mean()
data["STD_15"] = data["Adj Close"].rolling(window=15).std()
data["Z Score"] = ((data["Adj Close"] - data["SMA_15"]) / data["STD_15"])
data["DR_27"] = day_returns.rolling(window=27).mean()
data["STD_27"] = day_returns.rolling(window=27).std()
data["Sharpe Ratio"] = (data["DR_27"] / data["STD_27"])
data["NDR_27"] = negative_returns.rolling(window=27).std()
data["Sortino Ratio"] = (data["DR_27"] / data["NDR_27"])
data["Sortino Ratio"].fillna(method='ffill', inplace=True)
data["SMA_12"] = data["Adj Close"].rolling(window=12).mean()
data["SMA_26"] = data["Adj Close"].rolling(window=26).mean()
data["MACD"] = ((data["SMA_12"] - data["SMA_26"]).rolling(window=9).mean())

# Calculate weighted average of indicators
data["AVG"] = calculate_weighted_avg(data, weights)
data["AVG_6"] = data["AVG"].rolling(window=6).mean()

# Apply the Savitzky-Golay filter to AVG and AVG_6
apply_savgol_filter(data, "AVG", window_length, polyorder)
apply_savgol_filter(data, "AVG_6", window_length, polyorder)




# Plot the main chart
if option == 'AVG':
    y2 = data["AVG"]
    y3 = data["AVG_6"]
elif option == 'ROC':
    y2 = data["ROC"]
    y3 = data["ROC"]
elif option == 'MACD':
    y2 = data["MACD"]
    y3 = data["MACD"]
elif option == 'Sharpe':
    y2 = data["Sharpe Ratio"]
    y3 = data["Sharpe Ratio"]
elif option == 'Sortino':
    y2 = data["Sortino Ratio"]
    y3 = data["Sortino Ratio"]
elif option == 'Z Score':
    y2 = data["Z Score"]
    y3 = data["Z Score"]

plot_with_secondary_y(data.index, data["Adj Close"], y2, y3, "SPY Cycles", y1_name="Closing Price", y2_name="AVG", y3_name="", y1_color="#2d3745", y2_color="#02b32e", y3_color="red")

# Style
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("### Indicators")

# Plot individual indicators
col1, col2 = st.columns(2, gap='small')

with col1:
   plot(data.index, data["Sharpe Ratio"], title="Sharpe Ratio", line_style='solid')
with col2:
   plot(data.index, data["Sortino Ratio"], title="Sortino Ratio", line_color='orange', line_style='solid')
with col1:
    plot(data.index, data["ROC"], title="Rate of Change", line_color='green', line_style='solid')
with col2: 
    plot(data.index, data["Z Score"], title="Z Score", line_color='purple', line_style='solid')

plot(data.index, data["MACD"], title="MACD", line_color='blue', is_histogram=True)

# Additional information
st.image(image)

st.write(
    "About\n",
    "\nS&P Cycles is not a financial advisor\n",
    "\nMade with Streamlit v1.26.0 https://streamlit.io\n",
    "\nCopyright 2023 Snowflake Inc. All rights reserved.\n"
)
