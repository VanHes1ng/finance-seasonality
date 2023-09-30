import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import datetime

# Page Configurations
st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_icon= "〰️")

# Define a function to download S&P 500 data
def download_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

# Titles
st.header("Seasonality Performance", divider="gray")

st.sidebar.header("Settings")

# User Inputs
ticker = st.sidebar.selectbox(
    'Choose a Ticker:', ('^GSPC', 'ETH-USD', 'BTC-USD', "^IXIC"))

year = st.slider("Start Year", min_value=1960, max_value=2023, value=2022, step=1)
start_date = st.sidebar.date_input("Start Date", datetime.date(year, 1, 1), min_value=datetime.date(1960, 1, 1), max_value=datetime.date(2050, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.date(2050, 1, 1))

start_date = st.sidebar.date_input("Start Date", datetime.date(year, 7, 6), min_value=datetime.date(1960, 1, 1), max_value=datetime.date(2035, 1, 1))

# Download S&P 500 data from Yahoo Finance
data = download_data(ticker, start_date, end_date)

# Set the app title and sidebar description
if ticker == "^GSPC":
    ticker = "S&P500"
if ticker == "^IXIC":
    ticker = "NASDAQ"

log_returns = data["Adj Close"].pct_change()

# Resample to monthly frequency and calculate monthly returns
monthly_returns = log_returns.resample('M').apply(lambda x: (1 + x).prod() - 1)

# Drop the NaN value at the beginning (since there's no previous month)
monthly_returns = monthly_returns.dropna()

y=(1 + log_returns).cumprod()

# Add a drop-down box to select a month
selected_month = st.selectbox("Select a Month", range(1, 13), index=8)  # Default to September (index 8)

# Filter data for the selected month
selected_month_data = data[data.index.month == selected_month]

# Plot the cumulative returns chart
ret = go.Figure()

# Create and style traces
ret.add_trace(go.Line(x=data.index, y=y,
                      line=dict(color='gray', width=2)))

# Highlight the selected month with a light gray background
ret.add_shape(
    go.layout.Shape(
        type="rect",
        x0=selected_month_data.index[0],
        x1=selected_month_data.index[-1],
        y0=0,
        y1=max(y),
        fillcolor="rgba(220, 220, 220, 0.5)",
        layer="below",
        line=dict(width=0),
    )
)

ret.update_layout(title=ticker + " Cumulative Returns Chart")

# Create a DataFrame for monthly returns
monthly_returns_df = pd.DataFrame({'Date': monthly_returns.index, 'Monthly_Return': monthly_returns.values})

# Extract year and month from the Date column
monthly_returns_df['Year'] = monthly_returns_df['Date'].dt.year
monthly_returns_df['Month'] = monthly_returns_df['Date'].dt.month

# Calculate monthly avg returns
monthly_percentage_changes = monthly_returns_df.groupby('Month')['Monthly_Return'].mean()*100

# Pivot the DataFrame to create a heatmap
heatmap_data = monthly_returns_df.pivot_table(index='Year', columns='Month', values='Monthly_Return')



# Customize the color scale and axis labels for the heatmap
heatmap_data.columns = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
heatmap_data.index.name = "Year"


# Create the heatmap using Plotly Express
heatmap_fig = px.imshow(np.round(heatmap_data*100,2),
                       labels=dict(x="Month", y="Year", color="Monthly Return"),
                       title=f"Heatmap of Monthly Returns for {ticker}",
                       color_continuous_scale=["red", "white", "green"],
                       zmin=-30,
                       zmax=30, text_auto=True, height=1000)

# Customize the color scale and axis labels for the heatmap
heatmap_fig.update_xaxes(tickvals=list(range(12)), ticktext=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
heatmap_fig.update_yaxes(title_text="Year")



# Create a line plot for monthly percentage changes
percentage_changes_fig = go.Figure()

percentage_changes_fig.add_trace(go.Bar(x=heatmap_data.columns, y=np.round(monthly_percentage_changes,2),
    marker_color='rgb(132, 172, 209)'))

percentage_changes_fig.update_layout(title=f"                 SEASONALITY {ticker}", xaxis_title="Month", yaxis_title="Change (%)", height=700)
percentage_changes_fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='black')

# Streamlit integration
st.plotly_chart(ret, use_container_width=True)
st.plotly_chart(heatmap_fig, use_container_width=True)
st.plotly_chart(percentage_changes_fig, use_container_width=True)
