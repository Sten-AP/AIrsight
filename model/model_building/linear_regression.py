import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

training_data = pd.read_csv("model\calls\datasets\wekeo_data.csv")
target_data = pd.read_csv("model\calls\datasets\openAQ_data.csv")
target_variable = "pm10"

model = LinearRegression()

model.fit(training_data[["time"]], target_data[target_variable])

predictions = model.predict(target_data[["time"]])

target_data["predicted_" + target_variable] = predictions

plt.scatter(training_data["time"], training_data[target_variable], label="training Data", color="blue")
plt.scatter(target_data["time"], target_data[target_variable], label="actual Target Data", color="green")
plt.plot(target_data["time"], predictions, label="predicted Target Data", color="red")
plt.xlabel("time")
plt.ylabel(target_variable)
plt.legend()
plt.title(f"linear Regression for {target_variable}")
plt.show()