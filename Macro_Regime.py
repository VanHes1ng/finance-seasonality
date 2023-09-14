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
    "EXHOSLUSM495S",	
    "UMCSENT",
    "CPIAUCSL",
    "PCUOMFGOMFG",
    "RSXFS",
    "CSCICP03USM665S",
    "NFCI",
    "BAMLH0A0HYM2EY"]

data = pd.DataFrame()  # Create a dictionary to store data for each indicator

for ind in indicator_list:
    data[ind] = get_data(ind)

data["NFCI"] = data["NFCI"] *-1
data["BAMLH0A0HYM2EY"] = data["BAMLH0A0HYM2EY"] *-1
data["CCSA"] = data["CCSA"] *-1
data["STLFSI4"] = data["STLFSI4"] *-1

st.dataframe(data)


# Define a function to plot data using Plotly
def plot(x, y, title, line_color='blue', line_style='solid', is_histogram=False):
    y_column_name = y.name  # Get the name of the y column
    
    if is_histogram:
        data_fig = go.Figure(data=[go.Bar(x=x, y=y, marker=dict(color=line_color))])
    else:
        data_fig = go.Figure(data=[go.Scatter(x=x, y=y, mode='lines+markers', line=dict(color=line_color, dash=line_style))])
    
    data_fig.update_layout(title=title)
    st.plotly_chart(data_fig, use_container_width=True, theme=None)

