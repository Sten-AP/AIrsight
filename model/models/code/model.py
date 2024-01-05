import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import joblib
import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from scipy import stats


def merge_and_train():
    datasets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "datasets",)
    model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "saved_models",)
    training_data_path = os.path.join(datasets_dir, "wekeo_data.csv")
    target_data_path = os.path.join(datasets_dir, "openAQ_data.csv")

    training_data = pd.read_csv(training_data_path)
    target_data = pd.read_csv(target_data_path)

    training_data['local_date'] = pd.to_datetime(training_data['local_date'], utc=True)
    target_data['local_date'] = pd.to_datetime(target_data['local_date'], utc=True)
    training_data['sensor_id'] = training_data['sensor_id'].astype(int)
    target_data['sensor_id'] = target_data['sensor_id'].astype(int)
    #timezone differences
    training_data['local_date'] = training_data['local_date'].dt.tz_convert('UTC')
    target_data['local_date'] = target_data['local_date'].dt.tz_convert('UTC')
    #merging the two datasets
    merged_data = pd.merge(training_data, target_data, left_on=['local_date', 'sensor_id'], right_on=['local_date', 'sensor_id'], how='inner')
    merged_data = merged_data.sort_values(by=["sensor_id", "local_date"])
    merged_data_path = os.path.join(datasets_dir, "merged_data.csv")
    merged_data = merged_data.dropna()
    merged_data['local_date'] = pd.to_datetime(merged_data['local_date'])

    Q1 = merged_data.quantile(0.25)
    Q3 = merged_data.quantile(0.75)
    IQR = Q3 - Q1

    merged_data = merged_data[~((merged_data < (Q1 - 1.5 * IQR)) | (merged_data > (Q3 + 1.5 * IQR))).any(axis=1)]

    # Create new time-based features
    merged_data['hour'] = merged_data['local_date'].dt.hour
    merged_data['day_of_week'] = merged_data['local_date'].dt.dayofweek
    merged_data['month'] = merged_data['local_date'].dt.month

    # Create sine and cosine features for time-based features
    merged_data['hour_sin'] = np.sin(2 * np.pi * merged_data['hour']/24)
    merged_data['hour_cos'] = np.cos(2 * np.pi * merged_data['hour']/24)
    merged_data['day_of_week_sin'] = np.sin(2 * np.pi * merged_data['day_of_week']/7)
    merged_data['day_of_week_cos'] = np.cos(2 * np.pi * merged_data['day_of_week']/7)
    merged_data['month_sin'] = np.sin(2 * np.pi * merged_data['month']/12)
    merged_data['month_cos'] = np.cos(2 * np.pi * merged_data['month']/12)
    merged_data.drop(['hour', 'day_of_week', 'month'], axis=1, inplace=True)
    merged_data.to_csv(merged_data_path, index=False)
    merged_data.drop(['local_date'], axis=1, inplace=True)

    target_variable = input("Please enter the target variable you want to predict (pm10, pm25, no2): ")
    if (target_variable != "pm10" and target_variable != "pm25" and target_variable != "no2") :
        print("Please enter a valid target variable")
        target_variable = input("Please enter the target variable you want to predict (pm10, pm25, no2): ")
    if (target_variable == "pm10"):
        X = merged_data[["pm25_x", "pm10_x", "no2_x", "so2", "co_conc", "hour_sin","hour_cos","day_of_week_sin","day_of_week_cos","month_sin","month_cos"]]
    if (target_variable == "pm25"):
        X = merged_data[["pm10_x","pm25_x","no2_x","so2", "co_conc","hour_sin","hour_cos","day_of_week_sin","day_of_week_cos","month_sin","month_cos"]]
    if (target_variable == "no2"):
        X = merged_data[["pm10_x","pm25_x","no2_x","so2", "co_conc","hour_sin","hour_cos","day_of_week_sin","day_of_week_cos","month_sin","month_cos"]]
    Y = merged_data[target_variable + "_y"]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3)

    model = LinearRegression()
    model.fit(X_train, Y_train)
    predictions = model.predict(X_test)

    training_accuracy = model.score(X_train, Y_train)
    print("training_r2_score is: ", training_accuracy)
    print("test_r2_score is: ", model.score(X_test, Y_test))
    print("mean_squared_error : ", mean_squared_error(Y_test, predictions))
    print("mean_absolute_error : ", mean_absolute_error(Y_test, predictions))

    save = input("Do you want to save the model? (yes/no): ")
    if save.lower() == "yes":
        model_path = os.path.join(model_dir, f"linear_regression_{target_variable}.joblib")
        joblib.dump(model, model_path)
        print(f"Model saved as linear_regression_{target_variable}")

    plot = input("Do you want to plot the model? (yes/no): ")
    if plot.lower() == "yes":
        plt.figure(figsize=(8, 6))
        sns.regplot(x=Y_test, y=predictions, scatter_kws={'color':'blue'}, line_kws={'color':'orange'})
        plt.xlabel(f'actual {target_variable} values')
        plt.ylabel(f'predicted {target_variable} Values')
        plt.title('regression Line')
        plt.show()
        print(merged_data.describe())
        sns.pairplot(merged_data)
        plt.show()

