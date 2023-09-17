import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from sklearn.model_selection import train_test_split

# Load the SPY data
spy_data = pd.DataFrame(yf.download('SPY', '2015-01-01', '2023-09-16'))

# Preprocess the data
# Create a dummy variable for the direction of the market
spy_data['direction'] = spy_data['Close'].pct_change()
spy_data['direction'] = spy_data['direction'].apply(lambda x: 1 if x > 0 else 0)

# Create a list of features
features = ['Close', 'Open', 'High', 'Low', 'Volume']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(spy_data[features], spy_data['direction'], test_size=0.25, random_state=42)

# Create multiple logistic regression models
# Create a list of models
models = []
for i in range(10):
    model = LogisticRegression()
    model.fit(X_train, y_train)
    models.append(model)

# Evaluate the models
# Calculate the accuracy of each model on the test set
accuracies = []
for model in models:
    accuracy = model.score(X_test, y_test)
    accuracies.append(accuracy)

# Print the accuracy of each model
for i in range(len(models)):
    print(f'Model {i+1} accuracy: {accuracies[i]}')

# Plot the results using streamlit
# Create a streamlit app
st.title('Multiple Logic Regression Models for SPY')

# Create a dropdown menu to select the model
model_index = st.selectbox('Select model:', range(len(models)))

# Calculate the predictions for the selected model
predictions = models[model_index].predict(X_test)

# Plot the predictions vs. the actual values
plt.figure(figsize=(10, 6))
plt.scatter(X_test['Close'], predictions, c='blue', label='Predictions')
plt.scatter(X_test['Close'], y_test, c='red', label='Actual')
plt.xlabel('Close')
plt.ylabel('Direction')
plt.legend()
st.pyplot(plt)

# Calculate the confusion matrix for the selected model
confusion_matrix = pd.crosstab(y_test, predictions, rownames=['Actual'], colnames=['Predicted'])
st.dataframe(confusion_matrix)

