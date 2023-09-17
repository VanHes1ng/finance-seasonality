# Import necessary libraries
import streamlit as st
import pandas as pd
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Function to fetch historical stock price data from Yahoo Finance
def fetch_stock_data(symbol, start_date, end_date):
    df = yf.download(symbol, start=start_date, end=end_date)
    return df

# Function to preprocess data and create features
def preprocess_data(df):
    df['Price_Up'] = df['Close'] < df['Close'].shift(-1)
    df['Price_Up'] = df['Price_Up'].astype(int)
    return df

# Function to build and train a logistic regression model
def build_logistic_regression_model(X_train, y_train):
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
    
    # Select features and target
    X = df[['Open', 'High', 'Low', 'Volume']]
    y = df['Price_Up']
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Build and train the logistic regression model
    model = build_logistic_regression_model(X_train, y_train)
    
    # Model evaluation
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    st.write("## Model Evaluation")
    st.write(f"Accuracy: {accuracy:.2f}")
    
    st.write("## Classification Report")
    st.write(classification_report(y_test, y_pred))
    
    st.write("## Confusion Matrix")
    cm = confusion_matrix(y_test, y_pred)
    st.write(cm)
    
    # Visualize confusion matrix
    st.write("### Confusion Matrix Heatmap")
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, cmap="Blues", fmt="d")
    st.pyplot()
    
    # Visualize stock price data
    st.write("## SPY Stock Price Data")
    st.line_chart(df['Close'])
    
    # Visualize the logistic regression model's predictions
    st.write("## Model Predictions vs. Actual")
    predictions = model.predict(X)
    df['Predicted_Up'] = predictions
    st.line_chart(df[['Price_Up', 'Predicted_Up']])
    
if __name__ == "__main__":
    main()
