import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns 
import joblib

training_data = pd.read_csv("model\calls\datasets\wekeo_data.csv")
target_data = pd.read_csv("model\calls\datasets\openAQ_data.csv")
merged_data = pd.merge(training_data, target_data, on='local_date', how='inner')
merged_data.drop("local_date", axis=1, inplace=True)


print("=======training data=======")
print(training_data.head())
print(training_data.columns)

print("=======target data=======")
print(target_data.head())
print(target_data.columns)  

print("=======merged data=======")
print(merged_data.head())
print(merged_data.columns)  

target_variable = input("enter the target variable (pm25_y, pm10_x, no2_x): ")

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
#pearplot
training_accuracy = model.score(X_train,Y_train)
print("training_accuracy is: ",training_accuracy)
print("test_accuracy is: ",model.score(X_test,Y_test))
print('mean_squared_error : ', mean_squared_error(Y_test, predictions)) 
print('mean_absolute_error : ', mean_absolute_error(Y_test, predictions)) 

plt.figure(figsize=(8, 6))
sns.regplot(x=Y_test, y=predictions, scatter_kws={'color':'blue'}, line_kws={'color':'orange'})
plt.xlabel(f'actual {target_variable} values')
plt.ylabel(f'predicted {target_variable} Values')
plt.title('regression Line')
plt.show()