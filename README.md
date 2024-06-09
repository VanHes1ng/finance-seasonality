
The provided Python code creates an interactive web application using Streamlit to analyze and visualize the seasonality performance of various financial assets. Here's a detailed breakdown of the code:

#### 1. Imports and Initial Setup

```python
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import datetime
```

- **streamlit**: For creating the web app.
- **yfinance**: For downloading financial data.
- **pandas**: For data manipulation.
- **plotly.graph_objects & plotly.express**: For creating interactive visualizations.
- **numpy**: For numerical operations.
- **datetime**: For date handling.

#### 2. Streamlit Page Configuration

```python
st.set_page_config(page_title="Seasonality", layout="wide", initial_sidebar_state="expanded", page_icon="📈")
st.header("Seasonality Performance", divider="gray")
st.sidebar.header("Seasonality")
```

- **st.set_page_config**: Configures the page with a title, layout, and icon.
- **st.header**: Sets the main header of the app.
- **st.sidebar.header**: Sets the sidebar header.

#### 3. User Inputs

```python
ticker = st.sidebar.selectbox('Ticker:', ('^GSPC', 'ETH-USD', 'BTC-USD', "^IXIC"))
max_value = 2035
year = st.slider("Start Year", min_value=1960, max_value=max_value, value=2000, step=1)
```

- **st.sidebar.selectbox**: Dropdown for selecting a financial asset.
- **st.slider**: Slider for selecting the start year for analysis.

#### 4. Data Downloading

```python
@st.cache_data
def download_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

data = download_data(ticker, datetime.date(year, 1, 1), datetime.date(max_value, 1, 1))
```

- **@st.cache_data**: Caches the data download function to improve performance.
- **download_data**: Function to download data from Yahoo Finance.
- **data**: Downloads data based on the selected ticker and date range.

#### 5. Adjusting Ticker Names

```python
if ticker == "^GSPC":
    ticker = "S&P500"
if ticker == "^IXIC":
    ticker = "NASDAQ"
```

- Adjusts the ticker names for display purposes.

#### 6. Calculating Returns

```python
log_returns = data["Adj Close"].pct_change()
monthly_returns = log_returns.resample('M').apply(lambda x: (1 + x).prod() - 1)
monthly_returns = monthly_returns.dropna()
y = (1 + log_returns).cumprod()
```

- **log_returns**: Calculates daily log returns.
- **monthly_returns**: Resamples daily returns to monthly and calculates monthly returns.
- **y**: Computes cumulative returns over time.

#### 7. Cumulative Returns Chart

```python
ret = go.Figure()
ret.add_trace(go.Scatter(x=data.index, y=y, mode='lines', name='Cumulative Returns', line=dict(color='gray', width=2)))
ret.add_trace(go.Scatter(x=data.index, y=y, mode='lines', fill='tozeroy', fillcolor='rgba(220, 220, 220, 0.5)', line=dict(color='rgba(255, 255, 255, 0)')))
ret.update_layout(title=ticker + " Cumulative Returns Chart")
```

- **go.Figure**: Creates a new Plotly figure.
- **go.Scatter**: Adds line traces for cumulative returns.
- **ret.update_layout**: Updates the layout of the chart with a title.

#### 8. Monthly Returns Heatmap

```python
monthly_returns_df = pd.DataFrame({'Date': monthly_returns.index, 'Monthly_Return': monthly_returns.values})
monthly_returns_df['Year'] = monthly_returns_df['Date'].dt.year
monthly_returns_df['Month'] = monthly_returns_df['Date'].dt.month
monthly_percentage_changes = monthly_returns_df.groupby('Month')['Monthly_Return'].mean() * 100
heatmap_data = monthly_returns_df.pivot_table(index='Year', columns='Month', values='Monthly_Return')
heatmap_data.columns = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
heatmap_data.index.name = "Year"
heatmap_fig = px.imshow(np.round(heatmap_data * 100, 2), labels=dict(x="Month", y="Year", color="Monthly Return"), title=f"Heatmap of Monthly Returns for {ticker}", color_continuous_scale=["red", "white", "green"], text_auto=True, height=1000)
heatmap_fig.update_xaxes(tickvals=list(range(12)), ticktext=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
heatmap_fig.update_yaxes(title_text="Year")
```

- **monthly_returns_df**: Creates a DataFrame for monthly returns.
- **monthly_percentage_changes**: Calculates average monthly returns.
- **heatmap_data**: Pivots the DataFrame to create heatmap data.
- **heatmap_fig**: Creates the heatmap using Plotly Express with custom labels and color scales.

#### 9. Average Monthly Returns Histogram

```python
percentage_changes_fig = go.Figure()
percentage_changes_fig.add_trace(go.Bar(x=heatmap_data.columns, y=np.round(monthly_percentage_changes * 100, 2), orientation='v', marker=go.bar.Marker(color=monthly_percentage_changes, colorscale="Greens", colorbar=dict(title="value"), line=dict(color="rgb(0, 0, 0)", width=1))))
percentage_changes_fig.update_layout(title_text='Average monthly performance', height=500)
percentage_changes_fig.update_xaxes(title_text="Avg monthly returns")
percentage_changes_fig.add_hline(y=0)
percentage_changes_fig.add_annotation(text=("@VanHelsing"), showarrow=False, x=1, y=0.1, xref='paper', yref='paper', xanchor='right', yanchor='bottom', font=dict(size=12, color="grey"), align="left")
```

- **percentage_changes_fig**: Creates a new Plotly figure for the histogram.
- **go.Bar**: Adds bar traces for average monthly returns.
- **percentage_changes_fig.update_layout**: Updates the layout with a title and height.
- **percentage_changes_fig.update_xaxes**: Updates x-axis labels.
- **percentage_changes_fig.add_hline**: Adds a horizontal line at y=0.
- **percentage_changes_fig.add_annotation**: Adds an annotation for credit.

#### 10. Streamlit Integration

```python
st.plotly_chart(ret, use_container_width=True)
st.plotly_chart(heatmap_fig, use_container_width=True)
st.plotly_chart(percentage_changes_fig, use_container_width=False)
```

- **st.plotly_chart**: Renders the Plotly charts in the Streamlit app.

#### 11. Footer Information

```python
st.write(
    "About\n",
    "\nSeasonality Performance is not a financial advisor\n",
    "\nCopyright 2023 Snowflake Inc. All rights reserved.\n"
)
```

- Adds footer information with a disclaimer and copyright notice.

link to the app:
https://seasonalityasset.streamlit.app/
