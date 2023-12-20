import os
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
import joblib
from scipy import stats
import numpy as np

def merge_and_train():
    datasets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "datasets",)
    training_data_path = os.path.join(datasets_dir, "wekeo_data.csv")
    target_data_path = os.path.join(datasets_dir, "openAQ_data.csv")

    training_data = pd.read_csv(training_data_path)
    target_data = pd.read_csv(target_data_path)

    training_data['local_date'] = pd.to_datetime(training_data['local_date'])
    target_data['local_date'] = pd.to_datetime(target_data['local_date'])
    training_data['sensor_id'] = training_data['sensor_id'].astype(int)
    target_data['sensor_id'] = target_data['sensor_id'].astype(int)

    #merging the two datasets
    merged_data = pd.merge(training_data, target_data, left_on=['local_date', 'sensor_id'], right_on=['local_date', 'sensor_id'], how='inner')
    merged_data = merged_data.sort_values(by=["sensor_id", "local_date"])
    merged_data_path = os.path.join(datasets_dir, "merged_data.csv")
    merged_data.to_csv(merged_data_path, index=False)
    merged_data.drop(["local_date"], axis=1, inplace=True)
    merged_data = merged_data.dropna()

    target_variable = "pm10"

    X = merged_data[["pm25_x", "pm10_x", "no2_x", "so2", "co_conc", "time_x"]]
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