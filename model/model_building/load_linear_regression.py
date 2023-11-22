import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split
import joblib

training_data = pd.read_csv('../calls/datasets/wekeo_data.csv')
target_data = pd.read_csv('../calls/datasets/openAQ_data.csv')
filename = 'linear_model_2.sav'

print("=======training data=======")
print(training_data.head())
print(training_data.columns)

print("=======target data=======")
print(target_data.head())
print(target_data.columns)

target_variable = "pm10"

X = training_data
Y = target_data[target_variable]

print("=======X=======")
print(X)
print("=======Y=======")
print(Y)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=41)

# load the model
load_model = joblib.load(open(filename, 'rb'))

y_pred = load_model.predict(X_test)
print('root mean squared error : ', np.sqrt(
    metrics.mean_squared_error(Y_test, y_pred)))
training_accuracy = load_model.score(X_train, Y_train)
print("training_accuracy is: ", training_accuracy)