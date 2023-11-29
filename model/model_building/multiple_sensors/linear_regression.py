import os
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
import joblib

datasets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "calls", "multiple_sensors", "datasets")

training_data_path = os.path.join(datasets_dir, "wekeo_data.csv")
target_data_path = os.path.join(datasets_dir, "openAQ_data.csv")
merged_data_path = os.path.join(datasets_dir, "merged_data.csv")

training_data = pd.read_csv(training_data_path)
target_data = pd.read_csv(target_data_path)

merged_data = pd.merge(training_data, target_data, on="local_date", how="inner")
merged_data = merged_data.dropna()
merged_data.drop("Unnamed: 0_x", axis=1   , inplace=True)
merged_data.drop("Unnamed: 0_y", axis=1   , inplace=True)
merged_data.to_csv(merged_data_path, index=False)
merged_data.drop("local_date", axis=1, inplace=True)


best_combinations = {
    "pm10": ["pm25_x", "pm25_y", "pm10_y", "no2_x", "no2_y", "so2_x", "so2_y", "co"],
    "pm25": ["pm10_x", "pm10_y", "pm25_y", "no2_x", "no2_y", "so2_y"],
    "no2": ["pm25_x", "pm25_y", "no2_x", "no2_y", "so2_y", "co"],
    "so2": ["no2_x", "no2_y", "co"],
    "co": ["pm25_x", "pm25_y", "no2_x", "no2_y", "so2_y"]
}

filename = ""

target_variable = input("enter the target variable (pm25, pm10, no2): ")

if target_variable == "pm25":
    merged_data = merged_data[best_combinations["pm25"]]
elif target_variable == "pm10":
    merged_data = merged_data[best_combinations["pm10"]]
elif target_variable == "no2":
    merged_data = merged_data[best_combinations["no2"]]

target_variable = target_variable + "_y"

X = merged_data.drop(target_variable, axis=1)
Y = merged_data[target_variable]


X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.3, random_state=42
)
model = LinearRegression()
model.fit(X_train, Y_train)

current_dir = os.path.dirname(os.path.abspath(__file__))
saved_models_dir = os.path.join(current_dir, "saved_models")
if not os.path.exists(saved_models_dir):
    os.makedirs(saved_models_dir)

if target_variable == "pm25_y":
    filename = "linear_model_pm25.sav"
elif target_variable == "pm10_y":
    filename = "linear_model_pm10.sav"
elif target_variable == "no2_y":
    filename = "linear_model_no2.sav"

joblib.dump(model, os.path.join(saved_models_dir, filename))

loaded_model = joblib.load(os.path.join(saved_models_dir, filename))
predictions = loaded_model.predict(X_test)

training_accuracy = model.score(X_train, Y_train)
print("training_accuracy is: ", training_accuracy)
print("test_accuracy is: ", model.score(X_test, Y_test))
print("mean_squared_error : ", mean_squared_error(Y_test, predictions))
print("mean_absolute_error : ", mean_absolute_error(Y_test, predictions))
