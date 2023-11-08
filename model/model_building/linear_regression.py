import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns 


training_data = pd.read_csv("model\calls\datasets\wekeo_data.csv")
target_data = pd.read_csv("model\calls\datasets\openAQ_data.csv")


training_data.drop("time", axis=1, inplace=True)

print("=======training data=======")
print(training_data.head())
print(training_data.columns)

print("=======target data=======")
print(target_data.head())
print(target_data.columns)  

target_variable = "pm10"

X =  training_data
Y = target_data[target_variable]

print("=======X=======")
print(X)
print("=======Y=======")
print(Y)

sns.scatterplot(x='pm10', 
                y='pm10', data=training_data) 

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
model = LinearRegression()

model.fit(X_train, Y_train)
  
predictions = model.predict(X_test) 
  
print('mean_squared_error : ', mean_squared_error(Y_test, predictions)) 
print('mean_absolute_error : ', mean_absolute_error(Y_test, predictions)) 

plt.figure(figsize=(8, 6))
sns.regplot(x=Y_test, y=predictions, color='blue')
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Actual vs. Predicted Values with Regression Line')
plt.show()