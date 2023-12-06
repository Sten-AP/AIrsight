import os
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
import joblib
from scipy import stats
import numpy as np

datasets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "calls", "multiple_sensors", "datasets")

training_data_path = os.path.join(datasets_dir, "wekeo_data.csv")
target_data_path = os.path.join(datasets_dir, "openAQ_data.csv")

training_data = pd.read_csv(training_data_path)
target_data = pd.read_csv(target_data_path)

merged_data = pd.merge(training_data, target_data, on="local_date", how="inner")

# Drop unnecessary columns
merged_data.drop(["Unnamed: 0_x", "Unnamed: 0_y", "local_date"], axis=1, inplace=True)

# Handle missing values
merged_data = merged_data.dropna()

target_variable = "pm10"

# Perform feature selection
# Here, I'm assuming that "pm25_x" and "pm10_x" are the most relevant features for predicting "pm10_y"
# You should replace these with the actual most relevant features based on your domain knowledge
X = merged_data[["pm25_x", "pm10_x"]]
Y = merged_data[target_variable + "_y"]

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

model = LinearRegression()
model.fit(X_train, Y_train)
predictions = model.predict(X_test)

training_accuracy = model.score(X_train, Y_train)
print("training_accuracy is: ", training_accuracy)
print("test_accuracy is: ", model.score(X_test, Y_test))
print("mean_squared_error : ", mean_squared_error(Y_test, predictions))
print("mean_absolute_error : ", mean_absolute_error(Y_test, predictions))