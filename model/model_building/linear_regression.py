import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
import joblib

training_data = pd.read_csv("model\calls\datasets\wekeo_data.csv")
target_data = pd.read_csv("model\calls\datasets\openAQ_data.csv")
merged_data = pd.merge(training_data, target_data, on='local_date', how='inner')
merged_data.drop("local_date", axis=1, inplace=True)

best_combinations = {
    "pm10": ["pm25_x", "pm25_y","pm10_x", "pm10_y", "no2_x", "no2_y", "so2", "co_conc", "nmvoc"],
    "pm25": ['pm10_x', 'pm10_y', 'pm25_x', 'pm25_y', 'time_x', 'time_y', 'no2_x', 'no2_y', 'so2', 'nmvoc'],
    "no2": ["pm25_x", "pm25_y", "no2_x", "no2_y", "so2", "nmvoc", "co_conc"],
    "o3": ["time"],
    "so2": ["no2_x", "no2_y", "co_conc", "nmvoc", "no"],
    "co": ["pm25_x","pm25_y", "no2_x", "no2_y", "so2", "nmvoc", "no"],
    "nmvoc": ["pm25_x", "pm25_y", "no2_x", "no2_y", "so2", "co_conc", "no"],
    "no": ["pm25_x", "pm25_y","no2_x", "no2_y", "so2", "co_conc", "nmvoc"]
}

print("=======training data=======")
print(training_data.head())
print(training_data.columns)

print("=======target data=======")
print(target_data.head())
print(target_data.columns)

print("=======merged data=======")
print(merged_data.head())
print(merged_data.columns)  

target_variable = input("enter the target variable (pm25, pm10, no2): ")

if (target_variable == "pm25_y"):
    merged_data= merged_data[best_combinations["pm25"]]
elif (target_variable == "pm10_y"):
    merged_data= merged_data[best_combinations["pm10"]]
elif (target_variable == "no2_y"):
    merged_data= merged_data[best_combinations["no2"]]

X = merged_data.drop(target_variable, axis=1)
Y = merged_data[target_variable]

print("=======X=======")
print(X)
print("=======Y=======")
print(Y)



X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=42)
model = LinearRegression()
model.fit(X_train, Y_train)
predictions = model.predict(X_test)

print("=======predictions=======")
print(predictions)
print("=======Y_test=======")
print(Y_test)
training_accuracy = model.score(X_train,Y_train)
print("training_accuracy is: ",training_accuracy)
print("test_accuracy is: ",model.score(X_test,Y_test))
print('mean_squared_error : ', mean_squared_error(Y_test, predictions)) 
print('mean_absolute_error : ', mean_absolute_error(Y_test, predictions)) 

filename = 'linear_model_2.sav'
joblib.dump(model, open(filename, 'wb'))