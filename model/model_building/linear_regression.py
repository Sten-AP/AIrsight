import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

training_data = pd.read_csv('../calls/datasets/wekeo_data.csv')
target_data = pd.read_csv('../calls/datasets/openAQ_data.csv')

#training_data.drop("time", axis=1, inplace=True)


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



X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=41)
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
print('r2_score : ', r2_score(Y_test, predictions))

plt.figure(figsize=(8, 6))
sns.regplot(x=Y_test, y=predictions, scatter_kws={'color':'blue'}, line_kws={'color':'orange'})
plt.xlabel(f'actual {target_variable} values')
plt.ylabel(f'predicted {target_variable} Values')
plt.title('regression Line')
plt.show()

from sklearn2pmml import PMMLPipeline, sklearn2pmml
# package iris classifier model with PMML
sklearn2pmml(PMMLPipeline([("estimator",
                        	model)]),
         	"iris_model.pmml",
         	with_repr=True)