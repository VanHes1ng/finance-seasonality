# Import necessary libraries
import streamlit as st
import pandas as pd
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import plotly.express as px
import plotly.figure_factory as ff

# Function to fetch historical stock price data from Yahoo Finance
def fetch_stock_data(symbol, start_date, end_date):
    df = yf.download(symbol, start=start_date, end=end_date)
    return df

# Function to preprocess data and create features
def preprocess_data(df):
    # Create a column for predicting price increases
    df['Price_Up'] = df['Close'] > df['Close'].shift(-1)
    df['Price_Up'] = df['Price_Up'].astype(int)
    
    # Create a column for predicting price decreases
    df['Price_Down'] = df['Close'] < df['Close'].shift(-1)
    df['Price_Down'] = df['Price_Down'].astype(int)
    
    return df

# Function to build and train a logistic regression model for price increase
def build_logistic_regression_model_up(X_train, y_train):
    model = LogisticRegression()
    model.fit(X_train, y_train)
    return model

# Function to build and train a logistic regression model for price decrease
def build_logistic_regression_model_down(X_train, y_train):
    model = LogisticRegression()
    model.fit(X_train, y_train)
    return model

# Main Streamlit app
def main():
    st.title("SPY Stock Price Prediction with Logistic Regression")
    
    # Sidebar inputs
    start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2010-01-01"))
    end_date = st.sidebar.date_input("End Date", pd.to_datetime("2021-12-31"))
    
    # Fetch historical stock price data
    st.sidebar.write("Fetching data... (This may take a moment)")
    df = fetch_stock_data("SPY", start_date, end_date)
    
    # Preprocess data
    df = preprocess_data(df)
    
    # Select features and targets
    X = df[['Open', 'High', 'Low', 'Volume']]
    y_up = df['Price_Up']
    y_down = df['Price_Down']
    
    # Split data into training and testing sets for price increase prediction
    X_train_up, X_test_up, y_train_up, y_test_up = train_test_split(X, y_up, test_size=0.2, random_state=42)
    
    # Split data into training and testing sets for price decrease prediction
    X_train_down, X_test_down, y_train_down, y_test_down = train_test_split(X, y_down, test_size=0.2, random_state=42)
    
    # Build and train the logistic regression models
    model_up = build_logistic_regression_model_up(X_train_up, y_train_up)
    model_down = build_logistic_regression_model_down(X_train_down, y_train_down)
    
    # Model evaluation for price increase prediction
    y_pred_up = model_up.predict(X_test_up)
    accuracy_up = accuracy_score(y_test_up, y_pred_up)
    
    st.write("## Model Evaluation for Price Increase Prediction")
    st.write(f"Accuracy: {accuracy_up:.2f}")
    
    st.write("## Classification Report for Price Increase Prediction")
    st.write(classification_report(y_test_up, y_pred_up))
    
    # Confusion matrix for price increase prediction
    cm_up = confusion_matrix(y_test_up, y_pred_up)
    
    # Visualize confusion matrix as a Plotly heatmap for price increase prediction
    st.write("### Confusion Matrix Heatmap for Price Increase Prediction")
    fig_cm_up = ff.create_annotated_heatmap(
        z=cm_up,
        x=['Predicted 0', 'Predicted 1'],
        y=['Actual 0', 'Actual 1'],
        colorscale='Blues'
    )
    fig_cm_up.update_layout(xaxis_title='Predicted', yaxis_title='Actual')
    st.plotly_chart(fig_cm_up)
    
    # Model evaluation for price decrease prediction
    y_pred_down = model_down.predict(X_test_down)
    accuracy_down = accuracy_score(y_test_down, y_pred_down)
    
    st.write("## Model Evaluation for Price Decrease Prediction")
    st.write(f"Accuracy: {accuracy_down:.2f}")
    
    st.write("## Classification Report for Price Decrease Prediction")
    st.write(classification_report(y_test_down, y_pred_down))
    
    # Confusion matrix for price decrease prediction
    cm_down = confusion_matrix(y_test_down, y_pred_down)
    
    # Visualize confusion matrix as a Plotly heatmap for price decrease prediction
    st.write("### Confusion Matrix Heatmap for Price Decrease Prediction")
    fig_cm_down = ff.create_annotated_heatmap(
        z=cm_down,
        x=['Predicted 0', 'Predicted 1'],
        y=['Actual 0', 'Actual 1'],
        colorscale='Blues'
    )
    fig_cm_down.update_layout(xaxis_title='Predicted', yaxis_title='Actual')
    st.plotly_chart(fig_cm_down)
    
    # Visualize stock price data
    st.write("## SPY Stock Price Data")
    fig_stock_price = px.line(df, x=df.index, y='Close', title='SPY Stock Price')
    st.plotly_chart(fig_stock_price)
    
if __name__ == "__main__":
    main()
