from datetime import datetime
import os
import pandas as pd
import numpy as np
import joblib

model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "saved_models")
model_file = os.path.join(model_dir, 'linear_regression_pm10.joblib')
model = joblib.load(model_file)
# data orginates from wekeo call on 2023-12-02T13:00:00+00:00 and the lat and long from sensor: 4878
date_string = "2023-12-02T13:00:00+00:00"
date = datetime.fromisoformat(date_string.replace("Z", "+00:00"))

data = {
    "pm25_x": [32.781418],
    "pm10_x": [40.440094],
    "no2_x": [30.342562],
    "so2": [9.82618],
    "co_conc": [492.08505],
    "hour_sin": [np.sin(2 * np.pi * date.hour/24)],
    "hour_cos": [np.cos(2 * np.pi * date.hour/24)],
    "day_of_week_sin": [np.sin(2 * np.pi * date.weekday()/7)],
    "day_of_week_cos": [np.cos(2 * np.pi * date.weekday()/7)],
    "month_sin": [np.sin(2 * np.pi * date.month/12)],
    "month_cos": [np.cos(2 * np.pi * date.month/12)]
}

X_test = pd.DataFrame(data)

prediction = model.predict(X_test)

print(prediction)

