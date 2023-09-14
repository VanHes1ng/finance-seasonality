# Import necessary libraries
import streamlit as st

import pandas as pd
import plotly.graph_objects as go
from PIL import Image
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


def get_data(ticker):
    start = '2022-01-31'
    end = '2023-01-31'
    monthyl_yield_curve = pd.DataFrame(fred.get_series(
        ticker,
        observation_start=start,
        observation_end=end)).resample("M")


# Economic Indicators
list = [	"	TCU,	"	
	"	CCSA,	"	
	"	EXHOSLUSM495S,	"	
	"	INDPRO,	"	
	"	JTSHIL,	"	
	"	JTSJOL,	"	
	"	MRTSSM44X72USS,	"	
	"	NCBEILQ027S,	"	
	"	PERMIT,	"	
	"	STLFSI4,	"	
	"	TEMPHELPS,	"	
	"	TOTALSA,	"	
	"	EXHOSLUSM495S,	"	
	"	UMCSENT	"	]

for ind in list:
    data = get_data(ind)

st.write(data)