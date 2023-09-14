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
    start = '2000-01-31'
    end = '2023-01-31'
    data = pd.DataFrame(fred.get_series(
        ticker,
        observation_start=start,
        observation_end=end)).resample("W").mean() 
    return data

# Economic Indicators
indicator_list = ["TCU",	
    "CCSA",	
    "EXHOSLUSM495S",	
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
    "UMCSENT"]

data = {}  # Create a dictionary to store data for each indicator

for ind in indicator_list:
    data[ind] = get_data(ind)

# Now you can access the data dictionary for each indicator
st.write(data)
print(data)