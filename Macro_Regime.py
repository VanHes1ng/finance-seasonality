# Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from fredapi import Fred
import plotly.express as px

# Set up the Streamlit app configuration
st.set_page_config(
    page_title="Macro Regime",
    page_icon="🐉",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': "https://twitter.com/sxJEoRg7wwLR6ug",
        'Report a bug': "https://twitter.com/sxJEoRg7wwLR6ug",
        'About': "Macro Regime is not a financial advisor"
    }
)


# Initialize Fred API
fred = Fred(api_key="20256d454ab4cfe9d4a9672dff8337b0")  # Replace with your actual API key

def get_data(ticker):
    start = '2000-01-01'
    end = '2025-01-01'
    data = pd.DataFrame(fred.get_series(
        ticker,
        observation_start=start,
        observation_end=end)).resample("M").mean() 
    return data

# Economic Indicators
indicator_list = ["TCU",	
    "CCSA",	
    "INDPRO",	
    "JTSHIL",	
    "JTSJOL",	
    "MRTSSM44X72USS",	
    "NCBEILQ027S",	
    "PERMIT",	
    "STLFSI4",	
    "TEMPHELPS",	
    "TOTALSA",	
    "UMCSENT",
    "CPIAUCSL",
    "BSCICP03USM665S",
    "RSXFS",
    "CFNAI",
    "CSCICP03USM665S",
    "PCUOMFGOMFG",
    "NFCI",
    "BAMLH0A0HYM2EY",
    "T10Y2Y",
    "FEDFUNDS"]

data = pd.DataFrame()  # Create a dictionary to store data for each indicator

for ind in indicator_list:
    data[ind] = get_data(ind)

data["NFCI"] = data["NFCI"] *-1
data["BAMLH0A0HYM2EY"] = data["BAMLH0A0HYM2EY"] *-1
data["CCSA"] = data["CCSA"] *-1
data["STLFSI4"] = data["STLFSI4"] *-1
data["T10Y2Y"] = data["T10Y2Y"] *-1

# Fill NaN values with forward-fill
for ind, df in data.items():
    data[ind] = df.fillna(method='ffill')

data["AVG"] = data.sum(axis=1)

data["AVG"] = data["AVG"].div(len(indicator_list))

st.dataframe(data)


# Define a function to plot data using Plotly
def plot(x, y1, y2, title, range, y1_name='Primary Y-Axis', y2_name='Secondary Y-Axis', y1_color='blue', y2_color='red'):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=x, y=y1, mode='lines', name=y1_name, line=dict(color=y1_color)))

    fig.update_layout(
        yaxis=dict(title=y1_name, titlefont=dict(color=y1_color), showgrid=False, zeroline=True, range=range),
        yaxis2=dict(title=y2_name, titlefont=dict(color=y2_color), overlaying='y', side='right', showgrid=False, zeroline=True, range=range)
    )
    
    fig.add_trace(go.Scatter(x=x, y=y2, mode='lines', name=y2_name, line=dict(color=y2_color), yaxis='y2'))
    
    fig.update_layout(title=title)
    st.plotly_chart(fig, use_container_width=True)


def roc(src, len, smooth):
    roc = ((src / src.shift(len) -1)*100).rolling(smooth).mean()
    return roc


data["ROC"] = roc(data["AVG"], 4, 5)

data["ROC1"] = data["ROC"] - data["ROC"].shift(4)

plot(data.index, data["ROC"], data["ROC1"], "ROC", [-80, 120])


data["SPY"] = get_data("SP500")

plot(data.index, data["SPY"], data["AVG"], "SPY", [min(data["SPY"]), max(data["SPY"])])


for i in indicator_list:
    y_values = roc(data[i], 4, 5)
    x_values = y_values - y_values.shift(4)


# Create a DataFrame with the grid data
grid_data = {'x': x_values, 'y': y_values}
grid_data = pd.DataFrame(grid_data)

# Create a grid chart with only the last X and Y values
last_x = grid_data['x'].iloc[-1]
last_y = grid_data['y'].iloc[-1]

# Create a scatter plot using Plotly Express for the grid
fig = px.scatter(grid_data["x","y"], x='x', y='y', title='Grid with Zero at the Center')

# Customize the layout
fig.update_xaxes(range=[-100, 100])
fig.update_yaxes(range=[-100, 100])

# Add X and Y axes lines
fig.add_shape(
    type="line",
    x0=-100,
    y0=0,
    x1=100,
    y1=0,
    line=dict(color="gray", width=1)
)
fig.add_shape(
    type="line",
    x0=0,
    y0=-100,
    x1=0,
    y1=100,
    line=dict(color="gray", width=1)
)

# Create a separate trace for the zero marker using Plotly Express
zero_marker = px.scatter(x=[0], y=[0], text=['Zero'], title='Zero Marker')
zero_marker.update_traces(textfont=dict(size=12, color='red'))

# Append the zero marker trace to the original figure
for trace in zero_marker.data:
    fig.add_trace(trace)

# Streamlit app
st.title("Grid with Zero at the Center")
st.plotly_chart(fig)
