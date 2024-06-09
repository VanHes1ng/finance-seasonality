import streamlit as st

#-------------------------------------------------------------------------------------------------------
# Page Configurations
#-------------------------------------------------------------------------------------------------------

st.set_page_config(page_title = "About", layout="wide", initial_sidebar_state="expanded", page_icon= "@")

# Titles
st.header("About Seasonality", divider="gray")

st.write("""
### Seasonality Performance Web Application

The Seasonality Performance web application is an interactive tool designed to analyze and visualize the seasonal patterns in the performance of various financial assets.

#### Key Features:

1. **Interactive Interface**:
   - **Ticker Selection**: Choose from assets like S&P 500 (^GSPC), Ethereum (ETH-USD), Bitcoin (BTC-USD), and NASDAQ (^IXIC).
   - **Start Year Selection**: Adjust the start year for analysis using a slider.

2. **Data Fetching**:
   - Pulls historical data from Yahoo Finance based on user-selected asset and date range.

3. **Return Calculations**:
   - **Daily Log Returns**: Calculates daily returns.
   - **Monthly Returns**: Resamples daily returns to monthly.
   - **Cumulative Returns**: Computes cumulative returns over time.

4. **Visualizations**:
   - **Cumulative Returns Chart**: Shows the growth of the selected asset over time.
   - **Monthly Returns Heatmap**: Displays monthly returns across years to identify seasonal trends.
   - **Average Monthly Returns Histogram**: Shows average returns for each month.

5. **Educational Content**:
   - Disclaimers and information about the non-advisory nature of the tool.

#### Purpose and Benefits:

- **Seasonal Analysis**: Helps investors understand asset performance during specific times of the year.
- **Historical Performance Tracking**: Assists in predicting future asset behavior based on past performance.
- **User-Friendly**: Interactive elements and visualizations make complex data accessible.""")