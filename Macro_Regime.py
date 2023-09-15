# Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from fredapi import Fred

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
    start = '2001-01-01'
    end = '2025-01-01'
    data = pd.DataFrame(fred.get_series(
        ticker,
        observation_start=start,
        observation_end=end)).resample("M").mean() 
    return data

# Economic Indicators
indicator_list = ["CAPUTLG3311A2S",	
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
def plot(x, y1, y2, title, y1_name='Primary Y-Axis', y2_name='Secondary Y-Axis', y1_color='blue', y2_color='red'):
    fig = go.Figure()
    
    fig.add_trace(go.Line(x=x, y=y1, mode='lines', name=y1_name, line=dict(color=y1_color)))
    
    fig.update_layout(
        yaxis =dict(title=y1_name, titlefont=dict(color=y1_color), showgrid=False),
        yaxis2=dict(title=y2_name, titlefont=dict(color=y2_color), overlaying='y', side='right', showgrid=False)
    )
    
    fig.add_trace(go.Line(x=x, y=y2, mode='lines', name=y2_name, line=dict(color=y2_color), yaxis='y2'))
    
    fig.update_layout(title=title)
    st.plotly_chart(fig, use_container_width=True)


def roc(src, len, smooth):
    roc = ((src / src.shift(len) -1)*100).rolling(smooth).mean()
    return roc



data["ROC"] = roc(data["AVG"], 20, 5)

data["ROC1"] = data["ROC"].shift(1)

plot(data.index, data["ROC"], data["ROC1"], "ROC")

plot(data.index, data["AVG"], data["AVG"], "AVG")