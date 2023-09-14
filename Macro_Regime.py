# Import necessary libraries
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
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

